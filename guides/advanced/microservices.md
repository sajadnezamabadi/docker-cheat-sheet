# Microservices with Docker

Complete microservices example with service mesh and multi-container architecture.

## Complete Microservices Example

### Architecture

```
┌─────────────┐
│   Nginx     │ (Reverse Proxy)
│  Port 80   │
└──────┬──────┘
       │
       ├──────────┬──────────┐
       │          │          │
┌──────▼──────┐ ┌─▼──────┐ ┌─▼──────┐
│   API       │ │  Auth  │ │  User  │
│  Gateway    │ │ Service│ │ Service│
│  Port 8000  │ │ Port   │ │ Port   │
└──────┬──────┘ └────────┘ └───┬────┘
       │                        │
       ├────────────┬───────────┤
       │            │           │
┌──────▼──────┐ ┌──▼────┐ ┌────▼────┐
│ PostgreSQL  │ │ Redis │ │ MongoDB │
│  Port 5432  │ │ 6379  │ │ 27017   │
└─────────────┘ └────────┘ └─────────┘
```

### Docker Compose Setup

```yaml
# docker-compose.microservices.yml
services:
  # Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api-gateway
      - auth-service
      - user-service
    networks:
      - frontend
      - backend

  # API Gateway
  api-gateway:
    build: ./services/api-gateway
    ports:
      - "8000:8000"
    environment:
      - AUTH_SERVICE_URL=http://auth-service:8001
      - USER_SERVICE_URL=http://user-service:8002
      - REDIS_URL=redis://redis:6379
    depends_on:
      - auth-service
      - user-service
      - redis
    networks:
      - frontend
      - backend

  # Auth Service
  auth-service:
    build: ./services/auth-service
    ports:
      - "8001:8001"
    environment:
      - DATABASE_URL=postgresql://auth:auth@postgres:5432/authdb
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=your-secret-key
    depends_on:
      - postgres
      - redis
    networks:
      - backend

  # User Service
  user-service:
    build: ./services/user-service
    ports:
      - "8002:8002"
    environment:
      - DATABASE_URL=mongodb://mongo:27017/userdb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - mongo
      - redis
    networks:
      - backend

  # Databases
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: authdb
      POSTGRES_USER: auth
      POSTGRES_PASSWORD: auth
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

  mongo:
    image: mongo:7
    environment:
      MONGO_INITDB_DATABASE: userdb
    volumes:
      - mongo_data:/data/db
    networks:
      - backend

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - backend

volumes:
  postgres_data:
  mongo_data:
  redis_data:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

### Nginx Configuration

```nginx
# nginx/nginx.conf
upstream api_gateway {
    server api-gateway:8000;
}

upstream auth_service {
    server auth-service:8001;
}

upstream user_service {
    server user-service:8002;
}

server {
    listen 80;
    server_name localhost;

    # API Gateway
    location /api/ {
        proxy_pass http://api_gateway;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Auth Service
    location /auth/ {
        proxy_pass http://auth_service;
        proxy_set_header Host $host;
    }

    # User Service
    location /users/ {
        proxy_pass http://user_service;
        proxy_set_header Host $host;
    }

    # Health check
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

## Service Mesh with Traefik

### Traefik Service Mesh

```yaml
# docker-compose.traefik.yml
services:
  traefik:
    image: traefik:v2.10
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"  # Dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - traefik

  api-gateway:
    image: myapp/api-gateway:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.example.com`)"
      - "traefik.http.services.api.loadbalancer.server.port=8000"
    networks:
      - traefik
      - backend

  auth-service:
    image: myapp/auth-service:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.auth.rule=Host(`auth.example.com`)"
      - "traefik.http.services.auth.loadbalancer.server.port=8001"
    networks:
      - traefik
      - backend

  user-service:
    image: myapp/user-service:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.users.rule=Host(`users.example.com`)"
      - "traefik.http.services.users.loadbalancer.server.port=8002"
    networks:
      - traefik
      - backend

networks:
  traefik:
    driver: bridge
  backend:
    driver: bridge
```

## Service Mesh with Consul

### Consul Service Mesh

```yaml
# docker-compose.consul.yml
services:
  consul:
    image: consul:latest
    command: consul agent -dev -client=0.0.0.0
    ports:
      - "8500:8500"
    networks:
      - consul-mesh

  consul-connect:
    image: consul:latest
    command: consul connect envoy -sidecar-for api-gateway
    depends_on:
      - consul
      - api-gateway
    networks:
      - consul-mesh

  api-gateway:
    image: myapp/api-gateway:latest
    environment:
      - CONSUL_HTTP_ADDR=consul:8500
    depends_on:
      - consul
    networks:
      - consul-mesh

networks:
  consul-mesh:
    driver: bridge
```

## Example Service Implementation

### API Gateway (Python/Flask)

```python
# services/api-gateway/app.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_SERVICE = "http://auth-service:8001"
USER_SERVICE = "http://user-service:8002"

@app.route('/api/users', methods=['GET'])
def get_users():
    # Forward to user service
    response = requests.get(f"{USER_SERVICE}/users")
    return jsonify(response.json()), response.status_code

@app.route('/api/auth/login', methods=['POST'])
def login():
    # Forward to auth service
    response = requests.post(f"{AUTH_SERVICE}/login", json=request.json)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

### Auth Service (Node.js/Express)

```javascript
// services/auth-service/server.js
const express = require('express');
const { Pool } = require('pg');
const jwt = require('jsonwebtoken');

const app = express();
app.use(express.json());

const pool = new Pool({
  host: 'postgres',
  database: 'authdb',
  user: 'auth',
  password: 'auth',
  port: 5432,
});

app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  
  // Validate credentials
  const result = await pool.query(
    'SELECT * FROM users WHERE username = $1 AND password = $2',
    [username, password]
  );
  
  if (result.rows.length > 0) {
    const token = jwt.sign({ userId: result.rows[0].id }, 'your-secret-key');
    res.json({ token });
  } else {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});

app.listen(8001, '0.0.0.0', () => {
  console.log('Auth service running on port 8001');
});
```

### User Service (Python/FastAPI)

```python
# services/user-service/main.py
from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb://mongo:27017/")
db = client["userdb"]
users = db["users"]

@app.get("/users")
async def get_users():
    user_list = list(users.find({}, {"_id": 0}))
    return {"users": user_list}

@app.post("/users")
async def create_user(user: dict):
    result = users.insert_one(user)
    return {"id": str(result.inserted_id), "user": user}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
```

## Health Checks and Monitoring

### Health Check Configuration

```yaml
# docker-compose.yml
services:
  api-gateway:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  auth-service:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  user-service:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Service Communication Patterns

### Synchronous (HTTP/REST)

```python
# Service-to-service communication
import requests

def call_auth_service(token):
    response = requests.get(
        "http://auth-service:8001/validate",
        headers={"Authorization": f"{token}"}
    )
    return response.json()
```

### Asynchronous (Message Queue)

```yaml
# docker-compose.yml with RabbitMQ
services:
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"  # Management UI

  user-service:
    environment:
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      - rabbitmq
```

## Best Practices

1. **Service Isolation**: Each service in separate container
2. **Network Segmentation**: Use different networks for tiers
3. **Service Discovery**: Implement proper service discovery
4. **Load Balancing**: Distribute traffic across instances
5. **Health Checks**: Monitor service health
6. **Circuit Breakers**: Implement fault tolerance
7. **API Gateway**: Centralize API management
8. **Distributed Tracing**: Track requests across services
9. **Centralized Logging**: Aggregate logs from all services
10. **Configuration Management**: Externalize configuration

