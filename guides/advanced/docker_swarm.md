# Docker Swarm Guide

Complete guide to Docker Swarm orchestration, deployment, and management.

## What is Docker Swarm?

Docker Swarm is Docker's native clustering and orchestration solution. It allows you to manage a cluster of Docker hosts and deploy services across multiple nodes.

### Key Concepts

- **Swarm**: A cluster of Docker nodes (managers and workers)
- **Manager Node**: Controls the swarm and schedules services
- **Worker Node**: Runs tasks assigned by managers
- **Service**: Definition of tasks to execute on nodes
- **Stack**: Collection of services defined in a Compose file
- **Task**: A running container that's part of a service

## Swarm vs Kubernetes

| Feature | Docker Swarm | Kubernetes |
|---------|--------------|------------|
| **Complexity** | Simple | Complex |
| **Learning Curve** | Easy | Steep |
| **Setup Time** | Minutes | Hours |
| **Resource Usage** | Lightweight | Heavy |
| **Scaling** | Easy | Advanced |
| **Best For** | Small to medium teams | Large enterprises |

**When to use Swarm:**
- Simple orchestration needs
- Small to medium deployments
- Teams new to container orchestration
- Quick setup required

**When to use Kubernetes:**
- Complex microservices
- Large scale deployments
- Advanced features needed
- Enterprise requirements

## Architecture

```
┌─────────────────────────────────────────┐
│           Docker Swarm Cluster          │
│                                         │
│  ┌──────────────┐                       │
│  │   Manager    │  (Leader)            │
│  │   Node 1     │                       │
│  └──────┬───────┘                       │
│         │                               │
│  ┌──────▼───────┐  ┌──────────────┐    │
│  │   Manager    │  │   Manager    │    │
│  │   Node 2     │  │   Node 3     │    │
│  └──────────────┘  └──────────────┘    │
│         │                               │
│  ┌──────▼───────────────────────────┐  │
│  │         Worker Nodes              │  │
│  │  ┌──────┐  ┌──────┐  ┌──────┐   │  │
│  │  │Worker│  │Worker│  │Worker│   │  │
│  │  │  1   │  │  2   │  │  3   │   │  │
│  │  └──────┘  └──────┘  └──────┘   │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Getting Started

### 1. Initialize Swarm (Single Node)

```bash
# Initialize swarm on current node
docker swarm init

# Output will show:
# Swarm initialized: current node (xxx) is now a manager.
# To add a worker to this swarm, run the following command:
#   docker swarm join --token <token> <ip>:2377
```

### 2. Check Swarm Status

```bash
# List nodes in swarm
docker node ls

# Inspect swarm
docker info

# View swarm configuration
docker swarm inspect
```

### 3. Create a Service

```bash
# Create a service
docker service create --name web --replicas 3 -p 80:80 nginx:alpine

# List services
docker service ls

# Inspect service
docker service inspect web

# View service logs
docker service logs web

# Scale service
docker service scale web=5
```

### 4. Deploy a Stack

```bash
# Deploy stack from compose file
docker stack deploy -c docker-stack.yml myapp

# List stacks
docker stack ls

# List services in stack
docker stack services myapp

# Remove stack
docker stack rm myapp
```

## Service Management

### Create Service

```bash
# Basic service
docker service create --name myapp nginx:alpine

# With port mapping
docker service create --name web -p 80:80 nginx:alpine

# With replicas
docker service create --name web --replicas 3 nginx:alpine

# With environment variables
docker service create --name app \
  --env MYSQL_HOST=db \
  --env MYSQL_USER=user \
  nginx:alpine

# With volumes
docker service create --name app \
  --mount type=volume,source=mydata,target=/data \
  nginx:alpine

# With networks
docker service create --name app \
  --network mynetwork \
  nginx:alpine
```

### Update Service

```bash
# Update image
docker service update --image nginx:1.25 web

# Update replicas
docker service update --replicas 5 web

# Update environment variables
docker service update --env-add KEY=value web

# Update port
docker service update --publish-rm 80:80 --publish-add 8080:80 web

# Rollback to previous version
docker service rollback web
```

### Rolling Updates

```bash
# Update with rolling update (default)
docker service update --image nginx:1.25 web

# Update with specific update config
docker service update \
  --update-parallelism 2 \
  --update-delay 10s \
  --image nginx:1.25 web

# Update with failure action
docker service update \
  --update-failure-action rollback \
  --image nginx:1.25 web
```

### Service Configuration

```yaml
# docker-stack.yml
services:
  web:
    image: nginx:1.25-alpine
    deploy:
      replicas: 3
      update_config:
        parallelism: 2
        delay: 10s
        failure_action: rollback
        monitor: 60s
      rollback_config:
        parallelism: 1
        delay: 5s
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
      placement:
        constraints:
          - node.role == worker
        preferences:
          - spread: node.labels.zone
    ports:
      - "80:80"
    networks:
      - webnet
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  webnet:
    driver: overlay
```

## Health Checks

```yaml
services:
  web:
    image: nginx:alpine
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

```bash
# Service with health check
docker service create \
  --name web \
  --health-cmd "curl -f http://localhost || exit 1" \
  --health-interval 30s \
  --health-timeout 10s \
  --health-retries 3 \
  nginx:alpine
```

## Secrets Management

### Create Secret

```bash
# Create secret from file
echo "mysecretpassword" | docker secret create db_password -

# Create secret from stdin
docker secret create db_password -

# List secrets
docker secret ls

# Inspect secret
docker secret inspect db_password
```

### Use Secret in Service

```bash
# Service with secret
docker service create \
  --name app \
  --secret db_password \
  nginx:alpine

# Secret mounted as file
# Accessible at: /run/secrets/db_password
```

