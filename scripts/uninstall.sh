#!/usr/bin/env bash
set -e

echo "=== Docker Uninstall Script ==="

echo "[1] Stopping Docker services..."
sudo systemctl stop docker
sudo systemctl stop docker.socket
sudo systemctl stop docker.service

echo "[2] Removing Docker packages..."
sudo apt remove -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "[3] Removing Docker configuration..."
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd

echo "[4] Removing Docker group membership..."
sudo groupdel docker

echo "[5] Removing Docker from system..."
sudo apt purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "=== Docker uninstallation completed successfully ==="

