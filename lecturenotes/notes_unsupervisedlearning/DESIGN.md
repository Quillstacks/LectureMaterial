# Lecture Notes Design Guide
## Unsupervised Learning — Prof. Dr.-Ing. Mark Schutera

This document captures all layout, style, and structural decisions for these lecture notes so that new chapters can be written consistently. Wherever a rule is shown with a code snippet, that snippet is the canonical form; copy and adapt it.

---

## 0. Scope and Density Expectations

A finished chapter in this series sits in the following band, anchored by ch03/04/05/06:

| Quantity | Range | Notes |
|---|---|---|
| Total line count | **1300–1550** | Body matter, not counting includes |
| `\section{}` calls | 1 (ch03) – 10 (ch05) | Use ch04 hybrid model by default (see §3) |
| `\newthought{}` calls | 60–90 | Replaces internal subsections; one per conceptual unit |
| `\marginnote{}` calls | 10–25 | Notation, intuition, callbacks |
| Body figures | 7–12 | Each has `\caption{}` + `\label{fig:...}` |
| Margin figures | 5–10 | `width=\marginparwidth` |
| Tables | 1–3 | Always `table*[ht]` with booktabs |
| Algorithms | 1–3 | Every algorithm preceded by motivating prose |
| `align*` blocks | 24–52 | Heavier in math-driven chapters |
| Theory : exercise line ratio | **~3:1** | Block 2 ≫ Block 3, but Block 3 ≥ 280 lines |
| Exercise section worked items | 6–10 | Each opens with `\newthought{...}` |

A chapter with 525 lines, 4 worked exercises, and 5 figures is **not finished**; it is a draft.

---

## 1. Document Class & Preamble

- **Document class**: custom `tufte` class (`\documentclass{../sharedAssets/tufte}`)
- **Packages**: `amsmath`, `tikz`, `pgfplots` (compat=1.18), `booktabs`, `algorithm`/`algpseudocode`, `enumitem`, `soul`, `textcase`, `pifont`, `float`, `tabularx`
- **Fonts**: `\loadoptionalfonts` (Palatino/Bera/Helvetica stack from tufte class)
- **Index**: `\makeindex` enabled; use `\index{term}` liberally at chapter/section headings and first uses of key terms

---

## 2. Chapter Title and Subtitle

### Chapter title
- A **noun phrase naming the topic**, in title case, matching the file name. Examples:
  - `\chapter{Similarity and Distance}` (ch01)
  - `\chapter{Centroid Clustering}` (ch02)
  - `\chapter{Hierarchical Clustering}` (ch03)
  - `\chapter{Density-Based Clustering}` (ch04)
  - `\chapter{Dimensionality Reduction}` (ch05)
  - `\chapter{Variational Inference}` (ch06)
  - `\chapter{Uncertainty Estimation}` (ch07)
  - `\chapter{Self-Supervised Learning}` (ch08)
- **Never an aphorism, slogan, or full sentence in the title.** Aphorisms belong in the subtitle.
- Append 1–4 `\index{...}` entries on the same line for indexing the chapter heading.

### Chapter subtitle
- A `\newthought{...}` line **immediately after** `\chapter{...}`.
- 3–10 words. Often playful, lyrical, or evocative. Period optional; sentence-case or title-case both seen.
- Examples:
  - `\newthought{Enter the Feature Space}` (ch01)
  - `\newthought{Same Same but Different.}` (ch02)
  - `\newthought{Ich springe von Level zu Level zu Level.}` (ch03)
  - `\newthought{It is all about that space, about that space.}` (ch04)
  - `\newthought{Folding and Unfolding Space.}` (ch05)
  - `\newthought{embeddings and latent feature spaces.}` (ch06)
- This is where you put the punchy aphorism; the chapter title stays neutral and topical.

---

## 3. Chapter Structure (mandatory three blocks)

```
BLOCK 1 — INTRODUCTION
  \section{The Why}             ← see §4 for the layered Why pattern
    \subsection{Hands On Experience}  ← see §5 for the layered Hands-On pattern
  \newthought{The Learning Objectives}  ← exactly 3 bullets, verb-led
                                          ("Understand…", "Apply…", "Identify…")

BLOCK 2 — MAIN THEORY
  \section{...} or \subsection{...}   ← always opens with \newpage
  ... algorithm / figures / derivations / failure modes ...

BLOCK 3 — STUDENT ACTIVATION
  \newpage
  \section{Examples \& Exercises}   ← see §13 for the standard exercise pattern
  \section{Self-Reflection and Recap}
    ← reflection questions → recap bullets → chapter-end bridge
```

### Block boundary banner
Mandatory between every block:
```latex
% ==============================================================================================
% BLOCK 1: INTRODUCTION
% ==============================================================================================
```
Use the `=` character (ASCII), not the box-drawing `═`. Same banner before BLOCK 2 and BLOCK 3.

### Sectioning model — pick one
- **Ch03 model (subsection-heavy)**: only `\section{The Why}` is a section; everything else is `\subsection`. Used when the chapter is one cohesive method with stages.
- **Ch04 model (hybrid)**: `\section{The Why}` + `\subsection{Hands-On Experience}`; Block 2 uses `\subsection`s for major theory; Block 3 uses `\section{Examples \& Exercises}` and `\section{Self-Reflection and Recap}`. **This is the default for new chapters.**
- **Ch05 model (section-heavy)**: every major theory unit is its own `\section`. Use only when there are 3+ competing methods (PCA / ICA / t-SNE / UMAP) that each warrant top-level treatment.

