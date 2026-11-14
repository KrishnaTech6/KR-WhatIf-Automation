"""Thumbnail for 'What If You Didn't Use Your Phone for 30 Days?' (rules: brand/thumbnail_rules.md).
One thumbnail; text = the title; hero = a glowing phone locked inside a glass jar, notifications piling up on the glass."""
import math
import skia
from art import *  # noqa: F401,F403
from krwi.thumb import canvas, save, compare

T0 = 0.0


def outline_text(c, s, x, y, size, color="cream", stroke=18, kind="extrabold"):
    f = font(kind, size)
    sh = paint("#000000", 0.55); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 12))
    c.drawString(s, x + 6, y + 10, f, sh)
    c.drawString(s, x, y, f, paint("#120A24", stroke=stroke))
    c.drawString(s, x, y, f, paint(color))


def words(c, parts, x, y, size):
    f = font("extrabold", size)
    for s, colr in parts:
        outline_text(c, s, x, y, size, colr)
        x += text_w(s, f)


def jar(c, cx, cy):
    # glass jar body + lid, phone inside, notification bubbles pressed against the glass
    body = skia.RRect.MakeRectXY(skia.Rect(cx - 300, cy - 330, cx + 300, cy + 380), 90, 90)
    c.drawRRect(body, paint("#BFE8FF", 0.16))
    smartphone(c, cx, cy + 40, 0.92, T0, "notifs", rot=-6, glow_a=0.9, notifs=99)
    for i, (dx, dy, r) in enumerate([(-200, -200, -8), (170, -120, 6), (-210, 120, 4), (190, 220, -5), (-60, -280, 3)]):
        c.save(); c.translate(cx + dx, cy + dy); c.rotate(r)
        bubble(c, 0, 0, 0.8, 1.0, i=i)
        c.restore()
    c.drawRRect(body, paint("#FFFFFF", 0.85, stroke=14))                  # white sticker outline
    c.drawRRect(body, paint("#9FD8FF", 0.6, stroke=5))
    hl = skia.Path(); hl.moveTo(cx - 230, cy - 230); hl.quadTo(cx - 260, cy + 50, cx - 220, cy + 280)
    c.drawPath(hl, paint("#FFFFFF", 0.55, stroke=22))                      # glass highlight
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(cx - 320, cy - 420, cx + 320, cy - 330), 26, 26), paint("#C9CCD6"))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(cx - 320, cy - 420, cx + 320, cy - 330), 26, 26), paint("#FFFFFF", stroke=10))
    for k in range(9):
        c.drawLine(cx - 290 + k * 72, cy - 410, cx - 290 + k * 72, cy - 340, paint("#9AA0B0", stroke=6))
    padlock(c, cx + 250, cy - 330, 0.9, 1.0)


def grad(x0, y0, x1, y1, cols, stops=None, a=1.0):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)], [col(cc, a) for cc in cols], stops))
    return p


def jar_real(c, cx, cy):
    """A real-looking glass mason jar: thick rim, curved shoulders, glare, a brushed-metal screw lid, the phone inside."""
    w, top, bot = 290, cy - 300, cy + 390
    body = skia.Path()
    body.moveTo(cx - 200, top); body.lineTo(cx + 200, top)
    body.cubicTo(cx + 210, top + 60, cx + w, top + 70, cx + w, top + 170)
    body.lineTo(cx + w, bot - 70); body.quadTo(cx + w, bot, cx + w - 70, bot)
    body.lineTo(cx - w + 70, bot); body.quadTo(cx - w, bot, cx - w, bot - 70)
    body.lineTo(cx - w, top + 170); body.cubicTo(cx - w, top + 70, cx - 210, top + 60, cx - 200, top); body.close()
    # shadow on the ground
    sh = paint("#000000", 0.45); sh.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
    c.drawOval(skia.Rect(cx - w - 20, bot - 30, cx + w + 20, bot + 50), sh)
    # back glass tint
    c.drawPath(body, grad(cx - w, 0, cx + w, 0, ["#9ED8F0", "#DDF4FF", "#7FB8D8"], [0, 0.35, 1], 0.22))
    # the phone inside, slightly tinted by the glass
    smartphone(c, cx + 10, cy + 70, 0.88, T0, "notifs", rot=-7, glow_a=0.9, notifs=99)
    c.drawPath(body, paint("#BFEFFF", 0.12))
    # glass edges: thick darker sides, bright inner rim
    c.drawPath(body, paint("#E8FAFF", 0.9, stroke=10))
    c.drawPath(body, paint("#5E9FC0", 0.55, stroke=3))
    # glare streaks
    g1 = skia.Path(); g1.moveTo(cx - w + 45, top + 190); g1.quadTo(cx - w + 30, cy + 80, cx - w + 55, bot - 90)
    c.drawPath(g1, paint("#FFFFFF", 0.75, stroke=26))
    g2 = skia.Path(); g2.moveTo(cx - w + 95, top + 220); g2.quadTo(cx - w + 85, cy, cx - w + 100, cy + 140)
    c.drawPath(g2, paint("#FFFFFF", 0.35, stroke=9))
    g3 = skia.Path(); g3.moveTo(cx + w - 40, top + 200); g3.lineTo(cx + w - 40, bot - 120)
    c.drawPath(g3, paint("#FFFFFF", 0.3, stroke=12))
    # bottom thickness
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(cx - w + 30, bot - 40, cx + w - 30, bot - 12), 14, 14), paint("#E8FAFF", 0.35))
    # neck ring + metal screw lid
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect(cx - 215, top - 20, cx + 215, top + 14), 12, 12), paint("#E8FAFF", 0.7))
    lid = skia.Rect(cx - 230, top - 120, cx + 230, top - 10)
    c.drawRRect(skia.RRect.MakeRectXY(lid, 18, 18), grad(cx - 230, 0, cx + 230, 0, ["#6E7480", "#E9ECF2", "#A5ABB6", "#F5F7FA", "#5C626C"], [0, 0.25, 0.5, 0.7, 1]))
    for k in range(4):
        y = top - 100 + k * 26
        c.drawLine(cx - 228, y, cx + 228, y, paint("#4A4F58", 0.35, stroke=3))
    c.drawRRect(skia.RRect.MakeRectXY(lid, 18, 18), paint("#3C4048", stroke=4))


