---
name: addsome
description: Adds one book, film, or video to Appendix C "Further Reading & Watching" of the Philosophy of AI notes, with a bib entry, an entry in the right section, a local build, and a pull request, or adds one like to an entry already there. Use when someone wants to add, suggest, recommend, or like a book, novel, film, series, talk, lecture, interview, or video essay for these notes.
---

# Add an entry to Further Reading & Watching

Appendix C is an open collection of books, films, and videos that came up
around the sessions. This skill adds one entry to it, end to end.

Adding an entry is a contribution to the notes, not coursework. Do the LaTeX,
the bib entry, the build, and the pull request in full (see "When full help
is appropriate" in the root `AGENTS.md`). What the work says about the course
is the person's own judgement: ask for it, shape it, never write it from your
own knowledge.

One run adds one entry and ends in one pull request.

## Files

| File | Role |
|---|---|
| `chapters/ad_FurtherReadingWatching.tex` | the appendix, sections Reading, Films, Videos |
| `philosophyofai_references.bib` | one bib entry per work |
| `notes_philosophyofai.tex` | the book, build it to check the entry |

All paths are relative to `lecturenotes/notes_philosophyofai/`.

## 1. Ask

Ask one question at a time and wait for each answer.

- Which work: title, author or director, year. For a video, the link.
- What is it about, in a few sentences of their own. The entry keeps one
  line of it, so ask which image or question matters most.
- Where does it touch the course? Which session themes does it serve
  (Anthropomorphism, Accountability, Agency, Embodiment), or does it span the
  course (General)? Which vibe, idea, thought, or theme does it connect to?

If the answer to the last question is thin ("it's about AI"), ask what scene,
argument, or character made them think of the course. You may check facts
(spelling, year, director) and fix them; say what you changed.

Then check that the work is not already in:

```bash
grep -n -i "<title>" chapters/ad_FurtherReadingWatching.tex philosophyofai_references.bib
```

## 2. Add the bib entry

Append it to the end of `philosophyofai_references.bib`. The key is the
lowercase surname of author or director, the year, and the first content word
of the title: `adams1979hitchhiker`, `garland2015exmachina`. Brace a title
whose capitals must survive: `{{Ex Machina}}`.

Book, with the German edition (if one exists) and a Google Scholar search
link in `note`:

```bibtex
@book{herbert1965dune,
    author    = {Frank Herbert},
    title     = {Dune},
    year      = {1965},
    publisher = {Chilton Books},
    address   = {Philadelphia},
    note      = {German edition \textit{Der W{\"u}stenplanet}. \url{https://scholar.google.com/scholar?q=Dune+Frank+Herbert}}
}
```

Accents go in braces: `L'{\'E}tranger`. For a translation, `note` also names
the original: `First published as \textit{Sofies verden}, Aschehoug, Oslo, 1991.`

No `%` in any URL, so no `%27` for an apostrophe: drop the character. The
`\bibentry` in the margin note reads `%` as a comment and prints an empty
reference, without an error.

Film, with the studio or distributor in `note`:

```bibtex
@misc{garland2015exmachina,
    author       = {Alex Garland},
    title        = {{Ex Machina}},
    year         = {2015},
    howpublished = {Film},
    note         = {A24 / Universal Pictures}
}
```

Video, with the channel and the link in `howpublished` and the access date
in `note`:

```bibtex
@misc{kurzweil2009coming,
    author       = {Ray Kurzweil},
    title        = {{The Coming Singularity}},
    year         = {2009},
    howpublished = {Big Think, \href{https://www.youtube.com/watch?v=1uIzS1uCOcE}{youtube.com}},
    note         = {Accessed: 2026-11-19}
}
```

## 3. Write the entry

The template, from the comment at the top of the chapter file:

```latex
\medskip
\noindent\textbf{Title}\index{Title} by Author or Director (year).%
\entrynote{\likes{0}
\newthought{First words} of one line, at most 50 characters,
on what the work is about.\\
\textit{Connects to: Theme, idea, or thought.}\\
\bibentry{bibkey}}
```

`\likes{0}` is the like counter, a gray heart and a number on the first
line of the margin note. A new entry starts at 0. Use `\bibentry`, never `\cite`,
inside the margin note.

`\entrynote` sets the margin note and leaves as much room below the title
line as the note is tall, so every note stands next to its own entry. Use it
instead of `\marginnote` for every entry, and add no `\vspace` by hand.

Two works that belong together, a novel series or a film and its sequel,
share one entry: both titles in bold, both years, one `\bibentry` per work.

```latex
\noindent\textbf{Dune} and \textbf{Dune: Part Two}\index{Dune} by Denis Villeneuve (2021, 2024).%
\entrynote{\likes{0}
\newthought{Paul foresees the holy war.} Is he to blame?\\
\textit{Connects to: Accountability, Agency.}\\
\bibentry{villeneuve2021dune}\\
\bibentry{villeneuve2024dune}}
```

A video names speaker and channel:
`by Ray Kurzweil\index{Kurzweil, Ray}, Big Think (2009).`

Placement:

- Append the entry at the end of its section: Reading, Films, or Videos.
  The sections have no subtitles; the "Connects to" line carries the theme.
- Each section opens with `\collection{...}`, which starts a new page and
  draws the rule. Add no heading, `\clearpage`, or `\vspace` of your own.
- The first entry under a `\collection{...}` heading has no `\medskip`.
  Every later entry starts with `\medskip`.
- Index the title, and the author or speaker as `\index{Surname, First}`.
  A title with a leading article or accent gets a sort key:
  `\index{Etranger@L'\'Etranger}`, `\index{Mythe de Sisyphe, Le}`.

Writing rules:

- Build the line from the person's answers. Show it to them and let them
  change it before you go on.
- One line of at most 50 characters, spaces included, without the "Connects
  to" line and the reference. Count with `printf '%s' "<line>" | wc -m`
  before you build. The line names the core of the work,
  the image or question that ties it to the course: "Forty-two: an exact
  answer to an unknown question." Cut praise ("brilliant", "a must-see").
- Leave the ending out unless the course point depends on it.
- No dashes as punctuation, no `\emph`. The link lives in the bib entry, never
  in the paragraph.
- "Connects to" lists the session themes the work touches, in course order:
  Anthropomorphism, Accountability, Agency, Embodiment. A work that spans
  the course connects to General. An idea or thought of the person's own
  may follow the themes.

Touch nothing else: no other entry, no other margin note, no main file, no PDF, no
`chapter_versions.tex`.

## 4. Build and check

From `lecturenotes/notes_philosophyofai/`:

```bash
latexmk -pdf -jobname=entrycheck notes_philosophyofai.tex
grep -n "undefined\|Error" entrycheck.log
```

The `-jobname` keeps the build away from the tracked `notes_philosophyofai.pdf`.
Use `latexmk -pdf`. Plain `latexmk` builds a DVI and stops on errors. Every
build also rewrites the tracked `chapter_versions.tex`; leave it unstaged
and run `git restore chapter_versions.tex` when you are done.

The grep should print nothing new. Open `entrycheck.pdf` at Appendix C and
check:

- the entry sits in the right section, with the title in bold,
- the margin note stands beside its own title line, holds the line and the
  `\bibentry` reference with capitals intact, and the next entry starts
  below it,
- the gray heart and 0 open the margin note, directly above the small caps,
- the "Connects to" line is in italics on its own line.

Take a screenshot of the entry for the pull request, then delete
`entrycheck.pdf`.

## 5. Open the pull request

Stage the two source files by name, never `git add .`:

```bash
git switch -c philosophyofai-further-reading-<short-title>
git add chapters/ad_FurtherReadingWatching.tex philosophyofai_references.bib
git commit -m "notes_philosophyofai: Further Reading & Watching gains <Title>"
```

Ask before you push or open the pull request: both go out under the person's
GitHub account. Without write access to the repository, push to their fork.
Fill in `.github/PULL_REQUEST_TEMPLATE.md`:

- Linked issue: n/a, unless one exists.
- What this changes: the work and the section it went into.
- Why: their sentence on where it touches the course.
- After: the screenshot from step 4. Before: "new entry".
- Checklist: tick what is true.

## A like instead of an entry

If the person only wants to like a work that is already in the appendix,
raise the number in its `\likes{n}` by one and change nothing else. Stage
`chapters/ad_FurtherReadingWatching.tex` alone, commit as
`notes_philosophyofai: one like for <Title>`, and open the pull request as in
step 5. The build in step 4 is optional for a like.