### `\newpage` placement
- Between BLOCK 1 → BLOCK 2 (mandatory).
- Between BLOCK 2 → BLOCK 3 (mandatory).
- Inside BLOCK 2 before any major theory unit that needs a clean page (e.g. before a long algorithm or a new method).
- Typical chapter has 5–7 `\newpage`s.

---

## 4. The Why — layered pattern

Block 1's `\section{The Why}` is **never** just two paragraphs and a bullet list. It is a layered build-up. The pattern (4–6 `\newthought` paragraphs) is:

1. **Opening marginnote with a concrete example** (preferred but not mandatory). E.g.:
   ```latex
   \marginnote{\newthought{MNIST handwritten digits}\cite{LeCun1998}, for example,
   live in $\mathbb{R}^{784}$ ($28{\times}28$ pixels), but vary along a handful
   of latent factors. The intrinsic dimensionality is estimated at $k \approx 12$ to $14$.}
   ```

2. **Connection-to-prior paragraph** (`\newthought{...}`): "The clustering algorithms we have seen so far…", "In the previous chapter…", "PCA gave us a first answer…". This is the explicit hand-off from the previous chapter's outcome or limitation.

3. **Phenomenon paragraph** (`\newthought{...}`): names the broader fact that motivates this chapter ("Real-world data is high-dimensional", "Labels are expensive", "Models can be confidently wrong").

4. **Cost / limitation paragraphs** (each its own `\newthought{...}`, **3–4 of them**): each one names a single dimension of why the status quo hurts. Examples from ch05:
   - "Dimensionality has a price" → distance contrast collapses
   - "Computational cost" → $O(nd)$, $O(d^2)$, $O(d^3)$
   - "Expressiveness of the feature space" → features are correlated, redundant
   - "Interpretability" → humans don't reason in high dims

5. **New-mechanism paragraph** (`\newthought{...}`): a single direct sentence introducing what the new method does differently ("No centroid required", "A well-chosen mapping disentangles factors", "Self-supervised learning closes this gap by extracting supervision from the data itself").

6. **The "in order to move from X to Y" roadmap**:
   ```latex
   \newthought{In order to move from <prior state> to <new state>} we have good reason to find ways to,
   \begin{itemize}
       \item <first concrete capability>.
       \item <second concrete capability>.
       \item <third concrete capability>.
   \end{itemize}
   ```
   This is the canonical bullet list. **Identical structural recipe in all chapters** (ch03 l.107, ch04 l.65, ch05 l.54, ch06 l.96, ch07 l.25, ch08 l.27).

7. **Optional `\newthought{The fundamental question}` paragraph**: present in ch01, ch02, ch03, ch06; absent in ch04, ch05. When present, frames the chapter's central question one more time before the Hands-On (e.g. "The fundamental question this chapter answers is how do we find the clusters mathematically?").

A "Why" of two newthought paragraphs is **insufficient**.

---

## 5. The Hands-On Experience — layered pattern

`\subsection{Hands On Experience}` (no hyphen majority; ch03/ch05/ch06 use the hyphenated form, both acceptable). The structure is:

1. **"Consider" opener** (`\newthought{Consider}` …): describes the data scenario, often using or varying the canonical six points. Single paragraph.

2. **Body figure** (`\begin{figure}` not `marginfigure`): full-width pgfplots scatter showing the data without labels or with neutral labels. Use `tick style={black, thick}` (intro figure convention).

3. **Open-question marginnote** (or aside): pose the questions the student should think about. Often itemize:
   ```latex
   \marginnote{
   \begin{itemize}
       \item If you had to keep only one of the two features, which would you choose?
       \item How much information would you lose?
       \item Could you recover the two clusters from that single feature alone?
   \end{itemize}}
   ```

4. **Guiding paragraph** (`\newthought{...}`): nudges intuition without giving the answer. "How many clusters do you see?", "Which points lie in dense neighbourhoods?". 

5. **Negative-framing paragraph** (`\newthought{Our approaches so far would refuse...}` or `\newthought{Without labels, pattern is ambiguous...}`): names what the previous methods would do here, and why that is unsatisfying.

6. **Positive-framing paragraph** (`\newthought{Density allows us to do so}`, `\newthought{Self-supervised learning closes this gap}`): introduces what the new method allows.

7. **Supporting marginfigure** (often): visualizes the new method's signature operation (e.g. ε-circles around each point in ch04, latent-space scatter in ch06). This is where the audit's **Pattern B** (parametric circles) typically appears.

8. **Optional broader-concept marginnote**: connects the chapter's theme to a bigger idea (e.g. "Hand-crafted feature engineering is dimensionality reduction by another name"; "Pareidoly is the tendency to perceive meaningful patterns…").

9. **Learning Objectives close**:
   ```latex
   \newthought{The Learning Objectives} of this lecture:
   \begin{itemize}
       \item Understand <core mechanism>.
       \item Apply <method>...
       \item Identify <failure modes / when to use what>.
   \end{itemize}
   ```
   Always **3 bullets**, verb-led.

