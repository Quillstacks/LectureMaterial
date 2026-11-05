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

With "vector": true each stage is a PDF instead of a PNG, sharp at any
projector resolution: every ink colour is traced by potrace (brew install
potrace) from a "trace_scale"-fold upscale, then filled and stroked with round
joins, the stroke (thicken - 1 canvas px wide) doing the thickening. The traces
come from Notes' PNG, not the original pencil strokes, which Notes keeps out of
reach. \\includegraphics without an extension prefers the PDF over a PNG. A
side strip keeps its own page: "canvas": [W, H] replaces the shared canvas and
a stage's "at": [x, y] places the ink's top left corner instead of centring.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import zlib

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


def layers(im, red_gain):
    """Coverage per ink, painted in this order: later inks win an overlap."""
    r, g, b = im.split()
    top = ImageChops.lighter(ImageChops.lighter(r, g), b)
    chroma = ImageChops.subtract(top, ImageChops.darker(ImageChops.darker(r, g), b))
    # Mixing with the white page scales these differences evenly, so the tests
    # hold along a stroke's soft edge too.
    blue = ImageChops.subtract(b, ImageChops.lighter(r, g)).point(
        lambda v: 255 if v > 4 else 0)
    yellow = ImageChops.subtract(
        ImageChops.subtract(g, b).point(lambda v: min(255, int(v * 1.25))),
        chroma.point(lambda v: v // 2)).point(lambda v: 255 if v > 0 else 0)
    none = Image.new("L", im.size, 0)
    red = Image.composite(none, chroma, ImageChops.lighter(blue, yellow))
    return [(YEL, Image.composite(chroma, none, yellow)),
            (DIM, Image.composite(chroma, none, blue)),
            (RED, red.point(lambda v: min(255, int(v * red_gain)))),
            (FG, top.point(lambda v: 255 - v))]


def trace(cover, scale, tmp):
    """potrace one coverage layer; PDF path operators, 0.1 upscaled px units."""
    big = cover.resize((cover.width * scale, cover.height * scale), Image.BICUBIC)
    big = big.point(lambda v: 0 if v > 127 else 255).convert("1", dither=Image.Dither.NONE)
    pbm, pdf = os.path.join(tmp, "l.pbm"), os.path.join(tmp, "l.pdf")
    big.save(pbm)
    subprocess.run(["potrace", "-b", "pdf", "-c", "-M", "0", "-r", "72",
                    "-t", str(2 * scale), "-o", pdf, pbm], check=True)
    data = open(pdf, "rb").read()
    body = re.search(rb"stream\r?\n(.*?)endstream", data, re.S).group(1).decode("ascii")
    body = body.split("\n", 1)[1].replace("0 g\n", "", 1)  # our own cm and colours
    return re.sub(r"(?m)^f$", "B", body)


def write_pdf(path, W, H, content):
    stream = zlib.compress(content.encode("ascii"), 9)
    parts = [b"<</Type/Catalog/Pages 2 0 R>>",
             b"<</Type/Pages/Kids[3 0 R]/Count 1>>",
             f"<</Type/Page/Parent 2 0 R/MediaBox[0 0 {W} {H}]/Resources<<>>"
             f"/Contents 4 0 R>>".encode(),
             f"<</Length {len(stream)}/Filter/FlateDecode>>\nstream\n".encode()
             + stream + b"\nendstream"]
    out, offsets = bytearray(b"%PDF-1.5\n"), []
    for i, part in enumerate(parts, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + part + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(parts) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (f"trailer\n<</Size {len(parts) + 1}/Root 1 0 R>>\n"
            f"startxref\n{xref}\n%%EOF\n").encode()
    open(path, "wb").write(out)


def main_vector(spec, raw_dir, out_dir):
    margin = spec.get("margin", 0.03)
    stroke = spec.get("thicken", 5) - 1
    scale = spec.get("trace_scale", 3)
    red_gain = spec.get("red_gain", 1)
    width = spec.get("normalize_width")
    prep = {}
    for name, st in spec["stages"].items():
        im = prepared(raw_dir, st["src"], st["band"], st.get("masks", []), 1, width)
        total = None
        for _, cover in layers(im, red_gain):
            total = cover if total is None else ImageChops.lighter(total, cover)
        bbox = total.point(lambda v: 255 if v > 127 else 0).getbbox()
        if bbox is None:
            sys.exit(f"{name}: no ink in band {st['band']}")
        prep[name] = im.crop(bbox)
    href = max(im.height for im in prep.values())
    H = spec.get("canvas_height") or int(href / (1 - 2 * margin))
    W = int(H * 16 / 9)
    canvas = spec.get("canvas")
    if canvas:
        W, H = canvas
    else:
        assert href <= H * (1 - 2 * margin), "pinned canvas smaller than the ink"
    print(f"shared canvas {W}x{H}, tallest ink {href}")
    unit = 1 / (10 * scale)
    with tempfile.TemporaryDirectory() as tmp:
        for name, im in prep.items():
            assert im.width <= W * (1 - 2 * margin), f"{name} is too wide for the canvas"
            x, y = (W - im.width) // 2, (H - im.height) // 2
            at = spec["stages"][name].get("at")
            if at:
                x, y = at[0], H - at[1] - im.height
            content = [f"q {unit:.6f} 0 0 {unit:.6f} {x} {y} cm\n"
                       f"{stroke * 10 * scale} w 1 J 1 j\n"]
            for colour, cover in layers(im, red_gain):
                if cover.point(lambda v: 255 if v > 127 else 0).getbbox() is None:
                    continue
                rgb = " ".join(f"{c / 255:.4f}" for c in colour)
                content.append(f"{rgb} rg {rgb} RG\n{trace(cover, scale, tmp)}")
            content.append("Q\n")
            path = os.path.join(out_dir, name + ".pdf")
            write_pdf(path, W, H, "".join(content))
            print(f"{name}  ink {im.width}x{im.height}  {os.path.getsize(path) // 1024} KB")


def main():
    spec_path, raw_dir, out_dir = sys.argv[1:4]
    spec = json.load(open(spec_path))
    if spec.get("vector"):
        return main_vector(spec, raw_dir, out_dir)
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
