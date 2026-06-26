# Vibe Coding — One-Click Workbench Setup

Bootstraps the local stack used in Breakout 1:
**editor + Ollama (autostart) + a small coding model + opencode**, wired together.

## What it installs

| Component | macOS | Linux | Windows |
|---|---|---|---|
| Editor    | brew (micro / zed / vscode)           | apt/dnf/pacman / installer       | winget                  |
| Ollama    | Homebrew + `brew services` (autostart) | official installer + `systemctl --enable --now` | winget / installer (autostart via Run key) |
| Model     | `qwen2.5-coder:1.5b` (~1 GB)          | same                              | same                    |
| opencode  | official install script               | official install script           | winget                  |
| Config    | `~/.config/opencode/opencode.json` pointing at `http://localhost:11434/v1` |

All steps are **idempotent** — rerun safely.

## Usage

### macOS / Linux
```bash
bash bootstrap.sh
```

### Windows (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -File bootstrap.ps1
```

### Choose a different editor

Default is **`micro`** — a ~10 MB terminal editor with mouse support and zero
learning curve (Ctrl-S to save, Ctrl-Q to quit). It keeps the whole workbench
in one terminal window alongside opencode.

```bash
EDITOR=micro   bash bootstrap.sh   # default, lightweight, terminal
EDITOR=zed     bash bootstrap.sh   # native GUI, fast
EDITOR=vscode  bash bootstrap.sh   # if you want extensions / Copilot-style UI
EDITOR=none    bash bootstrap.sh   # bare terminal — opencode renders its own diffs
```

```powershell
$env:EDITOR="zed"; .\bootstrap.ps1
```

### Choose a different model

```bash
MODEL=qwen2.5-coder:7b   bash bootstrap.sh   # ~16 GB RAM
MODEL=llama3.2:3b        bash bootstrap.sh   # general-purpose fallback
```

## After it finishes

```bash
mkdir -p ~/projects/playground && cd ~/projects/playground
opencode
```

Smoke test prompt inside opencode:

> create a python script that prints the first ten Fibonacci numbers, then run it

If you see a diff and `0 1 1 2 3 5 8 13 21 34`, the workbench is live.

## Reading diffs and resolving merge conflicts

Inspecting what the agent changed is the line between vibe coding and
engineering. A self-contained walk-through that creates a synthetic conflict
and walks you through resolving it in micro:

```bash
bash diffs_and_merges.sh
```

See [diffs_and_merges.md](diffs_and_merges.md) for the prose explanation.

## Troubleshooting

- **`ollama` command not found after install (Windows):** open a fresh PowerShell window — the installer updates `PATH` for new shells only.
- **Port 11434 already in use:** another Ollama is running. `pkill ollama` (Unix) / Task Manager (Windows), then rerun.
- **Model download is slow:** the 1.5b model is ~1 GB; on a slow link, switch to `qwen2.5-coder:0.5b`.
- **Linux without systemd / snap:** the script falls back to `nohup ollama serve &`; add it to your shell rc for persistence.
- **Corporate proxy:** set `HTTPS_PROXY` before running. Ollama also reads `OLLAMA_HOST`.

## Uninstall

```bash
# macOS
brew services stop ollama && brew uninstall ollama
brew uninstall micro 2>/dev/null
rm -rf ~/.ollama ~/.config/opencode

# Linux
sudo systemctl disable --now ollama
sudo rm /etc/systemd/system/ollama.service /usr/local/bin/ollama
rm -rf ~/.ollama ~/.config/opencode
```