A Hands-On of "figure + question + objectives" is **insufficient**. Add the negative/positive framing and the supporting marginfigure.

---

## 5b. Block 2 — narrative-arc archetypes

Block 2 is **not a list of methods**; it tells a story. Two archetypes recur across the established chapters; pick one when planning a chapter.

### Archetype A: introduce-then-upgrade (ch03, ch04, ch06)

```
Foundation (definitions + canonical algorithm)
   ↓ "Notice that X is the only design choice."
Upgrade motivation (the foundation works, but...)
   ↓
Upgrade / hyperparameter beat (variants of the upgrade, or hyperparameter selection)
   ↓ "When [method] struggles..." failure-mode framing as its own beat with heading
Failures (named, with figures)
   ↓
Extensions (the engineering rescues / "Beyond [method]")
   ↓
Output reading / Use payoff (interpretation, generation, inference)
```

Used in: ch03 (Algorithm → Linkages → Failures → Complexity → Reading dendrograms → Inference), ch04 (Algorithm → Hyperparameters → Failures → OPTICS/HDBSCAN → Curse), ch06 (AE → Upgrade motivation → VAE → Variants → Reparameterisation → Bottleneck → Latent space).

### Archetype B: competition (ch05)

```
Naive baseline (deliberately weak; the pedagogical anchor)
   ↓ "When does it fail? When the signal does not align with the axis."
First principled method (linear)
   ↓ "There is a dual view that asks the opposite question."
Variant of first method (same family, fixes a named weakness)
   ↓ "X is linear. No rotation of the axes can untangle..."
Nonlinear pivot (different paradigm, fixes the dimension that was beyond reach)
   ↓ "Cluster sizes and distances are meaningless; use for visualization only."
Modern variant (production-ready successor)
```

Used in: ch05 (Variance-selection → PCA → Reconstruction-error dual → ICA → t-SNE → UMAP).

### Connective tissue rules

- Every section transition is a **single bridge sentence** that names the weakness the next section fixes. Pattern: "[Last sentence of section N stating a limitation]. → [First newthought of section N+1 announcing the response]."
- The bridge sentence pair must be **explicit**, not implicit. Do not start a section with a bare definition; start with a sentence that ties it to the prior beat.
- Every chapter should contain at least one **failure-mode beat with its own heading** ("When X Fails", "Failure modes of Y"). Failures are never asides.
- Every algorithm box is followed by a `\newthought{Notice that ...}` reflective callback that highlights the one design choice the reader must own.

### Recurring rhetorical / pedagogical moves (cross-chapter checklist)

1. **Trace through the canonical six (or seven) points** as a worked storyboard — a figure per step. The same coordinates recur across chapters as a visual anchor.
2. **"Notice that X" reflective callback** after every algorithm.
3. **Failure-mode framing as its own beat** with a heading.
4. **Extension framing** ("Beyond [method]" / "OPTICS / HDBSCAN") — always after failures, never before.
5. **Cross-chapter callbacks** ("Compare with chapter X", "PCA and ICA are linear, so...").
6. **Comparison-with-prior-method paragraphs** ("This stands in sharp contrast to K-Means").
7. **Analogy / metaphor anchors** ("no centroid required", "the points have not moved apart; the space has grown underneath them", "spreading mass costs more than translating it").
8. **Recipe / "practical protocol" boxes** ($k$-distance plot, scree plot, "A practical protocol for choosing $k$").
9. **The dual-view derivation**: "There is a dual view that asks the opposite question" (variance vs reconstruction in ch05; encoder distribution vs aggregate posterior in ch06).
10. **Hyperparameter as bridge**: a single hyperparameter ($L$, $\varepsilon$, $k$, $\beta$) organises a whole section.
11. **The "spoiler" mid-derivation**: "Spoiler. We can't" (used sparingly to acknowledge an impasse before resolving it).
12. **Use-payoff climax**: end Block 2 on a beat that demonstrates the method *does something* (interpolation, generation, sampling, decision-making) — not on a failure mode or a definition.

---

## 6. Text & Paragraph Conventions

### `\newthought{}`
- Used at the start of every new conceptual unit (replaces section breaks within body text)
- The argument is a short bold phrase (2–5 words); the sentence continues after `}` without a capital
- Examples: `\newthought{A distance function}`, `\newthought{The algorithm alternates between two steps}`
- **Never omit `\newthought` at the start of a new paragraph that introduces a new idea**

### Narrative voice
- First-person plural ("we"), direct and collegial
- Concrete examples before abstract definitions
- Rhetorical questions to guide the reader

### Spacing
- `\vspace{2.5em}` between major topic transitions within a section (8× per chapter typical)
- `\vspace{1.5em}` for minor transitions, before an algorithm, after a math display
- `\vspace{0.5em}` micro-breath between question-style `\newthought` and the next paragraph (esp. exercises)

### Inline math spacing
- Use `{=}` inside inline math to suppress the extra spacing around `=`: `$K{=}2$`, `$\mu_1{=}(0,3)$`
- Use `\,` for thin space in coordinate pairs: `$(2,\,1)$`
- Inline approx with no spacing: `$d(x_1,x_2){=}\sqrt{2}{\approx}1.41$`

