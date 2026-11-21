"""Posting-time test: which time of day works best, measured on this channel (Krishna, 21 Nov 2026).

Every post goes out at a random time inside one of the active-hour windows (settings "time_test").
Each track is tested on its own:  yt_main = YouTube main video, yt_short = YouTube Shorts, ig = Instagram Reels.
The data lives on its own branch (settings time_test.data_branch, "time-test"), so every session branch and
every workflow sees the same calendar and the same numbers:

  time_test.json   "plan":    every planned post  {slug, kind, track, at (IST ISO), window}
                   "results": every post we measured {track, id, at, title, snaps: [[age_hours, views], ...]}
  time_test.md     the daily report (which window wins per track)

  python3 scripts/time_test.py youtube              # learn-youtube workflow, daily: views snapshot of recent uploads
  python3 scripts/time_test.py instagram FILE.json  # Instagram posting tasks: FILE = [{"id","at","views"}, ...]
                                                    #   (from vidiq_instagram_owner_insights; missing views = leave out)
  python3 scripts/time_test.py report               # print the report (also rebuilt on every update)

A window's score = median of (views at 48 h / that track's typical 48 h views), so a strong topic doesn't
make its time look good on its own; it needs several posts per window before it counts.
"""
import json
import os
import statistics
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACKS = {"yt_main": "YouTube main videos", "yt_short": "YouTube Shorts", "ig": "Instagram Reels"}


def settings():
    return json.load(open(os.path.join(ROOT, "settings.json")))


def cfg():
    return settings()["time_test"]


def parse(at):
    return datetime.fromisoformat(at.replace("Z", "+00:00"))


def windows():
    """[('19-22', 19*60, 22*60), ...] in IST minutes of the day."""
    out = []
    for w in cfg()["windows"]:
        a, b = (int(x) for x in w.split("-"))
        out.append((w, a * 60, b * 60))
    return out


def label(w):
    """'19-22' -> '7-10 PM', '22-24' -> '10 PM-12 AM'."""
    if w not in [n for n, _, _ in windows()]:
        return w
    a, b = (int(x) for x in w.split("-"))
    h = lambda x: f"{(x - 1) % 12 + 1}"
    ap = lambda x: "AM" if x % 24 < 12 else "PM"
    return f"{h(a)}-{h(b)} {ap(b)}" if ap(a) == ap(b) else f"{h(a)} {ap(a)}-{h(b)} {ap(b)}"


def window_of(dt):
    m = dt.astimezone(IST).hour * 60 + dt.astimezone(IST).minute
    for w, a, b in windows():
        if a <= m < b:
            return w
    return "other"


# ---------------------------------------------------------------- shared data on the time-test branch
def _git(*args, cwd=ROOT, check=True):
    return subprocess.run(["git", *args], cwd=cwd, check=check, capture_output=True, text=True).stdout


EMPTY = {"_help": "Posting-time test. Written by scripts/time_test.py and scripts/release_times.py; never edit by hand.",
         "plan": [], "results": []}


def load():
    """Latest data from origin/<data_branch> (empty if the branch doesn't exist yet)."""
    br = cfg()["data_branch"]
    _git("fetch", "-q", "origin", f"+refs/heads/{br}:refs/remotes/origin/{br}", check=False)
    raw = subprocess.run(["git", "show", f"origin/{br}:time_test.json"], cwd=ROOT, capture_output=True, text=True)
    return json.loads(raw.stdout) if raw.returncode == 0 else json.loads(json.dumps(EMPTY))


def update(change, msg, tries=4):
    """Apply change(data) on top of the newest branch state, rebuild the report, commit, push. Retries on races."""
    br = cfg()["data_branch"]
    for n in range(tries):
        data = load()
        change(data)
        with tempfile.TemporaryDirectory() as wt:
            exists = subprocess.run(["git", "rev-parse", "-q", "--verify", f"origin/{br}"], cwd=ROOT,
                                    capture_output=True).returncode == 0
            if exists:
                _git("worktree", "add", "-q", "--detach", wt, f"origin/{br}")
            else:
                _git("worktree", "add", "-q", "--detach", wt)
                _git("checkout", "-q", "--orphan", "tt-tmp", cwd=wt)
                _git("rm", "-rqf", ".", cwd=wt)
            try:
                json.dump(data, open(os.path.join(wt, "time_test.json"), "w"), indent=1, ensure_ascii=False)
                open(os.path.join(wt, "time_test.md"), "w").write(report(data))
                _git("add", "time_test.json", "time_test.md", cwd=wt)
                if not _git("status", "--porcelain", cwd=wt).strip():
                    return data
                _git("-c", "user.name=kr-autopilot", "-c", "user.email=actions@users.noreply.github.com",
                     "commit", "-qm", msg, cwd=wt)
                if subprocess.run(["git", "push", "-q", "origin", f"HEAD:refs/heads/{br}"], cwd=wt,
                                  capture_output=True).returncode == 0:
                    return data
            finally:
                _git("worktree", "remove", "--force", wt, check=False)
                _git("branch", "-D", "tt-tmp", check=False)
        print(f"push race, retry {n + 1}", file=sys.stderr)
    sys.exit("could not push time-test data")


