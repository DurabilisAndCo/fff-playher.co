import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_processing import calculate_performance_metrics, calculate_home_advantage
from utils.visualizations import create_performance_evolution, create_momentum_chart

def show_accueil(filtered_data, france_data):
    """
    Page d'accueil avec vue d'ensemble et KPIs principaux
    """
    st.title("🏠 Tableau de Bord - Vue d'Ensemble")
    
    # Calcul des métriques pour la période filtrée et complète
    current_metrics = calculate_performance_metrics(filtered_data)
    historical_metrics = calculate_performance_metrics(france_data)
    
    # Section KPIs principaux
    st.markdown("### 📊 Indicateurs Clés de Performance")
    
    # Création de 4 colonnes pour les KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_wins = current_metrics.get('win_rate', 0) - historical_metrics.get('win_rate', 0)
        st.metric(
            label="🏆 Taux de Victoire",
            value=f"{current_metrics.get('win_rate', 0):.1f}%",
            delta=f"{delta_wins:.1f}%"
        )
    
    with col2:
        delta_goals = current_metrics.get('avg_goals_scored', 0) - historical_metrics.get('avg_goals_scored', 0)
        st.metric(
            label="⚽ Buts/Match (Marqués)",
            value=f"{current_metrics.get('avg_goals_scored', 0):.2f}",
            delta=f"{delta_goals:.2f}"
        )
    
    with col3:
        delta_conceded = historical_metrics.get('avg_goals_conceded', 0) - current_metrics.get('avg_goals_conceded', 0)
        st.metric(
            label="🛡️ Buts/Match (Encaissés)",
            value=f"{current_metrics.get('avg_goals_conceded', 0):.2f}",
            delta=f"{delta_conceded:.2f}",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="📅 Matchs Analysés",
            value=f"{current_metrics.get('total_matches', 0)}",
            delta=f"Total: {historical_metrics.get('total_matches', 0)}"
        )
    
    # Deuxième ligne de KPIs
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        home_advantage = calculate_home_advantage(filtered_data)
        st.metric(
            label="🏠 Avantage Domicile",
            value=f"{home_advantage:.1f}%",
            help="Différence entre % victoires à domicile et à l'extérieur"
        )
    
    with col6:
        clean_sheets_rate = (current_metrics.get('clean_sheets', 0) / current_metrics.get('total_matches', 1)) * 100
        st.metric(
            label="🥅 Clean Sheets",
            value=f"{clean_sheets_rate:.1f}%",
            delta=f"{current_metrics.get('clean_sheets', 0)} matchs"
        )
    
    with col7:
        big_wins_rate = (current_metrics.get('big_wins', 0) / current_metrics.get('total_matches', 1)) * 100
        st.metric(
            label="🚀 Larges Victoires",
            value=f"{big_wins_rate:.1f}%",
            delta=f"{current_metrics.get('big_wins', 0)} matchs",
            help="Victoires par 3+ buts d'écart"
        )
    
    with col8:
        goal_diff_total = current_metrics.get('goal_difference_total', 0)
        st.metric(
            label="📈 Diff. Buts Totale",
            value=f"{goal_diff_total:+d}",
            delta=f"{current_metrics.get('avg_goal_difference', 0):.2f}/match"
        )
    
    st.markdown("---")
    
    # Section graphiques principaux
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### 📈 Évolution des Performances")
        if len(filtered_data) > 0:
            evolution_chart = create_performance_evolution(filtered_data)
            st.plotly_chart(evolution_chart, use_container_width=True)
        else:
            st.warning("Aucune donnée disponible pour la période sélectionnée")
    
    with col_right:
        st.markdown("### 🎯 Répartition des Résultats")
        
        # Graphique en secteurs des résultats
        result_counts = filtered_data['result'].value_counts()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=result_counts.index,
            values=result_counts.values,
            hole=.3,
            marker_colors=['#28a745', '#dc3545', '#ffc107']
        )])
        
        fig_pie.update_layout(
            title="Distribution des Résultats",
            height=400,
            template="plotly_white"
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Statistiques détaillées
        st.markdown("**Détails:**")
        for result, count in result_counts.items():
            percentage = (count / len(filtered_data)) * 100
            st.write(f"• {result}: {count} ({percentage:.1f}%)")
    
    st.markdown("---")
    
    # Section analyse temporelle
    st.markdown("### ⏱️ Analyse du Momentum")
    
    if len(filtered_data) >= 10:  # Minimum de données pour le momentum
        momentum_chart = create_momentum_chart(filtered_data)
        st.plotly_chart(momentum_chart, use_container_width=True)
        
        # Analyse textuelle du momentum
        last_10_matches = filtered_data.sort_values('date').tail(10)
        recent_wins = len(last_10_matches[last_10_matches['result'] == 'Victoire'])
        recent_win_rate = (recent_wins / 10) * 100
        
        col_momentum1, col_momentum2 = st.columns(2)
        
        with col_momentum1:
            st.markdown("#### 📊 Forme Récente (10 derniers matchs)")
            if recent_win_rate >= 60:
                st.success(f"✅ Excellente forme: {recent_wins}/10 victoires ({recent_win_rate:.0f}%)")
            elif recent_win_rate >= 40:
                st.info(f"🔄 Forme correcte: {recent_wins}/10 victoires ({recent_win_rate:.0f}%)")
            else:
                st.warning(f"⚠️ Forme à améliorer: {recent_wins}/10 victoires ({recent_win_rate:.0f}%)")
        
        with col_momentum2:
            st.markdown("#### 🎯 Performance vs Objectifs")
            target_win_rate = 50  # Objectif arbitraire
            current_rate = current_metrics.get('win_rate', 0)
            
            if current_rate >= target_win_rate:
                st.success(f"🎉 Objectif atteint! ({current_rate:.1f}% vs {target_win_rate}%)")
            else:
                gap = target_win_rate - current_rate
                st.info(f"📈 Écart à combler: {gap:.1f} points de %")
    
    else:
        st.info("⚠️ Données insuffisantes pour l'analyse du momentum (minimum 10 matchs)")
    
    # Section résumé exécutif
    st.markdown("---")
    st.markdown("### 📋 Résumé Exécutif")
    
    # Analyse automatique des tendances
    insights = []
    
    # Performance générale
    win_rate = current_metrics.get('win_rate', 0)
    if win_rate >= 60:
        insights.append("🟢 **Performance excellente** avec un taux de victoire supérieur à 60%")
    elif win_rate >= 40:
        insights.append("🟡 **Performance correcte** avec un taux de victoire modéré")
    else:
        insights.append("🔴 **Performance à améliorer** avec un taux de victoire inférieur à 40%")
    
    # Équilibre offensif/défensif
    goals_scored = current_metrics.get('avg_goals_scored', 0)
    goals_conceded = current_metrics.get('avg_goals_conceded', 0)
    
    if goals_scored > goals_conceded * 1.5:
        insights.append("⚽ **Profil offensif dominant** - Excellence dans la finition")
    elif goals_conceded < goals_scored * 0.7:
        insights.append("🛡️ **Solidité défensive remarquable** - Peu de buts encaissés")
    else:
        insights.append("⚖️ **Équilibre offensif-défensif** - Style de jeu polyvalent")
    
    # Avantage du terrain
    if home_advantage > 15:
        insights.append("🏠 **Fort avantage du terrain** - Performance nettement supérieure à domicile")
    elif home_advantage < -5:
        insights.append("✈️ **Meilleure performance à l'extérieur** - Caractère de battante")
    else:
        insights.append("🌍 **Performance stable** - Peu d'influence du lieu de jeu")
    
    # Affichage des insights
    for insight in insights:
        st.markdown(f"- {insight}")
    
    # Recommandations rapides
    st.markdown("#### 🎯 Recommandations Prioritaires")
    
    recommendations = []
    
    if win_rate < 50:
        recommendations.append("Analyser les défaites récurrentes pour identifier les axes d'amélioration")
    
    if goals_conceded > goals_scored:
        recommendations.append("Renforcer la solidité défensive - Priority #1")
    
    if goals_scored < 1.5:
        recommendations.append("Développer l'efficacité offensive devant le but")
    
    if home_advantage < 0:
        recommendations.append("Optimiser la préparation des matchs à domicile")
    
    if len(recommendations) == 0:
        recommendations.append("Maintenir le niveau actuel et préparer les prochains défis")
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"{i}. {rec}")
    
    # Données de contexte
    st.markdown("---")
    with st.expander("ℹ️ Informations sur les Données"):
        st.markdown(f"""
        **Période d'analyse:** {filtered_data['date'].min().strftime('%d/%m/%Y')} - {filtered_data['date'].max().strftime('%d/%m/%Y')}
        
        **Répartition par lieu:**
        - Domicile: {len(filtered_data[filtered_data['is_home'] == True])} matchs
        - Extérieur: {len(filtered_data[filtered_data['is_home'] == False])} matchs
        
        **Types de compétition:**
        """)
        
        for tournament, count in filtered_data['tournament'].value_counts().items():
            st.markdown(f"- {tournament}: {count} matchs")
        
        st.markdown(f"""
        
        **Méthodologie:**
        - Taux de victoire = (Victoires / Total matchs) × 100
        - Avantage domicile = % victoires domicile - % victoires extérieur
        - Clean sheets = Matchs sans but encaissé
        - Larges victoires = Victoires par 3+ buts d'écart
        """)
