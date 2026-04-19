# Advanced Coding / Handwerkszeug — Lecture Outline

## Concept

Ten blocks. One application, built from scratch, start to finish.

Students leave with a deployed, monitored, auto-deploying AI-powered web service — and the muscle memory to build the next one themselves.

---

## The Application: PixelWise

A handwritten digit recognition web app, built incrementally across all 10 blocks:

- Users draw a digit on a pixelated 28×28 canvas in the browser
- The backend runs an image classification model trained on MNIST
- The model predicts the digit — class + confidence score
- Results are stored in a database; analytics and monitoring reveal usage patterns and model performance

Every tool we teach is introduced at the moment it is needed by PixelWise. The app is the narrative thread.

---

## Security Thread

Security is **not a dedicated block** — it is a recurring thread woven into every block at the moment it becomes contextually relevant. Students learn security as a mindset, not a checklist.

| Block | Security Concept |
|-------|-----------------|
| B1 | SSH key auth (never passwords), file permissions, principle of least privilege |
| B2 | `.gitignore` for secrets, never commit `.env`, git history is permanent; `setup-server.sh` must never contain credentials |
| B3 | `pip audit`, `.env.example` pattern, no secrets in source code |
| B4 | Training data and model artefacts not in git; no PII in training data; `train.py` is the reproducible source of truth |
| B5 | API key auth middleware, rate limiting, Pydantic as input validation boundary |
| B6 | DB credentials via env vars, no root DB user, parameterized queries (SQL injection) |
| B7 | Nginx security headers, HTTPS/TLS, CORS configuration |
| B8 | GitHub Actions secrets, SSH-only deploys, backup file permissions |
| B9 | Log sanitization (no PII), `/health` must not leak internals |
| B10 | AI-generated code must pass human review, prompt injection risks, never give AI access to secrets |

---

## Format

Each block is **2 × 45 minutes**:
- **Session A** — Theory, concepts, live demo by professor
- **Session B** — Hands-on lab: students apply the session A concepts directly to PixelWise

---

## The 10 Blocks

---

### Block 1 — The Lab: Servers, VMs & Linux Basics

> *Before you can build anything, you need to own the machine.*

**Session A: The Vision, the Map, and the Box**

*Part 1 — Course overview (≈15 min)*
- What this course is and what it is not: not more algorithms, but the craft layer underneath them
- The problem: you can write Python, but can you ship it? Can you keep it running?
- What we are building together: PixelWise — a deployed, monitored, auto-deploying AI web service
- The arc across 10 blocks: from bare metal to production
- What "done" looks like at Block 10: a live URL, a CI/CD pipeline, Discord monitoring alerts, and AI-assisted development skills
- The final project structure — shown once here so students always know where things are headed:

```
pixelwise/
├── app/                  # B3 — Python package: API, model loader, DB models
│   ├── __init__.py
│   ├── main.py           # B5 — FastAPI app
│   ├── models.py         # B6 — SQLAlchemy models
│   └── classifier.py     # B4 — model inference wrapper
├── data/                 # B4 — training data (gitignored)
├── models/               # B4 — trained model artefacts (gitignored)
├── frontend/             # B7 — HTML/CSS/JS with drawing canvas
├── nginx/                # B7 — Nginx config
├── scripts/              # B8 — deploy, backup scripts
├── tests/                # B8 — CI test suite
├── train.py              # B4 — reproducible training script
├── predict.py            # B4 — stepping stone: CLI inference (replaced by API in B5)
├── requirements.txt      # B3 — pinned dependencies
├── .env.example          # B3 — grows block by block
├── .gitignore
└── README.md
```

*Each folder is empty until its block. The map is here from day one.*

*Part 2 — The architecture and what VMs represent (≈10 min)*
- Introduce the two-VM setup as a physical metaphor for real-world deployment:
  - `dev` VM (192.168.56.10) = your laptop / developer machine — where you write and test code
  - `server` VM (192.168.56.11) = the production server — where real users hit your app
- The deploy step as the bridge: code travels from dev → server deliberately and reproducibly
- **The cautionary tale:** imagine editing code directly on the production server at 2pm, making a typo, and taking the app down for 300 users while you scramble to undo it — with no way back, no backup, no colleague who knows what you changed. That is why we have two machines.
- This two-machine mental model persists for the entire course

*Part 3 — Just enough Linux to survive (≈20 min)*
- What is a server? Just a computer that runs software and waits for requests — no screen, no mouse
- Virtual Machines: isolation + snapshots as safety nets (you can always roll back)
- The five commands you need today: `ls`, `cd`, `pwd`, `mkdir`, `cat`
- Where things live: `/home` (your files), `/etc` (config), `/opt` (our app will live here)
- You are not alone on this machine: users exist, files have owners — `whoami`, `ls -la`
- SSH: connecting to a remote machine from your terminal — the only door into the server

**Session B: Hands-On**
- Spin up two VMs: `dev` (192.168.56.10) and `server` (192.168.56.11)
- Generate an Ed25519 SSH key pair, copy public key to server with `ssh-copy-id`
- Disable password authentication on the server: `sudo nano /etc/ssh/sshd_config` → set `PasswordAuthentication no`, restart SSH — first use of `nano` on a real config file
- Explore the server: `ls`, `cd`, `pwd` — visit `/home`, `/etc`, `/opt`; read a config file with `cat`; understand who you are with `whoami`, `id`, `ls -la`

**Security Thread:** SSH key auth (never password auth), `chmod`/`chown`, principle of least privilege — know exactly what your user can and cannot do.

**Milestone:** Two networked VMs running. SSH key auth configured. You own the box.

---

### Block 2 — Version Everything: Git & GitHub

> *No zip files. No `final_v2_FINAL.py`. No excuses.*

**Session A: Git & Collaboration**
- The Git data model: blobs, trees, commits, branches, HEAD
- The staging workflow: `git add`, `git commit`, `git diff`, `git log`
- Branching: `git branch`, `git checkout`, `git merge`
- Merge conflicts: what they are, how to resolve them
- Tags: `git tag v0.1` — marking a point in history that matters; lightweight vs annotated tags
- Remotes: `git remote`, `git push`, `git pull`, `git fetch`
- GitHub: creating a repo, forking vs cloning, pull requests, issues, README conventions
- `.gitignore`: what to ignore and why

