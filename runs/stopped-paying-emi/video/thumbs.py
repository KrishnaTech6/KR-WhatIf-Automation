"""Thumbnails for 'What If You Stopped Paying Your EMI?' (rules: brand/thumbnail_rules.md).
Krishna (16 Nov 2026): the old gradient + sunburst look felt repetitive, try new styles. Two options:
A = paper-collage newspaper look (matches the video), B = dark spotlight drama. Text = the title."""
import math
import skia
from art import *  # noqa: F401,F403
from krwi.thumb import canvas, save, compare

T0 = 0.0


def hero_house(c, x, y, s, lit=True, dark=False):
    """A detailed house for the thumbnail: tiled roof, chimney, lit windows, rim light, ground shadow, sticker outline."""
    sh = paint("#000000", 0.45); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
    c.drawOval(skia.Rect(x - 330 * s, y - 30 * s, x + 330 * s, y + 40 * s), sh)
    body = skia.Rect(x - 260 * s, y - 330 * s, x + 260 * s, y)
    roof = skia.Path(); roof.moveTo(x - 320 * s, y - 320 * s); roof.lineTo(x, y - 560 * s); roof.lineTo(x + 320 * s, y - 320 * s); roof.close()
    out = skia.Path(); out.addRect(body); out.addPath(roof)
    c.drawPath(out, paint("#FFFFFF", stroke=26 * s))                    # white sticker outline
    c.drawRect(skia.Rect(x + 120 * s, y - 520 * s, x + 190 * s, y - 380 * s), paint("#7E2A1E"))   # chimney
    c.drawRect(body, paint("#F2D9A6" if not dark else "#C9B48A"))
    for i in range(10):
        c.drawLine(x - 260 * s, y - 300 * s + i * 30 * s, x + 260 * s, y - 300 * s + i * 30 * s, paint("#B9965F", 0.35, stroke=3 * s))
    c.drawPath(roof, paint("#B33A2A"))
    for i in range(1, 7):
        yy = y - 320 * s - i * 34 * s
        half = 320 * s * (1 - i * 34 / 240)
        c.drawLine(x - half, yy, x + half, yy, paint("#7E2A1E", 0.6, stroke=4 * s))
    for wx in (-170, 170):                                                    # windows
        r = skia.Rect(x + (wx - 60) * s, y - 260 * s, x + (wx + 60) * s, y - 150 * s)
        c.drawRect(r, paint("#FFD27A" if lit else "#3A3A46"))
        c.drawRect(r, paint("#5A3A22", stroke=10 * s))
        c.drawLine(r.centerX(), r.top(), r.centerX(), r.bottom(), paint("#5A3A22", stroke=6 * s))
    c.drawRect(skia.Rect(x - 70 * s, y - 220 * s, x + 70 * s, y), paint("#5A3A22"))
    rim = paint("#FFE9B0", 0.7, stroke=8 * s); rim.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6))
    c.drawLine(x + 260 * s, y - 320 * s, x + 260 * s, y, rim)
    c.drawLine(x, y - 560 * s, x + 320 * s, y - 320 * s, rim)


def outline_text(c, s, x, y, size, color="cream", stroke=18, kind="extrabold", ink="#120A24"):
    f = font(kind, size)
    sh = paint("#000000", 0.55); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12))
    c.drawString(s, x + 6, y + 10, f, sh)
    c.drawString(s, x, y, f, paint(ink, stroke=stroke))
    c.drawString(s, x, y, f, paint(color))


def rubber(c, x, y, label, size, rot, color="#D62828", fill=None):
    c.save(); c.translate(x, y); c.rotate(rot)
    f = font("extrabold", size)
    w = text_w(label, f) + 70
    h = size * 1.3
    r = skia.RRect.MakeRectXY(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), 16, 16)
    if fill:
        c.drawRRect(r, paint(fill))
    c.drawRRect(r, paint(color, stroke=16))
    c.drawString(label, -text_w(label, f) / 2, size * 0.36, f, paint(color))
    c.restore()


def thumb_a(c):
    """Newspaper front page: the title is the headline, the house gets a giant DEFAULTER stamp."""
    collage_bg(c, 0.0, "#E9DFC8")
    # newspaper sheet
    c.save(); c.rotate(-2, 960, 540)
    c.drawRect(skia.Rect(40, 40, 1880, 1060), paint("#F3EDDD"))
    halftone(c, skia.Path().addRect(skia.Rect(40, 40, 1880, 1060)), "#6E6A60", 0.08, step=10)
    f = font("extrabold", 46)
    c.drawString("THE DAILY NEWS", 80, 110, f, paint("#2A2A2A"))
    c.drawLine(70, 135, 1850, 135, paint("#2A2A2A", stroke=6))
    for col in range(3):
        for i in range(12):
            yy = 860 + i * 16
            if yy > 1040:
                break
            c.drawLine(80 + col * 300, yy, 330 + col * 300, yy, paint("#8A857A", 0.5, stroke=7))
    c.restore()
    # headline = title
    for s, y, col, sz in (("WHAT IF YOU", 270, "#151515", 128), ("STOPPED PAYING", 420, "#151515", 112),
                          ("YOUR", 560, "#151515", 128), ("EMI?", 800, "#C0392B", 250)):
        c.drawString(s, 90, y, font("extrabold", sz), paint(col))
    # hero: house + stamp
    hero_house(c, 1480, 960, 1.15)
    padlock(c, 1480, 900, 1.9, T0, key="ta_lock")
    rubber(c, 1480, 640, "DEFAULTER", 92, -12, fill="#FFFFFF")


def thumb_b(c):
    """Dark spotlight: one light on the house, a red AUCTION tag on the door, the title in heavy type."""
    c.drawRect(skia.Rect(0, 0, W, H), paint("#0B0B10"))
    sp = skia.Paint(Shader=skia.GradientShader.MakeRadial(skia.Point(1420, 600), 760,
                    [col("#FFB347", 0.95), col("#B23A1A", 0.55), col("#0B0B10", 0.0)], [0, 0.5, 1]))
    c.drawRect(skia.Rect(0, 0, W, H), sp)
    hero_house(c, 1420, 980, 1.25, lit=False)
    padlock(c, 1420, 910, 2.2, T0, key="tb_lock")
    # red AUCTION tag hanging on string
    c.drawLine(1420, 760, 1520, 760, paint("#EEEEEE", stroke=5))
    c.save(); c.translate(1580, 800); c.rotate(10)
    c.drawRect(skia.Rect(-150, -60, 150, 60), paint("#D62828"))
    f = font("extrabold", 64); c.drawString("AUCTION", -text_w("AUCTION", f) / 2, 22, f, paint("#FFFFFF"))
    c.restore()
    smartphone(c, 960, 860, 0.55, T0, [("EMI\nBOUNCED", "#C0392B")], 1.0, title="BANK", key="tb_phone", rot=-14)
    outline_text(c, "WHAT IF YOU", 70, 200, 120, "#FFFFFF")
    outline_text(c, "STOPPED PAYING", 70, 360, 130, "#FFFFFF")
    outline_text(c, "YOUR", 70, 520, 130, "#FFFFFF")
    outline_text(c, "EMI?", 70, 790, 280, "#FFD23F")
    vignette(c, W, H, 0.45)


if __name__ == "__main__":
    out = []
    for name, fn in (("THUMB_A.jpg", thumb_a), ("THUMB_B.jpg", thumb_b)):
        s, c = canvas()
        fn(c)
        out.append(save(s, name))
    compare(out)
