#!/usr/bin/env python3
"""KR's What If Explained: one command for the video engine.

    python3 tools/wi.py setup                       install libs, cache ASR model + orchestra samples (once per machine)
    python3 tools/wi.py <slug> new                  scaffold runs/<slug>/video/ from tools/templates
    python3 tools/wi.py <slug> timeline             beat keys, aliases, spans (estimate or real)
    python3 tools/wi.py <slug> sheets               one still per shot, 9 per contact sheet -> video/sheets/shots_N.png
    python3 tools/wi.py <slug> sheet NAME t1 t2 ... contact sheet at chosen times
    python3 tools/wi.py <slug> vsheet short|reel t1 ...   vertical stills
    python3 tools/wi.py <slug> trim JOB [max_gap keep]    cap long silences -> audio/final/JOB_edit.wav
    python3 tools/wi.py <slug> anchors main|short|reel|all   transcribe + align -> video/anchors*.json
    python3 tools/wi.py <slug> preview T0 T1        quick render of T0..T1 s (voice only) -> video/out/PREVIEW.mp4
    python3 tools/wi.py <slug> render               full main video -> video/out/MAIN.mp4 (+ QA), if it fits in 10 min
    python3 tools/wi.py <slug> render 1/3 ... 3/3   render in parts (one Bash call each), then:
    python3 tools/wi.py <slug> render join          mix the audio, mux the parts -> MAIN.mp4 (+ QA)
    python3 tools/wi.py <slug> remix                rebuild the mix only and re-mux MAIN.mp4
    python3 tools/wi.py <slug> vertical short|reel  9:16 render -> video/out/SHORT.mp4 / REEL.mp4 (+ QA)
    python3 tools/wi.py <slug> vertical short 1/2 ... then `vertical short join`   same, in parts
    python3 tools/wi.py <slug> qa FILE [seconds]    loudness / true peak / black frames / length

KR_WORKERS sets the number of render processes (default: CPU count). Speed on a 2-CPU workspace: ~0.13 s per
frame for the main video (5 min ~ 20 min: use `render 1/3` .. `3/3`, then `render join`) and ~0.3 s per frame for
verticals (a 58 s Short ~ 9 min: use `vertical short 1/2`, `2/2`, then `vertical short join`).
"""
import os
import shutil
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)


def setup():
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages",
                    "skia-python", "sherpa-onnx", "pyloudnorm", "soundfile", "scipy", "numpy"], check=False)
    sys.path.insert(0, TOOLS)
    from krwi import assets
    assets.setup()


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__); return
    if argv[0] == "setup":
        setup(); return
    slug, cmd, args = argv[0], argv[1] if len(argv) > 1 else "timeline", argv[2:]
    run = os.path.join(REPO, "runs", slug)
    if cmd == "new":
        dst = os.path.join(run, "video")
        os.makedirs(dst, exist_ok=True)
        for f in os.listdir(os.path.join(TOOLS, "templates")):
            if not os.path.exists(os.path.join(dst, f)):
                shutil.copy(os.path.join(TOOLS, "templates", f), dst)
                print("created", os.path.join("runs", slug, "video", f))
        return
    if not os.path.isdir(run):
        raise SystemExit(f"no run folder {run}")
    os.environ["KR_RUN"] = run
    sys.path.insert(0, TOOLS)
    from krwi import ctx  # noqa: F401  (sets sys.path for brand/ and the run's video/)

    if cmd == "timeline":
        from krwi import timeline as tl
        print("mode", tl.MODE, " total", round(tl.TOTAL, 1), "s  hard cut before:", tl.HARD_CUT)
        for k in tl.BEAT_KEYS:
            al = sorted(a for a, v in tl.BEATS.alias.items() if v == k and a != k)
            print(f"  {k:12s} {tl.SPANS[k][0]:7.1f} - {tl.SPANS[k][1]:7.1f}  {tl.BEATS.moods[k]:9s} aliases: {', '.join(al)}")
    elif cmd == "sheets":
        from krwi import stills
        stills.auto()
    elif cmd == "sheet":
        from krwi import stills
        stills.sheet(args[0], [float(x) for x in args[1:]])
    elif cmd == "vsheet":
        from krwi import stills
        stills.sheet(f"{args[0]}_check", [float(x) for x in args[1:]], job=args[0])
    elif cmd == "trim":
        import soundfile as sf
        from krwi.trim import cap_silences
        job = args[0]
        mg, kp = (float(args[1]), float(args[2])) if len(args) > 2 else (0.7, 0.55)
        src = os.path.join(ctx.FINAL, f"{job}.wav")
        x, sr = sf.read(src, dtype="float32")
        if x.ndim > 1:
            x = x.mean(1)
        y, cuts = cap_silences(x, sr, mg, kp)
        sf.write(os.path.join(ctx.FINAL, f"{job}_edit.wav"), y, sr)
        print(f"{job}: {len(x) / sr:.2f} -> {len(y) / sr:.2f} s, {len(cuts)} cuts")
    elif cmd == "anchors":
        from krwi import asr
        for job in (["main", "short", "reel"] if args[0] == "all" else args):
            asr.run(job)
    elif cmd == "preview":
        from krwi import render
        render.main(start=float(args[0]), end=float(args[1]))
    elif cmd == "render":
        from krwi import render
        if not args:
            render.main()
        elif args[0] == "join":
            render.join()
        else:
            i, n = map(int, args[0].split("/"))
            render.part(i, n)
    elif cmd == "remix":
        from krwi import render
        render.audio_only()
    elif cmd == "vertical":
        from krwi import vertical
        if len(args) == 1:
            vertical.render(args[0])
        elif args[1] == "join":
            vertical.join(args[0])
        else:
            i, n = map(int, args[1].split("/"))
            vertical.part(args[0], i, n)
    elif cmd == "qa":
        from krwi.qa import check
        ok = check(args[0], float(args[1]) if len(args) > 1 else None)
        sys.exit(0 if ok else 1)
    else:
        raise SystemExit(f"unknown command {cmd!r}\n{__doc__}")


if __name__ == "__main__":
    main(sys.argv[1:])
