@echo off
echo Starting AI Content Generator...
echo Recommended: Python 3.12 for optimal performance
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not available in PATH
    echo Please install Python 3.12+ from https://python.org
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version') do set python_version=%%i
echo Found Python %python_version%

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Dependencies installation failed
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found
    echo Create a .env file with: OPENAI_API_KEY=your_api_key
    echo.
)

echo.
echo Starting FastAPI server on port 8001...
echo Starting Streamlit frontend...
echo.
echo IMPORTANT: Two command windows will open
echo - FastAPI: http://localhost:8001
echo - Streamlit: http://localhost:8501
echo.
echo Press Ctrl+C in each window to stop the servers
echo.

REM Start FastAPI in a new window
start "FastAPI Server" cmd /k "python -m uvicorn app:app --reload --port 8001"

REM Wait 3 seconds for FastAPI to start
timeout /t 3 /nobreak >nul

REM Start Streamlit in a new window
start "Streamlit Frontend" cmd /k "streamlit run frontend.py"

echo.
echo Servers started successfully!
echo FastAPI: http://localhost:8001
echo Streamlit: http://localhost:8501
echo.
echo Note: For best performance, use Python 3.12+
echo For Docker deployment, use build_and_run.bat
echo.
pause