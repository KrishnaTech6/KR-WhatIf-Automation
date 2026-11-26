"""Vertical covers (1080x1920) for the Short and the Reel of 'What If Every Indian Got Rs 1 Crore Tomorrow?'.
Cover text <= 6 words, hero centred, all key content inside the 3:4 grid crop (y 240-1680) and clear of the
bottom ~20% / right 120 px UI. Run: KR_RUN=runs/every-indian-1-crore PYTHONPATH=tools:runs/every-indian-1-crore/video \
python3 runs/every-indian-1-crore/video/covers.py"""
import math
import os
import skia
from art import *  # noqa: F401,F403
from krwi.thumb import OUT
from thumbs import outline_text, CREAM, GOLD_T

VW_, VH_ = 1080, 1920
T0 = 0.0


def vcanvas():
    s = skia.Surface(VW_ * 2, VH_ * 2)
    c = s.getCanvas(); c.scale(2, 2)
    return s, c


def vsave(s, name):
    os.makedirs(OUT, exist_ok=True)
    small = skia.Surface(VW_, VH_)
    small.getCanvas().drawImageRect(s.makeImageSnapshot(), skia.Rect(0, 0, VW_, VH_),
                                    skia.SamplingOptions(skia.CubicResampler.Mitchell()))
    p = os.path.join(OUT, name)
    small.makeImageSnapshot().save(p, skia.kJPEG, 90)
    print("wrote", p, os.path.getsize(p) // 1024, "KB")
    return p


def centred(c, s, cy, size, color, max_w=960):
    f = font("extrabold", size)
    w = text_w(s, f)
    if w > max_w:
        size *= max_w / w; f = font("extrabold", size); w = text_w(s, f)
    outline_text(c, s, (VW_ - w) / 2, cy, size, color, stroke=size * 0.13)


def rays(c, cx, cy):
    for i in range(20):
        a = i / 20 * 2 * math.pi
        p = skia.Path(); p.moveTo(cx, cy)
        p.lineTo(cx + math.cos(a - 0.07) * 1800, cy + math.sin(a - 0.07) * 1800)
        p.lineTo(cx + math.cos(a + 0.07) * 1800, cy + math.sin(a + 0.07) * 1800); p.close()
        c.drawPath(p, paint("#FFD27A", 0.15))
    glow(c, cx, cy, 650, "#FF9A3D", 0.9)
    glow(c, cx, cy, 300, "#FFF0C2", 0.65)


def short_cover(c):
    lin(c, 0, 0, VW_, VH_, ["#0B2A6B", "#3A1670", "#8A1F5C"], [0, 0.55, 1])
    cx, cy = 540, 1090
    rays(c, cx, cy)
    for i, (bx, by, r, cr) in enumerate([(300, 1380, -18, 0.0), (790, 1390, 16, 0.0), (230, 1150, -30, 0.55),
                                         (860, 1150, 28, 0.6), (220, 910, -38, 0.9), (880, 890, 34, 0.95)]):
        bundle(c, bx, by, 1.0, T0, key=f"cb{i}", rot=r, crumble=cr)
    phone_msg(c, cx, cy, 1.15, T0, [("₹1,00,00,000", 64, "#1F6E43"), ("CREDITED", 54, "#1F6E43")],
              key="coverphone", rot=-5, head="BANK")
    centred(c, "₹1 CRORE", 420, 230, GOLD_T)
    centred(c, "= ₹2 LAKH?", 600, 170, CREAM)
    vignette(c, VW_, VH_, 0.3)


def reel_cover(c):
    lin(c, 0, 0, VW_, VH_, ["#0B2A6B", "#3A1670", "#8A1F5C"], [0, 0.55, 1])
    cx, cy = 540, 1100
    rays(c, cx, cy)
    # a crorepati's breakfast: the phone says CREDITED, the plate holds dry bread, the milk packet is empty
    phone_msg(c, 800, 1000, 0.8, T0, [("₹1,00,00,000", 64, "#1F6E43"), ("CREDITED", 54, "#1F6E43")],
              key="reelphone", rot=8, head="BANK")
    c.drawOval(skia.Rect(60, 1330, 1000, 1500), paint("#000000", 0.25))
    plate_bread(c, 380, 1300, 1.7, T0, key="cplate")
    milk_packet(c, 300, 960, 1.3, T0, empty=True, key="cmilk")
    c.save(); c.rotate(-12, 300, 1000)
    type_text(c, "EMPTY", 210, 1010, 64, 1.0, color=RED_INK)
    c.restore()
    centred(c, "₹1 CRORE.", 420, 230, GOLD_T)
    centred(c, "NO MILK.", 600, 200, CREAM)
    vignette(c, VW_, VH_, 0.3)


if __name__ == "__main__":
    for fn, name in ((short_cover, "COVER_SHORT.jpg"), (reel_cover, "COVER_REEL.jpg")):
        s, c = vcanvas(); fn(c); vsave(s, name)
