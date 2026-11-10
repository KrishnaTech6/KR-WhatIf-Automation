"""Render the brand reference images, or check the current code against them.

  python3 brand/render_reference.py           write brand/reference/*.png (only when the brand is meant to change)
  python3 brand/render_reference.py --check   re-render and compare; exit 1 if anything drifted (> 2% mean difference)
"""
import os
import sys

import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from primitives import font, finish, night_sky, paint, save_png, surface, text  # noqa: E402
from kr import EXPRESSIONS, draw_kr  # noqa: E402
from logo import chapter_card, draw_logo, end_card  # noqa: E402

W, H, T = 1920, 1080, 1.0      # t = 1.0: eyes open, mid-breath


def kr_sheet(c):
    night_sky(c, W, H, T)
    text(c, "KR · expression set", 60, 70, font("semibold", 34), paint("sand"), align="left")
    cols = [(240 + 480 * i, 480) for i in range(4)] + [(480 + 480 * i, 960) for i in range(3)]
    for (x, y), e in zip(cols, EXPRESSIONS):
        draw_kr(c, x, y - 70, 0.95, e, T)
        text(c, e, x, y + 28, font("semibold", 30), paint("cream", 0.85))
    finish(c, W, H, T)


def logo_still(c):
    night_sky(c, W, H, T)
    draw_logo(c, W / 2, H / 2, 1.3, 1.0, T)
    finish(c, W, H, T)


def sting_strip(c):
    night_sky(c, W, H, T)
    for i, p in enumerate([0.15, 0.35, 0.55, 1.0]):
        draw_logo(c, 240 + 480 * i, H / 2, 0.9, p, T)
        text(c, f"p = {p}", 240 + 480 * i, H - 120, font("regular", 28), paint("cream", 0.7))
    finish(c, W, H, T)


IMAGES = {
    "kr_sheet": kr_sheet,
    "logo": logo_still,
    "logo_sting": sting_strip,
    "chapter_card": lambda c: chapter_card(c, W, H, "+2 HOURS", "The city goes dark", 1.0, T),
    "end_card": lambda c: end_card(c, W, H, 1.0, T),
}


def render(name):
    s = surface(W, H)
    IMAGES[name](s.getCanvas())
    return s


def main():
    out = os.path.join(HERE, "reference")
    os.makedirs(out, exist_ok=True)
    if "--check" not in sys.argv:
        for n in IMAGES:
            save_png(render(n), os.path.join(out, f"{n}.png"))
            print("wrote", f"reference/{n}.png")
        return
    bad = []
    for n in IMAGES:
        ref = skia.Image.open(os.path.join(out, f"{n}.png")).toarray()[..., :3].astype(np.float32)
        now = render(n).makeImageSnapshot().toarray()[..., :3].astype(np.float32)
        diff = float(np.abs(ref - now).mean() / 255 * 100)
        print(f"{n:<14} {diff:.2f}% different")
        if diff > 2.0:
            bad.append(n)
    if bad:
        sys.exit("BRAND DRIFT: " + ", ".join(bad) + " — fix the code, never the reference")
    print("BRAND OK")


if __name__ == "__main__":
    main()
