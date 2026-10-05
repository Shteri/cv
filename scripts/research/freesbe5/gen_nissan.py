# Generator for Nissan schedules from the Israeli Carasso Motors (Freesbe) Nissan
# "warranty and service booklet" (Aug 2016), carz_warranty.pdf in this folder.
# Every mark below was transcribed with nparse.py (word coordinates) and checked
# against the rendered page images in img/nb_p*.png.
import json, os

OUT = '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/freesbe5'
BOOK = 'http://carz.co.il.s3.amazonaws.com/files/NewVehicle_Warranty.pdf'
CDN = 'https://www.nissan-cdn.net/content/dam/Nissan/israel/services/warrenty-pdf/NewVehicle_Warranty.pdf'
IMPORTER = 'פריסבי (קרסו מוטורס)'

R, I, ROT, DR, S, N = 'replace', 'inspect', 'rotate', 'drain', 'star', None

def book_src(pages):
    return {"url": BOOK, "kind": "importer",
            "note": "חוברת אחריות ושירות של קרסו מוטורס לרכבי ניסאן (מהדורת אוגוסט 2016, עותק של החוברת הישראלית שהועלה לאתר carz.co.il). "
                    "טבלת מועדי הטיפול לפי דגם בעמ' 18 בחוברת, סוגי שמן בעמ' 17, אחריות בעמ' 5-6; " + pages}

CDN_SRC = {"url": CDN, "kind": "importer",
           "note": "כתב האחריות לרכב חדש של ניסאן ישראל (2017) בתיקיית החוברות באתר ניסאן ישראל, יחד עם חוברות NT500/LEAF/GT-R מאותה סדרה (אוגוסט 2016). אין בו טבלת טיפולים; מאשר שמדובר בסדרת החוברות של היבואן"}

OIL_PETROL = 'בנזין: API SN בצמיגות 5W-30 (לפי טבלת השמנים בחוברת היבואן)'
OIL_MICRA = 'API SN בצמיגות 0W-30 (טבלת השמנים בחוברת היבואן מציינת את מיקרה, אלטימה ומקסימה בנפרד)'
OIL_DIESEL = 'דיזל עם מסנן חלקיקים: ACEA C4 בצמיגות 5W-30 (לפי טבלת השמנים בחוברת היבואן)'
WARRANTY = '3 שנים או 100,000 ק"מ, המוקדם (בשנתיים הראשונות ללא הגבלת ק"מ); צבע ושיתוך 3 שנים (חוברת 2016)'
WARRANTY_NV = '5 שנים או 160,000 ק"מ, המוקדם (בשנתיים הראשונות ללא הגבלת ק"מ); צבע ושיתוך 5 שנים (חוברת 2016, נבארה ו-NV200)'

SEVERE = ('בתנאי נסיעה קשים (דרכים מאובקות, נסיעות קצרות חוזרות, גרירה, עבודה ממושכת בסרק, חום או קור קיצוניים, לחות או אזורים הרריים, '
          'דרכים משובשות או מדבריות, בלימות תכופות, נהיגה מהירה ממושכת, מונית ורכב לימוד) החוברת מפנה לטיפולים תכופים יותר בתיאום עם מרכז השירות, בלי טבלה נפרדת. ')
TIMEBASIS = 'כשהנסועה השנתית נמוכה ממרווח הק"מ, הטיפולים נקבעים לפי הזמן (פעם בשנה). '

def build(rows, kms, notes_by_item=None):
    """rows: list of (item, marks list aligned with kms, note or None, drain_note)."""
    services = []
    for ci, km in enumerate(kms):
        items = []
        for row in rows:
            item, marks = row[0], row[1]
            note = row[2] if len(row) > 2 else None
            m = marks[ci]
            if m is None:
                continue
            if m == DR:
                e = {"item": item, "action": "clean", "note": "ניקוז מים ממסנן הסולר (בלי החלפה)"}
            elif m == S:
                continue  # star marks handled by long_interval + note
            else:
                e = {"item": item, "action": m}
                if note:
                    e["note"] = note
            items.append(e)
        services.append({"km": km, "items": items})
    return services

