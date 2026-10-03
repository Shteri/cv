---
workflow: product-launch-video
flow: automation
storyboard: no
message: "טיפולית למוסכים שומרת על הקשר עם הלקוחות: מי צריך לחזור ומתי, תזכורת בוואטסאפ, הצטרפות בקוד QR, היסטוריה, כרטיס עבודה, תורים וחלקים"
destination: reels
aspect: 1080x1920
language: he
length: 33s
angle: customer-retention
style_preset: dark-hud
---

## Intent

The garage-side promo, in the same dark HUD style as ../tipulit-hud (the driver video). Max: "one of the main points
for the garage side is keeping in touch with customers (and the other features)". So retention leads, the rest follows.

## Structure (seconds)

| beat | time | narration | picture (real /garage/?demo screens, dark mode) |
|---|---|---|---|
| hook | 0.2 | כמה מהלקוחות שלך לא חזרו השנה? | hologram car, words slam |
| logo | 2.4 | טיפולית למוסכים שומרת על הקשר. | logo + "למוסכים" pill, flash |
| 01 | 4.6 | כל לקוח, עם הטיפול הבא... ותזכורת בוואטסאפ, בלחיצה. | board row lens; KPI "6 באיחור"; filter "לא היו מעל שנה 9"; KPI "8 טסט"; WhatsApp tap → message lens |
| 02 | 14.55 | לקוחות מצטרפים בקוד QR, וכל ביקור נשמר בהיסטוריה של הרכב. | invite poster with QR (encodes https://tipulit.netlify.app/?join=demo); customer card history |
| 03 | 18.8 | כרטיס עבודה לפי ספר היבואן, ואישור עבודה נוספת מהטלפון. | work-order lines lens; customer's phone, approve tap |
| 04 | 23.1 | ובנוסף: תורים אונליין, ורשימת חלקים להזמין מראש. | booking slots lens; order list (oil, oil filter) |
| CTA | 27.2 | טיפולית למוסכים. הלקוחות שלך, בזמן. נסו את ההדגמה. | hologram, logo, button, tipulit.netlify.app/garage |

## Assets

- capture/: dark-mode Playwright captures of /garage/?demo at 1440x900 @2x (board, lapsed filter, WhatsApp dialog,
  invite, customer card, work order, order list) and the customer pages /approve/?demo and /book/?demo at 390x844 @3x.
- assets/vo/temp_*.wav: DRAFT voice (edge-tts he-IL Hila). Replace with ElevenLabs (see below).

## Next session (needs ELEVENLABS_API_KEY)

Same as ../tipulit-hud: `python3 tools/voice_elevenlabs.py --list`, then `--voice <id>` (use the same voice as the
driver video), adjust tools/vo_starts.json and beat times if a line runs over, `python3 tools/build.py eleven`, render.
