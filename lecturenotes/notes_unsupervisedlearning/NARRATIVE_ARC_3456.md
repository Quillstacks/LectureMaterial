# Narrative-Arc Analysis: BLOCK 2 of Chapters 03, 04, 05, 06

Goal: extract the story arc, transitions, and rhetorical moves from the four established BLOCK 2 sections so that ch07 and ch08 can be rewritten with the same kind of narrative spine.

---

## Chapter 03: Hierarchical Clustering

### 1. Section sequence (BLOCK 2)

| Line | Heading |
|------|---------|
| 206  | `\subsection{The Hierarchical Clustering Algorithm}` |
| 569  | (no heading; topic block) "Linkage criteria beyond two points is non-trivial" |
| 577  | (sub-block) Single Linkage |
| 627  | (sub-block) Complete Linkage |
| 677  | (sub-block) Average Linkage |
| 735  | (sub-block) Ward's Method |
| 799  | (no heading; topic block) "When Hierarchical Clustering Fails" |
| 856  | (no heading; topic block) "Computational Complexity" |
| 897  | (no heading; topic block) "Scalability by Compression / BIRCH" |
| 998  | (no heading; topic block) "Dendrogram vocabulary" |
| 1006 | (no heading; topic block) "Reading a dendrogram" |
| 1097 | (no heading; topic block) "How do we infer new data points?" |
| 1108 | (no heading; topic block, currently `\iffalse`) "Excursion: Prim's MST and Single Linkage" |

Note: ch03 uses one `\subsection` and then subsequent `\newthought` blocks function as section-level beats. The visible spine in BLOCK 2 is: Algorithm -> Linkage variants -> Failure modes -> Complexity/Scalability -> Reading the output -> Inference.

### 2. Topic-by-topic story

**The Hierarchical Clustering Algorithm (l. 206).**
- *What:* introduces the agglomerative bottom-up procedure, the algorithm box, and a worked storyboard merging the canonical six points step by step with a deterministic initialisation.
- *Why here:* Block 1 ended with the question "how do we build a hierarchy of clusterings?". This section answers it operationally before any choice has to be made.
- *Sets up:* the algorithm leaves one slot undefined, the linkage criterion `L`. The narrator explicitly flags `L` as the only hyperparameter, so the next beat is forced.
- *Opening newthought:* "The agglomerative strategy is bottom-up: given data $X = \{x_1,\ldots,x_n\}$, initialize $n$ singleton clusters $C_i = \{x_i\}$ in an active set and precompute a distance matrix $D[i,j] = d(x_i, x_j)$."

**Linkage criteria, single / complete / average / Ward (l. 569-794).**
- *What:* fills in the slot left by the algorithm box. Four linkages are presented with formula, margin figure, and one-paragraph behavioural fingerprint.
- *Why here:* the algorithm only works once `L` is chosen; the variants have to come immediately after the algorithm, not after failures.
- *Sets up:* the differences between linkages already foreshadow their failure modes (chaining vs shape bias).
- *Opening newthought:* "Linkage criteria beyond two points is non-trivial determine how the distance between two clusters is computed from the distances between their individual members."

**When Hierarchical Clustering Fails (l. 799).**
- *What:* surveys chaining, shape bias, irreversibility of greedy merges.
- *Why here:* the linkage tour gave each method a personality. Now the personalities are stress-tested.
- *Sets up:* irreversibility is named as the deeper problem; it implies a cost. That cost is paid in compute next.
- *Opening newthought:* "When Hierarchical Clustering Fails the root cause is that the linkage criterions optimises locally with no global view nor understanding for scale."

**Computational Complexity / Scalability / BIRCH (l. 856-897).**
- *What:* derives the $O(n^2)$ memory wall and $O(n^2)$/$O(n^3)$ time wall, then introduces SLINK as the special case and BIRCH as the engineering escape hatch.
- *Why here:* failure modes lead to the engineering question of when the method is even runnable.
- *Sets up:* having defended that the algorithm runs and produces a tree, the chapter can finally teach the reader to read the tree.
- *Opening newthought:* "Computational Complexity Memory is the hard wall."

