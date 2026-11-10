"""Chatterbox voiceover generator for KR's What If Explained (runs headless on a Kaggle GPU).

Modes
  python gen.py job.json              generate every beat (GPU), then assemble the final WAVs
  python gen.py job.json --assemble   only rebuild the final WAVs from parts/ (CPU, no torch)

job.json keys
  title, lang ("en" | "hi" | ...), tries (int)
  jobs     [{name, kind ("main"|"short"), script (beat format), strict [..], hard_cut_before [..]}]
  lexicon  {"bhopal": ["Bho-paal", "Bhopaal"], ...}   respellings tried in order; captions never see them
  refs     {mood: wav path}  voice samples, already 24 kHz mono
  only     {"main": [5, 7]}  optional: generate only these beats (a redo run)
  parts    dir for per-beat WAV + JSON     final  dir for <job>.wav     report  path of report.json

Every sentence chunk is checked right after it is spoken (Whisper words, speed, stuck silence) and
regenerated until it passes. A chunk that holds a lexicon word and still fails also tries that
word's other respellings. What never passes is listed in the report for Claude to fix.
"""
import json, os, re, sys, glob, subprocess, tempfile, hashlib, random
import numpy as np, soundfile as sf

PRESETS = {
    "soft":       dict(exaggeration=0.35, cfg_weight=0.50, temperature=0.70, speed=0.97, pause=0.35),
    "whispers":   dict(exaggeration=0.30, cfg_weight=0.50, temperature=0.60, speed=0.95, pause=0.40),
    "neutral":    dict(exaggeration=0.50, cfg_weight=0.50, temperature=0.80, speed=1.00, pause=0.25),
    "curious":    dict(exaggeration=0.55, cfg_weight=0.50, temperature=0.80, speed=1.00, pause=0.25),
    "confident":  dict(exaggeration=0.55, cfg_weight=0.50, temperature=0.75, speed=1.00, pause=0.25),
    "wonder":     dict(exaggeration=0.65, cfg_weight=0.40, temperature=0.85, speed=0.98, pause=0.30),
    "excited":    dict(exaggeration=0.75, cfg_weight=0.40, temperature=0.85, speed=1.03, pause=0.20),
    "playful":    dict(exaggeration=0.60, cfg_weight=0.45, temperature=0.85, speed=1.02, pause=0.25),
    "deadpan":    dict(exaggeration=0.30, cfg_weight=0.50, temperature=0.60, speed=0.97, pause=0.25),
    "warm":       dict(exaggeration=0.40, cfg_weight=0.45, temperature=0.70, speed=0.95, pause=0.40),
    "mysterious": dict(exaggeration=0.45, cfg_weight=0.35, temperature=0.75, speed=0.95, pause=0.40),
    "serious":    dict(exaggeration=0.50, cfg_weight=0.35, temperature=0.70, speed=0.96, pause=0.35),
    "sad":        dict(exaggeration=0.40, cfg_weight=0.40, temperature=0.70, speed=0.93, pause=0.45),
    "deep":       dict(exaggeration=0.45, cfg_weight=0.30, temperature=0.70, speed=0.92, pause=0.45),
    "tense":      dict(exaggeration=0.70, cfg_weight=0.35, temperature=0.80, speed=1.00, pause=0.20),
    "dramatic":   dict(exaggeration=0.85, cfg_weight=0.30, temperature=0.85, speed=1.00, pause=0.30),
}
ALIASES = {"softly": "soft", "slowly": "deep", "whisper": "whispers"}
FAMILY = {"soft": "soft", "whispers": "soft", "mysterious": "soft",
          "wonder": "wonder", "excited": "wonder", "dramatic": "wonder",
          "deep": "deep", "serious": "deep", "sad": "deep", "tense": "deep",
          "warm": "warm", "confident": "warm",
          "playful": "playful", "deadpan": "playful", "curious": "playful"}
