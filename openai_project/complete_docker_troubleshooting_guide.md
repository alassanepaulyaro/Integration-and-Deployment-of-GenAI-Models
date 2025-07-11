# Complete Docker & Troubleshooting Guide

## 🚀 Docker Commands Reference

### Quick Start Commands

#### Production Deployment (Recommended)
```bash
# Start both services
docker-compose up --build

# Start in background
docker-compose up -d --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
```

#### Development with Hot Reload
```bash
# Start with development configuration
docker-compose -f docker-compose.dev.yml up --build

# Enable hot reload for code changes
# Changes to app.py and frontend.py will auto-reload

# Stop development services
docker-compose -f docker-compose.dev.yml down
```

#### Version 3.8 Enhanced Features
```bash
# View resource usage (new in 3.8)
docker-compose top

# Check service health status
docker-compose ps

# View container resource stats
docker stats

# View configuration with resource limits
docker-compose config

# Check dependency health
docker-compose logs backend
docker-compose logs frontend
```

### Build Individual Services
```bash
# Build backend only
docker-compose build backend

# Build frontend only
docker-compose build frontend

# Build both
docker-compose build
```

### Service Management
```bash
# Start specific service
docker-compose up backend

# Restart specific service
docker-compose restart backend

# Stop specific service
docker-compose stop frontend

# Remove specific service
docker-compose rm frontend
```

### Development Commands
```bash
# Rebuild and restart
docker-compose down && docker-compose up --build

# Follow logs in real-time
docker-compose logs -f backend

# Execute commands in running container
docker-compose exec backend bash
docker-compose exec frontend bash

# Check service status
docker-compose ps
```

### Rebuild Commands
```bash
# Stop containers
docker-compose down

# Rebuild without cache to force fresh build
docker-compose build --no-cache frontend

# Rebuild specific service without cache
docker-compose build --no-cache backend

# Rebuild all services without cache
docker-compose build --no-cache

# Start everything
docker-compose up

# Rebuild and start in one command
docker-compose up --build --force-recreate
```

### Cleanup Commands
```bash
# Remove containers and networks
docker-compose down

# Remove containers, networks, and volumes
docker-compose down -v

# Remove everything including images
docker-compose down --rmi all

# Clean up unused Docker resources
docker system prune -a
```

### Resource Monitoring (Version 3.8 Features)
```bash
# View live resource usage
docker stats

# View service resource usage
docker-compose top

# Check container health status
docker-compose ps

# View detailed service information
docker-compose config

# Monitor logs with resource info
docker-compose logs -f --tail=50

# Check system resource usage
docker system df
docker system events --filter container=<container_name>
```

### Advanced Health Checks
```bash
# Test backend health manually
curl -f http://localhost:8001/

# Test frontend health manually
curl -f http://localhost:8501/_stcore/health

# Check health from within network
docker-compose exec frontend curl -f http://backend:8001/

# View health check history
docker inspect <container_name> | grep -A 10 "Health"
```

## 🧪 Network Connectivity Tests

### Test Docker Network Connectivity

#### Test if Frontend Can Reach Backend
```bash
# Test if frontend can reach backend by service name
docker-compose exec frontend curl -f http://backend:8001/

# Expected output: {"message":"FastAPI server is running. Use /generate endpoint for content generation."}

# Test backend health from frontend container
docker-compose exec frontend curl -f http://backend:8001/

# Test with actual generate endpoint
docker-compose exec frontend curl -X POST http://backend:8001/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "hello"}'
```

#### Check Environment Variables
```bash
# Check if BACKEND_HOST is set correctly in frontend container
docker-compose exec frontend env | grep BACKEND

# Expected output: BACKEND_HOST=backend
```

#### Debug Network
```bash
# List Docker networks
docker network ls

# Inspect the app network
docker network inspect openai_project_app-network

# Check container IPs
docker-compose exec frontend hostname -i
docker-compose exec backend hostname -i
```

#### Test from Host
```bash
# Test backend from host
curl http://localhost:8001/

# Test frontend from host  
curl http://localhost:8501/_stcore/health

# Test generate endpoint from host
curl -X POST http://localhost:8001/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "hello"}'
```

### Manual Network Testing
```bash
# Create a test network
docker network create test-network

# Run backend manually
docker run -d --name test-backend --network test-network -p 8001:8001 --env-file .env openai_project-backend

# Run frontend manually  
docker run -d --name test-frontend --network test-network -p 8501:8501 -e BACKEND_HOST=test-backend openai_project-frontend

# Test connection
docker exec test-frontend curl -f http://test-backend:8001/

# Cleanup
docker stop test-backend test-frontend
docker rm test-backend test-frontend
docker network rm test-network
```

