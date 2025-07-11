# Docker Commands Reference

# Docker Commands Reference

## Quick Start Commands

### Production Deployment (Recommended)
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

### Development with Hot Reload
```bash
# Start with development configuration
docker-compose -f docker-compose.dev.yml up --build

# Enable hot reload for code changes
# Changes to app.py and frontend.py will auto-reload

# Stop development services
docker-compose -f docker-compose.dev.yml down
```

### Version 3.8 Enhanced Features
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