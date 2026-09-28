from lib import grid, write

TESLA_NOTE_COMMON = ("טסלה אינה מגדירה טיפול תקופתי קבוע: הרכב מטופל לפי הצורך, ורק פריטים בודדים מקבלים מרווח. "
                     "הטיפול היחיד לפי ק\"מ הוא סבב צמיגים כל 10,000 ק\"מ (או כשהפרש עומק החריץ בין הצמיגים מגיע ל-1.5 מ\"מ), ולכן הוא משמש כאן כמרווח הבסיסי. "
                     "ניקוי ושימון קליפרים (כל שנה או 20,000 ק\"מ) נדרש רק באזורים שבהם מפזרים מלח על הכבישים בחורף - לא רלוונטי בישראל. "
                     "נוזל הקירור של הסוללה אינו מוחלף לאורך חיי הרכב ברוב המקרים. אין ספר עברי זמין: tesla.com חוסם את הסביבה הזו (403), ולכן זו טיוטה לפי העתקים של ספר הבעלים הבינלאומי.")

write({
    "id": "tesla-model-3-2021-2026-ev",
    "make": "Tesla", "make_he": "טסלה", "model": "Model 3", "model_he": "מודל 3",
    "generation": "Model 3 / Model 3 Highland", "years": [2021, 2026],
    "engines": ["EV (3D1 / 3D3 / 3D5 / 3D6 / 3D7)"], "fuel": "electric",
    "importer": "טסלה מוטורס ישראל",
    "interval": {"km": 10000, "months": 12,
                 "note": "אין טיפול תקופתי קבוע; המרווח כאן הוא סבב הצמיגים כל 10,000 ק\"מ. חודשים: אין מרווח זמן בספר לטיפול כללי - 12 חודשים הם ערך תצוגה בלבד"},
    "cycle_km": 10000,
    "services": grid(10000, 1, [
        ("tire_rotation", "T", "סבב צמיגים כל 10,000 ק\"מ, או מוקדם יותר אם הפרש עומק החריץ 1.5 מ\"מ ומעלה"),
        ("tires", "I", "מצב ולחץ - מומלץ גם בבדיקה יומית"),
    ]),
    "time_based": [
        {"item": "cabin_filter", "action": "replace", "months": 24, "note": "מסנן אוויר לתא הנוסעים כל שנתיים"},
        {"item": "brake_fluid", "action": "inspect", "months": 48, "note": "בדיקת מצב נוזל הבלמים כל 4 שנים והחלפה לפי הצורך (בספר הישן יותר: כל שנתיים); בגרירה, ירידות ארוכות ואקלים חם ולח - לעתים קרובות יותר"},
        {"item": "ac_system", "action": "replace", "months": 72, "note": "החלפת שקית הייבוש (desiccant) של מערכת המיזוג כל 6 שנים"},
    ],
    "specs": {"battery": "סוללת מתח גבוה + מצבר עזר 12V/סוללה במתח נמוך",
              "_note": "טיוטה - לפי ספר הבעלים הבינלאומי, לא נבדק מול מסמך של טסלה ישראל"},
    "sources": [
        {"url": "https://hamphi.com/en-eu/pages/tesla-original-guides/model-3-serviceintervall-for-fordon", "kind": "other",
         "note": "העתק (מתורגם) של פרק 'מרווחי טיפול' מספר הבעלים האירופי של Model 3 באתר Hamphi (שבדיה): נוזל בלמים 4 שנים, שקית ייבוש 6 שנים, מסנן מזגן שנתיים, סבב צמיגים 10,000 ק\"מ"},
        {"url": "https://www.manualslib.com/manual/1765784/Tesla-Model-3.html?page=163", "kind": "other",
         "note": "מהדורה ישנה יותר של ספר הבעלים של Model 3 (צפון אמריקה, מיילים וק\"מ), עמ' 162-163: נוזל בלמים כל שנתיים, שקית ייבוש 6 שנים, מסנן מזגן שנתיים, סבב צמיגים כל 16,000-20,000 ק\"מ; נפתח דרך Playwright"},
        {"url": "https://www.tesla.com/ownersmanual/model3/en_eu/GUID-E95DAAD9-646E-4249-9930-B109ED7B1D91.html", "kind": "manufacturer",
         "note": "המקור הרשמי (ספר בעלים אירופי) - חסום מכאן (403 ב-curl וב-WebFetch), לא נפתח ישירות"},
    ],
    "status": "draft",
    "notes": TESLA_NOTE_COMMON + " הערכים לקוחים מהמהדורה האירופית העדכנית; במהדורה ישנה יותר נוזל הבלמים נבדק כל שנתיים וסבב הצמיגים היה כל 16,000-20,000 ק\"מ.",
})

