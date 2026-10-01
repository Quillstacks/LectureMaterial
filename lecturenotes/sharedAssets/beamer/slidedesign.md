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
- **Soft cap: 500 characters of body text per slide.** Count what the audience
  reads on the slide: prose, bullets, card text, table cells. Do not count the
  frame title, a `\sidecaption`, the `\slidesources` marker, or an equation.
  This is a *soft* cap and a prompt to split, not a rule to obey mechanically:
  when a slide runs over, the first question is always "is this two slides?"
  and the answer is usually yes. A slide over the cap with no figure, table or
  equation on it is a handout page, not a slide.
  - **Prefer the next slide to a fuller one.** Two slides at 300 characters
    beat one at 600. Slide count is free; attention is not.
  - **Copy then extend.** The cheapest way to spend the second slide: repeat
    the first one's layout and change one thing. Research data, then production
    data. The latency sample, then the same sample read as percentiles. The
    audience re-reads nothing and sees exactly what moved.
  - Every slide wants one visual: a figure, a table, an equation, or a
    `\sideimage` strip. A slide that is only sentences is the exception, and
    it had better be a short one.
- **Prose first.** Lead with a short sentence or two. Reach for `itemize` only when
  the content is a genuine list. Never a bulleted wall.
- **Exactly one red element per slide.** Every slide carries a single red accent,
  and never more: the key term in an equation, the one result, the active element,
  one word of the hook. If nothing is red, the slide is missing its point; if two
  things are red, nothing is.
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
| a **portrait / hero image** | `\sideimage` — the image bleeds the full slide height on one edge, concise text in the `sidebody` beside it (see below) |
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

### The full-height side image

For a portrait photograph, illustration, or a diagram that deserves to dominate,
let it bleed the full slide height on one edge and keep the text beside it, in
`\sideimage` + `sidebody`. This is the KIT "picture vertical" move: the image is
the hero, the side column is its caption. The strip is always 0.33 of the page
width, on every frame, whatever the image's own aspect: a photo is cover-cropped
into it, a drawing is scaled to fit it. Keep the frame title short — the image bleeds over the title strip on its
side. Prefer this over shrinking a striking portrait into a timid margin figure.

## Don'ts

- No bulleted agenda / table-of-contents slide. The agenda is designed, not listed.
- No second red on a slide, and never zero: exactly one accent, every slide.
- No sans math — equations stay Palatino.
- No light background, no inverted figures — recolour figures with the dark-native
  styles (`tdbox`, `tufteplotdark`, …).
- No figure or equation tall enough to collide with the footer strip.
- No block used as a frame for ordinary prose — boxing must mean something.
- No shrinking body text to make it fit. Body, cards, bullets and tables run at
  the theme default size (no `\small`, `\footnotesize`, `\scriptsize`, `\tiny`);
  when a frame overflows, cut words or change the layout (cards → table or
  bullets), never the font. Exceptions: the derivation slide, TikZ node fonts,
  the References `\bibfont`, and the margin column's own theme size.
- No inset or padded side figure, and no side figure at any width but 0.33. A
  side figure is always the full-height edge strip (`\sideimage`, `\sideimagecover`, `\sidedrawing`); a placeholder is the
  same strip on `placeholder_gray.png` with a `\sidecaption`.

## Quick checklist before a deck ships

- Title → "lecture in one slide" agenda → sections (with dividers) → final takeaway.
- Every slide: one idea, ~5 min of talk, at most one red thing.
- Equations and figures on the 2/3 + 1/3 grid; derivations on their own small-font slide.
- Blocks only where they carry status. `\section{}` set so the footer nav is real.
- Compiled twice; aux files cleaned.