**Session B: Hands-On**
- **Before anything else**: create a GitHub account (if not already), configure git identity (`git config --global user.name` / `user.email`), generate and add an SSH key to GitHub — students must be able to push before they can do the rest
- On the server VM: install required system packages: `sudo apt install -y git python3 python3-pip python3-venv curl` — verify with `git --version`, `python3 --version`
- Write `setup-server.sh` — capturing exactly what you just ran, so any fresh VM can be provisioned identically
- On dev: initialise the PixelWise repo, write `README.md` and `.gitignore` (Python, editors, secrets, model files)
- Commit `setup-server.sh` as the very first file — version control paying for itself immediately
- Push to GitHub, tag `v0.1` with `git tag -a v0.1 -m "initial server setup"` and `git push --tags`
- SSH to the server, `git clone` the repo — PixelWise now has a home at `/opt/pixelwise`

**Security Thread:** `.gitignore` is a security control. Git history is permanent — a leaked secret committed once is leaked forever, even after deletion. `setup-server.sh` must never contain passwords, keys, or credentials.

**Milestone:** PixelWise lives on GitHub. Server has the repo cloned at `/opt/pixelwise`. `setup-server.sh` is version-controlled: provisioning is reproducible and auditable.

---

### Block 3 — Package the Stack: Dependencies & Project Structure

> *Reproducibility starts before you write a single line of application code.*

**Session A: Managing the Environment**
- Why dependency management matters: "works on my machine" — and why that excuse gets you fired
- `venv`: isolated per-project environments — one project, one venv, no conflicts
- `pip install`, `pip freeze`, `pip install -r requirements.txt` — the full cycle
- Anatomy of `requirements.txt`: one package per line, pinned versions (`==`), version ranges (`>=`, `~=`), why pinning matters for reproducibility and security
- Semantic versioning: MAJOR.MINOR.PATCH — what a version bump actually signals, and why you should care before upgrading
- `.env` files + `python-dotenv`: separating config from code — the 12-factor app principle
- `.env.example`: the contract between developers; it grows block by block as new services are introduced
- **The container alternative:** Docker and Docker Compose solve the same "reproducible environment" problem at the OS level rather than the Python level. This course teaches the virtualenv path to keep the OS layer visible and learnable. Docker is the natural next step after this course — students who want to go further are pointed to resources here.

*Optional self-study: `pyproject.toml` — when `requirements.txt` starts to hurt*
> `pip freeze > requirements.txt` captures everything — your direct dependencies, their dependencies, and their dependencies' dependencies, all flattened into one unreadable list. Six months later you want to upgrade one package: which of those 47 lines do you actually own, and which were pulled in automatically? `pyproject.toml` solves this by separating *what you depend on* (your direct deps, loosely pinned) from *what gets installed* (a generated lock file with the full resolved graph). Upgrades become surgical: bump one line, regenerate the lock, done. Tools like `uv` and `poetry` use this model and are fast becoming the standard. Once the `requirements.txt` workflow is second nature, this is the upgrade that makes dependency management sane at scale. *[link to pypa.io/en/latest/]*

**Session B: Hands-On**
- Create and activate a virtualenv: `python3 -m venv .venv && source .venv/bin/activate`
- Scaffold only what we need right now: `app/`, `data/`, `models/` — other folders appear in the block that first needs them (students already know the full map from Block 1)
- Install `scikit-learn`, `joblib`, `python-dotenv`; pin with `pip freeze > requirements.txt`
- Write the first `.env.example` — two lines to start, each a different kind of config:

```
# API key callers must send in the X-API-Key header (a secret — never a real value here)
SECRET_API_KEY=replace-me

# Debug mode: when true, FastAPI shows /docs and full error tracebacks to anyone.
# Never true in production — you'd be handing attackers a map of your API.
DEBUG=true
```

  Students create their actual `.env` with a real value for `SECRET_API_KEY`. The contrast is immediate: `.env.example` is committed and public; `.env` is local and secret.
- **Revisit `.gitignore` from Block 2:** now there are real things to protect — add `.venv/`, `*.pkl`, `data/`, `.env`. Students now feel the `.gitignore` rather than just reading it: without it, `git status` is full of noise and secrets are one careless `git add .` away from GitHub
- Run `pip audit` — inspect and discuss any findings; explain what a CVE is
- Commit the scaffold: `app/`, `data/`, `models/`, `requirements.txt`, `.env.example`, updated `.gitignore` — a meaningful second commit that shows the project taking shape

**Security Thread:** `pip audit` catches known CVEs in dependencies. `.env.example` makes the secrets contract explicit without exposing values. Never commit `.env`. The `.venv/` folder must be in `.gitignore` — it is large, machine-specific, and reconstructable from `requirements.txt` alone.

**Milestone:** PixelWise has `app/`, `data/`, `models/`, a virtualenv, pinned dependencies, and a minimal `.env.example`. The `.gitignore` is now doing real work. Anyone who clones the repo can recreate the environment in two commands.

---

### Block 4 — Integrate the Model: From Artefact to Interface

> *Your ML course teaches you to train models. This block teaches you to make one work inside a software system.*

**Session A: The Model as a Software Component**

*Part 1 — What a model file actually is (≈10 min)*
- A `.pkl` is a build artefact, not source code. You distribute it, you don't commit it.
- Who produced it: the course provides `models/digit_classifier_v1.pkl` — a LogisticRegression pipeline trained on MNIST digits 1–9 (9 classes, ~54 000 training samples, public domain). Class 0 is intentionally held back — students can add it without collecting any new data. Students did not train it; their job is to integrate it correctly.
- The training script (`train.py`) is provided as supplementary lecture material. Students who want to understand how the artefact was produced can run it: MNIST downloads automatically via `sklearn.datasets.fetch_openml`, training takes ~30 seconds on CPU. It is *not* part of the hands-on session — proper training practices (learning rate schedules, regularisation search, early stopping, GPU considerations) would double the length of this course. For that, read:
  - Karpathy, *A Recipe for Training Neural Networks*: <https://karpathy.github.io/2019/04/25/recipe/>
  - Google, *Rules of Machine Learning*: <https://developers.google.com/machine-learning/guides/rules-of-ml>
- The `pickle`/`joblib` deserialisation risk: loading a `.pkl` from an untrusted source can execute arbitrary code. Only load artefacts you control.

*Part 2 — Honouring the model contract (≈15 min)*
- Every model was trained on inputs in a specific format. Violate that format and it predicts silently wrong — no error, just garbage output. This is called **train/serve skew** and it is the most common production ML bug.
- The MNIST model expects: a 28×28 greyscale image, pixel values normalised to [0, 1], flattened to a 784-element vector.
- **Binarization:** the canvas in the browser produces uint8 (0–255). Converting to binary (0/1) reduces payload size, removes noise, and matches training-time preprocessing exactly. Show the difference visually — binarized digits are cleaner inputs.
- The sklearn Pipeline bundles preprocessing + model into one serialised object. Load it once and the preprocessing is guaranteed to match training. No separate normalisation step to forget.

