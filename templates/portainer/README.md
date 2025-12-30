# Portainer - Docker Web UI

Portainer is a lightweight management UI for Docker. It allows you to manage Docker containers, images, volumes, networks, and more through a web interface.

## Features

- **Web-based UI**: Manage Docker from your browser
- **Container Management**: Start, stop, restart, remove containers
- **Image Management**: Pull, push, remove images
- **Volume Management**: Create, remove, inspect volumes
- **Network Management**: Create and manage networks
- **Stack Management**: Deploy and manage Docker Compose stacks
- **Swarm Support**: Manage Docker Swarm clusters
- **User Management**: Multi-user support with roles
- **Templates**: Pre-configured application templates

## Quick Start

### Standalone Docker

```bash
# Go to project folder
cd templates/portainer

# Start Portainer
docker-compose up -d

# Access Portainer
# HTTP:  http://localhost:9000
# HTTPS: https://localhost:9443
```

### Docker Swarm

```bash
# Deploy Portainer on Swarm
docker stack deploy -c docker-compose.swarm.yml portainer

# Access Portainer
# HTTP:  http://localhost:9000
# HTTPS: https://localhost:9443
```

## First Time Setup

1. **Open Portainer**: Navigate to `http://localhost:9000` or `https://localhost:9443`

2. **Create Admin User**:
   - Username: `admin` (or your choice)
   - Password: Create a strong password
   - Click "Create user"

3. **Select Environment**:
   - Choose "Docker" for standalone Docker
   - Choose "Docker Swarm" if using Swarm mode

4. **Start Managing**: You're ready to use Portainer!

## Access URLs

- **HTTP**: http://localhost:9000
- **HTTPS**: https://localhost:9443 (recommended for production)

## What You Can Do

### Container Management

- View all containers
- Start/Stop/Restart containers
- View container logs
- Execute commands in containers
- View container stats (CPU, memory, network)
- Remove containers

### Image Management

- Browse Docker Hub images
- Pull images
- Remove images
- View image details
- Build images from Dockerfile

### Volume Management

- List all volumes
- Create new volumes
- Remove volumes
- Inspect volume details
- View volume usage

### Network Management

- List networks
- Create networks
- Remove networks
- Inspect network details

### Stack Management

- Deploy Docker Compose stacks
- View stack status
- Update stacks
- Remove stacks
- View stack logs

### Swarm Management (if using Swarm)

- View Swarm cluster
- Manage nodes
- Deploy services
- Scale services
- View service logs

## Useful Commands

### Standalone Docker

```bash
# Start Portainer
docker-compose up -d

# Stop Portainer
docker-compose down

# View logs
docker-compose logs -f portainer

# Restart Portainer
docker-compose restart portainer

# Update Portainer
docker-compose pull
docker-compose up -d
```

### Docker Swarm

```bash
# Deploy Portainer
docker stack deploy -c docker-compose.swarm.yml portainer

# View Portainer service
docker stack services portainer

# View Portainer logs
docker service logs portainer_portainer

# Update Portainer
docker service update --image portainer/portainer-ce:latest portainer_portainer

# Remove Portainer
docker stack rm portainer
```

## Configuration

### Change Port

Edit `docker-compose.yml`:

```yaml
ports:
  - "8080:9000"  # Change 9000 to 8080
  - "8443:9443"  # Change 9443 to 8443
```

### Use HTTPS Only

```yaml
ports:
  - "9443:9443"  # Remove HTTP port
```

### Persistent Data

Data is stored in `portainer_data` volume. To backup:

```bash
# Backup Portainer data
docker run --rm -v portainer_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/portainer-backup.tar.gz /data

# Restore Portainer data
docker run --rm -v portainer_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/portainer-backup.tar.gz -C /data
```

## Security Considerations

### Production Setup

1. **Use HTTPS**: Always use HTTPS in production
2. **Strong Password**: Use a strong admin password
3. **Firewall**: Restrict access to Portainer ports
4. **Reverse Proxy**: Use Nginx/Traefik as reverse proxy
5. **SSL Certificate**: Use valid SSL certificates

### Example with Nginx Reverse Proxy

```nginx
server {
    listen 443 ssl;
    server_name portainer.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

### Port Already in Use

```bash
# Check what's using port 9000
sudo lsof -i :9000

# Change port in docker-compose.yml
ports:
  - "8080:9000"
```

### Cannot Connect to Docker

```bash
# Check Docker socket permissions
ls -la /var/run/docker.sock

# Add user to docker group
sudo usermod -aG docker $USER
# Log out and log in again
```

### Portainer Not Starting

```bash
# Check logs
docker-compose logs portainer

# Check container status
docker-compose ps

# Restart Portainer
docker-compose restart portainer
```

### Reset Admin Password

```bash
# Stop Portainer
docker-compose down

# Remove data volume (WARNING: This deletes all data)
docker volume rm portainer_data

# Start Portainer again
docker-compose up -d
# You'll be prompted to create a new admin user
```

## Advanced Features

### Multiple Docker Environments

Portainer supports managing multiple Docker environments:

1. Go to "Environments" in Portainer
2. Click "Add environment"
3. Choose environment type (Docker, Swarm, Kubernetes)
4. Configure connection details
5. Start managing!

### Templates

Portainer includes pre-configured templates for common applications:

- WordPress
- MySQL
- PostgreSQL
- Redis
- Nginx
- And many more!

Access templates from the "App Templates" section.

### User Management

Create multiple users with different roles:

- **Administrator**: Full access
- **User**: Limited access
- **Operator**: Can manage containers but not settings

### API Access

Portainer provides REST API for automation:

- API documentation: `http://localhost:9000/api/docs`
- API key: Generate from "My account" → "API keys"

## Integration Examples

### With Docker Compose

You can add Portainer to any `docker-compose.yml`:

```yaml
services:
  portainer:
    image: portainer/portainer-ce:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - portainer_data:/data
    ports:
      - "9000:9000"
    restart: unless-stopped
```

### With Docker Swarm

Deploy Portainer as a stack:

```bash
docker stack deploy -c docker-compose.swarm.yml portainer
```

## Useful Links

- [Portainer Official Website](https://www.portainer.io/)
- [Portainer Documentation](https://docs.portainer.io/)
- [Portainer GitHub](https://github.com/portainer/portainer)
- [Portainer Community](https://www.portainer.io/community)

## Notes

- Portainer Community Edition (CE) is free and open source
- Portainer Business Edition (BE) has additional features
- Data persists in `portainer_data` volume
- Portainer requires access to Docker socket
- Use HTTPS in production environments