### Forbidden in prose
- **No `\textbf`, `\textit`, or `\emph` for emphasis or term introduction.** Use `\newthought` to mark conceptual openers; everything else is plain prose.
- **No em/en-dashes (`---`, `--`, `\textemdash{}`) in prose.** Use commas, semicolons, colons, or split into two sentences. `--` is allowed only for numeric ranges (e.g., `1--5`).
- **No parenthetical asides for explanations.** Fold explanations into inline clauses, not round brackets.

---

## 7. Mathematics

### `align*` environment
- Every multi-step calculation uses `align*`
- **Each `=` sign starts on its own line** — never chain `a = b = c` on one line; even short evaluations like `= 1 + 4 = 5` must be split into two `&=` lines
- Use `&=` for alignment; the LHS appears only once (first line)
- Vertical spacing between groups: `\\[4pt]` or `\\[6pt]`
- Canonical pattern:
  ```latex
  \begin{align*}
      d(x_1,\,x_2) &= \sqrt{(3-1)^2 + (1-1)^2} \\
                   &= \sqrt{4 + 0} \\
                   &= 2
  \end{align*}
  ```

### Fractions
- Use `\tfrac` (text-size fraction) inside `align*` and inline math for compactness
- Use `\frac` only in displayed equations that stand alone

### Notation
- Data points: $x_i$ (not A, B, C — those clash with cluster labels $C_k$)
- Vectors: bold or indexed, e.g. $x_i$
- Centroids: $\mu_k$ (open circle in figures); $\mu_k'$ for updated centroids
- Cluster: $C_k$; assignment: $c_i \leftarrow \arg\min_k$
- Inertia: $J$ (within-cluster sum of squares)
- Squared distance: $d^2(\cdot, \mu_k)$ in assignment tables/calculations
- Hard brace in subscripts: `{=}` for inline spacing

### Equations vs align*
- Numbered `\begin{align}...\label{eq:...}\end{align}` only for equations referenced later in the text
- All worked calculations use unnumbered `align*`
- **Do not use `\begin{equation}` even for labelled single-line equations**; use `align` with one row, so the convention is uniform across chapters

---

## 8. Margin Content

Tufte margins carry two types of content.

### `\marginnote{}` — content categories
- **Worked examples**: step-by-step calculations mirroring a body formula; placed immediately after the formula
- **Conceptual asides**: short clarifications, intuitions, caveats (introduced with `\newthought{}` inside the note)
- **Notation explanations**: e.g. "On ' notation. The prime symbol (') usually denotes updates…"
- **Callbacks**: `\marginnote{\newthought{Contrast with K-Means.} ...}` — explicit pointer to a previous chapter
- **Definition asides**: short formal definition that did not earn body space
- `align*` environments inside `\marginnote` are fine and encouraged; always close with `\end{align*}%` (the `%` prevents whitespace)
- When combining text and a calculation, put the text first, then the align
- **Vertical offset**: `\marginnote[-Xem]{...}` shifts a note upward, e.g. `\marginnote[-6em]{...}`

### Mandatory `\newthought` opener
**Every `\marginnote` must open with `\newthought{...}`.** Never write `\marginnote{Plain sentence here.}`.

### Recurring marginnote phrasings (verbatim)
- `\marginnote{\newthought{Code} will be provided as a Python notebook. Use it as a starting point, break things, and observe what changes.}` — opens the code exercise in every chapter
- `\marginnote{\newthought{Teaser.}}` — placed before the chapter-end bridge prose
- `\marginnote{\newthought{feedback}}` — empty placeholder, sits at end of file (mark for the author)
- `\marginnote{\newthought{Contrast with X.}}` — recurring callback

### `\marginfigure`
- Used for small supplementary figures
- Width: `\marginparwidth`, height: `\marginparwidth` (square) or `0.5\marginparwidth` (landscape)
- Tick labels: `font=\tiny`; node labels: `font=\tiny`
- Sparse ticks: 3–4 values matching the data range
- Always has `\caption{}` and `\label{fig:...}`

---

## 9. Figures (main body)

### Figure environments
- Use `\begin{figure}` (not `figure*`) for body figures
- Use `\begin{marginfigure}` for margin-width figures
- All figures have `\caption{}` and `\label{fig:...}`
- Caption style: concise, factual, references variable names from the body
- Caption titling pattern (ch03/ch04 hallmark): begin captions with embedded `\newthought{Step name}`, e.g. `\caption{\newthought{Visit $x_1$}: ...}`

### Figure sizing
- Main body figures: `width=0.5\textwidth, height=0.5\textwidth` (square)
- Failure-mode / comparison figures: `height=0.4\textwidth` (uniform across a row)
- Margin figures: `width=\marginparwidth, height=\marginparwidth`
- Wide architecture figures: `width=0.8\textwidth` if necessary

