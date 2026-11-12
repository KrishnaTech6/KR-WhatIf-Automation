from krwi.vertical import scene

HOOK = {"short": "THE SUN IS GONE", "reel": "THE SUN IS GONE"}
SUB = {"short": "AND NOBODY KNOWS YET", "reel": "AND NOBODY KNOWS YET"}
FIX = {"k": "", "r's": "KR's"}
CAPTIONS = "bold"


def plan_short(vt):
    return [scene(0.0, 2.6), scene(vt.T("sunlight"), 6.4), scene(vt.T("then"), 14.3)]


def plan_reel(vt):
    return plan_short(vt)
