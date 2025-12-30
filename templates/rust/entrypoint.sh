#!/bin/sh
set -e

echo "Waiting for PostgreSQL to be ready..."

# Wait for PostgreSQL
until PGPASSWORD="${POSTGRES_PASSWORD:-rust}" psql -h "${POSTGRES_HOST:-db}" -U "${POSTGRES_USER:-rust}" -d "${POSTGRES_DB:-rustdb}" -c '\q' 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is ready!"

# Run the application
exec "$@"

