#!/bin/bash
# setup-server.sh — Provision a fresh server VM for PixelWise
#
# Run on the server VM (192.168.56.11) as the student user.
# This script installs everything needed through Block 2.
# Later blocks add more packages (PostgreSQL, Nginx, etc.) on top.
#
# Usage:
#     bash setup-server.sh
#
# What it does:
#   1. Updates package lists
#   2. Installs git, python3, pip, venv, curl
#   3. Configures git user identity (edit the variables below)
#   4. Verifies the installation
#
# This is the first file students commit to their repo (Block 2).
# ----------------------------------------------------------------

set -euo pipefail

# ---- Configuration (students edit these) ----
GIT_USER_NAME="${GIT_USER_NAME:-Student Name}"
GIT_USER_EMAIL="${GIT_USER_EMAIL:-student@example.com}"

echo "=============================================="
echo "  PixelWise Server Setup"
echo "=============================================="

# ---- 1. System packages ----
echo ""
echo "[1/4] Updating package lists..."
sudo apt update

echo ""
echo "[2/4] Installing required packages..."
sudo apt install -y \
    git \
    python3 \
    python3-pip \
    python3-venv \
    curl

# ---- 2. Git configuration ----
echo ""
echo "[3/4] Configuring git..."
git config --global user.name "$GIT_USER_NAME"
git config --global user.email "$GIT_USER_EMAIL"
git config --global init.defaultBranch main

# ---- 3. Verify ----
echo ""
echo "[4/4] Verifying installation..."
echo "  git:     $(git --version)"
echo "  python3: $(python3 --version)"
echo "  pip:     $(pip3 --version)"
echo "  curl:    $(curl --version | head -1)"

echo ""
echo "=============================================="
echo "  Setup complete!"
echo ""
echo "  Next steps:"
echo "    1. Edit GIT_USER_NAME and GIT_USER_EMAIL above"
echo "       (or re-run: GIT_USER_NAME='Your Name' bash setup-server.sh)"
echo "    2. Create the project directory:"
echo "       sudo mkdir -p /opt/pixelwise"
echo "       sudo chown student:student /opt/pixelwise"
echo "    3. Initialize git repo and push to GitHub"
echo "=============================================="
