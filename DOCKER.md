# Docker Deployment Guide

## Quick Start with Docker

### Using Docker Compose (Recommended)

1. **Setup environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Start the service:**
   ```bash
   docker-compose up -d
   ```

3. **Check logs:**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the service:**
   ```bash
   docker-compose down
   ```

### Using Docker directly

1. **Build the image:**
   ```bash
   docker build -t ai-agent-system .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name ai-agent \
     -p 5000:5000 \
     --env-file .env \
     ai-agent-system
   ```

3. **View logs:**
   ```bash
   docker logs -f ai-agent
   ```

## Health Check

The container includes a health check that monitors the API endpoint:

```bash
docker ps
# Look for "healthy" status
```

## Accessing the API

Once running, the API is available at:
- http://localhost:5000/health
- http://localhost:5000/agents

## Troubleshooting

### Container won't start
Check logs:
```bash
docker-compose logs
```

### API not responding
1. Check if container is healthy: `docker ps`
2. Check logs: `docker-compose logs -f`
3. Verify .env configuration

### Port already in use
Change the port in docker-compose.yml or use:
```bash
SERVER_PORT=8000 docker-compose up -d
```
