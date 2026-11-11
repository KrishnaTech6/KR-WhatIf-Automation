"""Downloads cached once per machine in ~/.cache/kr-whatif (KR_CACHE): the ASR model and the FluidR3 orchestra samples.
Both come from GitHub (reachable from the workspace). Safe to call every time: it skips what's already there."""
import base64
import json
import os
import re
import subprocess
import urllib.request

import numpy as np

from . import ctx

ASR_NAME = "sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8"
ASR_URL = f"https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/{ASR_NAME}.tar.bz2"
SF_URL = "https://raw.githubusercontent.com/gleitz/midi-js-soundfonts/gh-pages/FluidR3_GM/{}-mp3.js"
INSTRUMENTS = ["acoustic_grand_piano", "string_ensemble_1", "choir_aahs", "celesta", "pizzicato_strings",
               "orchestral_harp", "pad_2_warm", "timpani", "taiko_drum", "cello", "contrabass", "french_horn",
               "music_box", "marimba", "glockenspiel", "synth_strings_1"]
SR = 48000


def asr_dir():
    d = os.path.join(ctx.CACHE, "asr", ASR_NAME)
    if not os.path.exists(os.path.join(d, "tokens.txt")):
        os.makedirs(os.path.dirname(d), exist_ok=True)
        print("downloading ASR model (~460 MB, once)...", flush=True)
        subprocess.run(f"curl -sSL {ASR_URL} | tar xj -C {os.path.dirname(d)}", shell=True, check=True)
    return d


def sf_dir():
    return os.path.join(ctx.CACHE, "sf")


def soundfont(inst):
    """FluidR3 instrument -> cached .npz of 48 kHz mono float32 notes keyed 'D4', 'Bb3', ..."""
    path = os.path.join(sf_dir(), inst + ".npz")
    if os.path.exists(path):
        return path
    os.makedirs(sf_dir(), exist_ok=True)
    js = urllib.request.urlopen(SF_URL.format(inst), timeout=120).read().decode()
    notes = dict(re.findall(r'"([A-G]b?\d)":\s*"data:audio/mp3;base64,([^"]+)"', js))
    out = {}
    for name, b64 in notes.items():
        pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", "pipe:0", "-f", "f32le", "-ac", "1", "-ar", str(SR), "pipe:1"],
                             input=base64.b64decode(b64), capture_output=True, check=True).stdout
        out[name] = np.frombuffer(pcm, np.float32)
    np.savez(path, **out)
    return path


def setup(instruments=INSTRUMENTS, asr=True):
    for i in instruments:
        soundfont(i)
    print("samples ok:", len(instruments), "instruments in", sf_dir())
    if asr:
        print("asr ok:", asr_dir())
