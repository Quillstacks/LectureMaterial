#!/usr/bin/env python3
"""Compose a print poster in the cover_compose.py house style.

Same page as the Sovereign covers (serif masthead, rule, tagline and issue
line, subject, accent dash, headline and dek, call to action on the bottom
margin) with three differences for paper:

  - A-series proportions (1 : sqrt 2) instead of 3 : 4, so the sheet fills an
    A4, A3 or A2 with no bands. The layout is designed in the cover's 1600-wide
    unit space and rendered at `px_width` pixels (default 3508, which is A3 at
    300 dpi, A2 at 212 dpi, A4 at 600 dpi). A PDF sized to A3 is written beside
    the PNG, so any printer scales it to the sheet.
  - A `theme`: "dark" is the cover palette, "light" is black on white for a
    printer that should not lay down a page of toner.
  - An optional `dissolve` block: the right part of the subject breaks up into
    flat square blocks along a noisy boundary, in interleaved sizes, thinning
    out and streaking off to the upper right. Antiquity turning into
    computation, and it survives a grayscale print because it is geometry, not
    colour.

Spec keys (beyond cover_compose: masthead, tagline, issue, headline, dek, cta,
subject_w, subject_fill, subject_max_scale):

  px_width      output width in pixels, default 3508
  theme         "dark" (default) or "light"
  accent        [r, g, b] override for the dash and accent blocks
  credit        one small line, right-aligned in the bottom margin: image
                source and licence
  subject_x     page fraction where the subject's horizontal centre sits, 0.5
  mirror        true flips the subject left to right, so the part that should
                survive faces the left margin and the rest dissolves rightward
  subject_level multiply the subject's tones, e.g. 0.88 to keep white marble
                off a white page
  white_point   for a picture without alpha: the gray level of its ground,
                lifted to paper white; the empty margins are trimmed and the
                picture is placed as is, with its own shadow and no drop shadow
  dissolve      {start, tilt, wobble, block_min, block_max, layers, reach,
                 lift, fly, seed, accent_frac}
                start       fraction of the subject width where blocks begin
                tilt        boundary shift from top to bottom, fraction of the
                            subject width; positive leans like a slash
                wobble      boundary wobble, as a fraction of the subject width
                fly         share of dropped blocks that fly instead of vanish
                spread      vertical jitter of flying blocks, in block edges
                block_min   smallest block edge, in 1600-wide units
                block_max   largest block edge, in 1600-wide units
                layers      number of block sizes between the two
                reach       how far blocks may fly, as a fraction of subject width
                lift        upward drift of flying blocks, as a fraction of reach
                seed        random seed, so a re-render is identical
                accent_frac fraction of flying blocks painted in the accent

Usage: python3 tools/poster_compose.py <spec.json>
       cutout path in the spec is relative to the spec; output is <spec>.png
"""
import os, sys, json, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cover_compose import SERIF_B, SANS_B, SANS, wrap  # noqa: E402
import cover_compose as cc  # noqa: E402

THEMES = {
    "dark":  dict(page=cc.PAGE, fg=cc.FG, dim=cc.DIM, faint=cc.FAINT, accent=cc.YELLOW, lift=(38, 40, 46), glow=True),
    "light": dict(page=(255, 255, 255), fg=(12, 12, 12), dim=(92, 92, 92), faint=(140, 140, 140), accent=(12, 12, 12), lift=None, glow=False),
}

W0, H0 = 1600, 2263        # design units, A proportions
M0 = 96


class Page:
    """Design-unit layout rendered at a pixel scale."""

    def __init__(self, px_width):
        self.S = px_width / W0
        self.W, self.H = round(W0 * self.S), round(H0 * self.S)
        self.M = self.u(M0)

    def u(self, v):
        return int(round(v * self.S))

    def font(self, path, size):
        return ImageFont.truetype(path, self.u(size))

    def tracked(self, d, xy, text, font, fill, track=0):
        x, y = xy
        for ch in text:
            d.text((x, y), ch, font=font, fill=fill)
            x += d.textlength(ch, font=font) + self.u(track)
        return x - xy[0]


