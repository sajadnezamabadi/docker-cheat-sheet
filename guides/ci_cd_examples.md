# CI/CD with Docker Examples

Complete CI/CD pipeline examples using Docker for DevOps engineers.

## GitHub Actions

### Basic Build and Push

```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Multi-Stage Build with Tests

```yaml
# .github/workflows/test-and-build.yml
name: Test and Build

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Run tests
        run: |
          docker build --target test -t app:test .
          docker run --rm app:test npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: myapp:latest
```

## GitLab CI

### Complete Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"

services:
  - docker:24-dind

before_script:
  - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest
  only:
    - main
    - develop

test:
  stage: test
  script:
    - docker build --target test -t app:test .
    - docker run --rm app:test npm test
  only:
    - merge_requests

deploy:
  stage: deploy
  script:
    - docker-compose -f docker-compose.prod.yml pull
    - docker-compose -f docker-compose.prod.yml up -d
  environment:
    name: production
    url: https://myapp.com
  only:
    - main
  when: manual
```

## Jenkins Pipeline

### Jenkinsfile

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'registry.example.com'
        IMAGE_NAME = 'myapp'
    }
    
    stages {
        stage('Build') {
            steps {
                script {
                    def image = docker.build("${IMAGE_NAME}:${env.BUILD_NUMBER}")
                    image.push()
                    image.push("latest")
                }
            }
        }
        
        stage('Test') {
            steps {
                sh 'docker run --rm ${IMAGE_NAME}:${env.BUILD_NUMBER} npm test'
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    docker-compose -f docker-compose.prod.yml pull
                    docker-compose -f docker-compose.prod.yml up -d
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
```

## Docker Compose for CI/CD

### docker-compose.ci.yml

```yaml
version: '3.8'

services:
  test:
    build:
      context: .
      target: test
    volumes:
      - ./coverage:/app/coverage
    command: npm test

  lint:
    build:
      context: .
      target: build
    command: npm run lint

  build:
    build:
      context: .
      target: production
    image: myapp:${CI_COMMIT_SHA}
```

## Multi-Architecture Builds

### Build for Multiple Platforms

```yaml
# .github/workflows/multi-arch.yml
name: Multi-Arch Build

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build for multiple platforms
        uses: docker/build-push-action@v5
        with:
          platforms: linux/amd64,linux/arm64
          push: true
          tags: myapp:latest
```

## Security Scanning

### Scan in CI/CD

```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:latest'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

## Best Practices

1. **Use Build Cache**: Leverage Docker layer caching
2. **Multi-stage Builds**: Separate build and runtime
3. **Tag Properly**: Use semantic versioning
4. **Scan Images**: Always scan for vulnerabilities
5. **Test Before Deploy**: Run tests in CI
6. **Use Secrets**: Never hardcode credentials
7. **Parallel Jobs**: Run tests in parallel when possible
8. **Clean Up**: Remove old images and containers

