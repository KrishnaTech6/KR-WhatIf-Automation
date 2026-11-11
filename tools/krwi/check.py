"""One check for a video: `python3 tools/wi.py <slug> check [script|audio|shots|video|text|all]`.

Every rule that used to live only as an instruction is code here, so it runs the same way every time.
Each line is PASS, WARN (look at it, may be fine) or FAIL (fix before the next checkpoint). Exit code 1 on any FAIL.
Parts that have nothing to check yet (no audio, no render) are skipped with an INFO line.
"""
import json
import os
import re
import subprocess
import sys

from . import ctx

VENDOR = os.path.join(ctx.TOOLS, "vendor", "ig")
MOODS = {"soft", "neutral", "wonder", "deep", "tense", "dramatic", "warm", "playful", "deadpan"}
LENGTHS = {"3-4 min": (480, 580), "4-5 min": (620, 720), "8-10 min": (1250, 1500)}
VERTICAL_WORDS = {"short": (115, 145), "reel": (80, 105)}


class Report:
    def __init__(self):
        self.fails = self.warns = 0

    def head(self, name):
        print(f"\n{name}")

    def line(self, status, name, msg):
        if status == "FAIL":
            self.fails += 1
        elif status == "WARN":
            self.warns += 1
        print(f"  {status:4s}  {name:16s} {msg}")

    def ok(self, cond, name, msg, bad="FAIL"):
        self.line("PASS" if cond else bad, name, msg)


def _spoken_words(lines):
    return [w for l in lines for w in re.sub(r"\{\w+\}|\(pause\s+[\d.]+\)|\(beat\)", " ", l).split()]


def _est_seconds(lines, wpm):
    words = len(_spoken_words(lines))
    beats = sum(l.count("(beat)") for l in lines)
    pauses = sum(float(x) for l in lines for x in re.findall(r"\(pause\s+([\d.]+)\)", l))
    return words * 60 / wpm + beats + pauses


def _first_sentence(lines):
    txt = " ".join(_spoken_words(lines[:1]))
    m = re.match(r"(.+?[.?!])(\s|$)", txt)
    return (m.group(1) if m else txt).split()


def _run(tool, *args):
    r = subprocess.run([sys.executable, "-I", os.path.join(VENDOR, tool)] + list(args), capture_output=True, text=True)
    return r.stdout + r.stderr


