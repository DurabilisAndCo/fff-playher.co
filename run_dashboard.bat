@echo off
echo 🚀 Lancement du Dashboard FFF - Equipe de France Feminine
echo.
echo 📁 Dossier de travail: %CD%
echo.

REM Activation de l'environnement virtuel si il existe
if exist .venv\Scripts\activate.bat (
    echo 🔧 Activation de l'environnement virtuel...
    call .venv\Scripts\activate.bat
) else (
    echo ⚠️  Environnement virtuel non trouvé, utilisation de Python global
)

echo.
echo 🧪 Test des dépendances...
python test_installation.py

echo.
echo 🌐 Lancement de l'application Streamlit...
echo 📍 L'application sera accessible sur: http://localhost:8501
echo 🛑 Appuyez sur Ctrl+C pour arrêter l'application
echo.

streamlit run app.py

pause
