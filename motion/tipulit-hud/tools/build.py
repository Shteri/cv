"""Builds index.html from tools/index.src.html: inlines @font-face rules, the hologram renderer and the narration.
Usage: python3 tools/build.py [voice]   voice = file prefix in assets/vo (temp = draft TTS, eleven = ElevenLabs)."""
import os, sys, json
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
voice = sys.argv[1] if len(sys.argv) > 1 else "temp"
src = open(os.path.join(here, "index.src.html"), encoding="utf-8").read()
fonts = open(os.path.join(here, "fonts.css"), encoding="utf-8").read()
holo = open(os.path.join(here, "holo.js"), encoding="utf-8").read()
# one narration clip per beat; the visuals are timed to these starts (see SCRIPT.txt and BRIEF.md)
VO_STARTS = json.load(open(os.path.join(here, "vo_starts.json")))
vo = "\n".join(f'      <audio id="vo-{i+1}" src="assets/vo/{voice}_{i+1}.wav" data-start="{t}" data-volume="1"></audio>' for i, t in enumerate(VO_STARTS))
out = src.replace("{{FONTS}}", fonts).replace("{{HOLO}}", holo).replace("{{VO}}", vo)
open(os.path.join(root, "index.html"), "w", encoding="utf-8").write(out)
print("built index.html with voice", voice)
