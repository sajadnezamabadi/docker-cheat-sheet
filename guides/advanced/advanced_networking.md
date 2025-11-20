# Advanced Docker Networking

Advanced networking concepts: overlay networks, service discovery, and load balancing.

## Overlay Networks

### Docker Swarm Overlay Network

```bash
# Initialize Swarm
docker swarm init

# Create overlay network
docker network create --driver overlay --attachable my-overlay-network

# Create service on overlay network
docker service create \
  --name web \
  --network my-overlay-network \
  --replicas 3 \
  nginx:alpine
```

### Multi-Host Networking

```yaml
# docker-compose.yml with overlay
services:
  web:
    image: nginx:alpine
    networks:
      - overlay-net
    deploy:
      replicas: 3

networks:
  overlay-net:
    driver: overlay
    attachable: true
```

### Custom Network Drivers

```bash
# Create network with custom options
docker network create \
  --driver bridge \
  --subnet=172.20.0.0/16 \
  --gateway=172.20.0.1 \
  --ip-range=172.20.240.0/20 \
  custom-network
```

## Service Discovery

### DNS-Based Service Discovery

```yaml
# docker-compose.yml
services:
  web:
    image: nginx:alpine
    networks:
      - app-network

  api:
    image: myapi:latest
    networks:
      - app-network
    # Accessible as 'api' from other containers

  db:
    image: postgres:15
    networks:
      - app-network
    # Accessible as 'db' from other containers

networks:
  app-network:
    driver: bridge
```

### Consul Service Discovery

```yaml
# docker-compose.yml with Consul
services:
  consul:
    image: consul:latest
    ports:
      - "8500:8500"
    command: consul agent -dev -client=0.0.0.0

  app:
    image: myapp:latest
    environment:
      - CONSUL_HOST=consul
      - CONSUL_PORT=8500
    depends_on:
      - consul
```

### etcd Service Discovery

```yaml
# docker-compose.yml with etcd
services:
  etcd:
    image: quay.io/coreos/etcd:latest
    environment:
      - ETCD_NAME=etcd
      - ETCD_DATA_DIR=/etcd-data
      - ETCD_LISTEN_CLIENT_URLS=http://0.0.0.0:2379
      - ETCD_ADVERTISE_CLIENT_URLS=http://etcd:2379
    ports:
      - "2379:2379"
```

## Load Balancing

### Nginx Load Balancer

```yaml
# docker-compose.yml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app1
      - app2
      - app3

  app1:
    image: myapp:latest
    networks:
      - app-network

  app2:
    image: myapp:latest
    networks:
      - app-network

  app3:
    image: myapp:latest
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### Nginx Load Balancer Configuration

```nginx
# nginx/nginx.conf
upstream backend {
    least_conn;
    server app1:8000;
    server app2:8000;
    server app3:8000;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

### HAProxy Load Balancer

```yaml
# docker-compose.yml with HAProxy
services:
  haproxy:
    image: haproxy:latest
    ports:
      - "80:80"
      - "8404:8404"  # Stats
    volumes:
      - ./haproxy/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg
    depends_on:
      - app1
      - app2

  app1:
    image: myapp:latest
    networks:
      - app-network

  app2:
    image: myapp:latest
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### HAProxy Configuration

```haproxy
# haproxy/haproxy.cfg
global
    log stdout format raw local0
    maxconn 4096

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend http_front
    bind *:80
    default_backend http_back

backend http_back
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200
    server app1 app1:8000 check
    server app2 app2:8000 check

stats enable
stats uri /stats
stats refresh 30s
```

### Traefik Load Balancer

```yaml
# docker-compose.yml with Traefik
services:
  traefik:
    image: traefik:v2.10
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
    ports:
      - "80:80"
      - "8080:8080"  # Dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro

  app1:
    image: myapp:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app1.rule=Host(`app1.example.com`)"
      - "traefik.http.services.app1.loadbalancer.server.port=8000"

  app2:
    image: myapp:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app2.rule=Host(`app2.example.com`)"
      - "traefik.http.services.app2.loadbalancer.server.port=8000"
```

## Network Policies

### Docker Swarm Network Policies

```yaml
# docker-compose.yml
services:
  web:
    image: nginx:alpine
    networks:
      - frontend
    deploy:
      placement:
        constraints:
          - node.role == worker

  api:
    image: myapi:latest
    networks:
      - frontend
      - backend

  db:
    image: postgres:15
    networks:
      - backend
    deploy:
      placement:
        constraints:
          - node.role == manager

networks:
  frontend:
    driver: overlay
  backend:
    driver: overlay
```

## Advanced Network Configurations

### Macvlan Network

```bash
# Create macvlan network
docker network create -d macvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  macvlan-net

# Run container with macvlan
docker run --network macvlan-net --ip=192.168.1.100 nginx
```

### IPvlan Network

```bash
# Create ipvlan network
docker network create -d ipvlan \
  --subnet=192.168.1.0/24 \
  --gateway=192.168.1.1 \
  -o parent=eth0 \
  ipvlan-net
```

### Custom Bridge Network

```bash
# Create custom bridge
docker network create \
  --driver bridge \
  --opt com.docker.network.bridge.name=mybridge \
  --opt com.docker.network.driver.mtu=1500 \
  custom-bridge
```

## Service Mesh

### Consul Connect

```yaml
# docker-compose.yml with Consul Connect
services:
  consul:
    image: consul:latest
    command: consul agent -dev -client=0.0.0.0
    ports:
      - "8500:8500"

  app1:
    image: myapp:latest
    environment:
      - CONSUL_HTTP_ADDR=consul:8500
    depends_on:
      - consul
```

## Network Troubleshooting

### Inspect Network

```bash
# Inspect network configuration
docker network inspect <network_name>

# List all networks
docker network ls

# Show network details
docker network inspect --format '{{json .}}' <network_name> | jq
```

### Test Connectivity

```bash
# Ping from container
docker exec <container> ping <target>

# Test DNS resolution
docker exec <container> nslookup <service_name>

# Check network connections
docker exec <container> netstat -tulpn
```

### Network Debugging

```bash
# View network traffic
docker exec <container> tcpdump -i eth0

# Check routing
docker exec <container> ip route

# View network interfaces
docker exec <container> ip addr show
```

## Best Practices

1. **Use Overlay Networks**: For multi-host deployments
2. **Service Discovery**: Use DNS or service discovery tools
3. **Load Balancing**: Implement at application or network level
4. **Network Isolation**: Separate networks for different tiers
5. **Security**: Use network policies to restrict communication
6. **Monitoring**: Monitor network traffic and performance
7. **Documentation**: Document network architecture and policies

