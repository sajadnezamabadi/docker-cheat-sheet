# Docker Registry Example - Ready to Run

A complete Docker Registry setup ready to run with authentication and TLS support.

## Features

- Docker Registry 2.0
- Authentication with htpasswd
- Self-signed TLS certificate (for testing)
- Health checks
- Persistent storage
- Simple mode (no auth) available

## Quick Start

### Method 1: With Setup Script (Recommended)

```bash
# Go to registry folder
cd templates/registry

# Run setup script (creates users and certificates)
chmod +x setup.sh
./setup.sh

# Start registry (with authentication)
docker-compose up -d
```

### Method 2: Simple Registry (No Authentication)

```bash
# Start simple registry without authentication
cd templates/registry
docker-compose -f docker-compose.simple.yml up -d
```

### Method 3: With TLS (After Running Setup)

```bash
# After running setup.sh (creates certificates)
cd templates/registry
docker-compose -f docker-compose.tls.yml up -d
```

### Default Credentials

- Username: `admin`
- Password: `admin123`

## Access

- **Registry URL**: `localhost:5000`
- **API Endpoint**: `http://localhost:5000/v2/`

## Usage Examples

### Complete Example: Push and Pull Image

```bash
# 1. Start registry
docker-compose up -d

# 2. Login to registry
docker login localhost:5000
# Username: admin
# Password: admin123

# 3. Pull a test image
docker pull alpine:latest

# 4. Tag image for registry
docker tag alpine:latest localhost:5000/alpine:latest

# 5. Push image to registry
docker push localhost:5000/alpine:latest

# 6. Remove local image
docker rmi localhost:5000/alpine:latest

# 7. Pull image back from registry
docker pull localhost:5000/alpine:latest

# 8. Verify image
docker images | grep localhost:5000
```

### Push Your Own Image

```bash
# Build your image
docker build -t myapp:latest .

# Tag for registry
docker tag myapp:latest localhost:5000/myapp:latest

# Push to registry
docker push localhost:5000/myapp:latest
```

### Pull Image from Registry

```bash
# Pull image
docker pull localhost:5000/myapp:latest

# Run container from registry image
docker run -d -p 8080:80 localhost:5000/myapp:latest
```

### Test Registry

```bash
# Run test script
chmod +x test_registry.sh
./test_registry.sh localhost:5000 alpine:latest
```

## Registry API

### List All Images

```bash
curl http://localhost:5000/v2/_catalog
```

### List Tags for Image

```bash
curl http://localhost:5000/v2/myimage/tags/list
```

### Get Image Manifest

```bash
curl -I -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
  http://localhost:5000/v2/myimage/manifests/latest
```

## Configuration

### Add New User

```bash
# Add user to htpasswd
htpasswd -B auth/htpasswd newuser

# Restart registry
docker-compose restart
```

### Use Custom Certificate

```bash
# Place your certificate files
cp your-cert.crt certs/domain.crt
cp your-key.key certs/domain.key

# Restart registry
docker-compose restart
```

### Use S3 Backend

Edit `docker-compose.yml`:

```yaml
environment:
  REGISTRY_STORAGE: s3
  REGISTRY_STORAGE_S3_ACCESSKEY: your-access-key
  REGISTRY_STORAGE_S3_SECRETKEY: your-secret-key
  REGISTRY_STORAGE_S3_BUCKET: my-registry-bucket
  REGISTRY_STORAGE_S3_REGION: us-east-1
```

## Project Structure

```
registry/
├── docker-compose.yml          # Registry with authentication
├── docker-compose.simple.yml   # Simple registry (no auth)
├── docker-compose.tls.yml      # Registry with auth and TLS
├── setup.sh                    # Setup script
├── test_registry.sh            # Test script
├── auth/
│   └── htpasswd                # User credentials (created by setup.sh)
├── certs/
│   ├── domain.crt              # SSL certificate (created by setup.sh)
│   └── domain.key              # SSL private key (created by setup.sh)
└── README.md
```

## Useful Commands

```bash
# View logs
docker-compose logs -f registry

# Check registry health
curl http://localhost:5000/v2/

# List all images
curl http://localhost:5000/v2/_catalog

# Garbage collection (cleanup)
docker exec docker-registry registry garbage-collect /etc/docker/registry/config.yml

# Stop registry
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Production Considerations

1. **Use Proper Certificates**: Replace self-signed certs with CA-signed certificates
2. **Strong Passwords**: Change default admin password
3. **Backup**: Regularly backup registry data volume
4. **Monitoring**: Set up monitoring for registry
5. **Storage Backend**: Use S3 or other persistent storage
6. **Access Control**: Implement proper access control policies
7. **Garbage Collection**: Schedule regular garbage collection
8. **HTTPS Only**: Use HTTPS in production

## Troubleshooting

### Cannot Push Image

```bash
# Check if registry is running
docker-compose ps

# Check logs
docker-compose logs registry

# Verify authentication
docker login localhost:5000
```

### Certificate Errors

```bash
# For testing, add to /etc/docker/daemon.json
{
  "insecure-registries": ["localhost:5000"]
}

# Restart Docker
sudo systemctl restart docker
```

### Port Already in Use

```bash
# Change port in docker-compose.yml
ports:
  - "5001:5000"  # Use different port
```

## Notes

- Self-signed certificates are for testing only
- For production, use proper TLS certificates
- Default credentials should be changed
- Registry data is stored in Docker volume

