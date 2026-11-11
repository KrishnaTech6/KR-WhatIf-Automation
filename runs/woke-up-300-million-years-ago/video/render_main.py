"""Main video: 1920x1080 frames (4 workers) + score/SFX/ambience + mix + mux + QA numbers."""
import os, sys, subprocess, json
import numpy as np, soundfile as sf
HERE = os.path.dirname(os.path.abspath(__file__)); RUN = os.path.dirname(HERE); FPS = 30
OUT = os.path.join(HERE, "out")


def frames(a, b, out):
    import skia, shots as S
    L = S.SHOTS()
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", "1920x1080", "-r", str(FPS),
                          "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", out + ".part.mp4"],
                         stdin=subprocess.PIPE)
    s = skia.Surface(1920, 1080)
    for i in range(a, b):
        c = s.getCanvas(); c.clear(skia.Color(0, 0, 0))
        S.render_frame(c, i / FPS, L)
        p.stdin.write(s.makeImageSnapshot().toarray(colorType=skia.kBGRA_8888_ColorType).tobytes())
    p.stdin.close(); p.wait(); os.rename(out + ".part.mp4", out)


def main():
    import mix as MX, cues
    from sfx import SR
    from timeline import TOTAL, B, E, MODE
    assert MODE == "real", "anchors.json missing: run anchors.py on main_edit.wav first"
    os.makedirs(OUT, exist_ok=True)
    total = TOTAL + 4.0                        # end card after the last word
    n = int(total * FPS); K = 4
    procs = [subprocess.Popen([sys.executable, __file__, "chunk", str(n * k // K), str(n * (k + 1) // K), f"{OUT}/main_{k}.mp4"])
             for k in range(K)]
    v, sr = sf.read(os.path.join(RUN, "audio", "final", "main_edit.wav"), dtype="float64")
    if v.ndim > 1: v = v.mean(1)
    if sr != SR:
        import scipy.signal as ss; v = ss.resample_poly(v, SR, sr)
    v = MX.voice_chain(v)
    m, f, a = cues.build()
    sections = [(0, E("hook"), -31), (E("hook"), E("hook") + 3.5, -24), (E("hook") + 3.5, B("minute"), -31),
                (B("minute"), B("night") - 1.5, -31), (B("night") - 1.5, B("night") + 0.3, None),
                (B("night") + 0.3, E("night"), -28), (E("night"), B("payoff"), -31), (B("payoff"), E("payoff"), -32),
                (E("payoff"), total, -25)]
    master, st = MX.master(v, m, f, a, sections, total, fade=1.8)
    sf.write(f"{OUT}/main.wav", master, SR)
    for p in procs: p.wait()
    with open(f"{OUT}/main_list.txt", "w") as fl:
        fl.write("".join(f"file 'main_{k}.mp4'\n" for k in range(K)))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/main_list.txt", "-i", f"{OUT}/main.wav",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", f"{OUT}/MAIN.mp4"], check=True)
    print("done", f"{OUT}/MAIN.mp4", round(total, 1))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "chunk":
        frames(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    else:
        main()
