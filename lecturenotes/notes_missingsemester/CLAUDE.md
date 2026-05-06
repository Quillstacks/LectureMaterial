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
% BLOCK 2: CONCEPTS AND PRACTICE
% ==============================================================================================

% ==============================================================================================
% BLOCK 3: CONSOLIDATION
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

### Block 2 — Concepts and Practice

Theory and exercise sections are interleaved as **theory→exercise pairs**, one pair per major concept. The student reads a concept and immediately practises it.

Conventions:

- Each pair is two top-level sections in this order:
  1. `\section{<Concept>}` — the theory section.
  2. `\section{Exercise: <Concept>}` — the matching hands-on practice.
- Start each section with `\newpage`. Pairs are ordered by dependency: each pair builds on the previous one.
- The exercise sequence is the spine; theory adapts to it. If a theory section has no clean exercise mirror, fold it into the closest related theory section as a `\subsection`. If an exercise has no theory mirror (an integration or wrap-up exercise), place it after all paired sections.
- Optional or forward-looking theory sections that have no exercise belong **at the very end of Block 2**, after all paired and integration exercises, just before the BLOCK 3 banner. Title them `\section{Optional: ...}`.
- The first exercise of the chapter carries a `\marginnote` framing exercises as practice and noting the snapshot/restore safety net when applicable.
- The last exercise (or the last optional theory section, if any) closes Block 2 with a `\newthought{A note on what comes next.}` paragraph that motivates the next chapter.
- Prose is Tufte-style: short paragraphs led by `\newthought{...}`, with `\marginnote{...}` for side commentary, definitions, tool pointers, and worked intuitions.
- Code and configuration go in `verbatim` blocks.
- Introduce concepts before they are used; first use of a term is marked with `\emph{...}` and indexed via `\index{...}`.
- Within each exercise, sequence steps in the order a student would actually carry them out, and end with a concrete verification or artefact (a ping reply, a passwordless login, a named snapshot).
- Do **not** lead an exercise with a phrase like "Block~N introduced X" — the theory now sits directly above; refer to it as "the theory above" or fold the lead-in into the first imperative sentence.

### Block 3 — Consolidation

A single section: `\section{Self-Reflection and Recap}`.

   - `\newthought{Self-Reflection}` questions as an `itemize` list, covering each theory section in Block 2.
   - `\newthought{Recap}` of key concepts as an `itemize` list.
   - Close with one or two `\marginnote` teasers bridging to the next chapter, plus a `\newthought{Milestone.}` paragraph summarising what the student now owns.

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