## 🚨 Connection Error Troubleshooting Guide

### Error: Connection Refused to Backend

#### Error Message
```
Error: HTTPConnectionPool(host='localhost', port=8001): Max retries exceeded with url: /generate
(Caused by NewConnectionError: Failed to establish a new connection: [Errno 111] Connection refused))
```

#### Root Cause
The Streamlit frontend (port 8501) cannot connect to the FastAPI backend (port 8001) because the backend is not running or networking is misconfigured.

### Solution Steps

#### Step 1: Check What's Running
```bash
# Check if anything is running on port 8001 (backend)
netstat -an | grep 8001
# Or on Windows
netstat -an | findstr 8001

# Check if anything is running on port 8501 (frontend)
netstat -an | grep 8501
# Or on Windows  
netstat -an | findstr 8501

# Check Docker containers
docker-compose ps
```

#### Step 2: Choose Your Deployment Method

##### Method A: Docker Compose (Recommended)
```bash
# Stop any running containers first
docker-compose down

# Start both services together
docker-compose up --build

# Check if both services are running
docker-compose ps

# View logs if there are issues
docker-compose logs backend
docker-compose logs frontend
```

##### Method B: Local Development (2 Services)
```bash
# Terminal 1 - Start Backend
python -m uvicorn app:app --reload --port 8001

# Terminal 2 - Start Frontend (after backend is running)
streamlit run frontend.py

# Or use the Windows script
start_servers.bat
```

#### Step 3: Verify Both Services Are Running

##### Check Backend Health
```bash
# Should return: {"message": "FastAPI server is running..."}
curl http://localhost:8001/

# Or in browser: http://localhost:8001
# Should show FastAPI welcome message
```

##### Check Frontend Access
```bash
# Should return Streamlit health status
curl http://localhost:8501/_stcore/health

# Or in browser: http://localhost:8501
# Should show the AI Content Generator interface
```

#### Step 4: Test the Connection
1. Open http://localhost:8501 in browser
2. Enter a simple prompt like "hello"
3. Click "Generate"
4. Should get response from OpenAI (if API key is set)

### Common Issues and Fixes

#### Issue 1: Backend Won't Start
```bash
# Check Python version (needs 3.7+, recommended 3.12+)
python --version

# Check if required packages are installed
pip install -r requirements.txt

# Check if .env file exists with API key
cat .env  # Linux/Mac
type .env  # Windows

# Manual backend start with debug
python -m uvicorn app:app --reload --port 8001 --log-level debug
```

#### Issue 2: Docker Issues
```bash
# Check Docker is running
docker version

# Check Docker Compose is available
docker-compose --version

# Clean up and rebuild
docker-compose down
docker system prune -f
docker-compose up --build

# Check container status
docker-compose ps
```

#### Issue 3: Port Conflicts
```bash
# Kill anything using port 8001
# Linux/Mac
sudo lsof -ti:8001 | xargs kill -9

# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# Kill anything using port 8501
# Linux/Mac  
sudo lsof -ti:8501 | xargs kill -9

# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

#### Issue 4: Environment Variables
```bash
# Check if .env file exists
ls -la .env  # Linux/Mac
dir .env     # Windows

# Verify .env file content
cat .env     # Linux/Mac
type .env    # Windows

# Should contain:
# OPENAI_API_KEY=your_actual_api_key_here

# Test environment variable loading
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

#### Issue 5: BACKEND_HOST Not Set
```bash
# Check if environment variable is set
docker-compose exec frontend printenv BACKEND_HOST

# If not set, rebuild with:
docker-compose down
docker-compose up --build
```

#### Issue 6: Network Isolation
```bash
# Both containers should be on same network
docker-compose exec frontend ping backend
docker-compose exec backend ping frontend
```

#### Issue 7: DNS Resolution
```bash
# Test DNS resolution in frontend container
docker-compose exec frontend nslookup backend
docker-compose exec frontend getent hosts backend
```

### Quick Fix Commands

#### Option A: Restart with Clean Build
```bash
docker-compose down
docker system prune -f
docker-compose up --build
```

#### Option B: Force Recreate Containers
```bash
docker-compose down
docker-compose up --build --force-recreate
```

#### Option C: Rebuild Without Cache
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Verification Checklist

