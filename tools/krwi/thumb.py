"""Thumbnail helpers. Draw at 2560x1440 on canvas(), then save() -> 1280x720 JPG under 2 MB, and compare() for the
check sheet (full size + ~320 px wide on light and dark backgrounds). Rules: brand/thumbnail_rules.md."""
import os

import skia

from . import ctx

TW, TH = 2560, 1440
OUT = os.path.join(ctx.VIDEO, "thumbs")


def canvas():
    """-> (surface, canvas) at 2560x1440, already scaled so you can draw in 1920x1080 coordinates (W, H)."""
    s = skia.Surface(TW, TH)
    c = s.getCanvas()
    c.scale(TW / ctx.W, TH / ctx.H)
    return s, c


def save(surface, name="THUMB.jpg"):
    os.makedirs(OUT, exist_ok=True)
    small = skia.Surface(1280, 720)
    small.getCanvas().drawImageRect(surface.makeImageSnapshot(), skia.Rect(0, 0, 1280, 720),
                                    skia.SamplingOptions(skia.CubicResampler.Mitchell()))
    img = small.makeImageSnapshot()
    path = os.path.join(OUT, name)
    for q in (92, 88, 84, 80, 75):
        img.save(path, skia.kJPEG, q)
        if os.path.getsize(path) < 2_000_000:
            break
    print("wrote", path, os.path.getsize(path) // 1024, "KB")
    return path


def compare(paths, name="compare.jpg"):
    """Full size row + a row at 320 px wide on YouTube's light and dark backgrounds."""
    imgs = [skia.Image.open(p) for p in paths]
    n = len(imgs)
    pad, small = 24, 320
    full_w = 1280 if n == 1 else 640
    full_h = full_w * 9 // 16
    w = max(pad + n * (full_w + pad), pad + n * (small + pad * 2))
    sh = small * 9 // 16
    H = pad + full_h + pad + 2 * (sh + pad * 2)
    S = skia.Surface(w, H)
    c = S.getCanvas(); c.clear(skia.Color(40, 40, 40))
    samp = skia.SamplingOptions(skia.CubicResampler.Mitchell())
    for i, im in enumerate(imgs):
        x = pad + i * (full_w + pad)
        c.drawImageRect(im, skia.Rect(x, pad, x + full_w, pad + full_h), samp)
    for row, bgc in enumerate((skia.Color(255, 255, 255), skia.Color(15, 15, 15))):
        y = pad + full_h + pad + row * (sh + pad * 2)
        c.drawRect(skia.Rect(0, y - pad / 2, w, y + sh + pad / 2), skia.Paint(Color=bgc))
        for i, im in enumerate(imgs):
            x = pad + i * (small + pad * 2)
            c.drawImageRect(im, skia.Rect(x, y, x + small, y + sh), samp)
    path = os.path.join(OUT, name)
    S.makeImageSnapshot().save(path, skia.kJPEG, 88)
    print("wrote", path)
    return path
