#!/usr/bin/env bash
set -e

echo "=== Docker Install Script ==="

echo "[1] Updating system packages..."
sudo apt update
sudo apt upgrade -y

echo "[2] Installing prerequisites..."
sudo apt install -y ca-certificates curl gnupg lsb-release

echo "[3] Adding Docker GPG key..."
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg \
    | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "[4] Adding Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "[5] Installing Docker Engine..."
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "[6] Installing standalone docker-compose binary..."
sudo curl -L \
  "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "[7] Adding current user to docker group..."
sudo usermod -aG docker "$USER"

echo "[8] Enabling Docker service..."
sudo systemctl enable docker
sudo systemctl start docker

echo "[9] Verifying installation..."
docker --version
docker-compose --version

echo "[10] Running hello-world test..."
docker run --rm hello-world || true

echo "=== Docker installation completed successfully ==="

# Usage:
# chmod +x install.sh
# ./install.sh
# 
# Note: After running this script, log out and log in again to apply docker group permissions.

