"""3 thumbnails, drawn at 2560x1440 (canvas scaled from 1920x1080 coords), saved 1280x720 JPG < 2 MB."""
import os, math, skia
from art import *  # noqa
from art import W, H
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumbs")
os.makedirs(OUT, exist_ok=True)
T0 = 1.3


def outline_text(c, s, x, y, size, color="gold", kind="extrabold", stroke=16, rot=0):
    f = font(kind, size)
    c.save(); c.translate(x, y); c.rotate(rot)
    sh = paint("space", 0.7); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14))
    text(c, s, 6, 10, f, sh)
    text(c, s, 0, 0, f, paint("space", 1, stroke=stroke))
    text(c, s, 0, 0, f, paint(color))
    c.restore()


def thumb_a(c):
    """Hero: a 70 cm dragonfly filling the frame, KR shocked for scale."""
    swamp_scene(c, T0, cam_x=0)
    c.drawRect(skia.Rect(0, 0, W, H), paint("space", 0.3))
    glow(c, 1180, 560, 700, "gold", 0.35)
    dragonfly(c, 1180, 470, 1.65, 0.37, ang=-8)
    glow(c, 330, 760, 360, "teal", 0.45)
    draw_kr(c, 330, 1080, 1.5, "shocked", T0, look=(1, -0.6))
    outline_text(c, "70 cm", 430, 210, 170, "gold")
    outline_text(c, "WINGS?!", 430, 390, 150, "cream")
    vignette(c, W, H, 0.6)


def thumb_b(c):
    """Hero: a wet forest on fire, oxygen gauge in the red."""
    swamp_scene(c, T0, night=0.9, burn=1.0)
    c.drawRect(skia.Rect(0, 0, W, H), paint("#0A0716", 0.35))
    for i, x in enumerate((420, 900, 1380)):
        lycopsid(c, x, 1000, 760, 80, T0, i, burn=1.0)
        for k in range(5):
            flame(c, x - 40 + k * 20, 1000 - 150 - k * 120, 1.6 - k * 0.15, T0 + k, k + i * 5)
    fire_wall(c, 2100, 1080, T0, 0.9, 0.9)
    gauge(c, 1600, 300, 210, 30, T0, True, alert=True)
    outline_text(c, "AIR THAT", 560, 220, 140, "cream")
    outline_text(c, "BURNS", 560, 400, 170, "coral")
    vignette(c, W, H, 0.55)


def bulb_forest(c, cx, cy, r):
    glow(c, cx, cy, r * 2.2, "gold", 0.55)
    glass = skia.Path(); glass.addCircle(cx, cy, r)
    neck = skia.Path(); neck.addRRect(skia.RRect.MakeRectXY(skia.Rect(cx - r * 0.42, cy + r * 0.7, cx + r * 0.42, cy + r * 1.25), 20, 20))
    glass = skia.Op(glass, neck, skia.PathOp.kUnion_PathOp)
    c.save(); c.clipPath(glass, doAntiAlias=True)
    lin(c, 0, cy - r, 0, cy + r, ["#FFE9A8", "#9FD0A0", "#2C4A48"], rect=skia.Rect(cx - r, cy - r, cx + r, cy + r * 1.3))
    c.save(); c.translate(cx, cy + r * 0.95); c.scale(r / 900, r / 900)
    for i in range(5):
        lycopsid(c, -760 + i * 380, 0, 900 + 120 * (i % 2), 80, T0, i)
    for i in range(4):
        tree_fern(c, -600 + i * 400, 0, 300, T0, i, 1.2)
    c.restore()
    dragonfly(c, cx + r * 0.25, cy - r * 0.35, r / 900, 0.4, ang=-20)
    c.restore()
    c.drawPath(glass, paint("cream", 0.9, stroke=8))
    c.drawCircle(cx - r * 0.45, cy - r * 0.45, r * 0.12, paint("cream", 0.6))
    for k in range(4):
        y = cy + r * 1.28 + k * 34
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(cx - r * 0.44, y, cx + r * 0.44, y + 28), 10, 10), paint("#9A8E78"))


def thumb_c(c):
    """Hero: a glowing light bulb with a prehistoric forest inside it."""
    lin(c, 0, 0, 0, H, ["#140C22", "#2A1A3A"])
    bulb_forest(c, 1260, 420, 330)
    draw_kr(c, 360, 1080, 1.5, "shocked", T0, look=(1, -0.5))
    outline_text(c, "300 MILLION", 470, 230, 115, "cream")
    outline_text(c, "YEARS OLD?", 470, 380, 125, "gold")
    vignette(c, W, H, 0.55)


def render(fn, name):
    S = skia.Surface(2560, 1440)
    c = S.getCanvas(); c.scale(2560 / 1920, 2560 / 1920)
    fn(c)
    grain(c, W, H, T0, 0.03)
    img = S.makeImageSnapshot()
    small = skia.Surface(1280, 720)
    small.getCanvas().drawImageRect(img, skia.Rect(0, 0, 1280, 720), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
    p = os.path.join(OUT, name)
    small.makeImageSnapshot().save(p, skia.kJPEG, 90)
    return p


def sheet(paths):
    ims = [skia.Image.open(p) for p in paths]
    S = skia.Surface(1280 * 3 + 40, 720 + 220 * 2 + 60)
    c = S.getCanvas(); c.clear(skia.Color(30, 28, 40))
    for i, im in enumerate(ims):
        c.drawImage(im, i * 1300, 0)
        for j, bg in enumerate([(255, 255, 255), (15, 15, 15)]):
            y = 740 + j * 230
            c.drawRect(skia.Rect(i * 1300, y, i * 1300 + 400, y + 220), skia.Paint(Color=skia.Color(*bg)))
            c.drawImageRect(im, skia.Rect(i * 1300 + 20, y + 20, i * 1300 + 340, y + 200), skia.SamplingOptions(skia.FilterMode.kLinear))
    S.makeImageSnapshot().save(os.path.join(OUT, "compare.jpg"), skia.kJPEG, 88)


if __name__ == "__main__":
    ps = [render(thumb_a, "THUMB_A.jpg"), render(thumb_c, "THUMB_B.jpg"), render(thumb_b, "THUMB_C.jpg")]
    sheet(ps)
    for p in ps: print(p, os.path.getsize(p))