# ---------------------------------------------------------------- script
def script(R):
    from .script import read, Beats
    R.head("SCRIPT (voice-full/short/reel.txt)")
    if not os.path.exists(os.path.join(ctx.SCRIPT, "voice-full.txt")):
        R.line("INFO", "script", "no voice-full.txt yet"); return
    bt = Beats("full")
    for job in ("full", "short", "reel"):
        p = os.path.join(ctx.SCRIPT, f"voice-{job}.txt")
        if not os.path.exists(p):
            R.line("FAIL", f"{job} script", f"missing voice-{job}.txt"); continue
        txt = open(p).read()
        _, beats = read(job)
        spoken = [l for b in beats for l in b["lines"]]
        digits = [l.strip() for l in spoken if re.search(r"\d", re.sub(r"\(pause\s+[\d.]+\)", "", l))]
        R.ok(not digits, f"{job} digits", "numbers spelled out" if not digits else f"digits left: {digits[0][:60]!r}")
        R.ok('"""' not in txt and "'''" not in txt, f"{job} quotes", 'no """ in the script')
        bad = sorted({b["mood"] for b in beats} - MOODS)
        R.ok(not bad, f"{job} moods", "only the 9 moods" if not bad else f"unknown mood(s): {', '.join(bad)}", "WARN")
    # main video
    _, beats = read("full")
    lines = [l for b in beats for l in b["lines"]]
    words = len(_spoken_words(lines))
    secs = _est_seconds(lines, 150) + 1.2 * (len(beats) - 1) + 1.2
    band = next((k for k, (a, b) in LENGTHS.items() if a * 0.9 <= words <= b * 1.1), None)
    R.ok(band is not None, "length", f"{words} words, ~{secs / 60:.1f} min" + (f" (fits {band})" if band else
         " (outside every length band +-10%)"), "WARN")
    hook = beats[0]
    hs = _est_seconds(hook["lines"], 150)
    R.line("PASS" if hs <= 15.0 else "WARN" if hs <= 17.0 else "FAIL", "hook length", f"~{hs:.1f} s estimated (max 15 s, then the logo sting)")
    first = _first_sentence(hook["lines"])
    R.ok(len(first) <= 8, "hook line 1", f"{len(first)} words: {' '.join(first)[:70]!r} (under 3 s)", "WARN")
    for h in ("KEY_BEATS", "HARD_CUT_BEFORE"):
        for w in [x.strip() for x in bt.headers.get(h, "").split(",") if x.strip()]:
            R.ok(w.lower() in bt.alias, h.lower(), f"{w!r} -> {bt.alias.get(w.lower(), 'matches no beat name')}")
    hc = bt.hard_cut
    if hc:
        pos = bt.keys.index(hc) / max(1, len(bt.keys) - 1)
        R.ok(0.45 <= pos <= 0.85, "hard cut place", f"before {hc} ({pos:.0%} through the beats; aim ~65-75% of runtime)", "WARN")
    else:
        R.line("WARN", "hard cut", "no HARD_CUT_BEFORE: the biggest escalation gets no silence before it")
    last = " ".join(beats[-1]["lines"]).lower()
    R.ok("next" in last and "what if" in last, "sign-off", "fixed sign-off with the next What If" if "next" in last and "what if" in last
         else "last beat has no 'Next time ... next What If' sign-off", "WARN")
    # verticals
    for job, (a, b) in VERTICAL_WORDS.items():
        if not os.path.exists(os.path.join(ctx.SCRIPT, f"voice-{job}.txt")):
            continue
        _, vb = read(job)
        vl = [l for x in vb for l in x["lines"]]
        n = len(_spoken_words(vl))
        R.ok(a <= n <= b, f"{job} words", f"{n} (target {a}-{b}), ~{_est_seconds(vl, 160):.0f} s", "WARN")
        f1 = _first_sentence(vl)
        R.ok(len(f1) <= 7, f"{job} line 1", f"{len(f1)} words: {' '.join(f1)[:60]!r} (under 2 s)", "WARN")
        hp = os.path.join(ctx.SCRIPT, f"hooks_{job}.txt")
        if os.path.exists(hp):
            scores = [float(x) for x in re.findall(r"^\s*([\d.]+)\s+(?:STRONG|OK|WEAK|SOLID|FAIR|POOR)", _run("hookscore.py", hp), re.M)]
            if scores:
                top = max(scores)
                R.line("PASS" if top >= 70 else "WARN" if top >= 50 else "FAIL", f"{job} hook score",
                       f"best {top:.0f} (>= 70 strong, under 50 never ships)")


# ---------------------------------------------------------------- audio
def audio(R):
    R.head("VOICE (audio/report.json + final wavs, gate A3)")
    rp = os.path.join(ctx.RUN, "audio", "report.json")
    if not os.path.exists(rp):
        R.line("INFO", "voice", "no audio/report.json yet"); return
    import numpy as np
    import soundfile as sf
    from .script import read
    rep = json.load(open(rp))
    for job, sj in (("main", "full"), ("short", "short"), ("reel", "reel")):
        j = rep.get(job)
        if not j:
            R.line("WARN" if job != "main" else "FAIL", job, "not in report.json"); continue
        ov = j.get("overall")
        if ov is None:
            R.line("WARN", f"{job} words", "no overall word match (redo-only report?)")
        else:
            R.ok(ov >= 97 if job == "main" else ov >= 95, f"{job} words", f"{ov:.1f}% of script words heard (main >= 97)",
                 "FAIL" if job == "main" else "WARN")
        for b in j.get("beats", []):
            for iss in b.get("issues", []):
                R.line("WARN", f"{job} beat {b['n']}", f"@{b['start']:.1f}s {b['name']}: said {iss.get('heard', '')[:50]!r} "
                       f"for {iss.get('text', '')[:50]!r} ({iss.get('why', '')})")
        wav = os.path.join(ctx.FINAL, f"{job}.wav")
        if os.path.exists(wav):
            x, sr = sf.read(wav, dtype="float32")
            pk = 20 * np.log10(max(1e-9, float(np.abs(x).max())))
            R.ok(pk <= -0.9, f"{job} peak", f"{pk:.1f} dBFS (max -1)")
            _, beats = read(sj)
            words = len(_spoken_words([l for b in beats for l in b["lines"]]))
            want = words / 150 * 60
            dur = len(x) / sr
            R.ok(abs(dur - want) <= 0.15 * want + 4 * len(beats) * 0.3, f"{job} length",
                 f"{dur:.1f} s for {words} words (~{want:.0f} s at 150 wpm + pauses)", "WARN")