# gap = between beats, hard = before a hard_cut_before beat, lead/tail = file edges
KINDS = {"main":  dict(pause_scale=1.0, speed_mult=1.00, gap=1.2, hard=2.4, lead=0.3, tail=0.8),
         "short": dict(pause_scale=0.6, speed_mult=1.04, gap=0.25, hard=0.6, lead=0.05, tail=0.2)}
KEYWORDS = [
    ("soft",     ["hook", "intro", "open", "cold open"]),
    ("wonder",   ["coral", "ocean", "life", "beauty", "wonder", "spawn"]),
    ("deep",     ["tilt", "axis", "wobble", "season", "ice age", "long term", "deep"]),
    ("tense",    ["tide", "tsunami", "chaos", "collapse", "danger", "storm", "flood"]),
    ("dramatic", ["climax", "reveal", "twist", "impact"]),
    ("warm",     ["outro", "ending", "end", "cta", "subscribe", "conclusion", "payoff"]),
]
TOKEN = re.compile(r"(\{\w+\}|\(beat\)|\(pause\s+[\d.]+\))", re.I)


# ------------------------------------------------------------------ script parsing
def norm_mood(m):
    m = ALIASES.get(m.lower().strip(), m.lower().strip())
    return m if m in PRESETS else None


def pick_mood(name):
    n = name.lower()
    for mood, words in KEYWORDS:
        if any(w in n for w in words):
            return mood
    return "neutral"


def parse(script):
    beats, cur = [], None
    for line in script.splitlines():
        m = re.match(r"^\s*\[(.+?)\]\s*$", line)
        if m:
            parts = [p.strip() for p in m.group(1).split("|")]
            mood = (len(parts) > 1 and norm_mood(parts[1])) or pick_mood(parts[0])
            cur = {"name": parts[0], "mood": mood, "text": ""}
            beats.append(cur)
        elif cur is not None:
            cur["text"] += " " + line.strip()
    for b in beats:
        b["text"] = re.sub(r"\s+", " ", b["text"]).strip()
    return [b for b in beats if TOKEN.sub("", b["text"]).strip()]


def chunks(text, limit=220):
    sents = re.split(r"(?<=[.!?…।])\s+", text)
    out, buf = [], ""
    for s in sents:
        if buf and len(buf) + len(s) + 1 > limit:
            out.append(buf); buf = s
        else:
            buf = (buf + " " + s).strip()
    if buf:
        out.append(buf)
    return out


def pieces(text, beat_mood, pause_scale=1.0):
    """-> (lead_silence, [[chunk, mood, pause_after], ...])"""
    out, mood, lead = [], beat_mood, 0.0
    for tok in TOKEN.split(text):
        tok = tok.strip()
        if not tok:
            continue
        p = re.fullmatch(r"\((beat|pause\s+([\d.]+))\)", tok, re.I)
        if p:
            secs = (1.0 if p.group(1).lower() == "beat" else float(p.group(2))) * pause_scale
            if out: out[-1][2] = max(out[-1][2], secs)
            else: lead = max(lead, secs)
            continue
        m = re.fullmatch(r"\{(\w+)\}", tok)
        if m:
            mood = norm_mood(m.group(1)) or mood
            continue
        for c in chunks(tok):
            out.append([c, mood, PRESETS[mood]["pause"] * pause_scale])
    return lead, out


# ------------------------------------------------------------------ pronunciation lexicon
def lexicon_pattern(lex):
    if not lex:
        return None
    words = sorted((re.escape(w) for w in lex), key=len, reverse=True)
    return re.compile(r"\b(" + "|".join(words) + r")\b", re.I)


def respell(text, lex, pat, idx):
    """Replace lexicon words with their idx-th respelling (last one if fewer)."""
    if pat is None:
        return text
    def rep(m):
        vs = lex.get(m.group(0).lower())
        return vs[min(idx, len(vs) - 1)] if vs else m.group(0)
    return pat.sub(rep, text)


