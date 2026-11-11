"""Render a vertical job: frames (2 workers, ffmpeg pipe) + score/SFX + mix + mux."""
import os, sys, subprocess, json
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.dirname(HERE)
FPS = 30


def frames(job, a, b, out):
    import skia, vertical as V
    vt = V.VT(job); plan = (V.plan_short if job == "short" else V.plan_reel)(vt)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", "1080x1920", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", out + ".part.mp4"],
                         stdin=subprocess.PIPE)
    s = skia.Surface(1080, 1920)
    for i in range(a, b):
        c = s.getCanvas(); c.clear(skia.Color(0, 0, 0))
        V.frame(c, job, vt, plan, i / FPS)
        p.stdin.write(s.makeImageSnapshot().toarray(colorType=skia.kBGRA_8888_ColorType).tobytes())
    p.stdin.close(); p.wait()
    os.rename(out + ".part.mp4", out)


def audio(job, total):
    import sfx as X, music as Mu, vertical as V
    vt = V.VT(job); plan = (V.plan_short if job == "short" else V.plan_reel)(vt)
    mus, fx = Mu.Track(total + 2), Mu.Track(total + 2)
    if job == "short":
        Mu.pulse(mus, 0, total - 0.3, "D2", "contrabass", 104, 0.55)
        Mu.pad(mus, 0, total, ["Dm", "Bb", "Gm", "A"], "string_ensemble_1", 0.3, 4)
        Mu.arp(mus, 0, total - 0.3, ["Dm", "Bb", "Gm", "A"], "pizzicato_strings", 104, 0.4)
        for k in range(int(total / 4.6)):
            mus.add(k * 4.6, Mu.note("timpani", "D2", 1.2, 0.6), 0.35)
        fx.add(0.0, X.buzz(1.5), 0.6)
        fx.add(vt.T("strike") - 0.05, X.thunder(32), 0.9)
        fx.add(vt.T("one") , X.impact(33, 0.9), 0.6)
        fx.add(vt.T("bed"), X.impact(14, 0.4), 0.5)
        fx.add(vt.T("look"), X.skitter(2.0, 1), 0.5)
        fx.add(total - 2.0, X.riser(2.0, 70), 0.45)             # riser lands on the loop point (frame 0)
    else:
        Mu.pad(mus, 0, total, ["Dm", "Bb", "F", "C"], "synth_strings_1", 0.35, 4)
        Mu.arp(mus, 0, total - 0.3, ["Dm", "Bb", "F", "C"], "celesta", 84, 0.35, 1)
        Mu.pad(mus, vt.T("meanwhile"), vt.T("later"), ["F", "C"], "choir_aahs", 0.3, 4)
        fx.add(0.0, X.impact(60, 0.7), 0.5)
        fx.add(vt.T("crashing") if any(w.lower().startswith("crashing") for _, w in vt.words) else 5, X.impact(61, 0.8), 0.5)
        fx.add(vt.T("odisha") if any("odisha" in w.lower() for _, w in vt.words) else 13, X.pop(700), 0.5)
        fx.add(total - 2.0, X.riser(2.0, 71), 0.4)
    for st, *_ in plan[1:]:
        fx.add(st - 0.12, X.whoosh(0.4, int(st * 10)), 0.25)
    return mus.buf, fx.buf


def main(job):
    import mix as MX
    from sfx import SR
    vt_words = json.load(open(os.path.join(HERE, f"anchors_{job}.json")))
    total = vt_words["total"]
    out = os.path.join(HERE, "out"); os.makedirs(out, exist_ok=True)
    n = int(total * FPS)
    K = 4
    bounds = [(n * k // K, n * (k + 1) // K) for k in range(K)]
    procs = [subprocess.Popen([sys.executable, __file__, "chunk", job, str(a), str(b), f"{out}/{job}_{k}.mp4"])
             for k, (a, b) in enumerate(bounds)]
    # audio while frames render
    wav = os.path.join(RUN, "audio", "final", f"{job}_edit.wav")
    v, sr = sf.read(wav, dtype="float64")
    if v.ndim > 1: v = v.mean(1)
    if sr != SR:
        import scipy.signal as ss; v = ss.resample_poly(v, SR, sr)
    v = MX.voice_chain(v)
    m, f = audio(job, total)
    sections = [(0, total + 2, -29.0)]
    master, stems = MX.master(v, m, f, np.zeros(10), sections, total, fade=0.05 if job == "short" else 1.0)
    sf.write(f"{out}/{job}.wav", master, SR)
    for p in procs: p.wait()
    with open(f"{out}/{job}_list.txt", "w") as fl:
        fl.write("".join(f"file '{job}_{k}.mp4'\n" for k in range(K)))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{out}/{job}_list.txt", "-i", f"{out}/{job}.wav",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest",
                    f"{out}/{job.upper()}.mp4"], check=True)
    print("done", f"{out}/{job.upper()}.mp4")


if __name__ == "__main__":
    if sys.argv[1] == "chunk":
        frames(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
    else:
        main(sys.argv[1])
