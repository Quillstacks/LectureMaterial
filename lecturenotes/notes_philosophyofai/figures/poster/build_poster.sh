#!/usr/bin/env bash
# Build this poster from one statue image.
#
#   ./build_poster.sh                       rebuild from statue.jpeg
#   ./build_poster.sh ~/Downloads/new.jpeg   swap the statue, then rebuild
#
# The picture is placed as is: a statue on a plain light ground, as the
# Gemini renders come. The generator lifts the ground (gray 243, the
# white_point in the json) to paper white and trims the empty margins; no
# cutout. Texts and sizes live in the json next to this script; the output
# lands beside it as .png and .pdf (A3 at 300 dpi, scales to A4 and A2 in
# the print dialog). For a photo with a dark backdrop, make_cutout.py cuts
# a transparent PNG and the json's "cutout" can point at that instead.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$(git rev-parse --show-toplevel)"

if [ $# -ge 1 ]; then
    cp "$1" statue.jpeg
fi
python3 "$ROOT/tools/poster_compose.py" ./*.json
