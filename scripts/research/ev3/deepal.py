from lib import write
IMP = "מכשירי תנועה ומכוניות (2004)"
BOOKS = "https://www.changan.co.il/pages/%D7%A1%D7%A4%D7%A8%D7%99-%D7%A8%D7%9B%D7%91-%D7%95%D7%9B%D7%AA%D7%91-%D7%90%D7%97%D7%A8%D7%99%D7%95%D7%AA"

def svc(km, model):
    even = (km // 20000) % 2 == 0
    it = [
        {"item": "electrical_system", "action": "inspect", "note": "מכלול מנוע ההנעה: מחברים, ברגי הארקה וקיבוע, צנרת הקירור שלו וניקיון חיצוני"},
        {"item": "transmission_oil", "action": "inspect", "note": "דליפות שמן ממשטחי החיבור של המנוע ותיבת ההפחתה, אטמים ופקקים"},
        {"item": "hybrid_system", "action": "inspect",
         "note": "סוללת המתח הגבוה: נזק למעטפת, ברגי קיבוע, בדיקת בידוד והפרש מתחים בין התאים; ברגים, מחברים ומעטפת של רתמות המתח הגבוה"
                 + ("; כיוון/תיקון לפי הצורך" if model == "S07" else "")},
        {"item": "brake_pads", "action": "inspect", "note": "רפידות וקליפרים מלפנים ומאחור"},
        {"item": "brake_discs", "action": "inspect"},
        {"item": "brake_lines", "action": "inspect"},
    ]
    if model == "S07":
        it.append({"item": "brake_fluid", "action": "replace" if even else "inspect"})
    rot = km >= (40000 if model == "S05" else 60000)
    it.append({"item": "tires", "action": "inspect", "note": "מצב ולחץ אוויר (כיוון), חישוקים וברגי גלגלים"})
    if rot:
        it.append({"item": "tire_rotation", "action": "rotate", "note": "בטבלה מסומן R לצד בדיקה וכיוון בשורת הצמיגים; פורש כאן כהצלבה (ספר הנהג ממליץ על הצלבה כל 10,000 ק\"מ)" if model == "S05" else "בטבלה מסומן R לצד בדיקה וכיוון בשורת הצמיגים; פורש כאן כהצלבה"})
    it += [
        {"item": "body_underside", "action": "inspect", "note": "ברגים ואומים של המרכב והשלדה"},
        {"item": "steering", "action": "inspect", "note": "חופש והידוקים"},
    ]
    if model == "S07":
        it.append({"item": "coolant", "action": "replace" if km in (60000, 100000, 140000, 180000) else "inspect"})
    if even:
        it += [
            {"item": "lights", "action": "inspect", "note": "חיווט, מחברים ותאורה של אביזרי החשמל"},
            {"item": "ac_refrigerant", "action": "inspect", "note": "כמות גז המזגן"},
            {"item": "ac_system", "action": "inspect", "note": "מדחס, מייבש וצנרת המיזוג; ניקוי אבק מהמעבה ומהמאייד"},
            {"item": "cooling_system", "action": "inspect", "note": "מעגל נוזל הקירור של מערכת המיזוג"},
            {"item": "coolant_hoses", "action": "inspect", "note": "צנרת ואביזרי מערכת הקירור, כולל כיוון/הידוק"},
        ]
    else:
        it.append({"item": "ac_system", "action": "clean", "note": "ניקוי אבק מפני המעבה והמאייד"})
    it.append({"item": "cabin_filter", "action": "replace", "note": "מסנן המזגן (בטבלה: בדיקה/החלפה בכל טיפול)"})
    return {"km": km, "items": it}

COMMON_NOTE_COND = "בתנאי שימוש קשים (נסיעות קצרות רבות, דרכים משובשות, בוציות או מאובקות) יש להקדים בדיקות והחלפות."

write(dict(
    id="deepal-s05-2025-2026-ev", make="Deepal", make_he="דיפאל", model="S05", model_he="S05", generation="S05 EV",
    years=[2025, 2026], engines=["EV (XTDM67)"], fuel="electric", importer=IMP,
    interval={"km": 20000, "months": 12, "note": "לפי טבלת הטיפולים בחוברת האחריות והשירות של היבואן: כל 20,000 ק\"מ או 12 חודשים"},
    cycle_km=200000,
    services=[svc(k, "S05") for k in range(20000, 200001, 20000)],
    long_interval=[
        {"item": "transmission_oil", "action": "replace", "every_km": 60000, "every_months": 36,
         "note": "שמן תיבת ההפחתה של מנוע ההנעה האחורי (ובדגמי AWD גם של יחידת ההנעה הקדמית): כל 3 שנים או 60,000 ק\"מ"},
        {"item": "brake_fluid", "action": "replace", "every_km": 40000, "every_months": 48,
         "note": "נוזל בלמים: כל 4 שנים או 40,000 ק\"מ, המוקדם"},
        {"item": "coolant", "action": "replace", "every_km": 80000, "every_months": 36,
         "note": "נוזל קירור: כל 3 שנים או 80,000 ק\"מ, המוקדם"},
        {"item": "tire_rotation", "action": "rotate", "every_km": 10000,
         "note": "ספר הנהג ממליץ על הצלבת גלגלים כל 10,000 ק\"מ לאחר הטיפול הראשון"},
    ],
    specs={"tires": "225/60 R18 או 245/45 R20 (אין גלגל חלופי)",
           "tire_pressure": "2.9 בר מלפנים ומאחור (מצב נוחות ללא עומס: 2.7 בר)",
           "spare": "אין גלגל חלופי",
           "battery": "סוללת הנעה + מצבר 12V"},
    sources=[
        {"url": "https://cdn.shopify.com/s/files/1/0910/1656/0946/files/S05_2026.pdf?v=1783953305", "kind": "importer",
         "note": "חוברת אחריות ושירות Deepal S05 (מק\"ט CH 28982225, עדכון 01, 07/2026): טבלת טיפולים תקופתית עמ' 13-15 בקובץ"},
        {"url": "https://cdn.shopify.com/s/files/1/0910/1656/0946/files/S05_59c81f5e-04e7-4505-bde1-137c0f0f4874.pdf?v=1767000221", "kind": "importer",
         "note": "מדריך תפעול ושירות S05 בעברית: אותה טבלה בעמ' 354-355 בקובץ; הצלבת גלגלים עמ' 294; צמיגים ולחצים עמ' 347"},
        {"url": BOOKS, "kind": "importer", "note": "עמוד 'ספרי רכב וכתב אחריות' באתר צ'אנגן ישראל"},
    ],
    status="reviewed",
    notes="לפי טבלת הטיפולים בחוברת האחריות והשירות העברית של היבואן (07/2026) ובספר הנהג. טיפול כל 20,000 ק\"מ או שנה: בדיקות של מנוע ההנעה, סוללת המתח הגבוה, הבלמים, ההיגוי והצמיגים, ניקוי מעבה ומאייד והחלפת מסנן מזגן; בכל טיפול שני נבדקות גם מערכת המיזוג, גז המזגן וצנרת הקירור. "
          "שמן תיבת ההפחתה כל 3 שנים/60,000 ק\"מ, נוזל בלמים כל 4 שנים/40,000 ק\"מ ונוזל קירור כל 3 שנים/80,000 ק\"מ (ב-long_interval). " + COMMON_NOTE_COND,
))

write(dict(
    id="deepal-s07-2025-2026-ev", make="Deepal", make_he="דיפאל", model="S07", model_he="S07", generation="S07 EV",
    years=[2025, 2026], engines=["EV (XTDM16)"], fuel="electric", importer=IMP,
    interval={"km": 20000, "months": 12, "note": "לפי טבלת הטיפולים בחוברת האחריות והשירות של היבואן: כל 20,000 ק\"מ או 12 חודשים"},
    cycle_km=200000,
    services=[svc(k, "S07") for k in range(20000, 200001, 20000)],
    long_interval=[
        {"item": "transmission_oil", "action": "replace", "every_km": 60000, "every_months": 36,
         "note": "שמן תיבת ההפחתה של מנוע ההנעה: כל 3 שנים או 60,000 ק\"מ"},
    ],
    specs={"tires": "235/55 R19 או 255/45 R20 (אין גלגל חלופי)",
           "tire_pressure": "2.7 בר מלפנים ומאחור; בעומס מלא 2.9 בר מאחור",
           "spare": "אין גלגל חלופי",
           "battery": "סוללת הנעה + מצבר 12V"},
    sources=[
        {"url": "https://cdn.shopify.com/s/files/1/0910/1656/0946/files/2026.pdf?v=1783953306", "kind": "importer",
         "note": "חוברת אחריות ושירות Deepal S07 (מק\"ט CH 28981124, עדכון 01, 07/2026): טבלת טיפולים תקופתית עמ' 14-16 בקובץ"},
        {"url": "https://cdn.shopify.com/s/files/1/0910/1656/0946/files/DEEPAL_S07_ver1_WEB_3bde21a4-f1cd-48b7-933c-587f2ba36d36.pdf?v=1740909916", "kind": "importer",
         "note": "מדריך תפעול ושירות S07 בעברית: צמיגים, לחצים ובלמים עמ' 288"},
        {"url": BOOKS, "kind": "importer", "note": "עמוד 'ספרי רכב וכתב אחריות' באתר צ'אנגן ישראל"},
    ],
    status="reviewed",
    notes="לפי טבלת הטיפולים בחוברת האחריות והשירות העברית של היבואן ל-S07 (07/2026). טיפול כל 20,000 ק\"מ או שנה עם בדיקות של מנוע ההנעה, סוללת המתח הגבוה, הבלמים, ההיגוי והצמיגים, ניקוי מעבה ומאייד והחלפת מסנן מזגן. "
          "נוזל הבלמים מוחלף כל 40,000 ק\"מ; נוזל הקירור מוחלף לראשונה ב-60,000 ק\"מ ואחר כך כל 40,000 ק\"מ (100, 140, 180 אלף) - כפי שמופיע בטבלה; שמן תיבת ההפחתה כל 3 שנים או 60,000 ק\"מ. "
          "הצלבת גלגלים מסומנת בטבלה מ-60,000 ק\"מ. " + COMMON_NOTE_COND,
))
