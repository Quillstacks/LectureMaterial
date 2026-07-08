# Build the Disciplined Vibe decks with the shared tuftedark theme.
# The theme .sty lives two directories up in sharedAssets/beamer; put it on
# TEXINPUTS so the decks find it without copying the theme in here.
# lualatex is required (academicons needs a Unicode engine); footer nav needs
# two passes, which latexmk handles automatically.
ensure_path('TEXINPUTS', '../../sharedAssets/beamer//');
$pdf_mode = 4;   # 4 = lualatex
$lualatex = 'lualatex -shell-escape -interaction=nonstopmode -synctex=1 %O %S';