# ---------------------------------------------------------------- shots + timing
def shots(R):
    R.head("SHOTS + TIMING (video/shots.py, anchors)")
    if not os.path.exists(os.path.join(ctx.VIDEO, "shots.py")):
        R.line("INFO", "shots", "no video/shots.py yet"); return
    from .timeline import MODE, E, B, TOTAL, BEAT_KEYS
    from .compose import check as cc
    import shots as S
    L = S.SHOTS()
    probs = cc(L)
    R.ok(not probs, "shot list", f"{len(L)} shots, order and transitions OK" if not probs else probs[0])
    R.ok(L[0][0] == 0, "cold open", "first shot at 0.0 s (frame 0 = the hook's consequence)")
    hook_end = E(BEAT_KEYS[0])
    logo = [st for st, fn, tr in L if getattr(fn, "kind", None) == "logo" or "logo" in getattr(fn, "__name__", "")]
    if not logo:
        R.line("FAIL", "logo sting", "no logo sting shot")
    else:
        right_after = abs(logo[0] - hook_end) <= 0.8
        R.line("FAIL" if not right_after or logo[0] > 17.5 else "WARN" if logo[0] > 16.0 else "PASS", "logo sting",
               f"at {logo[0]:.1f} s, hook ends {hook_end:.1f} s (right after the hook, by 0:16)")
    cards = [st for st, fn, tr in L if getattr(fn, "kind", None) == "card" or getattr(fn, "__name__", "") == "f"]
    R.ok(len(cards) >= 3, "chapter cards", f"{len(cards)} (every chapter gets one)", "WARN")
    long = [(i, L[i + 1][0] - st) for i, (st, fn, tr) in enumerate(L[:-1]) if L[i + 1][0] - st > 8.0]
    R.ok(not long, "shot length", "no shot over 8 s" if not long else
         f"{len(long)} shot(s) over 8 s, e.g. #{long[0][0]} {getattr(L[long[0][0]][1], '__name__', '')} {long[0][1]:.1f} s "
         "(needs a change inside at least every 3 s)", "WARN")
    R.ok(L[-1][0] >= TOTAL - 1.0, "end card", f"last shot at {L[-1][0]:.1f} s, voice ends {TOTAL:.1f} s", "WARN")
    R.line("INFO" if MODE == "estimate" else "PASS", "timing", f"{MODE} mode")
    for job, f, lim in (("main", "anchors.json", 0.90), ("short", "anchors_short.json", 0.85), ("reel", "anchors_reel.json", 0.85)):
        p = os.path.join(ctx.VIDEO, f)
        if os.path.exists(p):
            m = json.load(open(p)).get("match", 0)
            R.ok(m >= lim, f"{job} anchors", f"{m:.1%} of script words found in the audio (min {lim:.0%})",
                 "WARN" if m >= lim - 0.1 else "FAIL")


