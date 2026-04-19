# Instructor Prep Manual — Advanced Coding / Handwerkszeug

This document lists all manual preparation work required before each block.
Students receive pre-built VM snapshots so they can start fresh if they fall behind.

---

## Supplementary Materials

All supplementary code is in `hands-on/supplementary/`:

```
supplementary/
├── training/
│   ├── train.py              # B4 — trains digit_classifier_v1.pkl (digits 1–9)
│   └── train_v2.py           # B4/B8 — trains digit_classifier_v2.pkl (digits 0–9)
├── frontend/
│   ├── index.html             # B7 — 28×28 canvas, submit button, results panel
│   ├── style.css              # B7 — minimal styling
│   └── app.js                 # B7 — drawing logic, fetch, analytics counters
├── tests/
│   ├── conftest.py            # B8 — shared pytest config (env vars)
│   ├── test_classifier.py     # B8 — tests for classify_batch / classify
│   └── test_api.py            # B8 — tests for API endpoints
└── analytics/
    └── analytics_endpoint.py  # B9 — /analytics route + query helper
```

**Before the course:** run `train.py` and `train_v2.py` to produce the `.pkl` files.
Test the frontend against the API. Run the test suite to verify it passes.

---

## Host Machine Layout

Before you touch VirtualBox, decide where things live on your host machine. Two separate locations:

```
<wherever VirtualBox puts VMs>/              # default, leave alone
├── dev/
│   ├── dev.vbox
│   ├── dev.vdi                               # disk image
│   └── Snapshots/                            # internal snapshots live here
└── server/
    └── ...

pixelwise-exports/                            # YOU create this directory
├── B0-fresh-dev.ova
├── B0-fresh-server.ova
├── B1-complete-dev.ova
├── B1-complete-server.ova
└── ...                                       # one pair per block
```

