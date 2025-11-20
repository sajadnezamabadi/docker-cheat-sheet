#!/usr/bin/env bash
set -e

# Docker Volume Backup Script
# Usage: ./docker_backup.sh [volume_name] [backup_directory]

VOLUME_NAME=${1:-""}
BACKUP_DIR=${2:-"./backups"}
DATE=$(date +%Y%m%d_%H%M%S)

if [ -z "$VOLUME_NAME" ]; then
    echo "=== Available Volumes ==="
    docker volume ls --format "table {{.Name}}\t{{.Driver}}\t{{.Mountpoint}}"
    echo ""
    echo "Usage: $0 <volume_name> [backup_directory]"
    echo "Example: $0 postgres_data ./backups"
    exit 1
fi

# Check if volume exists
if ! docker volume inspect "$VOLUME_NAME" > /dev/null 2>&1; then
    echo "Error: Volume '$VOLUME_NAME' does not exist."
    exit 1
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo "=== Docker Volume Backup ==="
echo "Volume: $VOLUME_NAME"
echo "Backup directory: $BACKUP_DIR"
echo "Date: $DATE"
echo ""

# Create backup
BACKUP_FILE="${BACKUP_DIR}/${VOLUME_NAME}_${DATE}.tar.gz"
echo "Creating backup: $BACKUP_FILE"

docker run --rm \
    -v "$VOLUME_NAME":/data:ro \
    -v "$(realpath $BACKUP_DIR)":/backup \
    alpine tar czf "/backup/$(basename $BACKUP_FILE)" /data

if [ $? -eq 0 ]; then
    echo " Backup completed successfully!"
    echo "Backup file: $BACKUP_FILE"
    
    # Show backup size
    if [ -f "$BACKUP_FILE" ]; then
        SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
        echo "Backup size: $SIZE"
    fi
else
    echo " Backup failed!"
    exit 1
fi