# ---------------------------------------------------------------- rendered files
def video(R):
    from .qa import check as qa
    R.head("RENDERED FILES (video/out)")
    found = False
    for job, name in (("main", "MAIN.mp4"), ("short", "SHORT.mp4"), ("reel", "REEL.mp4")):
        p = os.path.join(ctx.OUT, name)
        if not os.path.exists(p):
            continue
        found = True
        if job == "main":
            from .timeline import TOTAL
            exp = TOTAL + 4.0
        else:
            ap = os.path.join(ctx.VIDEO, f"anchors_{job}.json")
            exp = json.load(open(ap))["total"] if os.path.exists(ap) else None
        ok = qa(p, exp)
        R.ok(ok, name, "all QA lines pass" if ok else "QA failed (see above)")
    thumbs = os.path.join(ctx.VIDEO, "thumbs")
    for f in sorted(os.listdir(thumbs)) if os.path.isdir(thumbs) else []:
        if f.startswith("THUMB") and f.endswith(".jpg"):
            import skia
            im = skia.Image.open(os.path.join(thumbs, f))
            size = os.path.getsize(os.path.join(thumbs, f))
            R.ok((im.width(), im.height()) == (1280, 720) and size < 2_000_000, f, f"{im.width()}x{im.height()}, {size // 1024} KB "
                 "(1280x720, under 2 MB)")
            found = True
    if not found:
        R.line("INFO", "files", "nothing rendered yet")


# ---------------------------------------------------------------- captions + upload text
def text(R):
    R.head("TEXT (Instagram captions, upload.json)")
    any_ = False
    for job in ("reel", "short"):
        p = next((os.path.join(ctx.SCRIPT, n) for n in (f"caption_{job}.clean.txt", f"caption_{job}.txt")
                  if os.path.exists(os.path.join(ctx.SCRIPT, n))), None)
        if not p:
            continue
        any_ = True
        out = _run("caption.py", p)
        for st, name, msg in re.findall(r"^\s*(PASS|WARN|FAIL)\s+([A-Z][A-Z ]+?)\s{2,}(.+)$", out, re.M):
            if st != "PASS" or name.strip() in ("FIRST LINE", "ONE ASK", "HASHTAGS"):
                R.line(st, f"{job} {name.strip().lower()}"[:16], msg.strip())
        body = "\n".join(l for l in open(p).read().splitlines() if not l.strip().startswith("#"))
        tmp = p + ".nohash.tmp"
        open(tmp, "w").write(body)
        m = re.search(r"HUMAN SCORE.*?([\d.]+)\s+(PASS|REVIEW|FLAGGED)", _run("detect.py", tmp))
        os.remove(tmp)
        if m:
            sc, lab = float(m.group(1)), m.group(2)
            R.line({"PASS": "PASS", "REVIEW": "WARN", "FLAGGED": "FAIL"}[lab], f"{job} human score",
                   f"{sc:.0f} {lab} (caption without hashtags; FLAGGED never ships)")
    up = os.path.join(ctx.RUN, "publish", "upload.json")
    if os.path.exists(up):
        any_ = True
        u = json.load(open(up))
        t = u["main"]["title"]
        R.ok(len(t) <= 60, "main title", f"{len(t)} chars: {t!r} (max 60)", "WARN")
        stamps = re.findall(r"^(\d{1,2}:\d{2})\s", u["main"]["description"], re.M)
        R.ok(len(stamps) >= 3 and stamps[0] in ("0:00", "00:00"), "chapters", f"{len(stamps)} timestamps, first {stamps[0] if stamps else '-'} "
             "(YouTube needs 0:00 first and at least 3)")
        for i, s in enumerate(u.get("shorts", [])):
            R.ok("{MAIN_URL}" in s["description"], f"short {i + 1} link", "description links the main video ({MAIN_URL})", "WARN")
            R.ok(len(s["title"]) <= 60, f"short {i + 1} title", f"{len(s['title'])} chars (max 60)", "WARN")
    if not any_:
        R.line("INFO", "text", "no captions or upload.json yet")


PARTS = {"script": script, "audio": audio, "shots": shots, "video": video, "text": text}


def run(which="all"):
    R = Report()
    print(f"CHECK {os.path.basename(ctx.RUN)}")
    for name, fn in PARTS.items():
        if which in ("all", name):
            try:
                fn(R)
            except Exception as e:                       # a broken part is a FAIL, the rest still runs
                R.line("FAIL", name, f"check crashed: {type(e).__name__}: {e}")
    print(f"\n{'FAIL' if R.fails else 'PASS'}: {R.fails} fail, {R.warns} warn")
    return R.fails == 0