def lexicon_words(text, lex, pat):
    return sorted({m.group(0).lower() for m in pat.finditer(text)}) if pat is not None else []


# ------------------------------------------------------------------ audio helpers
def tempo(wav, sr, speed):
    if abs(speed - 1.0) < 1e-3:
        return wav
    with tempfile.TemporaryDirectory() as d:
        a, b = f"{d}/a.wav", f"{d}/b.wav"
        sf.write(a, wav, sr)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a, "-filter:a", f"atempo={speed}", b], check=True)
        return sf.read(b, dtype="float32")[0]


def loudnorm(wav, sr, lufs=-16.0):
    try:
        import pyloudnorm as pyln
        wav = pyln.normalize.loudness(wav, pyln.Meter(sr).integrated_loudness(wav), lufs)
    except Exception:
        pass
    peak = np.max(np.abs(wav)) or 1.0
    return (wav * min(1.0, 0.89 / peak)).astype(np.float32)   # -1 dBFS ceiling


def word_errors(ref, hyp):
    r, h = ref.split(), hyp.split()
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev, d[j] = d[j], cur
    return d[len(h)]


def squash(s):
    """'k r's' (script) and 'kr's' (Whisper) are the same: join runs of single letters."""
    out, run = [], False
    for w in s.split():
        single = re.fullmatch(r"[a-z]('s)?", w) is not None
        if single and run:
            out[-1] += w
        else:
            out.append(w)
        run = single and not w.endswith("'s")
    return " ".join(out)


def is_strict(job, name):
    return any(k.lower() in name.lower() for k in job.get("strict", []))


def is_hard(job, name):
    return any(k.lower() in name.lower() for k in job.get("hard_cut_before", []))


def silence(sec, sr):
    return np.zeros(int(round(sec * sr)), np.float32)


def mmss(s):
    return f"{int(s // 60)}:{s % 60:04.1f}"


def beat_key(b, job, lang, ref_id, lex):
    used = {w: lex[w] for w in lexicon_words(b["text"], lex, lexicon_pattern(lex))}
    return hashlib.md5(json.dumps([b, job["kind"], lang, ref_id, used]).encode()).hexdigest()[:10]


# ------------------------------------------------------------------ assembly (CPU)
def assemble(cfg, report=None):
    """Join parts/<job>/<nn>.wav into final/<job>.wav. Jobs with a missing beat are skipped."""
    report = report or {}
    os.makedirs(cfg["final"], exist_ok=True)
    for job in cfg["jobs"]:
        beats, k = parse(job["script"]), KINDS[job["kind"]]
        jdir = f"{cfg['parts']}/{job['name']}"
        paths = [f"{jdir}/{i:02d}.wav" for i in range(1, len(beats) + 1)]
        if not all(os.path.exists(p) for p in paths):
            missing = [i for i, p in enumerate(paths, 1) if not os.path.exists(p)]
            print(f"⏭️  {job['name']}: beats {missing} not generated here, not assembled")
            continue
        sr = sf.info(paths[0]).samplerate
        out, t, rows = [silence(k["lead"], sr)], k["lead"], []
        for n, (b, p) in enumerate(zip(beats, paths), 1):
            if n > 1:
                g = k["hard"] if is_hard(job, b["name"]) else k["gap"]
                out.append(silence(g, sr)); t += g
            wav = sf.read(p, dtype="float32")[0]
            info = json.load(open(p[:-4] + ".json"))
            rows.append(dict(n=n, name=b["name"], start=round(t, 2), dur=round(len(wav) / sr, 2),
                             issues=info["issues"]))
            out.append(wav); t += len(wav) / sr
        out.append(silence(k["tail"], sr)); t += k["tail"]
        sf.write(f"{cfg['final']}/{job['name']}.wav", loudnorm(np.concatenate(out), sr), sr)
        prev = report.get(job["name"], {})
        report[job["name"]] = dict(kind=job["kind"], dur=round(t, 2), overall=prev.get("overall"), beats=rows)
        print(f"🎧 {job['name']}.wav · {mmss(t)}")
    json.dump(report, open(cfg["report"], "w"), indent=1)
    return report


