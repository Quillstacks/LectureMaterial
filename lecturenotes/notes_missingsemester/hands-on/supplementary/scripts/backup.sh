#!/bin/bash
# scripts/backup.sh — Nightly database backup to dev VM
#
# Dumps the PostgreSQL database and rsyncs it to the dev VM.
# Run as a nightly cron job on the server VM.
#
# Setup:
#     crontab -e
#     0 2 * * * /opt/pixelwise/scripts/backup.sh
#
# Prerequisites:
#   - SSH key auth from server → dev VM (passwordless)
#   - /backups/pixelwise/ directory exists on dev VM
#   - pixelwise PostgreSQL user has read access
# ----------------------------------------------------------------

set -euo pipefail

# Configuration
DB_NAME="pixelwise"
DB_USER="pixelwise"
BACKUP_DIR="/tmp/pixelwise-backups"
REMOTE_USER="student"
REMOTE_HOST="192.168.56.10"
REMOTE_DIR="/backups/pixelwise"
KEEP_LOCAL_DAYS=3

DATE=$(date +%Y%m%d_%H%M%S)
DUMP_FILE="${BACKUP_DIR}/${DB_NAME}_${DATE}.sql"

echo "=== PixelWise Backup ==="
echo "Time: $(date)"

# Create local backup directory
mkdir -p "$BACKUP_DIR"

# Dump the database
echo "[1/3] Dumping database..."
pg_dump -U "$DB_USER" "$DB_NAME" > "$DUMP_FILE"
echo "      Dump: $DUMP_FILE ($(du -h "$DUMP_FILE" | cut -f1))"

# Transfer to dev VM
echo "[2/3] Syncing to dev VM..."
rsync -az "$DUMP_FILE" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/"
echo "      Synced to ${REMOTE_HOST}:${REMOTE_DIR}/"

# Clean up old local backups
echo "[3/3] Cleaning local backups older than ${KEEP_LOCAL_DAYS} days..."
find "$BACKUP_DIR" -name "*.sql" -mtime "+${KEEP_LOCAL_DAYS}" -delete

echo ""
echo "=== Backup Complete ==="
echo "Time: $(date)"
