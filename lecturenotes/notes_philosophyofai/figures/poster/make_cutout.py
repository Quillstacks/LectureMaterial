#!/usr/bin/env python3
"""Cut a statue out of a photograph or render with a plain backdrop.

Three masks, picked by mode:
  light  subject brighter than `thresh` (marble on a black museum backdrop)
  dark   subject darker than `thresh` (a white Gemini render on its 243 gray
         ground, or bronze on a light wall)
  grad   backdrop estimated per row from the edge columns, subject darker
         than it by `thresh` (a backdrop that runs light to dark)

Then: hand-drawn patches, the row cap (mount, pin, plinth below the subject),
hole filling by flood fill from the corners (small enclosed holes such as eye
sockets are refilled, large ones such as a gap under an arm stay open), and
the largest connected component only, so stray patches of wall go.

Current source:
  statue.jpeg  seated marble reader holding a graphics
                                 card, generated with Google Gemini by Mark,
                                 768 x 1376, ground at luminance 243
  python3 make_cutout.py statue.jpeg statue_cut.png 1376 238 dark

Usage: python3 make_cutout.py <source> <out.png> <row_cap> [thresh] [light|dark|grad]
"""
import sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter

PAD = 40

# Source crops in source pixels, keyed by file name: for a print with a page
# border or a label, which the corner flood fill would take for the outside.
CROPS = {}

# Hand-drawn mask patches in (cropped) source pixels, keyed by file name, for
# parts the threshold loses: a lit crown as light as the backdrop, open to the
# outside so the hole fill cannot reach it.
PATCHES = {}


def backdrop(L):
    """Per-row backdrop from the outer 200 columns, interpolated across."""
    W, H = L.size
    px = L.load()
    est = Image.new("L", (2, H))
    ep = est.load()
    for y in range(H):
        ep[0, y] = int(sum(px[x, y] for x in range(0, 200, 4)) / 50)
        ep[1, y] = int(sum(px[x, y] for x in range(W - 200, W, 4)) / 50)
    return est.resize((W, H), Image.BILINEAR)


def main(src, out, row_cap, thresh=85, mode="light", hole_limit=0.06):
    im = Image.open(src).convert("RGB")
    name = src.split("/")[-1]
    if name in CROPS:
        im = im.crop(CROPS[name])
    W, H = im.size
    L = im.convert("L")
    if mode == "dark":
        mask = L.point(lambda v: 255 if v < thresh else 0)
    elif mode == "grad":
        diff = ImageChops.subtract(backdrop(L), L)
        mask = diff.point(lambda v: 255 if v > thresh else 0)
    else:
        mask = L.point(lambda v: 255 if v > thresh else 0)
    for poly in PATCHES.get(name, []):
        ImageDraw.Draw(mask).polygon(poly, fill=255)
    ImageDraw.Draw(mask).rectangle([0, row_cap, W, H], fill=0)
    outside = mask.copy()
    for xy in [(0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1)]:
        ImageDraw.floodfill(outside, xy, 128)
    # enclosed regions are holes (eye sockets, mouths) and get filled, except
    # large ones, which are backdrop seen through the figure (the gap between
    # the Thinker's arm, chin and knee) and stay open
    holes = outside.copy()
    hp = holes.load()
    limit = max(W, H) * hole_limit
    for y in range(0, H, 6):
        for x in range(0, W, 6):
            if hp[x, y] == 0:
                probe = holes.copy()
                ImageDraw.floodfill(probe, (x, y), 200)
                bb = ImageChops.difference(probe, holes).getbbox()
                big = bb and max(bb[2] - bb[0], bb[3] - bb[1]) > limit
                ImageDraw.floodfill(holes, (x, y), 128 if big else 255)
    mask = holes.point(lambda v: 0 if v == 128 else 255)
    # keep only the largest component: stray lighter patches of backdrop or
    # wall are separate blobs and go
    labels = mask.copy()
    lp = labels.load()
    best, best_area = None, 0
    for y in range(0, H, 6):
        for x in range(0, W, 6):
            if lp[x, y] == 255:
                probe = labels.copy()
                ImageDraw.floodfill(probe, (x, y), 200)
                bb = ImageChops.difference(probe, labels).getbbox()
                area = (bb[2] - bb[0]) * (bb[3] - bb[1])
                ImageDraw.floodfill(labels, (x, y), 128)
                if area > best_area:
                    best, best_area = (x, y), area
    keep = mask.copy()
    ImageDraw.floodfill(keep, best, 128)
    mask = keep.point(lambda v: 255 if v == 128 else 0)
    mask = mask.filter(ImageFilter.GaussianBlur(3)).point(lambda v: 255 if v > 140 else 0)
    mask = mask.filter(ImageFilter.GaussianBlur(1.2))
    cut = L.convert("RGB")
    cut.putalpha(mask)
    box = mask.getbbox()
    box = (max(0, box[0] - PAD), max(0, box[1] - PAD), min(W, box[2] + PAD), min(H, box[3] + PAD))
    cut = cut.crop(box)
    cut.save(out)
    print("wrote", out, cut.size)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]),
         int(sys.argv[4]) if len(sys.argv) > 4 else 85,
         sys.argv[5] if len(sys.argv) > 5 else "light")
