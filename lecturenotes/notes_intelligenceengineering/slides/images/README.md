Slide images for the Intelligence Engineering deck.

Drop files here and include them by bare name, the master sets
`\graphicspath{{images/}}`:

    \includegraphics[width=\linewidth]{backbone}
    \sideimage[0.36]{portrait}

Until an asset exists, use the placeholder box: `\phimg[0.6]{backbone}`.

## Hand drawn figures from the iPad

Mark sketches figures in Apple Notes on the iPad, one drawing per note, the
note named after the file it becomes (`IEa`, `IEb`, ...). Notes syncs them to
the Mac, and one command pulls a drawing out and recolours it for the dark
deck (white page transparent, black ink off-white, red ink DHBW red, strokes
thickened, padded to clear the title and footer):

    tools/notes_drawing.py IEb lecturenotes/notes_intelligenceengineering/slides/images/IEb.png

It prints the drawing's width fraction at full height. The slide ignores it:
every side figure takes the same 0.33 strip, and \sidedrawing scales the
drawing to fit that strip.

    \sidedrawing{IEb}                % beside a sidebody, like \sideimage
    \fulldrawing{IEc}{caption}        % the drawing is the whole slide

Re-run the command after editing the drawing on the iPad; nothing else moves.
