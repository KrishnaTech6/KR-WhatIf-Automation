"""Render stills at chosen times and tile them 3-up into contact sheets."""
import sys, os
import skia
from shots import SHOTS, render_frame, W, H
from art import font, text, paint

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sheets")
os.makedirs(OUT, exist_ok=True)


def still(t, shots):
    s = skia.Surface(W, H)
    c = s.getCanvas()
    sh = render_frame(c, t, shots)
    return s.makeImageSnapshot(), sh[1].__name__


def sheet(name, times, labels=None):
    shots = SHOTS()
    cols, tw, th, pad = 3, 640, 360, 12
    rows = (len(times) + cols - 1) // cols
    S = skia.Surface(cols * tw + (cols + 1) * pad, rows * (th + 46) + pad)
    c = S.getCanvas(); c.clear(skia.Color(20, 16, 30))
    for i, t in enumerate(times):
        img, fn = still(t, shots)
        x = pad + (i % cols) * (tw + pad); y = pad + (i // cols) * (th + 46)
        c.drawImageRect(img, skia.Rect(x, y, x + tw, y + th), skia.SamplingOptions(skia.FilterMode.kLinear))
        lab = (labels[i] if labels else "") + f"  t={t:.1f}s  {fn}"
        text(c, lab, x + 6, y + th + 32, font("semibold", 22), paint("cream"), align="left")
    S.makeImageSnapshot().save(os.path.join(OUT, name + ".png"), skia.kPNG)
    print("wrote", name)


if __name__ == "__main__":
    shots = SHOTS()
    t = float(sys.argv[1])
    img, fn = still(t, shots)
    img.save(os.path.join(OUT, f"still_{t:.1f}.png"), skia.kPNG)
    print(fn)