# ---------------------------------------------------------------- scoring
def views_at(snaps, hours):
    """Views at `hours` of age, interpolated between snapshots. None if we can't tell yet."""
    s = sorted(snaps)
    before = [p for p in s if p[0] <= hours]
    after = [p for p in s if p[0] >= hours]
    if before and after:
        (a, va), (b, vb) = before[-1], after[0]
        return va if b == a else va + (vb - va) * (hours - a) / (b - a)
    if after and after[0][0] <= hours * 1.5:      # first look came a bit late: close enough
        return after[0][1]
    return None


def scored(data, track):
    """[(window, normalized score, raw views at H)] for the track's measured posts (newest 60)."""
    h = cfg()["score_at_hours"]
    rows = [(r, views_at(r["snaps"], h)) for r in data["results"] if r["track"] == track]
    rows = [(r, v) for r, v in rows if v is not None][-60:]
    if not rows:
        return []
    typical = statistics.median(v for _, v in rows) or 1
    return [(window_of(parse(r["at"])), v / typical, v) for r, v in rows]


def window_stats(data, track):
    """{window: {"planned": n, "measured": n, "score": median or None, "views": median raw}}"""
    st = {w: {"planned": 0, "measured": 0, "score": None, "views": None} for w, _, _ in windows()}
    for p in data["plan"]:
        if p["track"] == track and p["window"] in st:
            st[p["window"]]["planned"] += 1
    by = {}
    for w, s, v in scored(data, track):
        by.setdefault(w, []).append((s, v))
    for w, vals in by.items():
        if w in st:
            st[w].update(measured=len(vals), score=statistics.median(s for s, _ in vals),
                         views=statistics.median(v for _, v in vals))
    return st


def best_window(data, track):
    """Best-scoring window, only once every window has min_tests measured posts; else None (still exploring)."""
    st = window_stats(data, track)
    need = cfg()["min_tests"]
    if any(s["measured"] < need for s in st.values()):
        return None
    return max(st, key=lambda w: st[w]["score"])


# ---------------------------------------------------------------- report
def report(data):
    c = cfg()
    now = datetime.now(IST)
    L = [f"# Posting-time test (updated {now:%a %d %b %Y, %I:%M %p} IST)", "",
         f"Each post goes out at a random time inside one window. Score = median of (views at {c['score_at_hours']} h ÷ "
         f"that track's typical {c['score_at_hours']} h views); 1.00 = typical, 1.50 = 50% better. A window counts once "
         f"it has {c['min_tests']} measured posts; until every window has, posts are spread evenly (exploring). "
         f"After that {int(c['exploit_share'] * 100)}% of posts go to the best window and the rest keep testing the others.", ""]
    for t, name in TRACKS.items():
        st = window_stats(data, t)
        best = best_window(data, t)
        L += [f"## {name}", "", "| Window (IST) | Planned | Measured | Median views @%dh | Score |" % c["score_at_hours"],
              "| --- | --- | --- | --- | --- |"]
        top = max((s["score"] for s in st.values() if s["score"] is not None), default=None)
        for w, s in st.items():
            sc = "–" if s["score"] is None else f"{s['score']:.2f}" + (" ⭐" if s["score"] == top else "")
            vv = "–" if s["views"] is None else f"{s['views']:.0f}"
            L.append(f"| {label(w)} | {s['planned']} | {s['measured']} | {vv} | {sc} |")
        L += ["", f"Status: **best = {label(best)}**" if best else
              f"Status: exploring (needs {c['min_tests']} measured posts in every window).", ""]
    up = sorted((p for p in data["plan"] if parse(p["at"]) > now), key=lambda p: p["at"])
    if up:
        L += ["## Coming up", ""] + [f"- {parse(p['at']).astimezone(IST):%a %d %b %I:%M %p} · {TRACKS[p['track']]} · "
                                     f"{p['slug']} {p['kind']} ({label(p['window'])})" for p in up] + [""]
    return "\n".join(L)


# ---------------------------------------------------------------- snapshots
def add_snaps(data, track_of, items, now):
    """items: [{"id","at","views",("title")}]. Keeps one snapshot per post per ~12 h, for 10 days."""
    have = {(r["track"], r["id"]): r for r in data["results"]}
    for it in items:
        at = parse(it["at"])
        age = (now - at).total_seconds() / 3600
        if age < 1 or age > 240 or it.get("views") is None:
            continue
        tr = track_of(it)
        r = have.get((tr, it["id"]))
        if not r:
            r = {"track": tr, "id": it["id"], "at": at.astimezone(IST).isoformat(timespec="minutes"),
                 "window": window_of(at), "title": it.get("title", ""), "snaps": []}
            data["results"].append(r)
            have[(tr, it["id"])] = r
        if not r["snaps"] or age - r["snaps"][-1][0] >= 12:
            r["snaps"].append([round(age, 1), int(it["views"])])


def youtube_snapshot():
    yt = json.load(open(os.path.join(ROOT, "learn", "youtube.json")))
    now = parse(yt["fetched"])
    items = [dict(id=v["id"], at=v["published"], views=v["views"], title=v["title"], d=v["duration"]) for v in yt["videos"]]
    track = lambda it: "yt_short" if it["d"] <= 180 else "yt_main"
    update(lambda d: add_snaps(d, track, items, now), "time-test: YouTube snapshot")


def instagram_snapshot(path):
    items = json.load(open(path))
    update(lambda d: add_snaps(d, lambda it: "ig", items, datetime.now(timezone.utc)), "time-test: Instagram snapshot")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"
    if cmd == "youtube":
        youtube_snapshot()
    elif cmd == "instagram":
        instagram_snapshot(sys.argv[2])
    print(report(load()))
