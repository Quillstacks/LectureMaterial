# AUDIT: Chapters 03, 04, 05 — style and density reference

A structured catalog produced for expansion of ch07 / ch08 to match the established
voice and pedagogical density of these three chapters.

---

## Chapter 03 — Hierarchical Clustering — overview

- Total line count: **1547**
- `\section{...}` calls: **1** (only `The Why`); the rest of Block 2/3 use `\subsection`.
  - `\subsection`: 3 (`Hands-On Experience`, `The Hierarchical Clustering Algorithm`, `Examples & Exercises`)
- `\newthought{...}` calls: **93** (incl. inline opener, theory openers, exercise openers, marginnote openers)
- `\marginnote{...}` calls: **23**
- Body figures (`\begin{figure}`): **12**
- Margin figures (`\begin{marginfigure}`): **10**
- Tables (`\begin{table*}`): **3**; `\begin{table}`: 0
- Algorithms (`\begin{algorithm}[H]`): **1**
- `\begin{align*}`: **24** environments (12 distinct math derivations, exercises ~7)
- `\newpage` calls: **5** (lines 118, 204, 734, 916, 1171)
- Theory vs exercise ratio: theory block ≈ lines 12–1166 ≈ **1155 lines**; Examples & Exercises ≈ lines 1173–1546 ≈ **373 lines** → **theory : exercise ≈ 3.1 : 1**

### Figures inventory (ch03)

Body figures:
- `fig:hc_intro_scatter` (l.130) — pgfplots scatter, six canonical points coloured black/black!55. axis line none, ticks at integers. **Companion:** none direct, sits inside Hands-On.
- `fig:hclust_init` (l.249) — pgfplots scatter, init state. Each point labelled `$x_i, C_i$`, font=\tiny anchor variants per quadrant. No axis lines, ticks={2,4,6,8}. Caption begins with inline `\newthought{Initialization}`.
- `fig:hclust_distances` (l.276) — same axis as init plus 15 dotted `(black!25, dotted, thin)` pairwise edges enumerating $\binom{6}{2}$. The figure is itself the Algorithm-trace storyboard.
- `fig:hclust_merge1` (l.323) — adds `densely dashed (black!55)` for the active merge edge; cluster labels switch to `$x_1, C_m$`.
- `fig:hclust_update1` (l.355) — past merge as `(black!35, thin)`, four new dotted candidate edges; caption ends with embedded `\newthought{Discuss Linkage}`.
- `fig:hclust_merge2` (l.394) — same template, second merge dashed.
- `fig:hclust_merge3` (l.423) — third merge.
- `fig:hclust_merge4` (l.453) — fourth merge.
- `fig:hclust_merge5` (l.484) — fifth merge.
- `fig:hclust_terminate` (l.516) — termination. All labels `$x_i, C_{11}$`.
- `fig:hc_chaining` (l.806) — chaining bridge demonstration: dark, light bridge, grey clusters; intra-cluster solid `(black!35, thin)`, dashed bridge edges `(black!55, densely dashed)`. Has marginnote companion `\newthought{Chaining and bridging}` at l.804.
- `fig:hc_elbow` (l.1012) — line-with-gaps elbow plot. **Filled** `mark=*` for elbow, **open** `mark=o` for others, line segments deliberately broken around each marker (4 short `\draw` segments). xtick={1,2,4,5,6} skips 3 to mark a missing value.
- `fig:hc_exercise_three_scatter` (l.1180) — exercise 3-point scatter (margin), companion to ex 1.
- `fig:hc_chaining_exercise` (l.1359) — exercise 4-point bridge scatter (margin), echoes the body's chaining figure.

Margin figures:
- `fig:why_canonical` (l.34) — six points + all 15 pairwise dashed lines + solid SL hierarchy overlay. Demonstrates "no centroids needed". Uses `width=\marginparwidth`, font=\tiny. **Sits adjacent to the Why text.**
- `fig:linkage_single` (l.583) — six points coloured by cluster (black/black!55/black!30) plus `(black!30, dotted)` nearest-pair edges between every active pair.
- `fig:linkage_complete` (l.633) — same template, dotted edges drawn from furthest members.
- `fig:linkage_average` (l.682) — same template, all 13 cross-cluster pairwise edges dotted.
- `fig:linkage_ward` (l.739) — adds open-circle centroids `mark=o, mark size=2pt, thick`; dotted edges between centroid pairs only.
- `fig:hc_exercise_scatter` (l.917) — clean exercise scatter showing the cut.
- `fig:dendrogram_canonical` (l.958) — **dendrogram on true scale**: stepped `\draw[thick] (x,0)--(x,h)--(x',h)--(x',0)` orthogonal connectors, height ticks `{1.41, 2.24, 6.40}`, dashed cut line `(black!60)`. width=\marginparwidth, height=1.8\marginparwidth (tall portrait).
- `fig:dendrogram_ward` (l.1043) — second dendrogram with same template but variance-based heights `{1.0, 3.0, 96.6}`. Demonstrates Ward's amplified gap.
- (1180) `fig:hc_exercise_three_scatter` (margin variant of exercise 1)
- (1359) `fig:hc_chaining_exercise` margin scatter
- (At l.1180 in marginfigure listing for `_three_scatter` variant) — three-point exercise opener.