*Part 3 — Designing the inference interface (≈15 min)*
- Before writing any code, design the contract. Start with the class roster, then the function signatures.
- **The class dict:** a named constant that makes the valid output set explicit and independent of the model file:
  ```python
  CLASSES = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
  # must match model.classes_ — verified at startup
  # note: "0" is intentionally absent in v1
  ```
  This list belongs in the code, not only in the model. The frontend, the DB schema, and the API docs all reference it. If the model is swapped for one trained on different classes, the assertion (see Session B) fails loudly at startup rather than returning silently wrong labels.
- **Online vs batch — design around batch.** Scalability question: what happens when 50 students submit a drawing at the same second? If the server processes each request one at a time, the model is called 50 times with a `(1, 784)` array each. If it batches them, the model is called once with a `(50, 784)` array — sklearn's `predict_proba` is natively vectorised, so the cost is nearly identical. Design the core function around batch; single-user is a special case:

  | | `classify_batch` (core) | `classify` (wrapper) |
  |---|---|---|
  | Input | `(N, 28, 28)` uint8 array | `(28, 28)` uint8 array |
  | Output | `list` of N result dicts | single result dict |
  | Who calls it | Block 5 API (always) | `predict.py` smoke test |

- **The function signatures:**
  ```python
  def classify_batch(images: np.ndarray) -> list[dict]:
      """
      Args:
          images: (N, 28, 28) uint8 numpy array, values 0-255
      Returns:
          List of N dicts, each:
          {
              "prediction": str,          # element of CLASSES
              "confidence": float,        # probability of top class, 0–1
              "scores": dict[str, float]  # probability per class, keys == CLASSES
          }
      Raises:
          ValueError: if images.ndim != 3 or images.shape[1:] != (28, 28)
      """
      if images.ndim != 3 or images.shape[1:] != (28, 28):
          raise ValueError(f"Expected (N,28,28), got {images.shape}")
      arr = (images > 128).astype(float).reshape(len(images), -1)  # binarize + flatten
      probs = _pipeline.predict_proba(arr)                         # (N, 10)
      return [
          {"prediction": CLASSES[p.argmax()],
           "confidence": float(p.max()),
           "scores": dict(zip(CLASSES, p.tolist()))}
          for p in probs
      ]

  def classify(image: np.ndarray) -> dict:
      """Convenience wrapper — single image."""
      return classify_batch(image[np.newaxis])[0]
  ```
- The API in Block 5 always calls `classify_batch`, even for a single drawing — it just passes a `(1, 28, 28)` array. When a request queue is added later, no signature changes needed.
- Load `_pipeline` once at module level — deserialising on every request kills throughput.

*Part 4 — The Model Card (≈10 min)*
- A model card is the documentation artefact that links a model to its provenance and limitations. Established standard (Google, HuggingFace). Contains:
  - What it was trained on (MNIST digits 1–9, 9 classes, ~54 000 training samples, ~9 000 test samples, public domain; class 0 withheld)
  - What it can do: predict handwritten digits 1–9, expected accuracy ~92% (LogisticRegression baseline)
  - What it cannot do: known failure modes (6 vs 9, 3 vs 8, messy or rotated digits)
  - Benchmarks: accuracy per class on MNIST test set (provided alongside the model)
  - Intended use: drawn digits from 28×28 canvas; out-of-scope: photographed digits, non-digit characters
- When `v2` is deployed via the Block 8 feature flag, the model card gets updated — traceability across versions

**Session B: Hands-On**
- Download `models/digit_classifier_v1.pkl` (provided) — inspect it: `joblib.load()`, `type(model)`, `model.classes_`
- Experiment with binarization: load a sample MNIST digit, show the raw pixel array vs binarized — observe that the digit structure is preserved and noise is eliminated
- Write `app/classifier.py`:
  ```python
  CLASSES = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]  # v1: 0 held back

  # Load once at module level
  _pipeline = joblib.load(os.getenv("MODEL_PATH"))
  assert list(_pipeline.classes_) == CLASSES, \
      f"Model classes don't match CLASSES constant: {_pipeline.classes_}"

  def classify_batch(images: np.ndarray) -> list[dict]:
      # validate shape (N, 28, 28)
      # binarize + flatten to (N, 784)
      # predict_proba → (N, 9)
      # return list of {prediction, confidence, scores} dicts

  def classify(image: np.ndarray) -> dict:
      """Convenience wrapper — single image."""
      return classify_batch(image[np.newaxis])[0]
  ```
  The assertion is the key teaching moment: it fires at startup. A swapped model with different classes is caught the moment the service starts, not when a user gets a wrong digit.
- Write `predict.py` as a smoke test: load 5 MNIST test samples, call `classify_batch()`, print predictions vs ground truth. *Frame it explicitly: "this is the CLI version of what the API will do in Block 5 — `POST /classify` calls `classify_batch` with a `(1, 28, 28)` array"*
- Update `.env` and `.env.example`: add `MODEL_PATH=models/digit_classifier_v1.pkl`
- Write `models/MODELCARD.md`:
  - Dataset: MNIST (source, license, ~54k train / ~9k test, digits 1–9; class 0 withheld for v2 challenge)
  - Input format: 28×28 uint8, binarized, flattened to 784 features
  - Performance: accuracy per digit class on MNIST test set (provided)
  - Known failure modes: 6/9 confusion, 3/8 confusion, rotated or messy digits
  - Version: v1, date, provider
- Commit `app/classifier.py`, `predict.py`, `models/MODELCARD.md`, updated `.env.example` — not the `.pkl`

**Optional challenge — add the missing 0:** The digit class `"0"` was intentionally excluded from v1. To produce v2: add `"0"` to `CLASSES`, include MNIST's class-0 samples in the training split, re-run `train.py`, save as `digit_classifier_v2.pkl`. The assertion will break the moment v2 is loaded against v1's `CLASSES` — fix it by updating the constant. Update `MODELCARD.md`: document that v2 covers all 10 digits and note any accuracy change from the added class. No data collection needed — MNIST has the 0s already. This challenge connects directly to Block 8: v2 is deployed via the feature flag, and Block 9's analytics compare v1 vs v2 performance.

