# Contributing to LectureMaterial

Thanks for helping improve these lecture notes. Most contributions come from students reading the PDFs and spotting something: a typo, a wrong formula, a confusing passage, a missing example. All of those are useful and welcome.

This guide is short on purpose. If something here is unclear, open an issue and say so.

## Two ways to contribute

**1. Open an issue.** Fastest path. Use one of the three templates:
- *Bug / Error in the notes* — typos, wrong math, broken references, missing figures
- *Unclear passage / Question* — a passage you cannot follow
- *Content suggestion* — propose a new example, exercise, citation, or topic

The templates ask for a chapter and page number, a screenshot, and (optionally but encouraged) a proposed fix. The more concrete, the faster it lands.

**2. Open a pull request.** Best for small fixes you are confident about (typos, a one-line equation correction, a clarified sentence). For larger changes, open an issue first so we can agree on direction before you invest time.

## Finding the source file for something you see in a PDF

The PDFs are built from LaTeX. To fix something, you need to edit the right `.tex` file.

```
lecturenotes/
  <series>/                              # e.g. notes_unsupervisedlearning
    <series>.tex                         # main file, builds the full book
    chapters/
      01_foundations.tex                 # one file per chapter — edit these
      02_centroid_clustering.tex
      ...
    chapter_pdfs/                        # per-chapter PDFs (build output)
    figures/
    literature/                          # .bib files
```

**Rule of thumb:** if a passage is on page X of chapter NN, edit `lecturenotes/<series>/chapters/NN_*.tex`. Do **not** edit files named `_ch_*.tex` or `draft.tex` — those are temporary build wrappers.

## Building locally

You need a working LaTeX install (TeX Live or MacTeX) with `latexmk`.

**Build the full book:**
```bash
cd lecturenotes/<series>
latexmk -pdf <series>.tex
```

**Build a single chapter (fast iteration):**
```bash
tools/draft.sh lecturenotes/<series> <chapter_basename>
# then build draft.tex in that folder
cd lecturenotes/<series> && latexmk -pdf draft.tex
```

**Rebuild all per-chapter PDFs:**
```bash
tools/build_chapter_pdfs.sh lecturenotes/<series>
```

If the build fails and you cannot tell why, attach the relevant lines from the `.log` file to your issue.

## Pull-request conventions

- **One fix per PR.** A PR that fixes one typo merges in minutes. A PR that fixes thirty things plus reorganises a section takes weeks.
- **Link the issue** it addresses (if one exists) in the PR description.
- **Show before and after.** A screenshot of the rendered PDF before and after your change makes review easy.
- **Confirm it builds.** Tick the checkbox in the PR template that says you compiled the affected file locally.
- **Do not commit build artifacts.** The `.gitignore` handles `.aux`, `.log`, `.pdf` wrappers, etc. If your `git status` shows a lot of these, something is off — ask before force-adding.
- **Keep the diff focused.** Do not reformat unrelated paragraphs in the same PR.

## Style notes

Each lecture-notes series may have a `DESIGN.md` (internal, not tracked) describing the writing and LaTeX conventions for that book. If your PR touches more than a one-line fix, look at neighbouring sections and mirror their style: section headings, math display, citation format, figure captions.

## Code of conduct

Be kind. Assume good faith. Disagreements about content are welcome; personal attacks are not. Issues or PRs that are rude, off-topic, or harass other contributors will be closed without discussion.

## Questions about contributing itself

If you are unsure whether something is worth reporting, report it. If you are unsure how to phrase an issue, open it anyway and say so. The cost of a low-quality issue is low; the cost of a problem that nobody flagged is higher.
