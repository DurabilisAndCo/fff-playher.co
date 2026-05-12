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

    # Alias columns expected by analyse.py / accueil.py
    df['france_score'] = df['goals_scored']
    df['opponent_score'] = df['goals_conceded']

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


def get_performance_by_opponent(df, min_matches=1):
    """
    Returns a DataFrame with win/draw/loss stats grouped by opponent.
    Only includes opponents with at least min_matches games.
    """
    if df is None or len(df) == 0:
        return pd.DataFrame()

    records = []
    for opponent, group in df.groupby('opponent'):
        total = len(group)
        if total < min_matches:
            continue
        wins = (group['result'] == 'Victoire').sum()
        draws = (group['result'] == 'Nul').sum()
        losses = (group['result'] == 'Défaite').sum()
        records.append({
            'opponent': opponent,
            'matches_played': total,       # alias used by analyse.py
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


def calculate_trend_metrics(df, window=5):
    """
    Returns a DataFrame with per-match trend data used by insights.py.
    Columns: date, result, points, rolling_points (rolling average of points).

    Points system: Victoire=3, Nul=1, Défaite=0.
    The window parameter controls the rolling average window size.
    """
    if df is None or len(df) == 0:
        return pd.DataFrame(columns=['date', 'result', 'points', 'rolling_points'])

    df_sorted = df.sort_values('date').copy()

    # Points per match (football scoring system)
    def match_points(result):
        if result == 'Victoire':
            return 3
        elif result == 'Nul':
            return 1
        return 0

    df_sorted['points'] = df_sorted['result'].apply(match_points)
    df_sorted['rolling_points'] = (
        df_sorted['points'].rolling(window, min_periods=1).mean()
    )

    # Keep all original columns + derived ones so caller can access 'result', 'date', etc.
    return df_sorted.reset_index(drop=True)