- **Internal snapshots** (VirtualBox's "Take Snapshot" feature) are stored automatically inside each VM's own folder. Leave them there — they're tied to the disk chain and break if moved.
- **`.ova` exports** are the portable files you distribute to students. Keep these in a dedicated `pixelwise-exports/` directory — separate from VirtualBox's working files, easy to upload, easy to back up.

**Disk budget:** expect each `.ova` to be 3–6 GB. Ten blocks × two VMs ≈ 60–120 GB total, plus whatever the live VMs themselves use (20 GB each, thin-provisioned). Plan for ~200 GB free on the host.

---

## General Setup — Base VM Images

### Prerequisites

- Host machine with ≥16 GB RAM and ≥200 GB free disk
- [VirtualBox 7.0+](https://www.virtualbox.org/wiki/Downloads)
- [Ubuntu 22.04 LTS Server ISO](https://releases.ubuntu.com/22.04/)

### Step 1 — Create the host-only network

**VirtualBox → File → Tools → Network Manager → Create**

- IPv4 address: `192.168.56.1`
- IPv4 mask: `255.255.255.0`
- DHCP: **disabled** (we assign static IPs manually)

The name will be `vboxnet0` (Linux/macOS) or `VirtualBox Host-Only Ethernet Adapter` (Windows). Remember which it is — you'll select it in Step 2.

### Step 2 — Create the `dev` VM

**Machine → New**
- Name: `dev`
- Type: Linux, Version: Ubuntu (64-bit)
- Memory: 2048 MB
- Create a new virtual hard disk: VDI, dynamically allocated, 10 GB

Then open **Settings** for the new VM:
- **System → Processor:** 2 CPUs
- **Network → Adapter 1:** NAT (for internet access)
- **Network → Adapter 2:** Host-only Adapter → select the adapter from Step 1
- **Storage:** click the `Empty` optical drive under the controller (IDE or SATA). On the right, click the small disc icon next to `Optical Drive`, choose `Choose a disk file`, and select the Ubuntu Server ISO.

Start the VM.

### Step 3 — Install Ubuntu on `dev`

In the Ubuntu Server installer:
- Language / keyboard / mirror: defaults are fine
- Network: accept defaults — both adapters should be detected
- Storage: use entire disk, LVM
- Profile:
  - Your name: `Student`
  - Server's name: `dev`
  - Username: `student`
  - Password: pick one and **write it down** (students will need it)
- **Install OpenSSH server** — required for Block 1
- Skip all featured snaps
- Wait for install → **Reboot Now** → remove the ISO when prompted

Log in as `student` and update:

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 4 — Configure the static IP on `dev`

```bash
ip link                                  # find interface names
sudo nano /etc/netplan/00-installer-config.yaml
```

Replace the contents with (adjust interface names if yours differ):

```yaml
network:
  version: 2
  ethernets:
    enp0s3:              # NAT adapter — DHCP for internet
      dhcp4: true
    enp0s8:              # host-only adapter — static IP
      dhcp4: false
      addresses:
        - 192.168.56.10/24
```

Apply and verify:

```bash
sudo netplan apply
ip addr show enp0s8      # should show 192.168.56.10
```

### Step 5 — Clone `dev` into `server`

Shut down `dev`:

```bash
sudo shutdown -h now
```

In VirtualBox: **right-click `dev` → Clone**
- Name: `server`
- MAC Address Policy: **Generate new MAC addresses for all network adapters**
- Clone type: **Full clone**

Start `server`, log in, then change hostname and IP:

```bash
sudo hostnamectl set-hostname server
sudo nano /etc/netplan/00-installer-config.yaml   # change .10 → .11
sudo netplan apply
```

### Step 6 — Verify connectivity

Boot both VMs. From `dev`:

```bash
ping -c 3 192.168.56.11    # reaches server
ping -c 3 8.8.8.8          # reaches internet
```

From `server`:

```bash
ping -c 3 192.168.56.10    # reaches dev
```

If all four pings succeed, the base setup is done. Shut both VMs down cleanly before the next step.

---

## Snapshot & Export Workflow

There are **two separate mechanisms** — don't confuse them:

| Mechanism | Purpose | Where it lives | When to use |
|-----------|---------|----------------|-------------|
| **Snapshot** (internal) | Your own rollback points while building `BN-complete` | Inside the VM folder (`Snapshots/`) | Iterate without losing work; restore to retry a block |
| **`.ova` export** | Distribute to students | `pixelwise-exports/` (you create it) | Once `BN-complete` is verified, export and hand out |

### Snapshot naming convention

Each block produces a pair — but they're the same state, relabelled:

- `BN-complete` — state after Block N is fully done (what students build toward)
- `B(N+1)-fresh` — identical to `BN-complete`, named for the next block's starting point

You don't need to take/export twice. `BN-complete.ova` *is* `B(N+1)-fresh.ova`. Just document the aliasing.

### Taking an internal snapshot

**GUI:** select the VM → **Snapshots** tab → **Take** → name it `B0-fresh`, `B1-complete`, etc.

**CLI:**
```bash
VBoxManage snapshot dev take "B0-fresh" --description "Bare Ubuntu + student user"
```

Fast (copy-on-write), meant for iteration. Students never see these.

### Exporting to `.ova`

**GUI:** **File → Export Appliance** → select the VM → Next
- Format: OVF 1.0
- File: `pixelwise-exports/B0-fresh-dev.ova`
- **Check "Strip all network adapter MAC addresses"** (prevents conflicts on student machines)
- Export. Repeat for `server`.

**CLI (faster, scriptable):**
```bash
VBoxManage export dev    --output pixelwise-exports/B0-fresh-dev.ova    --options manifest,nomacs
VBoxManage export server --output pixelwise-exports/B0-fresh-server.ova --options manifest,nomacs
```

### Building `BN-complete` from `B(N-1)-complete`

For each block:

1. Restore (or boot fresh from) the `B(N-1)-complete` internal snapshot
2. Work through the block's hands-on steps until the target state is reached
3. **Shut down cleanly** — `sudo shutdown -h now`, not Save State, not Close
4. Optionally shrink the disk: `sudo fstrim -av` inside the VM before shutdown
5. Take internal snapshot `BN-complete`
6. Export both VMs to `pixelwise-exports/BN-complete-{dev,server}.ova`
7. Test-import one of them (rename the running VM first, or use a spare machine) to make sure it boots cleanly

### Tips

- **Always shut down cleanly** before export. Paused/saved-state VMs produce `.ova` files that won't import reliably.
- **Run `fstrim` before each export.** Deleted files still inflate the disk image otherwise — `sudo fstrim -av` inside the VM reclaims the space.
- **Keep a "golden" branch.** Take snapshots frequently while building a block; if something goes wrong, roll back to the last good one instead of starting over from `B(N-1)-complete`.
- **Version your exports.** If you fix a bug in `B3-complete` after the course started, rename the old one to `B3-complete-v1.ova` before overwriting. Students may still be running on the old state.

---

## Per-Block Prep

### Block 1 — The Lab: Servers, VMs & Linux Basics

**Instructor prep:**
- Provide `B0-fresh` VM images (two bare Ubuntu VMs with student user)
- No additional files needed — students set up everything from scratch

**Snapshot to produce:** `B1-complete`
- Two VMs running, SSH key auth from dev → server, password auth disabled

---

### Block 2 — Version Everything: Git & GitHub

**Instructor prep:**
- Ensure GitHub classroom or individual repos are ready (if using GitHub Classroom)
- Provide `B1-complete` snapshots for students who didn't finish Block 1

**Snapshot to produce:** `B2-complete`
- Git + Python installed on server (`setup-server.sh` ran)
- PixelWise repo on GitHub, cloned to `/opt/pixelwise` on server
- Tagged `v0.1`

---

### Block 3 — Package the Stack: Dependencies & Project Structure

**Instructor prep:**
- Provide `B2-complete` snapshots

**Snapshot to produce:** `B3-complete`
- `app/`, `data/`, `models/` directories exist
- `.venv` created, dependencies installed and pinned
- `.env.example` with `SECRET_API_KEY` and `DEBUG`
- `.gitignore` covers `.venv/`, `*.pkl`, `data/`, `.env`

---

### Block 4 — Integrate the Model: From Artefact to Interface

**Instructor prep:**
- Provide `B3-complete` snapshots
- **Train and distribute the model files** (scripts in `supplementary/training/`):
  - Run `python supplementary/training/train.py` → produces `models/digit_classifier_v1.pkl` (MNIST 1–9)
  - Run `python supplementary/training/train_v2.py` → produces `models/digit_classifier_v2.pkl` (MNIST 0–9)
  - Host both `.pkl` files somewhere students can download (course website, shared drive, etc.)
  - Provide `train.py` as supplementary reading material (not part of hands-on)
- **Prepare MNIST test samples** for `predict.py` smoke test (5–10 sample images with ground truth labels) — `train.py` downloads MNIST automatically, so you can extract samples from there

**Snapshot to produce:** `B4-complete`
- `app/classifier.py` with `classify_batch` and `classify`
- `predict.py` smoke test working
- `models/MODELCARD.md` written
- `MODEL_PATH` in `.env.example`

---

### Block 5 — The Backend: APIs & Services

**Instructor prep:**
- Provide `B4-complete` snapshots

**Snapshot to produce:** `B5-complete`
- FastAPI app running: `POST /classify`, `GET /results` (stub), `GET /health`
- API key auth middleware working
- `slowapi` rate limiting configured
- `pixelwise.service` systemd unit file installed and enabled
- Service running, accessible from dev VM

---

### Block 6 — Data Lives Here: Databases & SQL

**Instructor prep:**
- Provide `B5-complete` snapshots

**Snapshot to produce:** `B6-complete`
- PostgreSQL installed, `pixelwise` user and database created
- SQLAlchemy model in `app/models.py`
- API wired to DB: predictions stored on classify
- `GET /results` returns real data
- Alembic initialised, first migration (confidence column) applied
- `DATABASE_URL` in `.env.example`

---

### Block 7 — Face the World: Frontend & Nginx

**Instructor prep:**
- Provide `B6-complete` snapshots
- **Distribute the frontend starter code** (ready in `supplementary/frontend/`):
  - `index.html` — page with 28×28 canvas, submit button, results panel
  - `style.css` — minimal styling
  - `app.js` — canvas drawing logic, `fetch` call to `/api/classify`, result rendering, analytics counters
  - **Important:** update the `API_KEY` constant in `app.js` to match the course's shared key, or instruct students to replace it
  - Test the starter code against the API to make sure it works end-to-end before distributing

**Snapshot to produce:** `B7-complete`
- Nginx installed and configured (static files + reverse proxy)
- Frontend deployed to `/opt/pixelwise/frontend/`
- HTTPS with self-signed certificate
- Security headers configured
- Full stack working: browser → Nginx → uvicorn → FastAPI → PostgreSQL

---

### Block 8 — Automate Everything: CI/CD, Cron, Webhooks & Backups

**Instructor prep:**
- Provide `B7-complete` snapshots
- **Distribute the test boilerplate** (ready in `supplementary/tests/`):
  - `test_classifier.py` — 11 tests for `classify_batch` and `classify` (shape, keys, values, error cases)
  - `test_api.py` — 5 tests for API endpoints (health, classify, results, auth)
  - `conftest.py` — shared pytest config that sets environment variables for CI
  - Students copy these into their `tests/` directory — they are provided, not written
- **Provide `digit_classifier_v2.pkl`** (if not already distributed in B4)
- Ensure students have GitHub Actions available (free tier is sufficient)

**Snapshot to produce:** `B8-complete`
- `.github/workflows/ci.yml` and `deploy.yml` working
- `scripts/deploy.sh` created
- Nightly backup cron job configured (pg_dump + rsync to dev VM)
- `/backups/pixelwise/` directory on dev VM
- Feature flag `MODEL_VERSION` in `.env`
- Both v1 and v2 model files in `models/`

---

### Block 9 — Watch It Run: Monitoring, Logging & Analytics

**Instructor prep:**
- Provide `B8-complete` snapshots
- **Set up a Discord server** for the course (or have students create their own):
  - Create a `#pixelwise-alerts` channel
  - Create a webhook for the channel
  - Distribute the webhook URL or have students create their own
- **Distribute the `/analytics` endpoint boilerplate** (ready in `supplementary/analytics/`):
  - `analytics_endpoint.py` — contains `compute_analytics()` helper and example route
  - Students integrate it into `app/main.py` — they deploy it, not write it
  - The focus is on interpreting the results, not writing SQL

**Snapshot to produce:** `B9-complete`
- Structured JSON logging configured
- `/health` upgraded with DB and model checks
- Discord health check cron running
- Low-confidence and canvas-clear Discord alerts wired
- `/analytics` endpoint deployed
- Frontend counters (page loads, submissions, clears) added

---

### Block 10 — AI Dev & Vibe Coding

**Instructor prep:**
- Provide `B9-complete` snapshots
- **Set up Ollama + Qwen on the server VM:**
  - Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
  - Pull the model: `ollama pull qwen2.5-coder`
  - Verify: `ollama run qwen2.5-coder "Hello"`
  - This must be done on the server VM (or a dedicated GPU machine if available)
  - Ensure Aider can connect: `pip install aider-chat && aider --model ollama/qwen2.5-coder`
- **Test the full Aider + Ollama workflow** on the PixelWise codebase before class
- No snapshot needed after this block — it's the final session

---

## Checklist Summary

| Block | Files to Provide | Manual Setup |
|-------|-----------------|--------------|
| B1 | Base VM images (.ova) | Create VMs, configure networking |
| B2 | — | GitHub Classroom setup (optional) |
| B3 | — | — |
| B4 | `v1.pkl`, `v2.pkl` (from `supplementary/training/`) | Run train.py, train_v2.py |
| B5 | — | — |
| B6 | — | — |
| B7 | `supplementary/frontend/` (index.html, style.css, app.js) | Test frontend against API |
| B8 | `supplementary/tests/` (test_classifier, test_api, conftest) | — |
| B9 | `supplementary/analytics/analytics_endpoint.py`, Discord webhook | Set up Discord server |
| B10 | — | Install Ollama + Qwen on server |
