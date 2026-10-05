from lib import *
cols = [20000 * i for i in range(1, 9)]
A = "I" * 8; RR = "R" * 8
rows = [
    ("engine_oil", RR), ("oil_filter", RR),
    ("cooling_system", A, "בדיקת מקרן ומעבה (לכלוך, עלים), צינורות ומחברים"),
    ("coolant", A, "השלמת מפלס בכל טיפול; בדיקת pH לפי long_interval"),
    ("exhaust", A, "צינורות פליטה ותומכים; בדיקת עשן סמיך"),
    ("air_filter", "-R-R-R-R"), ("fuel_filter", "-R-R-R-R", "מסנן סולר"),
    ("fuel_lines", A), ("adblue", "A" * 8, "מילוי תמיסת AdBlue בכל טיפול"),
    ("pedals", A, "דוושת בלם וידית בלם חניה"), ("parking_brake", A),
    ("brake_pads", A), ("brake_discs", A), ("brake_lines", A), ("brake_fluid", A),
    ("steering", A), ("cv_boots", A), ("suspension", A), ("tires", A),
    ("cabin_filter", "CRCRCRCR", "ניקוי בטיפולים האי-זוגיים, החלפה כל 40,000; מסנן פחמי (אם קיים) מוחלף בכל טיפול"),
    ("body_underside", A, "בדיקת קורוזיה ועיגון שטיח הנהג"),
    ("battery_12v", A), ("lights", A, "תאורה, צופר, מגבים ומתזים (בגיליון 2023)"),
    ("power_steering_fluid", A, "נוזל מערכת היגוי (בגיליון 2023)"),
]
write({
    "id": "toyota-proace-2017-2026-2.0-diesel", "make": "Toyota", "make_he": "טויוטה", "model": "Proace", "model_he": "פרואייס",
    "generation": "MDZ (K0, דור שני)", "years": [2017, 2026], "engines": ["2.0 BlueHDi diesel (DW10FC/DW10FE)"], "fuel": "diesel",
    "importer": "יוניון מוטורס",
    "interval": {"km": 20000, "months": 12, "note": "לפי לוח האחזקה של יוניון מוטורס: טיפול כל 20,000 ק\"מ או 12 חודשים, המוקדם מביניהם"},
    "cycle_km": 160000, "services": grid(cols, rows),
    "long_interval": [
        L("drive_belt", "replace", every_km=120000, every_months=72, note="רצועת הינע ומותחן: 120,000 ק\"מ או 72 חודשים"),
        L("timing_belt", "replace", every_km=140000, every_months=120, note="רצועת תזמון, מותחן ומשאבת מים: 140,000 ק\"מ או 120 חודשים"),
        L("coolant", "inspect", first_km=120000, first_months=48, then_every_km=20000, note="בדיקת pH של נוזל הקירור: לראשונה ב-120,000 ואחר כך בכל טיפול"),
        L("diagnostics", "inspect", first_km=160000, then_every_km=20000, note="בדיקת סתימות מסנן החלקיקים (DPF) במחשב: לראשונה ב-160,000 ואחר כך בכל טיפול"),
    ],
    "time_based": [{"item": "brake_fluid", "action": "replace", "months": 24, "note": "החלפה כל שנתיים ללא תלות בק\"מ"}],
    "specs": {"engine_oil": "0W-30 ACEA C2 (גיליון 2017); 5W-30 PSA B71 2297 (גיליון 2023)", "oil_capacity": "6 ליטר",
              "coolant": "Premium Long Life Coolant", "brake_fluid": "DOT 4", "fuel": "סולר",
              "timing": "רצועת תזמון, 140,000 ק\"מ או 10 שנים",
              "_note": "גיר ידני: ESSO/TOTAL 75W80, 2.6 ליטר; גיר אוטומטי: AW-1 / Special Oil AW2"},
    "sources": [
        {"url": "https://books.union-motors.co.il/app/api/files/432/download", "kind": "importer", "note": "לוח אחזקה 'פרואייס 2017' (26.7.2017), מנוע DW10FC/DW10FE: 8 עמודות של 20,000 ק\"מ עד 160,000, טבלת נוזלים. נקרא מהתמונה"},
        {"url": "https://books.union-motors.co.il/app/api/files/751/download", "kind": "importer", "note": "לוח אחזקה PROACE 2020 (MDZ342/362/642/662), אותה טבלה"},
        {"url": "https://books.union-motors.co.il/app/api/files/1132/download", "kind": "importer", "note": "לוח אחזקה ProAce MDZ (יולי 2023, DW10F): 11 עמודות של 20,000 ק\"מ עד 220,000 עם אותם מרווחים"},
    ],
    "status": "reviewed",
    "notes": "הועתק מלוחות האחזקה של יוניון מוטורס לפרואייס (מנוע דיזל 2.0 של קבוצת PSA). טיפול כל 20,000 ק\"מ או שנה; מסנן אוויר ומסנן סולר כל 40,000 ק\"מ או 4 שנים; רצועת אביזרים ב-120,000; רצועת תזמון עם משאבת מים ב-140,000 או 10 שנים; נוזל בלמים כל שנתיים; מילוי תוסף Eolys למסנן החלקיקים ב-80,000 וב-160,000. לוח 2023 מוסיף בדיקת מצבר, תאורה ונוזל היגוי ומגיע עד 220,000 ק\"מ.",
})
