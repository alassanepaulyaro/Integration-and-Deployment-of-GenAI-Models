#!/bin/bash
set -e

echo "🚀 Building and running AI Content Generator with Docker..."
echo "🐍 Using Python 3.12 and Docker Compose 3.8"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ ERROR: Docker is not installed or not available in PATH"
    echo "Please install Docker from https://www.docker.com/get-started"
    exit 1
fi

# Check Docker Compose version
if ! command -v docker-compose &> /dev/null; then
    echo "❌ ERROR: Docker Compose is not installed or not available in PATH"
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️ WARNING: .env file not found"
    echo "Create a .env file with: OPENAI_API_KEY=your_api_key"
    echo ""
    read -p "Do you want to continue without .env file? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled. Create .env file and try again."
        exit 1
    fi
fi

echo ""
echo "🔨 Building Docker images with Python 3.12..."
docker-compose build
if [ $? -ne 0 ]; then
    echo "❌ ERROR: Docker build failed"
    exit 1
fi

echo ""
echo "🚀 Starting containers..."
echo ""
echo "📍 IMPORTANT: The application will be available at:"
echo "   - Frontend: http://localhost:8501"
echo "   - Backend: http://localhost:8001"
echo "   - API Documentation: http://localhost:8001/docs"
echo ""
echo "✨ Features:"
echo "   - Python 3.12 for improved performance"
echo "   - FastAPI + Streamlit architecture"
echo "   - OpenAI GPT-4.1-nano integration"
echo "   - Docker containerized deployment"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Function to handle cleanup
cleanup() {
    echo ""
    echo "🛑 Stopping containers..."
    docker-compose down
    echo "✅ Containers stopped successfully"
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Start the containers
docker-compose up

echo ""
echo "✅ Containers stopped."
echo "To restart: docker-compose up"
echo "To rebuild: docker-compose up --build"