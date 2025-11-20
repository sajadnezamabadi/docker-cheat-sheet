# .dockerignore Examples

Complete .dockerignore examples for different programming languages and frameworks.

## Python

```dockerignore
# Python .dockerignore

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
env/
venv/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# Jupyter Notebook
.ipynb_checkpoints

# Environment variables
.env
.env.local
.env.*.local

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
*.sqlite
*.sqlite3
db.sqlite3
```

## Node.js

```dockerignore
# Node.js .dockerignore

# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*
.pnpm-debug.log*

# Testing
coverage/
.nyc_output/

# Production
build/
dist/

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log

# Runtime data
pids/
*.pid
*.seed
*.pid.lock

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity
```

## Java

```dockerignore
# Java .dockerignore

# Compiled class file
*.class

# Log file
*.log

# BlueJ files
*.ctxt

# Mobile Tools for Java (J2ME)
.mtj.tmp/

# Package Files
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar

# Virtual machine crash logs
hs_err_pid*

# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar

# Gradle
.gradle/
build/
!gradle/wrapper/gradle-wrapper.jar
!**/src/main/**/build/
!**/src/test/**/build/

# IDE
.idea/
*.iws
*.iml
*.ipr
.vscode/
.classpath
.project
.settings/
bin/
tmp/
*.tmp
*.bak
*.swp
*~.nib
local.properties
.loadpath
.recommenders

# Eclipse
.externalToolBuilders/
.project
.classpath
.settings/
.loadpath
.buildpath
.target
.factorypath

# NetBeans
/nbproject/private/
/nbbuild/
/dist/
/nbdist/
/.nb-gradle/

# VS Code
.vscode/

# Environment
.env
```

## Go

```dockerignore
# Go .dockerignore

# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary, built with `go test -c`
*.test

# Output of the go coverage tool
*.out

# Dependency directories
vendor/

# Go workspace file
go.work

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env

# Build artifacts
/bin/
/dist/

# OS
.DS_Store
Thumbs.db
```

## Rust

```dockerignore
# Rust .dockerignore

# Compiled files
target/
Cargo.lock

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env

# OS
.DS_Store
Thumbs.db

# Documentation
/target/doc/
```

## PHP

```dockerignore
# PHP .dockerignore

# Composer
/vendor/
composer.lock
composer.phar

# IDE
.vscode/
.idea/
*.swp
*.swo
*.sublime-project
*.sublime-workspace

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
logs/

# Cache
cache/
tmp/
*.cache

# OS
.DS_Store
Thumbs.db

# Testing
.phpunit.result.cache
```

## Ruby

```dockerignore
# Ruby .dockerignore

# Dependencies
/vendor/bundle
.bundle

# Logs
*.log
log/
tmp/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
coverage/
.rakeTasks
```

## General Purpose

```dockerignore
# General .dockerignore

# Version control
.git/
.gitignore
.gitattributes

# CI/CD
.github/
.gitlab-ci.yml
.travis.yml
Jenkinsfile

# Documentation
README.md
LICENSE
CHANGELOG.md
docs/
*.md

# Testing
test/
tests/
spec/
__tests__/
*.test.js
*.spec.js

# Coverage
coverage/
.nyc_output/
.coverage/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.env.*
!.env.example

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp
*.temp
*.bak
*.backup

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
Desktop.ini

# Docker
Dockerfile*
docker-compose*.yml
.dockerignore

# Build artifacts
build/
dist/
out/
target/
bin/
obj/
```

## Best Practices

1. **Exclude Dependencies**: Don't copy node_modules, vendor, etc.
2. **Exclude Build Artifacts**: Don't copy build/, dist/, target/
3. **Exclude Version Control**: Don't copy .git/
4. **Exclude IDE Files**: Don't copy .vscode/, .idea/
5. **Exclude Environment Files**: Don't copy .env (but keep .env.example)
6. **Exclude Documentation**: Don't copy README.md, docs/ (optional)
7. **Exclude Test Files**: Don't copy test/, spec/ (optional)
8. **Exclude Logs**: Don't copy *.log, logs/
9. **Use Patterns**: Use wildcards (*) for flexibility
10. **Test Your .dockerignore**: Verify what gets copied

## Testing .dockerignore

```bash
# See what would be sent to Docker daemon
docker build --no-cache -t test-image . 2>&1 | grep "Sending build context"

# Or use buildkit
DOCKER_BUILDKIT=1 docker build . 2>&1 | grep "transferring context"
```