def chain_lock(c, cx, cy):
    """The lid is what opens, so the lid is what gets locked: a chain wrapped round the screw lid and over its top,
    and a heavy brass padlock hanging from it in front of the jar's shoulder."""
    top = cy - 300
    def link(x, yy, i, ang=0.0):
        c.save(); c.translate(x, yy); c.rotate(ang)
        r = skia.Rect(-24, -13, 24, 13) if i % 2 == 0 else skia.Rect(-22, -6, 22, 6)
        c.drawOval(r, paint("#2E3138", stroke=13)); c.drawOval(r, paint("#B9BFCA", stroke=8))
        c.restore()
    # round the lid band
    for row, yy in enumerate((top - 92, top - 40)):
        for i in range(12):
            link(cx - 236 + i * 43, yy + 5 * math.sin(i + row), i + row)
    px, py = cx + 30, top + 40
    sh = skia.Path(); sh.addArc(skia.Rect(px - 52, py - 120, px + 52, py - 10), 180, 180)
    c.drawPath(sh, paint("#2E3138", stroke=26)); c.drawPath(sh, paint("#C9CED8", stroke=16))
    c.drawLine(px - 52, py - 65, px - 52, py - 10, paint("#C9CED8", stroke=16))
    c.drawLine(px + 52, py - 65, px + 52, py - 10, paint("#C9CED8", stroke=16))
    body = skia.RRect.MakeRectXY(skia.Rect(px - 85, py - 20, px + 85, py + 130), 22, 22)
    c.drawRRect(body, grad(px - 85, py - 20, px + 85, py + 130, ["#F7D27A", "#C9932E", "#8A5F14"], [0, 0.55, 1]))
    c.drawRRect(body, paint("#5E3F0C", stroke=5))
    c.drawLine(px - 60, py - 5, px + 50, py - 5, paint("#FFF1C4", 0.7, stroke=5))
    c.drawCircle(px, py + 45, 16, paint("#2A1A05")); c.drawRect(skia.Rect(px - 6, py + 45, px + 6, py + 90), paint("#2A1A05"))

def thumb(c):
    lin(c, 0, 0, W, H, ["#0E2A5C", "#2B1460", "#7A1E5A"], [0, 0.55, 1])
    cx, cy = 1490, 600
    for i in range(18):
        a = i / 18 * 2 * math.pi
        p = skia.Path(); p.moveTo(cx, cy)
        p.lineTo(cx + math.cos(a - 0.08) * 1400, cy + math.sin(a - 0.08) * 1400)
        p.lineTo(cx + math.cos(a + 0.08) * 1400, cy + math.sin(a + 0.08) * 1400); p.close()
        c.drawPath(p, paint("#FFB347", 0.16))
    glow(c, cx, cy, 700, "#FF8A3D", 0.9)
    glow(c, cx, cy, 300, "#FFE3A3", 0.55)
    jar_real(c, cx, cy)
    chain_lock(c, cx, cy)
    words(c, [("WHAT IF YOU", "cream")], 60, 230, 128)
    words(c, [("DIDN'T USE", "cream")], 60, 390, 128)
    words(c, [("YOUR PHONE", "cream")], 60, 550, 128)
    words(c, [("FOR ", "cream"), ("30 DAYS?", "gold")], 60, 730, 150)
    vignette(c, W, H, 0.3)


if __name__ == "__main__":
    s, c = canvas()
    thumb(c)
    p = save(s, "THUMB.jpg")
    compare([p])
