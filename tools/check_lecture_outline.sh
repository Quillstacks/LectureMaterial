#!/usr/bin/env bash
# Check that slides/lecture_outline.tex still agrees with the chapters.
# Usage: tools/check_lecture_outline.sh <slides_dir>
#
# Why. The orientation deck announces every lecture's subchapters, and each
# chapter opens with the same card. Those used to be two hand-typed copies and
# they drifted: ch01's first subchapter was renamed to "The small part and the
# big picture" while ch00 still said "When to Use Machine Learning" for weeks.
# Now both render from lecture_outline.tex, and this script is the other half:
# it compares that file against the \subsection commands the chapters actually
# declare, so renaming a subchapter without updating the outline is caught at
# build time instead of at lecture time.
#
# "Summary" subchapters are ignored on both sides: they are real subsections
# but they are deliberately left off the cards.
#
# Exit 0 when they agree, 1 when they do not. Called by
# build_slide_chapter_pdfs.sh, and safe to run on its own.
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <slides_dir>" >&2
  exit 2
fi

SLIDES_DIR="$(cd "$1" && pwd)"
OUTLINE="$SLIDES_DIR/lecture_outline.tex"

if [[ ! -f "$OUTLINE" ]]; then
  echo "check_lecture_outline: no $OUTLINE, nothing to check" >&2
  exit 0
fi

# chNN -> roman numeral, the same mapping the \lecturepage calls use.
romans=(I II III IV V VI VII VIII IX X XI)

status=0
for n in $(seq 1 11); do
  nn=$(printf '%02d' "$n")
  roman="${romans[$((n - 1))]}"
  chapter=$(ls "$SLIDES_DIR"/ch${nn}_*.tex 2>/dev/null | head -1 || true)
  [[ -n "$chapter" && -f "$chapter" ]] || continue

  # What the chapter declares.
  declared=$(grep -oE '^\\subsection\{[^}]*\}' "$chapter" \
    | sed -E 's/^\\subsection\{//; s/\}$//' \
    | grep -vx 'Summary' || true)

  # What the outline promises: the body of \td@setlecture{<roman>}{title}{items},
  # one item per line, trailing \\[0.2em] stripped.
  listed=$(awk -v r="$roman" '
    $0 ~ ("^\\\\td@setlecture\\{" r "\\}") { grab = 1; next }
    grab && /^\}[[:space:]]*$/ { exit }
    grab { print }
  ' "$OUTLINE" | sed -E 's/^[[:space:]]+//; s/\\\\\[0\.2em\][[:space:]]*$//' \
    | grep -v '^$' || true)

  if [[ "$declared" != "$listed" ]]; then
    status=1
    echo "check_lecture_outline: lecture $roman ($(basename "$chapter")) disagrees with lecture_outline.tex" >&2
    diff <(echo "$listed") <(echo "$declared") \
      | sed 's/^</  outline: /; s/^>/  chapter: /' >&2 || true
  fi
done

if [[ $status -eq 0 ]]; then
  echo "check_lecture_outline: outline matches all chapters"
else
  echo "check_lecture_outline: fix lecture_outline.tex (or the \\subsection) and rebuild" >&2
fi
exit $status
