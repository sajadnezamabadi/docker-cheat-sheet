# Redis Docker Example - Ready to Run

Redis server with Python Flask app, ready to run with Docker.

## Features

- Redis server
- Python Flask app
- Homepage with counter
- API endpoints for Redis
- Persistence with AOF

## Quick Start

```bash
cd templates/redis
docker-compose up --build
# Or detached
docker-compose up -d --build
Access
Homepage: http://localhost:5000

API Info: http://localhost:5000/api/

Redis CLI: docker-compose exec redis redis-cli

Project Structure
Copy code
redis/
├── Dockerfile
├── docker-compose.yml
├── redis.conf
├── demo.py
├── requirements.txt
└── README.md
API Endpoints
GET / - homepage with counter

GET /api/ - API info & Redis status

GET /api/increment - increment counter

GET /api/counter - get counter value

GET /api/reset - reset counter to 0

POST /api/set?value=<number> - set counter value

Useful Commands
bash
Copy code
docker-compose logs -f app
docker-compose exec redis redis-cli

# Redis CLI commands:
# GET counter
# SET counter 10
# INCR counter
# KEYS *

docker-compose down
docker-compose down -v
Test API (curl)
bash
Copy code
curl http://localhost:5000/api/
curl http://localhost:5000/api/increment
curl http://localhost:5000/api/counter
curl http://localhost:5000/api/reset
curl -X POST "http://localhost:5000/api/set?value=100"
Redis Settings
Edit redis.conf as needed.

Notes
Data persists with AOF

Counter stored in key counter

Data preserved on restart

Troubleshooting
Port in use: change port in docker-compose.yml
Connection refused: check docker-compose ps and docker-compose logs redis