**Dendrogram vocabulary / Reading a dendrogram (l. 998-1006).**
- *What:* gives the formal vocabulary then the one-rule reading procedure (cut at height $h$); compares gaps between single linkage and Ward.
- *Why here:* the algorithm has produced an artifact since page one of BLOCK 2 but the reader has not yet been taught how to interpret it. This is the interpretive payoff.
- *Sets up:* dendrogram is static, so the obvious question "what about new data?" arises.
- *Opening newthought:* "Dendrogram vocabulary borrows from genealogy and graph theory."

**How do we infer new data points? (l. 1097).**
- *What:* explains that hierarchical clustering has no native inference rule, then offers nearest-centroid or nearest-leaf workarounds.
- *Why here:* answers the natural reader question after dendrogram reading.
- *Sets up:* an honest limitation that motivates Block 3 reflection and the next chapter's density-based view.
- *Opening newthought:* "How do we infer new data points? The dendrogram is a static structure built on the original data; it does not directly provide a way to assign new points to clusters."

### 3. Connective tissue

- Algorithm -> Linkage: "Notice that $L$ is the only hyperparameter to determine." (l. 234) bridges to "Linkage criteria beyond two points is non-trivial determine how the distance between two clusters is computed from the distances between their individual members." (l. 569)
- Linkage -> Failures: Ward's Method block ends, then the bridge is "When Hierarchical Clustering Fails the root cause is that the linkage criterions optimises locally with no global view nor understanding for scale." (l. 799)
- Failures -> Complexity: "Irreversible greedy merges and local optima... A suboptimal early merge propagates through all future distance updates." (l. 846) bridges to "Computational Complexity Memory is the hard wall." (l. 856)
- Complexity -> Reading: BIRCH ends with the engineering rescue, then "Dendrogram vocabulary borrows from genealogy and graph theory." (l. 998)
- Reading -> Inference: "Compare the gaps. Single linkage gave a gap from 2.24 to 6.40... Ward's tends to amplify the gap signal." (l. 1087) bridges to "How do we infer new data points?" (l. 1097)

### 4. Narrative-arc archetype

**Definitions -> Algorithm -> Trace -> Hyperparameter (linkage) -> Failures -> Complexity -> Output reading -> Inference** — the formal build-up of one method, with linkage taking the role of the "hyperparameter" beat.

---

## Chapter 04: Density-Based Clustering

### 1. Section sequence (BLOCK 2)

| Line | Heading |
|------|---------|
| 205 | `\subsection{The Density-Based Algorithm}` |
| 606 | `\subsection{Hyperparameter Selection}` |
| 754 | `\subsection{When DB Scan Fails}` |
| 876 | (no heading; topic block) "OPTICS" |
| 898 | (no heading; topic block) "HDBSCAN" |
| 934 | (no heading; topic block) "The curse of dimensionality" |

### 2. Topic-by-topic story

**The Density-Based Algorithm (l. 205).**
- *What:* introduces DBSCAN with its two parameters ($\varepsilon$, $n_{\min}$), the three-role taxonomy of points (core, border, noise), density reachability and connectivity, then traces the algorithm on the seven canonical points.
- *Why here:* Block 1 set up the failure of centroid-based and link-based methods to handle a noise point sitting between clusters. The algorithm beat answers it.
- *Sets up:* the algorithm runs, but $\varepsilon$ and $n_{\min}$ are still magic numbers.
- *Opening newthought:* "DB Scan or Density-Based Spatial Clustering of Applications with Noise, builds clusters from local density rather than from a chosen number of centroids or a sequence of merges."

**Hyperparameter Selection (l. 606).**
- *What:* gives the rule of thumb $n_{\min} > d{+}1$ and the $k$-distance plot heuristic for $\varepsilon$, illustrated on the canonical seven.
- *Why here:* the algorithm beat repeatedly invoked $\varepsilon{=}2.5$, $n_{\min}{=}2$ without justification. The reader has earned a recipe.
- *Sets up:* once the reader can choose parameters confidently, the question of when even the right parameters fail comes next.
- *Opening newthought:* "Choosing $n_{\min}$ follows a practical rule of thumb: set $n_{\min} > d{+}1$ where $d$ is the dimension of the feature space."

