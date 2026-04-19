# notes_missingsemester — Chapter Structure Conventions

These notes define the layout every chapter in this directory must follow.
Later chapter drafts should mirror Chapter 1 (`chapters/01_servers_vms_linux.tex`) as the reference implementation.

## Three-block layout

Each chapter is partitioned into exactly three blocks, separated by banner comments:

```
% ==============================================================================================
% BLOCK 1: INTRODUCTION
% ==============================================================================================

% ==============================================================================================
% BLOCK 2: MAIN THEORY
% ==============================================================================================

% ==============================================================================================
% BLOCK 3: STUDENT ACTIVATION
% ==============================================================================================
```

### Block 1 — Introduction

Two consecutive parts:

1. `\section{The Why}` — motivation for the chapter's topic.
   - Open with a short framing paragraph (no `\newthought`).
   - Anchor the chapter to the **PixelWise** course narrative via a `\marginnote` and a `\newthought{Across ten lecture blocks we build PixelWise}` (or an analogous continuation).
   - Include a central figure when a visual mental model is useful (e.g. the two-machine diagram). Caption + `\label{fig:...}`.

2. `\subsection{Hands On Experience}` — concrete hook + learning objectives.
   - Open with a relatable scenario (`\newthought{Consider ...}`) that exposes the problem the chapter solves.
   - Follow with a short reflective passage that names the design decision or principle the chapter rests on.
   - Close with a `\newthought{This <nth> block}` paragraph that lists the block's learning objectives as an `itemize`. Phrase objectives as things the student will have done or be able to do by the end of the block.

> Do **not** preview architecture that later chapters actually build (frontend, reverse proxy, database wiring, etc.). Keep Block 1 scoped to what this chapter delivers.

### Block 2 — Main Theory

Multiple `\section{...}` entries that present the chapter's core concepts in reading order. Conventions:

- One `\section` per major concept; start each with `\newpage`.
- Sections are ordered by dependency: concepts required to perform the next hands-on step come first. The chapter's opening figure and Block 1 learning objectives should preview the same order.
- Do not include theory that the chapter does not operationalize. If a concept is decorative or is the load-bearing topic of a later chapter, push it there instead.
- Prose is Tufte-style: short paragraphs led by `\newthought{...}`, with `\marginnote{...}` for side commentary, definitions, tool pointers, and worked intuitions.
- Code and configuration go in `verbatim` blocks.
- Introduce concepts before they are used; first use of a term is marked with `\emph{...}` and indexed via `\index{...}`.

### Block 3 — Student Activation

Two sections, in this order:

1. `\section{Examples \& Exercises}` — hands-on work that students perform.
   - Open with a `\marginnote` framing exercises as practice, noting the snapshot/restore safety net when applicable.
   - **Mirror the theory block one-to-one.** Each `\section` in Block 2 must have a corresponding `\subsection` in Examples & Exercises, in the same order, so a student can read a concept and then immediately practise it.
   - A short `\newthought{Block~N introduced ...}` paragraph at the top of the section names the mirror explicitly.
   - Within each `\subsection`, sequence steps in the order a student would actually carry them out, and end with a concrete verification or artefact (a ping reply, a passwordless login, a named snapshot).
   - End the section with a forward-looking `\newthought{A note on what comes next.}` paragraph that motivates the next chapter.

2. `\section{Self-Reflection and Recap}` — consolidation.
   - `\newthought{Self-Reflection}` questions as an `itemize` list, covering each Block 2 section.
   - `\newthought{Recap}` of key concepts as an `itemize` list.
   - Close with one or two `\marginnote` teasers bridging to the next chapter.

## Formatting rules

- **Tufte primitives only** for emphasis and sidebars: `\newthought`, `\marginnote`, `\emph`. Do **not** use `\textbf` or `\textit` for emphasis in prose.
- **No parenthetical asides.** Fold explanations into inline clauses; avoid round brackets for side remarks.
- **Index consistently.** Add `\index{...}` on first substantive use of a term, and repeat for key terms at section openings.
- **Figures** use `tikzpicture`; captions should describe what the figure shows and why it matters, not just name it.
- **References** in the bibliography must carry a Google Scholar or arXiv URL.

## Naming and cross-references

- Chapter files: `NN_topic.tex` in `chapters/`, matching the master file `notes_missingsemester.tex`.
- Figure labels: `fig:<short_name>` scoped by topic, e.g. `fig:two_machines`.
- The two VMs are canonically `dev` at `192.168.56.10` and `server` (a.k.a. `prod`) at `192.168.56.11`. Keep these addresses stable across chapters.
