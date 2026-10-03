from lib import write
BASE = "https://zeekr-israel.co.il/wp-content/uploads/"
MODELS = [
    ("zeekr-x-2024-2026-ev", "X", "X", "ZEEKR X", [2024, 2026], ["EV (TZ22)"],
     BASE + "2026/04/Zeeker-BX_HEB26022024.pdf", "ספר הוראות הפעלה ZEEKR X בעברית (BX, 26.02.2024), טבלת פריטי שירות עמ' 345-346 בקובץ (343-344 בספר)",
     [(BASE + "2026/05/ZEEKR-X-אנגלית-ארוך.pdf", "ZEEKR X owner's manual באנגלית מאתר היבואן: אותה טבלה בעמ' 306")]),
    ("zeekr-001-2024-2026-ev", "001", "001", "ZEEKR 001", [2024, 2026], ["EV (TZ22)"],
     BASE + "2026/04/Zeeker-001-DC1E-text-for-trans-Hebrew_012024.pdf", "ספר הוראות הפעלה ZEEKR 001 בעברית (DC1E, 01/2024), טבלת פריטי שירות עמ' 352 בקובץ (350 בספר)",
     [(BASE + "2026/05/ZEEKR-001-אנגלית-ארוך.pdf", "ZEEKR 001 owner's manual באנגלית מאתר היבואן: אותה טבלה בעמ' 307")]),
    ("zeekr-7x-2025-2026-ev", "7X", "7X", "ZEEKR 7X", [2025, 2026], ["EV (TZ23 / TZ235XYC01)"],
     BASE + "2026/04/Zeeker-7x_Hebrew_31072025.pdf", "ספר הוראות הפעלה ZEEKR 7X בעברית (31.07.2025), תוכנית אחזקה עמ' 420 בקובץ (418 בספר)", []),
]
for mid, model, model_he, gen, years, eng, url, note, extra in MODELS:
    cab_note = "מסנן המזגן: כל 24 חודשים" + ("" if model == "7X" else " או 40,000 ק\"מ")
    write(dict(
        id=mid, make="Zeekr", make_he="זיקר", model=model, model_he=model_he, generation=gen,
        years=years, engines=eng, fuel="electric", importer="גיאו מוביליטי (קבוצת יוניון)",
        interval={"km": 40000, "months": 24, "note": "לפי ספר הנהג העברי: טיפול ובדיקה כל 40,000 ק\"מ או 24 חודשים; מועד הטיפול מוצג גם בלוח המחוונים (תזכורת תחזוקה חכמה)"},
        cycle_km=40000,
        services=[{"km": 40000, "items": [
            {"item": "cabin_filter", "action": "replace", "note": cab_note},
            {"item": "transmission_oil", "action": "replace", "note": "שמן תיבת ההפחתה - כל 40,000 ק\"מ"},
        ]}],
        time_based=[
            {"item": "brake_fluid", "action": "replace", "months": 24, "note": "נוזל בלמים כל 24 חודשים (לפי זמן בלבד)"},
            {"item": "coolant", "action": "replace", "months": 48, "note": "נוזל קירור כל 48 חודשים (לפי זמן בלבד)"},
        ],
        specs={"battery": "סוללת הנעה + מצבר 12V"},
        sources=[{"url": url, "kind": "importer", "note": note}] + [{"url": u, "kind": "importer", "note": n} for u, n in extra],
        status="reviewed",
        notes="לפי ספר הנהג העברי שמפרסם היבואן. היצרן ממליץ על טיפול ובדיקה כל 40,000 ק\"מ או שנתיים; בטבלה ארבעה פריטים בלבד: נוזל בלמים כל שנתיים, "
              + cab_note.replace("מסנן המזגן: ", "מסנן מזגן ") + ", נוזל קירור כל 4 שנים ושמן תיבת ההפחתה כל 40,000 ק\"מ. "
              "בתנאי נהיגה קשים (נסיעות קצרות, אבק או חול, בלימות תכופות, הרים, חום או קור קיצוניים) המרווח הוא חצי מהזמן והמרחק. בדיקות נוספות לפי המלצת מרכז השירות.",
    ))