**When DB Scan Fails (l. 754).**
- *What:* shows varying-density clusters and bridging chains, both pathologies of the single global $\varepsilon$.
- *Why here:* now that the reader can pick $\varepsilon$, they should also see why one global $\varepsilon$ is fundamentally insufficient.
- *Sets up:* the global-$\varepsilon$ critique demands a per-point reachability story; that is OPTICS and HDBSCAN.
- *Opening newthought:* "DB Scan has its own pathologies. Every density-based method sets a single threshold."

**OPTICS / HDBSCAN (l. 876, 898).**
- *What:* introduces per-point core distance and reachability distance (OPTICS), then the mutual reachability metric and HDBSCAN's hierarchical condensation.
- *Why here:* directly answers "how do we get rid of the global $\varepsilon$?".
- *Sets up:* HDBSCAN reduces hyperparameters to one ($n_{\min}$), but a deeper failure mode is shared by all distance-based methods.
- *Opening newthought:* "OPTICS or Ordering Points To Identify the Clustering Structure introduces two per-point distances."

**The curse of dimensionality (l. 934).**
- *What:* derives $d_{\text{NN}} \propto N^{-1/d}$ and shows $\varepsilon$-neighbourhoods become useless as $d$ grows.
- *Why here:* OPTICS/HDBSCAN fixed local-density issues; the deeper failure that affects every method in Part I is dimensionality, and this beat names it.
- *Sets up:* the explicit pivot to Part II of the book on representations.
- *Opening newthought:* "The curse of dimensionality: All distance-based methods share a deeper vulnerability as the number of features $d$ grows, the volume of the space increases so fast that a fixed number of points $N$ becomes sparse everywhere."

### 3. Connective tissue

- Algorithm -> Hyperparameters: end-of-trace caption "All points visited. Final result... No $K$ was chosen; the noise point was never forced into a cluster." (l. 600) bridges to "Choosing $n_{\min}$ follows a practical rule of thumb." (l. 608)
- Hyperparameters -> Failures: $k$-distance plot caption ends, then "DB Scan has its own pathologies. Every density-based method sets a single threshold." (l. 756)
- Failures -> Extensions: bridging-figure caption ends, then "OPTICS or Ordering Points To Identify the Clustering Structure introduces two per-point distances." (l. 876)
- Extensions -> Curse: "The only parameter the user must set is $n_{\min}$, and the result is often robust to its choice." (l. 910) bridges to "The curse of dimensionality: All distance-based methods share a deeper vulnerability." (l. 934)

### 4. Narrative-arc archetype

**Algorithm -> Hyperparameters -> Failures -> Extensions (OPTICS, HDBSCAN) -> Cross-method failure (curse)** — the same formal build-up as ch03, but the failure beat splits into two: a method-specific failure (global $\varepsilon$) that is then patched, and a Part-I-wide failure (curse of dimensionality) that motivates the next chapter.

---

## Chapter 05: Dimensionality Reduction

### 1. Section sequence (BLOCK 2)

| Line | Heading |
|------|---------|
| 179 | `\section{The Curse of Dimensionality, Revisited}` |
| 247 | `\section{A Na\"ive Baseline: Variance-Based Feature Selection}` |
| 342 | `\section{Principal Component Analysis}` |
| 636 | `\section{Reconstruction Error}` |
| 714 | `\section{Independent Component Analysis}` |
| 724 | `\section{t-SNE}` |
| 962 | `\section{UMAP}` |

### 2. Topic-by-topic story

**The Curse of Dimensionality, Revisited (l. 179).**
- *What:* reframes the curse from ch04 as a statement about *intrinsic* dimensionality $k$, not nominal $d$.
- *Why here:* picks up exactly where ch04's BLOCK 2 ended; turns the threat into an opportunity.
- *Sets up:* the question "how do we find the right $k$ directions?" demands a method.
- *Opening newthought:* "The key observation is that high $d$ is only fatal when all $d$ dimensions carry independent information."

