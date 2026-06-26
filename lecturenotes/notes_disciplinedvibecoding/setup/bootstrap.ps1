# Disciplined Vibe Coding — one-shot workbench bootstrap (Windows / PowerShell).
# Installs: an editor, Ollama (autostart via its installer), a small coding model,
# opencode, and writes %USERPROFILE%\.config\opencode\opencode.json.
#
# Usage:   powershell -ExecutionPolicy Bypass -File bootstrap.ps1
# Re-run:  safe; every step is idempotent.
#
# Knobs (env vars):
#   $env:MODEL  = "qwen2.5-coder:1.5b"
#   $env:EDITOR = "micro"   # micro (default) | zed | vscode | none

$ErrorActionPreference = "Stop"
if (-not $env:MODEL)  { $env:MODEL  = "qwen2.5-coder:1.5b" }
if (-not $env:EDITOR) { $env:EDITOR = "micro" }
$Model  = $env:MODEL
$Editor = $env:EDITOR

function Log  ($m) { Write-Host "[setup] $m" -ForegroundColor Cyan }
function Warn ($m) { Write-Host "[warn ] $m" -ForegroundColor Yellow }
function Have ($c) { [bool](Get-Command $c -ErrorAction SilentlyContinue) }

#############################################
# 1. Editor
#############################################
switch ($Editor) {
  "none"   { Log "Skipping editor install (EDITOR=none)" }
  "micro"  {
    if (Have micro) { Log "micro already installed" }
    elseif (Have winget) {
      Log "Installing micro via winget"
      winget install -e --id zyedidia.micro --accept-source-agreements --accept-package-agreements
    } elseif (Have scoop) {
      Log "Installing micro via scoop"
      scoop install micro
    } else {
      Warn "Neither winget nor scoop found — install micro manually from https://micro-editor.github.io/"
    }
  }
  "zed" {
    if (Have zed) { Log "Zed already installed" }
    elseif (Have winget) {
      Log "Installing Zed via winget"
      winget install -e --id Zed.Zed --accept-source-agreements --accept-package-agreements
    } else { Warn "winget not found — install Zed manually from https://zed.dev/" }
  }
  "vscode" {
    if (Have code) { Log "VS Code already installed" }
    elseif (Have winget) {
      Log "Installing VS Code via winget"
      winget install -e --id Microsoft.VisualStudioCode --accept-source-agreements --accept-package-agreements
    } else { Warn "winget not found — install VS Code manually from https://code.visualstudio.com/" }
  }
  default { throw "Unknown EDITOR=$Editor (use: micro|zed|vscode|none)" }
}

#############################################
# 2. Ollama (installer registers autostart)
#############################################
if (Have ollama) {
  Log "Ollama already installed"
} elseif (Have winget) {
  Log "Installing Ollama via winget"
  winget install -e --id Ollama.Ollama --accept-source-agreements --accept-package-agreements
} else {
  Log "Downloading Ollama installer"
  $exe = "$env:TEMP\OllamaSetup.exe"
  Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile $exe
  Start-Process -FilePath $exe -ArgumentList "/SILENT" -Wait
}

# Refresh PATH for current session.
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
            [System.Environment]::GetEnvironmentVariable("Path","User")

if (-not (Get-Process ollama -ErrorAction SilentlyContinue)) {
  Log "Starting Ollama"
  Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
}

Log "Waiting for Ollama API on :11434"
$ready = $false
for ($i = 0; $i -lt 30; $i++) {
  try {
    Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:11434/api/tags" -TimeoutSec 2 | Out-Null
    $ready = $true; break
  } catch { Start-Sleep -Seconds 1 }
}
if (-not $ready) { throw "Ollama did not respond on :11434" }

#############################################
# 3. Pull model
#############################################
$installed = (& ollama list) -split "`n" | ForEach-Object { ($_ -split "\s+")[0] }
if ($installed -contains $Model) {
  Log "Model $Model already present"
} else {
  Log "Pulling model $Model (one-time download)"
  & ollama pull $Model
}

#############################################
# 4. opencode + config
#############################################
if (Have opencode) {
  Log "opencode already installed"
} elseif (Have winget) {
  Log "Installing opencode via winget"
  winget install -e --id sst.opencode --accept-source-agreements --accept-package-agreements
} else {
  Warn "winget not found — install opencode manually from https://opencode.ai/"
}

$cfgDir = Join-Path $env:USERPROFILE ".config\opencode"
$cfg    = Join-Path $cfgDir "opencode.json"
New-Item -ItemType Directory -Force -Path $cfgDir | Out-Null
if (Test-Path $cfg) {
  Log "opencode config exists at $cfg (leaving as-is)"
} else {
  Log "Writing opencode config to $cfg"
  @"
{
  "`$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": { "baseURL": "http://localhost:11434/v1" },
      "models": {
        "$Model": { "name": "$Model" }
      }
    }
  }
}
"@ | Set-Content -Path $cfg -Encoding UTF8
}

Write-Host ""
Write-Host "[ok] Workbench ready." -ForegroundColor Green
Write-Host "  Editor: $Editor"
Write-Host "  Model:  $Model  (override with `$env:MODEL=...)"
Write-Host "  Ollama: http://localhost:11434  (autostarts on login)"
Write-Host "  Config: $cfg"
Write-Host ""
Write-Host "Try it:"
Write-Host "  mkdir `$HOME\projects\playground; cd `$HOME\projects\playground"
Write-Host "  opencode"
