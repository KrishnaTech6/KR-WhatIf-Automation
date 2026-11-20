"""3 hero stills for Krishna's look approval (frame 0 split rooms, Day 14 lab, Day 31 rooftop sunrise)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "../../.."))
sys.path[:0] = [os.path.join(REPO, "tools"), os.path.join(REPO, "brand")]
import skia
from primitives import col, paint, font, text, grain, vignette
from krwi.scene import *

W, H = 1920, 1080
OUT = sys.argv[1] if len(sys.argv) > 1 else HERE


def save(surf, name):
    img = surf.makeImageSnapshot()
    img.save(os.path.join(OUT, name), skia.kPNG)


def split_rooms(c, t=0.6):
    bedroom(c, 0, 0, 960, 1080, t, clock_bedtime=11, ring=1.0, hand_reach=0.5)
    bedroom(c, 960, 0, 960, 1080, t + 0.13, clock_bedtime=10, ring=1.0, hand_reach=0.5)
    c.drawLine(960, 0, 960, H, paint("#F4F1E8", 0.9, stroke=6))
    # title strip
    c.drawRRect(rrect(W / 2 - 330, 34, W / 2 + 330, 112, 39), paint("#0A0716", 0.78))
    c.drawRRect(rrect(W / 2 - 330, 34, W / 2 + 330, 112, 39), paint("#FFD27A", 0.9, stroke=3))
    text(c, "SPOT THE DIFFERENCE", W / 2 + 26, 89, font("extrabold", 46), paint("#FFD27A"))
    # ring timer
    cx, cy = W / 2 - 280, 73
    c.drawCircle(cx, cy, 24, paint("#FFFFFF", 0.25, stroke=6))
    pth = skia.Path(); pth.addArc(skia.Rect(cx - 24, cy - 24, cx + 24, cy + 24), -90, 360 * 0.65)
    c.drawPath(pth, paint("#FFD27A", stroke=6))
    c.drawRRect(rrect(W / 2 - 230, 980, W / 2 + 230, 1050, 35), paint("#0A0716", 0.8))
    text(c, "5 AM · 30 DAYS", W / 2, 1033, font("extrabold", 50), paint("#F4F1E8"))
    grain(c, W, H, t, 0.03)


def lab_day14(c, t=0.4, tired=0.8):
    """Over-the-shoulder: you at the reaction test in a sleep lab at night, beds behind, monitor lagging."""
    c.drawRect(skia.Rect(0, 0, W, H), lgrad(0, 0, 0, H, ["#06111C", "#0A1A2A", "#050A12"], [0, 0.6, 1]))
    # back wall panels + a row of lab beds receding to the right
    for k in range(9):
        x = 760 + k * 130
        c.drawRect(skia.Rect(x, 120, x + 126, 640), paint("#0E2234", 0.6))
    for k in range(4):
        s = 1 - k * 0.18
        bx = 1180 + k * 180; by = 640 - k * 30
        c.drawRRect(rrect(bx - 120 * s, by - 40 * s, bx + 120 * s, by + 10 * s, 10 * s), paint("#BFD6E6", 0.5 - k * 0.08))
        c.drawRRect(rrect(bx - 120 * s, by - 60 * s, bx - 60 * s, by - 34 * s, 8 * s), paint("#E6F0F8", 0.55 - k * 0.1))
        c.drawRect(skia.Rect(bx - 116 * s, by + 10 * s, bx + 116 * s, by + 40 * s), paint("#0A1622"))
        c.drawRRect(rrect(bx + 80 * s, by - 190 * s, bx + 150 * s, by - 120 * s, 6 * s), paint("#0A1A28"))
        c.drawPath(P(*[(bx + 86 * s + j * 6 * s, by - 155 * s + math.sin(j * 1.3 + k) * 14 * s) for j in range(10)], close=False), paint("#4FE0B0", 0.8, stroke=2.5 * s))
    # wall calendar: DAY 14 / 14 with crosses
    c.save(); c.translate(380, 210)
    c.drawRect(skia.Rect(-150, -80, 150, 150), paint("#D8E2EA"))
    c.drawRect(skia.Rect(-150, -80, 150, -36), paint("#2A6F8F"))
    text(c, "SLEEP STUDY", 0, -48, font("bold", 24), paint("#FFFFFF"))
    for k in range(14):
        cx, cy = -120 + (k % 7) * 40, -6 + (k // 7) * 60
        c.drawRect(skia.Rect(cx - 16, cy - 16, cx + 16, cy + 16), paint("#9AAAB8", stroke=2))
        c.drawLine(cx - 12, cy - 12, cx + 12, cy + 12, paint("#C0392B", stroke=4))
        c.drawLine(cx + 12, cy - 12, cx - 12, cy + 12, paint("#C0392B", stroke=4))
    c.restore()
    light(c, 380, 230, 260, "#9FD8FF", 0.10)
    # desk
    c.drawPath(P((0, 760), (1500, 700), (1920, 760), (1920, 1080), (0, 1080)), lgrad(0, 700, 0, 1080, ["#2A3442", "#0C1018"]))
    # the monitor: reaction test
    mx, my = 1040, 470
    c.drawRect(skia.Rect(mx - 20, my + 200, mx + 20, my + 290), paint("#151A22"))
    c.drawRRect(rrect(mx - 120, my + 280, mx + 120, my + 300, 8), paint("#151A22"))
    light(c, mx, my, 700, "#5FC8FF", 0.22)
    c.drawRRect(rrect(mx - 360, my - 220, mx + 360, my + 210, 18), paint("#0A0D12"))
    c.drawRRect(rrect(mx - 340, my - 200, mx + 340, my + 190, 8), lgrad(0, my - 200, 0, my + 190, ["#0F2A3C", "#081824"]))
    text(c, "REACTION TEST", mx, my - 140, font("bold", 34), paint("#9FD8FF"))
    light(c, mx, my - 10, 110, "#FF4A3A", 0.7)
    c.drawCircle(mx, my - 10, 44, rgrad(mx, my - 10, 44, ["#FFD0C0", "#FF4A3A", "#B01810"], [0, 0.5, 1]))
    text(c, "0.71 s", mx, my + 110, font("extrabold", 64), paint("#FF6A5A"))
    text(c, "LAPSE  ·  NORMAL ~0.25 s", mx, my + 160, font("bold", 22), paint("#9FD8FF", 0.8))
    # coffee mug + papers on the desk
    c.drawRRect(rrect(1500, 690, 1580, 790, 12), lgrad(1500, 0, 1580, 0, ["#E8E2D6", "#A8A094"]))
    c.drawPath(P((1580, 712), (1580, 770, "q", 1622, 742), close=False), paint("#C8C2B6", stroke=10))
    c.drawPath(P((1300, 800), (1460, 780), (1480, 860), (1310, 880)), paint("#DDE4EA", 0.85))
    # you, over the shoulder, head drooping
    person_desk(c, 470, 1000, 1.25, tired=tired, rim="#7FD8FF", rim_a=0.8)
    # hand on the space bar, keyboard
    c.drawRRect(rrect(760, 820, 1180, 880, 10), lgrad(0, 820, 0, 880, ["#2A303A", "#12161C"]))
    for k in range(14):
        c.drawRRect(rrect(780 + k * 28, 832, 802 + k * 28, 850, 3), paint("#3A4250"))
    c.drawRRect(rrect(880, 856, 1060, 872, 4), paint("#4A5262"))
    # sticky note falling: I FEEL FINE
    c.save(); c.translate(1560, 300); c.rotate(-18)
    c.drawRect(skia.Rect(-80, -70, 80, 70), blurp("#000000", 0.4, 8))
    c.drawRect(skia.Rect(-84, -76, 84, 76), lgrad(0, -76, 0, 76, ["#FFE98A", "#F2C94C"]))
    text(c, "I FEEL", 0, -6, font("extrabold", 34), paint("#3A3020"))
    text(c, "FINE", 0, 38, font("extrabold", 34), paint("#3A3020"))
    c.restore()
    for k in range(3):
        c.drawLine(1500 + k * 30, 190 - k * 10, 1520 + k * 30, 230 - k * 10, paint("#FFFFFF", 0.25, stroke=3))
    # chapter label
    text(c, "DAY 14", 200, 990, font("extrabold", 80), paint("#F4F1E8"), align="left") if False else None
    c.drawRect(skia.Rect(0, 0, W, H), rgrad(W * 0.55, H * 0.45, 1250, [("#000000", 0), ("#000000", 0.05), ("#000000", 0.75)], [0, 0.5, 1]))
    grain(c, W, H, t, 0.035)


def rooftop_sunrise(c, t=0.5, p=1.0):
    """Day 31: you on a Delhi rooftop at sunrise, seen from behind (the viewer is this person)."""
    sunrise_sky(c, 0, 0, W, 860, p, sun=(1360, 520, 70))
    # far haze layers of rooftops, warm rim light from the sun
    delhi_rooftops(c, 0, W, 700, t, layer=2, color="#7A4A5A", lit=0.0, seed=11, rim="#FFD08A", rim_a=0.5)
    c.drawRect(skia.Rect(0, 560, W, 760), lgrad(0, 560, 0, 760, [("#FFC890", 0), ("#FFC890", 0.35)]))
    delhi_rooftops(c, 0, W, 780, t, layer=1, color="#4A2A3A", lit=0.0, seed=5, rim="#FFC070", rim_a=0.6)
    c.drawRect(skia.Rect(0, 700, W, 860), lgrad(0, 700, 0, 860, [("#FFB070", 0), ("#FFB070", 0.25)]))
    # pigeons
    for k in range(7):
        x, y = 600 + k * 70 + math.sin(k) * 40, 300 + math.cos(k * 1.7) * 60
        c.drawPath(P((x - 16, y), (x, y + 4, "q", -8 + x, y - 10), (x + 16, y, "q", x + 8, y - 10), close=False), paint("#3A2430", stroke=4))
    # your rooftop: floor, parapet, water tank, clothesline
    c.drawPath(P((0, 860), (W, 830), (W, H), (0, H)), lgrad(0, 830, 0, H, ["#6A4A44", "#2A1A1C"]))
    c.drawRect(skia.Rect(0, 800, W, 870), lgrad(0, 800, 0, 870, ["#8A5A4A", "#3A2424"]))
    c.drawLine(0, 800, W, 800, paint("#FFD8A0", 0.7, stroke=4))
    water_tank(c, 260, 820, 2.6, color="#14121C", rim="#FFC870", rim_a=0.8)
    c.drawLine(420, 520, 1900, 560, paint("#2A1A1C", stroke=3))
    for k, (cl, w_) in enumerate((("#C8433A", 90), ("#3F6FB0", 70), ("#E9D8A6", 110), ("#2A9D8F", 80))):
        x = [420, 600, 1480, 1680][k]; y = 524 + [0, 4, 30, 36][k]
        c.drawPath(P((x, y), (x + w_, y + 3), (x + w_ - 8, y + 130), (x + 6, y + 126)), lgrad(x, y, x + w_, y + 130, [cl, "#000000"], [0.5, 1.6]))
        c.drawLine(x + w_ - 4, y + 4, x + w_ - 10, y + 126, paint("#FFD08A", 0.6, stroke=3))
    # you, back to camera, stretching toward the sun
    person_back(c, 980, 1050, 0.95, arms=0.85, rim="#FFD08A", rim_a=1.0)
    light(c, 1360, 520, 900, "#FFB060", 0.12)
    c.drawRect(skia.Rect(0, 0, W, H), rgrad(W * 0.6, H * 0.55, 1300, [("#000000", 0), ("#000000", 0.0), ("#000000", 0.5)], [0, 0.6, 1]))
    grain(c, W, H, t, 0.03)


if __name__ == "__main__":
    for fn, name in ((split_rooms, "hero1_split.png"), (lab_day14, "hero2_day14.png"), (rooftop_sunrise, "hero3_day31.png")):
        s = skia.Surface(W, H); fn(s.getCanvas()); save(s, name)