write({
    "id": "tesla-model-y-2022-2026-ev",
    "make": "Tesla", "make_he": "טסלה", "model": "Model Y", "model_he": "מודל Y",
    "generation": "Model Y / Model Y Juniper", "years": [2022, 2026],
    "engines": ["EV (3D3 / 3D6 / 3D7 / 4D1 / 4D3)"], "fuel": "electric",
    "importer": "טסלה מוטורס ישראל",
    "interval": {"km": 10000, "months": 12,
                 "note": "אין טיפול תקופתי קבוע; המרווח כאן הוא סבב הצמיגים כל 10,000 ק\"מ. חודשים: אין מרווח זמן בספר לטיפול כללי - 12 חודשים הם ערך תצוגה בלבד"},
    "cycle_km": 10000,
    "services": grid(10000, 1, [
        ("tire_rotation", "T", "סבב צמיגים כל 10,000 ק\"מ, או מוקדם יותר אם הפרש עומק החריץ 1.5 מ\"מ ומעלה"),
        ("tires", "I", "מצב ולחץ - מומלץ גם בבדיקה יומית"),
    ]),
    "time_based": [
        {"item": "cabin_filter", "action": "replace", "months": 24, "note": "מסנן אוויר לתא הנוסעים כל שנתיים (מסנני HEPA ופחם, אם קיימים: כל 3 שנים)"},
        {"item": "brake_fluid", "action": "inspect", "months": 24, "note": "בדיקת מצב נוזל הבלמים כל שנתיים והחלפה לפי הצורך; ברכב שגורר - החלפה כל שנתיים"},
        {"item": "ac_system", "action": "replace", "months": 48, "note": "החלפת שקית הייבוש (desiccant) של מערכת המיזוג כל 4 שנים"},
    ],
    "long_interval": [
        {"item": "cabin_filter", "action": "replace", "every_months": 36, "note": "מסנן HEPA (אם קיים) - כל 3 שנים"},
    ],
    "specs": {"battery": "סוללת מתח גבוה + מצבר עזר/סוללה במתח נמוך",
              "_note": "טיוטה - לפי ספר הבעלים הבינלאומי, לא נבדק מול מסמך של טסלה ישראל"},
    "sources": [
        {"url": "https://www.mycarusermanual.com/tesla/model-y/suv/2023/maintenance--maintenance-service-intervals", "kind": "other",
         "note": "העתק של פרק 'מרווחי טיפול' מספר הבעלים של Model Y 2023 (מיילים וק\"מ) באתר mycarusermanual"},
        {"url": "https://www.tesla.com/ownersmanual/modely/en_gb/Owners_Manual.pdf", "kind": "manufacturer",
         "note": "ספר הבעלים האירופי הרשמי - חסום מכאן (403), לא נפתח"},
    ],
    "status": "draft",
    "notes": TESLA_NOTE_COMMON + " הערכים לקוחים מהעתק של ספר Model Y 2023; לא נמצא העתק פתוח של הספר לגרסת Juniper (2025 ואילך).",
})