def dissolve(cut, p, u, accent, seed=7):
    """Break the right part of a cutout into blocks that thin out and scatter.

    Works on the cutout at its final page size, so block edges are page pixels.
    The boundary is a wobbling curve, not a line; blocks of several sizes
    interleave along it; dropped blocks fly to the upper right, some leaving a
    trail of smaller blocks. Returns a wider, taller RGBA image with the
    subject's top-left corner at (0, pad_y); pad_y is returned too.
    """
    rnd = random.Random(seed)
    w, h = cut.size
    start = p.get("start", 0.55)
    wobble = p.get("wobble", 0.07) * w
    s_min, s_max = u(p.get("block_min", 5)), u(p.get("block_max", 40))
    layers = p.get("layers", 5)
    reach = int(p.get("reach", 0.5) * w)
    lift = p.get("lift", 0.35)
    accent_frac = p.get("accent_frac", 0.0)

    # boundary x as a function of y: a tilted line (tilt is the shift from top
    # to bottom as a fraction of the width, positive leans like a slash) plus
    # three sines with random phase when wobble is set
    tilt = p.get("tilt", 0.0) * w
    phases = [rnd.uniform(0, 2 * math.pi) for _ in range(3)]
    freqs = [1.3, 2.9, 5.1]

    def xb(y):
        n = sum(math.sin(2 * math.pi * f * y / h + ph) for f, ph in zip(freqs, phases)) / 3
        return start * w + tilt * (0.5 - y / h) + wobble * n

    pad_y = int(0.22 * h)
    out = Image.new("RGBA", (w + reach + s_max, h + 2 * pad_y), (0, 0, 0, 0))
    od = ImageDraw.Draw(out)

    # the photo survives left of the boundary
    keep = Image.new("L", (w, h), 0)
    kd = ImageDraw.Draw(keep)
    for y in range(h):
        kd.line([(0, y), (xb(y), y)], fill=255)
    photo = cut.copy()
    photo.putalpha(Image.composite(cut.getchannel("A"), Image.new("L", (w, h), 0), keep))
    out.paste(photo, (0, pad_y), photo)

    alpha = cut.getchannel("A")
    rgb = cut.convert("RGB")
    sizes = [int(round(s_min * (s_max / s_min) ** (k / max(1, layers - 1)))) for k in range(layers)]
    for k, s in enumerate(sizes):
        lo, hi = k / layers, (k + 1) / layers        # this size owns this stretch of t
        for by in range(0, h, s):
            for bx in range(int(start * w - wobble - abs(tilt) / 2 - s), w, s):
                box = (max(0, bx), by, min(bx + s, w), min(by + s, h))
                if box[2] <= box[0]:
                    continue
                cx_, cy_ = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
                x0 = xb(cy_)
                t = (cx_ - x0) / max(1, w - x0)
                tj = t + rnd.uniform(-0.14, 0.14)
                if t < -0.02 or not (lo <= tj < hi):
                    continue
                a = alpha.crop(box).resize((1, 1), Image.BOX).getpixel((0, 0))
                if a < 90:
                    continue
                col = rgb.crop(box).resize((1, 1), Image.BOX).getpixel((0, 0))
                t0 = max(0.0, t)
                if rnd.random() < 0.04 + 0.9 * t0 ** 1.3:
                    # dropped: half of them fly off, trailing smaller blocks
                    if rnd.random() < p.get("fly", 0.6):
                        dist = reach * rnd.uniform(0.1, 1.0) * (0.3 + 0.7 * t0)
                        dx = int(dist)
                        spread = p.get("spread", 1.5)
                        dy = int(-dist * lift * rnd.uniform(0.2, 1.0) + rnd.uniform(-spread, spread) * s)
                        fade = int(255 * rnd.uniform(0.3, 0.9))
                        c = accent if rnd.random() < accent_frac else col
                        od.rectangle([bx + dx, by + dy + pad_y, bx + dx + s - 1, by + dy + s - 1 + pad_y],
                                     fill=(c[0], c[1], c[2], fade))
                        if rnd.random() < 0.45:
                            n = rnd.randint(2, 4)
                            for i in range(1, n + 1):
                                f = i / (n + 1)
                                ts = max(2, int(s * (1 - 0.6 * f)))
                                od.rectangle([bx + int(dx * f), by + int(dy * f) + pad_y,
                                              bx + int(dx * f) + ts - 1, by + int(dy * f) + ts - 1 + pad_y],
                                             fill=(col[0], col[1], col[2], int(fade * (1 - 0.5 * f))))
                    continue
                od.rectangle([box[0], box[1] + pad_y, box[2] - 1, box[3] - 1 + pad_y],
                             fill=(col[0], col[1], col[2], 255))
    return out, pad_y


