# Docker Networking Examples

## Network Types

### 1. Bridge Network (Default)
```bash
# Create bridge network
docker network create my-bridge-network

# Run container on specific network
docker run -d --name web --network my-bridge-network nginx

# Connect existing container to network
docker network connect my-bridge-network existing-container
```

### 2. Host Network
```bash
# Run container on host network (Linux only)
docker run -d --name web --network host nginx
```

### 3. None Network
```bash
# Run container with no network
docker run -d --name isolated --network none alpine
```

### 4. Overlay Network (Swarm)
```bash
# Create overlay network for swarm
docker network create --driver overlay my-overlay-network
```

## Docker Compose Networking

### Basic Example
```yaml
version: '3.8'

services:
  web:
    image: nginx
    ports:
      - "8080:80"
    networks:
      - frontend

  api:
    image: node:18
    networks:
      - frontend
      - backend

  db:
    image: postgres:15
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

### Custom Network Configuration
```yaml
version: '3.8'

services:
  web:
    image: nginx
    networks:
      app-network:
        ipv4_address: 172.20.0.10

networks:
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

## Container Communication

### Same Network
```bash
# Containers on same network can communicate by name
docker run -d --name web --network my-network nginx
docker run -d --name api --network my-network node:18

# From api container, access web by name:
# curl http://web
```

### Different Networks
```bash
# Container on network1
docker run -d --name web --network network1 nginx

# Container on network2
docker run -d --name api --network network2 node:18

# Connect web to network2
docker network connect network2 web
```

## Port Mapping Examples

### Basic Port Mapping
```bash
# Map host port 8080 to container port 80
docker run -p 8080:80 nginx

# Map specific host IP
docker run -p 127.0.0.1:8080:80 nginx

# Map random host port
docker run -p 80 nginx

# Map UDP port
docker run -p 8080:80/udp nginx
```

### Port Range Mapping
```bash
# Map port range
docker run -p 8000-8010:8000-8010 myapp
```

## DNS Configuration

### Custom DNS
```bash
# Use custom DNS server
docker run --dns 8.8.8.8 --dns 8.8.4.4 nginx

# Disable DNS
docker run --network none nginx
```

### Docker Compose DNS
```yaml
services:
  web:
    image: nginx
    dns:
      - 8.8.8.8
      - 8.8.4.4
    dns_search:
      - example.com
```

## Network Aliases

```bash
# Create container with alias
docker run -d --name web --network my-network --network-alias www nginx

# Other containers can access via alias
docker run --rm --network my-network alpine ping www
```

### Docker Compose Aliases
```yaml
services:
  web:
    image: nginx
    networks:
      app-network:
        aliases:
          - www
          - website
```

## External Networks

### Connect to External Network
```yaml
services:
  web:
    image: nginx
    networks:
      - external-network

networks:
  external-network:
    external: true
    name: existing-network
```

## Network Inspection

```bash
# List all networks
docker network ls

# Inspect network
docker network inspect my-network

# Show network details
docker network inspect --format '{{range .Containers}}{{.Name}} {{end}}' my-network

# Remove unused networks
docker network prune
```

## Real-World Examples

### Microservices Architecture
```yaml
version: '3.8'

services:
  # Frontend
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    networks:
      - frontend-network
    depends_on:
      - api-gateway

  # API Gateway
  api-gateway:
    build: ./api-gateway
    ports:
      - "8080:8080"
    networks:
      - frontend-network
      - backend-network
    depends_on:
      - user-service
      - order-service

  # User Service
  user-service:
    build: ./user-service
    networks:
      - backend-network
    depends_on:
      - user-db

  # Order Service
  order-service:
    build: ./order-service
    networks:
      - backend-network
    depends_on:
      - order-db

  # Databases
  user-db:
    image: postgres:15
    networks:
      - backend-network
    volumes:
      - user-data:/var/lib/postgresql/data

  order-db:
    image: postgres:15
    networks:
      - backend-network
    volumes:
      - order-data:/var/lib/postgresql/data

networks:
  frontend-network:
    driver: bridge
  backend-network:
    driver: bridge

volumes:
  user-data:
  order-data:
```

### Reverse Proxy Setup
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    networks:
      - app-network
    depends_on:
      - app1
      - app2

  app1:
    image: myapp:latest
    networks:
      - app-network
    expose:
      - "8000"

  app2:
    image: myapp:latest
    networks:
      - app-network
    expose:
      - "8000"

networks:
  app-network:
    driver: bridge
```

## Troubleshooting

### Test Connectivity
```bash
# Ping from container
docker exec -it container1 ping container2

# Test HTTP connection
docker exec -it container1 wget -O- http://container2:80

# Check DNS resolution
docker exec -it container1 nslookup container2
```

### Network Debugging
```bash
# Show network configuration
docker network inspect my-network

# Show container network settings
docker inspect container-name | grep -A 20 "Networks"

# Test port connectivity
docker exec -it container1 nc -zv container2 80
```

