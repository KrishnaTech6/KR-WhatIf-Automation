"""Short + Reel plans (engine: krwi.vertical; render: python3 tools/wi.py <slug> vertical short|reel).
Each scene: scene(start_in_vertical, main_video_time, cx=960, zoom=1.15, rate=1.0) -> from `start` show the main
video from `main_video_time` on, centred on x=cx. vt.T("word") = time of that word in the Short/Reel."""
from krwi.vertical import scene
from krwi.timeline import T as MT, at as MAT, B as MB, E as ME  # noqa: F401  main-video times

HOOK = {"short": "HOOK TEXT", "reel": "HOOK TEXT"}       # frame-0 text, <= 6 words
SUB = {"short": "SUBLINE", "reel": "SUBLINE"}
FIX = {}                                                  # caption fixes: {"three": "3", "hundred": ""}
CAPTIONS = "standard"                                     # or "bold" (Style 2) only sometimes: brand/styles/README.md


def plan_short(vt):
    return [
        scene(0.0, 0.5),                                  # frame 0 = the hook visual
        # scene(vt.T("because"), MT("minute_one", "today"), cx=900, zoom=1.2),
    ]


def plan_reel(vt):
    return [
        scene(0.0, 0.5),
    ]