# ---------------- Xpeng G6 (EU warranty & maintenance manual) ----------------
A = [
    ("hybrid_system", "II", "סוללת ההנעה: מראה חיצוני, ריח, מחברים ורתמות מתח גבוה ונמוך, מומנט ברגים, שסתום איזון/נשימה; מתג השירות נבדק רק בטיפול B"),
    ("electrical_system", "II", "מנועי ההנעה, רתמות, צנרת בקרת טמפרטורה, שקעי טעינה ופונקציות חשמל ברכב"),
    ("battery_12v", "II"),
    ("lights", "II", "תאורה חיצונית, פנימית וצופר"),
    ("diagnostics", "II", "קריאת תקלות ובדיקת/עדכון גרסת תוכנה"),
    ("parking_brake", "II", "בלם חניה חשמלי (EPB)"),
    ("brake_pads", "II"),
    ("brake_discs", "II", "דיסקים וקליפרים"),
    ("brake_fluid", "IR"),
    ("brake_lines", "II"),
    ("pedals", "II", "מהלך דוושת הבלם"),
    ("steering", "II", "חופש בהגה, עמוד היגוי, מנוע EPS, מוטות ומפרקים"),
    ("wipers", "II"),
    ("washer_fluid", "II", "השלמה"),
    ("door_hinges", "II", "בדיקה ושימון מנעולים, צירים ומעצורים, מכסה מנוע ותא מטען"),
    ("seat_belts", "II"),
    ("body_underside", "II", "חלודה במרכב, אטמים וחלונות"),
    ("transmission_oil", "II", "מפלס/מראה שמן תיבת ההפחתה"),
    ("cv_boots", "II", "גלי הינע וכיסויי אבק"),
    ("tires", "II", "צמיגים, חישוקים ומומנט אומים"),
    ("tire_rotation", "TT", "אם נדרש"),
    ("wheel_alignment", "II", "בדיקת בלאי לא אחיד; כיוון לפי הצורך"),
    ("suspension", "II", "מתלים, בולמים, קפיצים ומסבי גלגלים; מומנט ברגי שלדה"),
    ("coolant", "II"),
    ("cooling_system", "II", "צנרת, משאבת מים, מאוורר, תריס ומצנן (ניקוי)"),
    ("ac_system", "II", "מדחס, צנרת, ניקוי מעבה, ניקוז המאייד ורתמת PTC"),
    ("cabin_filter", "CR", "טיפול A: ניקוי; טיפול B: החלפה (לא יותר משנתיים)"),
]
write({
    "id": "xpeng-g6-2024-2026-ev",
    "make": "Xpeng", "make_he": "אקספנג", "model": "G6", "model_he": "G6",
    "generation": "G6", "years": [2024, 2026], "engines": ["EV (TZ230XY01F / TZ230XY01)"], "fuel": "electric",
    "importer": "פריסבי",
    "interval": {"km": 20000, "months": 12,
                 "note": "לפי ספר האחריות והתחזוקה האירופי של G6: טיפול כל 12 חודשים או 20,000 ק\"מ; הטור השני (טיפול מורחב) כל 24 חודשים או 40,000 ק\"מ"},
    "cycle_km": 40000,
    "services": grid(20000, 2, A),
    "long_interval": [
        {"item": "transmission_oil", "action": "replace", "every_km": 80000, "every_months": 48, "note": "שמן תיבת ההפחתה - כל 80,000 ק\"מ או 48 חודשים"},
        {"item": "coolant", "action": "replace", "every_km": 120000, "every_months": 72, "note": "נוזל קירור - כל 120,000 ק\"מ או 72 חודשים"},
        {"item": "wipers", "action": "replace", "every_km": 5000, "every_months": 3, "note": "פריט מומלץ לפי הצורך: להבי מגבים כל 3 חודשים או 5,000 ק\"מ"},
        {"item": "tires", "action": "inspect", "every_km": 5000, "every_months": 3, "note": "פריט מומלץ: בדיקת לחץ ובלאי לא אחיד כל 3 חודשים או 5,000 ק\"מ"},
    ],
    "specs": {"battery": "סוללת הנעה + מצבר 12V", "_note": "טיוטה - לפי מסמך אירופי, לא נבדק מול ספר היבואן"},
    "sources": [
        {"url": "https://s3.eu-central-1.amazonaws.com/datamotive-sulu-assets/xpeng-rotterdam/03/warranty-and-maintenance-manual-g6-for-eu.pdf",
         "kind": "manufacturer", "note": "Warranty and Maintenance Manual - XPENG G6 (for European Union), פרק 8 'Regular Maintenance', עמודי PDF 11-18 (אירופה, ק\"מ)"},
    ],
    "status": "draft",
    "notes": "אתר היבואן xpeng.co.il לא זמין מכאן (502) ולא נמצא ספר עברי, ולכן זו טיוטה לפי ספר האחריות והתחזוקה של G6 לאיחוד האירופי. טיפול A כל 20,000 ק\"מ/שנה וטיפול B כל 40,000 ק\"מ/שנתיים; בטיפול B מוחלפים נוזל הבלמים ומסנן המזגן. שמן תיבת ההפחתה ונוזל הקירור ב-long_interval. בתנאי שימוש קשים (אבק, חום מעל 40 מעלות, נסיעה בהרים, שימוש מסחרי) יש לטפל לעתים קרובות יותר.",
})
