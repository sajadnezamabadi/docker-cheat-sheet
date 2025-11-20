# Node.js Docker Example - Ready to Run

Complete Node.js + Express project ready to run with Docker.

## Features

- Node.js + Express server
- Homepage served
- RESTful API endpoints
- PostgreSQL connection
- CRUD operations for items

## Quick Start

```bash
cd templates/node
docker-compose up --build
# Or detached
docker-compose up -d --build
Access
Homepage: http://localhost:3000

API Info: http://localhost:3000/api/

Items List: http://localhost:3000/api/items

Health Check: http://localhost:3000/health

Project Structure
pgsql
Copy code
node/
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── package.json
├── server.js
└── README.md
API Endpoints
GET / - homepage

GET /api/ - API info

GET /api/items - list items

POST /api/items - create item

json
Copy code
{
  "name": "My Item",
  "description": "Item description"
}
GET /api/items/:id - get item by ID

DELETE /api/items/:id - delete item

GET /health - health check

Useful Commands
bash
Copy code
docker-compose logs -f app
docker-compose exec app node -e "console.log('Hello')"
docker-compose down
docker-compose down -v
Test API (curl)
bash
Copy code
curl http://localhost:3000/api/
curl -X POST "http://localhost:3000/api/items" -H "Content-Type: application/json" -d '{"name":"Test Item","description":"This is a test"}'
curl http://localhost:3000/api/items/
curl http://localhost:3000/api/items/1
curl -X DELETE http://localhost:3000/api/items/1
Settings
Change docker-compose.yml:

yaml
Copy code
environment:
  - NODE_ENV=development
  - POSTGRES_DB=nodedb
  - POSTGRES_USER=node
  - POSTGRES_PASSWORD=node
Notes
Demo only, not production-ready

Data in memory is lost on restart

Use real database for production

Troubleshooting
Port in use: change port in docker-compose.yml
Database connection failed: check docker-compose ps and docker-compose logs db

markdown
Copy code
