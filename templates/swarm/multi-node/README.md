# Docker Swarm - Multi-Node Example

Complete example for running Docker Swarm across multiple nodes (production-ready setup).

## What is This?

This example demonstrates Docker Swarm orchestration across multiple machines. Perfect for:
- Production deployments
- High availability
- Load distribution
- Real-world scenarios

## Architecture

```
┌─────────────────────────────────────────┐
│         Docker Swarm Cluster            │
│                                         │
│  ┌──────────────┐                       │
│  │   Manager    │  (Leader)            │
│  │   Node 1     │  192.168.1.10         │
│  └──────┬───────┘                       │
│         │                               │
│  ┌──────▼───────┐  ┌──────────────┐    │
│  │   Manager    │  │   Manager    │    │
│  │   Node 2     │  │   Node 3     │    │
│  │ 192.168.1.11 │  │ 192.168.1.12 │    │
│  └──────────────┘  └──────────────┘    │
│         │                               │
│  ┌──────▼───────────────────────────┐  │
│  │         Worker Nodes              │  │
│  │  ┌──────┐  ┌──────┐  ┌──────┐   │  │
│  │  │Worker│  │Worker│  │Worker│   │  │
│  │  │  1   │  │  2   │  │  3   │   │  │
│  │  │.13   │  │.14   │  │.15   │   │  │
│  │  └──────┘  └──────┘  └──────┘   │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Prerequisites

- At least 2 machines (1 manager + 1 worker minimum)
- Docker installed on all machines
- Network connectivity between nodes
- Ports 2377, 7946, 4789 open (Swarm ports)

## Setup Instructions

### Step 1: Initialize Swarm on Manager Node

```bash
# On Manager Node 1 (192.168.1.10)
docker swarm init --advertise-addr 192.168.1.10

# Output will show join token:
# docker swarm join --token <TOKEN> 192.168.1.10:2377
```

**Save the join token!** You'll need it for other nodes.

### Step 2: Add Manager Nodes (Optional but Recommended)

```bash
# Get manager join token
docker swarm join-token manager

# On Manager Node 2 (192.168.1.11)
docker swarm join --token <MANAGER_TOKEN> 192.168.1.10:2377

# On Manager Node 3 (192.168.1.12)
docker swarm join --token <MANAGER_TOKEN> 192.168.1.10:2377
```

### Step 3: Add Worker Nodes

```bash
# Get worker join token
docker swarm join-token worker

# On Worker Node 1 (192.168.1.13)
docker swarm join --token <WORKER_TOKEN> 192.168.1.10:2377

# On Worker Node 2 (192.168.1.14)
docker swarm join --token <WORKER_TOKEN> 192.168.1.10:2377

# On Worker Node 3 (192.168.1.15)
docker swarm join --token <WORKER_TOKEN> 192.168.1.10:2377
```

### Step 4: Label Worker Nodes (Optional)

```bash
# On Manager Node
docker node update --label-add zone=east worker1
docker node update --label-add zone=west worker2
docker node update --label-add zone=central worker3

# Verify labels
docker node inspect worker1 --pretty
```

### Step 5: Verify Cluster

```bash
# On Manager Node
docker node ls

# Should show:
# ID    HOSTNAME    STATUS    AVAILABILITY   MANAGER STATUS
# xxx   manager1    Ready     Active          Leader
# xxx   manager2    Ready     Active          Reachable
# xxx   manager3    Ready     Active          Reachable
# xxx   worker1     Ready     Active
# xxx   worker2     Ready     Active
# xxx   worker3     Ready     Active
```

### Step 6: Deploy Stack

```bash
# On Manager Node
docker stack deploy -c docker-stack.yml myapp

# Check deployment
docker stack services myapp
docker stack ps myapp
```

## Access Application

The application will be accessible on any node's IP:

```bash
# From any node or external machine
curl http://192.168.1.10
curl http://192.168.1.11
curl http://192.168.1.13
# All should work (load balanced)
```

## Service Management

### Scale Service

```bash
# Scale to 10 replicas (distributed across workers)
docker service scale myapp_web=10

# Check distribution
docker service ps myapp_web
```

### Update Service with Versioning

```bash
# Deploy version 1.0.0
docker service update --image nginx:1.25-alpine myapp_web

# Deploy version 1.0.1 (rolling update)
docker service update --image nginx:1.26-alpine myapp_web

# Monitor update across nodes
watch docker service ps myapp_web

# Rollback if needed
docker service rollback myapp_web
```

### Update with Custom Config

```bash
# Update with specific parallelism
docker service update \
  --image nginx:1.26-alpine \
  --update-parallelism 3 \
  --update-delay 5s \
  myapp_web
```

## Versioning Strategy

### 1. Build and Tag Images

```bash
# Build with semantic versioning
docker build -t myapp:1.0.0 .
docker build -t myapp:1.0.1 .
docker build -t myapp:1.1.0 .
docker build -t myapp:latest .

