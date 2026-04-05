# Lecture Notes Skill

Instructions for agents writing or editing lecture notes in this repository.

## Repository Layout

```
lecturenotes/
  sharedAssets/
    tufte.cls          # Custom document class (Tufte-style, A5, tufte-book base)
    meta.tex           # Shared metadata: author, publisher, copyright, front matter macros
  notes_<coursename>/
    notes_<coursename>.tex          # Main document (preamble, front matter, chapter includes)
    <coursename>_references.bib     # BibTeX references for the course
    chapters/
      01_TopicName.tex              # Content chapters (numbered)
      aa_AppendixName.tex           # Appendix chapters (lettered aa, ab, ac, ...)
    figures/                        # All figures for this course
    library/                        # Source texts (epubs, PDFs) for reference
```

Each course is a self-contained directory. All courses share `tufte.cls` and `meta.tex` via relative path `../sharedAssets/`.

## Document Class and Preamble

- Use `\documentclass{../sharedAssets/tufte}` (never raw `tufte-book`).
- The class auto-loads `meta.tex`, which provides `\defaultauthor`, `\defaultpublisher`, `\makestandardfrontmatter`, `\makededication`, `\makeintroduction`, and `\loadoptionalfonts`.
- The main `.tex` file sets `\title`, `\author`, `\publisher`, then calls `\loadoptionalfonts` and adds course-specific packages.

### Standard front matter sequence

```latex
\begin{document}
\makestandardfrontmatter
\makededication{\openepigraph{"Quote"}{Source, Author}}
\tableofcontents
\makeintroduction{%
  Introduction text with \newthought{} paragraph openers.
}
\mainmatter
```

## Chapter Structure

Every content chapter follows an identical three-part structure. Do not deviate from this order.

### Part 1: Opening Block

```latex
\chapter{Topic Name}\index{Topic Name}

\newthought{Thematic Subtitle}

\marginnote{%                        % Literary source with QR code
  \begin{flushright}
  \newthought{Title}\\
  Author (Year)\\
  Full text via Wikisource:\\[4pt]
  {\color{black}\qrcode[height=1.2cm]{URL}}
  \end{flushright}%
}

\marginnote{\newthought{Case/Experiment.}   % Opening activity or case study
    \begin{enumerate}
        \item Step or fact one.
        \item Step or fact two.
    \end{enumerate}
}

\newthought{Literary hook sentence} connecting the assigned text to the theme.\\

\newthought{Contemporary framing sentence} connecting the theme to AI.

\vspace{3.5em}

\begin{tabular}{p{3.8cm} p{6.5cm}}
    \textbf{Required reading} & \textit{Title}\cite{key} by Author (Year; edition) \\[3pt]
    \textbf{Preparation}      & Complete the Guided Reading Sheet individually before the session. \\
\end{tabular}

\vspace{3.5em}
```

### Part 2: Guided Reading Sheet

```latex
\section*{Guided Reading Sheet}

\noindent Read \emph{Title} before the session. Work through the
questions below individually, then bring your notes to the discussion.

\begin{enumerate}
    \item Question connecting the literary text to the theme.
    \item Question probing a specific scene or concept.
    \item Question asking for personal experience or analogy.
    \item Question linking to a technical or policy dimension.
    \item Question requiring comparison across ethical frameworks.\\
\end{enumerate}
```

Always five questions. Each question is a full paragraph (3-4 sentences). The final `\item` ends with `\\`.

### Part 3: Opinion Landscape and Debate

```latex
\section*{Opinion Landscape and Debate}

\noindent \textbf{Format:} Surrounded-style debate. See
Appendix~A for the full protocol, speaker's list rules, and
moderator scripts.

\medskip
\noindent \textbf{Opening question:} [Provocative question framing the debate]
\marginnote{\newthought{Concept.} Definition\cite{key}.}

\newthought{Opinion~A, Label.}\quad [Thesis A stated in one sentence.]
\vspace{1.5em}

\medskip
\noindent\textbf{Role Name} -- [one-line role description].
    \begin{itemize}
        \item \textit{Talking point in first person, in character.}
        \item \textit{Second talking point.}
        \item \textit{Third talking point.}
    \end{itemize}

\marginnote{\newthought{Concept.} Short definition\cite{key}.}
\medskip
\noindent\textbf{Role Name} -- [one-line role description].
    \begin{itemize}
        \item \textit{...}
    \end{itemize}


\newthought{Opinion~B, Label.}\quad [Thesis B stated in one sentence.]
\vspace{1.5em}

% Two more roles, same pattern as above.


\newthought{Key Learnings}
\marginnote{\newthought{Teaser.} [One or two sentences previewing the next chapter's theme.]}
[Paragraph summarising the core insights. 4-6 sentences. No bullet points.]
```

