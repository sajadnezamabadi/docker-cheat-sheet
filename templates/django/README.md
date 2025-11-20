# Django Docker Example - Ready to Run

A complete Django project ready to run with Docker.

## Features

- Complete Django project
- PostgreSQL integration
- Demo app with homepage
- API endpoint for testing
- Admin panel ready
- Automatic migrations
- Superuser created automatically (admin/admin123)

## Quick Start

```bash
# Go to project folder
cd templates/django

# Build and start containers
docker-compose up --build

# Or detached mode
docker-compose up -d --build

Access

Home page: http://localhost:8000

API Info: http://localhost:8000/api/

Admin Panel:

Username: admin

Password: admin123

Project Structure
django/
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh      # Auto-start script
├── requirements.txt
├── manage.py
├── myproject/         # Django settings
└── demo/              # Sample app
    └── templates/demo/home.html

Useful Commands
# View logs
docker-compose logs -f web

# Run Django command
docker-compose exec web python manage.py <command>

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Stop containers
docker-compose down

# Stop and remove all (including database)
docker-compose down -v

What Happens

PostgreSQL starts

Django waits for database readiness

Migrations run automatically

Superuser created if missing

Django server starts on port 8000

Settings

Modify docker-compose.yml:

environment:
  - DEBUG=1
  - POSTGRES_DB=djangodb
  - POSTGRES_USER=django
  - POSTGRES_PASSWORD=django

Notes

Demo example only, not production ready

Change secret key in production

DEBUG=1 only for development

Superuser created automatically

Troubleshooting

Port already in use

# Port 8000 or 5433 already used
# Change port in docker-compose.yml


Database connection failed

docker-compose ps
docker-compose logs db


Migrations failed

docker-compose down -v
docker-compose up --build