*Teaser — could we have spotted the missing class without reading the model card?* Think about it before reading the hints:
- **Class distribution in the DB:** after a few hundred predictions, run `SELECT prediction, COUNT(*) FROM predictions GROUP BY prediction ORDER BY prediction`. Does the distribution look right? A missing class is invisible in inference — the model never predicts it, users never see an error, the DB just never accumulates any 0s. Would you have noticed?
- **Input-side monitoring:** if a user draws a 0 and the model confidently predicts a 6, the confidence score looks normal. No exception is raised. How would you distinguish a wrong prediction from a missing class?
- **Confidence as a signal:** when the model sees an input it wasn't trained on, it is often — not always — less certain. If you track the distribution of confidence scores over time, a systematic drop in average confidence or a spike in low-confidence predictions could indicate out-of-distribution inputs. It is a weak signal, but it is a runtime signal that requires no labelled data.
- **Confidence thresholds:** instead of always returning a prediction, return `null` when `confidence < threshold`. The volume of rejected predictions is itself a monitoring signal — a sudden increase tells you something the model doesn't recognise is arriving. What should PixelWise do when it can't confidently classify a digit?
- **A catch-all "other" class:** train an explicit out-of-distribution class on samples the model should reject — noise, letters, symbols, blank canvases. Now the model can say "I don't recognise this" rather than hallucinating a confident wrong digit. What are the failure modes of this approach?

These questions don't have quick answers. Systematic detection of silent model failures — uncertainty estimation, distribution shift, missing classes, silent degradation — is the domain of **MLOps**. This surface is intentionally shallow here; it is covered in depth in the MLOps course.

**Security Thread:** Never load a `.pkl` from an untrusted source — `joblib`/`pickle` deserialisation executes arbitrary code. `MODEL_PATH` comes from `.env`, never hardcoded — so swapping the model in production requires only an env var change, not a code change.

**Milestone:** `app/classifier.py` exposes a batch-first inference interface that scales from one student to N concurrent users with no code changes. `predict.py` proves it works end-to-end on real MNIST samples. `MODELCARD.md` documents what the model is and isn't. Block 5 has everything it needs.

---

### Block 5 — The Backend: APIs & Services

> *Making your code speak to the world over HTTP.*


**Session A: From Script to Service & API Contracts**
- HTTP fundamentals: methods, status codes, headers, request/response cycle
- REST principles: resources, stateless, uniform interface, JSON
- API contracts: what is a contract, why document it, how to make it explicit

  - Show the Pydantic request/response models for `POST /classify`:
    ```python
    class ClassifyRequest(BaseModel):
        pixels: list[list[int]]  # 28×28, values 0-255

    class ClassifyResponse(BaseModel):
        prediction: str           # element of CLASSES
        confidence: float         # probability of top class, 0–1
        scores: dict[str, float]  # probability per class, keys == CLASSES
    ```
  - The response model makes the contract bidirectional: Block 7 frontend knows exactly what JSON to expect
  - Discuss input validation, shape, dtype, and error handling:
    - What happens if the input is not 28×28? (e.g. 27×27, 28×29, or a flat list)
    - How to define and document error responses (e.g. HTTP 422 Unprocessable Entity, custom error message)
    - Example error response:
      ```json
      {
        "detail": "Input must be a 28x28 array of integers (0-255)"
      }
      ```
    - How to document these in FastAPI (OpenAPI schema, response_model, examples)
  - FastAPI’s `/docs` as a living contract: auto-generated OpenAPI docs, including error responses
- FastAPI: path operations, Pydantic models for request/response validation
- `curl` as a first-class debugging tool
- Rate limiting: why it matters even in development — 30 students hitting the same endpoint simultaneously will surface it on day one; where it fits in the stack (application-level vs reverse proxy)
- From dev server to production process:
  - `uvicorn` runs fine for testing, but one Ctrl-C and it's gone — that is not a service
  - `systemd`: the OS-level supervisor — starts your service on boot, restarts it on crash, captures its logs. We use a fraction of what it can do; in practice, `systemd` manages timers (like cron but with dependency awareness), socket activation (start a service only when a connection arrives), resource limits (cap CPU/memory per service), dependency ordering (start the database before the app), and more. It is the init system of virtually every modern Linux server — worth exploring beyond this course.
  - `systemctl`: `start`, `stop`, `restart`, `status`, `enable` — the operator's interface to `systemd`
  - `journalctl`: structured log viewer — filtering by unit (`-u pixelwise`), by time (`--since`), following live (`-f`); where you go first when something breaks
  - *Sidenote — gunicorn:* in production, you'd run gunicorn in front of uvicorn to spawn multiple worker processes (concurrency, crash isolation). For our classroom setup, a single uvicorn worker behind `systemd` is sufficient. gunicorn is standard in production Python deployments — students who deploy beyond this course will encounter it.



**Session B: Hands-On**
- Build the PixelWise API in `app/main.py`:
  - `POST /classify` — accepts a 28×28 pixel array (JSON, see contract above), calls `classify_batch`, returns prediction + confidence + scores. This is the call `classifier.py` was designed for in Block 4. Test with valid and invalid input (wrong shape, wrong dtype) and observe the error response in the API docs and via `curl`.
  - `GET /results` — **stub only**: returns `{"results": [], "note": "persistence added in Block 6"}`. The endpoint exists and is documented; the DB is not wired yet.
  - `GET /health` — liveness check: confirms the model loaded, returns `{"status": "ok", "model_version": "v1"}`
- Add API key authentication middleware (`X-API-Key` header, value from `.env`)
- Add simple rate limiting (e.g. `slowapi` or custom decorator): limit requests per minute per IP or API key
- Run with `uvicorn app.main:app --host 0.0.0.0 --port 8000` — single-worker, sufficient for the classroom
- Register as a `systemd` service on the server VM: `pixelwise.service`
- Use `systemctl status pixelwise`, `journalctl -u pixelwise` to debug and monitor
- Intentionally kill and restart the backend at least once: observe logs, see what fails, fix and restart
- Draw a digit in the browser console: `POST /classify` returns a live prediction. First end-to-end loop.


**Security Thread:**
- API key auth via `X-API-Key` header middleware (value from `.env`, never hardcoded)
- Rate limiting: limit requests per minute per IP or API key (e.g. `slowapi`)
- Pydantic models are the input validation boundary — reject malformed input at the edge (wrong shape, wrong dtype)

**Milestone:** PixelWise API running as a managed `systemd` service on the server VM. `POST /classify` returns live digit predictions. `GET /results` is stubbed — the system is complete end-to-end except for persistence, which arrives in Block 6. Students have killed and restarted their backend at least once, and debugged with `journalctl`.

---

### Block 6 — Data Lives Here: Databases & SQL

> *Your API works. Now make it remember.*

