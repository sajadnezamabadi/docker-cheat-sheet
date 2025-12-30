# Docker Swarm - Single Node Example

Complete example for running Docker Swarm on a single node (for testing and learning).

## What is This?

This example demonstrates Docker Swarm orchestration on a single machine. Perfect for:
- Learning Docker Swarm
- Testing deployments
- Development environments
- Understanding Swarm concepts

## Quick Start

### 1. Initialize Swarm

```bash
# Initialize Docker Swarm
docker swarm init

# You should see:
# Swarm initialized: current node (xxx) is now a manager.
```

### 2. Deploy Stack

```bash
# Deploy the stack
docker stack deploy -c docker-stack.yml myapp

# Check status
docker stack services myapp
docker stack ps myapp
```

### 3. Access Application

```bash
# Access the application
curl http://localhost

# Or open in browser
# http://localhost
```

### 4. View Logs

```bash
# View service logs
docker service logs myapp_web

# Follow logs
docker service logs -f myapp_web
```

## What Happens

1. **Swarm Initialized**: Current node becomes a manager
2. **Stack Deployed**: Services are created and scheduled
3. **3 Replicas**: Nginx runs in 3 containers
4. **Load Balanced**: Requests are distributed across replicas
5. **Health Checks**: Containers are monitored

## Service Management

### Scale Service

```bash
# Scale to 5 replicas
docker service scale myapp_web=5

# Check replicas
docker service ps myapp_web
```

### Update Service

```bash
# Update to new version
docker service update --image nginx:1.26-alpine myapp_web

# Monitor update
watch docker service ps myapp_web

# Rollback if needed
docker service rollback myapp_web
```

### Update with Version Tag

```bash
# Deploy version 1.0.0
docker service update --image nginx:1.25-alpine myapp_web

# Deploy version 1.0.1
docker service update --image nginx:1.26-alpine myapp_web

# Rollback to previous
docker service rollback myapp_web
```

## Versioning Strategy

### Build and Tag Images

```bash
# Build with version
docker build -t myapp:1.0.0 .
docker build -t myapp:1.0.1 .
docker build -t myapp:latest .

# Push to registry
docker push myapp:1.0.0
docker push myapp:1.0.1
docker push myapp:latest
```

### Deploy Specific Version

```yaml
# docker-stack.yml
services:
  web:
    image: nginx:1.25-alpine  # Specific version
    # or
    image: myapp:1.0.0        # Your app version
```

### Rolling Update

```bash
# Update to new version
docker service update --image nginx:1.26-alpine myapp_web

# Update with custom config
docker service update \
  --image nginx:1.26-alpine \
  --update-parallelism 2 \
  --update-delay 10s \
  myapp_web
```

## Useful Commands

```bash
# List stacks
docker stack ls

# List services in stack
docker stack services myapp

# List tasks (containers)
docker stack ps myapp

# View service details
docker service inspect myapp_web --pretty

# Service logs
docker service logs myapp_web

# Scale service
docker service scale myapp_web=5

# Update service
docker service update --image nginx:1.26-alpine myapp_web

# Rollback service
docker service rollback myapp_web

# Remove stack
docker stack rm myapp
```

## Stack Configuration Explained

### Replicas

```yaml
deploy:
  replicas: 3  # Run 3 instances
```

### Update Configuration

```yaml
update_config:
  parallelism: 2      # Update 2 containers at a time
  delay: 10s          # Wait 10s between updates
  failure_action: rollback  # Rollback on failure
  monitor: 60s        # Monitor for 60s after update
```

### Rollback Configuration

```yaml
rollback_config:
  parallelism: 1     # Rollback 1 at a time
  delay: 5s          # Wait 5s between rollbacks
```

### Health Check

```yaml
healthcheck:
  test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost"]
  interval: 30s      # Check every 30s
  timeout: 10s       # Timeout after 10s
  retries: 3         # Retry 3 times
  start_period: 40s  # Grace period 40s
```

## Testing Rolling Updates

### 1. Deploy Initial Version

```bash
docker stack deploy -c docker-stack.yml myapp
```

### 2. Update to New Version

```bash
# Update image
docker service update --image nginx:1.26-alpine myapp_web

# Watch the update
watch docker service ps myapp_web
```

### 3. Verify Update

```bash
# Check service
docker service inspect myapp_web --pretty

# Test application
curl http://localhost
```

### 4. Rollback if Needed

```bash
docker service rollback myapp_web
```

## Cleanup

```bash
# Remove stack
docker stack rm myapp

# Leave swarm (optional)
docker swarm leave --force
```

## Troubleshooting

### Service Not Starting

```bash
# Check service status
docker service ps myapp_web

# Check logs
docker service logs myapp_web

# Inspect service
docker service inspect myapp_web --pretty
```

### Port Already in Use

```bash
# Check what's using port 80
sudo lsof -i :80

# Change port in docker-stack.yml
ports:
  - "8080:80"  # Use 8080 instead
```

### Update Failed

```bash
# Check update status
docker service ps myapp_web

# Rollback
docker service rollback myapp_web

# Try again with different config
docker service update \
  --update-parallelism 1 \
  --image nginx:1.26-alpine \
  myapp_web
```

## Next Steps

- Try scaling the service
- Test rolling updates
- Experiment with health checks
- Move to multi-node setup (see `../multi-node/`)

## See Also

- [Docker Swarm Guide](../../../guides/advanced/docker_swarm.md)
- [Multi-Node Example](../multi-node/README.md)

