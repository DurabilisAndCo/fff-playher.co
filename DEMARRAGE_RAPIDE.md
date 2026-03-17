# 🚀 Guide de Démarrage Rapide - Dashboard FFF

## ✅ Problèmes Résolus

Les erreurs suivantes ont été corrigées :

1. **ValueError: Trace type 'pie' is not compatible with subplot type 'xy'**
   - ✅ Corrigé : Configuration du subplot (2,2) avec `{"type": "domain"}` pour les pie charts

2. **ValueError: Trace type 'scatterpolar' is not compatible with subplot type 'xy'**
   - ✅ Corrigé : Configuration du subplot (2,2) avec `{"type": "polar"}` pour les radar charts

3. **Invalid property 'xaxis' for Scatterpolar**
   - ✅ Corrigé : Suppression des lignes de référence incompatibles avec les subplots polaires

## 🏃‍♂️ Lancement du Dashboard

### Méthode 1 : Script automatique (Windows)
```cmd
run_dashboard.bat
```

### Méthode 2 : PowerShell
```powershell
.\run_dashboard.ps1
```

### Méthode 3 : Ligne de commande
```bash
# Activer l'environnement virtuel
.venv\Scripts\activate

# Lancer le dashboard
streamlit run app.py
```

## 📊 Fonctionnalités Disponibles

### 🏠 Page Accueil
- Vue d'ensemble des performances
- Statistiques clés avec indicateurs visuels
- Évolution temporelle avec pie charts et graphiques linéaires
- Métriques de performance par année

### 📊 Page Analyse
- Comparaison internationale avec radar charts
- Performance par adversaire
- Analyse des buts marqués vs encaissés
- Graphiques en barres et scatter plots

### 💡 Page Insights
- Avantage du terrain (domicile vs extérieur)
- Tendances et momentum
- Performance par type de compétition
- Analyses statistiques avancées

## 🔧 Filtres Dynamiques

- **Période d'analyse** : Slider pour sélectionner les années
- **Type de compétition** : Multiselect pour filtrer par tournoi
- Navigation intuitive entre les pages

## 📁 Structure des Données

Le dashboard utilise le fichier `data/results.csv` avec les colonnes :
- `date` : Date du match
- `home_team` / `away_team` : Équipes
- `home_score` / `away_score` : Scores
- `tournament` : Type de compétition
- `neutral` : Match sur terrain neutre

## 🐛 Dépannage

Si vous rencontrez des erreurs :

1. **Vérifiez l'environnement virtuel** :
   ```bash
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Testez les visualisations** :
   ```bash
   python test_final_validation.py
   ```

3. **Vérifiez le fichier de données** :
   - Le fichier `data/results.csv` doit exister
   - Format CSV avec headers corrects

## 📈 Performance

- **Mise en cache** : Les données sont mises en cache avec `@st.cache_data`
- **Filtrage efficace** : Les filtres sont appliqués de manière optimisée
- **Rendu rapide** : Visualisations Plotly optimisées

## 🎨 Personnalisation

Le dashboard utilise les couleurs officielles FFF :
- Bleu : `#0055A4`
- Rouge : `#EF4135`
- Thème moderne avec design responsive

---

🇫🇷 **Dashboard FFF - Équipe de France Féminine** ⚽

*Développé pour l'analyse des performances de l'équipe de France féminine de football*