Most body figures have NO direct margin-note companion; instead the marginnote precedes the figure with a header phrase (e.g. `\newthought{Chaining and bridging}` at l.804 immediately before fig:hc_chaining).

### Exercises inventory (ch03)

Section starts l.1173 (`\subsection{Examples \& Exercises}`).

1. **"Given three points"** (l.1212) — worked numerical with margin scatter.
   - Type: worked numerical with full $d(x_1,x_2)$ derivation, then student-completes-table.
   - `align*` blocks: 2 (initial distance derivation + first-merge update).
   - Margin: `fig:hc_exercise_three_scatter` + `\marginnote{Reuse by design.}` at l.1220.
   - Length: ~50 lines (l.1212–~1265). Contains 1 `table*` of distances and 1 `table*` of merge history.

2. **"Guaranteed termination"** (l.1299) — conceptual reasoning.
   - `align*`: 0. Uses itemize for $n$-cases.
   - Margin: `\marginnote{\newthought{Contrast with K-Means.}}` at l.1313.
   - Length: ~18 lines.

3. **"Reading the dendrogram"** (l.1330) — student task with margin sketch + leaf-ordering trap.
   - `align*`: 0. Uses itemize for cuts at different heights.
   - Margin: `\marginnote{\newthought{Leaf ordering trap.}}` at l.1324.
   - Length: ~20 lines.

4. **"Linkage comparison with chaining"** (l.1355) — multi-part build-up with bridge point $x_4$.
   - `align*`: 1 (complete-linkage update).
   - Margin: `fig:hc_chaining_exercise` margin scatter.
   - Length: ~70 lines (l.1355–~1425).

5. **"Why single linkage is fast"** (l.1429) — conceptual + numerical follow-up.
   - `align*`: 4 (single-linkage update, Ward update definition, Ward derivation, none more).
   - Margin: `\marginnote{\newthought{SLINK}}` (l.1441) and `\marginnote{\newthought{Shortcut. Lance-Williams}}` (l.1454).
   - Length: ~55 lines (l.1429–~1480).
   - Sub-parts: "Now compare with Ward's update", "Verify the difference", "Back-of-envelope: scalability".

6. **"back at the coffeetable"** (l.1491) — code section.
   - `align*`: 0.
   - Margin: `\marginnote{\newthought{Code} will be provided as a Python notebook.}` at l.1488.
   - Length: ~15 lines (incl. "What to observe" sub-newthought).

### Pedagogical structural elements present (ch03)

- `\newthought{The fundamental question}` paragraph appears **in Block 1 at l.178**:
  > "The fundamental question this chapter answers is how do we formalize the bottom-up merging process? We will see how agglomerative clustering builds a dendrogram from pairwise distances; and how different linkage criteria encode different assumptions about what makes two clusters close."
- `\marginnote{\newthought{Teaser}}` precedes the bridge at l.1536:
  > "How can we define a cluster without any centroid, any linkage criterion, or any choice of $K$, label outliers as noise automatically, and still recover clusters of arbitrary shape?"
- Self-Reflection itemize: **6 items**.
- Recap itemize: **7 items**.
- Chapter subtitle (`\newthought{...}` after `\chapter{...}`): **`Ich springe von Level zu Level zu Level.`** (l.6, German; the only non-English subtitle).

---

## Chapter 04 — Density-Based Clustering — overview

- Total line count: **1361**
- `\section{...}`: **3** (`The Why`, `Examples & Exercises`, `Self-Reflection and Recap`).
  - `\subsection`: 4 (`Hands On Experience`, `The Density-Based Algorithm`, `Hyperparameter Selection`, `When DB Scan Fails`).