**A Na\"ive Baseline: Variance-Based Feature Selection (l. 247).**
- *What:* introduces variance-thresholding feature selection, the simplest possible answer.
- *Why here:* a deliberately weak baseline is the pedagogical anchor against which PCA will be measured.
- *Sets up:* the failure case (signal runs diagonally) is the gap PCA fills.
- *Opening newthought:* "When axes align with the signal consider the most straightforward way to reduce dimensions: measure the variance of each original feature independently and keep only those with the highest variance."

**Principal Component Analysis (l. 342).**
- *What:* derives PCA from variance maximisation, the Lagrangian, eigendecomposition, eigenvalue/eigenvector computation, and the scree-plot diagnostic.
- *Why here:* responds to the failure case of variance-based selection by *constructing* new axes instead of selecting old ones.
- *Sets up:* having taught maximisation, the dual formulation as reconstruction error is a natural follow-up.
- *Opening newthought:* "Here both features have nearly the same variance, so variance-based selection cannot decide which to keep."

**Reconstruction Error (l. 636).**
- *What:* presents the dual derivation of PCA via squared reconstruction loss and sets up the mental scaffold that autoencoders will inherit.
- *Why here:* the variance and reconstruction views are equivalent; teaching both is what makes the bridge to autoencoders in ch06 land.
- *Sets up:* PCA decorrelates but does not separate sources (ICA), and only rotates axes (limitation that motivates t-SNE).
- *Opening newthought:* "So far we derived PCA from variance maximisation: find the directions along which the projected data spreads the most. There is a dual view that asks the opposite question: if we compress from $d$ dimensions to $k$ and then decompress back to $d$, how much signal do we lose?"

**Independent Component Analysis (l. 714).**
- *What:* short PCA sibling that addresses statistical independence rather than decorrelation.
- *Why here:* completes the linear branch of methods before pivoting to nonlinear.
- *Sets up:* the explicit "PCA and ICA are linear" margin note that motivates t-SNE.
- *Opening newthought:* "PCA decorrelates but does not separate sources."

**t-SNE (l. 724).**
- *What:* full algorithmic recipe (high-D similarities, low-D Student-t similarities, KL gradient, perplexity), traced on the canonical six points across $t{=}0$, $t{=}2$, $t{=}100$.
- *Why here:* PCA/ICA cannot bend the coordinate system around a curved manifold; t-SNE can.
- *Sets up:* t-SNE has scale and reproducibility issues, which UMAP fixes.
- *Opening newthought:* "t-SNE. stands for t-distributed Stochastic Neighbour Embedding. It is optimised for one-, two- or three-dimensional visualization."

**UMAP (l. 962).**
- *What:* names UMAP's three practical strengths (scale, global structure, reproducibility) and gives the algorithm box.
- *Why here:* the modern, production-ready successor that addresses each named t-SNE weakness.
- *Sets up:* the bridge to ch06 (autoencoders / VAE) where the encoder *learns* the embedding rather than fitting one per dataset.
- *Opening newthought:* "UMAP brings three practical strengths."

### 3. Connective tissue

- Curse-revisited -> Na\"ive baseline: "The question is how to find the right $k$ directions. Picking original features by hand (as in variance-based selection) works when the axes happen to align with the signal." (l. 234) bridges to "When axes align with the signal consider the most straightforward way to reduce dimensions." (l. 251)
- Na\"ive baseline -> PCA: "When does it fail? When the signal does not happen to align with the axis." (l. 295) bridges to "Here both features have nearly the same variance, so variance-based selection cannot decide which to keep." (l. 350)
- PCA -> Reconstruction error: "The scree plot visualises exactly this." then "So far we derived PCA from variance maximisation... There is a dual view." (l. 636)
- PCA dual -> ICA: "PCA decorrelates but does not separate sources." (l. 716)
- ICA / linear methods -> t-SNE: margin note "PCA and ICA are linear. No rotation of the axes can untangle classes that live on a curved manifold." (l. 726) bridges to "t-SNE. stands for t-distributed Stochastic Neighbour Embedding." (l. 731)
- t-SNE -> UMAP: marginnote "Interpreting t-SNE. Cluster sizes and inter-cluster distances are meaningless... Use t-SNE for visualization only, never as preprocessing." (l. 950) bridges to "UMAP brings three practical strengths." (l. 966)

