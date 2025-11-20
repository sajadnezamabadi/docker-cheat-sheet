# Production Deployment Guide

Best practices for deploying Docker containers in production environments.

## Security Best Practices

### 1. Use Non-Root Users

```dockerfile
# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

### 2. Scan Images for Vulnerabilities

```bash
# Use Docker Scout or Trivy
docker scout cves <image>
# or
trivy image <image>
```

### 3. Use Secrets Management

```bash
# Docker Swarm secrets
echo "secret" | docker secret create db_password -

# Or use external secret managers
# - HashiCorp Vault
# - AWS Secrets Manager
# - Azure Key Vault
```

### 4. Limit Container Resources

```yaml
# docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 256M
```

## Monitoring & Logging

### 1. Container Logging

```yaml
# docker-compose.yml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 2. Health Checks

```dockerfile
# Dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

```yaml
# docker-compose.yml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### 3. Monitoring Tools

- **Prometheus + Grafana**: Metrics collection
- **ELK Stack**: Log aggregation
- **Datadog/New Relic**: APM and monitoring

## High Availability

### 1. Use Docker Swarm or Kubernetes

```bash
# Initialize Swarm
docker swarm init

# Create service with replicas
docker service create --replicas 3 --name web nginx
```

### 2. Load Balancing

```yaml
# docker-compose.yml with nginx load balancer
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    depends_on:
      - app1
      - app2
      - app3
```

## Backup & Restore

### 1. Volume Backups

```bash
# Backup volume
docker run --rm -v mydata:/data -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz /data

# Restore volume
docker run --rm -v mydata:/data -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /data
```

### 2. Database Backups

```bash
# PostgreSQL backup
docker exec postgres pg_dump -U user dbname > backup.sql

# MySQL backup
docker exec mysql mysqldump -u user dbname > backup.sql
```

## CI/CD Integration

### 1. GitHub Actions Example

```yaml
# .github/workflows/docker.yml
name: Build and Push
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Push to registry
        run: docker push myapp:${{ github.sha }}
```

### 2. GitLab CI Example

```yaml
# .gitlab-ci.yml
build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

## Environment Configuration

### 1. Use Environment Files

```bash
# .env file
DATABASE_URL=postgresql://user:pass@db:5432/db
REDIS_URL=redis://redis:6379
DEBUG=false
```

```yaml
# docker-compose.yml
services:
  app:
    env_file:
      - .env.production
```

### 2. Configuration Management

- Use config files mounted as volumes
- Use environment variables for secrets
- Consider using ConfigMaps (Kubernetes) or Docker Configs (Swarm)

## Performance Optimization

### 1. Image Optimization

```dockerfile
# Use multi-stage builds
# Use .dockerignore
# Minimize layers
# Use specific tags (not :latest)
```

### 2. Build Optimization

```bash
# Use BuildKit
DOCKER_BUILDKIT=1 docker build .

# Use cache mounts
RUN --mount=type=cache,target=/root/.npm npm install
```

## Deployment Strategies

### 1. Blue-Green Deployment

```bash
# Deploy new version
docker-compose -f docker-compose.blue.yml up -d

# Switch traffic
# Update load balancer config

# Stop old version
docker-compose -f docker-compose.green.yml down
```

### 2. Rolling Updates

```bash
# Docker Swarm
docker service update --image newimage:tag myservice

# Kubernetes
kubectl set image deployment/myapp myapp=newimage:tag
```