### pgfplots axes — standard preamble (Pattern A)
```latex
\begin{axis}[
    xlabel={$x^{(1)}$}, ylabel={$x^{(2)}$},
    xmin=0, xmax=10, ymin=0, ymax=10,
    width=0.5\textwidth, height=0.5\textwidth,
    axis line style={draw=none},
    tick style={black, thin},      % thin for theory, thick for hands-on intro
    xtick={2,4,6,8}, ytick={2,4,6,8},
    xticklabel style={font=\small},
    yticklabel style={font=\small},
    tick align=outside, tick pos=left,
]
\addplot[only marks, mark=*, mark size=2pt, black] coordinates {(1,2)(2,3)(3,1)};
\addplot[only marks, mark=*, mark size=2pt, black!55] coordinates {(6,8)(8,7)(8,9)};
\node[font=\small, anchor=north west] at (axis cs:1,2) {$x_1$};
```
Margin variant: replace width/height with `\marginparwidth`, font=\tiny everywhere.

### Pattern B: parametric circle in axis coordinates (ch04 hallmark)
```latex
\addplot[black!35, dashed, thin, domain=0:360, samples=60]
    ({1 + 2.5*cos(x)}, {2 + 2.5*sin(x)});
```
Canonical way to draw an ε-neighbourhood, decision boundary contour, or covariance ellipse inside a pgfplots axis. Adapt by swapping center `(cx, cy)`, radius `r`, and color.

### Pattern C: dendrogram on true scale (ch03)
```latex
\begin{axis}[
    xmin=-1.8, xmax=5.5, ymin=-0.7, ymax=7.5,
    width=\marginparwidth, height=1.8\marginparwidth,  % portrait
    axis line style={draw=none},
    tick style={black, thin},
    xtick=\empty,
    ytick={1.41, 2.24, 6.40},
    yticklabels={$1.41$, $2.24$, $6.40$},
    yticklabel style={font=\tiny},
    tick align=outside, tick pos=left,
]
\draw[thick] (axis cs:0,0) -- (axis cs:0,1.41) -- (axis cs:1,1.41) -- (axis cs:1,0);
\draw[densely dashed, black!60] (axis cs:-1.5,4.3) -- (axis cs:5.3,4.3);  % cut line
```
Heights are **literal data values**. Each merge is one orthogonal `up-across-down` polyline. Reusable for any tree-on-true-scale (e.g. uncertainty calibration trees, decision boundaries).

### Pattern D: elbow plot with broken line and open/filled markers (ch03 + ch04)
```latex
\addplot[only marks, mark=o, mark size=2pt, black] coordinates {(6,2.24)};  % elbow OPEN
\addplot[only marks, mark=*, mark size=2pt, black] coordinates {
    (1,1.41) (2,1.41) (3,2.00) (4,2.00) (5,2.24) (7,3.61)};
% Manually segmented line — gaps around markers
\draw[black, thin] (axis cs:1.18,1.41) -- (axis cs:1.82,1.41);
\draw[black, thin] (axis cs:2.18,1.48) -- (axis cs:2.82,1.90);
\draw[densely dashed, black!60] (axis cs:0.5,2.5) -- (axis cs:7.5,2.5);   % cut
\node[font=\small, anchor=north west] at (axis cs:0.55,3.7) {$\varepsilon{=}2.5$};
```
The line is **manually segmented** with start/end coordinates leaving 0.18-unit gaps around markers. Reuse for ROC curves, threshold sweeps, learning curves.

### Pattern E: PCA-style projection with dashed error to projection line (ch05)
```latex
\addplot[only marks, mark=*, mark size=2pt, black] coordinates { ... };       % data
\addplot[only marks, mark=o, mark size=2pt, black, thick] coordinates { ... }; % reconstructions
\draw[black, thin, dashed] (axis cs:-2.5,-3.1)--(axis cs:-2.8,-2.8);            % per-point error
\draw[-{Stealth[length=4pt,width=2.5pt]}, black!50, semithick]
    (axis cs:0,0) -- (axis cs:2.1,2.1);                                          % direction arrow
\node[font=\small, black!50, anchor=north west] at (axis cs:1.8,1.6) {$w_1$};
```
Stealth-tipped arrows for principal directions / learned directions. Reuse for any "projection + error" or "direction in feature space" figure.

### Pattern F: triple-curve loss plot (ch06 bottleneck figures)
```latex
\addplot[black, thick] {3.5*exp(-0.08*x) + 0.4};                                % L_R solid
\node[font=\footnotesize, anchor=west, xshift=4pt] at (axis cs:68,0.42) {$\mathcal{L}_R$};
\addplot[black!55, thick, densely dashed] {2.0*(1 - exp(-0.08*x))};             % L_KL dashed
\node[font=\footnotesize, black!55, anchor=west, xshift=4pt] at (axis cs:68,1.99) {$\mathcal{L}_{\text{KL}}$};
\addplot[black, thick, densely dotted] {1.5*exp(-0.08*x) + 2.4};                % L_total dotted
\addplot[only marks, mark=o, mark size=3pt, thick, black] coordinates {(32, 2.52)};  % sweet spot
```
Three curves (solid / dashed / dotted) with inline node labels at right edge, plus an open-circle marker at the key point. Reuse for any "two opposing forces and their sum" plot (precision vs recall, bias vs variance, etc.).

