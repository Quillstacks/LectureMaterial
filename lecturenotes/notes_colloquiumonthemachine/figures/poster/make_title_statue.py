#!/usr/bin/env python3
"""The poster's statue for the deck's white title page.

Lifts the picture's light ground to paper white, with the poster's own
white_point, and fades the picture out towards its edges, so neither the
ground nor the cut floor shadow draws a box on the white slide.

Usage: make_title_statue.py <statue.jpeg> <poster.json> <out.png>
"""
import json
import sys
from PIL import Image

src, spec, out = sys.argv[1:4]
wp = json.load(open(spec))["white_point"]
im = Image.open(src).convert("RGB").point(lambda v: min(255, round(v * 255 / wp)))
W, H = im.size

# the statue itself, without its floor shadow
x0, y0, x1, y1 = im.convert("L").point(lambda v: 255 if v < 190 else 0).getbbox()
PAD = 12
top, bot = max(0, y0 - 50), min(H, y1 + 95)


def ramp(v, a, b):
    """0 at a, 1 at b, smooth in between."""
    t = max(0.0, min(1.0, (v - a) / (b - a)))
    return t * t * (3 - 2 * t)


fx = [ramp(x, 4, x0 - PAD) * ramp(x, W - 5, x1 + PAD) for x in range(W)]
fy = [ramp(y, top, y0 - PAD) * ramp(y, bot, y1 + PAD) for y in range(H)]
mask = Image.new("L", (W, H))
mask.putdata([round(255 * a * b) for b in fy for a in fx])
im = Image.composite(im, Image.new("RGB", (W, H), "white"), mask)
# the last specks of the ground, then crop to the statue's height, at 1.5x so
# the marble stays smooth on a projector; PNG, since a JPEG's white decodes
# one level off and draws the box after all
im = im.point(lambda v: 255 if v >= 251 else v).crop((0, top, W, bot))
im = im.resize((im.width * 3 // 2, im.height * 3 // 2), Image.LANCZOS)
im.save(out, optimize=True)
print("wrote", out, im.size)