**Session A: Persistence**
- Why persist at all? Your API already returns predictions — but the moment the response is sent, the data is gone. A database makes it permanent:
  - **Analytics:** every prediction is a data point — what digits are drawn, how confident the model is, which model version served the request, when it happened. Block 9's `/analytics` endpoint queries this.
  - **Beyond this course:** in production you would also store raw inputs to build retraining datasets, let users correct wrong predictions for labelled data, or detect model drift over time. We won't do that here, but it all starts with having a database.
- Relational databases: tables, rows, columns, primary keys
- SQL fundamentals: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `WHERE` — enough to query and inspect your own data
- *Mention without deep dive:* `JOIN` (combining rows from multiple tables), `GROUP BY` / `COUNT` / `AVG` (aggregation), `ORDER BY`, `LIMIT`, `CREATE INDEX` (speeding up queries on large tables). Students will encounter these as the app grows; the full treatment belongs in a dedicated database course.
- Schema design: thinking in entities — design from the API response shape you already know
- *Why PostgreSQL over SQLite?* SQLite is convenient: zero setup, the DB is a single file, great for prototyping and embedded apps. But it has no user authentication, no password protection, no network access, and limited concurrency — a single writer blocks all readers. For a multi-user web service where 30 students hit the same DB simultaneously, PostgreSQL is the right tool: real users and permissions, network-accessible, concurrent reads and writes, `psql` as a proper operator interface. We go straight to PostgreSQL so students learn the production tool from day one.
- PostgreSQL: installation, users, databases, `psql` as the operator's interface to the DB
- SQLAlchemy: a Python library that maps database tables to Python classes. You define a `Prediction` class with fields like `prediction`, `confidence`, `created_at` — SQLAlchemy generates the SQL to create the table, insert rows, and query data. Students write Python, not SQL. This is called an ORM (Object-Relational Mapper) and is standard in Python web development.
- Schema migrations — why they matter:
  - You design a schema, deploy it, store 500 predictions. Then you realise you forgot a column. You cannot drop the table and recreate it — those 500 rows are real data. You need a tool that alters the live schema without losing data.
  - Alembic: the migration tool for SQLAlchemy. Generates migration scripts from model changes, applies them in order, tracks which migrations have run. Covered briefly here — this is a deep topic for later courses.
- *Sidenote — Redis:* an in-memory key-value store. Extremely fast reads (~1ms). Good for caching expensive, frequently repeated queries (e.g., a product page hit by thousands of users), session storage, or rate-limiting counters. In PixelWise, every hand-drawn digit is unique pixel data — cache hit rate ≈ 0%, so Redis adds nothing here. Mentioned so students know it exists; the use cases appear in larger-scale applications.

**Session B: Hands-On**
- Install PostgreSQL on the server VM: `sudo apt install postgresql`; create a dedicated `pixelwise` user and `pixelwise` database — first real encounter with DB administration
- Design the initial PixelWise schema (intentionally minimal — **only the class label**):
  - `Prediction` — `id`, `created_at`, `prediction` (str), `model_version` (str)
- Implement the SQLAlchemy model in `app/models.py`, create tables with `Base.metadata.create_all()`
- Wire `POST /classify` to store every result in PostgreSQL before returning the response
- Replace the `GET /results` stub with a real query: recent predictions, filterable by digit class
- Collect ~20 predictions via `curl`. Then ask: *"How confident is the model actually in these predictions? Is it always sure, or does it sometimes guess?"* The API returns confidence — but the database only stored the class label. You cannot answer the question from the data you have.
- **First migration:** use Alembic to add a `confidence` (float) column. Existing rows get `NULL`; new predictions store the top-class probability. Verify with `psql`: `SELECT prediction, confidence FROM predictions ORDER BY created_at DESC LIMIT 5;` — old rows show `NULL`, new rows show a real number.
  - *This is the teaching moment:* in a real system with millions of rows and live traffic, you cannot just drop and recreate. Migrations are how schemas evolve safely. This topic is covered in much more depth in database and backend courses — here we show the concept and the tool.
- Update `.env` and `.env.example`: add `DATABASE_URL`
- Restart the `systemd` service, verify end-to-end: draw a digit → prediction + confidence stored → `GET /results` returns both

**Security Thread:** DB credentials live in `.env`, never in code. Create a dedicated DB user with minimal privileges — no `CREATEDB`, no superuser. SQLAlchemy's parameterised queries prevent SQL injection — never string-format SQL.

**Milestone:** Every digit prediction is stored in PostgreSQL with confidence. `GET /results` returns real data. Students have run their first schema migration on a live database. The `GET /results` stub from Block 5 is now complete.

---

### Block 7 — Face the World: Frontend & Nginx

> *Browsers do not talk to your app server directly.*

**Session A: The Frontend & Nginx**
- The problem: uvicorn listens on port 8000, but browsers expect port 80 (HTTP) and 443 (HTTPS). You need something in front that handles the ports, serves static files, and forwards API requests. That something is Nginx.
- Nginx roles: static file server, reverse proxy, SSL terminator
- Nginx config anatomy: `http`, `server`, `location` blocks
- Reverse proxy: `proxy_pass` forwards `/api/` requests to `localhost:8000` (uvicorn) — the browser never talks to uvicorn directly
- Serving static files: `root`, `index` — Nginx serves HTML/CSS/JS far more efficiently than Python
- CORS: what it is (browser security policy that blocks cross-origin requests), why it causes pain during deployment (frontend on port 443, API on port 8000 = different origins), how to configure it in FastAPI and/or Nginx. Students will hit this — explain it before they do.
- The frontend stack — and why vanilla JS:
  - HTML for structure, CSS for layout, JavaScript for interactivity. The `fetch` API for sending requests to the backend.
  - *Why not React/Vue/Svelte?* Frameworks solve problems that appear at scale — component reuse, state management, routing across dozens of views. PixelWise has one page with one canvas and one results panel. A framework would add a build toolchain (Node.js, npm, bundler), a learning curve orthogonal to this course, and complexity that hides what's actually happening between browser and server. Vanilla JS keeps the HTTP layer visible: students see the raw `fetch` call, the JSON payload, the response — no abstraction in between.
  - *Why is this production-ready?* No build step, no `node_modules`, no framework version to maintain. The code runs in any browser, can be read by any developer, and deploys as static files served directly by Nginx. For a focused single-page tool, this is the right level of technology. Students who later build larger applications will recognise when a framework becomes necessary — and why.
  - The starter code is provided; students need to understand it well enough to wire it up and extend it in Block 10.
- URL design best practices:
  - Clean, readable URLs: `/results` not `/getResults.php?action=list`
  - Query parameters for filtering and configuration: `/results?digit=7&model=v2`
  - Storing IDs in URLs for analytics and state: `/classify?session=abc123` lets you track a user's session without cookies, link to specific results, or pass configuration to the frontend. The URL is state — treat it deliberately.