### Pattern G: architecture diagram with forward + gradient arrows (ch06)
```latex
\begin{tikzpicture}[
    every node/.style={font=\small, align=center},
    block/.style={rectangle, draw=black, thick, rounded corners=2pt,
                  minimum width=2.4cm, minimum height=0.7cm, inner sep=4pt},
    arr/.style={-{Triangle[length=4pt, width=4pt, fill=black!70]}, thick, black!70},
    gradarr/.style={-{Triangle[length=4pt, width=4pt, fill=black!30]}, thick, black!30, densely dashed},
]
    \node[block] (input) {$x \in \mathbb{R}^d$};
    \node[block, below=24pt of input, fill=black!8] (hidden) {$z \in \mathbb{R}^k$};
    \draw[arr]     (input.south) -- node[left, font=\tiny] {$\theta_E$} (hidden.north);
    \draw[gradarr] ([xshift=10pt]hidden.north) -- ([xshift=10pt]input.south);
\end{tikzpicture}
```
Solid arrows (`arr`) on the left side label the forward pass with `$\theta$`; dashed arrows (`gradarr`) on the right side show gradient flow. Reuse for any train-loop figure (uncertainty: posterior over weights → predictions; SSL: encoder → projector → loss).

### Pattern H: distribution overlay (ch06 KL penalty)
```latex
\addplot[black, thick] {exp(-x^2/2) / sqrt(2*pi)};                       % prior solid
\node[font=\tiny, anchor=south east] at (axis cs:-0.8,0.35) {$p(z)$};
\addplot[black!55, thick, densely dashed] {exp(-(x-2)^2/2) / sqrt(2*pi)}; % shifted
\node[font=\tiny, black!55, anchor=south west] at (axis cs:3.2,0.25) {$q_1$};
\addplot[black!55, thick, densely dotted] {exp(-x^2/8) / sqrt(2*pi*4)};   % widened
\node[font=\tiny, black!55, anchor=south] at (axis cs:-2.5,0.12) {$q_2$};
```
Three Gaussians (or any three distributions) with inline node labels. Reuse for: aleatoric vs epistemic uncertainty, energy vs softmax distributions on in/out-of-distribution data, contrastive loss temperature effect.

### Multi-axis comparison panels
For side-by-side panels (anomaly types, augmentation comparison, embedding spaces):
```latex
\begin{axis}[name=panel1, ...]  % first panel
    ...
\end{axis}
\begin{axis}[at={(panel1.east)}, anchor=west, xshift=0.5cm, name=panel2, ...]
    ...
\end{axis}
```
Use `title={...}` on each axis to label the panels. Use `xtick=\empty, ytick=\empty` if axes are noise.

---

## 10. Color Palette (canonical)

| Color | Use |
|---|---|
| `black` | Primary cluster A; focused / foreground points; principal data |
| `black!55` | Secondary cluster B; greyer points; alternative curve in dual plot |
| `black!30` | Tertiary / dimmed points; bridge points; noise candidates; background data |
| `black!8` | Fill for highlighted block in architecture diagram (e.g. latent layer `z`) |
| `black!25` | Dotted distance edges; prior circles (large, dashed) |
| `black!35` | Past-merge solid edges; sometimes ε-circle outlines |
| `black!40` | Encoder-distribution circles (small, dotted) |
| `black!60` | Dashed cut lines (cluster cut, threshold) |
| `black!70` | Forward-pass arrows in architecture diagrams |

Centroids: `mark=o, mark size=2pt, black, thick` (open circle), never `*`.
Noise points: `mark=x, thick` (only place `mark=x` appears).
Forward arrows: `arr` style with black!70 fill.
Gradient arrows: `gradarr` style with black!30 dashed.

---

## 11. Tables

- All tables use `booktabs`: `\toprule`, `\midrule`, `\bottomrule`; **no vertical rules**
- **Environment**: `\begin{table*}[ht]` — spans full page width to avoid overflow in tufte layout
- **Column format**: explicit `p{X\textwidth}` widths for every column (not `l`, `r`, `c`)
- **Header cells**: wrapped in `\textbf{...}` (this is the only acceptable use of `\textbf` in the body)
- `\vspace{2em}` between `\end{tabular}` and `\caption`
- Template:
  ```latex
  \begin{table*}[ht]
  \centering
  \begin{tabular}{p{0.10\textwidth}p{0.18\textwidth}p{0.18\textwidth}p{0.10\textwidth}}
      \toprule
      \textbf{Col1} & \textbf{Col2} & \textbf{Col3} & \textbf{Col4} \\
      \midrule
      ... rows ...
      \bottomrule
  \end{tabular}
  \vspace{2em}
  \caption{...}
  \label{tab:...}
  \end{table*}
  ```
- Bold minimum values in distance tables: `$\mathbf{value}$` in the column with the smallest distance per row
- Caption explains what bold values mean
- Variance / reconstruction summary tables include a `\midrule` before a **Total** row

---

## 12. Algorithms

- Use `\begin{algorithm}[H]` with `\begin{algorithmic}[1]` (line numbers)
- `\caption{}` on the algorithm float
- `\Require` / `\Ensure` for inputs/outputs
- `\Repeat ... \Until{condition}` for iterative loops
- `\State \textbf{Step name:}` for named steps within the loop
- `\Comment{...}` for inline comments (rare; only when essential)
- **Always preceded** by a `\newthought{...}` paragraph that motivates the algorithm in prose, plus `\vspace{1.5em}` separator
- **Always followed** by a `\newthought{Notice that ...}` or `\newthought{Termination ...}` paragraph reflecting on a property

