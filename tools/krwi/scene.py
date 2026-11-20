"""Detailed scene kit (Krishna, 20 Nov 2026: "it should feel like the scene, the viewer should see himself").
Painterly vector drawing with depth: gradients, soft light, blur, rim light. Reusable in every video:
  bedroom(c, x0, y0, w, h, t, ...)      Indian bedroom at night (fan, window grill + Delhi skyline, bed, side table)
  alarm_clock(c, x, y, s, t, ...)       twin-bell clock, metal + glass, optional bedtime sub-dial, ringing shake
  delhi_rooftops(c, y, t, warm, ...)    rooftops with water tanks, dish antennas, clotheslines, haze
  sunrise_sky(c, t, p)                  night -> gold sky with sun, rays and haze (p = 0 night .. 1 sunrise)
  person_back(c, x, y, s, ...)          a young Indian adult seen from behind (viewer = this person), rim light
  person_desk(c, x, y, s, ...)          seated at a desk, over-the-shoulder, head drooping by `tired`
All coordinates are frame pixels; s = scale (1 = a ~600 px tall adult)."""
import math
import skia

from primitives import col, paint, font, text, clamp, ease

# ------------------------------------------------------------------ low-level helpers


def P(*pts, close=True):
    """Path from points; a point (x, y, 'q', cx, cy) means a quad curve to (x, y) via (cx, cy)."""
    p = skia.Path()
    p.moveTo(*pts[0][:2])
    for q in pts[1:]:
        if len(q) == 2:
            p.lineTo(*q)
        elif q[2] == "q":
            p.quadTo(q[3], q[4], q[0], q[1])
        elif q[2] == "c":
            p.cubicTo(q[3], q[4], q[5], q[6], q[0], q[1])
    if close:
        p.close()
    return p


def blurp(color, a=1.0, sigma=8.0, stroke=None):
    pt = paint(color, a, stroke=stroke)
    pt.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, sigma))
    return pt


def lgrad(x0, y0, x1, y1, cols, stops=None, a=1.0):
    pt = skia.Paint(AntiAlias=True)
    pt.setShader(skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)],
                                                 [col(k, a) if isinstance(k, str) else col(*k) for k in cols], stops))
    return pt


def rgrad(x, y, r, cols, stops=None, a=1.0):
    pt = skia.Paint(AntiAlias=True)
    pt.setShader(skia.GradientShader.MakeRadial(skia.Point(x, y), max(r, 1),
                                                 [col(k, a) if isinstance(k, str) else col(*k) for k in cols], stops))
    return pt


def light(c, x, y, r, color, a=0.5):
    """Additive-looking soft light pool."""
    c.drawCircle(x, y, r, rgrad(x, y, r, [(color, a), (color, a * 0.35), (color, 0)], [0, 0.45, 1]))


def rrect(x0, y0, x1, y1, r):
    return skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)


def noise_rng(i, k=1.0):
    v = math.sin(i * 12.9898 + k * 78.233) * 43758.5453
    return v - math.floor(v)


# ------------------------------------------------------------------ alarm clock


