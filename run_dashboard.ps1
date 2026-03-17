# Script PowerShell pour lancer le Dashboard FFF
# Équipe de France Féminine - Analyses et Performance

Write-Host "🚀 Dashboard FFF - Équipe de France Féminine" -ForegroundColor Blue
Write-Host "================================================" -ForegroundColor Blue
Write-Host ""

# Vérification du dossier de travail
Write-Host "📁 Dossier de travail: $PWD" -ForegroundColor Green
Write-Host ""

# Vérification de Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "🐍 Python détecté: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python non trouvé. Veuillez installer Python 3.8+" -ForegroundColor Red
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

# Activation de l'environnement virtuel si disponible
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "🔧 Activation de l'environnement virtuel..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "⚠️  Environnement virtuel non trouvé, utilisation de Python global" -ForegroundColor Yellow
}

Write-Host ""

# Test des dépendances
Write-Host "🧪 Test des dépendances..." -ForegroundColor Cyan
try {
    python test_installation.py
} catch {
    Write-Host "❌ Erreur lors du test des dépendances" -ForegroundColor Red
    Write-Host "💡 Essayez: pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "Appuyez sur Entrée pour continuer quand même"
}

Write-Host ""
Write-Host "🌐 Lancement de l'application Streamlit..." -ForegroundColor Cyan
Write-Host "📍 L'application sera accessible sur: http://localhost:8501" -ForegroundColor Green
Write-Host "🛑 Appuyez sur Ctrl+C pour arrêter l'application" -ForegroundColor Yellow
Write-Host ""

# Lancement de Streamlit
try {
    streamlit run app.py
} catch {
    Write-Host "❌ Erreur lors du lancement de Streamlit" -ForegroundColor Red
    Write-Host "💡 Vérifiez que Streamlit est installé: pip install streamlit" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "👋 Application fermée. Merci d'avoir utilisé le Dashboard FFF !" -ForegroundColor Blue
Read-Host "Appuyez sur Entrée pour quitter"
