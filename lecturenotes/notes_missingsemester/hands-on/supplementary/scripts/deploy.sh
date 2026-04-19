#!/bin/bash
# scripts/deploy.sh — Deploy the latest PixelWise code
#
# Called by GitHub Actions (deploy.yml) or run manually on the server.
# Pulls the latest code, installs dependencies, runs migrations,
# and restarts the service.
#
# Usage:
#     bash scripts/deploy.sh
#
# Prerequisites:
#   - /opt/pixelwise is a git clone of the repo
#   - .venv exists with Python dependencies
#   - pixelwise.service is installed in systemd
#   - PostgreSQL is running with the pixelwise database
# ----------------------------------------------------------------

set -euo pipefail

cd /opt/pixelwise

echo "=== PixelWise Deploy ==="
echo "Time: $(date)"
echo "Branch: $(git rev-parse --abbrev-ref HEAD)"

# Pull latest code
echo ""
echo "[1/4] Pulling latest changes..."
git pull origin main

# Install/update dependencies
echo ""
echo "[2/4] Installing dependencies..."
source .venv/bin/activate
pip install -r requirements.txt --quiet

# Run database migrations
echo ""
echo "[3/4] Running database migrations..."
alembic upgrade head

# Restart the service
echo ""
echo "[4/4] Restarting pixelwise service..."
sudo systemctl restart pixelwise

# Verify
echo ""
echo "=== Deploy Complete ==="
echo "Time:    $(date)"
echo "Commit:  $(git log --oneline -1)"
echo "Service: $(systemctl is-active pixelwise)"