### 4. Narrative-arc archetype

**Naive baseline -> Linear method -> Linear variant -> Nonlinear method -> Modern variant** — a competition of methods, each one earning its place by fixing a named weakness of its predecessor.

---

## Chapter 06: Variational Inference

### 1. Section sequence (BLOCK 2)

| Line | Heading |
|------|---------|
| 260 | `\section{The Autoencoder}` |
| 388 | `\section{From Autoencoders to Variational Autoencoders}` |
| 555 | `\section{VAE Variants}` |
| 588 | `\section{The Reparameterisation Trick}` |
| 664 | `\section{Designing the Bottleneck}` |
| 871 | `\section{Exploring the Latent Space}` |

### 2. Topic-by-topic story

**The Autoencoder (l. 260).**
- *What:* presents the encoder-decoder bottleneck architecture, the forward pass, the reconstruction loss, and the explicit linear-AE-equals-PCA bridge.
- *Why here:* Block 1's hands-on game framed encoders and decoders as humans negotiating a code; this section makes that negotiation mathematical.
- *Sets up:* the autoencoder reconstructs but its latent space has no geometric guarantees.
- *Opening newthought:* (the section opens with the connecting prose) "Follows the notion of a bottleneck architecture: an encoder that compresses the input into a low-dimensional embedding, and a decoder that reconstructs the input from that embedding."

**From Autoencoders to Variational Autoencoders (l. 388).**
- *What:* names the latent-space disorganisation, then introduces the per-input Gaussian distribution, the KL term, and the reconstruction-vs-KL tug-of-war that yields a structured latent space.
- *Why here:* this is the upgrade-motivation beat. The plain AE works for compression but does not give you a generative or interpolable latent space.
- *Sets up:* the architecture motivates a family of variants, and exposes a numerical question (how do we backprop through a sample?).
- *Opening newthought:* "The latent space has no geometric guarantees. The objective only rewards reconstruction; nothing constrains how embeddings are arranged."

**VAE Variants (l. 555).**
- *What:* short tour of $\beta$-VAE, VQ-VAE, and Conditional VAE with one paragraph and one formula each.
- *Why here:* once the basic VAE is built, naming the obvious knobs is cheap and useful.
- *Sets up:* none of the variants explained how the loss is actually optimised through a stochastic sample. Time for the reparameterisation trick.
- *Opening newthought:* "$\beta$-VAE scales up the KL term to pressure the encoder to use the latent space efficiently."

**The Reparameterisation Trick (l. 588).**
- *What:* poses the intractable marginal-likelihood integral, gives the spoiler that it is intractable, and introduces $z = \mu + \sigma \epsilon$ as the gradient-friendly rewrite.
- *Why here:* the technical machinery had to wait until the reader cared about why we needed gradients through a sampled $z$.
- *Sets up:* with the loss now optimisable, the reader can ask the practical hyperparameter question: what should $k$ be?
- *Opening newthought:* "How do we now the distribution of the current embedding space?"

**Designing the Bottleneck (l. 664).**
- *What:* studies the latent dimensionality $k$ as the master hyperparameter: too few, too many, the information bottleneck principle, active units, a practical protocol, and prior shape.
- *Why here:* the most consequential design choice deserves its own beat after the math is settled.
- *Sets up:* a structured latent space exists and is sized; what does it look like?
- *Opening newthought:* "The latent dimensionality $k$ is the most consequential hyperparameter in a VAE."

**Exploring the Latent Space (l. 871).**
- *What:* latent interpolation (lerp vs slerp) and direct generation by sampling the prior.
- *Why here:* the payoff. Everything before exists so that this beat can demonstrate that the latent space is genuinely continuous and generative.
- *Sets up:* the bridge to ch07 ("low reconstruction error and high prior likelihood under $p(z)$ mean an input resembles the training data... uncertainty estimation turns familiarity into a principled tool").
- *Opening newthought:* "Latent interpolation reveals the structure that the VAE has learned."

