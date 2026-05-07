$force_mode = 1;
$bibtex_use = 2;

# After a successful main-book compile, also (re)build the standalone chapter
# PDFs under chapter_pdfs/. The env-var guard prevents infinite recursion:
# tools/build_chapter_pdfs.sh invokes latexmk per chapter wrapper, and those
# nested latexmk runs read this same .latexmkrc — without the guard their
# own $success_cmd would re-trigger the script.
$success_cmd = '[ -z "$LECTURENOTES_AUTOBUILD_CHAPTERS" ] && '
             . 'export LECTURENOTES_AUTOBUILD_CHAPTERS=1 && '
             . 'TOOLS_DIR="$(git rev-parse --show-toplevel 2>/dev/null)/tools" && '
             . '[ -x "$TOOLS_DIR/build_chapter_pdfs.sh" ] && '
             . '"$TOOLS_DIR/build_chapter_pdfs.sh" "$(pwd)" '
             . '|| true';
