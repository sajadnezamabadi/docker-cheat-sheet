#!/usr/bin/env bash
set -e

echo "=== Docker Cleanup Script ==="

echo "[1] Stopping all running containers..."
docker stop $(docker ps -aq) 2>/dev/null || echo "No containers to stop"

echo "[2] Removing all stopped containers..."
docker rm $(docker ps -aq) 2>/dev/null || echo "No containers to remove"

echo "[3] Removing all unused images..."
docker image prune -a -f

echo "[4] Removing all unused volumes..."
docker volume prune -f

echo "[5] Removing all unused networks..."
docker network prune -f

echo "[6] Removing all build cache..."
docker builder prune -a -f

echo "[7] System-wide cleanup..."
docker system prune -a -f --volumes

echo "=== Docker cleanup completed successfully ==="
echo "Disk space freed!"

