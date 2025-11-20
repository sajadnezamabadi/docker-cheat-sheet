#!/usr/bin/env bash
set -e

# Docker Exec Script
# Usage: ./docker_exec.sh [container_name] [command]

CONTAINER_NAME=${1:-""}
COMMAND=${2:-"/bin/bash"}

if [ -z "$CONTAINER_NAME" ]; then
    echo "=== Available Containers ==="
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
    echo ""
    echo "Usage: $0 <container_name> [command]"
    echo "Examples:"
    echo "  $0 my-container"
    echo "  $0 my-container /bin/sh"
    echo "  $0 my-container python manage.py shell"
    exit 1
fi

# Check if container is running
if ! docker ps --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
    echo "Error: Container '$CONTAINER_NAME' is not running."
    echo "Available running containers:"
    docker ps --format "  - {{.Names}}"
    exit 1
fi

echo "=== Executing into container: $CONTAINER_NAME ==="
echo "Command: $COMMAND"
echo ""

docker exec -it "$CONTAINER_NAME" $COMMAND

