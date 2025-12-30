# Rust Docker Example - Ready to Run

A complete Rust REST API with PostgreSQL, ready to run with Docker.

## Features

- Rust web server (Actix-web)
- PostgreSQL integration
- Full CRUD operations
- RESTful API endpoints
- JSON responses
- Automatic database initialization
- Health check endpoint

## Quick Start

```bash
# Go to project folder
cd templates/rust

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
rust/
├── Dockerfile
├── docker-compose.yml
├── Cargo.toml
├── entrypoint.sh
├── src/
│   ├── main.rs           # Entry point
│   ├── handlers/          # Request handlers (like views.py)
│   │   ├── mod.rs
│   │   ├── home.rs        # Homepage handler
│   │   ├── health.rs      # Health & API info handlers
│   │   └── items.rs       # CRUD operations handlers
│   ├── models/            # Data models (like models.py)
│   │   └── mod.rs         # Item structs
│   ├── database/          # Database connection
│   │   └── mod.rs         # Database initialization
│   └── routes/            # URL routing (like urls.py)
│       └── mod.rs         # Route configuration
└── README.md
```

## API Endpoints

### GET /
Homepage with API documentation

### GET /health
Health check endpoint

### GET /api/
API information and available endpoints

### GET /api/items
List all items

**Response:**
```json
[
  {
    "id": 1,
    "name": "My Item",
    "description": "Item description",
    "created_at": "2024-01-01 12:00:00"
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
  "created_at": "2024-01-01 12:00:00"
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
  "created_at": "2024-01-01 12:00:00"
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
  - POSTGRES_DB=rustdb
  - POSTGRES_USER=rust
  - POSTGRES_PASSWORD=rust
  - POSTGRES_HOST=db
```

## What Happens

1. PostgreSQL starts and waits for readiness
2. Rust API connects to database
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

## Rust Dependencies

- **actix-web**: Web framework
- **tokio**: Async runtime
- **sqlx**: PostgreSQL driver
- **serde**: Serialization
- **chrono**: Date/time handling

## Performance

Rust provides excellent performance:
- Fast startup time
- Low memory usage
- High throughput
- Type safety at compile time

