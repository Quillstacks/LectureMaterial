#!/bin/bash
# scripts/health_check.sh — Check PixelWise health and alert via Discord
#
# Runs as a cron job every 5 minutes. Hits the /health endpoint and
# sends a Discord webhook notification if the service is down.
#
# Setup:
#     1. Set DISCORD_WEBHOOK_URL in /opt/pixelwise/.env
#     2. Add to crontab: */5 * * * * /opt/pixelwise/scripts/health_check.sh
#
# Usage:
#     bash scripts/health_check.sh
# ----------------------------------------------------------------

set -euo pipefail

# Load environment variables
if [ -f /opt/pixelwise/.env ]; then
    export $(grep -v '^#' /opt/pixelwise/.env | xargs)
fi

HEALTH_URL="https://192.168.56.11/health"
WEBHOOK_URL="${DISCORD_WEBHOOK_URL:-}"

# Skip if no webhook configured
if [ -z "$WEBHOOK_URL" ]; then
    echo "DISCORD_WEBHOOK_URL not set, skipping alert"
    exit 0
fi

# Check health endpoint (-k for self-signed cert, 5s timeout)
HTTP_CODE=$(curl -sk -o /dev/null -w "%{http_code}" --max-time 5 "$HEALTH_URL" 2>/dev/null || echo "000")

if [ "$HTTP_CODE" = "200" ]; then
    echo "OK: /health returned 200"
    exit 0
fi

# Service is down — send Discord alert
HOSTNAME=$(hostname)
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

curl -s -H "Content-Type: application/json" \
    -X POST "$WEBHOOK_URL" \
    -d "{
        \"content\": \"**PixelWise Alert** :warning:\",
        \"embeds\": [{
            \"title\": \"Health Check Failed\",
            \"description\": \"/health returned HTTP $HTTP_CODE\",
            \"color\": 15158332,
            \"fields\": [
                {\"name\": \"Host\", \"value\": \"$HOSTNAME\", \"inline\": true},
                {\"name\": \"URL\", \"value\": \"$HEALTH_URL\", \"inline\": true},
                {\"name\": \"Time\", \"value\": \"$TIMESTAMP\", \"inline\": true}
            ]
        }]
    }"

echo "ALERT: /health returned $HTTP_CODE — Discord notification sent"
exit 1