# ------------------------------------------------------------------ generation (GPU)
def generate(cfg):
    import torch, librosa
    TRIES, REFS, LANG, JOBS = cfg["tries"], cfg.get("refs", {}), cfg["lang"], cfg["jobs"]
    LEX = {w.lower(): v for w, v in cfg.get("lexicon", {}).items() if v}
    PAT = lexicon_pattern(LEX)
    ONLY = {k: set(v) for k, v in cfg.get("only", {}).items()}
    REF_ID = hashlib.md5(b"".join(open(p, "rb").read() for p in REFS.values())).hexdigest()[:8] if REFS else ""

    plan = []
    for job in JOBS:
        if ONLY and job["name"] not in ONLY:
            continue
        beats = parse(job["script"])
        if not beats:
            sys.exit(f"❌ {job['name']}: empty script")
        plan.append((job, beats))

    print("⏳ loading Chatterbox + Whisper ...", flush=True)
    if LANG == "en":
        from chatterbox.tts import ChatterboxTTS
        model = ChatterboxTTS.from_pretrained(device="cuda")
        say = lambda text, **k: model.generate(text, **k)
    else:
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        model = ChatterboxMultilingualTTS.from_pretrained(device="cuda")
        say = lambda text, **k: model.generate(text, language_id=LANG, **k)
    sr = model.sr
    asr = None
    if LANG == "en":
        import whisper
        from whisper.normalizers import EnglishTextNormalizer
        asr, norm = whisper.load_model("small.en", device="cuda"), EnglishTextNormalizer()
    else:
        print("ℹ️ non-English: only speed and silence are checked")

    def hear(wav):
        a16 = librosa.resample(wav, orig_sr=sr, target_sr=16000).astype(np.float32)
        return norm(asr.transcribe(a16, language="en", fp16=True, temperature=0.0,
                                   condition_on_previous_text=False, verbose=None)["text"])

    def longest_gap(wav):
        iv = librosa.effects.split(wav, top_db=40)
        return max([(iv[k + 1][0] - iv[k][1]) / sr for k in range(len(iv) - 1)], default=0.0)

    def check(wav, original, spoken, strict):
        n_words = len(original.split())
        if wav.size < sr * 0.15 or not np.isfinite(wav).all():
            return dict(ok=False, score=99.0, why="empty or broken audio", heard="")
        why, score = [], 0.0
        wps = n_words / (len(wav) / sr)
        if not (1.2 if n_words < 5 else 1.5) <= wps <= 3.9:
            why.append(f"speed {wps:.1f} words/s"); score += 0.3
        gap = longest_gap(wav)
        if gap > 1.0:
            why.append(f"{gap:.1f}s stuck silence"); score += 0.3
        heard = ""
        if asr is not None:
            heard = squash(hear(wav))
            ref_o, ref_s = squash(norm(original)), squash(norm(spoken))
            errs = min(word_errors(ref_o, heard), word_errors(ref_s, heard))
            score += errs / max(1, len(ref_o.split()))
            if errs > (0 if strict else (1 if n_words >= 10 else 0)):
                why.append(f"{errs} word(s) wrong/missing/extra")
        return dict(ok=not why, score=score, why=", ".join(why), heard=heard)

    CONDS = {}
    for mood, path in REFS.items():
        model.prepare_conditionals(path, exaggeration=0.5)
        CONDS[mood] = model.conds
    FALLBACK = CONDS.get("default") or (next(iter(CONDS.values())) if CONDS else None)

    def use_voice(mood):
        if CONDS:
            model.conds = CONDS.get(mood) or CONDS.get(FAMILY.get(mood, "")) or FALLBACK

    print("✅ ready", flush=True)
    lex_hits = {}
    for job, beats in plan:
        k = KINDS[job["kind"]]
        jdir = f"{cfg['parts']}/{job['name']}"
        os.makedirs(jdir, exist_ok=True)
        only = ONLY.get(job["name"])
        print(f"\n🎬 {job['name']}", flush=True)
        for i, b in enumerate(beats, 1):
            if only is not None and i not in only:
                continue
            lead, parts = pieces(b["text"], b["mood"], k["pause_scale"])
            strict = is_strict(job, b["name"])
            base = random.randint(1, 10 ** 6) if only else 1000 * i
            audio, issues, tries_used = [silence(lead, sr)], [], 0
            for ci, (c, mood, gap) in enumerate(parts):
                words = lexicon_words(c, LEX, PAT)
                n_var = max([len(LEX[w]) for w in words], default=1)
                # variant 0 gets the full tries; each further respelling gets 2
                attempts = [(0, t) for t in range(TRIES + (2 if strict else 0))]
                attempts += [(v, t) for v in range(1, n_var) for t in range(2)]
                best = None
                for a, (v, t) in enumerate(attempts):
                    spoken = respell(c, LEX, PAT, v)
                    torch.manual_seed(base + 100 * ci + a)
                    p = PRESETS[mood]
                    use_voice(mood)
                    w = say(spoken, exaggeration=p["exaggeration"], cfg_weight=p["cfg_weight"],
                            temperature=p["temperature"]).squeeze(0).cpu().numpy().astype(np.float32)
                    w, _ = librosa.effects.trim(w, top_db=40)
                    w = tempo(w, sr, p["speed"] * k["speed_mult"])
                    res = check(w, c, spoken, strict)
                    tries_used += 1
                    if best is None or res["score"] < best[1]["score"]:
                        best = (w, res, v)
                    if res["ok"]:
                        break
                    print(f"      ↻ retry {a + 1}: {res['why']} · \"{spoken[:50]}\"", flush=True)
                w, res, v = best
                if res["ok"]:
                    for wd in words:
                        lex_hits[wd] = LEX[wd][min(v, len(LEX[wd]) - 1)]
                else:
                    issues.append(dict(text=c, heard=res["heard"], why=res["why"], lexicon_words=words))
                audio += [w, silence(gap, sr)]
            wav = loudnorm(np.concatenate(audio[:-1]), sr)
            sf.write(f"{jdir}/{i:02d}.wav", wav, sr)
            json.dump(dict(issues=issues, tries=tries_used, chunks=len(parts), text=b["text"]),
                      open(f"{jdir}/{i:02d}.json", "w"))
            print(f"   {'✅' if not issues else '⚠️'} {job['name']} {i:02d} {b['name']} — {len(wav) / sr:.1f}s, "
                  f"{tries_used} tries" + (f", {len(issues)} line(s) failed" if issues else ""), flush=True)

    report = assemble(cfg)
    if asr is not None:   # listen to each full file once: % of script words heard
        for job, beats in plan:
            path = f"{cfg['final']}/{job['name']}.wav"
            if job["name"] not in report or not os.path.exists(path):
                continue
            full = sf.read(path, dtype="float32")[0]
            ref = squash(norm(" ".join(TOKEN.sub(" ", b["text"]) for b in beats)))
            heard = squash(norm(asr.transcribe(librosa.resample(full, orig_sr=sr, target_sr=16000).astype(np.float32),
                                               language="en", fp16=True, verbose=None)["text"]))
            report[job["name"]]["overall"] = round(100 * (1 - word_errors(ref, heard) / max(1, len(ref.split()))), 1)
    report["_lexicon_hits"] = lex_hits
    json.dump(report, open(cfg["report"], "w"), indent=1)
    print("\n🎉 done", flush=True)


if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1]))
    if "--assemble" in sys.argv:
        prev = json.load(open(cfg["report"])) if os.path.exists(cfg["report"]) else {}
        assemble(cfg, {k: v for k, v in prev.items() if not k.startswith("_")})
    else:
        generate(cfg)
