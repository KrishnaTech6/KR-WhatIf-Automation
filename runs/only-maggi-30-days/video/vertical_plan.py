"""Short + Reel plans for 'What If You Ate Only Maggi for 30 Days?' (engine: krwi.vertical).
Each scene: scene(start_in_vertical, main_video_time, cx, zoom). vt.T("word") = time of that word in the Short/Reel.
Whole frame always (Krishna, 13 Nov: never crop the verticals). The Short loops: its last frame is its first frame."""
from krwi.vertical import scene
from krwi.timeline import T as MT, B as MB, E as ME  # noqa: F401  main-video times

HOOK = {"short": "7 PACKETS A DAY", "reel": "10 DAYS OF ONLY MAGGI"}
SUB = {"short": "ONLY MAGGI FOR 30 DAYS", "reel": "WHAT DIES INSIDE YOU"}
FIX = {"seven": "7", "ten": "10", "thirty": "30", "forty": "40", "percent": "%", "two": "2", "three": "3",
       "k": "KR'S", "r's": ""}
FULL = 1080 / 1920
CAPTIONS = "standard"   # EMI (two videos ago) used bold; this one stays standard


def plan_short(vt):
    w = vt.T
    F = dict(cx=960, zoom=FULL)
    return [
        scene(0.0, 0.4, **F),                                                   # frame 0: bowl + 3x salt
        scene(w("packets"), 3.0, **F),                                          # the pile grows, 210 packets
        scene(w("changes") - 0.4, MT("day_three", "puffy") - 0.6, **F),        # the puffy face in the mirror
        scene(w("feels") - 0.5, MT("day_one", "line") - 0.2, **F),             # day 1: the shelf like trophies
        scene(w("two"), MT("day_one", "two") - 0.3, **F),                      # 2 minutes a packet
        scene(w("around"), MT("day_one", "hundred") - 0.6, **F),               # Rs 100 vs a pizza
        scene(w("three") - 0.4, MB("day_three") - 0.5, **F),                   # DAY 3 card
        scene(w("puffy") - 0.6, MT("day_three", "face") - 0.1, **F),
        scene(w("rings"), MT("day_three", "slide") - 0.8, **F),                # ring stuck (iris close-up)
        scene(w("because"), MT("day_three", "packet") - 0.3, **F),             # 1 packet = 36% of the limit
        scene(w("three", 2) - 0.3, MT("day_three", "seven") - 0.3, **F),       # 7 pouches overflow the jar
        scene(w("holds") - 0.5, MT("day_three", "holds") + 0.2, **F),          # holding extra water
        scene(w("just"), MT("day_three", "two") - 0.3, **F),                   # drinking bottle after bottle
        scene(w("week"), MT("week_one", "twenty") - 0.2, **F),                 # bathroom, 20 min
        scene(w("there's"), MT("week_one", "fibre") - 0.4, **F),               # fibre: Maggi vs thali
        scene(w("ten") - 0.6, MT("day_ten", "inside") - 0.4, **F),             # iris into the gut
        scene(w("start"), MT("day_ten", "forty") - 0.4, **F),                  # before/after, -40%
        scene(w("they"), MT("day_ten", "fed") - 0.8, **F),                     # empty plates
        scene(w("stopped") - 0.2, MT("week_one", "isnt", 2) - 1.0, **F),       # what isn't in the packet
        scene(w("but"), MB("day_thirty") - 0.5, **F),                          # DAY 30 card
        scene(w("something"), MT("day_thirty", "zero") - 0.8, **F),            # vitamin C meter at 0
        scene(w("full") - 0.2, ME("day_twenty") + 0.4, **F),                   # silence: #210 ghosts in
        scene(w("because", 2), 0.0, rate=0.4 / max(0.1, vt.total - w("because", 2)), **F),  # loop -> frame 0
    ]


def plan_reel(vt):
    w = vt.T
    F = dict(cx=960, zoom=FULL)
    return [
        scene(0.0, MT("day_ten", "fed") - 0.2, **F),                           # frame 0: the gut city, empty plates
        scene(w("and") - 0.2, MT("day_thirty", "lost") - 0.3, **F),            # part of you starts dying
        scene(w("not"), MT("day_three", "cant") - 0.5, **F),                   # not your heart (x-ray)
        scene(w("not", 2), MT("day_twenty", "read") - 0.1, **F),               # not your brain (classroom)
        scene(w("gut") - 0.3, MT("day_ten", "inside") - 0.3, **F),             # iris into the gut
        scene(w("trillions"), MT("day_ten", "trillions") + 0.3, **F),
        scene(w("and", 2), MT("week_one", "fibre") - 0.2, **F),                # fibre: thali vs Maggi
        scene(w("dal"), MT("week_one", "isnt", 2) - 0.9, **F),                 # dal, veg, fruit: missing
        scene(w("maggi", 2), MT("day_ten", "fed") - 0.6, **F),                 # almost nothing
        scene(w("in"), MT("day_ten", "london") - 0.3, **F),                    # London
        scene(w("son"), MT("day_ten", "only") - 0.2, **F),                     # fast food, 10 days
        scene(w("when"), MT("day_ten", "forty") - 1.4, **F),                   # -40%
        scene(w("you", 2), MT("day_twenty", "full") - 0.3, **F),               # full, but empty gauge
        scene(w("they're"), MT("day_ten", "fed") + 0.4, **F),                  # starving
        scene(w("and", 3) - 0.2, MB("day_thirty") - 0.5, **F),                 # DAY 30 card
        scene(w("something"), MT("day_thirty", "zero") - 0.8, **F),
        scene(w("what's"), MT("payoff", "peas") - 0.4, **F),                   # add-ons drop in
        scene(w("full", 2), MT("payoff", "same") - 0.2, **F),                     # the bowl blooms
        scene(w("link"), 0.5, **F),                                            # the hero bowl
    ]