- HTTPS/TLS: why it matters (without it, API keys travel in plaintext), how certificates work, self-signed (dev) vs Let's Encrypt (prod)
- *Sidenote — `ufw`:* Ubuntu's firewall tool. On managed production servers, the firewall is typically preconfigured to allow only ports 22, 80, 443. On the classroom VMs this is a formality (host-only network), but students should know the concept exists.

**Session B: Hands-On**
- Deploy the PixelWise frontend (provided as starter code): 28×28 pixel drawing canvas, submit button, live prediction panel showing digit + confidence bar. Walk through the code so students understand what it does — the `fetch` call to `/api/classify`, the pixel array extraction from the canvas, the response rendering.
- Configure Nginx: serve `frontend/` as static files, proxy `/api/` to `localhost:8000`
- Verify CORS: confirm the frontend can reach the API through Nginx without cross-origin errors. If it breaks, debug it — this is a rite of passage.
- Enable HTTPS with a self-signed certificate; walk through Let's Encrypt conceptually
- Add security headers: `X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy`

**Security Thread:** Security headers are configured at the Nginx layer — one place, all responses covered. HTTPS encrypts the channel; without it, API keys travel in plaintext. CORS misconfiguration is a common deployment bug — configure allowed origins explicitly, never `*` in production.

**Milestone:** PixelWise accessible in a browser at `https://192.168.56.11`. Draw a digit, get a prediction. Nginx serves static files and proxies the API. The full stack is live: browser → Nginx → uvicorn → FastAPI → PostgreSQL.

---

### Block 8 — Automate Everything: CI/CD, Cron, Webhooks & Backups

> *Manual deploys are technical debt. Automate or regret.*

**Session A: Pipelines, Schedules & Automation**
- CI/CD — what it is and why it matters:
  - Continuous Integration: every push is automatically linted and tested — broken code is caught before it reaches the server
  - Continuous Deployment: every merge to `main` automatically deploys to the server — no manual SSH-and-pull
  - The pipeline: lint → test → deploy, each step gates the next
