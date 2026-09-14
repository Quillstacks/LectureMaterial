# Build the AI Foundations deck with the shared tuftedark theme.
# The theme .sty lives two directories up in sharedAssets/beamer; put it on
# TEXINPUTS so the deck finds it without copying the theme in here.
# lualatex is required (the theme's font stack needs a Unicode engine); the
# footer nav needs two passes, which latexmk handles automatically.
ensure_path('TEXINPUTS', '../../sharedAssets/beamer//');
$pdf_mode = 4;   # 4 = lualatex
$lualatex = 'lualatex -shell-escape -interaction=nonstopmode -synctex=1 %O %S';