def alarm_clock(c, x, y, s, t, hour=5.0, minute=0.0, ring=0.0, bedtime=None, glow_a=1.0, body="#C8433A"):
    """Twin-bell alarm clock centred on its face (x, y); face radius 100*s. ring 0..1 = shaking + sound arcs.
    bedtime: None, or a number shown on a small sub-dial at the bottom of the face (the 'spot the difference')."""
    sh = math.sin(t * 70) * 4 * ring * s
    rot = math.sin(t * 55) * 0.05 * ring
    c.save(); c.translate(x + sh, y); c.rotate(math.degrees(rot)); c.scale(s, s)
    R = 100
    # warm light the clock throws around it
    if glow_a > 0:
        light(c, 0, 10, 330, "#FFB45C", 0.32 * glow_a)
    # contact shadow
    c.drawOval(skia.Rect(-120, 150, 120, 182), blurp("#000000", 0.55, 10))
    # legs
    for sx in (-1, 1):
        c.drawPath(P((sx * 52, 92), (sx * 86, 160), (sx * 72, 166), (sx * 40, 104)), lgrad(0, 92, 0, 166, ["#8C2A24", "#3A0F0C"]))
        c.drawOval(skia.Rect(sx * 79 - 14, 156, sx * 79 + 14, 168), paint("#2A0B09"))
    # bells: domes on top, slightly apart
    for sx in (-1, 1):
        bx, by = sx * 70, -112
        c.save(); c.translate(bx, by); c.rotate(sx * 28)
        c.drawPath(P((-50, 18), (-46, -10, "q", -50, 6), (0, -46, "q", -36, -46), (46, -10, "q", 36, -46), (50, 18, "q", 50, 6)),
                   lgrad(-50, -46, 50, 18, ["#FFE8B8", "#D9A441", "#7A4E12"], [0, 0.45, 1]))
        c.drawPath(P((-34, -24), (0, -40, "q", -22, -40), (18, -32, "q", 10, -38), (-10, -16, "q", 0, -30)), paint("#FFFFFF", 0.55))
        c.drawRRect(rrect(-52, 12, 52, 22, 5), paint("#6B4210"))
        c.drawCircle(0, -48, 7, paint("#C99636"))
        c.restore()
    # hammer between the bells
    hx = math.sin(t * 90) * 26 * ring
    c.drawLine(0, -98, hx, -150, paint("#4A4A52", stroke=7))
    c.drawCircle(hx, -152, 9, paint("#9A9AA6"))
    # carry handle
    c.drawPath(P((-40, -104), (0, -150, "q", -40, -150), (40, -104, "q", 40, -150), close=False), paint("#2A2A30", stroke=10))
    # body ring (lacquered metal)
    c.drawCircle(0, 0, R + 22, lgrad(-R, -R, R, R, ["#F07A6A", body, "#5A1410"], [0, 0.45, 1]))
    c.drawCircle(0, 0, R + 22, paint("#FFD8C8", 0.5, stroke=3))
    c.drawPath(P((-R - 10, -30), (-30, -R - 12, "q", -R + 4, -R + 6), (-20, -R - 4, "q", -24, -R - 8), (-R + 4, -20, "q", -R + 14, -R + 14)), paint("#FFFFFF", 0.35))
    # chrome bezel
    c.drawCircle(0, 0, R + 6, lgrad(-R, -R, R, R, ["#FFFFFF", "#9EA3AE", "#4C505A", "#D7DAE0"], [0, 0.35, 0.7, 1]))
    # face
    c.drawCircle(0, 0, R, rgrad(-20, -30, R * 1.3, ["#FFF8E8", "#F2E6CC", "#D8C7A4"], [0, 0.6, 1]))
    # ticks and numbers
    f = font("bold", 24)
    for k in range(60):
        a = math.radians(k * 6 - 90)
        r0 = R - (16 if k % 5 == 0 else 9)
        c.drawLine(math.cos(a) * r0, math.sin(a) * r0, math.cos(a) * (R - 5), math.sin(a) * (R - 5),
                   paint("#2A2230", stroke=3.4 if k % 5 == 0 else 1.4))
    for n in range(1, 13):
        a = math.radians(n * 30 - 90)
        text(c, str(n), math.cos(a) * (R - 33), math.sin(a) * (R - 33) + 8, f, paint("#2A2230"))
    # bedtime sub-dial
    if bedtime is not None:
        c.drawCircle(0, 44, 25, paint("#E9DCC0"))
        c.drawCircle(0, 44, 25, paint("#8A7A5A", stroke=2.5))
        text(c, "BED", 0, 34, font("bold", 10), paint("#6A5A3A"))
        text(c, str(bedtime), 0, 60, font("extrabold", 21), paint("#B22A22"))
    # hands at hour:minute
    ha = math.radians((hour % 12 + minute / 60) * 30 - 90)
    ma = math.radians(minute * 6 - 90)
    c.drawLine(0, 0, math.cos(ha) * 50, math.sin(ha) * 50, paint("#1A1420", stroke=9))
    c.drawLine(0, 0, math.cos(ma) * 78, math.sin(ma) * 78, paint("#1A1420", stroke=6))
    alarm_a = math.radians(5 * 30 - 90)
    c.drawLine(0, 0, math.cos(alarm_a) * 62, math.sin(alarm_a) * 62, paint("#C9302C", stroke=3))
    c.drawCircle(0, 0, 9, paint("#1A1420")); c.drawCircle(0, 0, 4, paint("#C9302C"))
    # glass reflection
    c.drawPath(P((-70, -50), (-10, -88, "q", -56, -84), (-30, -60, "q", -40, -74), (-68, -24, "q", -58, -46)), paint("#FFFFFF", 0.38))
    c.restore()
    # ringing arcs (drawn unrotated)
    if ring > 0:
        for k in range(3):
            ph = (t * 2.2 + k / 3) % 1
            r = (150 + ph * 120) * s
            for sx in (-1, 1):
                pth = skia.Path(); pth.addArc(skia.Rect(x - r, y - 40 * s - r, x + r, y - 40 * s + r),
                                              (-90 + sx * 50) - 22, 44)
                c.drawPath(pth, paint("#FFE2A8", (1 - ph) * 0.8 * ring, stroke=6 * s))


