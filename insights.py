import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.data_processing import calculate_performance_metrics, calculate_trend_metrics, calculate_home_advantage

def show_insights(filtered_data, full_data):
    """
    Page insights avec tendances récentes et recommandations stratégiques
    """
    st.title("💡 Insights & Recommandations Stratégiques")
    
    # Calcul des périodes pour comparaison
    current_year = datetime.now().year
    recent_data = full_data[full_data['year'] >= current_year - 2]  # 2 dernières années
    historical_data = full_data[full_data['year'] < current_year - 2]  # Données historiques
    
    # Tabs pour organiser les insights
    tab1, tab2, tab3 = st.tabs(["📈 Tendances Récentes", "🎯 Projections & Objectifs", "🏆 Recommandations FFF"])
    
    with tab1:
        st.markdown("### 📈 Analyse des Tendances Récentes")
        
        # Comparaison récent vs historique
        col1, col2, col3 = st.columns(3)
        
        if len(recent_data) > 0 and len(historical_data) > 0:
            recent_metrics = calculate_performance_metrics(recent_data)
            historical_metrics = calculate_performance_metrics(historical_data)
            
            with col1:
                win_rate_trend = recent_metrics['win_rate'] - historical_metrics['win_rate']
                st.metric(
                    "🏆 Évolution Taux de Victoire",
                    f"{recent_metrics['win_rate']:.1f}%",
                    f"{win_rate_trend:+.1f}%"
                )
            
            with col2:
                goals_trend = recent_metrics['avg_goals_scored'] - historical_metrics['avg_goals_scored']
                st.metric(
                    "⚽ Évolution Offensive",
                    f"{recent_metrics['avg_goals_scored']:.2f}",
                    f"{goals_trend:+.2f}"
                )
            
            with col3:
                defense_trend = historical_metrics['avg_goals_conceded'] - recent_metrics['avg_goals_conceded']
                st.metric(
                    "🛡️ Évolution Défensive",
                    f"{recent_metrics['avg_goals_conceded']:.2f}",
                    f"{defense_trend:+.2f}",
                    delta_color="inverse"
                )
        
        # Analyse du momentum avec graphique de tendance
        st.markdown("---")
        st.markdown("### 🎲 Analyse du Momentum")
        
        if len(filtered_data) >= 15:
            # Calcul du momentum avec moyennes mobiles
            trend_data = calculate_trend_metrics(filtered_data, window=8)
            
            fig_momentum = go.Figure()
            
            # Points par match (moyenne mobile)
            fig_momentum.add_trace(go.Scatter(
                x=trend_data['date'],
                y=trend_data['rolling_points'],
                mode='lines+markers',
                name='Performance (Points)',
                line=dict(color='#0055A4', width=3),
                hovertemplate='<b>%{y:.2f}</b> points<br>%{x}<extra></extra>'
            ))
            
            # Ligne de référence (performance moyenne)
            avg_performance = trend_data['points'].mean()
            fig_momentum.add_hline(
                y=avg_performance,
                line_dash="dash",
                line_color="gray",
                annotation_text=f"Moyenne: {avg_performance:.2f}"
            )
            
            # Zones de performance
            fig_momentum.add_hrect(
                y0=2.5, y1=3, fillcolor="green", opacity=0.1,
                annotation_text="Excellence", annotation_position="top left"
            )
            fig_momentum.add_hrect(
                y0=1.5, y1=2.5, fillcolor="yellow", opacity=0.1,
                annotation_text="Correct", annotation_position="top left"
            )
            fig_momentum.add_hrect(
                y0=0, y1=1.5, fillcolor="red", opacity=0.1,
                annotation_text="À Améliorer", annotation_position="top left"
            )
            
            fig_momentum.update_layout(
                title="🎯 Évolution du Momentum (Moyenne Mobile 8 Matchs)",
                xaxis_title="Date",
                yaxis_title="Points par Match (3=Victoire, 1=Nul, 0=Défaite)",
                template="plotly_white",
                height=400
            )
            
            st.plotly_chart(fig_momentum, use_container_width=True)
            
            # Analyse des séries
            st.markdown("#### 🔥 Analyse des Séries")
            
            # Calcul des séries actuelles
            recent_matches = trend_data.sort_values('date').tail(10)
            current_streak = 0
            streak_type = "Unknown"
            
            if len(recent_matches) > 0:
                last_result = recent_matches.iloc[-1]['result']
                streak_type = last_result
                
                # Compter la série actuelle
                for i in range(len(recent_matches) - 1, -1, -1):
                    if recent_matches.iloc[i]['result'] == last_result:
                        current_streak += 1
                    else:
                        break
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if streak_type == "Victoire":
                    st.success(f"🔥 **Série de {current_streak} victoire(s)**")
                elif streak_type == "Défaite":
                    st.error(f"❌ **Série de {current_streak} défaite(s)**")
                else:
                    st.info(f"⚖️ **Série de {current_streak} nul(s)**")
            
            with col2:
                # Performance sur les 5 derniers matchs
                last_5 = recent_matches.tail(5)
                wins_5 = len(last_5[last_5['result'] == 'Victoire'])
                st.metric("📊 Forme Récente (5 matchs)", f"{wins_5}/5", f"{wins_5*20}%")
            
            with col3:
                # Tendance points
                if len(recent_matches) >= 5:
                    recent_avg = recent_matches.tail(5)['points'].mean()
                    previous_avg = recent_matches.head(5)['points'].mean() if len(recent_matches) >= 10 else recent_avg
                    trend = recent_avg - previous_avg
                    
                    if trend > 0.3:
                        st.success(f"📈 **Tendance Positive** (+{trend:.2f})")
                    elif trend < -0.3:
                        st.error(f"📉 **Tendance Négative** ({trend:.2f})")
                    else:
                        st.info(f"➡️ **Tendance Stable** ({trend:+.2f})")
        
        else:
            st.warning("⚠️ Données insuffisantes pour l'analyse du momentum (minimum 15 matchs)")
        
        # Analyse saisonnière
        st.markdown("---")
        st.markdown("### 📅 Patterns Temporels")
        
        if len(filtered_data) > 0:
            # Performance par mois
            monthly_performance = filtered_data.groupby('month').agg({
                'result': lambda x: (x == 'Victoire').sum() / len(x) * 100,
                'france_score': 'mean',
                'opponent_score': 'mean'
            }).reset_index()
            
            monthly_performance.columns = ['month', 'win_rate', 'goals_scored', 'goals_conceded']
            
            # Mapping des mois
            month_names = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun',
                          'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
            monthly_performance['month_name'] = monthly_performance['month'].map(
                lambda x: month_names[x-1] if 1 <= x <= 12 else 'Unknown'
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_monthly = px.bar(
                    monthly_performance,
                    x='month_name',
                    y='win_rate',
                    title="Performance par Mois de l'Année",
                    labels={'win_rate': '% Victoires', 'month_name': 'Mois'},
                    color='win_rate',
                    color_continuous_scale='RdYlGn'
                )
                fig_monthly.update_layout(template="plotly_white", height=350)
                st.plotly_chart(fig_monthly, use_container_width=True)
            
            with col2:
                # Identification des meilleurs/pires mois
                best_month = monthly_performance.loc[monthly_performance['win_rate'].idxmax()]
                worst_month = monthly_performance.loc[monthly_performance['win_rate'].idxmin()]
                
                st.markdown("#### 📊 Insights Saisonniers")
                st.success(f"🏆 **Meilleur mois:** {best_month['month_name']} ({best_month['win_rate']:.1f}%)")
                st.error(f"⚠️ **Mois difficile:** {worst_month['month_name']} ({worst_month['win_rate']:.1f}%)")
                
                # Analyse contextuelle
                summer_months = monthly_performance[monthly_performance['month'].isin([6, 7, 8])]
                winter_months = monthly_performance[monthly_performance['month'].isin([12, 1, 2])]
                
                if len(summer_months) > 0 and len(winter_months) > 0:
                    summer_avg = summer_months['win_rate'].mean()
                    winter_avg = winter_months['win_rate'].mean()
                    
                    if summer_avg > winter_avg + 10:
                        st.info("☀️ **Meilleures performances estivales**")
                    elif winter_avg > summer_avg + 10:
                        st.info("❄️ **Meilleures performances hivernales**")
    
    with tab2:
        st.markdown("### 🎯 Projections et Objectifs")
        
        # Définition d'objectifs basés sur les données
        if len(recent_data) > 0:
            current_performance = calculate_performance_metrics(recent_data)
            
            # Objectifs recommandés
            st.markdown("#### 🎯 Objectifs Recommandés pour la Prochaine Période")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 📊 Objectifs de Performance")
                
                current_win_rate = current_performance['win_rate']
                target_win_rate = min(current_win_rate + 5, 75)  # Amélioration progressive
                
                # Barre de progression pour le taux de victoire
                progress_win = current_win_rate / 100
                st.metric("Taux de Victoire Actuel", f"{current_win_rate:.1f}%")
                st.progress(progress_win)
                st.success(f"🎯 **Objectif:** {target_win_rate:.1f}% (+{target_win_rate - current_win_rate:.1f}%)")
                
                # Objectifs offensifs
                current_goals = current_performance['avg_goals_scored']
                target_goals = current_goals + 0.2  # Amélioration modeste
                
                st.metric("Buts/Match Actuel", f"{current_goals:.2f}")
                st.info(f"🎯 **Objectif:** {target_goals:.2f} buts/match")
                
                # Objectifs défensifs
                current_conceded = current_performance['avg_goals_conceded']
                target_conceded = max(current_conceded - 0.1, 0.5)  # Amélioration défensive
                
                st.metric("Buts Encaissés/Match", f"{current_conceded:.2f}")
                st.warning(f"🎯 **Objectif:** {target_conceded:.2f} buts encaissés/match")
            
            with col2:
                st.markdown("##### 📈 Projections Basées sur les Tendances")
                
                # Projection simple basée sur la tendance récente
                if len(recent_data) >= 10:
                    # Calcul de la tendance sur les matchs récents
                    recent_sorted = recent_data.sort_values('date')
                    first_half = recent_sorted.head(len(recent_sorted)//2)
                    second_half = recent_sorted.tail(len(recent_sorted)//2)
                    
                    if len(first_half) > 0 and len(second_half) > 0:
                        trend_wins = (len(second_half[second_half['result'] == 'Victoire']) / len(second_half)) - \
                                   (len(first_half[first_half['result'] == 'Victoire']) / len(first_half))
                        
                        # Projection à 12 mois
                        projected_win_rate = current_win_rate + (trend_wins * 100 * 2)  # Extrapolation
                        projected_win_rate = max(0, min(100, projected_win_rate))  # Bornes réalistes
                        
                        st.markdown("**🔮 Projection 12 mois:**")
                        
                        if trend_wins > 0.1:
                            st.success(f"📈 Tendance positive: {projected_win_rate:.1f}% victoires projetées")
                        elif trend_wins < -0.1:
                            st.error(f"📉 Tendance négative: {projected_win_rate:.1f}% victoires projetées")
                        else:
                            st.info(f"➡️ Tendance stable: {projected_win_rate:.1f}% victoires projetées")
                        
                        # Graphique de projection
                        months = ['Actuel', 'Dans 3 mois', 'Dans 6 mois', 'Dans 12 mois']
                        projections = [
                            current_win_rate,
                            current_win_rate + (trend_wins * 100 * 0.5),
                            current_win_rate + (trend_wins * 100 * 1),
                            projected_win_rate
                        ]
                        
                        fig_projection = px.line(
                            x=months,
                            y=projections,
                            title="Projection Performance",
                            markers=True
                        )
                        fig_projection.add_hline(y=50, line_dash="dash", line_color="gray")
                        fig_projection.update_layout(
                            template="plotly_white",
                            height=250,
                            yaxis_title="% Victoires"
                        )
                        st.plotly_chart(fig_projection, use_container_width=True)
        
        # Benchmarking international
        st.markdown("---")
        st.markdown("### 🌍 Benchmarking International")
        
        # Simulation de standards internationaux (à adapter avec de vraies données)
        international_standards = {
            'Top 5 Mondial': {'win_rate': 70, 'goals_per_match': 2.1, 'goals_conceded': 0.8},
            'Top 10 Mondial': {'win_rate': 60, 'goals_per_match': 1.8, 'goals_conceded': 1.1},
            'Top 20 Mondial': {'win_rate': 50, 'goals_per_match': 1.5, 'goals_conceded': 1.4}
        }
        
        current_metrics = calculate_performance_metrics(filtered_data)
        
        st.markdown("#### 📊 Positionnement vs Standards Internationaux")
        
        # Graphique radar de comparaison
        categories = ['Taux de Victoire', 'Efficacité Offensive', 'Solidité Défensive']
        
        fig_radar = go.Figure()
        
        # Performance France (normalisée)
        france_values = [
            current_metrics.get('win_rate', 0),
            current_metrics.get('avg_goals_scored', 0) * 50,  # Normalisation
            (3 - current_metrics.get('avg_goals_conceded', 1)) * 33.33  # Inverse et normalisation
        ]
        
        fig_radar.add_trace(go.Scatterpolar(
            r=france_values,
            theta=categories,
            fill='toself',
            name='France Actuel',
            line_color='#0055A4'
        ))
        
        # Standards Top 10
        top10_values = [60, 90, 66.67]  # Valeurs normalisées
        fig_radar.add_trace(go.Scatterpolar(
            r=top10_values,
            theta=categories,
            fill='toself',
            name='Standard Top 10',
            line_color='#28a745',
            opacity=0.5
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Comparaison vs Standards Internationaux",
            template="plotly_white"
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Gap analysis
        st.markdown("#### 📈 Analyse des Écarts")
        
        gaps = []
        current_win_rate = current_metrics.get('win_rate', 0)
        
        for level, standards in international_standards.items():
            win_gap = standards['win_rate'] - current_win_rate
            if win_gap > 0:
                gaps.append({
                    'Niveau': level,
                    'Écart Victoires': f"+{win_gap:.1f}%",
                    'Matchs à Gagner': f"{win_gap/100 * 20:.0f} sur 20",  # Sur une base de 20 matchs
                    'Priorité': '🔴 Élevée' if win_gap > 20 else '🟡 Modérée' if win_gap > 10 else '🟢 Faible'
                })
        
        if gaps:
            gap_df = pd.DataFrame(gaps)
            st.dataframe(gap_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### 🏆 Recommandations Stratégiques pour la FFF")
        
        # Analyse SWOT automatisée
        st.markdown("#### 📊 Analyse SWOT Automatisée")
        
        current_metrics = calculate_performance_metrics(filtered_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 💪 **FORCES**")
            forces = []
            
            if current_metrics.get('win_rate', 0) > 55:
                forces.append("✅ Taux de victoire supérieur à 55%")
            
            if current_metrics.get('avg_goals_scored', 0) > 1.7:
                forces.append("✅ Efficacité offensive (>1.7 buts/match)")
            
            if current_metrics.get('avg_goals_conceded', 0) < 1.2:
                forces.append("✅ Solidité défensive (<1.2 buts encaissés/match)")
            
            home_adv = calculate_home_advantage(filtered_data) if len(filtered_data) > 0 else 0
            if home_adv > 10:
                forces.append("✅ Fort avantage du terrain à domicile")
            
            if current_metrics.get('clean_sheets', 0) / current_metrics.get('total_matches', 1) > 0.3:
                forces.append("✅ Régularité défensive (>30% clean sheets)")
            
            if not forces:
                forces.append("🔍 Potentiel d'amélioration identifié")
            
            for force in forces:
                st.success(force)
            
            st.markdown("##### 🚀 **OPPORTUNITÉS**")
            opportunities = [
                "🌟 Développement des jeunes talents",
                "📈 Croissance de la visibilité du football féminin",
                "🏟️ Amélioration des infrastructures",
                "🤝 Partenariats internationaux renforcés",
                "📺 Augmentation de l'audience médiatique"
            ]
            
            for opp in opportunities:
                st.info(opp)
        
        with col2:
            st.markdown("##### ⚠️ **FAIBLESSES**")
            weaknesses = []
            
            if current_metrics.get('win_rate', 0) < 45:
                weaknesses.append("❌ Taux de victoire insuffisant (<45%)")
            
            if current_metrics.get('avg_goals_scored', 0) < 1.3:
                weaknesses.append("❌ Manque d'efficacité offensive")
            
            if current_metrics.get('avg_goals_conceded', 0) > 1.5:
                weaknesses.append("❌ Vulnérabilité défensive")
            
            if home_adv < 0:
                weaknesses.append("❌ Absence d'avantage domicile")
            
            if current_metrics.get('big_wins', 0) / current_metrics.get('total_matches', 1) < 0.1:
                weaknesses.append("❌ Peu de victoires convaincantes")
            
            if not weaknesses:
                weaknesses.append("✨ Aucune faiblesse majeure identifiée")
            
            for weakness in weaknesses:
                st.error(weakness)
            
            st.markdown("##### 🚨 **MENACES**")
            threats = [
                "🏃‍♀️ Progression rapide des nations concurrentes",
                "💰 Écarts de moyens avec certaines fédérations",
                "🏥 Risques de blessures des joueuses clés",
                "📅 Calendrier international chargé",
                "🔄 Rotation nécessaire entre clubs et sélection"
            ]
            
            for threat in threats:
                st.warning(threat)
        
        # Plan d'action stratégique
        st.markdown("---")
        st.markdown("#### 🎯 Plan d'Action Stratégique 2024-2026")
        
        # Priorités basées sur l'analyse des données
        priorities = []
        
        if current_metrics.get('win_rate', 0) < 50:
            priorities.append({
                'priorité': 1,
                'domaine': 'Performance Générale',
                'objectif': 'Atteindre 50% de victoires minimum',
                'actions': [
                    'Analyse vidéo systématique des défaites',
                    'Renforcement mental et cohésion groupe',
                    'Optimisation des schémas tactiques'
                ]
            })
        
        if current_metrics.get('avg_goals_scored', 0) < 1.5:
            priorities.append({
                'priorité': 2,
                'domaine': 'Efficacité Offensive',
                'objectif': 'Améliorer la production offensive',
                'actions': [
                    'Travail spécifique finition et dernière passe',
                    'Développement variantes tactiques offensives',
                    'Intégration nouveaux profils créatifs'
                ]
            })
        
        if current_metrics.get('avg_goals_conceded', 0) > 1.3:
            priorities.append({
                'priorité': 3,
                'domaine': 'Solidité Défensive',
                'objectif': 'Réduire les buts encaissés',
                'actions': [
                    'Amélioration communication défensive',
                    'Travail situations d\'arrêt défensives',
                    'Renforcement physique et duels'
                ]
            })
        
        if home_adv < 5:
            priorities.append({
                'priorité': 4,
                'domaine': 'Optimisation Domicile',
                'objectif': 'Créer un véritable avantage à domicile',
                'actions': [
                    'Amélioration préparation pré-match domicile',
                    'Gestion pression et attentes public',
                    'Optimisation logistique et confort'
                ]
            })
        
        # Affichage du plan d'action
        for i, priority in enumerate(priorities[:3]):  # Max 3 priorités
            with st.expander(f"🎯 **Priorité {priority['priorité']}: {priority['domaine']}**"):
                st.markdown(f"**Objectif:** {priority['objectif']}")
                st.markdown("**Actions concrètes:**")
                for action in priority['actions']:
                    st.markdown(f"• {action}")
                
                # Timeline suggérée
                st.markdown("**Timeline suggérée:** 6-12 mois")
                
                # Indicateurs de suivi
                if priority['domaine'] == 'Performance Générale':
                    st.markdown("**Indicateurs:** Taux de victoire, points par match")
                elif priority['domaine'] == 'Efficacité Offensive':
                    st.markdown("**Indicateurs:** Buts/match, occasions créées, conversion")
                elif priority['domaine'] == 'Solidité Défensive':
                    st.markdown("**Indicateurs:** Buts encaissés/match, clean sheets")
                elif priority['domaine'] == 'Optimisation Domicile':
                    st.markdown("**Indicateurs:** % victoires domicile vs extérieur")
        
        # Investissements recommandés
        st.markdown("---")
        st.markdown("#### 💰 Investissements Recommandés")
        
        investment_areas = [
            {
                'domaine': '👥 Formation et Détection',
                'budget': 'Élevé',
                'impact': 'Long terme',
                'description': 'Renforcement centres de formation, détection précoce talents'
            },
            {
                'domaine': '🧠 Staff Technique',
                'budget': 'Modéré',
                'impact': 'Court terme',
                'description': 'Spécialistes analyse vidéo, préparateurs mentaux, nutritionnistes'
            },
            {
                'domaine': '🏥 Médical et Performance',
                'budget': 'Modéré',
                'impact': 'Moyen terme',
                'description': 'Prévention blessures, optimisation récupération, suivi physique'
            },
            {
                'domaine': '🏟️ Infrastructures',
                'budget': 'Élevé',
                'impact': 'Long terme',
                'description': 'Centres d\'entraînement dédiés, terrains de qualité'
            }
        ]
        
        for investment in investment_areas:
            with st.expander(f"{investment['domaine']} - Budget: {investment['budget']}"):
                st.markdown(f"**Impact attendu:** {investment['impact']}")
                st.markdown(f"**Description:** {investment['description']}")
                
                # ROI estimé
                if investment['budget'] == 'Élevé':
                    st.info("💡 ROI élevé sur le long terme, investissement structurel")
                else:
                    st.success("💡 ROI rapide, amélioration performance immédiate")
        
        # Conclusion et vision
        st.markdown("---")
        st.markdown("### 🚀 Vision Stratégique 2026")
        
        st.markdown(f"""
        Basé sur l'analyse des {len(filtered_data)} matchs de la période sélectionnée, 
        voici la feuille de route recommandée pour l'équipe de France féminine :
        
        **🎯 Objectifs 2026:**
        - ✅ Atteindre le Top 8 mondial de façon stable
        - ✅ 60% de taux de victoire minimum
        - ✅ Qualification systématique aux phases finales des grandes compétitions
        
        **🏆 Ambitions Competition:**
        - 🥇 Podium Euro 2025
        - 🌍 Quart de finale Coupe du Monde 2027 minimum
        - 🏅 Médaille Jeux Olympiques 2028
        
        **💪 Piliers du Succès:**
        1. **Excellence technique** - Formation continue et innovation tactique
        2. **Mentalité de gagnante** - Culture de la performance et résilience
        3. **Professionnalisation** - Structures et moyens de niveau mondial
        4. **Identité de jeu** - Style reconnaissable et efficace
        """)
        
        # Call to action
        st.success("""
        🎯 **La France a tous les atouts pour rejoindre l'élite mondiale du football féminin. 
        Les données montrent un potentiel inexploité qui ne demande qu'à être révélé par 
        une approche structurée et des investissements ciblés.**
        """)
    
    # Sidebar avec données contextuelles
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📊 Données de Contexte")
        
        if len(filtered_data) > 0:
            st.markdown(f"""
            **Période analysée:**
            {filtered_data['date'].min().strftime('%d/%m/%Y')} - {filtered_data['date'].max().strftime('%d/%m/%Y')}
            
            **Données récentes (2 ans):**
            {len(recent_data)} matchs
            
            **Base historique:**
            {len(historical_data)} matchs
            
            **Dernière mise à jour:**
            {datetime.now().strftime('%d/%m/%Y %H:%M')}
            """)
