"""Main video render: 1920x1080 frames in parallel worker processes piped to ffmpeg, score + SFX + ambience,
mix to -14 LUFS, mux. Output: video/out/MAIN.mp4, then the QA check."""
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

from . import ctx

TOOLS = ctx.TOOLS


def _ffmpeg_pipe(w, h, out):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{w}x{h}", "-r", str(ctx.FPS),
                             "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", out + ".part.mp4"],
                            stdin=subprocess.PIPE)


def frames(a, b, out):
    import skia
    import shots as S
    from .compose import render_frame
    L = S.SHOTS()
    p = _ffmpeg_pipe(ctx.W, ctx.H, out)
    s = skia.Surface(ctx.W, ctx.H)
    for i in range(a, b):
        c = s.getCanvas(); c.clear(skia.Color(0, 0, 0))
        render_frame(c, i / ctx.FPS, L)
        p.stdin.write(s.makeImageSnapshot().toarray(colorType=skia.kBGRA_8888_ColorType).tobytes())
    p.stdin.close(); p.wait(); os.rename(out + ".part.mp4", out)


def spawn(args):
    env = dict(os.environ, KR_RUN=ctx.RUN, PYTHONPATH=TOOLS + os.pathsep + os.environ.get("PYTHONPATH", ""))
    return subprocess.Popen([sys.executable, "-m"] + args, env=env)


def voice(job):
    from . import mix as MX
    from .sfx import SR
    v, sr = sf.read(ctx.voice_wav(job), dtype="float64")
    if v.ndim > 1:
        v = v.mean(1)
    if sr != SR:
        import scipy.signal as ss
        v = ss.resample_poly(v, SR, sr)
    return MX.voice_chain(v)


def concat(parts, wav, out):
    lst = out + ".list.txt"
    with open(lst, "w") as fl:
        fl.write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", out], check=True)
    os.remove(lst)