Each opinion has exactly two roles. Each role has exactly three talking points in italics. Talking points are written in first person, in character.

## Style Rules

### Typography
- Use `\newthought{...}` to open new paragraphs or conceptual shifts (produces small caps lead-in). This is the primary structural rhythm device.
- Use `\marginnote{...}` for definitions, concepts, and contextual information. Keep them to 2-4 sentences.
- Use `\textit{...}` for talking points in debate roles and for book titles in running text.
- Use `\emph{...}` for emphasis within prose and for book titles in the reading sheet instructions.
- Use `\textbf{...}` sparingly: only for labels in tables, role names, and format headings.
- Use `\medskip`, `\bigskip`, `\vspace{1.5em}`, `\vspace{3.5em}` for vertical spacing. Never use `\vspace` with absolute units like `cm`.

### Dashes
- **Never use dashes in prose.** No `---` (em-dash), no `\textemdash{}`, no `--` as punctuation. Restructure the sentence instead (use a comma, a semicolon, parentheses, or split into two sentences). The only permitted use of `--` is for numeric ranges (e.g., `1--5`, `2014--2018`).

### Sectioning
- Chapters use `\chapter{...}`.
- Sections within chapters are always `\section*{...}` (unnumbered).
- Never use `\subsection` in content chapters. Subsections may appear in appendix chapters.
- Do not use comment-line separators (`% ----`) between sections. Use whitespace only.

### Comments
- The comment `% As a leading group, you are required to moderate this session...` appears after the opening case/experiment marginnote in every content chapter. Preserve it.
- Personal author notes are placed at the end of the main `.tex` file, prefixed with `% Hey Mark`.

### Citations and References
- Use `natbib` style: `\cite{key}` in text and margin notes.
- Bibliography style is `abbrvnat`.
- All references go in `<coursename>_references.bib`.
- Every margin note concept should cite at least one source.

### Index
- Add `\index{...}` to every `\chapter{}` call.
- Add `\index{...}` to significant concepts, author names, and text titles where they first appear.

### Figures
- Place all figures in the `figures/` directory.
- Use `\includegraphics` with captions that explain what the figure shows and why it matters.
- Cite the source in the caption or an adjacent margin note.

### QR Codes
- Each chapter's literary source gets a QR code in the opening margin note linking to the full text (preferably Wikisource).
- Use `\qrcode[height=1.2cm]{URL}` wrapped in `{\color{black}...}`.

## Appendix Conventions

- Appendix files use letter prefixes: `aa_`, `ab_`, `ac_`, etc.
- Appendix chapters use `\chapter{...}` (LaTeX auto-numbers them A, B, C after `\appendix`).
- Appendices contain procedural/structural content (preparation guides, debate protocols), not session content.

## Main Document Conventions

- Each content chapter is included with `\input{chapters/XX_Name.tex}` followed by `\newpage`.
- Appendix chapters come after `\appendix`.
- The introduction uses `\makeintroduction{...}` with `\newthought{}` paragraph openers and a `\begin{itemize}` lecture outline at the end.

## What Not To Do

- Never use dashes in prose (`---`, `\textemdash{}`, or `--` as punctuation). Restructure the sentence instead. `--` is only for numeric ranges.
- Never use numbered sections (`\section{}`) in content chapters.
- Never use `\subsection` in content chapters.
- Never add comment-line separators (`% -----`).
- Never create new document classes or override `tufte.cls` locally.
- Never add packages to `tufte.cls`; add them in the course's main `.tex` file.
- Never write margin notes longer than 4 sentences.
- Never write talking points outside of italics or outside first person.
- Never break the three-part chapter structure (Opening, Reading Sheet, Debate).
- Never omit the Key Learnings paragraph or the Teaser margin note at the end of a chapter.
