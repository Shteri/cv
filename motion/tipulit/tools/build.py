"""Builds index.html from tools/index.src.html: inlines @font-face rules, Phosphor icons and the narration clips."""
import re, os, sys
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
voice = sys.argv[1] if len(sys.argv) > 1 else "hila"
src = open(os.path.join(here, "index.src.html"), encoding="utf-8").read()
fonts = open(os.path.join(here, "fonts.css"), encoding="utf-8").read()
def icon(m):
    svg = open(os.path.join(here, "icons", m.group(1) + ".svg"), encoding="utf-8").read().strip()
    return svg.replace("<svg ", '<svg class="ic" aria-hidden="true" ', 1)
VO_STARTS = [0.15, 3.6, 12.4, 20.0, 25.95]  # one line per beat, see SCRIPT.txt
vo = "\n".join(f'      <audio id="vo-{i+1}" src="assets/vo/{voice}_{i+1}.wav" data-start="{t}" data-volume="1"></audio>' for i, t in enumerate(VO_STARTS))
out = src.replace("{{FONTS}}", fonts).replace("{{VO}}", vo)
out = re.sub(r"\{\{icon:([\w-]+)\}\}", icon, out)
open(os.path.join(root, "index.html"), "w", encoding="utf-8").write(out)
print("built index.html with voice", voice)
