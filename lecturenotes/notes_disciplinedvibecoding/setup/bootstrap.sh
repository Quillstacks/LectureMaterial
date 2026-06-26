#!/usr/bin/env bash
# Disciplined Vibe Coding — one-shot workbench bootstrap (macOS + Linux).
# Installs: an editor, Ollama (+ autostart), a small coding model, opencode,
# and writes ~/.config/opencode/opencode.json wired to the local Ollama.
#
# Usage:   bash bootstrap.sh
# Re-run:  safe; every step is idempotent.
#
# Knobs (env vars):
#   MODEL=qwen2.5-coder:1.5b   # any tag from https://ollama.com/library
#   EDITOR=micro               # micro (default) | zed | vscode | none

set -euo pipefail

MODEL="${MODEL:-qwen2.5-coder:1.5b}"
EDITOR_CHOICE="${EDITOR:-micro}"
OS="$(uname -s)"

log()  { printf '\033[1;34m[setup]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[warn ]\033[0m %s\n' "$*"; }
die()  { printf '\033[1;31m[fail ]\033[0m %s\n' "$*" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

############################################
# 0. Package manager (macOS only)
############################################
ensure_brew() {
  if ! have brew; then
    log "Installing Homebrew"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv)"
  fi
}

############################################
# 1. Editor
############################################
install_editor_macos() {
  case "$EDITOR_CHOICE" in
    none)   log "Skipping editor install (EDITOR=none)" ;;
    micro)
      have micro && { log "micro already installed"; return; }
      log "Installing micro (terminal editor, ~10 MB)"
      brew install micro ;;
    zed)
      have zed && { log "Zed already installed"; return; }
      log "Installing Zed"
      brew install --cask zed ;;
    vscode)
      have code && { log "VS Code already installed"; return; }
      log "Installing VS Code"
      brew install --cask visual-studio-code ;;
    *) die "Unknown EDITOR=$EDITOR_CHOICE (use: micro|zed|vscode|none)" ;;
  esac
}

install_editor_linux() {
  case "$EDITOR_CHOICE" in
    none) log "Skipping editor install (EDITOR=none)" ;;
    micro)
      have micro && { log "micro already installed"; return; }
      log "Installing micro"
      if have apt-get; then sudo apt-get update && sudo apt-get install -y micro
      elif have dnf;     then sudo dnf install -y micro
      elif have pacman;  then sudo pacman -S --noconfirm micro
      else
        log "Falling back to upstream install script"
        curl -fsSL https://getmic.ro | sudo sh -s -- -d /usr/local/bin
      fi ;;
    zed)
      have zed && { log "Zed already installed"; return; }
      log "Installing Zed"
      curl -f https://zed.dev/install.sh | sh ;;
    vscode)
      have code && { log "VS Code already installed"; return; }
      log "Installing VS Code"
      if have snap; then
        sudo snap install code --classic
      elif have apt-get; then
        sudo apt-get update
        sudo apt-get install -y wget gpg
        wget -qO- https://packages.microsoft.com/keys/microsoft.asc \
          | gpg --dearmor | sudo tee /usr/share/keyrings/packages.microsoft.gpg >/dev/null
        echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/packages.microsoft.gpg] \
https://packages.microsoft.com/repos/code stable main" \
          | sudo tee /etc/apt/sources.list.d/vscode.list >/dev/null
        sudo apt-get update && sudo apt-get install -y code
      else
        warn "No snap/apt found — install VS Code manually from https://code.visualstudio.com/"
      fi ;;
    *) die "Unknown EDITOR=$EDITOR_CHOICE (use: micro|zed|vscode|none)" ;;
  esac
}

############################################
# 2. Ollama install + autostart
############################################
install_ollama_macos() {
  if have ollama; then log "Ollama already installed"; else
    log "Installing Ollama"; brew install ollama
  fi
  if brew services list | grep -q '^ollama .* started'; then
    log "Ollama service already running"
  else
    log "Enabling Ollama autostart (brew services)"
    brew services start ollama
  fi
}

install_ollama_linux() {
  if have ollama; then
    log "Ollama already installed"
  else
    log "Installing Ollama"
    curl -fsSL https://ollama.com/install.sh | sh
  fi
  if systemctl list-unit-files 2>/dev/null | grep -q '^ollama\.service'; then
    log "Enabling Ollama systemd service"
    sudo systemctl enable --now ollama
  else
    warn "No systemd unit found — starting ollama in background"
    pgrep -x ollama >/dev/null || nohup ollama serve >/tmp/ollama.log 2>&1 &
  fi
}

wait_for_ollama() {
  log "Waiting for Ollama API on :11434"
  for _ in $(seq 1 30); do
    curl -fsS http://localhost:11434/api/tags >/dev/null 2>&1 && return 0
    sleep 1
  done
  die "Ollama did not respond on :11434"
}

############################################
# 3. Pull model
############################################
pull_model() {
  if ollama list 2>/dev/null | awk '{print $1}' | grep -qx "$MODEL"; then
    log "Model $MODEL already present"
  else
    log "Pulling model $MODEL (one-time download)"
    ollama pull "$MODEL"
  fi
}

############################################
# 4. opencode + config
############################################
install_opencode() {
  if have opencode; then log "opencode already installed"; else
    log "Installing opencode"
    curl -fsSL https://opencode.ai/install | bash
  fi
}

write_opencode_config() {
  local cfg_dir="$HOME/.config/opencode"
  local cfg="$cfg_dir/opencode.json"
  mkdir -p "$cfg_dir"
  if [[ -f "$cfg" ]]; then
    log "opencode config exists at $cfg (leaving as-is)"
    return
  fi
  log "Writing opencode config to $cfg"
  cat >"$cfg" <<EOF
{
  "\$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": { "baseURL": "http://localhost:11434/v1" },
      "models": {
        "$MODEL": { "name": "$MODEL" }
      }
    }
  }
}
EOF
}

############################################
# Main
############################################
case "$OS" in
  Darwin) ensure_brew; install_editor_macos; install_ollama_macos ;;
  Linux)  install_editor_linux; install_ollama_linux ;;
  *) die "Unsupported OS: $OS (use bootstrap.ps1 on Windows)" ;;
esac

wait_for_ollama
pull_model
install_opencode
write_opencode_config

cat <<EOF

\033[1;32m[ok]\033[0m Workbench ready.

  Editor:  $EDITOR_CHOICE
  Model:   $MODEL  (override with MODEL=... next time)
  Ollama:  http://localhost:11434  (autostarts on login)
  Config:  ~/.config/opencode/opencode.json

Try it:
  mkdir -p ~/projects/playground && cd ~/projects/playground
  opencode

Smoke test inside opencode:
  > create a python script that prints the first ten Fibonacci numbers, then run it

Diffs & merge conflicts walk-through:
  bash $(dirname "$0")/diffs_and_merges.sh

EOF