- [ ] Backend running on port 8001
- [ ] Frontend running on port 8501  
- [ ] .env file exists with OPENAI_API_KEY
- [ ] Both services can communicate
- [ ] No port conflicts
- [ ] Docker/Python properly installed

### Expected Results

#### Successful Network Test
```bash
$ docker-compose exec frontend curl -f http://backend:8001/
{"message":"FastAPI server is running. Use /generate endpoint for content generation."}

$ docker-compose exec frontend env | grep BACKEND
BACKEND_HOST=backend

$ docker-compose exec frontend curl -X POST http://backend:8001/generate -H "Content-Type: application/json" -d '{"prompt": "hello"}'
{"response":"Hello! How can I assist you today?"}
```

#### Frontend Debug Output
When you open http://localhost:8501, you should see in the debug section:
- Backend Host: backend
- API URL: http://backend:8001/generate
- BACKEND_HOST: backend

## 🆘 Still Having Issues?

### Check Logs
```bash
# Docker Compose logs
docker-compose logs -f

# Individual service logs
docker-compose logs backend
docker-compose logs frontend

# Local development logs
# Check the terminal windows where you started the services
```

### Network Connectivity Test
```bash
# From frontend container to backend (Docker)
docker-compose exec frontend curl -f http://backend:8001/

# From host to both services
curl http://localhost:8001/
curl http://localhost:8501/_stcore/health
```

### Environment Check
```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(fastapi|streamlit|openai|uvicorn)"

# Check Docker
docker --version
docker-compose --version
```

## 💡 Pro Tips

1. **Always start backend before frontend** in local development
2. **Use Docker Compose** for the most reliable experience
3. **Check logs** when services fail to start
4. **Verify .env file** exists and contains valid API key
5. **Ensure no port conflicts** before starting services
6. **Use rebuild commands** when code changes don't take effect
7. **Test network connectivity** when frontend can't reach backend

## Manual Docker Commands

### Backend
```bash
# Build
docker build -f Dockerfile.backend -t ai-backend .

# Run
docker run -d -p 8001:8001 --env-file .env --name ai-backend ai-backend

# Stop
docker stop ai-backend
docker rm ai-backend
```

### Frontend
```bash
# Build
docker build -f Dockerfile.frontend -t ai-frontend .

# Run
docker run -d -p 8501:8501 --name ai-frontend ai-frontend

# Stop
docker stop ai-frontend
docker rm ai-frontend
```

### Networking
```bash
# Create network
docker network create ai-network

# Run with network
docker run -d --network ai-network -p 8001:8001 --env-file .env --name ai-backend ai-backend
docker run -d --network ai-network -p 8501:8501 -e BACKEND_HOST=ai-backend --name ai-frontend ai-frontend
```

## Security Considerations

### Why Volumes Are Commented Out
The `# - .:/app` volumes mount is commented out for security:

```yaml
# ❌ NEVER DO THIS IN PRODUCTION
volumes:
  - .:/app  # Exposes ALL files including secrets

# ✅ SECURE APPROACH
volumes:
  - ./app.py:/app/app.py          # Only specific files
  - ./frontend.py:/app/frontend.py # Only what's needed
  # Never mount .env, .git, or sensitive files
```

### Files to NEVER Mount
```bash
# These files contain sensitive data
.env                 # API keys and secrets
.git/                # Source control history
.DS_Store           # OS metadata
*.key, *.pem        # Certificates
secrets/            # Secret directories
```

### Safe Development Mounting
```yaml
# ✅ SAFE for development
volumes:
  - ./app.py:/app/app.py
  - ./frontend.py:/app/frontend.py
  - ./requirements.txt:/app/requirements.txt

# ❌ UNSAFE - never mount these
# - ./.env:/app/.env              # API keys exposed
# - ./.git:/app/.git              # Source history exposed
# - .:/app                        # Everything exposed
```

## Environment Variables

### Backend (.env file)
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Frontend (Docker Compose)
```env
BACKEND_HOST=backend  # Service name in Docker Compose
```

## Health Checks

### Check Backend Health
```bash
curl http://localhost:8001/
```

### Check Frontend Health
```bash
curl http://localhost:8501/_stcore/health
```

### Check from within containers
```bash
# From frontend container to backend
docker-compose exec frontend curl -f http://backend:8001/

# From host to services
docker-compose exec backend curl -f http://localhost:8001/
docker-compose exec frontend curl -f http://localhost:8501/_stcore/health
```