### 3. Connective tissue

- Autoencoder -> VAE motivation: "Connection to PCA. If the encoder and decoder are both linear..." (l. 380) bridges to "The latent space has no geometric guarantees. The objective only rewards reconstruction." (l. 392)
- VAE core -> Variants: "Together they turn the encoder into a feature extractor whose embeddings are both informative and geometrically well behaved." (l. 545) bridges to "$\beta$-VAE scales up the KL term." (l. 557)
- Variants -> Reparameterisation: variants block ends, then "How do we now the distribution of the current embedding space?" (l. 590)
- Reparameterisation -> Bottleneck: trick figure caption ends, then "The latent dimensionality $k$ is the most consequential hyperparameter in a VAE." (l. 666)
- Bottleneck -> Latent space: prior-shape paragraph and KL annealing margin note close the section, then "Latent interpolation reveals the structure that the VAE has learned." (l. 873)

### 4. Narrative-arc archetype

**Foundation (AE) -> Upgrade motivation (no geometry) -> Upgrade (VAE) -> Sub-variants -> Technical machinery (reparameterisation) -> Hyperparameter (k) -> Use (interpolation, generation)** — the introduce-then-upgrade arc.

---

## Cross-chapter rhetorical / pedagogical moves

Every chapter in this set deploys most of the following moves. Collect them as a checklist.

1. **The "trace through our $n$ canonical points" worked storyboard.** ch03 traces six points through every merge with a figure per step; ch04 traces seven points (plus a bonus $x_8$); ch05 traces six points through PCA arithmetic and t-SNE iterations $t{=}0,2,100$; ch06 uses six points implicitly in the hands-on game and in MNIST exercises. The same coordinates recur across chapters as a visual anchor.

2. **"Notice that $X$" reflective callback.** Inserted right after an algorithm to highlight the one design choice the reader must own: "Notice that $L$ is the only hyperparameter to determine" (ch03), "Notice, that the sorting does not reflect cluster membership" (ch04), "Notice the missing value at $k{=}3$" (ch03 dendrogram).

3. **Failure-mode framing as its own beat.** "When Hierarchical Clustering Fails" (ch03), "When DB Scan Fails" (ch04), "When does it fail?" (ch05 naive baseline), "Too few dimensions / Too many dimensions" (ch06). Failures are never asides; they get headings.

4. **Extension framing.** "Beyond [method]" or extensions section: "Scalability by Compression" / BIRCH (ch03), OPTICS and HDBSCAN (ch04), VAE Variants (ch06). Always after failures, never before.

