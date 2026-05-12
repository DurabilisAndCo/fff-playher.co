"""
Data processing utilities for FFF Dashboard.
Handles loading, cleaning, and computing metrics from match data.
"""

import pandas as pd
import numpy as np
from datetime import datetime


def load_and_process_data():
    """
    Load and process the France women's matches CSV.
    Returns a cleaned DataFrame with derived columns.
    """
    try:
        df = pd.read_csv('france_matches.csv')
    except FileNotFoundError:
        try:
            df = pd.read_csv('data/france_matches.csv')
        except FileNotFoundError:
            raise FileNotFoundError("Fichier france_matches.csv introuvable.")

    # Parse dates
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    # Normalize team names to lowercase for matching
    df['home_team'] = df['home_team'].str.lower().str.strip()
    df['away_team'] = df['away_team'].str.lower().str.strip()

    # Determine if France is home or away
    df['is_home'] = df['home_team'] == 'france'

    # Goals scored and conceded from France's perspective
    df['goals_scored'] = np.where(df['is_home'], df['home_score'], df['away_score'])
    df['goals_conceded'] = np.where(df['is_home'], df['away_score'], df['home_score'])
    df['goal_difference'] = df['goals_scored'] - df['goals_conceded']

    # Determine result
    def get_result(row):
        if row['goals_scored'] > row['goals_conceded']:
            return 'Victoire'
        elif row['goals_scored'] < row['goals_conceded']:
            return 'Défaite'
        else:
            return 'Nul'

    df['result'] = df.apply(get_result, axis=1)

    # Opponent name
    df['opponent'] = np.where(df['is_home'], df['away_team'], df['home_team'])
    df['opponent'] = df['opponent'].str.title()

    # Location label
    df['location'] = np.where(
        df['neutral'].astype(str).str.lower() == 'true',
        'Neutre',
        np.where(df['is_home'], 'Domicile', 'Extérieur')
    )

    return df.sort_values('date').reset_index(drop=True)


def filter_data_by_period(df, start_year, end_year):
    """Return rows within [start_year, end_year] inclusive."""
    return df[(df['year'] >= start_year) & (df['year'] <= end_year)].copy()


def calculate_performance_metrics(df):
    """
    Compute a dict of KPI metrics from a DataFrame of matches.
    """
    if df is None or len(df) == 0:
        return {
            'total_matches': 0,
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'win_rate': 0.0,
            'draw_rate': 0.0,
            'loss_rate': 0.0,
            'avg_goals_scored': 0.0,
            'avg_goals_conceded': 0.0,
            'avg_goal_difference': 0.0,
            'goal_difference_total': 0,
            'clean_sheets': 0,
            'big_wins': 0,
        }

    total = len(df)
    wins = len(df[df['result'] == 'Victoire'])
    draws = len(df[df['result'] == 'Nul'])
    losses = len(df[df['result'] == 'Défaite'])

    return {
        'total_matches': total,
        'wins': wins,
        'draws': draws,
        'losses': losses,
        'win_rate': (wins / total) * 100 if total > 0 else 0.0,
        'draw_rate': (draws / total) * 100 if total > 0 else 0.0,
        'loss_rate': (losses / total) * 100 if total > 0 else 0.0,
        'avg_goals_scored': df['goals_scored'].mean() if total > 0 else 0.0,
        'avg_goals_conceded': df['goals_conceded'].mean() if total > 0 else 0.0,
        'avg_goal_difference': df['goal_difference'].mean() if total > 0 else 0.0,
        'goal_difference_total': int(df['goal_difference'].sum()),
        'clean_sheets': int((df['goals_conceded'] == 0).sum()),
        'big_wins': int(((df['result'] == 'Victoire') & (df['goal_difference'] >= 3)).sum()),
    }


def calculate_home_advantage(df):
    """
    Returns the difference in win rate: home win % minus away win %.
    Positive values mean France performs better at home.
    """
    home_matches = df[df['location'] == 'Domicile']
    away_matches = df[df['location'] == 'Extérieur']

    home_win_rate = (
        (home_matches['result'] == 'Victoire').sum() / len(home_matches) * 100
        if len(home_matches) > 0 else 0.0
    )
    away_win_rate = (
        (away_matches['result'] == 'Victoire').sum() / len(away_matches) * 100
        if len(away_matches) > 0 else 0.0
    )

    return home_win_rate - away_win_rate


def get_performance_by_opponent(df):
    """
    Returns a DataFrame with win/draw/loss stats grouped by opponent.
    """
    if df is None or len(df) == 0:
        return pd.DataFrame()

    records = []
    for opponent, group in df.groupby('opponent'):
        total = len(group)
        wins = (group['result'] == 'Victoire').sum()
        draws = (group['result'] == 'Nul').sum()
        losses = (group['result'] == 'Défaite').sum()
        records.append({
            'opponent': opponent,
            'total_matches': total,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'win_rate': round((wins / total) * 100, 1) if total > 0 else 0.0,
            'avg_goals_scored': round(group['goals_scored'].mean(), 2),
            'avg_goals_conceded': round(group['goals_conceded'].mean(), 2),
            'goal_difference': int(group['goal_difference'].sum()),
        })

    return pd.DataFrame(records).sort_values('win_rate', ascending=False).reset_index(drop=True)


def calculate_trend_metrics(df):
    """
    Returns rolling/trend metrics to identify form over time.
    """
    if df is None or len(df) == 0:
        return {}

    df_sorted = df.sort_values('date').copy()
    df_sorted['win_flag'] = (df_sorted['result'] == 'Victoire').astype(int)

    # Rolling 5-match win rate
    df_sorted['rolling_win_rate_5'] = df_sorted['win_flag'].rolling(5, min_periods=1).mean() * 100
    df_sorted['rolling_goals_scored_5'] = df_sorted['goals_scored'].rolling(5, min_periods=1).mean()
    df_sorted['rolling_goals_conceded_5'] = df_sorted['goals_conceded'].rolling(5, min_periods=1).mean()

    # Current streak
    streak = 0
    streak_type = None
    for result in reversed(df_sorted['result'].tolist()):
        if streak_type is None:
            streak_type = result
        if result == streak_type:
            streak += 1
        else:
            break

    # Last 5 and 10 match performance
    last_5 = df_sorted.tail(5)
    last_10 = df_sorted.tail(10)

    return {
        'current_streak': streak,
        'current_streak_type': streak_type,
        'last_5_win_rate': (last_5['result'] == 'Victoire').mean() * 100 if len(last_5) > 0 else 0,
        'last_10_win_rate': (last_10['result'] == 'Victoire').mean() * 100 if len(last_10) > 0 else 0,
        'trend_data': df_sorted[['date', 'rolling_win_rate_5', 'rolling_goals_scored_5', 'rolling_goals_conceded_5']],
        'best_year': int(df_sorted.groupby('year')['win_flag'].mean().idxmax()) if len(df_sorted) > 0 else None,
    }
