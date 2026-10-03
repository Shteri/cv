---
workflow: product-launch-video
flow: automation
storyboard: no
message: "מתי הטיפול הבא? טיפולית יודעת: תזכורת לפי ק\"מ וזמן, מצב הרכב לפי פריט, מוסך מורשה ליד הבית"
destination: reels
aspect: 1080x1920
language: he
length: 32s
angle: problem-solution-sell
style_preset: dark-hud
---

## Intent

Version 3 of the Tipulit promo, after Max's feedback on v2: "should be high-tech, dynamic, futuristic; it wasn't
clear, didn't highlight the app, didn't explain, didn't sell, looked basic; the voice sounds AI; the car looked
pasted". So:

- Dark futuristic HUD: graphite background, moving perspective grid, scanlines, HUD corners and a timecode.
  Plate yellow (#F7C948) is the neon accent; red/green/grey only for item status.
- A 3D hologram car built in code (tools/holo.js): CAD-style contour wireframe of a sedan, drawn on a canvas each
  frame (the renderer has no WebGL). Parts glow inside it: engine (oil, green = OK), brake discs (red = overdue),
  tyres (grey = unknown). No pasted photos.
- Every app moment is explained: a spotlight dims the rest of the real screenshot, the spotted UI pops out
  enlarged ("lens"), and a one-line label says what it means. Big numbers count up (7,700 km, 4,963 garages).
- Script is problem → answer → three features → CTA (SCRIPT.txt).

## Structure (seconds)

| beat | time | narration | picture |
|---|---|---|---|
| hook | 0.2 | מתי הטיפול הבא של הרכב שלך? | hologram car builds, words slam in |
| answer | 2.1 | רוב הנהגים מנחשים. טיפולית יודעת. | "?" marks, glitch, logo slam with flash |
| 01 reminder | 5.3 | מקלידים מספר רכב... לפי קילומטרים, וגם לפי זמן. | phone; plate lens; oil + brake rows lens; 7,700 km count; "עד נובמבר 2026" |
| 02 condition | 12.6 | מצב הרכב, פריט אחרי פריט... לפני שזה עולה ביוקר. | X-ray hologram, parts light up; overdue brake-fluid row lens; red stamp |
| 03 garages | 21.45 | צריכים מוסך? מוסכים מורשים ליד הבית... | city chip lens; 4,963 count; recommended garage lens |
| CTA | 26.85 | טיפולית. הרכב שלך, בזמן. נסו עכשיו. | hologram, logo, plate types itself, button, URL |

## Assets

- capture/v_*.png, rects.json: the real app in dark mode (Playwright, 390x844 @3x), demo car Alfa Romeo Giulia 2021,
  52,300 km, brake fluid last changed at 15,200 km (overdue), oil at 45,200. Capture script: ../tipulit/tools/capture-app.mjs.
- assets/vo/temp_*.wav: DRAFT voice (Microsoft he-IL Hila via edge-tts, +12%). Placeholder only.
- assets/sfx: starter-kit sounds. assets/fonts: the app's fonts (Rubik, IBM Plex Sans Hebrew, Unbounded).
- tools/index.src.html + tools/holo.js → `python3 tools/build.py <voice>` → index.html.

## Next session (needs ELEVENLABS_API_KEY in the environment)

1. `python3 tools/voice_elevenlabs.py --list` and pick a natural Hebrew voice (male or female, warm, confident).
2. `python3 tools/voice_elevenlabs.py --voice <id>`; it reports each line's length against its slot.
3. If a line is too long, adjust tools/vo_starts.json and the matching beat times in tools/index.src.html
   (word timings are in assets/vo/eleven_*.words.json).
4. `python3 tools/build.py eleven`, `npx hyperframes check`, render to renders/tipulit-hud.mp4.
5. The garage-side version in this style is ../tipulit-garage-hud (same voice steps).
