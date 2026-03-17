# 🚀 Guide de Démarrage Rapide - Dashboard FFF

## ✅ MISE À JOUR : Prêt pour vos données results.csv

**✅ Le code a été adapté pour utiliser votre fichier `results.csv`**

### 🔧 Adaptations Réalisées
- **Source de données :** `data/results.csv` (votre fichier)
- **Normalisation :** Noms d'équipes en minuscules automatique
- **Méthode robuste :** Utilisation de `apply()` comme dans votre exemple
- **Types Streamlit :** Conversion automatique numpy.int64 → int Python
- **Gestion d'erreurs :** Fallback sur données d'exemple si problème

### 🧪 Tests Disponibles
```bash
# Test général avec vos données
python test_real_data.py

# Test spécifique types Streamlit
python test_streamlit_types.py
```

**Résultat attendu :** ✅ Tous les tests passent sans erreur KeyError

---

## 📋 Checklist de Lancement

### ✅ 1. Vérification de l'Installation

Double-cliquez sur `run_dashboard.bat` ou exécutez dans le terminal :
```bash
python test_installation.py
```

Vous devriez voir :
- ✅ Streamlit importé avec succès
- ✅ Pandas importé avec succès  
- ✅ NumPy importé avec succès
- ✅ Plotly importé avec succès
- ✅ Données chargées: XX matchs

### ✅ 2. Lancement de l'Application

**Option A - Script automatique (Recommandé)**
```bash
./run_dashboard.bat
```

**Option B - Manuel**
```bash
streamlit run app.py
```

### ✅ 3. Accès à l'Application

Ouvrez votre navigateur et allez à : `http://localhost:8501`

## 🎯 Première Utilisation

### Navigation
1. **🏠 Accueil** : Vue d'ensemble avec KPIs principaux
2. **📊 Analyse** : Comparaisons internationales et facteurs de performance  
3. **💡 Insights** : Tendances récentes et recommandations stratégiques

### Filtres Disponibles
- **Période d'analyse** : Slider dans la sidebar (par défaut: 10 dernières années)
- **Type de compétition** : Sélection multiple des tournois
- **Navigation** : Menu latéral pour changer de page

## 📊 Données Fournies

Le fichier d'exemple `data/france_matches.csv` contient **50 matchs récents** de l'équipe de France féminine (2021-2024) incluant :

- Matchs de Coupe du Monde 2023
- Qualifications Euro 2022
- Matchs amicaux internationaux
- Diverses compétitions (SheBelieves Cup, etc.)

## 🔧 Personnalisation

### Remplacer les Données
1. Remplacez le fichier `data/france_matches.csv` par vos propres données
2. Respectez le format des colonnes (voir README.md)
3. Relancez l'application (le cache se videra automatiquement)

### Modifier les Analyses
- **Pages** : Modifiez les fichiers dans `pages/`
- **Calculs** : Ajoutez des fonctions dans `utils/data_processing.py`
- **Graphiques** : Créez de nouvelles visualisations dans `utils/visualizations.py`

## ⚠️ Résolution de Problèmes

### L'application ne se lance pas
```bash
# Vérifiez Python
python --version

# Réinstallez les dépendances
pip install -r requirements.txt

# Testez l'installation
python test_installation.py
```

### Erreur "Module not found"
```bash
# Assurez-vous d'être dans le bon dossier
cd "Dashboard fff"

# Vérifiez la structure des fichiers
dir/ls
```

### Erreur de données
- Vérifiez que `data/france_matches.csv` existe
- Contrôlez le format des dates (YYYY-MM-DD)
- Assurez-vous que les colonnes requises sont présentes

### Performance lente
- Réduisez la période d'analyse avec le slider
- Limitez les types de compétition sélectionnés
- Vérifiez la taille du fichier CSV (recommandé < 1000 matchs)

## 📱 Fonctionnalités Clés

### 🏠 Page Accueil
- **KPIs temps réel** avec comparaisons historiques
- **Évolution performance** sur 4 dimensions
- **Analyse momentum** avec moyennes mobiles
- **Recommandations automatiques** basées sur les données

### 📊 Page Analyse  
- **Comparaisons internationales** : Performance vs principales nations
- **Avantage terrain** : Analyse domicile/extérieur/neutre
- **Patterns de jeu** : Distribution scores, style tactique
- **Performance par compétition** : Efficacité selon le contexte

### 💡 Page Insights
- **Tendances récentes** : Évolution 2 dernières années vs historique
- **Projections** : Objectifs recommandés et extrapolations
- **Benchmarking** : Positionnement vs standards mondiaux  
- **Plan d'action FFF** : Recommandations stratégiques prioritaires

## 🎨 Interface

### Couleurs FFF
- **Bleu France** : #0055A4 (éléments principaux)
- **Rouge** : #EF4135 (contrastes/alertes)  
- **Gris clair** : #F0F2F6 (zones neutres)

### Responsive Design
- ✅ **Desktop** : Affichage complet
- ✅ **Tablet** : Colonnes adaptées
- ✅ **Mobile** : Interface simplifiée

## 🚀 Prochaines Étapes

1. **Explorez les 3 pages** pour découvrir toutes les analyses
2. **Testez les filtres** pour voir l'impact sur les métriques
3. **Exportez les graphiques** en cliquant sur l'icône appareil photo
4. **Personnalisez avec vos données** en remplaçant le fichier CSV
5. **Adaptez les analyses** selon vos besoins spécifiques

## 💡 Conseils d'Utilisation

### Pour les Entraîneurs
- Focalisez sur la page **Analyse** pour les facteurs de performance
- Utilisez les **comparaisons par adversaire** pour préparer les matchs
- Analysez l'**avantage terrain** pour optimiser les stratégies

### Pour les Dirigeants
- Consultez la page **Insights** pour la vision stratégique
- Suivez les **projections** et objectifs recommandés
- Utilisez le **plan d'action FFF** pour les décisions d'investissement

### Pour les Analystes
- Exploitez tous les **filtres** pour des analyses ciblées
- Exportez les **graphiques** pour vos présentations
- Modifiez le **code** pour des analyses personnalisées

---

🇫🇷 **Bonne analyse des performances de l'équipe de France féminine !** ⚽
