# Docker CLI Cheat Sheet

## Container Management

### Run Containers
```bash
# Run a container
docker run <image>

# Run in detached mode
docker run -d <image>

# Run with name
docker run --name my-container <image>

# Run with port mapping
docker run -p 8080:80 <image>

# Run with volume mount
docker run -v /host/path:/container/path <image>

# Run with environment variables
docker run -e KEY=value <image>

# Run with interactive terminal
docker run -it <image>

# Run with all options
docker run -d -p 8080:80 -v /data:/app/data -e ENV=prod --name my-app <image>
```

### Container Lifecycle
```bash
# Start a container
docker start <container>

# Stop a container
docker stop <container>

# Restart a container
docker restart <container>

# Pause a container
docker pause <container>

# Unpause a container
docker unpause <container>

# Remove a container
docker rm <container>

# Force remove a running container
docker rm -f <container>

# Remove all stopped containers
docker container prune
```

### Container Information
```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Show container logs
docker logs <container>

# Follow logs
docker logs -f <container>

# Show last N lines
docker logs --tail 100 <container>

# Execute command in container
docker exec -it <container> <command>

# Enter container shell
docker exec -it <container> /bin/bash

# Show container stats
docker stats

# Show container details
docker inspect <container>

# Show container processes
docker top <container>
```

## Image Management

### Build Images
```bash
# Build from Dockerfile
docker build -t <image-name> .

# Build with tag
docker build -t <image-name>:<tag> .

# Build without cache
docker build --no-cache -t <image-name> .

# Build with build args
docker build --build-arg KEY=value -t <image-name> .
```

### Image Operations
```bash
# List images
docker images

# Pull image
docker pull <image>

# Push image
docker push <image>

# Remove image
docker rmi <image>

# Remove all unused images
docker image prune -a

# Tag image
docker tag <source> <target>

# Save image to tar
docker save -o image.tar <image>

# Load image from tar
docker load -i image.tar
```

## Volume Management

```bash
# List volumes
docker volume ls

# Create volume
docker volume create <volume-name>

# Inspect volume
docker volume inspect <volume-name>

# Remove volume
docker volume rm <volume-name>

# Remove all unused volumes
docker volume prune
```

## Network Management

```bash
# List networks
docker network ls

# Create network
docker network create <network-name>

# Inspect network
docker network inspect <network-name>

# Connect container to network
docker network connect <network> <container>

# Disconnect container from network
docker network disconnect <network> <container>

# Remove network
docker network rm <network-name>

# Remove all unused networks
docker network prune
```

## System Commands

```bash
# Show Docker version
docker version

# Show system information
docker info

# Show disk usage
docker system df

# Clean up system
docker system prune

# Clean up everything including volumes
docker system prune -a --volumes
```

## Docker Compose

```bash
# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Execute command
docker-compose exec <service> <command>

# Build images
docker-compose build

# Restart services
docker-compose restart

# Scale services
docker-compose up --scale <service>=3
```