# Push to registry
docker push myregistry.com/myapp:1.0.0
docker push myregistry.com/myapp:1.0.1
docker push myregistry.com/myapp:latest
```

### 2. Deploy Specific Version

```yaml
# docker-stack.yml
services:
  web:
    image: myregistry.com/myapp:1.0.0  # Specific version
```

### 3. Rolling Update Process

```bash
# Step 1: Build new version
docker build -t myapp:1.0.1 .

# Step 2: Push to registry
docker push myregistry.com/myapp:1.0.1

# Step 3: Update service
docker service update --image myregistry.com/myapp:1.0.1 myapp_web

# Step 4: Monitor
watch docker service ps myapp_web

# Step 5: Verify
curl http://<any-node-ip>

# Step 6: Rollback if needed
docker service rollback myapp_web
```

## Node Management

### Drain Node (Maintenance)

```bash
# Drain node (stop tasks, don't schedule new ones)
docker node update --availability drain worker1

# Tasks will move to other nodes
docker service ps myapp_web

# Make node active again
docker node update --availability active worker1
```

### Remove Node

```bash
# On node to remove
docker swarm leave

# On manager node
docker node rm <NODE_ID>
```

### Promote Worker to Manager

```bash
docker node promote worker1
```

## Resource Management

### View Resource Usage

```bash
# Node resources
docker node inspect <NODE> --pretty

# Service resources
docker service inspect myapp_web --pretty
```

### Update Resource Limits

```bash
# Update CPU and memory limits
docker service update \
  --limit-cpu 1.0 \
  --limit-memory 512M \
  --reserve-cpu 0.5 \
  --reserve-memory 256M \
  myapp_web
```

## High Availability

### Manager High Availability

With 3 manager nodes:
- 1 can fail, cluster continues
- Leader election automatic
- Raft consensus for decisions

### Service High Availability

```yaml
deploy:
  replicas: 6  # Distribute across nodes
  placement:
    constraints:
      - node.role == worker
```

## Monitoring

### Service Status

```bash
# List all services
docker service ls

# Service details
docker service inspect myapp_web --pretty

# Service tasks (containers)
docker service ps myapp_web

# Service logs
docker service logs myapp_web
```

### Node Status

```bash
# List nodes
docker node ls

# Node details
docker node inspect <NODE> --pretty

# Node tasks
docker node ps <NODE>
```

## Useful Commands

```bash
# Swarm Management
docker swarm init --advertise-addr <IP>
docker swarm join --token <TOKEN> <IP>:2377
docker swarm leave
docker swarm update

# Node Management
docker node ls
docker node inspect <NODE>
docker node update <NODE>
docker node promote <NODE>
docker node demote <NODE>
docker node rm <NODE>

# Stack Management
docker stack deploy -c docker-stack.yml myapp
docker stack ls
docker stack services myapp
docker stack ps myapp
docker stack rm myapp

# Service Management
docker service ls
docker service ps myapp_web
docker service inspect myapp_web
docker service update --image nginx:1.26-alpine myapp_web
docker service scale myapp_web=10
docker service rollback myapp_web
docker service logs myapp_web
```

## Configuration Explained

### Replicas Distribution

```yaml
deploy:
  replicas: 6  # Will be distributed across worker nodes
```

### Placement Constraints

```yaml
placement:
  constraints:
    - node.role == worker  # Only on workers
  preferences:
    - spread: node.labels.zone  # Spread across zones
```

### Resource Limits

```yaml
resources:
  limits:
    cpus: '0.5'      # Max 0.5 CPU
    memory: 256M     # Max 256MB
  reservations:
    cpus: '0.25'     # Reserve 0.25 CPU
    memory: 128M     # Reserve 128MB
```

### Update Strategy

```yaml
update_config:
  parallelism: 2      # Update 2 at a time
  delay: 10s          # Wait 10s between batches
  failure_action: rollback
  monitor: 60s
  order: start-first  # Start new before stopping old
```

## Troubleshooting

### Service Not Distributed

```bash
# Check node availability
docker node ls

# Check placement constraints
docker service inspect myapp_web --pretty

# Check node labels
docker node inspect <NODE> --pretty
```

### Update Stuck

```bash
# Check update status
docker service ps myapp_web

# Force update
docker service update --force myapp_web

# Rollback
docker service rollback myapp_web
```

### Node Connection Issues

```bash
# Check node status
docker node ls

# Inspect node
docker node inspect <NODE>

# Check network connectivity
ping <NODE_IP>

# Check Swarm ports
netstat -tulpn | grep 2377
```

## Production Checklist

- [ ] At least 3 manager nodes (for HA)
- [ ] Worker nodes labeled appropriately
- [ ] Resource limits configured
- [ ] Health checks enabled
- [ ] Update policies set
- [ ] Monitoring in place
- [ ] Logging configured
- [ ] Backup strategy
- [ ] Network segmentation
- [ ] Security policies

## Next Steps

- Add more services to stack
- Implement secrets management
- Set up monitoring (Prometheus/Grafana)
- Configure logging aggregation
- Set up CI/CD for deployments

## See Also

- [Docker Swarm Guide](../../../guides/advanced/docker_swarm.md)
- [Single-Node Example](../single-node/README.md)

