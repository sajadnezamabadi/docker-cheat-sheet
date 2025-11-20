# Docker Volumes & Backup Examples

Complete guide to Docker volumes, data persistence, and backup strategies.

## Volume Types

### 1. Named Volumes (Recommended)

```bash
# Create named volume
docker volume create mydata

# Use in container
docker run -v mydata:/app/data nginx

# List volumes
docker volume ls

# Inspect volume
docker volume inspect mydata
```

### 2. Bind Mounts

```bash
# Mount host directory
docker run -v /host/path:/container/path nginx

# Use absolute paths
docker run -v $(pwd)/data:/app/data nginx
```

### 3. Anonymous Volumes

```bash
# Created automatically
docker run -v /app/data nginx
```

## Backup Strategies

### Backup Named Volume

```bash
# Backup PostgreSQL volume
docker run --rm \
  -v postgres_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/postgres_backup_$(date +%Y%m%d).tar.gz /data

# Backup MySQL volume
docker run --rm \
  -v mysql_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/mysql_backup_$(date +%Y%m%d).tar.gz /data
```

### Restore Named Volume

```bash
# Restore PostgreSQL volume
docker run --rm \
  -v postgres_data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/postgres_backup_20241121.tar.gz"

# Restore MySQL volume
docker run --rm \
  -v mysql_data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/mysql_backup_20241121.tar.gz"
```

## Database-Specific Backups

### PostgreSQL Backup

```bash
# Backup database
docker exec postgres pg_dump -U postgres mydb > backup.sql

# Backup with timestamp
docker exec postgres pg_dump -U postgres mydb | gzip > backup_$(date +%Y%m%d).sql.gz

# Restore database
docker exec -i postgres psql -U postgres mydb < backup.sql

# Restore from gzip
gunzip < backup_20241121.sql.gz | docker exec -i postgres psql -U postgres mydb
```

### MySQL Backup

```bash
# Backup database
docker exec mysql mysqldump -u root -p mydb > backup.sql

# Backup all databases
docker exec mysql mysqldump -u root -p --all-databases > all_backup.sql

# Restore database
docker exec -i mysql mysql -u root -p mydb < backup.sql
```

### MongoDB Backup

```bash
# Backup database
docker exec mongo mongodump --out /backup

# Backup specific database
docker exec mongo mongodump --db mydb --out /backup

# Restore database
docker exec mongo mongorestore /backup
```

## Automated Backup Script

```bash
#!/bin/bash
# backup-volumes.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# List of volumes to backup
VOLUMES=("postgres_data" "mysql_data" "redis_data")

for volume in "${VOLUMES[@]}"; do
    echo "Backing up volume: $volume"
    docker run --rm \
        -v $volume:/data \
        -v $BACKUP_DIR:/backup \
        alpine tar czf /backup/${volume}_${DATE}.tar.gz /data
    echo "Backup completed: ${volume}_${DATE}.tar.gz"
done

# Cleanup old backups (keep last 7 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

## Docker Compose Backup

### docker-compose.backup.yml

```yaml
services:
  backup:
    image: alpine:latest
    volumes:
      - postgres_data:/data:ro
      - ./backups:/backup
    command: >
      sh -c "
        tar czf /backup/postgres_$(date +%Y%m%d).tar.gz /data &&
        echo 'Backup completed'
      "

volumes:
  postgres_data:
    external: true
```

```bash
# Run backup
docker-compose -f docker-compose.backup.yml run --rm backup
```

## Volume Migration

### Export Volume

```bash
# Export volume to tar
docker run --rm \
  -v mydata:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/mydata.tar.gz /data
```

### Import Volume

```bash
# Create new volume
docker volume create newdata

# Import data
docker run --rm \
  -v newdata:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/mydata.tar.gz"
```

## Best Practices

1. **Use Named Volumes**: Better portability and management
2. **Regular Backups**: Automate backup process
3. **Test Restores**: Regularly test backup restoration
4. **Offsite Storage**: Store backups in different location
5. **Encryption**: Encrypt sensitive backups
6. **Retention Policy**: Keep backups for appropriate duration
7. **Monitor Backups**: Set up alerts for backup failures

## Backup to Cloud

### AWS S3 Example

```bash
#!/bin/bash
# backup-to-s3.sh

VOLUME="postgres_data"
S3_BUCKET="my-backups"
DATE=$(date +%Y%m%d)

# Create backup
docker run --rm \
  -v $VOLUME:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz /data

# Upload to S3
aws s3 cp backup.tar.gz s3://$S3_BUCKET/postgres_${DATE}.tar.gz

# Cleanup
rm backup.tar.gz
```

### Google Cloud Storage Example

```bash
# Upload to GCS
gsutil cp backup.tar.gz gs://my-backups/postgres_${DATE}.tar.gz
```

## Monitoring Volume Usage

```bash
# Check volume size
docker system df -v

# Check specific volume
docker volume inspect mydata | grep Mountpoint
sudo du -sh $(docker volume inspect mydata | grep Mountpoint | cut -d'"' -f4)
```

