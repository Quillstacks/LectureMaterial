# Slide design guide — what to build, and when

This is the editorial companion to [AGENTS.md](AGENTS.md). AGENTS.md tells you how
the theme works mechanically; this file tells you *which* layout to reach for given
*what* you are trying to say. It encodes Prof. Schutera's preferences. When a deck
decision is not covered here, follow the spirit: restraint, one point at a time,
the accent reserved for what matters.

## Philosophy

- **One idea per slide — sized for about five minutes of talking.** A slide is one
  conceptual move, but it should carry enough to speak to for ~5 min. Not a single
  thin line, not a wall. If a slide needs two ideas, it is two slides.
- **Prose first.** Lead with a short sentence or two. Reach for `itemize` only when
  the content is a genuine list. Never a bulleted wall.
- **One red element per slide, maximum.** Red always means "this is the point": the
  key term in an equation, the one result, the active element. If two things are
  red, nothing is.
- **Boxes carry meaning.** A block is not decoration; it signals status
  (definition, example, warning). Used sparingly, it stays meaningful.

## Deck skeleton

1. **Title slide** — `\begin{frame}[plain]\titlepage\end{frame}`.
2. **Agenda — the "lecture in one slide".** Not a table of contents. One designed
   slide that answers **why this lecture matters** and, having shown it matters,
   **what you will be able to do after it**. Render it as the lecture deserves: a
   small figure/map (sections as a `tdbox`/`tdarr` flow), a probing question, or a
   motivation line plus a short "after this lecture …" note in the side third.
   Never bullets.
3. **Sections**, each opened by a divider (`\sectionpage`, auto via
   `\AtBeginSection`). The footer nav mirrors this structure.
4. **One final takeaway** for the whole talk — a single `takeaway` slide with the
   distilled point. Not one per section; save it for the end.
5. **Close** — optionally mirror the agenda as a recap ("what you can now do").

## Layout catalogue — pick by purpose

| You are presenting… | Use |
|---|---|
| a concept, claim, or step | standard prose frame; accent the one key word if any |
| an **equation** | the **2/3 + 1/3** grid: equation in the main two-thirds, its reading/interpretation in the right third, one term in red (see below) |
| a **derivation** | a single **derivation slide**: the multi-step `align*` in `\small`/`\footnotesize`, steps stacked, no side column |
| a **figure** | the same **2/3 + 1/3** grid: figure in the main two-thirds, commentary in the right third. Same grammar as equations |
| a **definition / theorem** | `tddef{Term}` |
| a **worked example** | `exampleblock` |
| a **warning / the one caveat** | `alertblock` (red — counts as the slide's one red) |
| a plain aside or boxed note | `tdblock`, or put it in the margin |
| **code / commands** | `tdcode` inside a `[fragile]` frame |
| a **citation or side caveat** | the margin third (`tdmargin`), dim and small |
| the **punchline** | the single final `takeaway` |

### The 2/3 + 1/3 grid (the workhorse)

Equations and figures share one layout: the artefact lives in the main two-thirds,
its reading lives in the right third. This keeps a consistent grammar across the
deck — the eye learns that the right column always explains the left.

```latex
\begin{withmargin}
  \begin{tdmain}
    \[ \mathcal{J}(C,\mu)=\sum_k\sum_{x\in C_k}\lVert x-\textcolor{DHBWred}{\mu_k}\rVert^2 \]
  \end{tdmain}
  \begin{tdmargin}
    Sum of squared distances from each point to \textcolor{DHBWred}{its centroid}.
  \end{tdmargin}
\end{withmargin}
```

The accented term in the main column and its mention in the side third should be
the *same* red thing — that is how the explanation binds to the artefact.

### The derivation slide

When the point is the *steps*, not one equation, give them a whole slide and shrink
the font. No side column — the derivation is the content. Keep each line one move;
let the `align*` alignment carry the eye down the equals signs.

## Don'ts

- No bulleted agenda / table-of-contents slide. The agenda is designed, not listed.
- No second red on a slide. One accent, or none.
- No sans math — equations stay Palatino.
- No light background, no inverted figures — recolour figures with the dark-native
  styles (`tdbox`, `tufteplotdark`, …).
- No figure or equation tall enough to collide with the footer strip.
- No block used as a frame for ordinary prose — boxing must mean something.

## Quick checklist before a deck ships

- Title → "lecture in one slide" agenda → sections (with dividers) → final takeaway.
- Every slide: one idea, ~5 min of talk, at most one red thing.
- Equations and figures on the 2/3 + 1/3 grid; derivations on their own small-font slide.
- Blocks only where they carry status. `\section{}` set so the footer nav is real.
- Compiled twice; aux files cleaned.