- `\newthought{...}` calls: **63**
- `\marginnote{...}` calls: **12**
- Body figures: **12**
- Margin figures: **10**
- Tables (`table*`): **1**; `table`: 0
- Algorithms: **1**
- `\begin{align*}`: **30**
- `\newpage`: **5** (l.82, 203, 301, 753, 1040)
- Theory vs exercise ratio: theory ≈ lines 18–1035 ≈ **1018 lines**; Examples & Exercises ≈ lines 1042–1326 ≈ **285 lines** → **theory : exercise ≈ 3.6 : 1**

### Figures inventory (ch04)

Body figures:
- `fig:dbscan_intro_scatter` (l.87) — pgfplots scatter, 7 canonical points coloured by group (black, black!55, black!30 for $x_7$). Companion to "Consider the same six canonical points".
- `fig:dbscan_trace_start` (l.353) — all-grey unvisited state, opens DBSCAN trace.
- `fig:dbscan_trace_x1` (l.384) — adds dashed $\varepsilon$-circle around $x_1$ via `\addplot[black!35, dashed, thin, domain=0:360, samples=60] ({1 + 2.5*cos(x)}, {2 + 2.5*sin(x)})`. Caption uses `\newthought{Visit $x_1$}` + escaped checkmarks `\checkmark`.
- `fig:dbscan_trace_expand_c1` (l.421) — adds two more dashed circles (one per absorbed neighbour).
- `fig:dbscan_trace_c2` (l.461) — single $\varepsilon$-circle on $x_4$ + dotted distance connectors with $\sqrt{5}$ labels at midpoints.
- `fig:hypothetical_border_x8` (l.512) — adds a hypothetical $x_8$ at $(8,5.5)$ with a dashed circle around it; demonstrates border classification.
- `fig:dbscan_trace_noise` (l.563) — final state with $x_7$ marked `mark=x` (instead of `*`) signalling noise.
- `fig:kdistance_x4` (l.649) — large body version of $\varepsilon$-neighbourhood with dashed connector to nearest neighbour.
- `fig:kdistance_plot` (l.704) — **k-distance elbow**: open elbow marker, filled others, broken line segments (same gap-around-marker style as ch03 elbow), xticklabels are `{$x_1$,$x_2$,$x_5$,$x_6$,$x_3$,$x_4$,$x_7$}` (sorted by $d_k$), dashed horizontal cut at $\varepsilon{=}2.5$ with text label.
- `fig:dbscan_fail_density` (l.765) — varying-density failure: ~15 dashed circles on a tight cluster cluttering visibly + 12 sparse-cluster circles with same $\varepsilon$. Uses `axis equal` (a feature unique to ch04). Marginnote header `\newthought{Varying Density}` at l.763 immediately above.
- `fig:dbscan_fail_bridging` (l.832) — chain of 5 light "bridge" points between two clusters, dashed circles overlapping along chain. Marginnote header `\newthought{Bridging and Chaining}` at l.830.
- `fig:kmeans_baseline` (l.1229) — exercise figure: K-Means with $K{=}2$ forcing $x_7$ into $C_1$, contrast with `fig:dbscan_trace_noise` (referenced explicitly in caption). Has open-circle centroids.

Margin figures:
- `fig:dbscan_intro_circles_unlabeled` (l.26, no label) — opening intuition figure: each point carries its own dashed `circle [radius=1.0]` (TikZ circle, not pgfplots cosines!), with a small grey digit `{4}, {2}, {2}, {2}, {1}` next to each point indicating $|N_\varepsilon|$.
- `fig:dbscan_intro_circles` (l.147) — labelled version with parametric circles `\addplot[black!25, dashed, thin, domain=0:360, samples=40] ({1 + 2.5*cos(x)}, {2 + 2.5*sin(x)})`. **The conversion from `circle [radius]` (TikZ-native) to parametric `\addplot` (pgfplots) is the recurring trick to put circles in axis coordinates.**
- `fig:dbscan_core` (l.220) — pure TikZ (no axis), schematic of a core point with `\fill[black] (0,0) circle (2.5pt)` and four black!55 satellites + the count digit.
- `fig:dbscan_border` (l.252) — schematic with two overlapping dashed circles + count digits 5/3.
- `fig:dbscan_noise` (l.275) — schematic of an empty dashed circle with one grey point.
- `fig:nmin_intuition` (l.613) — three points on a 1D number line with dashed vertical $\varepsilon$ boundaries; aspect ratio `width=\marginparwidth, height=0.5\marginparwidth` (landscape).
- `fig:cod_spacing_1d` (l.937) — 10 points on the unit interval with a small dashed NN-spacing circle.
- `fig:cod_spacing_2d` (l.971) — same 10 points in $[0,1]^2$ with larger dashed NN-spacing circle.
- `fig:dbscan_exercise_scatter` (l.1048) — exercise 7-point scatter (margin).
- `fig:dbscan_exercise_borderpoint` (l.1149) — exercise 8-point scatter (margin) for border-point exercise.

