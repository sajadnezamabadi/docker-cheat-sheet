#!/usr/bin/env bash
set -e

# Docker Logs Viewer Script
# Usage: ./docker_logs.sh [container_name] [options]

CONTAINER_NAME=${1:-""}
FOLLOW=${2:-""}

if [ -z "$CONTAINER_NAME" ]; then
    echo "=== Available Containers ==="
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    echo "Usage: $0 <container_name> [--follow]"
    echo "Example: $0 my-container --follow"
    exit 1
fi

if [ "$FOLLOW" == "--follow" ] || [ "$FOLLOW" == "-f" ]; then
    echo "=== Following logs for: $CONTAINER_NAME ==="
    echo "Press Ctrl+C to stop"
    docker logs -f "$CONTAINER_NAME"
else
    echo "=== Logs for: $CONTAINER_NAME ==="
    docker logs --tail 100 "$CONTAINER_NAME"
    echo ""
    echo "To follow logs in real-time, use: $0 $CONTAINER_NAME --follow"
fi