def build(spec_path):
    spec = json.load(open(spec_path))
    base = os.path.dirname(os.path.abspath(spec_path))
    out_png = os.path.splitext(spec_path)[0] + ".png"
    out_pdf = os.path.splitext(spec_path)[0] + ".pdf"

    th = dict(THEMES[spec.get("theme", "dark")])
    if spec.get("accent"):
        th["accent"] = tuple(spec["accent"])
    PAGE, FG, DIM, ACCENT = th["page"], th["fg"], th["dim"], th["accent"]

    pg = Page(spec.get("px_width", 3508))
    W, H, M, u = pg.W, pg.H, pg.M, pg.u
    canvas = Image.new("RGB", (W, H), PAGE)
    if th["glow"]:
        glow = Image.new("L", (W, H), 0)
        ImageDraw.Draw(glow).ellipse([-W * 0.15, H * 0.18, W * 1.15, H * 0.92], fill=70)
        glow = glow.filter(ImageFilter.GaussianBlur(u(220)))
        canvas = Image.composite(Image.new("RGB", (W, H), th["lift"]), canvas, glow)
    d = ImageDraw.Draw(canvas)

    # ---- masthead and rule ---------------------------------------------
    mast, size = spec["masthead"], 250
    f = pg.font(SERIF_B, size)
    while d.textlength(mast, font=f) > W - 2 * M and size > 60:
        size -= 4
        f = pg.font(SERIF_B, size)
    d.text((M, u(96)), mast, font=f, fill=FG)
    ry = u(96 + size * 1.02 + 26)
    d.rectangle([M, ry, W - M, ry + u(3)], fill=FG)
    pg.tracked(d, (M, ry + u(20)), spec["tagline"].upper(), pg.font(SANS_B, 25), DIM, track=4.5)
    fi = pg.font(SANS, 25)
    d.text((W - M - d.textlength(spec["issue"], font=fi), ry + u(20)), spec["issue"], font=fi, fill=DIM)
    header_bottom = ry + u(62)

    # ---- call to action, bottom margin, drawn last ---------------------
    cta = spec.get("cta", [])
    cta_top = H - M - u(len(cta) * 42) + u(8) if cta else H - M

    # ---- headline block, anchored upward from the call to action --------
    fh, fd = pg.font(SANS_B, 96), pg.font(SANS, 38)
    head_lines = wrap(d, spec["headline"].upper(), fh, W - 2 * M)
    dek_lines = wrap(d, spec["dek"], fd, int((W - 2 * M) * 0.9)) if spec.get("dek") else []
    block_h = u(len(head_lines) * 104 + (32 + len(dek_lines) * 50 if dek_lines else 0))
    block_top = cta_top - u(74) - block_h
    y = block_top
    d.rectangle([M, y - u(34), M + u(92), y - u(24)], fill=ACCENT)
    for line in head_lines:
        d.text((M, y), line, font=fh, fill=FG)
        y += u(104)
    y += u(32)
    for line in dek_lines:
        d.text((M, y), line, font=fd, fill=DIM)
        y += u(50)

    # ---- subject ---------------------------------------------------------
    src = Image.open(os.path.join(base, spec["cutout"]))
    has_alpha = src.mode in ("RGBA", "LA") or "transparency" in src.info
    if has_alpha:
        cut = src.convert("RGBA")
        cut = cut.crop(cut.getchannel("A").getbbox())
    else:
        # a plain picture on a light ground: no cutout, just lift the ground to
        # paper white (white_point is the ground's gray level) and trim the
        # empty margins; the picture keeps its own shadow and edges
        rgb = src.convert("RGB")
        wp = spec.get("white_point")
        if wp:
            rgb = rgb.point(lambda v: min(255, round(v * 255 / wp)))
        content = rgb.convert("L").point(lambda v: 255 if v < 236 else 0).getbbox()
        pad = int(0.03 * max(rgb.size))
        rgb = rgb.crop((max(0, content[0] - pad), max(0, content[1] - pad),
                        min(rgb.width, content[2] + pad), min(rgb.height, content[3] + pad)))
        cut = rgb.convert("RGBA")
    if spec.get("mirror"):
        cut = cut.transpose(Image.FLIP_LEFT_RIGHT)
    if spec.get("subject_level") and has_alpha:
        # a plain picture keeps its tones: levelling would gray its ground
        lv = spec["subject_level"]
        a = cut.getchannel("A")
        cut = cut.convert("RGB").point(lambda v: int(v * lv)).convert("RGBA")
        cut.putalpha(a)
    band_top, band_bot = header_bottom, block_top - u(96)
    box_w = int(W * spec.get("subject_w", 0.88))
    box_h = int((band_bot - band_top) * spec.get("subject_fill", 0.94))
    k = min(box_w / cut.width, box_h / cut.height, spec.get("subject_max_scale", 1.3))
    cut = cut.resize((int(cut.width * k), int(cut.height * k)), Image.LANCZOS)
    subj_w, subj_h = cut.size
    pad_y = 0
    if spec.get("dissolve"):
        cut, pad_y = dissolve(cut, spec["dissolve"], u, ACCENT, spec["dissolve"].get("seed", 7))
    cx = int(W * spec.get("subject_x", 0.5) - subj_w / 2)
    cy = int(band_top + (band_bot - band_top - subj_h) / 2) - pad_y
    bb = cut.getchannel("A").getbbox()
    if cx + bb[2] > W - M:
        print(f"  note: scatter runs {cx + bb[2] - (W - M)}px into the right margin")
    if cy + bb[1] < header_bottom:
        print(f"  note: scatter rides {header_bottom - (cy + bb[1])}px into the header")

    canvas = canvas.convert("RGBA")
    if has_alpha:
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sh = Image.new("RGBA", cut.size, (0, 0, 0, 0))
        sh.putalpha(cut.getchannel("A").point(lambda a: int(a * (0.75 if th["glow"] else 0.35))))
        shadow.paste(sh, (cx + u(10), cy + u(26)), sh)
        shadow = shadow.filter(ImageFilter.GaussianBlur(u(30)))
        canvas = Image.alpha_composite(canvas, shadow)
    canvas.paste(cut, (cx, cy), cut)
    d = ImageDraw.Draw(canvas)

    fc = pg.font(SANS_B, 24)
    y = cta_top
    for line in cta:
        d.rectangle([M, y + u(6), M + u(11), y + u(17)], fill=ACCENT)
        pg.tracked(d, (M + u(32), y), line.upper(), fc, DIM, track=2.2)
        y += u(42)

    # image credit and licence, small, right-aligned in the bottom margin
    if spec.get("credit"):
        fcr = pg.font(SANS, 15)
        cw = d.textlength(spec["credit"], font=fcr)
        d.text((W - M - cw, H - M + u(44)), spec["credit"], font=fcr, fill=th["faint"])

    rgb = canvas.convert("RGB")
    rgb.save(out_png)
    # 3508 px across 297 mm is 300 dpi: the PDF page is an A3 sheet
    dpi = W / (297 / 25.4)
    rgb.save(out_pdf, resolution=dpi)
    print("wrote", out_png, rgb.size, "and", out_pdf, f"at {dpi:.0f} dpi")


if __name__ == "__main__":
    build(sys.argv[1])