# ------------------------------------------------------------------ Delhi skyline / rooftops


def water_tank(c, x, y, s, color="#0B0E1E", rim=None, rim_a=0.0):
    """Black plastic rooftop water tank (ribbed cylinder, domed lid), base at (x, y)."""
    w, h = 64 * s, 70 * s
    c.drawRRect(rrect(x - w / 2, y - h, x + w / 2, y, 10 * s), paint(color))
    c.drawPath(P((x - w / 2, y - h + 6 * s), (x + w / 2, y - h + 6 * s, "q", x, y - h - 30 * s)), paint(color))
    c.drawRRect(rrect(x - 12 * s, y - h - 26 * s, x + 12 * s, y - h - 14 * s, 3 * s), paint(color))
    for k in range(3):
        yy = y - h * (0.25 + k * 0.25)
        c.drawLine(x - w / 2, yy, x + w / 2, yy, paint("#FFFFFF", 0.05, stroke=2 * s))
    if rim and rim_a > 0:
        c.drawLine(x + w / 2 - 2 * s, y - h, x + w / 2 - 2 * s, y - 4 * s, paint(rim, rim_a, stroke=3 * s))


def dish(c, x, y, s, color="#0B0E1E"):
    c.drawLine(x, y, x + 6 * s, y - 34 * s, paint(color, stroke=4 * s))
    c.save(); c.translate(x + 6 * s, y - 40 * s); c.rotate(-30)
    c.drawOval(skia.Rect(-22 * s, -14 * s, 22 * s, 14 * s), paint(color))
    c.drawLine(0, 0, 18 * s, -18 * s, paint(color, stroke=2.5 * s))
    c.restore()


def delhi_rooftops(c, x0, x1, y, t, layer=0, color="#0B0E1E", lit=0.0, rim=None, rim_a=0.0, seed=0):
    """A band of flat-roofed houses from x0 to x1, roof line around y. layer 0 = near (big), 2 = far (small)."""
    s = [1.0, 0.62, 0.38][layer]
    x = x0 - 40
    i = seed * 31
    while x < x1 + 40:
        w = (150 + noise_rng(i, 1) * 180) * s
        h = (40 + noise_rng(i, 2) * 160) * s
        top = y - h
        c.drawRect(skia.Rect(x, top, x + w, y + 900), paint(color))
        # parapet
        c.drawRect(skia.Rect(x - 4 * s, top - 14 * s, x + w + 4 * s, top), paint(color))
        if rim and rim_a > 0:
            c.drawLine(x, top - 14 * s, x + w, top - 14 * s, paint(rim, rim_a, stroke=3 * s))
        # windows (some lit)
        for wy in range(int(top + 30 * s), int(y + 200 * s), int(70 * s)):
            for wx in range(int(x + 22 * s), int(x + w - 30 * s), int(56 * s)):
                k = i * 7 + wx * 3 + wy
                if noise_rng(k, 5) < 0.22 * lit + 0.02:
                    c.drawRect(skia.Rect(wx, wy, wx + 20 * s, wy + 28 * s), paint("#FFC873", 0.75))
        if noise_rng(i, 3) > 0.35:
            water_tank(c, x + w * (0.2 + 0.5 * noise_rng(i, 4)), top - 14 * s, s, color, rim, rim_a)
        if noise_rng(i, 6) > 0.6:
            dish(c, x + w * 0.8, top - 14 * s, s, color)
        if noise_rng(i, 7) > 0.7:   # stair room (mumty)
            c.drawRect(skia.Rect(x + w * 0.05, top - 70 * s, x + w * 0.3, top), paint(color))
        x += w + 6 * s
        i += 1


