# Slide images

Drop images for the deck here (`.png`, `.jpg`, `.pdf`).

The master sets `\graphicspath{{images/}}`, so include by bare filename, no path:

```latex
\includegraphics[width=\linewidth]{dino}          % images/dino.png
\includegraphics[width=0.6\textwidth]{smart-zone} % images/smart-zone.pdf
```

A common full-bleed pattern on this dark theme:

```latex
\begin{frame}{Title}
  \centering
  \includegraphics[width=\linewidth]{myfigure}
\end{frame}
```

## Bringing an image in beside text (do NOT box it in a column)

Do not drop a photo into a `\begin{column}{0.42\textwidth}\includegraphics[width=\linewidth]`
padded box. On this dark theme it reads as a small floating rectangle with dead
space around it -- ugly. Use the theme's **side-image hero** instead: the image
bleeds the full slide height on one edge and the text is held on the other side.
This is the default way to pair an image with text here.

```latex
\begin{frame}{Title}
  \sideimage[0.33]{myfigure}   % right strip, full height, ~33% wide. Call it FIRST.
  \begin{sidebody}
    ... all the text (blocks, itemize, ...) goes here ...
  \end{sidebody}
\end{frame}
```

- The optional arg is the width fraction reserved for the image. Match it to the
  image's natural width at full slide height: a portrait ~0.33, a near-square ~0.6.
- `\sideimage*[..]{..}` puts the strip on the LEFT (keep the title short then --
  the image bleeds over the title/footer on its strip).
- `\sideimagecover[..]{..}` centre-crops the image to fill the strip exactly; use
  it for a photo whose aspect does not match the strip. `\sideimage` keeps the
  image whole (better for diagrams).
- **A landscape image will not fill a tall one-third strip.** Rotate it to
  portrait first: `sips -r 90 images/foo.jpeg` (macOS). Then `\sideimage` fills
  the strip and the `[frac]` you pass matches its new width.
- Definitions live in the theme `.sty` (`\sideimage`, `sidebody`, `withmargin` /
  `tdmain` / `tdmargin` for the softer in-flow Tufte margin third).

Animated GIFs are handled separately by the theme's `\gif{clip}` command, which
reads from a `gifs/` folder, not this one. See the theme `.sty` for details.
