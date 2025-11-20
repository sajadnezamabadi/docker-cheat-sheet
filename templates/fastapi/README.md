# FastAPI Docker Example - Ready to Run

A complete FastAPI project ready to run with Docker.

## Features

- Complete FastAPI project
- HTML homepage
- Full API endpoints
- Interactive API Docs (Swagger & ReDoc)
- PostgreSQL integration
- CRUD operations for items

## Quick Start

```bash
# Go to project folder
cd templates/fastapi

# Build and start containers
docker-compose up --build

# Or detached mode
docker-compose up -d --build

Access

Home page: http://localhost:8000

API Info: http://localhost:8000/api/

Swagger Docs: http://localhost:8000/docs

ReDoc Docs: http://localhost:8000/redoc

Project Structure
fastapi/
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── main.py
└── README.md

API Endpoints

GET / - Home page

GET /api/ - API info

GET /items/ - List items

POST /items/ - Create new item

{
  "name": "My Item",
  "description": "Item description"
}


GET /items/{item_id} - Get item by ID

DELETE /items/{item_id} - Delete item by ID

Useful Commands
# View logs
docker-compose logs -f api

# Execute command in container
docker-compose exec api python -c "print('Hello')"

# Stop containers
docker-compose down

# Stop and remove all (including database)
docker-compose down -v

Settings

Modify docker-compose.yml:

environment:
  - POSTGRES_DB=fastapidb
  - POSTGRES_USER=fastapi
  - POSTGRES_PASSWORD=fastapi

Notes

Demo example only, not production ready

Data stored in memory (lost on restart)

Use a real database for production

Troubleshooting

Port already in use

# Port 8000 or 5433 already used
# Change port in docker-compose.yml


Database connection failed

docker-compose ps
docker-compose logs db