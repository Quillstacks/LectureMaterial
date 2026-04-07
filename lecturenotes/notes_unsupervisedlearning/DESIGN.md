# Lecture Notes Design Guide
## Unsupervised Learning — Prof. Dr.-Ing. Mark Schutera

This document captures all layout, style, and structural decisions for these lecture notes so that new chapters can be written consistently.

---

## 1. Document Class & Preamble

- **Document class**: custom `tufte` class (`\documentclass{../sharedAssets/tufte}`)
- **Packages**: `amsmath`, `tikz`, `pgfplots` (compat=1.18), `booktabs`, `algorithm`/`algpseudocode`, `enumitem`, `soul`, `textcase`, `pifont`, `float`, `tabularx`
- **Fonts**: `\loadoptionalfonts` (Palatino/Bera/Helvetica stack from tufte class)
- **Index**: `\makeindex` enabled; use `\index{term}` liberally at chapter/section headings and first uses of key terms

---

## 2. Chapter Structure (mandatory pattern)

Every chapter follows three blocks in order:

```
BLOCK 1 — INTRODUCTION
  \section{The Why}          ← motivation, connection to prior chapter's outcome/failure
    \subsection{Hands On Experience}  ← concrete, unlabelled exercise with no answer
  Learning Objectives        ← exactly 3 bullet items, verb-led ("Understand…", "Apply…", "Identify…")

BLOCK 2 — MAIN THEORY
  \section{The [Method Name]}   ← always starts with \newpage
  ... algorithm / figures / derivations / failure modes ...

BLOCK 3 — STUDENT ACTIVATION
  \newpage
  \section{Examples & Exercises}
    ← worked by-hand trace → solution table → student tasks → code exercise
  \section{Self-Reflection and Recap}
    ← reflection questions → recap bullets → chapter-end bridge
```

- Blocks are separated by `% ==============================...==============================` comment banners
- The `Hands On Experience` subsection always poses a visual question with unlabelled data and no answer given
- `\newthought{The Learning Objectives}` ends Block 1, followed immediately by `\newpage` or the Block 2 banner

---

## 3. Text & Paragraph Conventions

### `\newthought{}`
- Used at the start of every new conceptual unit (replaces section breaks within body text)
- The argument is a short bold phrase (2–5 words); the sentence continues after `}` without a capital
- Examples: `\newthought{A distance function}`, `\newthought{The algorithm alternates between two steps}`
- Never omit `\newthought` at the start of a new paragraph that introduces a new idea

### Narrative voice
- First-person plural ("we"), direct and collegial
- Concrete examples before abstract definitions
- Rhetorical questions to guide the reader: "How many clusters do you see?", "Where would you place a representative point?"

### Spacing
- `\vspace{2.5em}` between major topic transitions within a section (not between sections)
- `\vspace{1.5em}` for minor transitions within a topic

### Inline math spacing
- Use `{=}` inside inline math to suppress the extra spacing around `=` that LaTeX adds: `$K{=}2$`, `$\mu_1{=}(0,3)$`
- Use `\,` for thin space in coordinate pairs: $(2,\,1)$

---

## 4. Mathematics

