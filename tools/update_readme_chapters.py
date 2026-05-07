#!/usr/bin/env python3
"""Regenerate per-lecture chapter tables in README.md.

For each `<!-- BEGIN:lecture:<book> --> ... <!-- END:lecture:<book> -->`
block in README.md, scan `lecturenotes/<book>/chapter_pdfs/*.pdf` and
extract the human-readable chapter title from the matching
`lecturenotes/<book>/chapters/<stem>.tex` via `\\chapter{...}`, then
rewrite the block as a `<details>` dropdown with a 3-column table.

Usage:
    tools/update_readme_chapters.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
BASE_URL = "https://material.schutera.com/lecturenotes"

CHAPTER_RE = re.compile(r"\\chapter\*?\{([^}]+)\}")
INDEX_RE = re.compile(r"\\index\{[^}]*\}")
APPENDIX_PREFIX = re.compile(r"^a[a-z]_")  # aa_, ab_, ac_, ...

LECTURE_TITLES = {
    "notes_philosophyofai": "Philosophy of AI",
    "notes_unsupervisedlearning": "Unsupervised Deep Learning",
    "notes_numerischemethoden": "Numerical Methods",
    "notes_missingsemester": "Full Stack Handwerkszeug",
}


def detex(s: str) -> str:
    s = INDEX_RE.sub("", s)
    s = s.replace(r"\&", "&").replace(r"\#", "#").replace(r"\%", "%")
    s = s.replace("|", r"\|")
    return re.sub(r"\s+", " ", s).strip()


def chapter_title(book_dir: Path, stem: str) -> str:
    tex = book_dir / "chapters" / f"{stem}.tex"
    if tex.exists():
        for line in tex.read_text(encoding="utf-8", errors="replace").splitlines():
            m = CHAPTER_RE.search(line)
            if m:
                return detex(m.group(1))
    return stem.split("_", 1)[-1].replace("_", " ").title()


def number_label(stem: str) -> str:
    head = stem.split("_", 1)[0]
    if head.isdigit():
        return f"{int(head):02d}"
    if APPENDIX_PREFIX.match(stem) and len(head) == 2:
        return head[1].upper()
    return head.upper()


def build_block(book: str) -> str:
    full_title = LECTURE_TITLES.get(book, book)
    book_dir = REPO_ROOT / "lecturenotes" / book
    base = f"{BASE_URL}/{book}"
    full_pdf = f"{base}/{book}.pdf"

    rows = [f"| Full | {full_title} · Lecture Notes | [📄 PDF]({full_pdf}) |"]

    chapter_dir = book_dir / "chapter_pdfs"
    if chapter_dir.is_dir():
        pdfs = sorted(chapter_dir.glob("*.pdf"))
        numeric = [p for p in pdfs if not APPENDIX_PREFIX.match(p.stem)]
        appendix = [p for p in pdfs if APPENDIX_PREFIX.match(p.stem)]

        for p in numeric:
            label = number_label(p.stem)
            title = chapter_title(book_dir, p.stem)
            url = f"{base}/chapter_pdfs/{p.name}"
            rows.append(f"|  {label}  | {title} | [📄 PDF]({url}) |")

        for i, p in enumerate(appendix):
            label = chr(ord("A") + i)
            title = chapter_title(book_dir, p.stem)
            url = f"{base}/chapter_pdfs/{p.name}"
            rows.append(f"|   {label}  | {title} *(Appendix)* | [📄 PDF]({url}) |")

    return (
        '<details markdown="1">\n'
        "<summary>📑 <b>Lecture Notes</b></summary>\n"
        "\n"
        "|   #  | Chapter | Download |\n"
        "| :--: | :--- | :-: |\n"
        + "\n".join(rows) + "\n"
        "\n"
        "</details>"
    )


def main() -> int:
    text = README.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(<!-- BEGIN:lecture:(\w+) -->)(.*?)(<!-- END:lecture:\2 -->)",
        re.DOTALL,
    )

    def replace(m: re.Match) -> str:
        begin, book, _, end = m.group(1), m.group(2), m.group(3), m.group(4)
        return f"{begin}\n{build_block(book)}\n{end}"

    new_text, n = pattern.subn(replace, text)
    if n == 0:
        print("warning: no lecture markers found in README.md", file=sys.stderr)
        return 0
    if new_text != text:
        README.write_text(new_text, encoding="utf-8")
        print(f"updated README.md ({n} block{'s' if n != 1 else ''})")
    else:
        print(f"README.md already up to date ({n} block{'s' if n != 1 else ''})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
