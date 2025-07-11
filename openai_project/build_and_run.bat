@echo off
echo Building and running AI Content Generator with Docker...
echo Using Python 3.12 and Docker Compose 3.8
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not available in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Check Docker Compose version
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker Compose is not installed or not available in PATH
    echo Please install Docker Desktop which includes Docker Compose
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found
    echo Create a .env file with: OPENAI_API_KEY=your_api_key
    echo.
    echo Do you want to continue without .env file? (y/n)
    set /p continue=
    if /i not "%continue%"=="y" (
        echo Cancelled. Create .env file and try again.
        pause
        exit /b 1
    )
)

echo.
echo Building Docker image with Python 3.12...
docker build -t ai-content-generator .
if %errorlevel% neq 0 (
    echo ERROR: Docker build failed
    pause
    exit /b 1
)

echo.
echo Starting container...
echo.
echo IMPORTANT: The application will be available at:
echo - Frontend: http://localhost:8501
echo - Backend: http://localhost:8001
echo - API Documentation: http://localhost:8001/docs
echo.
echo Features:
echo - Python 3.12 for improved performance
echo - FastAPI + Streamlit architecture
echo - OpenAI GPT-4.1-nano integration
echo.
echo Press Ctrl+C to stop the container
echo.

REM Run the container
if exist .env (
    docker run -p 8001:8001 -p 8501:8501 --env-file .env ai-content-generator
) else (
    docker run -p 8001:8001 -p 8501:8501 ai-content-generator
)

echo.
echo Container stopped.
pause