def main(workers=None, start=None, end=None):
    """Full render. start/end (seconds) render only that part, silent voice-only preview: out/preview.mp4."""
    from . import mix as MX, cues
    from .sfx import SR
    from .timeline import TOTAL, MODE
    import shots as S
    from .compose import check
    os.makedirs(ctx.OUT, exist_ok=True)
    L = S.SHOTS()
    bad = check(L)
    if bad:
        raise SystemExit("shot list problems:\n  " + "\n  ".join(bad))
    K = workers or int(os.environ.get("KR_WORKERS", os.cpu_count() or 2))
    total = TOTAL + 4.0                                   # end card after the last word
    a0, a1 = int((start or 0) * ctx.FPS), int((end or total) * ctx.FPS)
    preview = start is not None or end is not None
    if not preview:
        assert MODE == "real", "anchors.json missing: run `wi.py <slug> anchors main` first"
    n = a1 - a0
    tag = "preview" if preview else "main"
    parts = [f"{ctx.OUT}/{tag}_{k}.mp4" for k in range(K)]
    procs = [spawn(["krwi.render", "chunk", str(a0 + n * k // K), str(a0 + n * (k + 1) // K), parts[k]]) for k in range(K)]
    if preview:
        v = voice("main") if MODE == "real" else np.zeros(int(total * SR))
        seg = v[int(a0 / ctx.FPS * SR):int(a1 / ctx.FPS * SR)]
        sf.write(f"{ctx.OUT}/preview.wav", seg.astype(np.float32), SR)
        for p in procs:
            p.wait()
        concat(parts, f"{ctx.OUT}/preview.wav", f"{ctx.OUT}/PREVIEW.mp4")
        print("preview", f"{ctx.OUT}/PREVIEW.mp4")
        return
    v = voice("main")
    m, f, a = cues.build(L)
    master, _ = MX.master(v, m, f, a, cues.sections(total), total, fade=1.8)
    sf.write(f"{ctx.OUT}/main.wav", master, SR)
    for p in procs:
        p.wait()
    if any(p.returncode for p in procs):
        raise SystemExit("a frame worker failed")
    concat(parts, f"{ctx.OUT}/main.wav", f"{ctx.OUT}/MAIN.mp4")
    for p in parts:
        os.remove(p)
    print("done", f"{ctx.OUT}/MAIN.mp4", round(total, 1), "s")
    from .qa import check as qa
    qa(f"{ctx.OUT}/MAIN.mp4", total)


def part(i, n, workers=None):
    """Render part i of n (1-based) of the main video's frames into out/part_<i>of<n>.mp4 (no audio).
    Each part should finish inside one 10-minute Bash call; then `join` mixes the audio and muxes."""
    from .timeline import TOTAL, MODE
    assert MODE == "real", "anchors.json missing: run `wi.py <slug> anchors main` first"
    os.makedirs(ctx.OUT, exist_ok=True)
    nf = int((TOTAL + 4.0) * ctx.FPS)
    a0, a1 = nf * (i - 1) // n, nf * i // n
    K = workers or int(os.environ.get("KR_WORKERS", os.cpu_count() or 2))
    subs = [f"{ctx.OUT}/part_{i}of{n}_{k}.mp4" for k in range(K)]
    procs = [spawn(["krwi.render", "chunk", str(a0 + (a1 - a0) * k // K), str(a0 + (a1 - a0) * (k + 1) // K), subs[k]])
             for k in range(K)]
    for p in procs:
        p.wait()
    if any(p.returncode for p in procs):
        raise SystemExit("a frame worker failed")
    lst = f"{ctx.OUT}/part_{i}of{n}.txt"
    open(lst, "w").write("".join(f"file '{os.path.abspath(x)}'\n" for x in subs))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                    f"{ctx.OUT}/part_{i}of{n}.mp4"], check=True)
    for x in subs + [lst]:
        os.remove(x)
    print(f"part {i}/{n}: frames {a0}-{a1} -> out/part_{i}of{n}.mp4")


def join():
    """After all `part i/n` calls: mix the audio and mux the parts into out/MAIN.mp4, then QA."""
    import glob
    import re
    from . import mix as MX, cues
    from .sfx import SR
    from .timeline import TOTAL
    import shots as S
    parts = glob.glob(f"{ctx.OUT}/part_*of*.mp4")
    if not parts:
        raise SystemExit("no out/part_*of*.mp4 files: run `render 1/N` ... `render N/N` first")
    ns = {int(re.search(r"of(\d+)", x).group(1)) for x in parts}
    if len(ns) != 1:
        raise SystemExit(f"parts from different splits {sorted(ns)}: delete out/part_* and render again")
    n = ns.pop()
    have = sorted(int(re.search(r"part_(\d+)of", x).group(1)) for x in parts)
    if have != list(range(1, n + 1)):
        raise SystemExit(f"missing parts: {sorted(set(range(1, n + 1)) - set(have))}")
    total = TOTAL + 4.0
    m, f, a = cues.build(S.SHOTS())
    master, _ = MX.master(voice("main"), m, f, a, cues.sections(total), total, fade=1.8)
    sf.write(f"{ctx.OUT}/main.wav", master, SR)
    concat([f"{ctx.OUT}/part_{i}of{n}.mp4" for i in range(1, n + 1)], f"{ctx.OUT}/main.wav", f"{ctx.OUT}/MAIN.mp4")
    for i in range(1, n + 1):
        os.remove(f"{ctx.OUT}/part_{i}of{n}.mp4")
    print("done", f"{ctx.OUT}/MAIN.mp4", round(total, 1), "s")
    from .qa import check as qa
    qa(f"{ctx.OUT}/MAIN.mp4", total)


def audio_only():
    """Rebuild only the mix (after an audio fix) and re-mux onto the existing MAIN.mp4 video."""
    from . import mix as MX, cues
    from .sfx import SR
    from .timeline import TOTAL
    import shots as S
    total = TOTAL + 4.0
    m, f, a = cues.build(S.SHOTS())
    master, _ = MX.master(voice("main"), m, f, a, cues.sections(total), total, fade=1.8)
    sf.write(f"{ctx.OUT}/main.wav", master, SR)
    src = f"{ctx.OUT}/MAIN.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", f"{ctx.OUT}/main.wav", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", src + ".tmp.mp4"], check=True)
    os.replace(src + ".tmp.mp4", src)
    print("remuxed", src)


if __name__ == "__main__":
    if sys.argv[1] == "chunk":
        frames(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
