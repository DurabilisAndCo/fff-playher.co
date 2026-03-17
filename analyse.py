import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_processing import get_performance_by_opponent, calculate_home_advantage
from utils.visualizations import create_comparison_charts, create_home_advantage_chart, create_tournament_performance_chart

def show_analyse(filtered_data, full_data):
    """
    Page d'analyse avec comparaisons internationales et facteurs de performance
    """
    st.title("📊 Analyse Approfondie")
    
    # Tabs pour organiser les analyses
    tab1, tab2, tab3 = st.tabs(["🌍 Comparaisons Internationales", "🏠 Facteurs de Performance", "🏆 Analyse par Compétition"])
    
    with tab1:
        st.markdown("### 🌍 Performance contre les Principales Nations")
        
        # Sélection des adversaires à analyser
        all_opponents = filtered_data['opponent'].value_counts()
        min_matches = st.slider("Nombre minimum de confrontations", 1, 10, 3)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Graphique de comparaison principal
            if len(filtered_data) > 0:
                comparison_chart = create_comparison_charts(filtered_data)
                st.plotly_chart(comparison_chart, use_container_width=True)
            else:
                st.warning("Aucune donnée disponible pour la période sélectionnée")
        
        with col2:
            st.markdown("#### 🎯 Top Adversaires")
            top_opponents = all_opponents.head(5)
            
            for opponent, matches in top_opponents.items():
                opp_data = filtered_data[filtered_data['opponent'] == opponent]
                wins = len(opp_data[opp_data['result'] == 'Victoire'])
                win_rate = (wins / matches) * 100 if matches > 0 else 0
                
                # Détermination de la couleur selon la performance
                if win_rate >= 60:
                    color = "🟢"
                elif win_rate >= 40:
                    color = "🟡"
                else:
                    color = "🔴"
                
                st.markdown(f"""
                **{color} {opponent}**
                - {matches} matchs - {win_rate:.1f}% victoires
                - Buts: {opp_data['france_score'].sum()}-{opp_data['opponent_score'].sum()}
                """)
        
        # Analyse détaillée par adversaire
        st.markdown("---")
        st.markdown("### 📈 Analyse Détaillée par Adversaire")
        
        # Performance par adversaire (tableau)
        if len(all_opponents[all_opponents >= min_matches]) > 0:
            opponent_performance = get_performance_by_opponent(filtered_data, min_matches)
            
            if len(opponent_performance) > 0:
                # Préparation des données pour l'affichage
                display_df = opponent_performance[['opponent', 'matches_played', 'win_rate', 
                                                 'avg_goals_scored', 'avg_goals_conceded']].copy()
                display_df.columns = ['Adversaire', 'Matchs', '% Victoires', 'Buts/Match', 'Buts Encaissés/Match']
                display_df['% Victoires'] = display_df['% Victoires'].round(1)
                display_df['Buts/Match'] = display_df['Buts/Match'].round(2)
                display_df['Buts Encaissés/Match'] = display_df['Buts Encaissés/Match'].round(2)
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Graphique scatter des performances
                st.markdown("#### 📊 Positionnement Performance vs Expérience")
                
                fig_scatter = px.scatter(
                    opponent_performance,
                    x='matches_played',
                    y='win_rate',
                    size='avg_goals_scored',
                    color='avg_goals_conceded',
                    hover_name='opponent',
                    color_continuous_scale='RdYlGn_r',
                    title="Performance vs Nombre de Confrontations",
                    labels={
                        'matches_played': 'Nombre de Matchs',
                        'win_rate': 'Pourcentage de Victoires (%)',
                        'avg_goals_scored': 'Buts Marqués/Match',
                        'avg_goals_conceded': 'Buts Encaissés/Match'
                    }
                )
                
                # Ligne de référence à 50%
                fig_scatter.add_hline(y=50, line_dash="dash", line_color="gray", 
                                    annotation_text="Équilibre (50%)")
                
                st.plotly_chart(fig_scatter, use_container_width=True)
        
        else:
            st.info(f"Aucun adversaire avec au moins {min_matches} confrontations dans la période sélectionnée")
    
    with tab2:
        st.markdown("### 🏠 Facteurs Influençant la Performance")
        
        # Analyse de l'avantage du terrain
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if len(filtered_data) > 0:
                home_chart = create_home_advantage_chart(filtered_data)
                st.plotly_chart(home_chart, use_container_width=True)
        
        with col2:
            # Calculs pour le résumé
            home_data = filtered_data[filtered_data['is_home'] == True]
            away_data = filtered_data[filtered_data['is_home'] == False]
            
            if len(home_data) > 0 and len(away_data) > 0:
                home_win_rate = len(home_data[home_data['result'] == 'Victoire']) / len(home_data) * 100
                away_win_rate = len(away_data[away_data['result'] == 'Victoire']) / len(away_data) * 100
                home_advantage = home_win_rate - away_win_rate
                
                st.markdown("#### 🏠 Résumé Avantage Terrain")
                st.metric("Avantage Domicile", f"{home_advantage:.1f}%")
                
                st.markdown(f"""
                **À Domicile:**
                - {len(home_data)} matchs
                - {home_win_rate:.1f}% victoires
                - {home_data['france_score'].mean():.2f} buts/match
                
                **À l'Extérieur:**
                - {len(away_data)} matchs  
                - {away_win_rate:.1f}% victoires
                - {away_data['france_score'].mean():.2f} buts/match
                """)
                
                # Analyse contextuelle
                if home_advantage > 15:
                    st.success("🏠 Fort avantage domicile")
                elif home_advantage > 5:
                    st.info("🔄 Léger avantage domicile")
                elif home_advantage > -5:
                    st.warning("⚖️ Performance équilibrée")
                else:
                    st.error("✈️ Meilleure performance extérieur")
        
        # Analyse des scores et patterns de jeu
        st.markdown("---")
        st.markdown("### ⚽ Analyse des Patterns de Score")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Distribution des scores France
            st.markdown("#### 🎯 Distribution Buts Marqués")
            goals_dist = filtered_data['france_score'].value_counts().sort_index()
            
            fig_goals = px.bar(
                x=goals_dist.index,
                y=goals_dist.values,
                title="Fréquence des Scores (Buts Marqués)",
                labels={'x': 'Buts Marqués', 'y': 'Nombre de Matchs'}
            )
            fig_goals.update_layout(template="plotly_white", height=300)
            st.plotly_chart(fig_goals, use_container_width=True)
        
        with col2:
            # Distribution des scores encaissés
            st.markdown("#### 🛡️ Distribution Buts Encaissés")
            conceded_dist = filtered_data['opponent_score'].value_counts().sort_index()
            
            fig_conceded = px.bar(
                x=conceded_dist.index,
                y=conceded_dist.values,
                title="Fréquence des Scores (Buts Encaissés)",
                labels={'x': 'Buts Encaissés', 'y': 'Nombre de Matchs'},
                color_discrete_sequence=['#dc3545']
            )
            fig_conceded.update_layout(template="plotly_white", height=300)
            st.plotly_chart(fig_conceded, use_container_width=True)
        
        with col3:
            # Écarts de buts
            st.markdown("#### 📊 Écarts de Buts")
            goal_diff_dist = filtered_data['goal_difference'].value_counts().sort_index()
            
            colors = ['red' if x < 0 else 'green' if x > 0 else 'gray' for x in goal_diff_dist.index]
            
            fig_diff = px.bar(
                x=goal_diff_dist.index,
                y=goal_diff_dist.values,
                title="Distribution des Écarts",
                labels={'x': 'Écart de Buts', 'y': 'Nombre de Matchs'},
                color=goal_diff_dist.index,
                color_continuous_scale='RdYlGn'
            )
            fig_diff.update_layout(template="plotly_white", height=300)
            st.plotly_chart(fig_diff, use_container_width=True)
        
        # Analyse des matchs serrés vs larges écarts
        st.markdown("---")
        st.markdown("### 🎯 Analyse Tactique des Résultats")
        
        narrow_wins = len(filtered_data[(filtered_data['result'] == 'Victoire') & (filtered_data['goal_difference'] == 1)])
        big_wins = len(filtered_data[filtered_data['goal_difference'] >= 3])
        narrow_defeats = len(filtered_data[(filtered_data['result'] == 'Défaite') & (filtered_data['goal_difference'] == -1)])
        heavy_defeats = len(filtered_data[filtered_data['goal_difference'] <= -3])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🔥 Victoires Serrées", narrow_wins, help="Victoires par 1 but d'écart")
        with col2:
            st.metric("🚀 Larges Victoires", big_wins, help="Victoires par 3+ buts d'écart")
        with col3:
            st.metric("⚠️ Défaites Serrées", narrow_defeats, help="Défaites par 1 but d'écart")
        with col4:
            st.metric("❌ Lourdes Défaites", heavy_defeats, help="Défaites par 3+ buts d'écart")
        
        # Analyse contextuelle
        total_matches = len(filtered_data)
        if total_matches > 0:
            clutch_performance = (narrow_wins / total_matches) * 100
            dominance = (big_wins / total_matches) * 100
            fragility = (heavy_defeats / total_matches) * 100
            
            st.markdown("#### 📈 Profil Tactique")
            
            if clutch_performance > 20:
                st.success(f"🔥 **Excellence dans les matchs serrés** ({clutch_performance:.1f}% de victoires courtes)")
            
            if dominance > 15:
                st.success(f"🚀 **Capacité de domination** ({dominance:.1f}% de larges victoires)")
            
            if fragility < 5:
                st.success(f"🛡️ **Solidité mentale** (seulement {fragility:.1f}% de lourdes défaites)")
            elif fragility > 15:
                st.warning(f"⚠️ **Vulnérabilité aux corrections** ({fragility:.1f}% de lourdes défaites)")
    
    with tab3:
        st.markdown("### 🏆 Performance par Type de Compétition")
        
        # Graphique de performance par tournoi
        if len(filtered_data) > 0:
            tournament_chart = create_tournament_performance_chart(filtered_data)
            st.plotly_chart(tournament_chart, use_container_width=True)
        
        # Tableau détaillé par compétition
        st.markdown("#### 📊 Statistiques Détaillées par Compétition")
        
        tournament_stats = []
        for tournament in filtered_data['tournament'].unique():
            tourn_data = filtered_data[filtered_data['tournament'] == tournament]
            
            if len(tourn_data) >= 2:  # Minimum 2 matchs
                wins = len(tourn_data[tourn_data['result'] == 'Victoire'])
                draws = len(tourn_data[tourn_data['result'] == 'Nul'])
                defeats = len(tourn_data[tourn_data['result'] == 'Défaite'])
                
                tournament_stats.append({
                    'Compétition': tournament,
                    'Matchs': len(tourn_data),
                    'V-N-D': f"{wins}-{draws}-{defeats}",
                    '% Victoires': round((wins / len(tourn_data)) * 100, 1),
                    'Buts/Match': round(tourn_data['france_score'].mean(), 2),
                    'Buts Encaissés/Match': round(tourn_data['opponent_score'].mean(), 2),
                    'Diff./Match': round(tourn_data['goal_difference'].mean(), 2)
                })
        
        if tournament_stats:
            tournament_df = pd.DataFrame(tournament_stats)
            tournament_df = tournament_df.sort_values('Matchs', ascending=False)
            
            st.dataframe(tournament_df, use_container_width=True, hide_index=True)
            
            # Analyse comparative
            st.markdown("#### 🎯 Points Clés par Type de Compétition")
            
            # Identification de la meilleure compétition
            best_tournament = tournament_df.loc[tournament_df['% Victoires'].idxmax()]
            worst_tournament = tournament_df.loc[tournament_df['% Victoires'].idxmin()]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.success(f"""
                **🏆 Meilleure Performance:**
                - {best_tournament['Compétition']}
                - {best_tournament['% Victoires']}% de victoires
                - {best_tournament['Buts/Match']} buts/match
                """)
            
            with col2:
                st.error(f"""
                **⚠️ Performance à Améliorer:**
                - {worst_tournament['Compétition']}
                - {worst_tournament['% Victoires']}% de victoires
                - {worst_tournament['Buts/Match']} buts/match
                """)
            
            # Recommandations spécifiques
            st.markdown("#### 💡 Recommandations par Compétition")
            
            for _, row in tournament_df.iterrows():
                with st.expander(f"📋 {row['Compétition']} - {row['Matchs']} matchs"):
                    win_rate = row['% Victoires']
                    
                    if win_rate >= 60:
                        st.success("🟢 Performance excellente - Maintenir le niveau")
                    elif win_rate >= 40:
                        st.info("🟡 Performance correcte - Identifier les axes d'amélioration")
                    else:
                        st.warning("🔴 Performance insuffisante - Revoir la préparation")
                    
                    # Analyse spécifique
                    offensive_ratio = row['Buts/Match'] / row['Buts Encaissés/Match'] if row['Buts Encaissés/Match'] > 0 else float('inf')
                    
                    if offensive_ratio > 2:
                        st.write("⚽ **Force offensive dominante**")
                    elif offensive_ratio < 0.8:
                        st.write("🛡️ **Problème offensif - Renforcer l'attaque**")
                    else:
                        st.write("⚖️ **Équilibre offensif-défensif**")
                    
                    st.write(f"""
                    - Buts marqués: {row['Buts/Match']}/match
                    - Buts encaissés: {row['Buts Encaissés/Match']}/match
                    - Différentiel: {row['Diff./Match']:+.2f}/match
                    """)
        
        else:
            st.info("Données insuffisantes pour l'analyse par compétition (minimum 2 matchs par tournoi)")
    
    # Section synthèse
    st.markdown("---")
    st.markdown("### 📋 Synthèse de l'Analyse")
    
    # Calcul des insights clés
    insights = []
    
    # Performance globale
    total_win_rate = len(filtered_data[filtered_data['result'] == 'Victoire']) / len(filtered_data) * 100 if len(filtered_data) > 0 else 0
    
    # Adversaires les plus difficiles
    if len(all_opponents) > 0:
        main_opponents = get_performance_by_opponent(filtered_data, min_matches=2)
        if len(main_opponents) > 0:
            toughest_opponent = main_opponents.loc[main_opponents['win_rate'].idxmin()]
            best_opponent = main_opponents.loc[main_opponents['win_rate'].idxmax()]
            
            insights.append(f"🔴 **Adversaire le plus difficile:** {toughest_opponent['opponent']} ({toughest_opponent['win_rate']:.1f}% victoires)")
            insights.append(f"🟢 **Meilleure confrontation:** {best_opponent['opponent']} ({best_opponent['win_rate']:.1f}% victoires)")
    
    # Avantage terrain
    home_advantage = calculate_home_advantage(filtered_data)
    if home_advantage > 10:
        insights.append(f"🏠 **Fort avantage domicile:** +{home_advantage:.1f}% de performance")
    elif home_advantage < -5:
        insights.append(f"✈️ **Paradoxe extérieur:** {abs(home_advantage):.1f}% de performance en plus à l'extérieur")
    
    # Profil de jeu
    avg_goals_scored = filtered_data['france_score'].mean() if len(filtered_data) > 0 else 0
    avg_goals_conceded = filtered_data['opponent_score'].mean() if len(filtered_data) > 0 else 0
    
    if avg_goals_scored > 2:
        insights.append("⚽ **Profil offensif** - Plus de 2 buts/match en moyenne")
    
    if avg_goals_conceded < 1:
        insights.append("🛡️ **Solidité défensive** - Moins d'1 but encaissé/match")
    
    # Affichage des insights
    for insight in insights:
        st.markdown(f"- {insight}")
    
    # Actions recommandées
    st.markdown("#### 🎯 Plan d'Action Recommandé")
    
    action_plan = []
    
    if total_win_rate < 50:
        action_plan.append("1. **Analyse vidéo approfondie** des défaites pour identifier les patterns récurrents")
    
    if home_advantage < 0:
        action_plan.append("2. **Optimisation de la préparation domicile** - Gestion de la pression, routines pré-match")
    
    if avg_goals_scored < 1.5:
        action_plan.append("3. **Travail offensif spécifique** - Finition, création d'occasions, mouvements sans ballon")
    
    if avg_goals_conceded > avg_goals_scored:
        action_plan.append("4. **Renforcement défensif prioritaire** - Organisation, communication, situations d'arrêt")
    
    if len(action_plan) == 0:
        action_plan.append("1. **Consolidation** - Maintenir le niveau actuel et préparer les prochains objectifs")
    
    for action in action_plan:
        st.markdown(action)
