# Docker Security Best Practices

Comprehensive security guide for Docker containers and images.

## Image Security

### 1. Use Official Base Images

```dockerfile
# Good - Official image
FROM node:18-alpine

# Bad - Unofficial or outdated
FROM some-random-user/node:latest
```

### 2. Pin Image Versions

```dockerfile
# Good - Specific version
FROM node:18.17.0-alpine

# Bad - Latest tag
FROM node:latest
```

### 3. Use Minimal Base Images

```dockerfile
# Good - Alpine (smaller attack surface)
FROM python:3.11-alpine

# Bad - Full OS image
FROM ubuntu:22.04
```

## Image Scanning

### Docker Scout

```bash
# Scan image for vulnerabilities
docker scout cves <image>

# Scan and show recommendations
docker scout recommendations <image>

# Compare two images
docker scout compare <old-image> <new-image>
```

### Trivy

```bash
# Install Trivy
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy

# Scan image
trivy image <image>

# Scan with JSON output
trivy image -f json -o report.json <image>

# Scan filesystem
trivy fs .
```

### Snyk

```bash
# Install Snyk
npm install -g snyk

# Authenticate
snyk auth

# Test Docker image
snyk test --docker <image>

# Monitor image
snyk monitor --docker <image>
```

## Secrets Management

### Docker Secrets (Swarm Mode)

```bash
# Create secret
echo "my-secret-password" | docker secret create db_password -

# Use in service
docker service create \
  --secret db_password \
  --name myapp \
  myapp:latest

# Secret is available at /run/secrets/db_password in container
```

### Environment Variables (Not for Secrets)

```yaml
# docker-compose.yml
services:
  app:
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/db
    # Better: Use env_file
    env_file:
      - .env
```

### Docker Compose Secrets

```yaml
# docker-compose.yml
services:
  app:
    secrets:
      - db_password
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### External Secret Managers

#### HashiCorp Vault

```bash
# Run Vault
docker run -d --name vault \
  -p 8200:8200 \
  -e 'VAULT_DEV_ROOT_TOKEN_ID=myroot' \
  vault:latest

# Store secret
vault kv put secret/db password=mysecret

# Retrieve in application
# Use Vault API or SDK
```

#### AWS Secrets Manager

```python
# Python example
import boto3

client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='db_password')
password = response['SecretString']
```

## Container Security

### Run as Non-Root User

```dockerfile
# Create user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Switch to user
USER appuser

# Verify
RUN id
```

### Read-Only Root Filesystem

```bash
# Run with read-only root
docker run --read-only <image>

# Mount tmpfs for writable directories
docker run --read-only --tmpfs /tmp <image>
```

### Limit Capabilities

```bash
# Drop all capabilities, add only needed
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE <image>

# Remove specific capabilities
docker run --cap-drop CHOWN <image>
```

### Resource Limits

```yaml
# docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 256M
```

## Network Security

### Use Custom Networks

```bash
# Create isolated network
docker network create --driver bridge isolated_network

# Connect container
docker run --network isolated_network <image>
```

### Firewall Rules

```bash
# Block all incoming, allow specific
docker run -p 127.0.0.1:8080:8080 <image>

# Use iptables
sudo iptables -A DOCKER -p tcp --dport 8080 -j DROP
```

## Image Build Security

### Multi-Stage Builds

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Production stage (no build tools)
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER node
CMD ["node", "server.js"]
```

### .dockerignore

```dockerignore
# Exclude sensitive files
.env
*.key
*.pem
secrets/
.git/
```

### Build Arguments

```dockerfile
# Use build args for non-sensitive data
ARG NODE_VERSION=18
FROM node:${NODE_VERSION}-alpine

# Don't use for secrets (they're visible in image history)
```

## Runtime Security

### Security Options

```bash
# Disable new privileges
docker run --security-opt=no-new-privileges <image>

# AppArmor profile
docker run --security-opt apparmor=my-profile <image>

# SELinux
docker run --security-opt label=type:container_runtime_t <image>
```

### User Namespaces

```bash
# Enable user namespace remapping
# Edit /etc/docker/daemon.json
{
  "userns-remap": "default"
}

# Restart Docker
sudo systemctl restart docker
```

## Logging and Auditing

### Enable Audit Logging

```bash
# Configure auditd
sudo auditctl -w /var/lib/docker -k docker

# View audit logs
sudo ausearch -k docker
```

### Container Logging

```yaml
# docker-compose.yml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "production"
```

## Security Checklist

- [ ] Use official, minimal base images
- [ ] Pin image versions (no :latest)
- [ ] Scan images for vulnerabilities
- [ ] Run containers as non-root user
- [ ] Use read-only root filesystem when possible
- [ ] Limit container capabilities
- [ ] Set resource limits
- [ ] Use secrets management (not env vars for secrets)
- [ ] Enable security options (no-new-privileges)
- [ ] Use custom networks for isolation
- [ ] Implement proper logging
- [ ] Keep Docker and images updated
- [ ] Use multi-stage builds
- [ ] Exclude sensitive files with .dockerignore
- [ ] Enable user namespace remapping
- [ ] Regular security audits

## Tools

- **Docker Scout**: Built-in vulnerability scanning
- **Trivy**: Comprehensive security scanner
- **Snyk**: Security scanning and monitoring
- **Clair**: Static analysis of container images
- **Falco**: Runtime security monitoring
- **Notary**: Content trust and signing

