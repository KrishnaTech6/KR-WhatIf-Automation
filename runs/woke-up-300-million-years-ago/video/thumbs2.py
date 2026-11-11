"""Thumbnails v2 (Krishna's rules: no KR; text = the video title). Drawn at 2560x1440, saved 1280x720."""
import os, math, skia
from art import *  # noqa
from art import W, H
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumbs")
os.makedirs(OUT, exist_ok=True)
T0 = 1.3
TITLE = ("WHAT IF YOU WOKE UP", "300 MILLION", "YEARS AGO?")


def ot(c, s, x, y, size, color, align="left", stroke=18):
    f = font("extrabold", size)
    sh = paint("space", 0.75); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 16))
    text(c, s, x + 6, y + 12, f, sh, align)
    text(c, s, x, y, f, paint("space", 1, stroke=stroke), align)
    text(c, s, x, y, f, paint(color), align)


def title_block(c, x=60, y=160, k=0.9):
    ot(c, TITLE[0], x, y, 92 * k, "cream")
    ot(c, TITLE[1], x, y + 175 * k, 175 * k, "gold", stroke=22)
    ot(c, TITLE[2], x, y + 320 * k, 128 * k, "cream")


def blurred(c, draw, sigma=9):
    S = skia.Surface(W, H); draw(S.getCanvas())
    p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(sigma, sigma))
    c.drawImage(S.makeImageSnapshot(), 0, 0, skia.SamplingOptions(), p)


def person(c, x, base, h, pose="stand", rim="gold", a=1.0):
    """faceless silhouette with rim light. h = height in px."""
    s = h / 170.0
    c.save(); c.translate(x, base); c.scale(s, s)
    body = skia.Path()
    if pose == "stand":
        body.addCircle(0, -155, 14)
        b = skia.Path(); b.moveTo(-18, -138); b.lineTo(18, -138); b.lineTo(22, -70); b.lineTo(14, 0); b.lineTo(4, 0)
        b.lineTo(0, -60); b.lineTo(-4, 0); b.lineTo(-14, 0); b.lineTo(-22, -70); b.close()
        body = skia.Op(body, b, skia.PathOp.kUnion_PathOp)
        arm = skia.Path(); arm.moveTo(16, -132); arm.lineTo(44, -170); arm.lineTo(50, -166); arm.lineTo(24, -120); arm.close()
        body = skia.Op(body, arm, skia.PathOp.kUnion_PathOp)
    c.drawPath(body, paint("#07050E", a))
    rp = paint(rim, 0.45 * a, stroke=2.5); c.drawPath(body, rp)
    c.restore()


def thumb_dragonfly(c):
    """A 70 cm griffinfly hovering right above you, swamp blurred behind."""
    blurred(c, lambda cc: swamp_scene(cc, T0, cam_x=60), 10)
    c.drawRect(skia.Rect(0, 0, W, H), paint("space", 0.35))
    god_rays(c, T0, 2.0)
    glow(c, 1470, 430, 600, "gold", 0.45)
    glow(c, 1470, 430, 280, "cream", 0.25)
    dragonfly(c, 1470, 330, 1.68, 0.37, ang=-6)
    person(c, 1180, 1030, 330, "stand", "gold")          # a person, for scale (faceless)
    title_block(c)
    vignette(c, W, H, 0.6)


def thumb_bulb(c):
    """Today's light bulb glowing with the 300-million-year-old forest inside."""
    lin(c, 0, 0, 0, H, ["#0C0818", "#1E1230"])
    for i in range(14):
        a = math.radians(-90 + (i - 7) * 13)
        p = skia.Path(); p.moveTo(1520, 450); p.lineTo(1520 + math.cos(a - 0.04) * 1400, 450 + math.sin(a - 0.04) * 1400)
        p.lineTo(1520 + math.cos(a + 0.04) * 1400, 450 + math.sin(a + 0.04) * 1400); p.close()
        c.drawPath(p, paint("gold", 0.05))
    c.drawLine(1520, 0, 1520, 120, paint("#3A3048", stroke=10))
    import thumbs as T1
    T1.bulb_forest(c, 1520, 450, 330)
    title_block(c)
    vignette(c, W, H, 0.55)


def thumb_scale(c):
    """You, tiny, in a forest of 30 m trees with a giant dragonfly overhead."""
    swamp_sky(c, T0)
    god_rays(c, T0, 2.2)
    for i in range(7):
        lycopsid(c, 700 + i * 200 + rng(i, 3) * 60, 900, 600 + 200 * rng(i, 4), 34, T0, i, dark=0.3)
    mist(c, 820, T0, 0.25)
    water(c, 900, T0)
    lycopsid(c, 1180, 1000, 860, 110, T0, 9)
    lycopsid(c, 1760, 1000, 900, 120, T0, 10)
    glow(c, 1500, 330, 380, "gold", 0.35)
    dragonfly(c, 1500, 250, 1.25, 0.4, ang=8)
    person(c, 1450, 1000, 170, "stand", "gold")
    millipede(c, 1180, 975, 0.55, T0, 9)
    ferns_ground(c, 1040, T0, 1.0, seed=4)
    spores(c, T0, 0.8)
    c.drawRect(skia.Rect(0, 0, 900, H), paint("space", 0.25))
    title_block(c)
    vignette(c, W, H, 0.55)


def render(fn, name):
    S = skia.Surface(2560, 1440)
    c = S.getCanvas(); c.scale(2560 / 1920, 2560 / 1920)
    fn(c); grain(c, W, H, T0, 0.03)
    small = skia.Surface(1280, 720)
    small.getCanvas().drawImageRect(S.makeImageSnapshot(), skia.Rect(0, 0, 1280, 720), skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear))
    p = os.path.join(OUT, name); small.makeImageSnapshot().save(p, skia.kJPEG, 90); return p


if __name__ == "__main__":
    import thumbs as T1
    ps = [render(thumb_dragonfly, "THUMB_A.jpg"), render(thumb_scale, "THUMB_B.jpg"), render(thumb_bulb, "THUMB_C.jpg")]
    T1.sheet(ps)
    for p in ps: print(p, os.path.getsize(p))