### Exercises inventory (ch04)

Section starts l.1042 (`\section{Examples \& Exercises}`, NOT subsection).

1. **"Given seven points"** (l.1083) — worked numerical with margin scatter + table.
   - `align*`: 1 (full distance derivation $d(x_1,x_2), d(x_1,x_3), d(x_1,x_7)$).
   - Margin: `fig:dbscan_exercise_scatter`.
   - Length: ~45 lines. Contains 1 `table*`.

2. **"Verify $x_7$ is $p_n$"** (l.1133) — worked numerical follow-up.
   - `align*`: 1.
   - Length: ~10 lines.

3. **"Adding a border point"** (l.1144) — student task with margin sketch.
   - `align*`: 0 (purely conceptual/instructional).
   - Margin: `fig:dbscan_exercise_borderpoint`.
   - Length: ~5 lines.

4. **"Density reachability from $x_8$"** (l.1186) — conceptual reasoning.
   - `align*`: 0.
   - Length: ~5 lines.

5. **"Parameter sensitivity"** (l.1192) — student task.
   - `align*`: 0.
   - Length: ~5 lines.

6. **"Building the $k$-distance plot"** (l.1196) — worked numerical with student completion.
   - `align*`: 1 (full $d(x_5,x_4), d(x_5,x_6), d_1(x_5)$).
   - Length: ~15 lines.

7. **"Comparison with K-Means" + "K-Means baseline result"** (l.1211, 1215) — worked numerical with body figure.
   - `align*`: 1 (distance to two centroids).
   - Body figure: `fig:kmeans_baseline`.
   - Length: ~60 lines incl. figure.

8. **"From global to local density"** (l.1277) — worked numerical building OPTICS / HDBSCAN distances.
   - `align*`: 2 ($\varepsilon_c(x_5)$ derivation + the two `d_mreach` definitions).
   - Margin: `\marginnote{The core distance $\varepsilon_c(x_5){=}2.00$...}`.
   - Length: ~25 lines.

9. **"The curse of dimensionality by the numbers"** (l.1299) — back-of-envelope.
   - `align*`: 0.
   - Length: ~6 lines.

10. **"Back at the coffeetable code"** (l.1312) — code section + What to observe.
    - `align*`: 0.
    - Margin: `\marginnote{\newthought{Code} will be provided as a Python notebook.}` at l.1309.
    - Length: ~13 lines.

### Pedagogical structural elements present (ch04)

- `\newthought{The fundamental question}` in Block 1: **NO** — chapter 04 omits this exact paragraph form. Instead the Why section just enumerates pathologies and uses `\newthought{In order to move from pairwise distances to density-aware neighbourhoods}` (l.65) as the bullet-list introducer.
- `\marginnote{\newthought{Teaser.}}` before the bridge: **YES**, l.1356 (after Recap):
  > "The curse of dimensionality breaks every method in this chapter, yet real data rarely uses all its ambient dimensions. Can we find the directions that carry the most signal and build a lower-dimensional representation around them, so that the clustering methods of Part I regain their footing?"
- A second marginnote `\marginnote{\newthought{Feedback.}}` (empty body) appears at l.1357 — recurring placeholder.
- Self-Reflection itemize: **7 items**.
- Recap itemize: **8 items**.
- Chapter subtitle: **`It is all about that space, about that space.`** (l.12, song-lyric riff).

---

## Chapter 05 — Dimensionality Reduction — overview

- Total line count: **1374**
- `\section{...}`: **10** — chapter 05 uses sections heavily, not subsections.
  - `The Why`, `The Curse of Dimensionality, Revisited`, `A Naïve Baseline: Variance-Based Feature Selection`, `Principal Component Analysis`, `Reconstruction Error`, `Independent Component Analysis`, `t-SNE\cite{vanDerMaaten2008}`, `UMAP`, `Examples & Exercises`, `Self-Reflection and Recap`.
  - `\subsection`: 1 (`Hands-On Experience`).