def sunrise_sky(c, x0, y0, x1, y1, p=0.0, sun=None):
    """Sky gradient from night (p=0) to sunrise (p=1). sun=(x, y, r) draws the sun with rays."""
    def mix(a, b, k):
        ca, cb = col(a), col(b)
        return "#%02X%02X%02X" % tuple(int(skia.ColorGetR(ca) * (1 - k) + skia.ColorGetR(cb) * k) if i == 0 else
                                       int(skia.ColorGetG(ca) * (1 - k) + skia.ColorGetG(cb) * k) if i == 1 else
                                       int(skia.ColorGetB(ca) * (1 - k) + skia.ColorGetB(cb) * k) for i in range(3))
    top = mix("#070A22", "#2B3F7A", p)
    mid = mix("#14204E", "#E7875A", p)
    low = mix("#2A2E5E", "#FFD08A", p)
    c.drawRect(skia.Rect(x0, y0, x1, y1), lgrad(0, y0, 0, y1, [top, mid, low], [0, 0.62, 1]))
    if p < 0.6:
        for k in range(90):
            sx = x0 + noise_rng(k, 1) * (x1 - x0)
            sy = y0 + noise_rng(k, 2) * (y1 - y0) * 0.7
            c.drawCircle(sx, sy, 0.8 + noise_rng(k, 3) * 1.8, paint("#FFFFFF", (0.25 + 0.6 * noise_rng(k, 4)) * (1 - p / 0.6)))
    if sun:
        sx, sy, r = sun
        light(c, sx, sy, r * 9, "#FFB050", 0.55 * p)
        light(c, sx, sy, r * 3.5, "#FFE6A8", 0.7 * p)
        # god rays
        for k in range(14):
            a = math.radians(-180 + k * 13 + 4)
            L = r * (10 + 4 * noise_rng(k, 9))
            wdt = 0.05 + 0.04 * noise_rng(k, 8)
            pth = P((sx, sy), (sx + math.cos(a - wdt) * L, sy + math.sin(a - wdt) * L), (sx + math.cos(a + wdt) * L, sy + math.sin(a + wdt) * L))
            c.drawPath(pth, blurp("#FFE7B0", 0.10 * p, 14))
        c.drawCircle(sx, sy, r, rgrad(sx, sy, r, ["#FFFBEA", "#FFE7A0", "#FFC060"], [0, 0.7, 1]))


# ------------------------------------------------------------------ people


