"""
Visualization utilities for FFF Dashboard.
Creates Plotly charts used across the dashboard pages.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ─── Color palette (Durabilis & FFF) ──────────────────────────────────────────
COLORS = {
    'win': '#28a745',
    'draw': '#ffc107',
    'loss': '#dc3545',
    'primary': '#1970b4',
    'secondary': '#2ea9df',
    'dark': '#2d3381',
    'fff_blue': '#0055A4',
    'fff_red': '#EF4135',
}

TEMPLATE = 'plotly_white'


# ─── Performance evolution chart ──────────────────────────────────────────────
def create_performance_evolution(df):
    """
    Line chart showing yearly win rate and goal averages over time.
    """
    if df is None or len(df) == 0:
        return go.Figure()

    yearly = (
        df.groupby('year')
        .agg(
            matches=('result', 'count'),
            wins=('result', lambda x: (x == 'Victoire').sum()),
            goals_scored=('goals_scored', 'mean'),
            goals_conceded=('goals_conceded', 'mean'),
        )
        .reset_index()
    )
    yearly['win_rate'] = (yearly['wins'] / yearly['matches']) * 100

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=("Taux de Victoire (%)", "Buts Moyens par Match"),
        vertical_spacing=0.12,
    )

    fig.add_trace(
        go.Scatter(
            x=yearly['year'],
            y=yearly['win_rate'],
            mode='lines+markers',
            name='Taux de Victoire',
            line=dict(color=COLORS['primary'], width=3),
            marker=dict(size=8),
        ),
        row=1, col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=yearly['year'],
            y=yearly['goals_scored'],
            mode='lines+markers',
            name='Buts Marqués',
            line=dict(color=COLORS['win'], width=2),
            marker=dict(size=7),
        ),
        row=2, col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=yearly['year'],
            y=yearly['goals_conceded'],
            mode='lines+markers',
            name='Buts Encaissés',
            line=dict(color=COLORS['loss'], width=2, dash='dash'),
            marker=dict(size=7),
        ),
        row=2, col=1,
    )

    fig.update_layout(
        template=TEMPLATE,
        height=500,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hovermode='x unified',
    )
    fig.update_yaxes(title_text='%', row=1, col=1)
    fig.update_yaxes(title_text='Buts', row=2, col=1)

    return fig


# ─── Comparison charts ────────────────────────────────────────────────────────
def create_comparison_charts(df):
    """
    Bar chart comparing wins/draws/losses per year.
    """
    if df is None or len(df) == 0:
        return go.Figure()

    yearly = (
        df.groupby(['year', 'result'])
        .size()
        .reset_index(name='count')
    )

    fig = px.bar(
        yearly,
        x='year',
        y='count',
        color='result',
        color_discrete_map={
            'Victoire': COLORS['win'],
            'Nul': COLORS['draw'],
            'Défaite': COLORS['loss'],
        },
        barmode='stack',
        title='Résultats par Année',
        labels={'count': 'Nombre de matchs', 'year': 'Année', 'result': 'Résultat'},
        template=TEMPLATE,
    )
    fig.update_layout(height=400, legend_title='Résultat')
    return fig


# ─── Home advantage chart ─────────────────────────────────────────────────────
def create_home_advantage_chart(df):
    """
    Grouped bar chart comparing home vs away win rates.
    """
    if df is None or len(df) == 0:
        return go.Figure()

    location_stats = []
    for loc in ['Domicile', 'Extérieur', 'Neutre']:
        subset = df[df['location'] == loc]
        if len(subset) == 0:
            continue
        total = len(subset)
        wins = (subset['result'] == 'Victoire').sum()
        draws = (subset['result'] == 'Nul').sum()
        losses = (subset['result'] == 'Défaite').sum()
        location_stats.append({
            'location': loc,
            'Victoire': round((wins / total) * 100, 1),
            'Nul': round((draws / total) * 100, 1),
            'Défaite': round((losses / total) * 100, 1),
        })

    stats_df = pd.DataFrame(location_stats)

    fig = go.Figure()
    for result, color in [('Victoire', COLORS['win']), ('Nul', COLORS['draw']), ('Défaite', COLORS['loss'])]:
        if result in stats_df.columns:
            fig.add_trace(go.Bar(
                name=result,
                x=stats_df['location'],
                y=stats_df[result],
                marker_color=color,
                text=stats_df[result].apply(lambda v: f'{v:.1f}%'),
                textposition='auto',
            ))

    fig.update_layout(
        barmode='group',
        title="Performance selon le lieu de jeu",
        yaxis_title="Taux (%)",
        template=TEMPLATE,
        height=400,
        legend_title='Résultat',
    )
    return fig


# ─── Tournament performance chart ─────────────────────────────────────────────
def create_tournament_performance_chart(df):
    """
    Horizontal bar chart ranking tournaments by win rate.
    """
    if df is None or len(df) == 0:
        return go.Figure()

    tourn_stats = []
    for tournament, group in df.groupby('tournament'):
        total = len(group)
        if total < 2:
            continue
        wins = (group['result'] == 'Victoire').sum()
        tourn_stats.append({
            'tournament': tournament,
            'win_rate': round((wins / total) * 100, 1),
            'total_matches': total,
            'avg_goals': round(group['goals_scored'].mean(), 2),
        })

    if not tourn_stats:
        return go.Figure()

    stats_df = pd.DataFrame(tourn_stats).sort_values('win_rate')

    fig = go.Figure(go.Bar(
        x=stats_df['win_rate'],
        y=stats_df['tournament'],
        orientation='h',
        marker=dict(
            color=stats_df['win_rate'],
            colorscale=[[0, COLORS['loss']], [0.5, COLORS['draw']], [1, COLORS['win']]],
            showscale=False,
        ),
        text=stats_df['win_rate'].apply(lambda v: f'{v:.1f}%'),
        textposition='outside',
        customdata=stats_df['total_matches'],
        hovertemplate='%{y}<br>Taux de victoire: %{x:.1f}%<br>Matchs: %{customdata}<extra></extra>',
    ))

    fig.update_layout(
        title='Performance par Compétition',
        xaxis_title='Taux de Victoire (%)',
        template=TEMPLATE,
        height=max(300, len(stats_df) * 45),
        margin=dict(l=200),
    )
    return fig


# ─── Momentum chart ───────────────────────────────────────────────────────────
def create_momentum_chart(df):
    """
    Rolling 5-match win rate over time to visualise form momentum.
    """
    if df is None or len(df) < 5:
        return go.Figure()

    df_sorted = df.sort_values('date').copy()
    df_sorted['win_flag'] = (df_sorted['result'] == 'Victoire').astype(int)
    df_sorted['momentum'] = df_sorted['win_flag'].rolling(5, min_periods=1).mean() * 100

    # Background color bands
    fig = go.Figure()

    fig.add_hrect(y0=60, y1=100, fillcolor='rgba(40,167,69,0.08)', line_width=0, annotation_text='Excellente', annotation_position='top left')
    fig.add_hrect(y0=40, y1=60, fillcolor='rgba(255,193,7,0.08)', line_width=0, annotation_text='Correcte', annotation_position='top left')
    fig.add_hrect(y0=0, y1=40, fillcolor='rgba(220,53,69,0.08)', line_width=0, annotation_text='À améliorer', annotation_position='top left')

    fig.add_trace(go.Scatter(
        x=df_sorted['date'],
        y=df_sorted['momentum'],
        mode='lines',
        fill='tozeroy',
        fillcolor='rgba(25,112,180,0.15)',
        line=dict(color=COLORS['primary'], width=2.5),
        name='Momentum (5 matchs)',
        hovertemplate='%{x|%d/%m/%Y}<br>Momentum: %{y:.1f}%<extra></extra>',
    ))

    # Mark individual results
    color_map = {'Victoire': COLORS['win'], 'Nul': COLORS['draw'], 'Défaite': COLORS['loss']}
    for result in ['Victoire', 'Nul', 'Défaite']:
        subset = df_sorted[df_sorted['result'] == result]
        fig.add_trace(go.Scatter(
            x=subset['date'],
            y=subset['momentum'],
            mode='markers',
            marker=dict(color=color_map[result], size=7, symbol='circle'),
            name=result,
            hovertemplate='%{x|%d/%m/%Y}<br>' + result + '<extra></extra>',
        ))

    fig.update_layout(
        title='Momentum - Forme sur les 5 Derniers Matchs',
        xaxis_title='Date',
        yaxis_title='Taux de Victoire Glissant (%)',
        yaxis=dict(range=[0, 105]),
        template=TEMPLATE,
        height=400,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hovermode='x unified',
    )
    return fig
