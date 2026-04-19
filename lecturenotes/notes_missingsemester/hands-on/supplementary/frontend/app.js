/**
 * PixelWise — Frontend starter code
 *
 * Provides:
 *   - 28×28 pixel drawing canvas (scaled to 280×280 for usability)
 *   - Extracts pixel array and sends POST /api/classify
 *   - Displays prediction, confidence, and per-class confidence bars
 *   - Frontend analytics counters (page loads, submissions, clears)
 *
 * Students should read and understand this code in Block 7.
 * Block 9 extends it with analytics and the canvas-clear event.
 */

// ============================================================
// Configuration
// ============================================================

const API_BASE = "/api";
const API_KEY = "replace-me"; // must match .env SECRET_API_KEY
const GRID_SIZE = 28;
const CANVAS_SIZE = 280; // 28 * 10
const PIXEL_SIZE = CANVAS_SIZE / GRID_SIZE; // 10px per logical pixel

// ============================================================
// Canvas setup
// ============================================================

const canvas = document.getElementById("drawing-canvas");
const ctx = canvas.getContext("2d");

// Internal 28×28 pixel grid (0 = black/empty, 255 = white/drawn)
let pixelGrid = Array.from({ length: GRID_SIZE }, () =>
    Array.from({ length: GRID_SIZE }, () => 0)
);

let isDrawing = false;

// --- Drawing handlers ---

function getGridCoords(e) {
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor(((e.clientX - rect.left) / rect.width) * GRID_SIZE);
    const y = Math.floor(((e.clientY - rect.top) / rect.height) * GRID_SIZE);
    return [
        Math.max(0, Math.min(GRID_SIZE - 1, x)),
        Math.max(0, Math.min(GRID_SIZE - 1, y)),
    ];
}

function drawPixel(x, y) {
    // Draw with a small brush (center + neighbors for smoother strokes)
    for (let dy = -1; dy <= 1; dy++) {
        for (let dx = -1; dx <= 1; dx++) {
            const nx = x + dx;
            const ny = y + dy;
            if (nx >= 0 && nx < GRID_SIZE && ny >= 0 && ny < GRID_SIZE) {
                // Center pixel gets full intensity, neighbors get partial
                const intensity = dx === 0 && dy === 0 ? 255 : 180;
                pixelGrid[ny][nx] = Math.max(pixelGrid[ny][nx], intensity);
            }
        }
    }
    renderCanvas();
}

function renderCanvas() {
    ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
    for (let y = 0; y < GRID_SIZE; y++) {
        for (let x = 0; x < GRID_SIZE; x++) {
            const val = pixelGrid[y][x];
            if (val > 0) {
                ctx.fillStyle = `rgb(${val}, ${val}, ${val})`;
                ctx.fillRect(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE);
            }
        }
    }
}

canvas.addEventListener("mousedown", (e) => {
    isDrawing = true;
    const [x, y] = getGridCoords(e);
    drawPixel(x, y);
});

canvas.addEventListener("mousemove", (e) => {
    if (!isDrawing) return;
    const [x, y] = getGridCoords(e);
    drawPixel(x, y);
});

canvas.addEventListener("mouseup", () => { isDrawing = false; });
canvas.addEventListener("mouseleave", () => { isDrawing = false; });

// Touch support for mobile
canvas.addEventListener("touchstart", (e) => {
    e.preventDefault();
    isDrawing = true;
    const touch = e.touches[0];
    const [x, y] = getGridCoords(touch);
    drawPixel(x, y);
});

canvas.addEventListener("touchmove", (e) => {
    e.preventDefault();
    if (!isDrawing) return;
    const touch = e.touches[0];
    const [x, y] = getGridCoords(touch);
    drawPixel(x, y);
});

canvas.addEventListener("touchend", () => { isDrawing = false; });

// ============================================================
// API interaction
// ============================================================

async function classifyDrawing() {
    const resultDisplay = document.getElementById("result-display");
    const confidenceBars = document.getElementById("confidence-bars");

    // Check if canvas is empty
    const hasContent = pixelGrid.some(row => row.some(val => val > 0));
    if (!hasContent) {
        resultDisplay.innerHTML = '<div class="result-placeholder">Draw something first!</div>';
        return;
    }

    resultDisplay.innerHTML = '<div class="result-placeholder">Classifying...</div>';

    try {
        const response = await fetch(`${API_BASE}/classify`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-API-Key": API_KEY,
            },
            body: JSON.stringify({ pixels: pixelGrid }),
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(err.detail || `HTTP ${response.status}`);
        }

        const result = await response.json();
        displayResult(result);
        stats.submissions++;
        updateStats();
    } catch (err) {
        resultDisplay.innerHTML = `<div class="result-placeholder" style="color:#dc2626;">Error: ${err.message}</div>`;
        confidenceBars.style.display = "none";
    }
}

function displayResult(result) {
    const resultDisplay = document.getElementById("result-display");
    const confidenceBars = document.getElementById("confidence-bars");
    const barsContainer = document.getElementById("bars-container");

    // Main prediction
    const confidencePct = (result.confidence * 100).toFixed(1);
    resultDisplay.innerHTML = `
        <div>
            <div class="result-prediction">${result.prediction}</div>
            <div class="result-confidence">${confidencePct}% confidence</div>
        </div>
    `;

    // Per-class confidence bars
    if (result.scores) {
        confidenceBars.style.display = "block";
        barsContainer.innerHTML = "";

        // Sort classes numerically
        const sortedClasses = Object.keys(result.scores).sort(
            (a, b) => parseInt(a) - parseInt(b)
        );

        for (const cls of sortedClasses) {
            const score = result.scores[cls];
            const pct = (score * 100).toFixed(1);
            const isTop = cls === result.prediction;

            const row = document.createElement("div");
            row.className = "bar-row";
            row.innerHTML = `
                <div class="bar-label">${cls}</div>
                <div class="bar-track">
                    <div class="bar-fill ${isTop ? "top" : ""}"
                         style="width: ${pct}%"></div>
                </div>
                <div class="bar-value">${pct}%</div>
            `;
            barsContainer.appendChild(row);
        }
    }
}

// ============================================================
// Clear canvas
// ============================================================

function clearCanvas() {
    pixelGrid = Array.from({ length: GRID_SIZE }, () =>
        Array.from({ length: GRID_SIZE }, () => 0)
    );
    renderCanvas();
    document.getElementById("result-display").innerHTML =
        '<div class="result-placeholder">Draw a digit and press Classify</div>';
    document.getElementById("confidence-bars").style.display = "none";

    stats.clears++;
    updateStats();

    // Block 9: notify backend about canvas clear (uncomment when ready)
    // fetch(`${API_BASE}/events/clear`, {
    //     method: "POST",
    //     headers: { "X-API-Key": API_KEY },
    // }).catch(() => {});
}

// ============================================================
// Frontend analytics counters (Block 9)
// ============================================================

const stats = {
    loads: 0,
    submissions: 0,
    clears: 0,
};

function updateStats() {
    document.getElementById("stat-loads").textContent = stats.loads;
    document.getElementById("stat-submissions").textContent = stats.submissions;
    document.getElementById("stat-clears").textContent = stats.clears;
}

// ============================================================
// Button handlers
// ============================================================

document.getElementById("btn-submit").addEventListener("click", classifyDrawing);
document.getElementById("btn-clear").addEventListener("click", clearCanvas);

// ============================================================
// Init
// ============================================================

stats.loads++;
updateStats();
renderCanvas();
