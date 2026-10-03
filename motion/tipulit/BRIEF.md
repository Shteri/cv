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

## Assets

- capture/app/v_home.png, v_next.png — מסך הבית, למעלה ואחרי גלילה לכרטיס "הטיפול הבא". צולמו מהאפליקציה האמיתית (Playwright, 390x844 @3x, ערכת צבעים בהירה) עם רכב לדוגמה: מאזדה 3 2021, 52,300 ק"מ.
- capture/app/v_reminders.png — מסך "אני", כרטיס התזכורות.
- capture/app/v_condition.png — מסך "הרכב", מצב לפי פריט.
- capture/app/v_garages.png — "מוסך ליד הבית" ברמת גן, ממאגר המוסכים המורשים.
- capture/app/rects.json — מיקומי האלמנטים בכל צילום (פיקסלים של הצילום), משמשים לזומים ולהדגשות.
- assets/fonts — Rubik, IBM Plex Sans Hebrew ו-Unbounded (הפונטים של האפליקציה, מ-Google Fonts).
- assets/sfx — 9 הסאונדים מה-starter kit.

## Customizations

- הצילומים משמשים כמו שהם, בלי לצייר אותם מחדש. זומים והדגשות מעליהם.
- סאונדים קטנים רק ברגעים החשובים: pop על הלוגו, counter על ספירת הק"מ, switch על התזכורות, snap על פריט באיחור, pop על המיקום, chime על הקריאה לפעולה.

## Notes

- המספרים בסרטון הם מהאפליקציה עם נתוני הרכב לדוגמה. 4,963 מוסכים מורשים ו-12 ברמת גן הם מהמאגר (data/garages.json, 28.9.2026).
- הרינדור המקורי ביקש ~/Desktop/Motion/tipulit/renders/tipulit.mp4; הסשן רץ בענן, אז הקובץ נמצא ב-renders/tipulit.mp4 בפרויקט הזה.