- `\newthought{...}` calls: **80**
- `\marginnote{...}` calls: **21**
- Body figures: **7**
- Margin figures: **5**
- Three additional inline tikzpictures (lines 840, 880, 920) wrapped in `\begin{center}` instead of `figure` — t-SNE timeline diagrams.
- Tables (`table*`): **3**; `table`: 0
- Algorithms: **3** (PCA, t-SNE, UMAP)
- `\begin{align*}`: **52** (heavily math-driven chapter)
- `\newpage`: **7** (l.72, 177, 635, 723, 1024, 1115, 1203)
- Theory vs exercise ratio: theory ≈ lines 12–1019 ≈ **1008 lines**; Examples & Exercises ≈ lines 1026–1328 ≈ **303 lines** → **theory : exercise ≈ 3.3 : 1**

### Figures inventory (ch05)

Body figures:
- `fig:dimred_intro_scatter` (l.78) — pgfplots scatter; six canonical points repositioned so that $x^{(1)}$ varies tiny, $x^{(2)}$ carries spread. Companion margin itemize at l.114 (without `\marginnote` wrapper).
- `fig:naive_projection` (l.300) — diagonal data + open-circle projection onto $x$-axis + per-point dashed error using `\foreach \xa/\ya in {...} {\addplot[black, thin, dashed] ...}`. xmin/xmax `[-4,4]`.
- `fig:pca_projection` (l.357) — PCA projection onto $y{=}x$ line. Uses small individual `\draw[black,thin] (axis cs:-3.1,-2.9)--(axis cs:-2.9,-3.1)` X-tick marks along the projection line plus open-circle reconstructions plus dashed perpendicular error segments. PC1 label as `\node`.
- `fig:pca_eigenvectors` (l.480) — same scatter + two stealth-tipped arrows: `\draw[-{Stealth[length=4pt,width=2.5pt]}, black!50, semithick] (axis cs:0,0) -- (axis cs:2.1,2.1)`.
- `fig:scree_plot` (l.568) — two-point pgfplots, filled markers, single broken line segment between them.
- `fig:cumvar_plot` (l.597) — two-point cumulative variance plot with dashed horizontal `0.95` reference line and inline node label.
- `fig:pca_reconstruction` (l.655) — full reconstruction-error figure with light-grey open reconstructions and per-point dashed error (10 explicit `\draw` commands). Caption explicitly references `Figure~\ref{fig:naive_projection}` for visual contrast.

Margin figures:
- `fig:mnist_eight` (l.131) — `\includegraphics[width=0.5\marginparwidth]{./figures/eight.png}` — only raster image used in any of the three chapters.
- `fig:nn_spacing_curse` (l.186) — pgfplots curve $N^{-1/d}$ for $N{=}100$, plus dashed asymptote at $y{=}1$, in-axis label `$N{=}100$`. Demonstrates pgfplots smooth curve plotting via explicit coordinates list.
- `fig:naive_aligned` (l.266) — flat scatter showing axis-aligned variance.
- `fig:tsne_canonical_ref` (l.798) — full-width canonical reference scatter (uses `width=\textwidth` inside marginfigure for square aspect).
- `fig:pca_exercise_scatter` (l.1037) — exercise 6-point margin scatter, mirrors ch03/04 format.

Inline tikzpictures (no figure env):
- l.840 (`$t{=}0$`), l.880 (`$t{=}2$`), l.920 (`$t{=}100$`) — t-SNE iteration snapshots: 1D number-line embeddings inside `\begin{center}` blocks. `title style={font=\small, at={(0,0.5)}, anchor=east, xshift=-5pt}` puts the time-step label as a left-side row label. `width=0.7\textwidth, height=3cm`.

### Exercises inventory (ch05)

Section starts l.1026 (`\section{Examples \& Exercises}`).

1. **"Given the canonical six points"** (l.1076) — multi-part worked numerical (PCA by hand).
   - Sub-parts: Centering, The covariance matrix, Eigenvalues, Eigenvector for $\lambda_1$, Eigenvector for $\lambda_2$, Explained variance.
   - `align*`: ~10 (mean derivation, $\tilde{x}_1$ derivation, $\Sigma_{11}$ derivation, $\Sigma$ matrix, $a+c$ derivation, $(a-c)^2+4b^2$ derivation, quadratic formula, eigenvector $w_1$ derivation, normalisation, eigenvector $w_2$ derivation, explained-variance ratio).
   - Margin: `fig:pca_exercise_scatter` + 2 `\marginnote`s (orthogonality verify; geometric interpretation).
   - Length: ~115 lines (l.1076–~1190). The largest single exercise across all three chapters. Contains 1 `table*` of centred data.

