#!/bin/sh
set -e

REGISTRY_URL=${1:-"localhost:5000"}
IMAGE_NAME=${2:-"alpine:latest"}

echo "=== Testing Docker Registry ==="
echo "Registry: $REGISTRY_URL"
echo "Image: $IMAGE_NAME"
echo ""

# Pull test image
echo "[1] Pulling test image..."
docker pull $IMAGE_NAME

# Tag image for registry
echo "[2] Tagging image for registry..."
docker tag $IMAGE_NAME $REGISTRY_URL/test-image:latest

# Login to registry (if authentication enabled)
echo "[3] Logging in to registry..."
if docker login $REGISTRY_URL -u admin -p admin123 2>/dev/null; then
    echo "Login successful"
else
    echo "Login skipped (no authentication or already logged in)"
fi

# Push image
echo "[4] Pushing image to registry..."
docker push $REGISTRY_URL/test-image:latest

# List images in registry
echo "[5] Listing images in registry..."
curl -s http://$REGISTRY_URL/v2/_catalog | python3 -m json.tool || curl -s http://$REGISTRY_URL/v2/_catalog

# List tags
echo "[6] Listing tags for test-image..."
curl -s http://$REGISTRY_URL/v2/test-image/tags/list | python3 -m json.tool || curl -s http://$REGISTRY_URL/v2/test-image/tags/list

# Pull image back
echo "[7] Pulling image back from registry..."
docker pull $REGISTRY_URL/test-image:latest

echo ""
echo "=== Test Complete ==="
echo "Registry is working correctly!"

