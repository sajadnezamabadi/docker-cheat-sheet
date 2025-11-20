#!/bin/sh
set -e

echo "=== Docker Registry Setup ==="

# Create directories
mkdir -p auth certs

# Check if htpasswd is installed
if ! command -v htpasswd > /dev/null 2>&1; then
    echo "Installing apache2-utils..."
    sudo apt-get update
    sudo apt-get install -y apache2-utils
fi

# Create default user
if [ ! -f auth/htpasswd ]; then
    echo "Creating default user..."
    echo "Default credentials:"
    echo "  Username: admin"
    echo "  Password: admin123"
    echo ""
    htpasswd -Bbn admin admin123 > auth/htpasswd
    echo "User created in auth/htpasswd"
else
    echo "htpasswd file already exists"
fi

# Generate self-signed certificate (optional)
if command -v openssl > /dev/null 2>&1; then
    if [ ! -f certs/domain.crt ] || [ ! -f certs/domain.key ]; then
        echo ""
        echo "Generating self-signed certificate (optional)..."
        openssl req -newkey rsa:4096 -nodes -sha256 \
            -keyout certs/domain.key \
            -x509 -days 365 \
            -out certs/domain.crt \
            -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
        echo "Certificate created in certs/"
        echo ""
        echo "Note: For production, use proper certificates from CA"
        echo "Note: TLS is optional - registry works without it"
    else
        echo "Certificate files already exist"
    fi
else
    echo ""
    echo "OpenSSL not found - skipping certificate generation"
    echo "Registry will work without TLS (HTTP only)"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To start registry:"
echo "  docker-compose up -d"
echo ""
echo "To use without authentication (simple mode):"
echo "  docker-compose -f docker-compose.simple.yml up -d"

