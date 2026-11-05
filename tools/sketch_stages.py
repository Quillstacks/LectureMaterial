#!/usr/bin/env python3
"""Band-crop, mask and recolour iPad sketches into build-up stage images.

    sketch_stages.py <spec.json> <raw_dir> <out_dir>

Recolouring as in tools/notes_drawing.py: white -> transparent, dark ink ->
tdfg #F2F2F2, red -> DHBWred #E2001A, plus blue -> tddim #9A9A9A (an aside
voice) and yellow -> #FFCE00, kept as drawn (further reading). Every stage lands centred on ONE shared 16:9 canvas sized so the
tallest ink spans (1 - 2*margin) of the page height: one handwriting scale
across all slides, full height for the tallest sketch, centred otherwise.

spec.json:
{
  "margin": 0.03,            // ink clearance from the page edges
  "thicken": 5,              // MinFilter px; odd, 1 = off
  "red_gain": 1,             // alpha gain on red ink; a pen like (254,58,48)
                             // caps at 81% alpha and reads maroon, 1.25 fixes it
  "canvas_height": null,     // pin the canvas (px) to match an earlier run
  "normalize_width": null,   // upscale raws to this width first; Notes caps tall
                             // drawings near 3076 px, shrinking their handwriting
  "stages": {
    "IEf1": {"src": "IEf", "band": [0, 1],
             "masks": [[0.40, 0.68, 1, 1], [0.735, 0.24, 0.93, 0.70]]},
    "IEf2": {"src": "IEf", "band": [0, 1], "masks": []}
  }
}
band = [y0, y1] and masks = [x0, y0, x1, y1] as fractions of the FULL raw
image; masks are erased (white) before the band crop. Each stage crops to its
OWN ink bbox, so every slide's visible content is centred on the page.
"""
import json
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter

FG = (0xF2, 0xF2, 0xF2)
RED = (0xE2, 0x00, 0x1A)
DIM = (0x9A, 0x9A, 0x9A)
YEL = (0xFF, 0xCE, 0x00)


def prepared(raw_dir, src, band, masks, thicken, width=None):
    im = Image.open(os.path.join(raw_dir, src + ".png")).convert("RGB")
    if width and im.width != width:
        im = im.resize((width, round(im.height * width / im.width)), Image.BICUBIC)
    w, h = im.size
    d = ImageDraw.Draw(im)
    for x0, y0, x1, y1 in masks:
        d.rectangle([x0 * w, y0 * h, x1 * w, y1 * h], fill=(255, 255, 255))
    im = im.crop((0, int(band[0] * h), w, int(band[1] * h)))
    if thicken > 1:
        im = im.filter(ImageFilter.MinFilter(thicken))  # ink is dark: min widens
    return im


def split(im):
    r, g, b = im.split()
    ink = ImageChops.darker(ImageChops.darker(r, g), b).point(lambda v: 255 - v)
    ink = ink.point(lambda v: 0 if v < 12 else v)
    red = ImageChops.subtract(r, ImageChops.lighter(g, b)).point(
        lambda v: 255 if v > 40 else 0)
    blue = ImageChops.subtract(b, ImageChops.lighter(r, g)).point(
        lambda v: 255 if v > 40 else 0)
    # Pure yellow also clears the red test, so it composites last, over red.
    yellow = ImageChops.subtract(ImageChops.darker(r, g), b).point(
        lambda v: 255 if v > 40 else 0)
    return ink, red, blue, yellow


def main():
    spec_path, raw_dir, out_dir = sys.argv[1:4]
    spec = json.load(open(spec_path))
    margin = spec.get("margin", 0.03)
    thicken = spec.get("thicken", 5)
    red_gain = spec.get("red_gain", 1)
    width = spec.get("normalize_width")
    stages = spec["stages"]

    prep, boxes = {}, {}
    for name, st in stages.items():
        im = prepared(raw_dir, st["src"], st["band"], st.get("masks", []), thicken, width)
        ink, red, blue, yellow = split(im)
        if red_gain != 1:
            boosted = ink.point(lambda v: min(255, int(v * red_gain)))
            ink = Image.composite(boosted, ink, red)
        bbox = ink.getbbox()
        if bbox is None:
            sys.exit(f"{name}: no ink in band {st['band']}")
        prep[name] = (im, ink, red, blue, yellow)
        boxes[name] = bbox

    href = max(b[3] - b[1] for b in boxes.values())
    pinned = spec.get("canvas_height")
    H = pinned or int(href / (1 - 2 * margin))
    W = int(H * 16 / 9)
    print(f"shared canvas {W}x{H}, tallest ink {href}")
    wide = max(b[2] - b[0] for b in boxes.values())
    assert wide <= W * (1 - 2 * margin), "a stage is too wide for the canvas"
    if pinned:
        assert href <= pinned * (1 - 2 * margin), \
            "pinned canvas smaller than the ink"

    for name, (im, ink, red, blue, yellow) in prep.items():
        out = Image.composite(Image.new("RGB", im.size, RED),
                              Image.new("RGB", im.size, FG), red)
        out = Image.composite(Image.new("RGB", im.size, DIM), out, blue)
        out = Image.composite(Image.new("RGB", im.size, YEL), out, yellow)
        out.putalpha(ink)
        out = out.crop(boxes[name])
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        canvas.paste(out, ((W - out.width) // 2, (H - out.height) // 2), out)
        canvas.save(os.path.join(out_dir, name + ".png"), optimize=True)
        print(f"{name}  ink {out.width}x{out.height}")


if __name__ == "__main__":
    main()