2. **"Project and reconstruct"** (l.1198) — worked numerical follow-up.
   - `align*`: 3 ($z_1$ projection, $\hat{x}_1$ reconstruction, error squared).
   - Length: ~55 lines incl. `table*` of all six z, x_hat, errors.

3. **"Naïve feature selection vs PCA"** (l.1259) — worked numerical comparison.
   - Sub-parts: Drop $x^{(2)}$, Drop $x^{(1)}$.
   - `align*`: 2 (the two error derivations).
   - Length: ~50 lines incl. `table*` of 3-column reconstruction-error comparison.

4. **"The Code exercises load"** (l.1314) — code section.
   - `align*`: 0.
   - Margin: `\marginnote{\newthought{Code} is provided as a Python notebook.}` at l.1311 (NB: subtle wording variant — "is" vs ch03/04 "will be").
   - Length: ~16 lines incl. "What to observe".

### Pedagogical structural elements present (ch05)

- `\newthought{The fundamental question}` paragraph in Block 1: **NO** — chapter 05 omits this. The Why section ends with `\newthought{In order to move from high-dimensional observations...}` (l.54) bullet-list introducer instead.
- `\marginnote{\newthought{Teaser.}}` before bridge: **YES**, l.1364:
  > "If we replace the fixed eigenvector projection with a learned, nonlinear encoder, can we get a compact representation that generalises to unseen inputs?"
- Trailing `\marginnote{\newthought{feedback}}` placeholder at l.1374 — same convention as ch04.
- Self-Reflection itemize: **8 items**.
- Recap itemize: **5 items**.
- Chapter subtitle: **`Folding and Unfolding Space.`** (l.6).

---

## Notable figure code patterns to reuse

### Pattern A: standard 2D scatter axis preamble (used in every chapter)

```latex
\begin{axis}[
    xlabel={$x^{(1)}$}, ylabel={$x^{(2)}$},
    xmin=0, xmax=10, ymin=0, ymax=10,
    width=0.5\textwidth, height=0.5\textwidth,
    axis line style={draw=none},
    tick style={black, thin},
    xtick={2,4,6,8}, ytick={2,4,6,8},
    xticklabel style={font=\small},
    yticklabel style={font=\small},
    tick align=outside, tick pos=left,
]
\addplot[only marks, mark=*, mark size=2pt, black] coordinates {(1,2)(2,3)(3,1)};
\addplot[only marks, mark=*, mark size=2pt, black!55] coordinates {(6,8)(8,7)(8,9)};
\node[font=\tiny, anchor=north west] at (axis cs:1,2) {$x_1$};
```

Margin variant: replace `width=0.5\textwidth, height=0.5\textwidth` with `width=\marginparwidth, height=\marginparwidth`, font=\tiny everywhere, ticks `{1,3,5,7,9}` (5 ticks instead of 4).

### Pattern B: parametric circle in axis coordinates (ch04 hallmark)

```latex
\addplot[black!35, dashed, thin, domain=0:360, samples=60]
    ({1 + 2.5*cos(x)}, {2 + 2.5*sin(x)});
```