- GitHub Actions: workflow YAML syntax, triggers (`push`, `pull_request`), jobs, steps, runners
- Using secrets in Actions: `${{ secrets.MY_SECRET }}` — never echo them, never hardcode them
- Cron syntax: the five fields, common patterns, `crontab -e`
  - What cron jobs are good for — a sample of real-world uses:
    - Database backups (`pg_dump` on a schedule)
    - Clearing old temporary files or expired sessions
    - Health checks that ping your own service and alert on failure
    - Certificate renewal (Let's Encrypt auto-renewal)
    - Triggering retraining pipelines on new data
    - Sending periodic summary reports
    - Log rotation (compressing and deleting old log files so disks don't fill up)
  - The common thread: anything that needs to happen reliably on a schedule without a human remembering
  - Students have already seen one form of this: `systemd` restarts their crashed service automatically (Block 5). The system is full of similar automation they haven't noticed — `journalctl` rotates its own logs, package managers run unattended security updates, certificate tools schedule renewals. Cron jobs are the explicit, user-controlled version of automation that is already everywhere under the hood.
- Webhooks: HTTP endpoints triggered by external events — the internet is event-driven. GitHub can call your server when code is pushed; Discord can receive a message when your deploy succeeds. The pattern is always the same: an event happens → an HTTP POST is sent to a URL you control.
- Backup strategy: what to back up (the database — code is on GitHub, the model is reproducible from `train.py`), how (`pg_dump`), where (off-site — a backup on the same server dies with the server). The dev VM is the natural off-site target: `pg_dump` creates the dump, `rsync` copies it to the dev VM over SSH. The two-machine setup from Block 1 pays off again. How to verify: restore from a backup at least once — an untested backup is not a backup.
- `rsync`: efficient file sync over SSH — incremental (only transfers changed bytes), fast, scriptable. The right tool for moving backup files between machines.
- Feature flags: deploying new behaviour without deploying new code. The simplest form: an env var that controls which code path runs. Change the flag, restart the service — the new behaviour is live. No code change, no PR, no CI pipeline. This is how teams roll out features gradually or switch between model versions without risk.
- *Tests — where they live:* the CI pipeline runs `pytest`, but writing tests is an entire discipline covered in dedicated courses. Here we show where tests live (`tests/`), what a test looks like (a few example tests are provided in the boilerplate), and how the CI pipeline runs them. The goal is to see the feedback loop: push code → tests run → green or red.

**Session B: Hands-On**
- Write `.github/workflows/ci.yml`: on push, lint with `ruff`, run `pytest` against the boilerplate tests in `tests/`
- Write `.github/workflows/deploy.yml`: on merge to `main`, SSH to server, `git pull`, restart `systemd` service — boilerplate provided, students adapt it to their setup
- Write `scripts/deploy.sh`: the deploy steps as a standalone script (pull, install deps, run migrations, restart service) — reusable from both Actions and manual deploys
- Add a cron job: nightly `pg_dump` on the server, then `rsync` the dump to the dev VM (`192.168.56.10:/backups/pixelwise/`) over SSH. Date-stamped filenames, 7-day retention. Verify by restoring one backup into a test database on the dev VM.
- Add a simple feature flag: an env var `MODEL_VERSION=v1` in `.env` that the API reads to decide which model to load. Both `digit_classifier_v1.pkl` and `digit_classifier_v2.pkl` are provided. Switching the model is a config change + service restart, not a code deploy. Block 9 will use this to compare model performance.

**Security Thread:** Store all deployment credentials (SSH keys, server IP) as GitHub Actions secrets — never in workflow files. `rsync` and SSH-based deploys only, never plain protocols. Backup files contain your entire database — protect them accordingly (permissions, encryption for off-site storage).

**Milestone:** Every push to `main` automatically lints and tests. Every merge deploys to the server. Nightly database backup is running and has been verified by restoring once. Feature flag for model version switching is in place.

---

### Block 9 — Watch It Run: Monitoring, Logging & Analytics

> *You cannot improve what you cannot measure.*

**Session A: Observability**
- You already know `journalctl` for reading logs and debugging crashes (Block 5). Now the question changes: your service is running and nobody is watching the terminal. How do you know it's working well? Three pillars:
  1. **Logs** — structured, queryable records of what happened
  2. **Monitoring** — automated checks that alert you when something breaks
  3. **Analytics** — patterns in your data that reveal how the system behaves over time
- Structured logging: why plain strings (`print("got request")`) are not enough. JSON log format: every log line is a dict with `timestamp`, `level`, `endpoint`, `request_id`, `latency`, `predicted_class`, `confidence`, `model_version`. Parseable by machines, readable by humans, queryable with `jq` or piped into any log aggregation tool.
- The `/health` endpoint — upgraded: liveness (is the process running?) vs readiness (can it serve requests? is the DB reachable? is the model loaded?). What to expose externally vs what to keep internal.
- Monitoring without new tools: a cron job that `curl`s `/health` every 5 minutes and sends a Discord webhook notification on failure. Your service talks to you when something breaks — on your phone, in your pocket. No infrastructure to install, no dashboard to maintain.
- Event-driven notifications: the Discord webhook pattern generalises beyond health checks. Any event worth knowing about can trigger a notification. A second example: notify when the model produces a low-confidence prediction (below a threshold). If these spike, the model may be struggling with inputs it wasn't trained on — a real signal, not noise.
- This is the natural step toward model monitoring: tracking confidence over time, spotting distribution shifts, detecting when a model goes stale. You don't need a dedicated MLOps platform to start — you need structured logs and a way to query the data you're already storing.
- Analytics — everything that happens in the app is a potential data point:
  - **Backend signals:** prediction counts, confidence values, model version usage — already stored in PostgreSQL from Block 6
  - **Frontend signals:** page loads, drawings submitted, canvas clears, time spent drawing — any user interaction can be tracked by the frontend and sent to the API
  - *Brief intro to analytics concepts:* funnels (open page → draw → submit → view result — where do users drop off?), retention (do users come back?), sessions (grouping events into a single visit — recall the session IDs from Block 7's URL design). These concepts are how product teams understand user behaviour at scale.
- The `/analytics` endpoint: provided as boilerplate — returns prediction counts, average confidence, and model version breakdown. Students hit the endpoint and see the data. The lesson is not how to write the queries, but what the numbers tell you about your app.

**Session B: Hands-On**
- Add structured JSON logging to the PixelWise API: every request logs `timestamp`, `level`, `endpoint`, `request_id`, `latency`, `predicted_class`, `confidence`, `model_version`
- Upgrade `/health` to check DB connectivity and model load status — return `{"status": "ok"}` externally, log details internally
- Set up Discord webhook monitoring: configure a Discord webhook URL, write a cron job that `curl`s `/health` every 5 minutes, sends a Discord notification on failure. Test it by stopping the `systemd` service — does your phone ping?
- Add a second Discord notification: alert when a prediction's confidence falls below a threshold (e.g. 0.5). Test it by drawing an ambiguous digit — does Discord ping? In production, a spike in low-confidence alerts is a real signal that something changed.
- Deploy the `/analytics` endpoint (provided as boilerplate): returns prediction counts per digit class, average confidence, model version breakdown. Hit it with `curl` and interpret the results — which digit is drawn most? Is one model version more confident than the other?
- Add frontend analytics: instrument the starter code to count page loads, drawings submitted, and canvas clears. Display these in a small panel in the UI. Discuss: what would you track if this were a real product?
  - *Sidenote:* in production, analytics panels are never public — they reveal usage patterns and internal metrics. They belong behind authentication on a separate internal route (e.g. `/admin/analytics`).

**Security Thread:** Log sanitization — never log raw pixel data or user identifiers unnecessarily. The `/health` endpoint confirms the system is alive but does not expose internal state (DB passwords, stack traces, version details) to unauthenticated callers.

**Milestone:** PixelWise is fully observable. Logs are structured and queryable. Discord alerts on health check failure and low-confidence predictions. Analytics endpoint and frontend counters show usage patterns. Students can answer: "how is my app being used, and how is my model performing?"

---

### Block 10 — AI Dev & Vibe Coding

> *The tools changed. The fundamentals did not. Know both.*

**Session A: AI-Assisted Development**
- Two ways AI helps you code — and when to use which:
  - **Terminal/CLI agents:** Claude Code, Aider, Codex CLI — work directly in your repo from the terminal, read your files, make changes, run commands. Best for: implementing features, debugging, refactoring across multiple files. You describe what you want, the agent does the work.
  - **IDE-integrated agents:** Cursor, Windsurf, Cline — full IDE with AI built in, visual diffs, inline suggestions. Best for: editing in context, reviewing changes visually, inline completions while typing.
  - *Briefly:* autocomplete tools (GitHub Copilot) and chat-based tools (ChatGPT, Claude.ai) exist too — students will have encountered these. CLI and IDE agents are the next level: they read your whole project, not just the current file.
- How these tools actually work — the agent loop:
  1. **Observe:** the agent collects context — your repo structure, git status, recent commits, the files you point it at
  2. **Inspect:** it analyses the code and your request to understand what needs to change
  3. **Choose:** it selects an action — edit a file, run a command, ask you a question
  4. **Act:** it executes the action, gets the result, and loops back to observe
  - This loop repeats until the task is done or the agent is stuck. The harness (the program wrapping the LLM) validates every action before execution: is the tool recognised? Are the arguments valid? Is the file path inside the repo? The LLM proposes, the harness gatekeeps.
  - The quality depends entirely on what context you give the agent. Garbage in, garbage out.
- Git as a safety net — commit before you let an agent touch your code:
  - `git diff` shows exactly what the agent changed — nothing hidden, nothing missed
  - `git checkout .` reverts everything if the agent made a mess
  - `git stash` saves your current state before experimenting
  - `git checkout -b experiment` — let the agent work on a branch. If it works, merge. If not, delete the branch and nothing ever touched `main`.
  - This is not just an AI workflow — it's how you work with any risky change: experimental refactors, dependency upgrades, merge conflict resolution. Always commit clean state first, then change, then review the diff.
- Sandboxing — AI agents run on your machine, so what stops them from doing damage?
  - The risk: an unrestricted agent can run `rm -rf /`, `curl` your secrets to an external server, install packages, or modify system files. It runs with your user's permissions.
  - How sandboxing works in practice:
    - **Permission prompts:** agents like Claude Code ask before executing each command — you approve or deny. The human stays in the loop.
    - **Code-only mode:** Aider is code-only by default — it reads and edits files but does not run shell commands at all.
    - **Restricted execution:** Docker containers, VMs, or chroot jails — the agent runs in an isolated environment where it physically cannot access the host system. Professional setups use this for untrusted code execution.
    - **Allow/deny lists:** configure which commands or directories the agent can access. Some tools let you whitelist specific tools (e.g., "can run `pytest` but nothing else").
  - The principle: give the agent the minimum access it needs. Read your code — yes. Edit files — yes. Run arbitrary commands — only with explicit approval. Access `.env` or SSH keys — never.
- Context management — agents have a limited context window (how much text the LLM can process at once):
  - Long conversations degrade quality: the agent forgets earlier instructions, repeats mistakes, or contradicts itself. Older parts of the conversation get compressed or dropped.
  - Practical rules: start a fresh conversation when switching tasks. Point the agent at specific files rather than letting it read everything. Keep instructions files short and focused.
  - Subagents: some tools can spawn child agents for subtasks — e.g., "research this question in a separate context, report back." The child agent operates with tighter permissions and its own context window, keeping the parent conversation clean.
- Reading diffs — the core review skill:
  - When an agent (or a colleague) makes changes, you don't re-read the entire file. You read the diff: what was added, what was removed, what was modified.
  - `git diff` in the terminal, side-by-side diffs in the IDE, GitHub's pull request diff view — all the same skill. Students need to read diffs fluently. This is how code review actually works.
- Teaching the AI your project — instructions as code:
  - `CLAUDE.md` — project-level instructions for Claude Code: conventions, architecture, what NOT to do
  - `.github/copilot-instructions.md` — same concept for GitHub Copilot
  - `.cursorrules` — Cursor-specific project rules
  - Skill files (`.md` files with structured instructions for specific tasks — e.g., "how to add a new API endpoint", "how to write a migration"). These are reusable recipes the AI follows consistently.
  - The pattern across all tools: declarative instructions that persist across sessions. You write them once, the AI follows them every time. This is the highest-leverage thing you can do with AI tools.
- Working with AI agents effectively:
  - Use `/plan` to let the agent think before it acts — review the plan, adjust, then let it execute. Don't jump straight to implementation.
  - The agent-edit-verify loop: agent makes changes → `git diff` → run the app → works or doesn't → if not, feed the error back to the agent or fix it yourself → iterate
  - Code review with AI: have the agent review your own code — it catches things you're blind to after staring at the same file for hours.
- MCP and tool use: agents can do more than edit code. MCP (Model Context Protocol) lets agents connect to external tools — reading documentation, searching the web, running tests, querying databases, interacting with APIs. Brief overview: the agent is not limited to what's in your repo.
- When to trust AI output:
  - Strong: boilerplate, tests for known behaviour, documentation, refactoring, explaining unfamiliar code
  - Weak: security-sensitive code, novel algorithms, anything touching infrastructure or secrets
  - Never: blind trust without reading the output.

**Session B: Hands-On**
- Set up Aider (open-source CLI agent) connected to Qwen via Ollama (self-hosted on the server, provided by the course). Aider works from the terminal, reads your repo, and makes changes directly — students experience the full agent workflow with a local model, no external API needed.
- **First rule:** commit clean state before you start. `git add -A && git commit -m "pre-agent checkpoint"` — your undo button.
- Explore the tool on the PixelWise codebase: ask it to explain a file, describe the architecture, find where a function is called. Get comfortable with the conversation loop.
- Write a `CLAUDE.md` (or equivalent instructions file) for the PixelWise project: document the stack, the conventions, what the AI should and should not do. Commit it to the repo.
- Write a skill file for a specific task — e.g., "how to add a new API endpoint to this project" — with step-by-step instructions the AI can follow. Test it: does the AI produce correct code when given only the skill file and a task description?
- Use the AI to make a change to PixelWise (student's choice — a new feature, a refactor, a bug fix). Review: `git diff` — read every line. Run the app — does it work? If not, feed the error back. Iterate until it's right or revert and try a different approach.
- Group discussion: when was the AI faster than writing code by hand? When was it slower? When was it confidently wrong?

**Security Thread:** AI-generated code must pass the same security review as human-written code. Prompt injection: user-submitted text that ends up in an AI prompt is an injection vector — never pipe untrusted input into an AI call. The AI must never be given access to `.env`, SSH keys, or production credentials directly.

**Milestone:** Students have used a terminal AI agent on a real codebase. Instructions file and skill file committed to the repo. Every student can read a diff, revert a bad change, and iterate with an agent.

*Course wrap-up:* Look at what you've built — from two empty VMs to a deployed, monitored, auto-deploying AI web service with structured logging, database persistence, CI/CD, and now AI-assisted development. The full stack, end to end. You own every layer.

---

## Application Progression (PixelWise Across the Blocks)

```
Block 1   Two VMs running, SSH access configured
          │
Block 2   Server has Python/git installed; repo on GitHub + cloned to /opt/pixelwise
          │
Block 3   App skeleton scaffolded, virtualenv, pinned deps, .env.example
          │
Block 4   Digit classifier integrated, batch inference interface live, MODELCARD written
          │
Block 5   FastAPI + systemd — API serving digit predictions on the server
          │
Block 6   PostgreSQL wired, first migration run, GET /results stub completed
          │
Block 7   Nginx reverse proxy, 28×28 pixel canvas frontend, HTTPS — full stack live
          │
Block 8   CI/CD pipeline, push-to-deploy, nightly backup, feature flag for model version
          │
Block 9   Structured logging, Discord alerting, analytics queries, model monitoring
          │
Block 10  AI coding tools learned, instructions + skill files committed, course wrap-up
          │
          ▼
    Complete: deployed, monitored, auto-deploying AI digit recognition service — and the skills to build the next one
```

---

## Scope Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Containers (Docker) | Out of scope | Students learn the OS layer first; Docker abstracts it away too early |
| Testing | No dedicated block | Introduced inline where relevant (B5 API, B8 CI pipeline) |
| Security | Cross-cutting thread | Mindset > checklist; teach it at the moment of relevance |
| SSH depth | Keys + safe access only | tmux, port forwarding out of scope for this course |
| Shell scripting | Distributed across blocks | Navigation in B1, `apt`/`git clone` in B2, scripts deferred to where they are first needed |
| Editor | `nano` in B1 | Introduced at first contact with the server (editing SSH config in Session B) |
| ML Model | Dedicated Block 4 | Model artefact must exist before the API (B5) can serve it; establishes the `train.py` → `.pkl` pattern |
| Redis | Sidenote (Block 6) | Mentioned in theory so students know it exists; no hands-on — PixelWise doesn't benefit from it |
| Webhooks | In (Block 8 theory, Block 9 hands-on) | Concept in B8; Discord webhook monitoring implemented in B9 |
| Discord webhook | In (Block 9) | Monitoring and alerting tool — service talks to you on failure or low-confidence predictions |
| Backups | Paired with automation (Block 8) | Backups without automation are not real backups |
| Feature flags | In (Block 8) | Simple env var approach; enables v1/v2 model comparison in Block 9 |