### `align*` environment
- Every multi-step calculation uses `align*`
- **Each `=` sign starts on its own line** — never chain `a = b = c` on one line; this applies even to short chained evaluations like `= 1 + 4 = 5`, which must be split into two `&=` lines
- Use `&=` for alignment; the left-hand side appears only once (first line), subsequent lines are indented with spaces to align with the `&`
- Vertical spacing between groups: `\\[4pt]` or `\\[6pt]`
- Example pattern:
  ```latex
  \begin{align*}
      d^2(x_1,\,\mu_1) &= (1-0)^2 + (1-3)^2 \\
                       &= 1 + 4 \\
                       &= 5
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
- Squared distance: $d^2(\cdot, \mu_k)$ (always squared in assignment tables/calculations)
- Hard brace in subscripts: `{=}` for inline spacing, e.g. `$K{=}2$`, `$\mu_1{=}(2,4)$`

### Equations vs align*
- Numbered `\begin{align}...\label{eq:...}\end{align}` only for equations that are referenced later in the text
- All worked calculations use unnumbered `align*`

---

## 5. Margin Content

Tufte margins carry two types of content:

### `\marginnote{}`
- **Worked examples**: step-by-step calculations that mirror a formula introduced in the body; placed immediately after the formula
- **Conceptual asides**: short clarifications, intuitions, caveats (introduced with `\newthought{}` inside the note)
- **Notation explanations**: e.g. "On ' notation. The prime symbol (') usually denotes updates..."
- `align*` environments inside `\marginnote` are fine and encouraged; always close with `\end{align*}%` (the `%` prevents unwanted whitespace)
- When combining explanatory text with a calculation, put the text first, then the align
- **Vertical offset**: use `\marginnote[-Xem]{...}` to shift a note upward when it should visually align with the content it annotates, e.g. `\marginnote[-6em]{...}`

### `\marginnote{\newthought{feedback}}` — placeholder convention
- Left in the document during editing to mark: "this style/pattern should be saved to the memory MD files"
- When encountered: extract the relevant rule, save it to memory, then delete the placeholder from the source

### `\marginfigure`
- Used for small supplementary figures that don't need full body width
- Width: `\marginparwidth`, height: `\marginparwidth` (square)
- Axis options **one per line** (not cramped inline)
- Tick labels: `font=\tiny`; node labels: `font=\small`
- Sparse ticks: 3–4 values matching the data range (e.g. `{0,3,6,9}` for a 0–9 range)
- Always has `\caption{}` and `\label{fig:...}`
- Centroids use `mark=o, mark size=2pt, black, thick` (same as in body figures)

---

## 6. Figures (main body)

### pgfplots axes — standard settings
```latex
\begin{axis}[
    xlabel={$x^{(1)}$}, ylabel={$x^{(2)}$},
    xmin=0, xmax=N, ymin=0, ymax=N,
    width=0.5\textwidth, height=0.5\textwidth,
    axis line style={draw=none},
    tick style={black, thin},       % thin for body, thick for hands-on intro figures
    xtick={...}, ytick={...},       % only ticks where data actually lies
    xticklabel style={font=\small},
    yticklabel style={font=\small},
    tick align=outside, tick pos=left,
]
```

- **No box around axes**: `axis line style={draw=none}` always
- **Ticks only on left and bottom**: `tick pos=left`
- **Ticks only at data values** (no automatic tick generation); set `xtick` and `ytick` explicitly
- `tick style={black, thick}` in introductory/hands-on figures; `{black, thin}` in theory figures

### Point styles (consistent throughout all chapters)
| Role | Mark | Color |
|------|------|-------|
| Primary / foreground points | `mark=*, mark size=2pt, black` | solid black |
| Secondary / background points | `mark=*, mark size=2pt, black!55` | 55% grey |
| Tertiary / distant points | `mark=*, mark size=2pt, black!30` | 30% grey |
| Centroid / mean (initial or updated) | `mark=o, mark size=2pt, black, thick` | open circle, thick |

### Figure sizing
- Main body figures: `width=0.5\textwidth, height=0.5\textwidth` (square)
- Failure-mode / comparison figures: `height=0.4\textwidth` for uniform vertical space across a row of comparisons
- Margin figures: `width=\marginparwidth, height=\marginparwidth`

### Figure environments
- Use `\begin{figure}` (not `figure*`) for all body figures — content stays in main text column, does not bleed into margin
- Use `\begin{marginfigure}` for margin-width figures
- All figures have `\caption{}` and `\label{fig:...}`
- Caption style: concise, factual, references variable names from the body

### Node labels in figures
- `font=\small` in body figures, `font=\tiny` in margin figures
- Anchor chosen to avoid overlap with the mark: `anchor=south west`, `anchor=north east`, etc.
- Point labels: `$x_1$`, `$x_2$`, ..., `$\mu_1$`, `$C_1$`, etc. (not A, B, C — see Notation section)

### Parametric curves (rings / failure modes)
- `domain=0:360, samples=N` for circles
- Remove `axis equal image` when controlling height explicitly; instead set `ymin`/`ymax` so that `(xmax-xmin)/(ymax-ymin) = width/height` to keep circles circular

---

## 7. Tables

- All tables use `booktabs`: `\toprule`, `\midrule`, `\bottomrule`; no vertical rules
- **Environment**: `\begin{table*}[ht]` — spans full page width (text + margin) to avoid overflow in tufte layout
- **Column format**: explicit `p{X\textwidth}` widths for every column (not `l`, `r`, `c`)
- **Header cells**: wrapped in `\textbf{...}`
- **`\vspace{2em}`** between `\end{tabular}` and `\caption`
- Template:
  ```latex
  \begin{table*}[ht]
  \centering
  \begin{tabular}{p{0.Xwidth}p{0.X\textwidth}...}
      \toprule
      \textbf{Col1} & \textbf{Col2} & ... \\
      \midrule
      ... rows ...
      \bottomrule
  \end{tabular}
  \vspace{2em}
  \caption{...}
  \label{tab:...}
  \end{table*}
  ```
- Bold minimum values in distance tables: `\mathbf{value}` in the column with the smallest distance per row
- Caption explains what bold values mean

---

## 8. Running Example (canonical data)

The **six intro points** appear in every chapter as the worked example:

| Label | Coordinates |
|-------|-------------|
| x_1 | (1, 2) |
| x_2 | (2, 3) |
| x_3 | (3, 1) |
| x_4 | (6, 8) |
| x_5 | (8, 7) |
| x_6 | (8, 9) |

- Two natural clusters: {x_1, x_2, x_3} (bottom-left) and {x_4, x_5, x_6} (top-right)
- In figures: x_1/x_2/x_3 in `black`, x_4/x_5/x_6 in `black!55`
- **Do not use A, B, C labels** — these clash with cluster labels C_1, C_2; use x_i notation throughout

### Chapter 2 exercise baseline (K-Means trace)
- 3 points: x_1=(1,1), x_2=(3,1), x_3=(8,7); K=2
- Initial centroids (non-data points): μ_1=(0,3), μ_2=(6,5)
- Assignment: C_1={x_1, x_2}, C_2={x_3}
- Updated centroids: μ_1'=(2,1), μ_2'=(8,7)
- Inertia at convergence: J=2
- Inertia for K=1: J=50; K=3: J=0

---

## 9. Algorithms

- Use `\begin{algorithm}[H]` with `\begin{algorithmic}[1]` (line numbers)
- `\caption{}` on the algorithm float
- `\Require` / `\Ensure` for inputs/outputs
- `\Repeat ... \Until{condition}` for iterative loops
- `\State \textbf{Step name:}` for named steps within the loop

---

## 10. Failure-Mode Figures

When showing cases where an algorithm fails:
- Precede each figure with `\marginnote{\newthought{Failure mode name}}` to label it
- Each figure has `height=0.4\textwidth` for uniform vertical space
- The centroid (`mark=o`) is always shown to illustrate where the algorithm places the mean
- After the figures, `\newthought{When [algorithm] struggles}` paragraph names the shared root cause

---

## 11. Evaluation Figures (silhouette / box plots)

- Box plot style: whiskers to Q1/Q3 (Tufte style), filled dot at median, open markers at hinges
- Caption reports both **median** and **mean**: e.g. "median ≈ 0.37, mean ≈ 0.30"

---

## 12. Examples & Exercises Section Structure

The `\section{Examples \& Exercises}` follows a fixed sequence:

1. **Opening** (`\newthought{Computing by hand}...`): one sentence motivating hand calculation
2. **Setup figure**: `\begin{marginfigure}` showing the data and initial state
3. **Problem statement** (`\newthought{Given ...}`): specifies points, K, initial centroids, tasks
4. **Step-by-step trace**: one fully worked step (`align*`) for the first item, then "compute the rest yourself"
5. **Solution table**: `table*[ht]` with all values, bold minimum per row
6. **\newpage** before the update step
7. **Update step**: full derivation for one centroid, "derive the other yourself", then solution
8. **Convergence check** + inertia calculation
9. **Elbow/K-selection task**: give the inertia table in a marginnote, ask student to sketch and identify elbow
10. **Optional silhouette** exercise (labelled optional)
11. **Code section**: `\marginnote{\newthought{Code} will be provided...}` + `\newthought{A [domain] dataset to explore.}` + specific tasks + `\newthought{What to observe.}` with expected findings

---

## 13. Self-Reflection and Recap Structure

### Self-Reflection questions
- 7–9 questions
- Graduate from recall → application → synthesis
- At least one question names a specific failure mode or variant from the chapter
- At least one question sets up the conceptual need that the next chapter addresses
- No arbitrary count constraints ("what are your first three steps" → "what would you check")

### Recap bullets
- 4–5 items
- Each is specific, not generic: names the method, the mechanism, and the condition
- Cover: objective/algorithm, convergence/optimality trade-off, evaluation heuristics, failure modes, variants mentioned in the chapter

---

## 14. Chapter-End Bridge

The bridge after the Recap follows this structure:

1. **Marginnote** naming the root cause of the chapter's failure modes in one sentence
2. **`\newthought`** opening naming the shared problem, with a concrete example that makes the limitation tangible
3. **`\newthought`** pivot introducing what the next chapter does differently, framed as the direct answer to the failure
4. One-sentence aside for any secondary next topic (e.g. density-based methods)

The bridge must come from the failure modes actually shown in the chapter — not a generic "the next chapter covers X."

---

## 15. LaTeX Hygiene

- `%` comment after `\end{align*}` inside `\marginnote` to suppress whitespace: `\end{align*}%`
- Never chain `=` signs on one line inside `align*`
- `\marginnote{}` must always be a balanced group — verify with brace counter before committing
- After edits, build check:
  ```bash
  cd lecturenotes/notes_unsupervisedlearning
  pdflatex -interaction=nonstopmode notes_unsupervisedlearning.tex 2>&1 | grep "^!\|Runaway"
  ```
- Run twice to resolve cross-references and citations
- The formatter rewrites the file after saves — always re-read before a second Edit call; use a Python script for replacements when the Edit tool reports stale content