5. **Cross-chapter callbacks.** "Compare with Figure naive_projection" (ch05 -> baseline), "PCA and ICA are linear... t-SNE and UMAP" (ch05 -> ch05's own pivot), "The curse of dimensionality" (ch04 explicitly motivates ch05), "uncertainty estimation turns familiarity into a principled tool" (ch06 -> ch07).

6. **Comparison-with-prior-method paragraphs.** "Initialization is deterministic. This stands in sharp contrast to k-means" (ch03), "DB Scan builds clusters from local density rather than from a chosen number of centroids or a sequence of merges" (ch04), "Connection to PCA" (ch06 AE).

7. **Analogy / metaphor anchors.** "no centroid required" (ch04), "the points have not moved apart; the space has grown underneath them" (ch04 curse), "the bridge point chains the two groups together" (ch03), "spreading mass costs more than translating it" (ch06 KL).

8. **Recipe / "practical protocol" boxes.** $k$-distance plot recipe (ch04), scree plot diagnostic (ch05), "A practical protocol for choosing $k$" (ch06).

9. **The dual-view derivation.** Variance maximisation vs reconstruction error (ch05), encoder distribution vs aggregate posterior (ch06). Always presented as "There is a dual view that asks the opposite question."

10. **Hyperparameter as bridge.** The single hyperparameter is repeatedly used to organise an entire section: $L$ for ch03, $\varepsilon$/$n_{\min}$ for ch04, $k$ for ch05, $k$ and $\beta$ for ch06.

11. **The "spoiler" mid-derivation.** "Spoiler. We can't" (ch06 reparameterisation). Used sparingly to acknowledge an impasse before resolving it.

---

## Recommendations for ch07 and ch08 BLOCK 2

### Ch07 Uncertainty Estimation (recommended archetype: **Foundation -> Upgrade motivation -> Methods -> Failure modes / Calibration -> Use**, the ch06 arc)

Ch07's content is closest to ch06 in shape: a concept with a definitional foundation (sources of uncertainty), a method beat that quantifies it (MC Dropout, Deep Ensembles), and a "use" beat at the end (acting under uncertainty). The current ordering already approximates this, but the analogy to ch06's arc suggests three concrete moves:

1. **Make Anomaly Detection and OOD Detection one beat with sub-variants, not two parallel sections.** Ch06's "VAE Variants" beat hosts $\beta$-VAE, VQ-VAE, and Conditional VAE under a single roof. Anomaly detection (statistical, proximity, reconstruction) and OOD detection (softmax, ODIN, energy) are the same kind of catalogue: applied scoring methods that turn the upstream uncertainty story into actionable signals. A single section "Scoring Methods: From Uncertainty to Decisions" with subsections for anomaly families and OOD families gives the chapter the same compact catalog rhythm.
2. **Cut "Evaluation Without Labels" from BLOCK 2 or relocate it.** Silhouette, Calinski-Harabasz, and stability are unsupervised cluster quality metrics, not uncertainty quantification. They break the spine. They belong either as a margin callback to ch03/ch04 or as a Block 3 exercise.
3. **Rename and elevate "Acting Under Uncertainty" as the use payoff,** mirroring ch06's "Exploring the Latent Space". The current bullet list reads like a checklist; rewrite as a worked storyboard with one or two cases (the medical-imaging handoff, the autonomous-vehicle abstain) so it lands as the climax beat the arc demands.

Bridge sentence to seed the chapter: between Sources of Uncertainty and Quantifying Epistemic Uncertainty, add a "Notice that aleatoric uncertainty is irreducible" callback that forces the upgrade to epistemic methods, exactly the way ch06 forces the AE-to-VAE jump.

### Ch08 Self-Supervised Learning (recommended archetype: **Naive baseline -> Method -> Variants -> Nonlinear / non-contrastive method -> Modern / cross-modal variant**, the ch05 arc)

Ch08 is a competition of methods that increase in sophistication, exactly the shape of ch05. Pretext tasks are the variance-based-selection-style baseline ("works when handcrafted invariances align with the task, fails otherwise"). Contrastive learning is the PCA equivalent: the first principled method that constructs invariances from data. SimCLR and MoCo are the linear-variants tier: same family, different engineering trade-offs. Non-contrastive (BYOL, SimSiam) and Masked Prediction are the t-SNE-style nonlinear pivot, doing the job without negatives. CLIP is the UMAP-style modern variant that scales and crosses domains.

To strengthen the arc:

1. **Make every section transition a "fixes the named weakness of the predecessor" sentence,** exactly as ch05 does ("PCA and ICA are linear. No rotation of the axes can untangle classes..."). Pretext to InfoNCE: "Handcrafted invariances do not transfer." InfoNCE to SimCLR: "InfoNCE is silent on what the positive pair should look like." SimCLR to MoCo: "The cost of SimCLR sits in the batch." MoCo to BYOL: "Contrastive losses need negatives." Masked Prediction to CLIP: "Masking still confines supervision to a single modality."
2. **Add a "Why don't they collapse?" failure-mode paragraph,** which the current chapter already attempts. Promote it to a proper beat with the same status as ch04's "When DB Scan Fails": this is the chapter's most pedagogically interesting failure mode and currently sits underweight.
3. **Trace one method on the canonical six points.** Every other chapter uses the recurring coordinates as a visual anchor. SimCLR with two augmentations of the six points and a small InfoNCE worked example would lock the arc into the existing series style.

The shared move across both chapters: end BLOCK 2 with a "use" or "what comes next" beat that closes the arc and bridges to the following chapter, the way ch04 ends on the curse, ch05 ends on UMAP's modernity, and ch06 ends on generation.
