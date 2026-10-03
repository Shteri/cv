"""Generate the narration with ElevenLabs (one clip per line of SCRIPT.txt) and report how it fits the timeline.

Needs ELEVENLABS_API_KEY in the environment (cloud environment settings, never the repo) or the ElevenLabs connector,
which injects the credential at the proxy.

  python3 tools/voice_elevenlabs.py --list                      # Hebrew-capable voices on the account
  python3 tools/voice_elevenlabs.py --voice <voice_id>          # writes assets/vo/eleven_N.wav + eleven_N.words.json
  python3 tools/build.py eleven                                  # then build index.html with that voice

The visuals are timed to tools/vo_starts.json (one start per line). After generating, the script prints each
clip's length against the gap to the next start; if a clip runs over, shorten the line or move the starts and the
matching beats in tools/index.src.html.
"""
import argparse, base64, json, os, ssl, subprocess, sys, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
API = "https://api.elevenlabs.io/v1"
CTX = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE") or None)


def call(path, body=None):
    # with no key set, the request goes out bare and the session's egress proxy adds the ElevenLabs credential
    key = os.environ.get("ELEVENLABS_API_KEY")
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if key: headers["xi-api-key"] = key
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None, headers=headers)
    try:
        with urllib.request.urlopen(req, context=CTX, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs {e.code}: {e.read().decode(errors='replace')[:300]}")


def words_from_alignment(al, offset):
    chars, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    out, cur, s0 = [], "", None
    for c, a, b in zip(chars, st, en):
        if c.isspace():
            if cur: out.append({"text": cur, "start": round(s0 - offset, 3), "end": round(prev - offset, 3)})
            cur, s0 = "", None
        else:
            if s0 is None: s0 = a
            cur += c; prev = b
    if cur: out.append({"text": cur, "start": round(s0 - offset, 3), "end": round(prev - offset, 3)})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--voice")
    ap.add_argument("--model", default="eleven_v3", help="eleven_v3 reads Hebrew; try eleven_multilingual_v2 / eleven_flash_v2_5 if the account lacks v3")
    ap.add_argument("--stability", type=float, default=0.45)
    ap.add_argument("--style", type=float, default=0.35)
    a = ap.parse_args()
    if a.list:
        for v in call("/voices")["voices"]:
            labels = v.get("labels") or {}
            print(v["voice_id"], "|", v["name"], "|", labels.get("gender", ""), labels.get("accent", ""), labels.get("language", ""), "|", v.get("category", ""))
        return
    if not a.voice:
        sys.exit("pass --voice <voice_id> (see --list)")
    lines = [l.strip() for l in open(os.path.join(ROOT, "SCRIPT.txt"), encoding="utf-8") if l.strip()]
    starts = json.load(open(os.path.join(HERE, "vo_starts.json")))
    for i, text in enumerate(lines, 1):
        r = call(f"/text-to-speech/{a.voice}/with-timestamps?output_format=mp3_44100_128",
                 {"text": text, "model_id": a.model, "voice_settings": {"stability": a.stability, "similarity_boost": 0.8, "style": a.style, "use_speaker_boost": True}})
        raw = os.path.join(ROOT, "assets/vo", f"eleven_{i}.mp3")
        open(raw, "wb").write(base64.b64decode(r["audio_base64"]))
        al = r.get("alignment") or r.get("normalized_alignment")
        lead = al["character_start_times_seconds"][0] if al else 0.0
        wav = os.path.join(ROOT, "assets/vo", f"eleven_{i}.wav")
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", str(max(0, lead - 0.02)), "-i", raw, "-af",
                        "areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse", "-ar", "48000", "-ac", "1", wav], check=True)
        os.remove(raw)
        if al: json.dump(words_from_alignment(al, lead), open(os.path.join(ROOT, "assets/vo", f"eleven_{i}.words.json"), "w"), ensure_ascii=False, indent=0)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav], capture_output=True, text=True).stdout)
        room = (starts[i] if i < len(starts) else 32.2) - starts[i - 1]
        print(f"line {i}: {dur:5.2f}s of {room:5.2f}s room {'OK' if dur <= room - 0.15 else 'TOO LONG'}  | {text}")


if __name__ == "__main__":
    main()
