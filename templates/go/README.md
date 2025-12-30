# Go Docker Example - Ready to Run

A complete Go REST API with PostgreSQL, ready to run with Docker.

## Features

- Go web server (Gin framework)
- PostgreSQL integration
- Full CRUD operations
- RESTful API endpoints
- JSON responses
- Automatic database initialization
- Health check endpoint

## Quick Start

```bash
# Go to project folder
cd templates/go

# Build and start containers
docker-compose up --build

# Or detached mode
docker-compose up -d --build
```

## Access

- **Home page**: http://localhost:8000
- **API Info**: http://localhost:8000/api/
- **Health Check**: http://localhost:8000/health
- **Items List**: http://localhost:8000/api/items

## Project Structure

```
go/
├── Dockerfile
├── docker-compose.yml
├── go.mod
├── go.sum
├── entrypoint.sh
├── src/
│   ├── main.go           # Entry point
│   ├── handlers/          # Request handlers (like views.py)
│   │   ├── home.go        # Homepage handler
│   │   ├── health.go      # Health & API info handlers
│   │   └── items.go        # CRUD operations handlers
│   ├── models/            # Data models (like models.py)
│   │   └── item.go        # Item structs
│   ├── database/          # Database connection
│   │   └── database.go    # Database initialization
│   └── routes/            # URL routing (like urls.py)
│       └── routes.go      # Route configuration
└── README.md
```

## API Endpoints

### GET /
Homepage with API documentation

### GET /health
Health check endpoint

**Response:**
```json
{
  "status": "ok",
  "message": "Go API is running"
}
```

### GET /api/
API information and available endpoints

**Response:**
```json
{
  "name": "Go REST API",
  "version": "1.0.0",
  "endpoints": {
    "GET /": "Homepage",
    "GET /health": "Health check",
    "GET /api/": "API info",
    "GET /api/items": "List all items",
    "POST /api/items": "Create new item",
    "GET /api/items/:id": "Get item by ID",
    "DELETE /api/items/:id": "Delete item by ID"
  }
}
```

### GET /api/items
List all items

**Response:**
```json
[
  {
    "id": 1,
    "name": "My Item",
    "description": "Item description",
    "created_at": "2024-01-01T12:00:00Z"
  }
]
```

### POST /api/items
Create a new item

**Request:**
```json
{
  "name": "My Item",
  "description": "Item description"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "My Item",
  "description": "Item description",
  "created_at": "2024-01-01T12:00:00Z"
}
```

### GET /api/items/{id}
Get item by ID

**Response:**
```json
{
  "id": 1,
  "name": "My Item",
  "description": "Item description",
  "created_at": "2024-01-01T12:00:00Z"
}
```

### DELETE /api/items/{id}
Delete item by ID

**Response:**
```json
{
  "message": "Item deleted successfully",
  "id": 1
}
```

## Useful Commands

```bash
# View logs
docker-compose logs -f api

# Execute command in container
docker-compose exec api /bin/sh

# Stop containers
docker-compose down

# Stop and remove all (including database)
docker-compose down -v

# Rebuild after code changes
docker-compose up --build
```

## Test API (curl)

```bash
# Health check
curl http://localhost:8000/health

# API info
curl http://localhost:8000/api/

# List items
curl http://localhost:8000/api/items

# Create item
curl -X POST http://localhost:8000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Item","description":"This is a test"}'

# Get item by ID
curl http://localhost:8000/api/items/1

# Delete item
curl -X DELETE http://localhost:8000/api/items/1
```

## Settings

Modify `docker-compose.yml`:

```yaml
environment:
  - POSTGRES_DB=godb
  - POSTGRES_USER=go
  - POSTGRES_PASSWORD=go
  - POSTGRES_HOST=db
  - PORT=8000
```

## What Happens

1. PostgreSQL starts and waits for readiness
2. Go API connects to database
3. Database tables are created automatically
4. Web server starts on port 8000

## Notes

- Demo example only, not production ready
- Data persists in PostgreSQL volume
- Database is initialized automatically on first run
- Uses multi-stage Docker build for smaller image size
- Runs as non-root user for security

## Troubleshooting

### Port already in use
```bash
# Port 8000 or 5433 already used
# Change port in docker-compose.yml
```

### Database connection failed
```bash
# Check container status
docker-compose ps

# Check database logs
docker-compose logs db

# Check API logs
docker-compose logs api
```

### Build fails
```bash
# Clean build cache
docker-compose build --no-cache

# Rebuild
docker-compose up --build
```

## Go Dependencies

- **gin-gonic/gin**: Web framework
- **lib/pq**: PostgreSQL driver
- **joho/godotenv**: Environment variables

## Architecture

This project follows Go best practices with a modular structure:

### Structure Overview

- **main.go**: Application entry point, database connection, server setup
- **handlers/**: Request handlers (business logic) - similar to Django views.py
  - `home.go`: Homepage handler
  - `health.go`: Health check and API info endpoints
  - `items.go`: CRUD operations for items
- **models/**: Data structures - similar to Django models.py
  - `Item`: Response model
  - `CreateItemRequest`: Request model
- **database/**: Database connection and initialization
  - `InitDB()`: Creates tables automatically
- **routes/**: URL routing configuration - similar to Django urls.py
  - `SetupRoutes()`: Registers all endpoints

## Performance

Go provides excellent performance:
- Fast startup time
- Low memory usage
- High throughput
- Compiled binary (no runtime needed)

