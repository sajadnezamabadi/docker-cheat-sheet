# Dockerfile Best Practices

## General Principles

### 1. Use Multi-stage Builds
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 2. Use Specific Tags
```dockerfile
# Bad
FROM node

# Good
FROM node:18-alpine
```

### 3. Minimize Layers
```dockerfile
# Bad
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y pip

# Good
RUN apt-get update && \
    apt-get install -y python3 pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 4. Order Instructions by Change Frequency
```dockerfile
# Dependencies change less frequently
COPY package*.json ./
RUN npm install

# Source code changes more frequently
COPY . .
RUN npm run build
```

### 5. Use .dockerignore
```
node_modules
npm-debug.log
.git
.gitignore
.env
*.md
.DS_Store
```

### 6. Don't Run as Root
```dockerfile
# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

### 7. Use Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1
```

### 8. Use Build Arguments
```dockerfile
ARG NODE_VERSION=18
FROM node:${NODE_VERSION}-alpine
```

### 9. Leverage Build Cache
```dockerfile
# Copy dependency files first
COPY requirements.txt .
RUN pip install -r requirements.txt

# Then copy source code
COPY . .
```

### 10. Use COPY Instead of ADD
```dockerfile
# Prefer COPY for local files
COPY . /app

# Use ADD only for URLs or tar extraction
ADD https://example.com/file.tar.gz /tmp/
```

## Language-Specific Examples

### Python
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["python", "app.py"]
```

### Node.js
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application
COPY . .

# Non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

EXPOSE 3000
CMD ["node", "server.js"]
```

### Go
```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/main .

# Final stage
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/main .
CMD ["./main"]
```

## Security Best Practices

1. **Scan images for vulnerabilities**
   ```bash
   docker scan <image>
   ```

2. **Don't store secrets in images**
   - Use environment variables
   - Use secrets management
   - Use build-time secrets carefully

3. **Keep base images updated**
   ```dockerfile
   FROM node:18-alpine  # Use latest patch version
   ```

4. **Minimize attack surface**
   - Use minimal base images (alpine, distroless)
   - Remove unnecessary packages
   - Don't install development tools in production

5. **Use specific versions**
   - Avoid `latest` tag in production
   - Pin dependency versions

## Performance Tips

1. **Use BuildKit**
   ```bash
   DOCKER_BUILDKIT=1 docker build .
   ```

2. **Parallel builds**
   ```dockerfile
   # BuildKit can build stages in parallel
   FROM base AS stage1
   FROM base AS stage2
   ```

3. **Cache mount**
   ```dockerfile
   RUN --mount=type=cache,target=/root/.npm \
       npm install
   ```

4. **Use .dockerignore effectively**
   - Exclude large files
   - Exclude build artifacts
   - Exclude version control files

