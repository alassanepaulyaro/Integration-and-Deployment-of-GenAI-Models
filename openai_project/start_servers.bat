@echo off
echo Starting AI Content Generator...
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python n'est pas installé ou non disponible dans le PATH
    pause
    exit /b 1
)

REM Installer les dépendances
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Installation des dépendances échouée
    pause
    exit /b 1
)

REM Vérifier si le fichier .env existe
if not exist .env (
    echo WARNING: Fichier .env introuvable
    echo Créez un fichier .env avec: OPENAI_API_KEY=votre_clé_api
    echo.
)

echo.
echo Starting FastAPI server on port 8001...
echo Starting Streamlit frontend...
echo.
echo IMPORTANT: Deux fenêtres de commande vont s'ouvrir
echo - FastAPI: http://localhost:8001
echo - Streamlit: http://localhost:8501
echo.
echo Press Ctrl+C dans chaque fenêtre pour arrêter les serveurs
echo.

REM Lancer FastAPI dans une nouvelle fenêtre
start "FastAPI Server" cmd /k "python -m uvicorn app:app --reload --port 8001"

REM Attendre 3 secondes pour que FastAPI démarre
timeout /t 3 /nobreak >nul

REM Lancer Streamlit dans une nouvelle fenêtre
start "Streamlit Frontend" cmd /k "streamlit run frontend.py"

echo.
echo Servers started successfully!
echo FastAPI: http://localhost:8001
echo Streamlit: http://localhost:8501
echo.
pause