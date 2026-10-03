from lib import grid, write
I7 = "IIIIIII"
ROWS = [
    ("battery_12v", I7, None),
    ("cooling_system", I7, "משטח המצנן (רדיאטור)"),
    ("lights", I7, "כל פנסי הרכב"),
    ("body_underside", I7, "איתור דליפות שמן, מים וגז ובדיקת זליגת חשמל"),
    ("suspension", I7, "אומים וברגים"),
    ("cv_boots", I7, "מפרקים וכיסויי אבק"),
    ("brake_pads", I7, "בלמים: דיסקים, רפידות וידית בלם היד"),
    ("brake_discs", I7, None),
    ("parking_brake", I7, None),
    ("cabin_filter", "RRRRRRR", None),
    ("hybrid_system", I7, "סוללת המתח הגבוה: מומנט ברגי החיבור לשלדה, היחידה עצמה, מחברי מתח נמוך וגבוה, ומצב הסוללה (בריאות והתנגדות בידוד)"),
    ("electrical_system", I7, "מצב מרכב הרכב"),
]
write(dict(
    id="ora-funky-cat-2023-2026-ev", make="ORA", make_he="אורה", model="Funky Cat / ORA 03", model_he="פאנקי קאט / אורה 03", generation="ORA 03 (Funky Cat)",
    years=[2023, 2026], engines=["EV (TZ153XS001)"], fuel="electric", importer="כלמוביל",
    interval={"km": 30000, "months": 24, "note": "לפי תכנית הבדיקות והטיפולים בתעודת האחריות של היבואן: כל 30,000 ק\"מ או 24 חודשים"},
    cycle_km=210000,
    services=grid(30000, 7, ROWS),
    long_interval=[
        {"item": "brake_fluid", "action": "replace", "every_km": 40000, "every_months": 24,
         "note": "נוזל בלמים: לכל המאוחר כל שנתיים או 40,000 ק\"מ"},
        {"item": "coolant", "action": "replace", "every_km": 40000, "every_months": 48,
         "note": "נוזל קירור: לכל המאוחר כל 4 שנים או 40,000 ק\"מ (כך בטבלה)"},
        {"item": "tires", "action": "inspect", "every_km": 10000, "every_months": 12,
         "note": "בדיקה שגרתית של לחץ אוויר ובלאי על ידי המשתמש (מומלץ פעם בשנה או כל 10,000 ק\"מ); סבב גלגלים כשמתגלה בלאי חריג"},
    ],
    specs={"brake_fluid": "DOT 4 סינתטי, 0.72 ליטר",
           "coolant": "אתילן גליקול 35; מעגל מערכת ההנעה 6.5 ליטר, מעגל המיזוג/חימום 2.1 ליטר",
           "battery": "סוללת הנעה + מצבר 12V",
           "_note": "שמן תיבת ההילוכים: Castrol BOT 352 B1 BEV, 0.74 ליטר (ספר הרכב העברי, עמ' 221)"},
    sources=[
        {"url": "https://res.cloudinary.com/colmobil/images/v1781681468/ora-warranty-06.2024-1/ora-warranty-06.2024-1.pdf", "kind": "importer",
         "note": "תעודת אחריות ORA של כלמוביל (06.2024), 'תכנית בדיקות וטיפולי תחזוקה תקופתיים' עמ' 8-9; מקושרת מעמוד השירות ora-israel.co.il/service"},
        {"url": "https://res.cloudinary.com/colmobil/images/v1715766312/ספר-רכב-אורה-03-28.3/ספר-רכב-אורה-03-28.3.pdf", "kind": "importer",
         "note": "ספר רכב אורה 03 בעברית (28.3): נתוני שמנים ונוזלים עמ' 221, סבב צמיגים עמ' 209"},
    ],
    status="reviewed",
    notes="לפי תעודת האחריות של כלמוביל ל-ORA. טיפול כל 30,000 ק\"מ או שנתיים: בדיקות מצבר, מצנן, תאורה, דליפות, ברגים, מפרקים, בלמים וסוללת המתח הגבוה, והחלפת מסנן מזגן. "
          "נוזל בלמים מוחלף לכל המאוחר כל שנתיים או 40,000 ק\"מ ונוזל קירור כל 4 שנים או 40,000 ק\"מ. שמן תיבת ההילוכים אינו דורש החלפה בשימוש רגיל; בתנאים קשים (נסיעות קצרות, אבק, קור, מלח, הצפות) - כל 50,000 ק\"מ. "
          "ORA 3 החדשה (2025-2026) נושאת אותו קוד מנוע ושויכה לאותה תכנית.",
))