def person_back(c, x, y, s, arms=0.3, shirt="#2F5D8C", pants="#22263A", rim="#FFC870", rim_a=0.9, skin="#B9805A",
                hair="#140E14"):
    """Young adult from behind, feet at (x, y); ~640*s px tall. arms 0 = down, 1 = raised in a V (stretching)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawOval(skia.Rect(-130, -16, 130, 16), blurp("#000000", 0.45, 10))
    # legs: track pants, slight A-stance, knee fold, chappals
    for sx in (-1, 1):
        c.drawPath(P((sx * 6, -310), (sx * 74, -316), (sx * 66, -150, "q", sx * 74, -230), (sx * 58, -16), (sx * 22, -16),
                     (sx * 12, -150, "q", sx * 14, -90), (sx * 6, -310, "q", sx * 8, -230)),
                   lgrad(sx * 74, -316, sx * 6, -16, [pants, "#11131C"]))
        c.drawPath(P((sx * 30, -170), (sx * 60, -160, "q", sx * 46, -176), close=False), paint("#000000", 0.25, stroke=3))
        c.drawLine(sx * (66 if sx > 0 else 64), -300, sx * 58, -40, paint(rim, rim_a * (0.6 if sx > 0 else 0.2), stroke=3))
        c.drawRRect(rrect(sx * 40 - 26, -24, sx * 40 + 26, 0, 10), paint("#3A2A22"))
        c.drawRRect(rrect(sx * 40 - 18, -30, sx * 40 + 18, -16, 6), paint(skin))
    # arms (drawn before the torso so the shoulders cover the joint)
    for sx in (-1, 1):
        th = math.radians(14 + 128 * arms)             # angle away from straight down
        sh_x, sh_y = sx * 96, -536
        ux, uy = sh_x + sx * math.sin(th) * 128, sh_y + math.cos(th) * 128
        th2 = th + math.radians(12 * arms)
        hx, hy = ux + sx * math.sin(th2) * 122, uy + math.cos(th2) * 122
        c.drawLine(sh_x, sh_y, ux, uy, paint(skin, stroke=34))
        c.drawLine(ux, uy, hx, hy, paint(skin, stroke=30))
        c.drawLine(sh_x, sh_y, sh_x + sx * math.sin(th) * 60, sh_y + math.cos(th) * 60, paint(shirt, stroke=52))   # sleeve
        c.drawLine(ux, uy, hx, hy, paint(rim, rim_a * 0.6, stroke=4))
        ang = math.degrees(math.atan2(hy - uy, hx - ux))
        c.save(); c.translate(hx, hy); c.rotate(ang)
        c.drawOval(skia.Rect(-6, -17, 34, 17), paint(skin))                     # palm along the forearm
        for k in range(4):
            yy = -12 + k * 8
            c.drawLine(28, yy, 50 - abs(k - 1.5) * 4, yy * 1.15, paint(skin, stroke=7))
        c.drawLine(8, -15 * sx, 24, -30 * sx, paint(skin, stroke=8))           # thumb
        c.restore()
    # torso: T-shirt, broad shoulders, slight waist taper, folds, hem
    c.drawPath(P((-70, -556), (70, -556, "q", 0, -566), (116, -520, "q", 106, -556), (92, -300, "q", 104, -420),
                 (-92, -300, "q", 0, -292), (-116, -520, "q", -104, -420), (-70, -556, "q", -106, -556)),
               lgrad(-110, -556, 110, -300, [shirt, "#1B3554"]))
    c.drawPath(P((-30, -500), (-14, -330, "q", -40, -420), close=False), paint("#000000", 0.18, stroke=5))
    c.drawPath(P((46, -490), (34, -330, "q", 60, -410), close=False), paint("#000000", 0.18, stroke=5))
    c.drawPath(P((-60, -520), (60, -520, "q", 0, -500), close=False), paint("#000000", 0.15, stroke=4))   # shoulder-blade fold
    c.drawLine(-92, -306, 92, -306, paint("#000000", 0.3, stroke=6))
    c.drawPath(P((116, -516), (92, -304, "q", 106, -420), close=False), paint(rim, rim_a, stroke=6))
    c.drawPath(P((-116, -516), (-92, -304, "q", -106, -420), close=False), paint(rim, rim_a * 0.4, stroke=4))
    # neck, ears, head
    c.drawPath(P((-26, -600), (26, -600), (32, -552), (-32, -552)), paint(skin))
    c.drawPath(P((-26, -572), (26, -572, "q", 0, -560), close=False), paint("#000000", 0.15, stroke=6))
    c.drawOval(skia.Rect(-64, -680, -44, -630), paint(skin)); c.drawOval(skia.Rect(44, -680, 64, -630), paint(skin))
    c.drawOval(skia.Rect(-54, -720, 54, -588), paint(skin))
    # hair: fuller on top, short at the nape with an uneven hairline
    c.drawPath(P((-58, -640), (-52, -712, "q", -66, -688), (0, -742, "q", -32, -744), (52, -712, "q", 32, -744),
                 (58, -640, "q", 66, -688), (44, -612, "q", 54, -620), (24, -602, "q", 36, -598), (0, -606, "q", 12, -596),
                 (-24, -602, "q", -12, -596), (-44, -612, "q", -36, -598), (-58, -640, "q", -54, -620)),
               lgrad(0, -742, 0, -600, ["#2E2228", hair]))
    for k in range(10):
        xx = -44 + k * 10
        c.drawPath(P((xx, -730 + abs(xx) * 0.35), (xx + 4, -616, "q", xx - 10, -670), close=False), paint("#FFFFFF", 0.06, stroke=2))
    c.drawPath(P((50, -712), (58, -640, "q", 64, -684), close=False), paint(rim, rim_a * 0.6, stroke=3))
    c.restore()


def person_desk(c, x, y, s, tired=0.0, shirt="#3B4A6B", skin="#B9805A", hair="#140E14", rim="#7FE0FF", rim_a=0.7):
    """Seated at a desk, seen over the left shoulder; (x, y) = seat point. tired 0..1 droops the head."""
    c.save(); c.translate(x, y); c.scale(s, s)
    # chair back
    c.drawRRect(rrect(-150, -360, 70, 40, 30), lgrad(0, -360, 0, 40, ["#1C2030", "#0B0D16"]))
    # torso (back three-quarter)
    c.drawPath(P((-130, -300), (110, -320), (130, -40, "q", 150, -180), (-120, -30), (-130, -300, "q", -150, -170)),
               lgrad(-130, -320, 130, -30, [shirt, "#1A2236"]))
    c.drawPath(P((110, -318), (128, -60, "q", 150, -190), close=False), paint(rim, rim_a, stroke=6))
    # right arm forward to the desk
    c.drawPath(P((90, -280), (300, -150, "q", 200, -260), (300, -110), (80, -200, "q", 180, -170)), lgrad(90, -280, 300, -110, [shirt, "#222B44"]))
    c.drawOval(skia.Rect(290, -150, 345, -108), paint(skin))
    # neck + head (back of head, drooping forward with `tired`)
    droop = 26 * tired
    c.save(); c.translate(0, -330); c.rotate(14 * tired)
    c.drawRRect(rrect(-28, -50, 28, 10, 12), paint(skin))
    c.drawOval(skia.Rect(-70, -170 + droop * 0.2, 70, -20 + droop * 0.2), paint(skin))
    c.drawPath(P((-72, -90), (-60, -160, "q", -78, -140), (0, -186, "q", -36, -188), (64, -156, "q", 40, -186),
                 (74, -84, "q", 82, -130), (40, -50, "q", 66, -58), (-44, -48, "q", 0, -40), (-72, -90, "q", -70, -60)),
               lgrad(0, -186, 0, -48, ["#2A1E24", hair]))
    c.drawOval(skia.Rect(62, -110, 84, -66), paint(skin))
    c.drawPath(P((64, -150), (78, -86, "q", 84, -124), close=False), paint(rim, rim_a, stroke=5))
    c.restore()
    c.restore()


# ------------------------------------------------------------------ bedroom


def ceiling_fan(c, x, y, s, t, spin=0.0, color="#0A0C18", rim="#8FA6FF", rim_a=0.25):
    """Ceiling fan seen from below at an angle (blades as ellipses in perspective)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.drawLine(0, -200, 0, -30, paint(color, stroke=12))
    a0 = t * 360 * spin
    for k in range(3):
        a = math.radians(a0 + k * 120)
        bx, by = math.cos(a) * 190, math.sin(a) * 38
        pth = P((0, -10), (bx - math.sin(a) * 30, by - 6), (bx + math.cos(a) * 20, by + 4, "q", bx + math.cos(a) * 40, by), (0, 10))
        c.drawPath(pth, paint(color))
        c.drawPath(pth, paint(rim, rim_a, stroke=2))
    c.drawOval(skia.Rect(-44, -36, 44, 22), lgrad(0, -36, 0, 22, ["#2A2E44", color]))
    c.drawOval(skia.Rect(-44, -36, 44, 22), paint(rim, rim_a, stroke=2))
    c.restore()


