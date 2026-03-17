import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard FFF - Équipe de France Féminine",
    page_icon="🇫🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour les couleurs Durabilis&Co + FFF
st.markdown("""
<style>
    /* Variables CSS pour les couleurs Durabilis */
    :root {
        --durabilis-light: #2ea9df;
        --durabilis-medium: #1970b4;
        --durabilis-dark: #2d3381;
        --durabilis-gradient: linear-gradient(135deg, #2ea9df 0%, #1970b4 50%, #2d3381 100%);
        --fff-blue: #0055A4;
        --fff-red: #EF4135;
        --fff-gradient: linear-gradient(90deg, #0055A4 0%, #EF4135 100%);
    }
    
    /* Header principal avec dégradé FFF */
    .main-header {
        background: var(--fff-gradient);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 85, 164, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" fill="white" opacity="0.1"><polygon points="0,0 1000,0 1000,60 0,100"/></svg>');
        pointer-events: none;
    }
    
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
        font-size: 2.5rem;
    }
    
    /* Logo et branding */
    .header-content {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .fff-logo {
        max-height: 80px;
        filter: brightness(0) invert(1);
        animation: logoFloat 3s ease-in-out infinite;
    }
    
    .durabilis-logo {
        max-height: 50px;
        filter: brightness(0) invert(1);
    }
    
    .title-section {
        text-align: center;
    }
    
    .title-main {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .title-sub {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
        font-weight: 300;
    }
    
    /* Animation pour le logo FFF */
    @keyframes logoFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    /* Cartes métriques avec couleurs Durabilis */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid var(--durabilis-medium);
        box-shadow: 0 2px 8px rgba(25, 112, 180, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(25, 112, 180, 0.15);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    /* Logos en bas de sidebar */
    .sidebar-logos {
        position: fixed;
        bottom: 1rem;
        left: 1rem;
        width: calc(100% - 2rem);
        max-width: 280px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        gap: 1rem;
        background: white;
        padding: 0.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        z-index: 1000;
    }
    
    .sidebar-logos img {
        max-height: 40px;
        max-width: 80px;
        object-fit: contain;
    }
    
    /* Navigation buttons */
    .nav-container {
        margin: 1rem 0;
    }
    
    .nav-button {
        display: block;
        width: 100%;
        margin-bottom: 0.5rem;
        padding: 1rem;
        border: none;
        border-radius: 10px;
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        color: #333;
        text-decoration: none;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        text-align: left;
        font-size: 1rem;
        border-left: 4px solid transparent;
    }
    
    .nav-button:hover {
        background: linear-gradient(145deg, #2ea9df, #1970b4);
        color: white;
        transform: translateX(5px);
        border-left-color: #2d3381;
    }
    
    .nav-button.active {
        background: linear-gradient(145deg, #1970b4, #2d3381);
        color: white;
        border-left-color: #2ea9df;
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(25, 112, 180, 0.3);
    }
    
    .nav-button.active:hover {
        background: linear-gradient(145deg, #2d3381, #1970b4);
    }
    
    .stSelectbox > div > div {
        background-color: white;
        border: 2px solid var(--durabilis-light);
        border-radius: 8px;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: var(--durabilis-medium);
        box-shadow: 0 0 0 2px rgba(46, 169, 223, 0.2);
    }
    
    /* Slider personnalisé */
    .stSlider > div > div > div {
        background: var(--durabilis-light);
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        border: 2px solid var(--durabilis-light);
        border-radius: 8px;
    }
    
    /* Boutons et interactions */
    .stButton > button {
        background: var(--durabilis-gradient);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(45, 51, 129, 0.2);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(145deg, var(--durabilis-light), var(--durabilis-medium));
        color: white;
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--durabilis-dark);
    }
    
    /* Footer avec branding Durabilis */
    .footer {
        background: var(--durabilis-gradient);
        color: white;
        text-align: center;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
    }
    
    .footer a {
        color: #2ea9df;
        text-decoration: none;
        font-weight: 500;
    }
    
    /* Animation pour les métriques */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .metric-card {
        animation: fadeInUp 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Header principal avec logos FFF et Durabilis
# Chargement des logos
try:
    import base64
    
    # Logo FFF
    with open("pngfff.png", "rb") as fff_file:
        fff_logo_data = base64.b64encode(fff_file.read()).decode()
    
    # Logo Durabilis
    durabilis_logo_data = ""
    try:
        with open("Logo-Durabilis_PNG.png", "rb") as durabilis_file:
            durabilis_logo_data = base64.b64encode(durabilis_file.read()).decode()
    except FileNotFoundError:
        pass
    
    # Header avec les deux logos
    st.markdown(f"""
    <div class="main-header">
        <div class="header-content">
            <img src="data:image/png;base64,{fff_logo_data}" class="fff-logo" alt="Logo FFF">
            <div class="title-section">
                <h1 class="title-main">🇫🇷 Dashboard FFF - Équipe de France Féminine ⚽</h1>
                <p class="title-sub">Analyse des performances • Powered by Durabilis&Co</p>
            </div>
            {f'<img src="data:image/png;base64,{durabilis_logo_data}" class="durabilis-logo" alt="Durabilis&Co">' if durabilis_logo_data else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
except FileNotFoundError:
    # Fallback si les logos ne sont pas trouvés
    st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="title-section">
                <h1 class="title-main">🇫🇷 Dashboard FFF - Équipe de France Féminine ⚽</h1>
                <p class="title-sub">Analyse des performances • Powered by Durabilis&Co</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
except FileNotFoundError:
    # Fallback si les logos ne sont pas trouvés
    st.markdown("""
    <div class="main-header">
        <div class="header-content">
            <div class="title-section">
                <h1 class="title-main">🇫🇷 Dashboard FFF - Équipe de France Féminine ⚽</h1>
                <p class="title-sub">Analyse des performances • Powered by Durabilis&Co</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Import des fonctions utilitaires
from utils.data_processing import load_and_process_data, calculate_performance_metrics, filter_data_by_period
from utils.visualizations import create_performance_evolution, create_comparison_charts, create_home_advantage_chart

# Chargement des données
@st.cache_data
def load_data():
    return load_and_process_data()

try:
    df = load_data()
    france_data = df.copy()
except Exception as e:
    st.error("⚠️ Erreur lors du chargement des données. Veuillez vérifier que le fichier CSV est présent dans le dossier 'data/'")
    st.info("📁 Structure attendue : data/france_matches.csv")
    st.stop()

# Sidebar avec logos FFF et Durabilis&Co en bas
# Navigation avec boutons personnalisés
st.sidebar.markdown("### 🧭 Navigation")

# Initialiser l'état de la page si ce n'est pas déjà fait
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Accueil"

# Créer les boutons de navigation
pages_info = [
    ("🏠 Accueil", "🏠", "Tableau de bord principal"),
    ("📊 Analyse", "📊", "Analyses approfondies"),
    ("💡 Insights", "💡", "Insights et tendances")
]

# Boutons de navigation stylés
for page_name, icon, description in pages_info:
    is_active = st.session_state.current_page == page_name
    
    # Bouton avec style conditionnel
    button_style = """
    background: linear-gradient(145deg, #1970b4, #2d3381);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px;
    margin: 5px 0;
    width: 100%;
    border-left: 4px solid #2ea9df;
    box-shadow: 0 4px 12px rgba(25, 112, 180, 0.3);
    """ if is_active else """
    background: linear-gradient(145deg, #f8f9fa, #e9ecef);
    color: #333;
    border: none;
    border-radius: 10px;
    padding: 12px;
    margin: 5px 0;
    width: 100%;
    border-left: 4px solid transparent;
    """
    
    if st.sidebar.button(
        f"{icon} {page_name.split(' ', 1)[1]}", 
        help=description,
        key=f"nav_{page_name}",
        use_container_width=True
    ):
        st.session_state.current_page = page_name
        st.rerun()

# Afficher la page actuelle
page = st.session_state.current_page

st.sidebar.markdown("---")

# Filtres globaux
st.sidebar.markdown("### 🔧 Filtres")
years = sorted([int(year) for year in france_data['year'].unique()])
year_range = st.sidebar.slider(
    "Période d'analyse",
    min_value=min(years),
    max_value=max(years),
    value=(max(years) - 10, max(years)),
    step=1
)

match_type = st.sidebar.multiselect(
    "Type de compétition",
    options=list(france_data['tournament'].unique()),
    default=list(france_data['tournament'].unique())
)

# Logos en bas de sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### Partenaires")

# Affichage des logos côte à côte en bas
try:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.image("pngfff.png", width=60, caption="FFF")
    with col2:
        st.image("Logo-Durabilis_PNG.png", width=60, caption="Durabilis&Co")
except:
    # Fallback avec texte si les images ne chargent pas
    st.sidebar.markdown("🇫🇷 **FFF** | 🏢 **Durabilis&Co**")

# Application des filtres
filtered_data = filter_data_by_period(france_data, year_range[0], year_range[1])
if match_type:
    filtered_data = filtered_data[filtered_data['tournament'].isin(match_type)]

# Affichage des pages
# if page == "🏠 Accueil":
#     from pages.accueil import show_accueil
#     show_accueil(filtered_data, france_data)
   
# elif page == "📊 Analyse":
#     from pages.analyse import show_analyse
#     show_analyse(filtered_data, france_data)
# elif page == "💡 Insights":
#     from pages.insights import show_insights
#     show_insights(filtered_data, france_data)

# Remplacez cette section dans votre app.py (lignes 75-82 environ)

# Affichage des pages
if page == "🏠 Accueil":
    try:
        from page_modules.accueil import show_accueil
        show_accueil(filtered_data, france_data)
    except Exception as e:
        st.error(f"Erreur lors du chargement de la page Accueil: {str(e)}")
        st.info("Vérifiez que le fichier page_modules/accueil.py existe et contient la fonction show_accueil")

elif page == "📊 Analyse":
    try:
        from page_modules.analyse import show_analyse
        show_analyse(filtered_data, france_data)
    except Exception as e:
        st.error(f"Erreur lors du chargement de la page Analyse: {str(e)}")
        st.info("Vérifiez que le fichier page_modules/analyse.py existe et contient la fonction show_analyse")

elif page == "💡 Insights":
    try:
        from page_modules.insights import show_insights
        show_insights(filtered_data, france_data)
    except Exception as e:
        st.error(f"Erreur lors du chargement de la page Insights: {str(e)}")
        st.info("Vérifiez que le fichier page_modules/insights.py existe et contient la fonction show_insights")


# Footer Durabilis&Co
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div style="flex: 1; text-align: left;">
            <h4 style="margin: 0; color: white;">Durabilis&Co</h4>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Solutions d'analyse de données sportives</p>
        </div>
        <div style="flex: 2; text-align: center;">
            <h3 style="margin: 0; color: white;">Dashboard FFF - Équipe de France Féminine</h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
                📅 Données mises à jour : {datetime.now().strftime("%d/%m/%Y")} | 
                📊 Analyses en temps réel | 
                ⚽ Performance et statistiques
            </p>
        </div>
        <div style="flex: 1; text-align: right;">
            <p style="margin: 0; font-size: 0.9em; opacity: 0.8;">
                Développé avec ❤️<br>
                par l'équipe Durabilis&Co
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
