#!/bin/bash
set -e

echo "🚀 Starting AI Content Generator..."
echo "Recommended: Python 3.12 for optimal performance"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ ERROR: Python is not installed or not available in PATH"
    echo "Please install Python 3.12+ from https://python.org"
    exit 1
fi

# Use python3 if available, fallback to python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo "✅ Found Python $PYTHON_VERSION"

# Install dependencies
echo "📦 Installing dependencies..."
$PYTHON_CMD -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ ERROR: Dependencies installation failed"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️ WARNING: .env file not found"
    echo "Create a .env file with: OPENAI_API_KEY=your_api_key"
    echo ""
fi

echo ""
echo "🚀 Starting FastAPI server on port 8001..."
echo "🌐 Starting Streamlit frontend on port 8501..."
echo ""
echo "📍 IMPORTANT: Two terminal windows will open"
echo "   - FastAPI Backend: http://localhost:8001"
echo "   - Streamlit Frontend: http://localhost:8501"
echo ""
echo "🛑 Press Ctrl+C in each terminal to stop the servers"
echo ""

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    if [ ! -z "$FASTAPI_PID" ]; then
        kill $FASTAPI_PID 2>/dev/null || true
    fi
    if [ ! -z "$STREAMLIT_PID" ]; then
        kill $STREAMLIT_PID 2>/dev/null || true
    fi
    echo "✅ Services stopped"
    exit 0
}

# Set trap for cleanup on script exit
trap cleanup SIGINT SIGTERM

# Check if we're in a terminal that supports opening new windows
if [ -n "$TERM" ] && [ "$TERM" != "dumb" ]; then
    # Try to open new terminal windows (OS-specific)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # MacOS
        osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && python3 -m uvicorn app:app --reload --port 8001"' 2>/dev/null || {
            echo "Could not open new Terminal window. Running in background..."
            $PYTHON_CMD -m uvicorn app:app --reload --port 8001 &
            FASTAPI_PID=$!
        }
        
        sleep 3
        
        osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && streamlit run frontend.py"' 2>/dev/null || {
            echo "Could not open new Terminal window for Streamlit. Running in background..."
            streamlit run frontend.py &
            STREAMLIT_PID=$!
        }
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux - try different terminal emulators
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "cd '$PWD' && $PYTHON_CMD -m uvicorn app:app --reload --port 8001; exec bash" 2>/dev/null || {
                echo "Running FastAPI in background..."
                $PYTHON_CMD -m uvicorn app:app --reload --port 8001 &
                FASTAPI_PID=$!
            }
            sleep 3
            gnome-terminal -- bash -c "cd '$PWD' && streamlit run frontend.py; exec bash" 2>/dev/null || {
                echo "Running Streamlit in background..."
                streamlit run frontend.py &
                STREAMLIT_PID=$!
            }
        elif command -v xterm &> /dev/null; then
            xterm -e "cd '$PWD' && $PYTHON_CMD -m uvicorn app:app --reload --port 8001" &
            sleep 3
            xterm -e "cd '$PWD' && streamlit run frontend.py" &
        else
            echo "No supported terminal emulator found. Running services in background..."
            $PYTHON_CMD -m uvicorn app:app --reload --port 8001 &
            FASTAPI_PID=$!
            sleep 3
            streamlit run frontend.py &
            STREAMLIT_PID=$!
        fi
    else
        # Other Unix systems or unsupported
        echo "Running services in background..."
        $PYTHON_CMD -m uvicorn app:app --reload --port 8001 &
        FASTAPI_PID=$!
        sleep 3
        streamlit run frontend.py &
        STREAMLIT_PID=$!
    fi
else
    # No terminal or dumb terminal - run in background
    echo "Running services in background..."
    $PYTHON_CMD -m uvicorn app:app --reload --port 8001 &
    FASTAPI_PID=$!
    sleep 3
    streamlit run frontend.py &
    STREAMLIT_PID=$!
fi

echo ""
echo "✅ Servers started successfully!"
echo "   - FastAPI Backend: http://localhost:8001"
echo "   - Streamlit Frontend: http://localhost:8501"
echo "   - API Documentation: http://localhost:8001/docs"
echo ""
echo "💡 Note: For best performance, use Python 3.12+"
echo "🐳 For Docker deployment, use: ./build_and_run.sh"
echo ""

# If we have background processes, wait for them
if [ ! -z "$FASTAPI_PID" ] || [ ! -z "$STREAMLIT_PID" ]; then
    echo "Services running in background. Press Ctrl+C to stop."
    wait
fi