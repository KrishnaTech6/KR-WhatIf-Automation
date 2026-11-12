"""Render the style reference sheets from brand/styles/demo (same shots in every style).

    python3 brand/render_styles.py          -> brand/styles/atlas.jpg, cinematic.jpg, collage.jpg, bold_captions.jpg
Look at these before drawing a video in a style; they are the approved look of each one (Nov 2026).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DEMO = os.path.join(HERE, "styles", "demo")
TIMES = ["0.3", "2.2", "4.5", "6.6", "9.8", "12.6", "14.6", "17.6", "5.5"]

CODE = """
import sys, os, skia
sys.path.insert(0, {tools!r})
from krwi import ctx, stills
if {vert}:
    p = stills.sheet("v", [0.4, 4.6, 9.0, 12.5], job="short")
else:
    p = stills.sheet("m", [float(x) for x in {times!r}])
skia.Image.open(p).save({out!r}, skia.kJPEG, 82)
"""

for style, vert, name in (("atlas", False, "atlas"), ("cinematic", False, "cinematic"), ("collage", False, "collage"),
                          ("collage", True, "bold_captions")):
    env = dict(os.environ, KR_RUN=DEMO, KR_STYLE=style)
    out = os.path.join(HERE, "styles", name + ".jpg")
    code = CODE.format(tools=os.path.join(REPO, "tools"), vert=vert, times=TIMES, out=out)
    subprocess.run([sys.executable, "-c", code], env=env, check=True)
    print("wrote", os.path.relpath(out, REPO))
