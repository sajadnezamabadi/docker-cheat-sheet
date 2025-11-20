# Docker Compose Cheat Sheet

## Basic Commands

```bash
# Start all services
docker-compose up

# Start in detached mode
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart services
docker-compose restart

# Stop services
docker-compose stop

# Start stopped services
docker-compose start
```

## Build Commands

```bash
# Build images
docker-compose build

# Build without cache
docker-compose build --no-cache

# Build specific service
docker-compose build <service>

# Rebuild and start
docker-compose up --build
```

## Logs and Debugging

```bash
# View logs
docker-compose logs

# Follow logs
docker-compose logs -f

# View logs for specific service
docker-compose logs <service>

# View last N lines
docker-compose logs --tail=100

# View logs with timestamps
docker-compose logs -t
```

## Service Management

```bash
# Execute command in service
docker-compose exec <service> <command>

# Execute as specific user
docker-compose exec -u root <service> <command>

# Run one-off command
docker-compose run <service> <command>

# Scale services
docker-compose up --scale <service>=3

# List running services
docker-compose ps

# Show service status
docker-compose top
```

## Configuration

```bash
# Validate compose file
docker-compose config

# Show resolved configuration
docker-compose config

# Use specific compose file
docker-compose -f docker-compose.prod.yml up

# Use multiple compose files
docker-compose -f docker-compose.yml -f docker-compose.override.yml up
```

## Cleanup

```bash
# Remove stopped containers
docker-compose rm

# Remove with volumes
docker-compose rm -v

# Remove all including images
docker-compose down --rmi all

# Remove volumes
docker-compose down -v
```

## docker-compose.yml Structure

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=1
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:

networks:
  default:
    driver: bridge
```

## Environment Variables

```yaml
# Using .env file
services:
  web:
    env_file:
      - .env
    environment:
      - DATABASE_URL=${DATABASE_URL}
```

## Health Checks

```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Resource Limits

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

