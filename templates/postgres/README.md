# PostgreSQL Docker Example - Ready to Run

PostgreSQL server with Python Flask app, ready to run with Docker.

## Features

- PostgreSQL server
- Python Flask app
- Homepage with DB info
- API endpoints for PostgreSQL
- Sample data
- `users` table with example rows

## Quick Start

```bash
cd templates/postgres
docker-compose up --build
# Or detached
docker-compose up -d --build
Access
Homepage: http://localhost:5000

API Info: http://localhost:5000/api/

Users List: http://localhost:5000/api/users

PostgreSQL CLI: docker-compose exec db psql -U postgres -d mydb

Project Structure
csharp
Copy code
postgres/
├── Dockerfile
├── Dockerfile.app
├── docker-compose.yml
├── init.sql
├── demo.py
├── requirements.txt
└── README.md
API Endpoints
GET / - homepage

GET /api/ - API info & DB status

GET /api/users - list users

POST /api/users?name=<name>&email=<email> - create user

Useful Commands
bash
Copy code
docker-compose logs -f app
docker-compose exec db psql -U postgres -d mydb

# PostgreSQL CLI commands:
# SELECT * FROM users;
# INSERT INTO users (name,email) VALUES ('Test','test@example.com');
# \dt
# \q

docker-compose down
docker-compose down -v
Test API (curl)
bash
Copy code
curl http://localhost:5000/api/
curl http://localhost:5000/api/users
curl -X POST "http://localhost:5000/api/users?name=Test&email=test@example.com"
Sample Data
init.sql includes three sample users:

John Doe (john@example.com)

Jane Smith (jane@example.com)

Bob Johnson (bob@example.com)

Settings
Change docker-compose.yml:

yaml
Copy code
environment:
  POSTGRES_DB: mydb
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: postgres
Notes
Data persists in volume

init.sql runs only on first start

Troubleshooting
Port in use: change port in docker-compose.yml
Connection refused: check docker-compose ps and docker-compose logs db