def bedroom(c, x0, y0, w, h, t, clock_bedtime=None, ring=0.0, hand_reach=0.0, sky_p=0.0, made=False, phone_glow=0.0,
            calendar="30 DAYS"):
    """An Indian bedroom at 5 AM, drawn into the rect (x0, y0, w, h) (designed at 960 x 1080, scaled to fit).
    Window with grill + Delhi skyline, ceiling fan, bed with "you" under a blanket (hand reaching for the clock),
    wooden side table with the twin-bell clock (its bedtime sub-dial = clock_bedtime), charging phone, wall calendar.
    made=True: the bed is empty and made (Day 31 callback)."""
    c.save(); c.clipRect(skia.Rect(x0, y0, x0 + w, y0 + h)); c.translate(x0, y0); c.scale(w / 960, h / 1080)
    W, H = 960, 1080
    # wall
    c.drawRect(skia.Rect(0, 0, W, H), lgrad(0, 0, 0, H, ["#1A2147", "#121735", "#0C1026"], [0, 0.6, 1]))
    for k in range(40):   # plaster texture
        xx = noise_rng(k, 1) * W
        c.drawLine(xx, 0, xx + 6, 820, paint("#FFFFFF", 0.012, stroke=30 + 60 * noise_rng(k, 2)))
    # window
    wx0, wy0, wx1, wy1 = 470, 150, 880, 560
    c.save(); c.clipRect(skia.Rect(wx0, wy0, wx1, wy1))
    sunrise_sky(c, wx0, wy0, wx1, wy1 + 60, sky_p)
    light(c, 820, 210, 60, "#DDE6FF", 0.5 * (1 - sky_p))
    c.drawCircle(820, 210, 18, paint("#F2F4FF", 1 - sky_p))
    c.drawCircle(828, 204, 16, paint("#1A2650", 1 - sky_p))  # crescent
    c.drawRect(skia.Rect(wx0, wy1 - 200, wx1, wy1), lgrad(0, wy1 - 200, 0, wy1, [("#E08A50", 0), ("#E08A50", 0.35)]))
    delhi_rooftops(c, wx0, wx1, wy1 - 120, t, layer=2, color="#1E2448", lit=0.3, seed=3, rim="#F0A060", rim_a=0.35)
    delhi_rooftops(c, wx0, wx1, wy1 - 30, t, layer=1, color="#0A0E24", lit=0.5, seed=7)
    c.restore()
    # grill bars + frame
    for k in range(1, 8):
        xx = wx0 + k * (wx1 - wx0) / 8
        c.drawLine(xx, wy0, xx, wy1, paint("#05060E", stroke=6))
    for yy in (wy0 + 130, wy0 + 270):
        c.drawLine(wx0, yy, wx1, yy, paint("#05060E", stroke=6))
    c.drawRect(skia.Rect(wx0, wy0, wx1, wy1), paint("#2A2244", stroke=22))
    c.drawRect(skia.Rect(wx0 - 30, wy1 + 8, wx1 + 30, wy1 + 34), lgrad(0, wy1 + 8, 0, wy1 + 34, ["#3A3156", "#1A1530"]))
    # curtains (fabric folds)
    for cx0, cx1 in ((wx0 - 80, wx0 + 30), (wx1 - 30, wx1 + 70)):
        for k in range(5):
            xx = cx0 + k * (cx1 - cx0) / 5
            c.drawRect(skia.Rect(xx, wy0 - 40, xx + (cx1 - cx0) / 5 + 2, wy1 + 120),
                       lgrad(xx, 0, xx + (cx1 - cx0) / 5, 0, ["#5B2A3E", "#7A3A52", "#3A1828"]))
    c.drawLine(wx0 - 100, wy0 - 40, wx1 + 90, wy0 - 40, paint("#2A1A22", stroke=8))
    # moonlight beam across the room
    beam = P((wx0, wy0), (wx1, wy0), (wx1 - 340, H), (wx0 - 520, H))
    c.drawPath(beam, blurp("#9FB4FF" if sky_p < 0.5 else "#FFC890", 0.07, 30))
    # wall calendar
    if calendar:
        c.save(); c.translate(150, 230); c.rotate(-2)
        c.drawRect(skia.Rect(-70, -20, 70, 150), blurp("#000000", 0.4, 8))
        c.drawRect(skia.Rect(-74, -26, 74, 144), paint("#E9E2D2"))
        c.drawRect(skia.Rect(-74, -26, 74, 18), paint("#B8342E"))
        text(c, calendar.split()[0], 0, 92, font("extrabold", 62), paint("#2A2230"))
        text(c, " ".join(calendar.split()[1:]), 0, 128, font("bold", 22), paint("#5A5060"))
        c.drawCircle(0, -32, 5, paint("#888888"))
        c.restore()
    # floor
    c.drawRect(skia.Rect(0, 860, W, H), lgrad(0, 860, 0, H, ["#2A1E24", "#140E14"]))
    for k in range(7):
        c.drawLine(0, 880 + k * 30, W, 880 + k * 30, paint("#000000", 0.18, stroke=2))
    # ceiling fan (top, partly cropped)
    ceiling_fan(c, 330, 40, 1.15, t, spin=1.6)
    # ---- bed
    c.drawRRect(rrect(-80, 520, 120, 940, 26), lgrad(0, 520, 0, 940, ["#5A3A28", "#2E1C14"]))   # headboard
    c.drawRRect(rrect(-60, 545, 100, 900, 18), paint("#000000", 0.15))
    c.drawRect(skia.Rect(-40, 790, 640, 950), lgrad(0, 790, 0, 950, ["#3A2A22", "#1E140F"]))      # frame
    c.drawRRect(rrect(-40, 730, 620, 820, 26), lgrad(0, 730, 0, 820, ["#D9D2E8", "#9C94B4"]))     # mattress + sheet
    for k in range(8):   # bedsheet print
        c.drawCircle(40 + k * 75, 790, 9, paint("#6A5A9A", 0.4))
    # pillow
    c.drawPath(P((0, 680), (190, 676, "q", 100, 650), (200, 744, "q", 220, 710), (-6, 748, "q", 100, 760), (0, 680, "q", -18, 712)),
               lgrad(0, 650, 0, 760, ["#F2EEF8", "#B9B2CC"]))
    if not made:
        # the sleeper's head on the pillow: face turned away, cheek + ear showing, hair on top
        c.drawOval(skia.Rect(52, 676, 176, 752), blurp("#000000", 0.25, 8))
        c.drawOval(skia.Rect(60, 676, 172, 744), lgrad(60, 676, 172, 744, ["#C68A60", "#9A6440"]))
        c.drawOval(skia.Rect(118, 700, 140, 726), paint("#A86E48"))                      # ear
        c.drawPath(P((128, 712), (134, 706, "q", 134, 714), close=False), paint("#6E4228", stroke=2))
        c.drawPath(P((54, 712), (70, 672, "q", 48, 684), (150, 664, "q", 104, 652), (178, 700, "q", 182, 672),
                     (150, 700, "q", 168, 694), (114, 690, "q", 132, 684), (80, 712, "q", 96, 696), (54, 712, "q", 62, 722)),
                   lgrad(0, 652, 0, 720, ["#33242C", "#0E0A10"]))
        for k in range(7):
            c.drawPath(P((70 + k * 14, 670 + abs(k - 3) * 3), (64 + k * 16, 708, "q", 84 + k * 13, 686), close=False), paint("#FFFFFF", 0.07, stroke=2))
        c.drawPath(P((150, 664), (178, 700, "q", 182, 672), close=False), paint("#9FB4FF", 0.35, stroke=3))
        # blanket with a body shape under it
        c.drawPath(P((130, 712), (300, 690, "q", 210, 680), (470, 700, "q", 390, 670), (610, 735, "q", 560, 700),
                     (620, 820), (120, 830), (130, 712, "q", 100, 760)),
                   lgrad(0, 680, 0, 830, ["#3F6FB0", "#24467A", "#162C52"], [0, 0.5, 1]))
        for (a, b) in ((260, 700), (380, 690), (500, 712)):   # folds
            c.drawPath(P((a, b), (a + 50, 820, "q", a - 30, 770), close=False), paint("#0A1830", 0.35, stroke=7))
        c.drawPath(P((130, 712), (300, 690, "q", 210, 680), (470, 700, "q", 390, 670), close=False), paint("#9FC0FF", 0.25, stroke=4))
    else:
        c.drawPath(P((140, 744), (610, 738), (620, 820), (120, 830)), lgrad(0, 738, 0, 830, ["#3F6FB0", "#1E3A68"]))
        c.drawRRect(rrect(140, 736, 610, 760, 8), paint("#EDE8F6"))
    # ---- side table
    tx0, tx1, ty = 640, 900, 780
    c.drawRect(skia.Rect(tx0 + 10, ty, tx1 - 10, 990), lgrad(0, ty, 0, 990, ["#6B4630", "#2C1A10"]))
    c.drawRect(skia.Rect(tx0, ty - 18, tx1, ty + 8), lgrad(0, ty - 18, 0, ty + 8, ["#9A6A48", "#5A3A26"]))
    c.drawRect(skia.Rect(tx0 + 30, ty + 40, tx1 - 30, ty + 120), paint("#000000", 0.18))
    c.drawRect(skia.Rect(tx0 + 30, ty + 40, tx1 - 30, ty + 120), paint("#C8946A", 0.25, stroke=2))
    c.drawCircle((tx0 + tx1) / 2, ty + 80, 7, paint("#E2B07A"))
    # phone charging on the table
    c.save(); c.translate(712, ty - 16)
    c.drawRRect(rrect(-46, -4, 46, 6, 4), blurp("#000000", 0.5, 4))
    c.drawRRect(rrect(-44, -10, 44, 0, 5), lgrad(0, -10, 0, 0, ["#3A3A48", "#101016"]))
    c.drawLine(-38, -9, 38, -9, paint("#9FB4FF", 0.35, stroke=1.5))
    if phone_glow > 0:
        light(c, 0, -6, 70, "#7FD8FF", 0.4 * phone_glow)
    c.restore()
    c.drawPath(P((678, ty - 18), (650, ty - 6, "q", 660, ty - 20), (648, ty + 4, "q", 644, ty - 2), close=False), paint("#EDEDED", 0.8, stroke=3))
    # the clock
    alarm_clock(c, 820, ty - 132, 0.62, t, ring=ring, bedtime=clock_bedtime)
    # hand reaching out from under the blanket toward the clock
    if hand_reach > 0 and not made:
        hx = 560 + 150 * ease(hand_reach)
        c.drawPath(P((540, 740), (hx, 724, "q", 600, 718), (hx + 6, 752), (540, 770, "q", 600, 772)), lgrad(540, 720, hx, 760, ["#24467A", "#2F5A96"]))
        c.drawOval(skia.Rect(hx - 6, 720, hx + 46, 756), paint("#B9805A"))
        for k in range(3):
            c.drawLine(hx + 30, 726 + k * 9, hx + 54, 724 + k * 9, paint("#B9805A", stroke=8))
    # cool + warm light, vignette
    light(c, 820, ty - 132, 420, "#FFB45C", 0.18 * (1 + ring))
    c.drawRect(skia.Rect(0, 0, W, H), rgrad(W * 0.6, H * 0.55, 900, [("#000000", 0), ("#000000", 0.0), ("#000000", 0.6)], [0, 0.55, 1]))
    c.restore()
