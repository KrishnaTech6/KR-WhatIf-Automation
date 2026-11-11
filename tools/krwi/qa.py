"""Final-file QA: loudness -14 LUFS +-1, true peak <= -1 dBTP, no black frames over 0.5 s, length matches the audio.
Prints one PASS/FAIL line per check; returns True if all pass."""
import json
import re
import subprocess


def _ff(args):
    return subprocess.run(["ffmpeg", "-hide_banner", "-nostats"] + args, capture_output=True, text=True).stderr


def check(path, expected=None, tol=1.0):
    ok = True
    dur = float(json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", path],
                                          capture_output=True, text=True).stdout)["format"]["duration"])
    log = _ff(["-i", path, "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"])
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", log)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", log)[-1])
    blk = _ff(["-i", path, "-map", "0:v", "-vf", "blackdetect=d=0.5:pix_th=0.06", "-an", "-f", "null", "-"])
    blacks = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", blk)

    def line(name, good, msg):
        nonlocal ok
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'}  {name:12s} {msg}")

    print(f"QA {path}")
    line("loudness", abs(lufs + 14) <= 1.0, f"{lufs:.1f} LUFS (target -14 +-1)")
    line("true peak", tp <= -1.0, f"{tp:.1f} dBTP (max -1)")
    line("black", not blacks, "none over 0.5 s" if not blacks else ", ".join(f"{float(a):.1f}-{float(b):.1f}s" for a, b in blacks))
    if expected:
        line("length", abs(dur - expected) <= tol, f"{dur:.1f} s (expected {expected:.1f})")
    else:
        print(f"  info  length       {dur:.1f} s")
    return ok
