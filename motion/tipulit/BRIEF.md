---
workflow: product-launch-video
flow: automation
storyboard: no
message: "טיפולית אומרת לך מתי הטיפול הבא, מה מצב כל פריט ברכב, ואיפה המוסך הקרוב"
destination: reels
aspect: 1080x1920
language: he
length: 30s
angle: show-the-app-working
style_preset: liquid-glass
---

## Intent

סרטון פרומו קצר ל-Tipulit (טיפולית), אפליקציה בעברית שעוקבת אחרי מצב הרכב ולוח הטיפולים לפי ספר היבואן. אנכי, 30 שניות, בלי קריינות. סגנון Liquid Glass: כרטיסי זכוכית חלבית, רקע בהיר עם כתמי צבע רכים, תנועה רגועה. הצהוב של לוחית הרישוי הוא המבטא היחיד של המותג.

מבנה (מהבקשה של מקס): פתיחה עם הלוגו, שלושה רגעים שמראים את האפליקציה עובדת (תזכורת לפי ק"מ וזמן, מצב הרכב לפי פריט, מוסך ליד הבית), וסיום עם קריאה לפעולה.

## Version 2 (current)

- Demo car: Alfa Romeo Giulia 2021 (schedule alfa-romeo-giulia-2016-2025-2.0), 52,300 km. Brake fluid last changed at 15,200 km, so it shows as overdue (due 45,200); oil changed at 45,200.
- Narration in Hebrew (SCRIPT.txt). Two voices rendered: Hila (renders/tipulit-v2-hila.mp4, main) and Avri (same picture, audio remixed). TTS from Microsoft's he-IL neural voices via edge-tts, used as a draft voice; for a paid campaign, re-voice with a licensed TTS account or a human recording.
- 3D: the phone tilts and flips between screens, rows and tiles from the real screenshots lift out of the phone, callouts flip in.
- Real photos instead of icons: a floating Alfa Romeo Giulia (cut out, plate and driver's window masked), a car X-ray with the parts marked on it, and a dive into a real Alfa engine bay for the oil.

## Assets

- capture/app/v_home.png, v_next.png — מסך הבית, למעלה ואחרי גלילה לכרטיס "הטיפול הבא". צולמו מהאפליקציה האמיתית (Playwright, 390x844 @3x, ערכת צבעים בהירה) עם רכב לדוגמה: אלפא רומיאו ג'וליה 2021, 52,300 ק"מ (בגרסה 1: מאזדה 3).
- capture/app/v_reminders.png — מסך "אני", כרטיס התזכורות.
- capture/app/v_condition.png — מסך "הרכב", מצב לפי פריט.
- capture/app/v_garages.png — "מוסך ליד הבית" ברמת גן, ממאגר המוסכים המורשים.
- capture/app/rects.json — מיקומי האלמנטים בכל צילום (פיקסלים של הצילום), משמשים לזומים ולהדגשות.
- assets/fonts — Rubik, IBM Plex Sans Hebrew ו-Unbounded (הפונטים של האפליקציה, מ-Google Fonts).
- assets/sfx — 9 הסאונדים מה-starter kit.
- assets/vo — narration clips (hila_*, avri_*) and word timings.
- assets/photos/giulia.png — cut-out of "Alfa Romeo Giulia 2.0 Turbo MultiAir (2020) (54723466036).jpg", Wikimedia Commons, CC0. Licence plate and the driver's window were masked.
- assets/photos/engine.jpg — "Alfa Romeo Tonale Plug-in Hybrid engine.jpg", Wikimedia Commons, CC0.
- tools/icons — Phosphor Icons (MIT), used in the small part labels.
- tools/build.py builds index.html from tools/index.src.html (fonts, icons and narration inlined). Edit the .src file, then run `python3 tools/build.py hila` (or avri).

## Customizations

- הצילומים משמשים כמו שהם, בלי לצייר אותם מחדש. זומים והדגשות מעליהם.
- סאונדים קטנים רק ברגעים החשובים: pop על הלוגו, counter על ספירת הק"מ, switch על התזכורות, snap על פריט באיחור, pop על המיקום, chime על הקריאה לפעולה.

## Notes

- המספרים בסרטון הם מהאפליקציה עם נתוני הרכב לדוגמה. 4,963 מוסכים מורשים ו-12 ברמת גן הם מהמאגר (data/garages.json, 28.9.2026).
- הרינדור המקורי ביקש ~/Desktop/Motion/tipulit/renders/tipulit.mp4; הסשן רץ בענן, אז הקובץ נמצא ב-renders/tipulit.mp4 בפרויקט הזה.
