# Docker Troubleshooting Guide

Common Docker issues and their solutions for DevOps engineers.

## Container Issues

### Container Won't Start

```bash
# Check container logs
docker logs <container_name>

# Check container status
docker ps -a

# Inspect container configuration
docker inspect <container_name>

# Check if port is already in use
sudo lsof -i :8080
# or
netstat -tulpn | grep :8080
```

### Container Exits Immediately

```bash
# Run container interactively to see errors
docker run -it <image> /bin/sh

# Check exit code
docker inspect <container_name> | grep ExitCode

# View logs before container exits
docker logs <container_name>
```

### Permission Denied Errors

```bash
# Check file permissions in container
docker exec <container> ls -la /path/to/file

# Fix ownership
docker exec -u root <container> chown user:user /path/to/file

# Run container as specific user
docker run -u 1000:1000 <image>
```

## Network Issues

### Cannot Connect to Container

```bash
# Check if container is running
docker ps

# Check network configuration
docker network inspect bridge

# Test connectivity from host
docker exec <container> ping <target>

# Check port mapping
docker port <container>
```

### DNS Resolution Fails

```bash
# Use custom DNS
docker run --dns 8.8.8.8 <image>

# Check DNS in container
docker exec <container> cat /etc/resolv.conf

# Restart Docker daemon (if needed)
sudo systemctl restart docker
```

## Volume Issues

### Volume Not Mounting

```bash
# Check volume exists
docker volume ls

# Inspect volume
docker volume inspect <volume_name>

# Check mount point
docker inspect <container> | grep -A 10 Mounts

# Verify host path exists and has correct permissions
ls -la /host/path
```

### Data Loss After Container Restart

```bash
# Ensure you're using named volumes (not bind mounts for persistence)
docker run -v mydata:/app/data <image>

# Check volume is attached
docker inspect <container> | grep -A 5 Mounts
```

## Build Issues

### Build Fails with "No such file or directory"

```bash
# Check Dockerfile context
docker build -f Dockerfile .

# Verify files exist in build context
docker build --no-cache -t test .

# Check .dockerignore isn't excluding needed files
cat .dockerignore
```

### Build is Slow

```bash
# Use BuildKit
DOCKER_BUILDKIT=1 docker build .

# Leverage cache layers
# Order Dockerfile instructions from least to most frequently changing

# Use .dockerignore to exclude unnecessary files
```

### Out of Disk Space

```bash
# Check disk usage
docker system df

# Clean up unused resources
docker system prune -a

# Remove unused volumes (careful!)
docker volume prune
```

## Image Issues

### Image Too Large

```bash
# Use multi-stage builds
# Use alpine/minimal base images
# Remove unnecessary packages in same RUN command
# Use .dockerignore

# Analyze image layers
docker history <image>

# Check image size
docker images
```

### Cannot Pull Image

```bash
# Check internet connection
ping registry-1.docker.io

# Login to registry
docker login

# Try pulling with full tag
docker pull <image>:<tag>

# Check registry authentication
cat ~/.docker/config.json
```

## Docker Compose Issues

### Services Won't Start

```bash
# Validate compose file
docker-compose config

# Check service dependencies
docker-compose ps

# View logs for all services
docker-compose logs

# Start services one by one
docker-compose up <service_name>
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :8080
# or
sudo netstat -tulpn | grep :8080

# Change port in docker-compose.yml
ports:
  - "8081:8080"  # Use different host port
```

### Environment Variables Not Working

```bash
# Check environment variables
docker-compose config

# Verify .env file exists and is loaded
docker-compose config | grep -A 5 environment

# Test with explicit env vars
docker-compose run -e KEY=value <service>
```

## Performance Issues

### High CPU Usage

```bash
# Monitor container resources
docker stats

# Limit CPU usage
docker run --cpus="1.5" <image>

# In docker-compose.yml:
deploy:
  resources:
    limits:
      cpus: '1.5'
```

### High Memory Usage

```bash
# Monitor memory
docker stats

# Limit memory
docker run -m 512m <image>

# In docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 512M
```

## Security Issues

### Running as Root

```bash
# Create non-root user in Dockerfile
RUN useradd -m -u 1000 appuser
USER appuser

# Run container as specific user
docker run -u 1000:1000 <image>
```

### Exposed Secrets

```bash
# Use Docker secrets (Swarm mode)
echo "secret" | docker secret create my_secret -

# Use environment files (not in image)
docker run --env-file .env <image>

# Never commit .env files to git
```

## Debugging Commands

```bash
# Get into running container
docker exec -it <container> /bin/sh

# Execute command in stopped container
docker run --rm -it <image> /bin/sh

# Inspect container configuration
docker inspect <container> | jq

# View container processes
docker top <container>

# Check container resource usage
docker stats <container>

# View Docker daemon logs
sudo journalctl -u docker.service
# or
sudo tail -f /var/log/docker.log
```

## Common Error Messages

### "Cannot connect to the Docker daemon"

```bash
# Check Docker service is running
sudo systemctl status docker

# Start Docker service
sudo systemctl start docker

# Add user to docker group
sudo usermod -aG docker $USER
# Then logout and login again
```

### "No space left on device"

```bash
# Clean up Docker
docker system prune -a --volumes

# Check disk space
df -h

# Remove old images
docker image prune -a
```

### "Bind for 0.0.0.0:8080 failed: port is already allocated"

```bash
# Find process using port
sudo lsof -i :8080

# Kill process or change port
sudo kill -9 <PID>
```

## Getting Help

```bash
# Docker version info
docker version

# System information
docker info

# Check Docker daemon
sudo systemctl status docker

# View Docker logs
sudo journalctl -u docker.service -f
```

