# Docker Registry Setup

Complete guide to setting up private Docker registries and Harbor.

## Docker Registry (Basic)

### Simple Registry Setup

```yaml
# docker-compose.registry.yml
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY: /data
    volumes:
      - registry_data:/data

volumes:
  registry_data:
```

### Registry with Authentication

```yaml
# docker-compose.registry-auth.yml
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_AUTH: htpasswd
      REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
      REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
    volumes:
      - registry_data:/data
      - ./auth:/auth

volumes:
  registry_data:
```

### Create Authentication File

```bash
# Install htpasswd
sudo apt-get install apache2-utils

# Create password file
htpasswd -Bbn username password > auth/htpasswd

# Add more users
htpasswd -B auth/htpasswd anotheruser
```

### Push/Pull from Private Registry

```bash
# Login to registry
docker login localhost:5000

# Tag image
docker tag myimage:latest localhost:5000/myimage:latest

# Push image
docker push localhost:5000/myimage:latest

# Pull image
docker pull localhost:5000/myimage:latest
```

### Registry with TLS

```yaml
# docker-compose.registry-tls.yml
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_HTTP_TLS_CERTIFICATE: /certs/domain.crt
      REGISTRY_HTTP_TLS_PRIVATE_KEY: /certs/domain.key
    volumes:
      - registry_data:/data
      - ./certs:/certs

volumes:
  registry_data:
```

## Harbor Setup

### Complete Harbor Installation

```yaml
# docker-compose.harbor.yml
version: '3.8'

services:
  log:
    image: goharbor/harbor-log:latest
    container_name: harbor-log
    restart: always
    volumes:
      - ./log:/var/log/docker/
    networks:
      - harbor

  registry:
    image: goharbor/registry-photon:v2.10.0
    container_name: registry
    restart: always
    volumes:
      - ./data/registry:/storage
      - ./common/config/registry/:/etc/registry/
    networks:
      - harbor
    depends_on:
      - log

  registryctl:
    image: goharbor/harbor-registryctl:v2.10.0
    container_name: registryctl
    restart: always
    volumes:
      - ./data/registry:/storage
      - ./common/config/registry/:/etc/registry/
    networks:
      - harbor
    depends_on:
      - log
      - registry

  postgresql:
    image: goharbor/harbor-db:v2.10.0
    container_name: harbor-db
    restart: always
    volumes:
      - ./data/database:/var/lib/postgresql/data
    networks:
      - harbor
    depends_on:
      - log

  core:
    image: goharbor/harbor-core:v2.10.0
    container_name: harbor-core
    restart: always
    volumes:
      - ./common/config/core:/etc/core
      - ./data/ca_download/:/etc/core/ca/
      - ./data/:/data/
    networks:
      - harbor
    depends_on:
      - log
      - registry
      - postgresql

  portal:
    image: goharbor/harbor-portal:v2.10.0
    container_name: harbor-portal
    restart: always
    networks:
      - harbor
    depends_on:
      - log
      - core

  jobservice:
    image: goharbor/harbor-jobservice:v2.10.0
    container_name: harbor-jobservice
    restart: always
    volumes:
      - ./common/config/jobservice:/etc/jobservice
      - ./data/job_logs:/var/log/jobs
      - ./data/:/data/
    networks:
      - harbor
    depends_on:
      - log
      - redis
      - core

  redis:
    image: goharbor/redis-photon:v2.10.0
    container_name: redis
    restart: always
    volumes:
      - ./data/redis:/var/lib/redis
    networks:
      - harbor
    depends_on:
      - log

  proxy:
    image: goharbor/nginx-photon:v2.10.0
    container_name: nginx
    restart: always
    volumes:
      - ./common/config/nginx:/etc/nginx
    ports:
      - "80:8080"
      - "443:8443"
    networks:
      - harbor
    depends_on:
      - log
      - registry
      - core
      - portal

networks:
  harbor:
    external: false
```

### Harbor Installation (Official Method)

```bash
# Download Harbor installer
wget https://github.com/goharbor/harbor/releases/download/v2.10.0/harbor-offline-installer-v2.10.0.tgz

# Extract
tar xvf harbor-offline-installer-v2.10.0.tgz
cd harbor

# Configure
cp harbor.yml.tmpl harbor.yml
# Edit harbor.yml with your settings

# Install
sudo ./install.sh
```

### Harbor Configuration

```yaml
# harbor.yml
hostname: registry.example.com
http:
  port: 80
https:
  port: 443
  certificate: /path/to/cert.crt
  private_key: /path/to/key.key

harbor_admin_password: Harbor12345

database:
  password: root123
  max_idle_conns: 50
  max_open_conns: 1000

data_volume: /data
```

## Registry Management

### List Images in Registry

```bash
# Using registry API
curl -X GET http://localhost:5000/v2/_catalog

# List tags for specific image
curl -X GET http://localhost:5000/v2/myimage/tags/list
```

### Delete Image from Registry

```bash
# Get digest
curl -I -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
  http://localhost:5000/v2/myimage/manifests/latest

# Delete manifest
curl -X DELETE http://localhost:5000/v2/myimage/manifests/<digest>
```

### Registry Garbage Collection

```bash
# Run garbage collection
docker exec registry registry garbage-collect /etc/docker/registry/config.yml

# Dry run
docker exec registry registry garbage-collect --dry-run /etc/docker/registry/config.yml
```

## Registry with S3 Backend

```yaml
# docker-compose.registry-s3.yml
services:
  registry:
    image: registry:2
    ports:
      - "5000:5000"
    environment:
      REGISTRY_STORAGE: s3
      REGISTRY_STORAGE_S3_ACCESSKEY: your-access-key
      REGISTRY_STORAGE_S3_SECRETKEY: your-secret-key
      REGISTRY_STORAGE_S3_BUCKET: my-registry-bucket
      REGISTRY_STORAGE_S3_REGION: us-east-1
    volumes:
      - registry_data:/data

volumes:
  registry_data:
```

## Registry Mirror

```json
# /etc/docker/daemon.json
{
  "registry-mirrors": [
    "https://registry.example.com",
    "https://mirror.example.com"
  ]
}
```

## Best Practices

1. **Use HTTPS**: Always use TLS for production registries
2. **Authentication**: Implement proper authentication
3. **Storage Backend**: Use S3 or other persistent storage
4. **Garbage Collection**: Regularly clean up unused images
5. **Backup**: Backup registry data regularly
6. **Monitoring**: Monitor registry performance and storage
7. **Access Control**: Implement proper access control policies
8. **Image Scanning**: Scan images for vulnerabilities
9. **Retention Policies**: Set up image retention policies
10. **Documentation**: Document registry usage and policies

## Harbor Features

- **Role-Based Access Control**: Fine-grained permissions
- **Image Scanning**: Vulnerability scanning with Trivy/Clair
- **Image Replication**: Sync images between registries
- **Webhooks**: Event notifications
- **Helm Chart Repository**: Store Helm charts
- **Image Retention**: Automatic cleanup policies
- **Quota Management**: Storage quotas per project
- **Audit Logs**: Complete audit trail