---

## 13. Examples & Exercises Section Structure

`\section{Examples \& Exercises}\index{examples}\index{exercises}` opens with the canonical encouragement marginnote:
```latex
\marginnote{\newthought{Exercises} are for practice and reinforcing concepts. Try to solve them on your own first,
try things, play with it, discuss, this is not a time trial. And there is no shame in not ending up at the right answer,
in the same sense, that uncovering great questions
and tossing them around is usually pretty fruitful on the long run.}
```

### Standard exercise template (every chapter has this as Exercise 1)

```
\newthought{Computing by hand} builds the intuition that no <method> can replace.
Step through the arithmetic slowly.

\vspace{1em}

\begin{marginfigure}
    ... margin scatter showing the data setup ...
\end{marginfigure}

\newthought{Given <points>, <constants>}, <task>.
Your tasks: <task 1>, <task 2>, <task 3>.

\vspace{0.5em}

\newthought{<First step name>.} For each <thing> compute <quantity>.
Here is the full calculation for <one entry>:

\begin{align*}
    <first quantity> &= <step 1> \\
                     &= <step 2> \\
                     &= <step 3>
\end{align*}

Compute the remaining <entries> yourself, then verify against the table below.

\begin{table*}[ht]
    ... full table of all values, bold minimums, with caption ...
\end{table*}
```

### Sequence of exercises (6–10 worked items)

1. **Opening worked numerical**: full derivation for one entry + student completes the rest + table verification (always present)
2. **Verification subexercise**: a short follow-up computing one more value to confirm a label (often)
3. **Extension exercise**: introduces a new datum (a border point, a new dimension, a different parameter) and asks the student to re-classify
4. **Conceptual reasoning**: itemize-style questions exploring edge cases or asymmetries; margin-note answer at the end
5. **Multi-part build-up**: combines 2–3 sub-questions tracking a multi-step computation (a chain of distance comparisons, a parameter sweep)
6. **Comparison-with-prior-method**: re-runs an earlier method on the new data, with a worked numerical contrast (e.g. "K-Means baseline result"); often references a body figure for visual contrast
7. **Diagnostic / pattern-recognition exercise**: gives several scenarios or numerical patterns and asks the student to identify what is happening (which method is overfitting, which encoder has collapsed)
8. **Back-of-envelope**: short numerical exercise checking scaling, complexity, or a property
9. **Code section** (always last):
   ```latex
   \marginnote{\newthought{Code} will be provided as a Python notebook.
   Use it as a starting point, break things, and observe what changes.}
   \marginnote{<dataset spec, line-broken>\\<format details>\\[4pt]implement: <list>}

   \newthought{A <domain> dataset to explore.} <2–4 sentence task description>.

   \newthought{What to observe.} <2–4 sentence expected findings discussion>.
   ```

Each exercise opens with `\newthought{Exercise title.}` (period included). Use `\vspace{2.5em}` between exercises.

### Margin notes inside exercises
- Margin scatter figures (small) for data setup
- Margin sketches as answers to conceptual questions: `\marginnote{\newthought{Sketch.} <answer>}`
- Margin commentary on subtle points: `\marginnote{\newthought{Why the asymmetry.} ...}`
- One margin-note per exercise minimum

A Block 3 of fewer than 4 worked items with no table verification and no code-section is **insufficient**. Target 6–10.

---

## 14. Self-Reflection and Recap

```latex
\section{Self-Reflection and Recap}\index{reflection}\index{recap}

\newthought{Self-Reflection} questions to guide your thinking:
\begin{itemize}
    \item ...
\end{itemize}

\newthought{Recap} of Key Concepts:
\begin{itemize}
    \item ...
\end{itemize}
```

### Self-Reflection itemize
- **6–9 questions** (audit: ch03=6, ch04=7, ch05=8, ch06=8, ch07=7, ch08=7)
- Always `\begin{itemize}`, never `\begin{enumerate}`
- Graduate from recall → application → synthesis
- At least one question names a specific failure mode or variant from the chapter
- At least one question sets up the conceptual need that the next chapter addresses
- **Mirror principle**: every major theory `\newthought` in Block 2 should produce at least one self-reflection question

### Recap itemize
- **5–8 items** (audit: ch03=7, ch04=8, ch05=5, ch06=7, ch07=5, ch08=5)
- Each item is specific, not generic: names the method, the mechanism, and the condition
- Cover: objective/algorithm, optimality trade-off, evaluation heuristics, failure modes, variants
- **Mirror principle**: every major theory section should produce at least one recap bullet

---

## 15. Chapter-End Bridge

After Recap, the bridge follows a four-part pattern:

```latex
\marginnote{\newthought{<Root cause name>.} <One sentence stating the fundamental limit of every method in this chapter>.}

\newthought{<Concrete failure paragraph>.} <Names the shared problem with a tangible example
that makes the limitation real, e.g. "A fraud detector trained on last year's patterns will keep
waving through this year's novel scheme until enough damage accumulates...">

\newthought{<Pivot paragraph>.} <Introduces what the next chapter does differently, framed as the
direct answer to the failure named above. E.g. "Self-supervised learning addresses this brittleness
from the other direction. Instead of modelling what is normal, it learns representations directly
from the structure of the data...">

\marginnote{\newthought{Teaser.} <One-sentence question previewing the next chapter's mystery>.}

\newthought{<Forward-look sentence>.} <One sentence on a secondary follow-on topic or what comes after the next chapter>.

\marginnote{\newthought{feedback}}
```