This is the canonical way to draw an $\varepsilon$-neighbourhood inside a pgfplots axis. Used 30+ times in ch04. (Compare with TikZ-only schematic margin figures that use `\draw[black!40, dashed] (0,0) circle (1.0cm)` directly.)

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
% Stepped merge connector
\draw[thick] (axis cs:0,0) -- (axis cs:0,1.41) -- (axis cs:1,1.41) -- (axis cs:1,0);
% Leaf labels and dashed cut line at chosen height
\draw[densely dashed, black!60] (axis cs:-1.5,4.3) -- (axis cs:5.3,4.3);
```

Heights are **literal data values**, not normalised. Each merge is one orthogonal `up-across-down` polyline.

### Pattern D: elbow plot with broken line and open/filled markers (ch03 + ch04)

```latex
\addplot[only marks, mark=o, mark size=2pt, black] coordinates {(6,2.24)};         % elbow open
\addplot[only marks, mark=*, mark size=2pt, black] coordinates {(1,1.41) (2,1.41) (3,2.00) (4,2.00) (5,2.24) (7,3.61)};
\draw[black, thin] (axis cs:1.18,1.41) -- (axis cs:1.82,1.41);  % gaps around markers
\draw[black, thin] (axis cs:2.18,1.48) -- (axis cs:2.82,1.90);
\draw[densely dashed, black!60] (axis cs:0.5,2.5) -- (axis cs:7.5,2.5);  % chosen-eps line
\node[font=\small, anchor=north west] at (axis cs:0.55,3.7) {$\varepsilon{=}2.5$};
```

The line is **manually segmented** with start/end coordinates leaving 0.18-unit gaps around markers. Notice ch03 uses filled `*` for the elbow and open `o` for others, ch04 inverts. Either is acceptable — the broken line is the convention.

### Pattern E: PCA projection with dashed error to projection line (ch05)

```latex
\addplot[only marks, mark=*, mark size=2pt, black] coordinates { ... };           % data
\addplot[only marks, mark=o, mark size=2pt, black, thick] coordinates { ... };    % reconstructions
% Per-point dashed error lines
\draw[black,thin,dashed] (axis cs:-2.5,-3.1)--(axis cs:-2.8,-2.8);
% Direction arrow
\draw[-{Stealth[length=4pt,width=2.5pt]}, black!50, semithick] (axis cs:0,0) -- (axis cs:2.1,2.1);
\node[font=\small, black!50, anchor=north west] at (axis cs:1.8,1.6) {$w_1$};
```

Stealth-tipped arrows for eigenvectors / principal directions. Errors as black thin dashed segments. Reconstructions as `mark=o, thick`.

---

## Recurring conventions worth documenting

### Layout / spacing

- `\vspace{2.5em}` is the canonical "section-internal big breath" — appears 8× in ch03, 8× in ch04, 4× in ch05. Used between sub-newthought blocks within Block 2 to separate concept groups (e.g. between "Compute is the soft wall" and the complexity table).
- `\vspace{1.5em}` is the smaller breath — typically before an `algorithm` or after a math display.
- `\vspace{0.5em}` is the micro-breath — between a question-style `\newthought` and the next paragraph (esp. exercises).
- `\newpage` is used **between blocks** (Block 1 → Block 2, Block 2 → Block 3) AND inside Block 2 to give large theory subsections a clean page start (e.g. `\newpage` before `\subsection{The Hierarchical Clustering Algorithm}` at l.204 ch03; before `\section{The Curse of Dimensionality, Revisited}` at l.177 ch05). Ch05 uses 7 `\newpage`s; ch03 only 5.
- `% ===== BLOCK X: ... =====` banner comments mark every block boundary.

### Recurring marginnote phrasings

- `\marginnote{\newthought{Teaser.}}` or `\marginnote{\newthought{Teaser}}` — placed before chapter-bridge text at end (ch03 l.1536, ch04 l.1356, ch05 l.1364).
- `\marginnote{\newthought{Code} will be provided as a Python notebook. Use it as a starting point, break things, and observe what changes.}` — exact wording in ch03 l.1488 and ch04 l.1309. Ch05 l.1311 uses `is provided` (variant).
- `\newthought{What to observe.}` — opens the post-code commentary in all three chapters.
- `\newthought{Self-Reflection} questions to guide your thinking:` — itemize template.
- `\newthought{Recap} of Key Concepts:` — itemize template.
- `\marginnote{\newthought{feedback}}` / `\marginnote{\newthought{Feedback.}}` — empty placeholder appearing as last marginnote of ch04 (l.1357) and ch05 (l.1374).
- `\marginnote{\newthought{Contrast with K-Means.}}` — recurring "callback to previous chapter" phrasing in ch03 l.1313 and ch04 has direct K-Means baseline figure (l.1229).
- `\newthought{In order to move from ... we have good reason to find ways to,}` followed by itemize — opens the Why-section's roadmap bullet list. Identical structural recipe in all three chapters (ch03 l.107, ch04 l.65, ch05 l.54).
- `\newthought{The Learning Objectives} of this lecture:` — closes Block 1 in all three.

### Figure-internal conventions

- Font: `font=\tiny` for all margin-figure labels (and most body-figure point labels); `font=\small` only when the figure is wide.
- Colours: **black** = primary cluster A or focused points; **black!55** = secondary cluster B (greyer); **black!30** = tertiary class, bridge points, or dimmed; **black!25** = dotted distance edges; **black!35** = past-merge solid edges; **black!40** = $\varepsilon$-circle outlines; **black!60** = dashed cut lines.
- Cluster centroids use `mark=o, mark size=2pt, thick` (open circle), never `*`.
- Noise points use `mark=x, thick` (the only place `mark=x` appears, ch04 l.584).
- Caption titling pattern: most body-figure captions begin with `\newthought{...}` (e.g. `\newthought{Visit $x_1$}:`, `\newthought{Merge 1}:`). This is uniquely common in ch03 and ch04, less so in ch05.
- Captions often contain **escaped checkmarks `\checkmark` and crosses `\times`** for in-line distance verifications (ch04 figs 384–602).
- Caption embeds line breaks `\\[4pt]` for multi-paragraph captions (ch04 trace figures).

### Algorithm conventions

- All algorithms use `\begin{algorithm}[H]` (here-float) with `\begin{algorithmic}[1]` (line-numbered).
- Always preceded by a `\newthought{...}` paragraph that motivates the algorithm in prose, plus a `\vspace{2.5em}` or `\vspace{1.5em}` separator.
- Each algorithm has a `\Require` and `\Ensure` line.
- Comments use `\Comment{...}` (rare; only ch05 PCA algorithm).
- After the algorithm, a `\newthought{Notice that ...}` or `\newthought{Termination ...}` paragraph reflects on a property.

### Math display conventions

- Math derivations use `align*` (never `align` with numbering) — every chapter.
- Multi-step derivations show intermediate equality on each line:
  ```
  \begin{align*}
      d(x_1,\,x_2) &= \sqrt{(3-1)^2 + (1-1)^2} \\
                   &= \sqrt{4 + 0} \\
                   &= 2
  \end{align*}
  ```
- Inline distance approx pattern: `$d(x_1,x_2){=}\sqrt{2}{\approx}1.41\;\checkmark$`. Note the `{=}` and `{\approx}` braces produce no spacing.
- $K{=}2$ style for inline parameter values everywhere.
- Variance and reconstruction tables always include a `\midrule` before the **Total** row.

### Notation / index conventions

- `\index{...}` calls are sprinkled liberally — every key concept gets one or several. Hierarchical: `\index{single linkage!complexity}`, `\index{failure modes!DBSCAN}`. Each chapter introduces 30–60 distinct index entries.
- `\cite{...}` placement: inline with the algorithm name (`DB Scan\cite{Ester1996}`, `Ward1963`, `Sibson1973`, `Zhang1996`, `Ankerst1999`, `Campello2013`, `Pearson1901`, `vanDerMaaten2008`, `McInnes2018`, `LeCun1998`, `Halevy2009`, `JohnsonLindenstrauss1984`, `Hotelling1933`, `Prim1957`).
- Special notation for DBSCAN: `$p_c$`, `$p_b$`, `$p_n$` (italic subscripted) — the chapter's own glyph.
- Cluster labels in figures: `$x_i, C_m$` for "$x_i$ currently in active cluster $C_m$"; `$x_i, C_k$` for sealed clusters.

### Block 3 / exercise conventions

- Every chapter's exercise section opens with one of these "Computing by hand…" / "Given … points …" framings.
- First exercise is almost always: a worked numerical with full derivation of one entry, then "compute the rest yourself, then verify against the table below" + a `\begin{table*}[ht]` of all values.
- Final exercise is almost always: the **coffeetable code** exercise (ch03/ch04 use 1797 aroma fingerprints, ch05 uses 1000 MNIST digits) preceded by margin-noted Python notebook reference, followed by `\newthought{What to observe.}` discussion paragraph.
- Tables in exercises use `p{...textwidth}` column specifications, `\toprule / \midrule / \bottomrule` (booktabs), `\vspace{2em}` between table body and caption.

### Section/subsection organisation differences across chapters

- **Ch03**: uses `\subsection` for theory blocks and `\subsection{Examples & Exercises}` (no `\section` after Block 1).
- **Ch04**: uses both — `\section{The Why}`, `\subsection`s within Block 2, then `\section{Examples & Exercises}` and `\section{Self-Reflection and Recap}`.
- **Ch05**: uses `\section`s everywhere for major theory units (PCA, ICA, t-SNE, UMAP get their own `\section`s). This is the heaviest sectioning of the three.

Suggestion for ch07/ch08: follow ch04's hybrid model (Block 1 = `\section{The Why}` + `\subsection{Hands-On Experience}`; Block 2 = `\subsection`s; Block 3 = `\section{Examples & Exercises}` + `\section{Self-Reflection and Recap}`). Use ch05's heavy sectioning only when you have multiple competing methods (PCA / ICA / t-SNE / UMAP).
