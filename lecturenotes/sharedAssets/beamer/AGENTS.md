# Agent guide — the `tuftedark` slide theme

You are looking at the shared slide theme for Prof. Schutera's lecture courses:
a dark, DHBW-coloured beamer theme whose **structure is ported from the official
KIT corporate-design beamer template** and recoloured for a dark canvas. This file
tells you where everything is, how to build it, and the rules to follow when
authoring decks or editing the theme. For *which* layout to use for *which* kind
of content, read the companion [slidedesign.md](slidedesign.md).

## Files

- `beamerthemetuftedark.sty` — the theme. One file: palette, fonts, colours,
  inner theme, background card, title/section pages, footer, blocks, margin
  layout, and the dark figure vocabulary. Invoked with `\usetheme{tuftedark}`.
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
\title[Short Title]{Full Title}            % short forms feed the footer
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
- Set the short title/author; the footer shows `author – short title`.

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

**Figures — always dark-native, never inverted.** Use the parallel light-on-dark
styles, the twins of the print TikZ / tufteplot vocabulary:
- TikZ: `td`, `tdbox`, `tdboxhi` (red highlight), `tdarr`, `tdarrhi`, `tdarrdim`
  (dashed grey). E.g. `\node[tdbox]{...}; \draw[tdarr] ... ;`.
- pgfplots: the `tufteplotdark` axis style (no frame, outside thin ticks, white
  strokes). Highlight a point with `DHBWred`.
- A figure must clear the **12 mm footer strip**: keep plot `height` modest
  (≈`0.40\textwidth`) or content collides with the footer.

## Palette (defined in the theme)

`DHBWred` `#E2001A` (HKS 14, the only accent) · `DHBWgray` `#717776` (HKS 92) ·
`tdpage` `#050505` (page/margin behind the card) · `tdcard` `#17181A` (content
card) · `tdfg` `#F2F2F2` (text) · `tddim` `#9A9A9A` (de-emphasis) · `tdrule`
(hairlines). Block fills: `tdblocktitle`, `tdblockbody`, `tdexbody`.

## Conventions (do not drift from these)

- **Dark only.** Near-black card on a darker page. No light variant.
- **Red is the single accent, used sparingly.** The highlighted equation term,
  `\alert{...}`, the takeaway, `alertblock`, the section/title accent rules. Body
  text, bullets, frame-title rules, and the footer are off-white / grey — **never
  red in the footer**.
- **Sans body + serif math.** Source Sans for text and titles; Palatino for math
  (`mathpazo`). Do not switch equations to a sans math font.
- **Prose-first.** Lead with short prose; reserve `itemize` for genuine lists.
- **Footer** = KIT mini-frame navigation (section names + per-frame circles that
  fill off-white as you advance) over `author – title` / `date  n/total`. It is
  driven by `\section{}` and the short title/author.

## Gotchas

- **Compile twice** (footer nav). A one-pass PDF looks broken; that is expected.
- **`\MakeUppercase` crashes** here (LaTeX3 `\__text_expand_space:w` clash). Use
  `\uppercase\expandafter{...}` instead, as the title page does.
- **Verbatim needs `[fragile]`** frames (the code slide).
- **Figure height** must respect the footer strip (see above).
- Editing the theme: keep `demo.tex` building and re-render to verify visually;
  this theme has a lot of pgf/beamer-internal code (the custom `\slideentry` that
  drives the cumulative circle fill) where a silent wrong number breaks the nav.

When in doubt about *what kind of slide to build for a given purpose*, defer to
[slidedesign.md](slidedesign.md) — that is the editorial guide; this file is the
mechanical one.
