# Docker Cheat Sheet & Commands

A comprehensive collection of Docker commands, cheatsheets, templates, and examples for developers.

##  Project Structure

```
docker-cheat-sheet-commands/
│
├── scripts/
│   ├── install.sh          # Docker installation script
│   ├── uninstall.sh         # Docker uninstallation script
│   ├── docker_clean.sh      # Clean up Docker resources
│   └── docker_backup.sh     # Backup Docker volumes
│
├── cheatsheets/
│   ├── docker_cli.md                    # Docker CLI commands reference
│   ├── docker_compose.md                # Docker Compose commands reference
│   └── dockerfile_best_practices.md     # Dockerfile best practices
│
├── guides/
│   ├── troubleshooting.md               # Troubleshooting common issues
│   ├── production_deployment.md         # Production deployment guide
│   ├── ci_cd_examples.md                # CI/CD pipeline examples
│   └── advanced/
│       ├── security.md                  # Docker security, image scanning, secrets
│       ├── monitoring.md                # Prometheus + Grafana, ELK
│       ├── advanced_networking.md       # Overlay networks, service discovery, load balancing
│       ├── microservices.md             # Multi-container/microservices example, service mesh
│       ├── dockerignore_examples.md     # .dockerignore examples per language
│       ├── registry_setup.md            # Private registry, Harbor
│       └── docker_swarm.md              # Docker Swarm orchestration
│
├── templates/
│   ├── django/              # Django Docker setup
│   ├── fastapi/             # FastAPI Docker setup
│   ├── node/                # Node.js Docker setup
│   ├── go/                  # Go REST API Docker setup
│   ├── rust/                # Rust REST API Docker setup
│   ├── redis/               # Redis Docker setup
│   ├── postgres/            # PostgreSQL Docker setup
│   ├── nginx/               # Nginx Docker setup
│   ├── registry/            # Docker Registry setup
│   ├── portainer/           # Portainer web UI for Docker
│   └── swarm/               # Docker Swarm examples
│       ├── single-node/     # Single-node Swarm setup
│       └── multi-node/      # Multi-node Swarm setup
│
├── examples/
│   ├── dockerfile_multi_stage.md        # Multi-stage build examples
│   ├── docker_networking_examples.md    # Docker networking examples
│   └── docker_volumes_backup.md         # Volumes and backup strategies
│
└── README.md
```

##  Quick Start

### Installation

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Install Docker
./scripts/install.sh
```

### Usage

```bash
# Clean up Docker resources
./scripts/docker_clean.sh
```

##  Cheatsheets

### Docker CLI
Comprehensive reference for Docker command-line interface commands. See [docker_cli.md](cheatsheets/docker_cli.md)

### Docker Compose
Complete guide for Docker Compose commands and configuration. See [docker_compose.md](cheatsheets/docker_compose.md)

### Dockerfile Best Practices
Best practices and patterns for writing efficient Dockerfiles. See [dockerfile_best_practices.md](cheatsheets/dockerfile_best_practices.md)

##  Templates

Ready-to-use Docker configurations for popular technologies:

- **Django**: Full Django setup with PostgreSQL
- **FastAPI**: FastAPI application with database
- **Node.js**: Node.js application template
- **Go**: Go REST API with PostgreSQL
- **Rust**: Rust REST API with PostgreSQL
- **Redis**: Redis server configuration
- **PostgreSQL**: PostgreSQL database setup
- **Nginx**: Nginx reverse proxy configuration
- **Registry**: Docker Registry with authentication and TLS
- **Portainer**: Web-based Docker management UI
- **Swarm**: Docker Swarm orchestration (single-node and multi-node examples)

Each template includes:
- `Dockerfile` - Container image definition
- `docker-compose.yml` - Multi-container setup
- Configuration files as needed

##  Guides

### Troubleshooting
Complete guide to solving common Docker issues. See [troubleshooting.md](guides/troubleshooting.md)

### Production Deployment
Best practices for deploying Docker in production. See [production_deployment.md](guides/production_deployment.md)

### CI/CD Examples
Complete CI/CD pipeline examples with GitHub Actions, GitLab CI, and Jenkins. See [ci_cd_examples.md](guides/ci_cd_examples.md)

### Advanced Guides

#### Security
Docker security best practices, image scanning, and secrets management. See [security.md](guides/advanced/security.md)

#### Monitoring
Setup Prometheus + Grafana and ELK stack for container monitoring. See [monitoring.md](guides/advanced/monitoring.md)

#### Advanced Networking
Overlay networks, service discovery, and load balancing. See [advanced_networking.md](guides/advanced/advanced_networking.md)

#### Microservices
Complete microservices example with service mesh. See [microservices.md](guides/advanced/microservices.md)

#### .dockerignore Examples
.dockerignore examples for different programming languages. See [dockerignore_examples.md](guides/advanced/dockerignore_examples.md)

#### Registry Setup
Private Docker registry and Harbor setup. See [registry_setup.md](guides/advanced/registry_setup.md)

#### Docker Swarm
Complete Docker Swarm orchestration guide with single-node and multi-node examples. See [docker_swarm.md](guides/advanced/docker_swarm.md)

##  Examples

### Multi-Stage Builds
Learn how to create optimized Docker images using multi-stage builds. See [dockerfile_multi_stage.md](examples/dockerfile_multi_stage.md)

### Networking
Examples of Docker networking configurations and patterns. See [docker_networking_examples.md](examples/docker_networking_examples.md)

### Volumes & Backup
Complete guide to Docker volumes, data persistence, and backup strategies. See [docker_volumes_backup.md](examples/docker_volumes_backup.md)

##  Scripts

### install.sh
Installs Docker Engine and Docker Compose on Debian/Ubuntu systems.

**Usage:**
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

**Note:** After installation, log out and log in again to apply docker group permissions.

### uninstall.sh
Completely removes Docker from the system.

**Usage:**
```bash
chmod +x scripts/uninstall.sh
./scripts/uninstall.sh
```

### docker_clean.sh
Cleans up unused Docker resources (containers, images, volumes, networks, and build cache).

**Usage:**
```bash
chmod +x scripts/docker_clean.sh
./scripts/docker_clean.sh
```

### docker_backup.sh
Backup Docker volumes to tar.gz files.

**Usage:**
```bash
chmod +x scripts/docker_backup.sh

# Backup volume
./scripts/docker_backup.sh <volume_name> [backup_directory]

# Example
./scripts/docker_backup.sh postgres_data ./backups
```

##  Common Docker Commands

### Container Management
```bash
# Run a container
docker run -d -p 8080:80 --name my-app nginx

# List containers
docker ps -a

# Stop container
docker stop my-app

# Remove container
docker rm my-app
```

### Image Management
```bash
# Build image
docker build -t my-image .

# List images
docker images

# Remove image
docker rmi my-image
```

### Docker Compose
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

##  License

This project is open source and available under the [MIT License](LICENSE).

##  Useful Links

- [Docker Official Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
