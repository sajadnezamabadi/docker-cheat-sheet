# Nginx Docker Example - Ready to Run

A complete Nginx example ready to run with Docker.

## Features

- Complete Nginx server
- Homepage served
- Health check endpoint
- Gzip compression
- Static file serving
- Ready for reverse proxy

## Quick Start

```bash
# Go to project folder
cd templates/nginx

# Build and start container
docker-compose up --build

# Or detached mode
docker-compose up -d --build
Access
Home page: http://localhost

Health check: http://localhost/health

Project Structure
css
Copy code
nginx/
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── html/
│   └── index.html
└── README.md
Useful Commands
bash
Copy code
# View logs
docker-compose logs -f nginx

# Test Nginx configuration
docker-compose exec nginx nginx -t

# Reload configuration without restart
docker-compose exec nginx nginx -s reload

# Stop container
docker-compose down
Test with curl
bash
Copy code
# Get homepage
curl http://localhost

# Health check
curl http://localhost/health

# Get headers
curl -I http://localhost
Settings
Edit nginx.conf to change Nginx configuration. Example reverse proxy:

nginx
Copy code
location /api/ {
    proxy_pass http://backend:8000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
Enabled Features
Gzip Compression

Static File Serving

Health Check /health

Custom Error Pages

Notes
Demo example only

Add security settings for production

Enable SSL/TLS for production

Troubleshooting
Port already in use

bash
Copy code
# Port 80 is in use
# Change port in docker-compose.yml
Permission denied

bash
Copy code
docker-compose exec nginx ls -la /usr/share/nginx/html