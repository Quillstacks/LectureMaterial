# Agent guide — the `tuftedark` slide theme

You are looking at the shared slide theme for Prof. Schutera's lecture courses:
a dark, DHBW-coloured beamer theme whose **structure is ported from the official
KIT corporate-design beamer template** and recoloured for a dark canvas. This file
tells you where everything is, how to build it, and the rules to follow when
authoring decks or editing the theme. For *which* layout to use for *which* kind
of content, read the companion [slidedesign.md](slidedesign.md).

## Files

- `beamerthemetuftedark.sty` — the theme. One file: palette, fonts, colours,
  inner theme, the two-band background (grey content + dark footer), title/section
  pages, footer, blocks, margin layout, and the dark figure vocabulary. Invoked
  with `\usetheme{tuftedark}`.
- `demo.tex` / `demo.pdf` — a showcase deck exercising every layout. Treat it as
  the living reference: if you add a feature to the theme, demonstrate it here.
- `AGENTS.md` (this file) and `slidedesign.md` — documentation.

## Build

```
pdflatex demo.tex      # run TWICE
pdflatex demo.tex
```

The footer navigation reads `demo.nav`, written on the first pass, so a
**single pass shows an empty/half-built footer**. Always compile twice. Clean the
aux files (`.aux .log .nav .snm .out .toc .vrb .fls .fdb_latexmk`) when done; keep
only `.tex`, `.sty`, `.pdf`. The theme `.sty` must sit on `TEXINPUTS` — in
practice, keep the deck in this directory (next to the `.sty`) or export the path.

## Starting a deck

```latex
\documentclass[aspectratio=169]{beamer}   % 16:9
\usetheme{tuftedark}
\title[Short Title]{Full Title}            % short forms used on the title page
\author[Surname]{Full Name}
\institute{DHBW Ravensburg}
\date{\today}
\AtBeginSection[]{\begin{frame}\sectionpage\end{frame}}  % auto dividers
\begin{document}
\begin{frame}[plain]\titlepage\end{frame}
\section{...}
\begin{frame}{Frame title}...\end{frame}
\end{document}
```

- Use `\section{...}` (and optionally `\subsection`) — the footer nav is built
  from sections, so a deck with no sections has an empty nav.

## Theme API (what you can use in a deck)

**Layouts / structure**
- Title page: `\begin{frame}[plain]\titlepage\end{frame}`.
- Section divider: `\sectionpage` (auto via the `\AtBeginSection` hook above).
- Standard frame: `\begin{frame}{Title} ... \end{frame}`.
- Two columns: `\begin{columns}[T]\begin{column}{.5\textwidth}...\end{column}...\end{columns}`.

**Blocks**
- Native, rounded, KIT-style: `block` (grey title bar), `exampleblock` (lighter
  grey), `alertblock` (DHBW red — reserved for warnings / the one thing not to miss).
- `\begin{tddef}{Term}...\end{tddef}` — titled definition/theorem box (red title).
- `\begin{tdblock}...\end{tdblock}` — plain bordered box, no title bar.
- `\begin{tdcode}...\end{tdcode}` — dark code panel; put a `Verbatim` inside and
  mark the frame `[fragile]`.
- `\begin{takeaway}...\end{takeaway}` — one centred red statement (the punchline).

**Margin column** (Tufte sidenotes)
```latex
\begin{withmargin}
  \begin{tdmain} ...body... \end{tdmain}
  \begin{tdmargin} sidenote, citation, small figure \end{tdmargin}
\end{withmargin}
```

**Full-height side image** (`\sideimage`) — a portrait image bleeds the full
slide height on one edge, text confined to the other side. Ported from the KIT
corporate "picture NN vertical" layout.
```latex
\begin{frame}{Title}                 % keep the title short: the image
  \sideimage[0.33]{portrait}         % bleeds over the title strip on its side
  \begin{sidebody} ...concise text... \end{sidebody}
\end{frame}
```
The optional argument is the width fraction reserved for the image. **Always
0.33** (Mark, 2026-09-30): every side figure in a deck takes the same strip, so
the text column never jumps width from frame to frame. Do not size the strip to
the image; fit the image to the strip instead (cover-crop a photo, scale a
drawing to fit). `\sideimage` puts the image at the right edge; `\sideimage*`
at the left. The text column is the image's caption, so keep it concise.

`\sideimagecover[0.33]{img}` is the same, but **cover-crops** the image to fill a
strip of exactly the reserved width at full height (centre crop) — use it to
force a photo or near-square screenshot into a full-height one-third strip. Use
plain `\sideimage` for a diagram that must stay whole (no crop).

**Figures — always dark-native, never inverted.** Use the parallel light-on-dark
styles, the twins of the print TikZ / tufteplot vocabulary:
- TikZ: `td`, `tdbox`, `tdboxhi` (red highlight), `tdarr`, `tdarrhi`, `tdarrdim`
  (dashed grey). E.g. `\node[tdbox]{...}; \draw[tdarr] ... ;`.
- pgfplots: the `tufteplotdark` axis style (no frame, outside thin ticks, white
  strokes). Highlight a point with `DHBWred`.
- A figure must clear the **footer**: keep plot `height` modest
  (≈`0.40\textwidth`) or content collides with the footer.

## Palette (defined in the theme)

`DHBWred` `#E2001A` (HKS 14, the only accent) · `DHBWgray` `#717776` (HKS 92) ·
`tdpage` `#050505` (page + recessed footer margin, darkest) · `tdcard` `#16171B`
(lighter content card) · `tdfg` `#F2F2F2` (text) · `tddim` `#9A9A9A`
(de-emphasis, also the mini-frame grey) · `tdrule`
(hairlines). Block fills: `tdblocktitle`, `tdblockbody`, `tdexbody`.

## Conventions (do not drift from these)

- **Dark only.** A lighter content card (`tdcard`) on a darker page (`tdpage`) --
  the KIT structure inverted for dark mode. The footer navigation is recessed in
  the dark page margin below the card, separated by the rounded card edge. No
  light variant.
- **Red is the single accent, used sparingly.** The highlighted equation term,
  `\alert{...}`, the takeaway, `alertblock`, the section/title accent rules. Body
  text, bullets, frame-title rules, and the footer are off-white / grey — **never
  red in the footer**.
- **Sans body + serif math.** Source Sans for text and titles; Palatino for math
  (`mathpazo`). Do not switch equations to a sans math font.
- **Prose-first.** Lead with short prose; reserve `itemize` for genuine lists.
- **Footer** = the standard KIT mini-frame navigation (section names + per-frame
  grey circles; only the *current* frame is filled, the rest hollow, other
  sections dimmed) recessed in the dark page margin below the card, with the
  slide counter `n / total` on the *same row* at the right edge. One full-width
  `beamercolorbox`, driven by `\section{}`.

## Gotchas

- **Compile twice** (footer nav). A one-pass PDF looks broken; that is expected.
- **`\MakeUppercase` crashes** here (LaTeX3 `\__text_expand_space:w` clash). Use
  `\uppercase\expandafter{...}` instead, as the title page does.
- **Verbatim needs `[fragile]`** frames (the code slide).
- **Figure height** must respect the footer (see above).
- Editing the theme: keep `demo.tex` building and re-render to verify visually.
  The navigation is now beamer's stock `\insertnavigation` (no custom
  `\slideentry`); recolour via the `mini frame` beamer-colour, do not reintroduce
  a cumulative-fill override.

When in doubt about *what kind of slide to build for a given purpose*, defer to
[slidedesign.md](slidedesign.md) — that is the editorial guide; this file is the
mechanical one.
