# 🇫🇷 Dashboard FFF - Équipe de France Féminine ⚽

## 📊 Description

Dashboard interactif développé pour la Fédération Française de Football (FFF) permettant d'analyser les performances de l'équipe de France féminine de football. L'application fournit des insights stratégiques basés sur des données historiques de matchs internationaux.

## 🚀 Fonctionnalités Principales

### 🏠 Page d'Accueil
- **KPIs principaux** : Taux de victoire, efficacité offensive/défensive, avantage domicile
- **Évolution historique** : Graphiques interactifs des performances dans le temps
- **Analyse du momentum** : Tendances récentes avec moyennes mobiles
- **Résumé exécutif** : Insights automatisés et recommandations

### 📊 Page Analyse
- **Comparaisons internationales** : Performance face aux principales nations
- **Facteurs de performance** : Analyse domicile/extérieur, patterns de jeu
- **Performance par compétition** : Analyse détaillée par type de tournoi
- **Analyse tactique** : Distribution des scores, style de jeu

### 💡 Page Insights
- **Tendances récentes** : Évolution sur les 2 dernières années vs historique
- **Projections** : Objectifs recommandés et extrapolations
- **Benchmarking international** : Positionnement vs standards mondiaux
- **Recommandations FFF** : Plan d'action stratégique et investissements

## 🛠️ Installation

### Prérequis
- Python 3.8+
- pip

### Installation des dépendances
```bash
pip install -r requirements.txt
```

### Lancement de l'application
```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

## 📁 Structure du Projet

```
Dashboard fff/
├── app.py                      # Application principale Streamlit
├── requirements.txt            # Dépendances Python
├── README.md                  # Documentation
├── data/
│   └── france_matches.csv     # Données des matchs (exemple inclus)
├── pages/
│   ├── accueil.py            # Page d'accueil avec KPIs
│   ├── analyse.py            # Page d'analyse approfondie
│   └── insights.py           # Page insights et recommandations
└── utils/
    ├── data_processing.py    # Fonctions de traitement des données
    └── visualizations.py    # Fonctions de création des graphiques
```

## 📈 Données

### Format Attendu
Le fichier CSV doit contenir les colonnes suivantes :
- `date` : Date du match (YYYY-MM-DD)
- `home_team` : Équipe à domicile
- `away_team` : Équipe à l'extérieur
- `home_score` : Score équipe domicile
- `away_score` : Score équipe extérieur
- `tournament` : Type de compétition
- `city` : Ville du match
- `country` : Pays hôte
- `neutral` : Terrain neutre (booléen)

### Données d'Exemple
Un fichier d'exemple avec 50 matchs récents de l'équipe de France est fourni dans `data/france_matches.csv`.

## 🎨 Fonctionnalités Interactives

### Filtres Disponibles
- **Période d'analyse** : Slider pour sélectionner la plage d'années
- **Type de compétition** : Sélection multiple des tournois
- **Navigation** : Menu latéral pour basculer entre les pages

### Visualisations
- **Graphiques Plotly interactifs** : Zoom, hover, export
- **Métriques dynamiques** : Avec indicateurs de tendance
- **Tableaux filtrables** : Données détaillées par adversaire/compétition
- **Graphiques radar** : Comparaisons multi-dimensionnelles

## 📊 Métriques Calculées

### Performance Générale
- **Taux de victoire** : (Victoires / Total matchs) × 100
- **Efficacité offensive** : Buts marqués par match
- **Solidité défensive** : Buts encaissés par match
- **Différentiel** : Écart de buts moyen par match

### Métriques Avancées
- **Avantage domicile** : % victoires domicile - % victoires extérieur
- **Clean sheets** : Pourcentage de matchs sans but encaissé
- **Larges victoires** : Victoires par 3+ buts d'écart
- **Momentum** : Moyenne mobile des performances

## 🎯 Insights Automatisés

L'application génère automatiquement :
- **Analyse SWOT** basée sur les données
- **Recommandations tactiques** selon les patterns identifiés
- **Objectifs de performance** adaptés au niveau actuel
- **Plan d'action stratégique** avec priorités

## 🔧 Personnalisation

### Couleurs FFF
- Bleu France : `#0055A4`
- Rouge : `#EF4135`
- Gris clair : `#F0F2F6`

### Modification des Seuils
Les seuils d'analyse peuvent être ajustés dans les fichiers `utils/`:
- Minimum de matchs pour les comparaisons
- Définition des "larges victoires"
- Périodes de référence pour les tendances

## 🚀 Déploiement

### Streamlit Cloud
1. Fork le repository
2. Connecter à Streamlit Cloud
3. Déployer directement depuis GitHub

### Heroku
```bash
# Ajouter Procfile
echo "web: sh setup.sh && streamlit run app.py" > Procfile

# Déployer
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## 📱 Responsive Design

L'application est optimisée pour :
- **Desktop** : Affichage complet avec toutes les fonctionnalités
- **Tablet** : Adaptation automatique des colonnes
- **Mobile** : Interface simplifiée mais fonctionnelle

## 🔍 Analyse des Performances

### Temps de Chargement
- **Objectif** : < 3 secondes pour le chargement initial
- **Optimisation** : Cache des données avec `@st.cache_data`
- **Graphiques** : Rendu optimisé avec Plotly

### Données Supportées
- **Minimum** : 10 matchs pour les analyses de base
- **Recommandé** : 50+ matchs pour analyses complètes
- **Maximum testé** : 500+ matchs sans problème de performance

## 🛡️ Qualité du Code

### Standards
- **PEP 8** : Respect des conventions Python
- **Documentation** : Docstrings pour toutes les fonctions
- **Modularité** : Code organisé en modules réutilisables
- **Gestion d'erreurs** : Validation des données et affichage d'erreurs explicites

### Tests
- **Données manquantes** : Gestion automatique
- **Périodes vides** : Messages informatifs
- **Erreurs de format** : Validation et suggestions

## 📞 Support

Pour toute question ou amélioration :
1. Vérifier les logs Streamlit en cas d'erreur
2. Valider le format des données CSV
3. Contrôler les dépendances Python

## 🔄 Mises à Jour

### Ajout de Nouvelles Données
1. Mettre à jour le fichier CSV dans `data/`
2. Relancer l'application (cache automatiquement vidé)

### Nouvelles Fonctionnalités
- Modifier les fichiers dans `pages/` pour nouvelles analyses
- Ajouter des fonctions dans `utils/` pour nouveaux calculs
- Mettre à jour `requirements.txt` si nouvelles dépendances

## 📈 Roadmap

### Améliorations Prévues
- [ ] Export PDF des rapports
- [ ] Comparaison avec d'autres équipes nationales
- [ ] Analyse prédictive avec ML
- [ ] Intégration API temps réel
- [ ] Dashboard coach avec analyses tactiques avancées

---

*Dashboard développé pour la Fédération Française de Football (FFF)*  
*Équipe de France Féminine - Analyses et Performance*