def write(d):
    with open(os.path.join(OUT, d['id'] + '.json'), 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print('wrote', d['id'])

def base(id_, model, model_he, gen, years, engines, fuel, km, months, cycle, services, long_, specs, sources, status, notes, inote):
    return {"id": id_, "make": "Nissan", "make_he": "ניסאן", "model": model, "model_he": model_he, "generation": gen,
            "years": years, "engines": engines, "fuel": fuel, "importer": IMPORTER,
            "interval": {"km": km, "months": months, "note": inote},
            "cycle_km": cycle, "services": services, "long_interval": long_, "time_based": [],
            "specs": specs, "sources": sources, "status": status, "notes": notes}

CAB10 = 'בנסועה שנתית של פחות מ-10,000 ק"מ: החלפה כל שנתיים'
CAB15 = 'בנסועה שנתית של פחות מ-15,000 ק"מ: החלפה כל שנתיים'
BRK = 'בדיקת הבלמים מלפנים ומאחור'

# ---------------- Micra K13 (book p.20, PDF p.21): 20,000 km / 12 months, 6 columns
k = [20000, 40000, 60000, 80000, 100000, 120000]
rows = [
    ("engine_oil", [R]*6), ("oil_filter", [R]*6),
    ("air_filter", [I, I, R, I, I, R]),
    ("cabin_filter", [N, R, N, R, N, R], CAB10),
    ("spark_plugs", [N, N, N, N, R, N]),
    ("brake_pads", [I]*6, BRK),
    ("tire_rotation", [ROT]*6),
    ("coolant", [I, I, I, I, R, R], 'לפי הערת השוליים: החלפה ראשונה ב-100,000 ק"מ או 5 שנים; הטבלה מסמנת החלפה גם ב-120,000'),
    ("brake_fluid", [I, R, I, R, I, R]),
    ("cvt_oil", [I, I, R, I, I, R], 'החלפה כל 60,000 ק"מ או 4 שנים, המוקדם'),
]
write(base("nissan-micra-2011-2019-1.2", "Micra", "מיקרה", "K13", [2011, 2019], ["1.2 (HR12DE)"], "petrol",
     20000, 12, 120000, build(rows, k),
     [{"item": "coolant", "action": "replace", "first_km": 100000, "first_months": 60, "then_every_km": 60000, "then_every_months": 48,
       "note": "הערת שוליים בטבלת היבואן: החלפה ראשונה ב-100,000 ק\"מ או 5 שנים ואחר כך כל 60,000 ק\"מ או 4 שנים"}],
     {"engine_oil": OIL_MICRA, "warranty": WARRANTY},
     [book_src("טבלת מיקרה K13 בעמ' 20 (עמ' 21 בקובץ)"), CDN_SRC], "reviewed",
     "לוח היבואן הישראלי (קרסו מוטורס) למיקרה החדשה K13 בבנזין: טיפול כל 20,000 ק\"מ או שנה. מצתים מוחלפים ב-100,000 ק\"מ; נוזל בלמים כל 40,000; "
     "מסנן אוויר כל 60,000; שמן CVT כל 60,000 ק\"מ או 4 שנים. " + TIMEBASIS + SEVERE + "לאחר הטיפול האחרון בטבלה ממשיכים באותה תדירות.",
     "טיפול כל 20,000 ק\"מ או שנה, המוקדם (לוח היבואן הישראלי)"))

# ---------------- Juke F15 2x4 (book p.21, PDF p.22): 30,000 km / 12 months
k = [30000, 60000, 90000, 120000, 150000, 180000]
rows = [
    ("engine_oil", [R]*6), ("oil_filter", [R]*6),
    ("air_filter", [I, R, I, R, I, R]),
    ("cabin_filter", [R]*6, CAB15),
    ("spark_plugs", [N, N, R, N, N, R]),
    ("brake_pads", [I]*6, BRK),
    ("tire_rotation", [ROT]*6),
    ("coolant", [I, I, R, I, R, I]),
    ("brake_fluid", [I, R, I, R, I, R]),
    ("cvt_oil", [I, I, R, I, I, R]),
]
write(base("nissan-juke-2010-2019-1.6", "Juke", "ג'וק", "F15", [2010, 2019], ["1.6 (HR16DE)"], "petrol",
     30000, 12, 180000, build(rows, k),
     [{"item": "coolant", "action": "replace", "first_km": 90000, "first_months": 60, "then_every_km": 60000, "then_every_months": 48,
       "note": "הערת שוליים בטבלת היבואן: החלפה ראשונה ב-90,000 ק\"מ או 5 שנים ואחר כך כל 60,000 ק\"מ או 4 שנים"}],
     {"engine_oil": OIL_PETROL, "warranty": WARRANTY},
     [book_src("טבלת ג'וק F15 בהנעה קדמית (2x4) בעמ' 21 (עמ' 22 בקובץ)"), CDN_SRC], "reviewed",
     "לוח היבואן הישראלי לג'וק F15 בהנעה קדמית (מנוע 1.6 בנזין, גיר CVT): טיפול כל 30,000 ק\"מ או שנה. מצתים, נוזל קירור ושמן CVT מוחלפים ב-90,000 ק\"מ; "
     "מסנן אוויר ונוזל בלמים כל 60,000; מסנן מזגן בכל טיפול. לג'וק 4x4 יש בחוברת טבלה נפרדת של 20,000 ק\"מ (כולל שמן סרן אחורי ותיבת העברה) והיא לא נכללת כאן. "
     + TIMEBASIS + SEVERE,
     "טיפול כל 30,000 ק\"מ או שנה, המוקדם (לוח היבואן הישראלי לג'וק 2x4)"))

# ---------------- Qashqai J11 / X-Trail T32 petrol (book p.22? no: p.23, PDF p.24): 20,000 / 12
k = [20000, 40000, 60000, 80000, 100000, 120000]
rows = [
    ("engine_oil", [R]*6), ("oil_filter", [R]*6),
    ("air_filter", [N, N, R, N, N, R]),
    ("coolant", [I, I, I, I, R, I]),
    ("spark_plugs", [N, N, N, R, N, N]),
    ("drive_belt", [N, N, N, R, N, N], 'סט רצועת מנוע'),
    ("brake_fluid", [N, R, N, R, N, R]),
    ("cabin_filter", [N, R, N, R, N, R]),
]
write(base("nissan-qashqai-2014-2019-1.2-turbo", "Qashqai", "קשקאי", "J11", [2014, 2019], ["1.2 DIG-T (HRA2DDT)", "1.2 TCe (H5F)"], "petrol",
     20000, 12, 120000, build(rows, k), [],
     {"engine_oil": OIL_PETROL, "warranty": WARRANTY},
     [book_src("טבלת קשקאי J11 / אקס-טרייל T32 בנזין בעמ' 23 (עמ' 24 בקובץ)"), CDN_SRC], "reviewed",
     "לוח היבואן הישראלי לקשקאי J11 בבנזין: טיפול כל 20,000 ק\"מ או שנה. מסנן אוויר כל 60,000; מצתים וסט רצועת מנוע ב-80,000; נוזל קירור ב-100,000; "
     "נוזל בלמים ומסנן מזגן כל 40,000. בטבלה זו אין שורות לבדיקת בלמים, סבב גלגלים ושמן CVT. " + TIMEBASIS + SEVERE,
     "טיפול כל 20,000 ק\"מ או שנה, המוקדם (לוח היבואן הישראלי)"))

# ---------------- Qashqai J11 / X-Trail T32 diesel (book p.24, PDF p.25): 30,000 / 12, 5 columns
k = [30000, 60000, 90000, 120000, 150000]
diesel_rows = [
    ("engine_oil", [R]*5), ("oil_filter", [R]*5),
    ("air_filter", [N, R, N, R, N]),
    ("coolant", [N, N, S, N, S]),
    ("brake_fluid", [N, R, N, R, N]),
    ("cabin_filter", [R]*5),
    ("drive_belt", [N, N, N, N, R], 'סט רצועת מנוע'),
    ("fuel_filter", [N, R, N, R, N]),
]
diesel_long = [{"item": "coolant", "action": "replace", "every_km": 90000, "every_months": 60,
                "note": "בטבלת היבואן נוזל הקירור מסומן בכוכבית (בעמודות 90,000 ו-150,000) עם הערה: כל 5 שנים או 90,000 ק\"מ, המוקדם"}]
diesel_notes = ("טיפול כל 30,000 ק\"מ או שנה. מסנן מזגן בכל טיפול; מסנן אוויר, מסנן סולר ונוזל בלמים כל 60,000; סט רצועת מנוע ב-150,000; "
                "נוזל קירור כל 5 שנים או 90,000 ק\"מ. " + TIMEBASIS + SEVERE)
DSRC = "טבלת קשקאי J11 / אקס-טרייל T32 דיזל בעמ' 24 (עמ' 25 בקובץ)"
DI = "טיפול כל 30,000 ק\"מ או שנה, המוקדם (לוח היבואן הישראלי לדגמי דיזל)"

write(base("nissan-qashqai-2014-2021-1.6-diesel", "Qashqai", "קשקאי", "J11", [2014, 2021], ["1.6 dCi (R9M)"], "diesel",
     30000, 12, 150000, build(diesel_rows, k), diesel_long, {"engine_oil": OIL_DIESEL, "warranty": WARRANTY},
     [book_src(DSRC), CDN_SRC], "reviewed", "לוח היבואן הישראלי לקשקאי J11 בדיזל: " + diesel_notes, DI))

write(base("nissan-x-trail-2014-2021-1.6-diesel", "X-Trail", "אקס-טרייל", "T32", [2014, 2021], ["1.6 dCi (R9M)"], "diesel",
     30000, 12, 150000, build(diesel_rows, k), diesel_long, {"engine_oil": OIL_DIESEL, "warranty": WARRANTY},
     [book_src(DSRC), CDN_SRC], "reviewed", "לוח היבואן הישראלי לאקס-טרייל T32 בדיזל: " + diesel_notes, DI))

write(base("nissan-qashqai-2014-2021-1.5-diesel", "Qashqai", "קשקאי", "J11", [2014, 2021], ["1.5 dCi (K9K)"], "diesel",
     30000, 12, 150000, build(diesel_rows, k), diesel_long, {"engine_oil": OIL_DIESEL, "warranty": WARRANTY},
     [book_src(DSRC), CDN_SRC], "draft",
     "טיוטה: הלוח הוא טבלת הדיזל של היבואן הישראלי לקשקאי J11 (חוברת 2016), אבל קשקאי 1.5 dCi נרשם בישראל רק מ-2019, אחרי מהדורת החוברת, "
     "ולא נמצאה מהדורה מאוחרת יותר. " + diesel_notes, DI))

write(base("nissan-x-trail-2019-2021-1.7-diesel", "X-Trail", "אקס-טרייל", "T32", [2017, 2021], ["1.7 dCi (R9N)", "2.0 dCi (M9R)"], "diesel",
     30000, 12, 150000, build(diesel_rows, k), diesel_long, {"engine_oil": OIL_DIESEL, "warranty": WARRANTY},
     [book_src(DSRC), CDN_SRC], "draft",
     "טיוטה: הלוח הוא טבלת הדיזל של היבואן הישראלי לאקס-טרייל T32 (חוברת אוגוסט 2016). מנועי 2.0 dCi (2017-2019) ו-1.7 dCi (2019-2021) נמכרו בישראל אחרי מהדורת החוברת "
     "ולא נמצאה מהדורה מאוחרת יותר, לכן הסטטוס נשאר טיוטה. " + diesel_notes, DI))

# ---------------- Note E12 (book p.25, PDF p.26): 20,000 / 12
k = [20000, 40000, 60000, 80000, 100000, 120000]
rows = [
    ("engine_oil", [R]*6), ("oil_filter", [R]*6),
    ("air_filter", [N, N, R, N, N, R]),
    ("coolant", [I, I, I, I, R, I]),
    ("spark_plugs", [N, N, R, N, N, R]),
    ("brake_fluid", [N, R, N, R, N, R]),
    ("cabin_filter", [N, R, N, R, N, R]),
]
write(base("nissan-note-2014-2017-1.2", "Note", "נוט", "E12", [2014, 2017], ["1.2 DIG-S (HR12DDR)"], "petrol",
     20000, 12, 120000, build(rows, k), [],
     {"engine_oil": OIL_PETROL, "warranty": WARRANTY},
     [book_src("טבלת נוט החדשה E12 בעמ' 25 (עמ' 26 בקובץ)"), CDN_SRC], "reviewed",
     "לוח היבואן הישראלי לנוט E12 בבנזין: טיפול כל 20,000 ק\"מ או שנה. מסנן אוויר ומצתים כל 60,000; נוזל בלמים ומסנן מזגן כל 40,000; נוזל קירור ב-100,000. "
     + TIMEBASIS + SEVERE,
     "טיפול כל 20,000 ק\"מ או שנה, המוקדם (לוח היבואן הישראלי)"))

# ---------------- Altima (book p.27, PDF p.28): 15,000 / 12, 8 columns
k = [15000*i for i in range(1, 9)]
rows = [
    ("engine_oil", [R]*8), ("oil_filter", [R]*8),
    ("air_filter", [I, R]*4),
    ("coolant", [N, N, N, N, N, S, N, N]),
    ("spark_plugs", [N, N, N, N, N, R, N, N]),
    ("brake_fluid", [N, R]*4),
    ("cabin_filter", [N, R]*4),
]
write(base("nissan-altima-2013-2019-2.5", "Altima", "אלטימה", "L33", [2013, 2019], ["2.5 (QR25DE)"], "petrol",
     15000, 12, 120000, build(rows, k),
     [{"item": "coolant", "action": "replace", "every_km": 90000, "every_months": 60,
       "note": "בטבלת היבואן נוזל הקירור מסומן בכוכבית בעמודת 90,000 עם הערה: כל 5 שנים או 90,000 ק\"מ, המוקדם"}],
     {"engine_oil": OIL_MICRA, "warranty": WARRANTY},
     [book_src("טבלת אלטימה בנזין בעמ' 27 (עמ' 28 בקובץ)"), CDN_SRC], "reviewed",
     "לוח היבואן הישראלי לאלטימה בבנזין (חוברת 2016, דור L33): טיפול כל 15,000 ק\"מ או שנה. מסנן אוויר, נוזל בלמים ומסנן מזגן כל 30,000; מצתים ב-90,000; "
     "נוזל קירור כל 5 שנים או 90,000 ק\"מ. אלטימה L34 (מנוע PR25, 2019 ואילך) לא מכוסה בחוברת. " + TIMEBASIS + SEVERE,
     "טיפול כל 15,000 ק\"מ או שנה, המוקדם (לוח היבואן הישראלי)"))

# ---------------- Maxima (book p.28, PDF p.29): 15,000 / 12
rows = [
    ("engine_oil", [R]*8), ("oil_filter", [R]*8),
    ("air_filter", [I, R]*4),
    ("coolant", [N, N, N, N, N, S, N, N]),
    ("brake_fluid", [I, R]*4),
    ("cabin_filter", [N, R]*4),
    ("spark_plugs", [N, N, N, N, N, R, N, N]),
]
write(base("nissan-maxima-2014-2021-3.5", "Maxima", "מקסימה", "A36", [2014, 2021], ["3.5 V6 (VQ35DE)"], "petrol",
     15000, 12, 120000, build(rows, k),
     [{"item": "coolant", "action": "replace", "every_km": 90000, "every_months": 60,
       "note": "בטבלת היבואן נוזל הקירור מסומן בכוכבית בעמודת 90,000 עם הערה: כל 5 שנים או 90,000 ק\"מ, המוקדם"}],
     {"engine_oil": OIL_MICRA, "warranty": WARRANTY},
     [book_src("טבלת מקסימה בנזין בעמ' 28 (עמ' 29 בקובץ)"), CDN_SRC], "reviewed",
     "לוח היבואן הישראלי למקסימה בבנזין (חוברת 2016): טיפול כל 15,000 ק\"מ או שנה. מסנן אוויר, נוזל בלמים ומסנן מזגן כל 30,000 (בטיפולים שביניהם בדיקת נוזל בלמים); "
     "מצתים ב-90,000; נוזל קירור כל 5 שנים או 90,000 ק\"מ. החוברת לא מפרטת דור; היא חלה על המקסימה שנמכרה בזמן הוצאתה (A36, מ-2016), ורכבי 2014-2015 משויכים אליה לפי הדגם. "
     + TIMEBASIS + SEVERE,
     "טיפול כל 15,000 ק\"מ או שנה, המוקדם (לוח היבואן הישראלי)"))

# ---------------- Navara D40 / Pathfinder R51 diesel (book p.32, PDF p.33): 20,000 / 12
k = [20000, 40000, 60000, 80000, 100000, 120000]
rows = [
    ("engine_oil", [R]*6), ("oil_filter", [R]*6),
    ("air_filter", [I, R]*3),
    ("cabin_filter", [R]*6, CAB10),
    ("fuel_filter", [DR, DR, R, DR, DR, R]),
    ("brake_pads", [I]*6, BRK),
    ("parking_brake", [I]*6),
    ("tire_rotation", [ROT]*6),
    ("coolant", [I, I, I, I, R, I]),
    ("brake_fluid", [I, R]*3),
    ("transmission_oil", [I, R]*3, 'בגיר אוטומטי; בבדיקה: נזילות'),
    ("differential_oil", [I, I, R, I, I, R], 'סרן קדמי ואחורי'),
    ("transfer_case_oil", [I]*6),
]
write(base("nissan-navara-pathfinder-2006-2015-2.5-diesel", "Navara / Pathfinder", "נבארה / פאת'פיינדר", "D40 / R51", [2006, 2015],
     ["2.5 dCi (YD25DDTi)"], "diesel", 20000, 12, 120000, build(rows, k),
     [{"item": "coolant", "action": "replace", "first_km": 100000, "first_months": 48, "then_every_km": 60000, "then_every_months": 36,
       "note": "הערת שוליים בטבלת היבואן: החלפה ראשונה ב-100,000 ק\"מ או 4 שנים ואחר כך כל 60,000 ק\"מ או 3 שנים"}],
     {"engine_oil": OIL_DIESEL, "warranty": WARRANTY_NV},
     [book_src("טבלת נבארה D40 / פאת'פיינדר R51 דיזל בעמ' 32 (עמ' 33 בקובץ)"), CDN_SRC], "reviewed",
     "לוח היבואן הישראלי לנבארה D40 ולפאת'פיינדר R51 בדיזל: טיפול כל 20,000 ק\"מ או שנה. מסנן סולר: ניקוז מים בכל טיפול והחלפה כל 60,000; מסנן אוויר, נוזל בלמים ושמן גיר אוטומטי כל 40,000; "
     "שמן סרן קדמי ואחורי כל 60,000; שמן תיבת העברה נבדק בכל טיפול. החוברת היא מהדורת 2016, ורכבי 2006-2015 משויכים לפי הדגם. " + TIMEBASIS + SEVERE,
     "טיפול כל 20,000 ק\"מ או שנה, המוקדם (לוח היבואן הישראלי)"))

# ---------------- NV200 M20 diesel, without tow hook (book p.33, PDF p.34): 30,000 / 12
k = [30000, 60000, 90000, 120000, 150000]
rows = [
    ("engine_oil", [R]*5), ("oil_filter", [R]*5),
    ("air_filter", [I, R, I, R, I]),
    ("cabin_filter", [R]*5, CAB15),
    ("fuel_filter", [DR, R, DR, R, DR]),
    ("brake_pads", [I]*5, BRK),
    ("tire_rotation", [ROT]*5),
    ("coolant", [I, I, I, I, R], 'לפי הערת השוליים ההחלפה הראשונה ב-90,000 ק"מ או 5 שנים (ראו מרווח ארוך); הטבלה מסמנת החלפה ב-150,000'),
    ("brake_fluid", [I, R, I, R, I]),
    ("manual_gearbox_oil", [I]*5),
    ("timing_belt", [N, N, N, N, R], 'רצועת תזמון ומותח: כל 150,000 ק"מ או 5 שנים, המוקדם'),
]
write(base("nissan-nv200-2012-2019-1.5-diesel", "NV200", "NV200", "M20", [2012, 2019], ["1.5 dCi (K9K)"], "diesel",
     30000, 12, 150000, build(rows, k),
     [{"item": "coolant", "action": "replace", "first_km": 90000, "first_months": 60, "then_every_km": 60000, "then_every_months": 48,
       "note": "הערת שוליים בטבלת היבואן: החלפה ראשונה ב-90,000 ק\"מ או 5 שנים ואחר כך כל 60,000 ק\"מ או 4 שנים"},
      {"item": "timing_belt", "action": "replace", "every_km": 150000, "every_months": 60,
       "note": "רצועת תזמון ומותח: כל 150,000 ק\"מ או 5 שנים, המוקדם (הערת שוליים בטבלה)"}],
     {"engine_oil": OIL_DIESEL, "warranty": WARRANTY_NV},
     [book_src("טבלאות NV200 M20 בעמ' 33-34 (עמ' 34-35 בקובץ); הלוח כאן הוא הטבלה לרכב ללא וו גרירה"), CDN_SRC], "reviewed",
     "לוח היבואן הישראלי ל-NV200 דיזל ללא וו גרירה: טיפול כל 30,000 ק\"מ או שנה; מסנן מזגן בכל טיפול; מסנן אוויר, מסנן סולר ונוזל בלמים כל 60,000; "
     "רצועת תזמון ומותח כל 150,000 ק\"מ או 5 שנים. לרכב עם וו גרירה החוברת קובעת טבלה נפרדת: טיפול כל 15,000 ק\"מ או שנה, עם החלפת מסנן אוויר, נוזל בלמים ומסנן סולר ב-60,000 "
     "ומסנן מזגן ב-30,000/60,000/90,000. " + TIMEBASIS + SEVERE,
     "טיפול כל 30,000 ק\"מ או שנה, המוקדם (רכב ללא וו גרירה; עם וו גרירה כל 15,000 ק\"מ)"))

# ---- corroborating Israeli brochure sources (old versions still cached on www.nissan-cdn.net)
B = 'https://www.nissan-cdn.net/content/dam/Nissan/israel/brochures/'
BRO = {
 'nissan-juke-2010-2019-1.6': ('Nissan-Juke-Brochure.pdf', 'ג\'וק HR16DE 2x4: מרווח טיפולים 30,000 ק"מ או 12 חודשים'),
 'nissan-qashqai-2014-2019-1.2-turbo': ('Nissan-New-Qashqai-Brochure.pdf', 'קשקאי 1.2 טורבו בנזין (HRA2): מרווח טיפולים 20,000 ק"מ או שנה; 1.6 דיזל: 30,000 ק"מ או שנה'),
 'nissan-qashqai-2014-2021-1.6-diesel': ('Nissan-Qashqai-Brochure.pdf', 'קשקאי 1.6 דיזל (R9M): מרווח טיפולים 30,000 ק"מ או שנה'),
 'nissan-note-2014-2017-1.2': ('Nissan-Note-Brochure.pdf', 'נוט HR12DDR: מרווח טיפולים 20,000 ק"מ או שנה'),
 'nissan-nv200-2012-2019-1.5-diesel': ('Nissan-NV200-Brochure.pdf', 'NV200 K9K: מרווח טיפולים 30,000 ק"מ או שנה'),
 'nissan-altima-2013-2019-2.5': ('Nissan-Altima-Brochure.pdf', 'אלטימה QR25DE: מרווח טיפולים 15,000 ק"מ או שנה'),
 'nissan-maxima-2014-2021-3.5': ('Nissan-Maxima-Brochure.pdf', 'מקסימה VQ35DE: מרווח טיפולים 15 (אלף) ק"מ או שנה'),
}
for i, (f, n) in BRO.items():
    p = os.path.join(OUT, i + '.json')
    d = json.load(open(p, encoding='utf-8'))
    if not any(s['url'] == B + f for s in d['sources']):
        d['sources'].append({"url": B + f, "kind": "importer", "note": "קטלוג מפרט טכני של ניסאן ישראל (גרסה ישנה במטמון של www.nissan-cdn.net), מאשר את המרווח: " + n})
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('brochure sources added')
