# 🎨 Guide de Style Durabilis&Co - Dashboard FFF

## 🏢 Identité Visuelle

### Logo
- **Fichier** : `Logo-Durabilis_PNG.png`
- **Utilisation** : Header principal et sidebar
- **Taille recommandée** : 60px (header), 120px (sidebar)

### Couleurs Principales

```css
/* Palette Durabilis&Co */
--durabilis-light:  #2ea9df  /* Bleu clair */
--durabilis-medium: #1970b4  /* Bleu moyen */
--durabilis-dark:   #2d3381  /* Bleu foncé */
```

#### Usage des Couleurs
- **Bleu moyen (#1970b4)** : Couleur principale, boutons, liens
- **Bleu clair (#2ea9df)** : Accents, hover states, éléments secondaires  
- **Bleu foncé (#2d3381)** : Textes importants, borders, contrastes

### Dégradés
```css
/* Dégradé principal */
background: linear-gradient(135deg, #2ea9df 0%, #1970b4 50%, #2d3381 100%);

/* Dégradé léger */
background: linear-gradient(135deg, #2ea9df 0%, #1970b4 100%);

/* Dégradé sombre */
background: linear-gradient(135deg, #1970b4 0%, #2d3381 100%);
```

## 🎯 Composants Design

### Header Principal
- Dégradé Durabilis avec overlay subtil
- Logo en blanc (filtre brightness/invert)
- Typography centrée avec ombre
- Padding généreux et border-radius moderne

### Cartes Métriques
- Dégradé subtil blanc vers gris clair
- Border-left coloré (bleu moyen)
- Hover effects avec élévation
- Animation fadeInUp au chargement

### Sidebar
- Logo Durabilis en haut
- Éléments avec borders colorés
- Focus states avec couleurs Durabilis
- Background dégradé léger

### Footer
- Layout en 3 colonnes
- Informations Durabilis&Co
- Couleurs inversées (blanc sur bleu)
- Responsive avec flex-wrap

## 📊 Visualisations

### Couleurs Plotly
```python
COLORS = {
    'primary': '#1970b4',     # Bleu moyen
    'secondary': '#2ea9df',   # Bleu clair  
    'accent': '#2d3381',      # Bleu foncé
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545'
}
```

### Échelle de Couleurs
- Utilisation cohérente des 3 bleus Durabilis
- Dégradés pour les graphiques en aires
- Couleurs système pour status (succès, warning, danger)

## 🔧 Implémentation Technique

### Structure CSS
1. **Variables CSS** : Définition centralisée des couleurs
2. **Composants modulaires** : Styles réutilisables
3. **Animations subtiles** : Transitions et hover effects
4. **Responsive design** : Adaptation mobile/desktop

### Fichiers Modifiés
- `app.py` : CSS principal et header
- `utils/visualizations.py` : Couleurs des graphiques
- `utils/durabilis_theme.py` : Configuration centralisée

## 🎨 Bonnes Pratiques

### Cohérence
- Utiliser les variables CSS définies
- Respecter la hiérarchie des couleurs
- Maintenir les proportions et espacements

### Performance
- Optimisation des images (logo)
- CSS efficient avec variables
- Animations légères

### Accessibilité
- Contrastes suffisants
- Lisibilité des textes
- Navigation claire

## 🚀 Déploiement

### Vérifications Avant Mise en Production
1. ✅ Logo Durabilis présent et affiché
2. ✅ Couleurs cohérentes dans tous les composants
3. ✅ Responsive design fonctionnel
4. ✅ Performance des animations
5. ✅ Tests sur différents navigateurs

### Commandes de Test
```bash
# Test du design
python test_durabilis_design.py

# Lancement du dashboard
streamlit run app.py
```

---

**Développé par Durabilis&Co** 🏢  
*Solutions d'analyse de données sportives*

Dashboard FFF - Équipe de France Féminine ⚽  
*Analyse des performances avec style et professionnalisme*