### Secrets in Stack

```yaml
version: '3.8'

secrets:
  db_password:
    external: true

services:
  app:
    image: nginx:alpine
    secrets:
      - db_password
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password
```

## Networking

### Overlay Networks

```bash
# Create overlay network
docker network create --driver overlay mynetwork

# Service on specific network
docker service create \
  --name app \
  --network mynetwork \
  nginx:alpine
```

### Network in Stack

```yaml
networks:
  frontend:
    driver: overlay
  backend:
    driver: overlay
    internal: true  # No external access

services:
  web:
    networks:
      - frontend
  api:
    networks:
      - frontend
      - backend
```

## Multi-Node Setup

### 1. Initialize Manager

```bash
# On manager node
docker swarm init --advertise-addr <MANAGER_IP>
```

### 2. Add Worker Nodes

```bash
# Get join token
docker swarm join-token worker

# On worker node, run the command shown:
docker swarm join --token <TOKEN> <MANAGER_IP>:2377
```

### 3. Add Manager Nodes

```bash
# Get manager join token
docker swarm join-token manager

# On new manager node:
docker swarm join --token <TOKEN> <MANAGER_IP>:2377
```

### 4. Promote Worker to Manager

```bash
docker node promote <NODE_ID>
```

### 5. Demote Manager to Worker

```bash
docker node demote <NODE_ID>
```

## Versioning and Tagging

### Image Versioning Strategy

```bash
# Build with version tag
docker build -t myapp:1.0.0 .
docker build -t myapp:1.0.1 .
docker build -t myapp:latest .

# Push to registry
docker push myapp:1.0.0
docker push myapp:1.0.1
docker push myapp:latest
```

### Deploy Specific Version

```bash
# Deploy version 1.0.0
docker service update --image myapp:1.0.0 web

# Or in stack file
services:
  web:
    image: myapp:1.0.0
```

### Rolling Update with Versions

```bash
# Update to new version
docker service update --image myapp:1.0.1 web

# Monitor update
docker service ps web

# Rollback if needed
docker service rollback web
```

## Best Practices

### 1. Use Health Checks

Always define health checks for services:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### 2. Configure Update Policies

```yaml
update_config:
  parallelism: 2
  delay: 10s
  failure_action: rollback
```

### 3. Use Resource Limits

```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 512M
    reservations:
      cpus: '0.25'
      memory: 256M
```

### 4. Label Nodes

```bash
# Label node
docker node update --label-add zone=east node1

# Use in placement
placement:
  constraints:
    - node.labels.zone == east
```

### 5. Use Secrets for Sensitive Data

Never use environment variables for passwords. Use secrets:

```yaml
secrets:
  db_password:
    external: true
```

### 6. Monitor Services

```bash
# Watch service status
watch docker service ps web

# Service logs
docker service logs -f web
```

## Troubleshooting

### Service Not Starting

```bash
# Check service status
docker service ps web

# Check logs
docker service logs web

# Inspect service
docker service inspect web --pretty
```

### Node Issues

```bash
# List nodes
docker node ls

# Inspect node
docker node inspect <NODE_ID>

# Drain node (stop tasks)
docker node update --availability drain <NODE_ID>

# Make node active again
docker node update --availability active <NODE_ID>
```

### Network Issues

```bash
# List networks
docker network ls

# Inspect network
docker network inspect <NETWORK_NAME>

# Test connectivity
docker exec -it <CONTAINER> ping <OTHER_CONTAINER>
```

## Common Commands Reference

```bash
# Swarm Management
docker swarm init
docker swarm join --token <TOKEN> <IP>
docker swarm leave
docker swarm update

# Node Management
docker node ls
docker node inspect <NODE>
docker node update <NODE>
docker node rm <NODE>

# Service Management
docker service create <OPTIONS> <IMAGE>
docker service ls
docker service ps <SERVICE>
docker service inspect <SERVICE>
docker service update <SERVICE>
docker service scale <SERVICE>=<REPLICAS>
docker service rm <SERVICE>
docker service logs <SERVICE>
docker service rollback <SERVICE>

# Stack Management
docker stack deploy -c <FILE> <STACK>
docker stack ls
docker stack services <STACK>
docker stack ps <STACK>
docker stack rm <STACK>

# Secret Management
docker secret create <NAME> <FILE>
docker secret ls
docker secret inspect <SECRET>
docker secret rm <SECRET>

# Network Management
docker network create --driver overlay <NAME>
docker network ls
docker network inspect <NETWORK>
docker network rm <NETWORK>
```

## Migration from Docker Compose

### Docker Compose File

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
```

### Docker Stack File

```yaml
# docker-stack.yml
version: '3.8'
services:
  web:
    image: nginx:alpine
    deploy:
      replicas: 3
    ports:
      - "80:80"
```

**Key Differences:**
- Add `deploy` section for Swarm
- Remove `build` (use pre-built images)
- Use `secrets` instead of environment variables for sensitive data
- Networks should be `overlay` type

## Production Checklist

- [ ] At least 3 manager nodes (for HA)
- [ ] Health checks configured
- [ ] Update policies set
- [ ] Resource limits defined
- [ ] Secrets used for sensitive data
- [ ] Logging configured
- [ ] Monitoring in place
- [ ] Backup strategy for volumes
- [ ] Node labels for placement
- [ ] Network segmentation

## Useful Links

- [Docker Swarm Official Docs](https://docs.docker.com/engine/swarm/)
- [Docker Stack Deploy](https://docs.docker.com/engine/reference/commandline/stack_deploy/)
- [Swarm Mode Tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/)

