"""Where things are. The CLI (tools/wi.py) sets KR_RUN to runs/<slug>; every module reads it from here."""
import os
import sys

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(TOOLS)
BRAND = os.path.join(REPO, "brand")
CACHE = os.path.expanduser(os.environ.get("KR_CACHE", "~/.cache/kr-whatif"))
RUN = os.path.abspath(os.environ.get("KR_RUN", os.getcwd()))
VIDEO = os.path.join(RUN, "video")
SCRIPT = os.path.join(RUN, "script")
FINAL = os.path.join(RUN, "audio", "final")
OUT = os.path.join(VIDEO, "out")
FPS = 30
W, H = 1920, 1080          # main video
VW, VH = 1080, 1920        # Short / Reel

for p in (BRAND, VIDEO):   # brand modules (primitives, kr, logo) and the run's own modules (shots, art, cues, ...)
    if p not in sys.path:
        sys.path.insert(0, p)


def voice_wav(job):
    """The voice file for a job: the silence-trimmed <job>_edit.wav if it exists, else <job>.wav."""
    for name in (f"{job}_edit.wav", f"{job}.wav"):
        p = os.path.join(FINAL, name)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"no {job}.wav in {FINAL} (download the voiceover first)")


def run_module(name):
    """Import an optional module from the run's video/ folder (None if it doesn't exist)."""
    if not os.path.exists(os.path.join(VIDEO, name + ".py")):
        return None
    import importlib
    return importlib.import_module(name)