The Teaser marginnote is **mandatory** and goes inline with the bridge prose, not at the very end. The trailing `\marginnote{\newthought{feedback}}` placeholder always appears as the last line of the file (the author uses these to mark sections to revisit).

The bridge must come from the **failure modes actually shown in the chapter** — not a generic "the next chapter covers X."

---

## 16. Running Example (canonical data)

The **six intro points** appear in every chapter as the worked example:

| Label | Coordinates |
|-------|-------------|
| $x_1$ | $(1, 2)$ |
| $x_2$ | $(2, 3)$ |
| $x_3$ | $(3, 1)$ |
| $x_4$ | $(6, 8)$ |
| $x_5$ | $(8, 7)$ |
| $x_6$ | $(8, 9)$ |

- Two natural clusters: $\{x_1, x_2, x_3\}$ (bottom-left, `black`) and $\{x_4, x_5, x_6\}$ (top-right, `black!55`)
- **Do not use A, B, C labels** — these clash with cluster labels $C_1, C_2$
- Variations: ch04 adds $x_7{=}(4,5)$ as bridge point (`black!30`); ch05 repositions so $x^{(1)}$ is degenerate; ch07 uses an anomaly-detection variant (10 cluster + 3 outliers); ch08 uses the points unchanged for a contrastive-pair intuition

### Chapter 2 exercise baseline (K-Means trace)
- 3 points: $x_1{=}(1,1)$, $x_2{=}(3,1)$, $x_3{=}(8,7)$; $K{=}2$
- Initial centroids: $\mu_1{=}(0,3)$, $\mu_2{=}(6,5)$
- Updated centroids: $\mu_1'{=}(2,1)$, $\mu_2'{=}(8,7)$
- Inertia at convergence: $J{=}2$; $K{=}1$: $J{=}50$; $K{=}3$: $J{=}0$

---

## 17. Failure-Mode Figures

When showing cases where an algorithm fails:
- Precede each figure with `\marginnote{\newthought{Failure mode name}}` to label it
- Each figure has `height=0.4\textwidth` for uniform vertical space
- The centroid (`mark=o`) is always shown to illustrate where the algorithm places the mean
- After the figures, `\newthought{When [algorithm] struggles}` paragraph names the shared root cause

---

## 18. LaTeX Hygiene

- `%` comment after `\end{align*}` inside `\marginnote` to suppress whitespace: `\end{align*}%`
- Never chain `=` signs on one line inside `align*`
- `\marginnote{}` must always be a balanced group — verify before committing
- After edits, build check (PowerShell):
  ```powershell
  cd lecturenotes/notes_unsupervisedlearning
  pdflatex -interaction=nonstopmode notes_unsupervisedlearning.tex 2>&1 | Select-String "^!|Runaway"
  ```
- Run twice to resolve cross-references and citations
- The formatter rewrites the file after saves — always re-read before a second Edit call; use Write or a Python script for replacements when the Edit tool reports stale content
- Avoid loading `tikz` libraries (`calc`, `cref`) that are not in the main preamble; if you need them, add to the main `.tex` first

---

## Quick checklist for a new (or rewritten) chapter

- [ ] Topical noun-phrase title with index entries on the same line
- [ ] Short evocative `\newthought{...}` subtitle immediately after `\chapter{}`
- [ ] BLOCK 1, 2, 3 banner comments with `=` characters
- [ ] Why section: 4–6 layered `\newthought` paragraphs (connection-to-prior, phenomenon, 3 cost dims, new mechanism)
- [ ] "In order to move from X to Y" bullet list closes the Why
- [ ] Optional `\newthought{The fundamental question}` paragraph
- [ ] Hands-On with body figure + open-question marginnote + guiding paragraph + negative/positive framing + supporting marginfigure
- [ ] Learning Objectives = 3 verb-led bullets
- [ ] Block 2 with multiple `\subsection`s (ch04 model), each opening with motivating `\newthought`
- [ ] At least one algorithm preceded by motivating prose and followed by reflection
- [ ] 7–12 body figures + 5–10 marginfigures using the canonical templates
- [ ] Color palette respected (black / !55 / !30 etc.)
- [ ] Tables in `table*[ht]` with booktabs and `p{X\textwidth}` columns
- [ ] Block 3 with exercises encouragement marginnote at start
- [ ] 6–10 worked exercises, opener has full derivation + student completion + table verification
- [ ] Code section with notebook + dataset marginnotes + "What to observe" paragraph
- [ ] Self-Reflection (6–9 itemize questions) mirrors Block 2 sections
- [ ] Recap (5–8 itemize bullets) mirrors Block 2 sections
- [ ] Bridge: marginnote root cause + concrete-failure newthought + pivot newthought + Teaser marginnote + forward-look newthought
- [ ] Trailing `\marginnote{\newthought{feedback}}` placeholder
- [ ] Total length 1300–1550 lines
- [ ] Two `pdflatex` passes clean (no `!` errors, no `Runaway` warnings)
