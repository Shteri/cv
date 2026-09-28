# Generates VAG schedule files + registry rules into staging/vag
import json, os, collections

OUT = '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/vag'
REG = json.load(open('/home/user/cv/data/sources/registry-counts.json'))
IMP = "צ'מפיון מוטורס"

# ---------------------------------------------------------------- sources
SRC = {
 'CH': {"url": "https://www.championmotors.co.il/service-routine/", "kind": "importer",
        "note": "שגרת טיפולים תקופתיים של צ'מפיון מוטורס, טבלאות לפי נפח וסוג מנוע (15,000 עד 120,000 ק\"מ). הדף חסום לבוטים; נקרא בדפדפן אמיתי (Playwright) ב-28.9.2026 והטבלאות פוענחו מקוד הדף"},
 'SK_OM': {"url": "https://www.manualslib.com/manual/1260581/Skoda-Kodiaq.html?page=275", "kind": "manufacturer",
        "note": "ספר נהג סקודה (קודיאק, אנגלית), פרק מרווחי שירות: במרווח קבוע QI4 החלפת שמן כל 15,000 ק\"מ או שנה; נוזל בלמים ראשון אחרי 3 שנים ואז כל שנתיים, בכפוף לשונות בין מדינות"},
 'AU': {"url": "https://www.skoda.com.au/_doc/987d9c66-f652-44dd-a721-dea7aec49440", "kind": "manufacturer",
        "note": "תנאי חבילות שירות של סקודה אוסטרליה: מרווח שירות 15,000 ק\"מ או 12 חודשים"},
 'OCT3': {"url": "https://vwts.ru/skoda/octavia3/skoda-octavia-3-a7-maintenance-eng.pdf", "kind": "manufacturer",
        "note": "Skoda Octavia III Maintenance, מהדורה 03.2020 (מדריך מוסך של היצרן, העתק באתר צד שלישי): עמ' 22-34 טבלאות עבודה לפי זמן/ק\"מ עד שנת דגם 2016 ומשנת דגם 2017, עמ' 33-36 מרווחי שירות, עמ' 40 רשימת 'מדינות מאובקות' שכוללת את ישראל, עמ' 41 'מדינות טרופיות' (ישראל)"},
 'KOD': {"url": "https://vwts.ru/skoda/kodiaq/skoda-kodiaq-maintenance-eng.pdf", "kind": "manufacturer",
        "note": "Skoda Kodiaq Maintenance, מהדורה 05.2019: עמ' 20-23 עבודות נוספות, עמודה 'מדינות מאובקות' (ישראל ברשימה בעמ' 28), קודי מנוע בעמ' 36-38"},
 'OCT4': {"url": "https://www.manualslib.com/manual/3050537/Skoda-Octavia-Iv-2020.html?page=26", "kind": "manufacturer",
        "note": "Skoda Octavia IV Maintenance, מהדורה 12.2020 (manualslib): עמ' 20-22 של המדריך (עמודי אתר 26-28) עבודות נוספות ועמודת מדינות מאובקות; ישראל ברשימה (עמוד אתר 35); קודי מנוע DPCA/DLAA/DFYA/DNPA/DGEA בעמ' 35-36"},
 'RAPID': {"url": "https://www.manualslib.com/manual/1655019/Skoda-Rapid-Nh-2013.html?page=26", "kind": "manufacturer",
        "note": "Skoda Rapid NH Maintenance, מהדורה 06.2018 (manualslib): עמודי אתר 21-31 עבודות עד שנת דגם 2016 ומשנת דגם 2017, עמודי אתר 36-38 ישראל ברשימת המדינות המאובקות, עמודי אתר 51-57 קודי מנוע (CBZ, CAX, CJZ, CZC, CHZ, DKR)"},
 'FAB3': {"url": "https://vwts.ru/skoda/fabia3/skoda-fabia-3-maintenance-eng.pdf", "kind": "manufacturer",
        "note": "Skoda Fabia III Maintenance, מהדורה 04.2020: עמ' 23-32 טבלאות עד 2016 ומ-2017, ישראל ברשימת המדינות המאובקות (עמ' 37)"},
 'GOLF7': {"url": "https://vwts.ru/vw/g7/vw-golf-7-maintenance-eng.pdf", "kind": "manufacturer",
        "note": "VW Golf 7 Maintenance, מהדורה 04.2021: עמ' 25-31 טבלאות מרווחים (עמודה 'מדינות עם אבק רב' ו'שווקים מחוץ לאירופה'), עמ' 39 ו-42 ישראל ברשימות 'אקלים חם' ו'אבק רב'; טבלת מנועים עמ' 1-17 (סוג הנעת גל זיזים)"},
 'LEON3': {"url": "https://vwts.ru/seat/leon_5f/seat-leon-3-maintenance-eng.pdf", "kind": "manufacturer",
        "note": "SEAT Leon 3 Maintenance, מהדורה 07.2018: עמ' 8-13 טבלאות שירות, ישראל ברשימת 'מדינות עם אבק רב' (עמ' 13) ו'מדינות חמות' (עמ' 16)"},
 'TIG1': {"url": "https://vwts.ru/vw/tiguan/vw-tiguan-2008-maintenance-eng.pdf", "kind": "manufacturer",
        "note": "VW Tiguan 2008 Maintenance, מהדורה 03.2021: עמ' 15-21 טבלאות (אבק רב, מחוץ לאירופה), רשימת מנועים עם סוג הנעה (שרשרת/רצועה) בעמ' 1-4"},
 'PASSAT7': {"url": "https://vwts.ru/vw/b7/vw-passat-b7-maintenance-eng.pdf", "kind": "manufacturer",
        "note": "VW Passat B7 Maintenance, מהדורה 01.2019: עמ' 12-20 טבלאות מרווחים; מצתים 90,000/6 שנים למנועי CDAA/CDAB/CCZB; ישראל ברשימות 'אקלים חם' ו'אבק רב' (עמ' 29-30)"},
 'POLO': {"url": "https://www.manualslib.com/manual/3717022/Volkswagen-Polo-2018.html?page=18", "kind": "manufacturer",
        "note": "VW Polo 2018 Maintenance, מהדורה 10.2021 (manualslib): טבלאות מסנן אוויר/מזגן/רצועות/מצתים/נוזל בלמים ו-DSG, עמודי אתר 17-29"},
 'GOLF5': {"url": "https://vwts.ru/vw/g5/golf_2004_golf_plus_2005_maintenance_eng.pdf", "kind": "manufacturer",
        "note": "VW Golf 5 / Golf Plus Maintenance, מהדורה 11.2009 (לפני הוספת טבלאות 'אבק רב'): עמ' 11-28; רצועת תזמון 1.6 BSE ו-1.4 BUD בלי החלפה קבועה (בדיקה מ-90,000 ואז כל 30,000); ישראל ברשימת 'אקלים חם' (עמ' 44)"},
 'VWTS_ENG': {"url": "https://vwts.ru/petrol-engine-vw-audi-skoda-repair-manual.html", "kind": "other",
        "note": "אינדקס ספרי תיקון מנועים של קבוצת פולקסווגן לפי קודי מנוע (לשיוך קוד מנוע לנפח ומשפחה, למשל CHZ/DKR/DLA/DUS = 1.0 TSI, DAD/DPC/DFY/DXD = 1.5 TSI, CBZ = 1.2 TSI EA111, CAX = 1.4 TSI EA111, CGGB = 1.4 MPI עם רצועה)"},
 'VWTS_DSL': {"url": "https://vwts.ru/diesel-engine-vw-audi-skoda-repair-manual.html", "kind": "other",
        "note": "אינדקס ספרי תיקון מנועי דיזל של קבוצת פולקסווגן לפי קודי מנוע"},
 'BOOKS': {"url": "https://books.championmotors.co.il/cars/", "kind": "importer",
        "note": "תקצירי הוראות השימוש של צ'מפיון (FlippingBook) לכל הדגמים; אין בהם טבלת טיפולים"},
}

SRC.update({
 'T5': {"url": "https://vwts.ru/vw/t5/vw-t5-maintenance-eng.pdf", "kind": "manufacturer",
        "note": "VW Transporter 2004/2010 Maintenance, מהדורה 09.2018: עמ' 9-18 מרווחים (דיזל 2010 ואילך: החלפת שמן קבועה כל 20,000 ק\"מ או שנה), עמ' 37-41 עבודות לפי זמן/ק\"מ עד 2009 ומ-2010 (כולל שורות 'באזורים מאובקים'), עמ' 44 ישראל ברשימת המדינות המאובקות; עמ' 14 ישראל בעמודת דלק תקני (פחות מ-500 ppm גופרית)"},
 'T6': {"url": "https://vwts.ru/vw/t6/vw-t6-maintenance-eng.pdf", "kind": "manufacturer",
        "note": "VW Transporter 2016 Maintenance, מהדורה 10.2018: עמ' 6-7 מרווחים (QI5 החלפת שמן קבועה כל 20,000 ק\"מ או שנה, בדיקה לדיזל כל 40,000), עמ' 14-15 עבודות לפי זמן/ק\"מ, עמ' 17-18 ישראל ברשימת המדינות המאובקות"},
 'CADDY3': {"url": "https://vwts.ru/vw/caddy3_2c/vw-caddy-3-maintenance-eng.pdf", "kind": "manufacturer",
        "note": "VW Caddy 2004/2011 Maintenance, מהדורה 09.2018: עמ' 9-11 מרווחים, עמ' 38-41 עבודות לפי זמן/ק\"מ, עמ' 42-43 ישראל ברשימת המדינות המאובקות"},
 'CADDY4': {"url": "https://vwts.ru/vw/caddy4/vw-caddy-4-maintenance-eng.pdf", "kind": "manufacturer",
        "note": "VW Caddy 2016 Maintenance, מהדורה 12.2018: עמ' 8 מרווחים (QI4 15,000 ק\"מ או שנה, בדיקה אחרי 30,000/שנתיים ואז כל 30,000/שנה), עמ' 15-16 עבודות לפי זמן/ק\"מ כולל שורות 'באזורים מאובקים', עמ' 17-18 ישראל ברשימת המדינות המאובקות"},
})

# ---------------------------------------------------------------- building blocks
def it(item, action='inspect', note=None):
    d = {"item": item, "action": action}
    if note: d["note"] = note
    return d

INSP30 = ['battery_12v', 'lights', 'wipers', 'tires', 'brake_lines', 'cooling_system', 'cv_boots', 'suspension']
INSP60 = ['steering', 'exhaust', 'body_underside']

def grid(step=15000, cycle=120000):
    return list(range(step, cycle + 1, step))

def assemble(rows, step=15000, cycle=120000, inspections=True):
    """rows: list of (predicate(km)->bool, item dict)"""
    services = []
    for km in grid(step, cycle):
        items = []
        for pred, d in rows:
            if pred(km):
                items.append(dict(d))
        if inspections:
            if km % 30000 == 0:
                items += [it(x) for x in INSP30]
            if km % 60000 == 0:
                items += [it(x) for x in INSP60]
        # de-duplicate item+action keeping first note; drop 'inspect' when the same item is replaced
        repl = {d['item'] for d in items if d['action'] == 'replace'}
        items = [d for d in items if not (d['action'] == 'inspect' and d['item'] in repl)]
        seen = set(); out = []
        for d in items:
            k = (d['item'], d['action'])
            if k in seen: continue
            seen.add(k); out.append(d)
        services.append({"km": km, "items": out})
    return services

every = lambda n: (lambda km: km % n == 0)
at = lambda *ks: (lambda km: km in ks)

OIL = [(every(15000), it('engine_oil', 'replace')), (every(15000), it('oil_filter', 'replace'))]
BRAKES_CH = [(every(15000), it('brake_pads', 'inspect', 'קדמיות ואחוריות, כולל מצב הדיסקים')), (every(15000), it('brake_discs', 'inspect'))]
BRAKES_FAC = [(every(15000), it('brake_pads', 'inspect', 'עובי רפידות ומצב דיסקים נבדקים בכל טיפול שמן')), (every(15000), it('brake_discs', 'inspect'))]

# ---------------------------------------------------------------- templates
def T_CH_SMALL(o):
    """Champion tables '1.0 ל' בנזין' and '1.5 ל' בנזין' (identical apart from the 1.5-only rows)."""
    has15 = o.get('has15', True); has10 = o.get('has10', True)
    rows = OIL + BRAKES_CH + [
        (every(30000), it('air_filter', 'replace', 'או כל שנתיים, המוקדם')),
        (every(30000), it('cabin_filter', 'replace', 'או כל שנה, המוקדם')),
        (every(60000), it('spark_plugs', 'replace', 'או כל 4 שנים, המוקדם')),
        (every(60000), it('drive_belt', 'replace', 'רצועת אביזרים' + (' (במנועי 1.5 עם מערכת 48 וולט מוחלף גם המותחן)' if has15 else ''))),
        (at(120000), it('timing_belt', 'replace', 'רצועת תזמון עם מותחן וגלגלת סרק, וגם רצועת השיניים של משאבת המים')),
    ]
    if has15:
        rows.append((at(120000), it('dct_oil', 'replace', 'רק בתיבת DSG רטובה 7 הילוכים (DQ381); בתיבת DSG יבשה (DQ200) היבואן לא מציין החלפה')))
    li = [
        {"item": "brake_fluid", "action": "replace", "every_months": 24, "note": "לפי זמן בלבד, כל שנתיים"},
        {"item": "cabin_filter", "action": "replace", "every_months": 12, "note": "אם לא הגיע ל-30,000 ק\"מ בתוך שנה"},
        {"item": "air_filter", "action": "replace", "every_months": 24},
        {"item": "spark_plugs", "action": "replace", "every_months": 48},
    ]
    notes = ("הלוח הועתק מטבלאות שגרת הטיפולים של צ'מפיון מוטורס לפי נפח מנוע: "
             + ("'1.0 ל' בנזין'" if has10 else '') + (" ו-" if has10 and has15 else '') + ("'1.5 ל' בנזין'" if has15 else '')
             + ". שתי הטבלאות זהות פרט לשמן תיבת DSG רטובה (DQ381) ב-120,000 ולמותחן רצועת האביזרים במנועי 48 וולט, שקיימים רק בטבלת ה-1.5. "
             "היבואן מציין שהטבלה כללית לדגמים נפוצים מהשנים האחרונות ואינה מחליפה לוח לרכב ספציפי. "
             "החלפת מסנני אוויר ומזגן כל 30,000 ק\"מ, רצועת אביזרים כל 60,000 ורצועת תזמון ב-120,000 תואמות את עמודת 'מדינות מאובקות' בטבלאות היצרן (ישראל ברשימה). "
             "בדיקות בכל 30,000 ק\"מ (מצבר, תאורה, מגבים, צמיגים, מערכת בלמים, קירור, גומיות ציריות, בולמים) ובכל 60,000 (היגוי, פליטה, תחתית) הוספו מתוך היקף הבדיקה (Inspection) במדריכי היצרן ואינן מופיעות בטבלת היבואן.")
    return dict(rows=rows, li=li, notes=notes, srcs=['CH', 'SK_OM', 'OCT4', 'KOD', 'VWTS_ENG'],
                interval_note="לפי טבלת צ'מפיון: טיפול כל 15,000 ק\"מ. תקרת הזמן (שנה) לקוחה ממרווח השירות הקבוע QI4 של היצרן", status='reviewed')

def T_CH_20(o):
    brand = o.get('brand', 'vw')
    haldex_m = 36 if brand in ('audi', 'cupra', 'seat') else 24
    rows = OIL + BRAKES_CH + [
        (every(30000), it('air_filter', 'replace', 'או כל שנתיים, המוקדם')),
        (every(30000), it('cabin_filter', 'replace', 'או כל שנה, המוקדם')),
        (every(60000), it('spark_plugs', 'replace', 'או כל 4 שנים, המוקדם')),
        (every(60000), it('brake_fluid', 'replace', 'בטבלת ה-2.0 של היבואן מסומן ב-60,000 וב-120,000')),
        (at(120000), it('dct_oil', 'replace', 'שמן תיבת הילוכים לפי טבלת היבואן; בטבלאות היצרן DSG רטובה 6 הילוכים (02E/0D9) ו-DQ500 (0DL/0BH) כל 60,000, DQ381 (0GC) כל 120,000')),
    ]
    li = [
        {"item": "differential_oil", "action": "replace", "every_months": haldex_m,
         "note": "שמן מצמד ההנעה הכפולה (הלדקס), רק בגרסאות 4x4. היבואן: פולקסווגן וסקודה כל שנתיים, קופרה ואאודי כל 3 שנים" + ("; סיאט לא מוזכרת, לפי ספר היצרן של לאון כל 3 שנים" if brand == 'seat' else '')},
        {"item": "differential_oil", "action": "replace", "every_months": 24,
         "note": "שמן מצמד נעילת הדיפרנציאל הקדמי, רק ברכב שמצויד בה (בעיקר גרסאות ספורט)"},
        {"item": "brake_fluid", "action": "replace", "every_months": 24, "note": "טבלאות היצרן לשווקים מחוץ לאירופה במרווח קבוע: כל שנתיים"},
        {"item": "cabin_filter", "action": "replace", "every_months": 12},
        {"item": "air_filter", "action": "replace", "every_months": 24},
        {"item": "spark_plugs", "action": "replace", "every_months": 48},
    ]
    notes = ("הלוח הועתק מטבלת '2.0 ל' בנזין' בשגרת הטיפולים של צ'מפיון מוטורס (מנועי 2.0 TSI/TFSI עם שרשרת תזמון; אין שורת רצועת תזמון). "
             "בטבלה זו נוזל הבלמים מסומן ב-60,000 וב-120,000; טבלאות היצרן לשוק מחוץ לאירופה קובעות גם החלפה כל שנתיים, ולכן נוספה גם שורת זמן. "
             "בטבלת ה-2.0 של היבואן אין רצועת אביזרים; בטבלאות היצרן למדינות מאובקות רצועה זו מוחלפת כל 60,000 ק\"מ, כדאי לוודא במוסך. "
             "שמן הלדקס ונעילת הדיפרנציאל רלוונטיים רק לרכב שמצויד בהם. "
             "בדיקות בכל 30,000/60,000 ק\"מ נוספו מהיקף הבדיקה במדריכי היצרן.")
    return dict(rows=rows, li=li, notes=notes, srcs=['CH', 'SK_OM', 'KOD', 'VWTS_ENG'],
                interval_note="לפי טבלת צ'מפיון: טיפול כל 15,000 ק\"מ; תקרת שנה לפי מרווח QI4 של היצרן", status=o.get('status', 'reviewed'))

def T_CH_D20(o):
    rows = OIL[:1] + [(every(15000), it('oil_filter', 'replace'))] + BRAKES_CH + [
        (every(30000), it('air_filter', 'replace')),
        (every(30000), it('cabin_filter', 'replace', 'או כל שנה, המוקדם')),
        (every(60000), it('drive_belt', 'replace', 'רצועת אביזרים')),
        (at(120000), it('timing_belt', 'replace', 'רצועת תזמון')),
        (at(120000), it('dct_oil', 'replace', 'רק בתיבת DSG רטובה 7 הילוכים (DQ381)')),
    ]
    li = [
        {"item": "fuel_filter", "action": "replace", "every_km": 90000, "note": "מסנן סולר; בטבלת היבואן מסומן ב-90,000"},
        {"item": "differential_oil", "action": "replace", "every_months": 24, "note": "שמן מצמד ההנעה הכפולה (הלדקס), רק בגרסאות 4x4"},
        {"item": "brake_fluid", "action": "replace", "every_months": 24},
        {"item": "cabin_filter", "action": "replace", "every_months": 12},
    ]
    notes = ("הלוח הועתק מטבלת '2.0 ל' דיזל' בשגרת הטיפולים של צ'מפיון מוטורס (מנועי 2.0 TDI ממשפחת EA288). "
             "בטבלה המקורית חסר סימון למסנן השמן ב-105,000; כאן הוא מוחלף בכל החלפת שמן כמו בכל טבלאות היצרן. "
             "מסנן סולר ב-90,000 ורצועת תזמון ב-120,000 תואמים גם את טבלאות היצרן למדינות מאובקות. "
             "בדיקות בכל 30,000/60,000 ק\"מ נוספו מהיקף הבדיקה במדריכי היצרן.")
    return dict(rows=rows, li=li, notes=notes, srcs=['CH', 'SK_OM', 'KOD', 'OCT3', 'VWTS_DSL'],
                interval_note="לפי טבלת צ'מפיון: טיפול כל 15,000 ק\"מ; תקרת שנה לפי מרווח QI4 של היצרן", status='reviewed')

def T_CH_PHEV(o):
    rows = OIL + BRAKES_CH + [
        (every(30000), it('air_filter', 'replace')),
        (every(30000), it('cabin_filter', 'replace')),
        (every(60000), it('spark_plugs', 'replace', 'או כל 4 שנים, המוקדם')),
        (every(60000), it('dct_oil', 'replace', 'תיבת DSG רטובה 6 הילוכים (DQ400E)')),
        (at(120000), it('timing_belt', 'replace', 'רצועת תזמון עם מותחן וגלגלת סרק, וגם רצועת ההנעה של משאבת המים')),
    ]
    li = [
        {"item": "brake_fluid", "action": "replace", "every_months": 24},
        {"item": "spark_plugs", "action": "replace", "every_months": 48},
    ]
    notes = ("הלוח הועתק מטבלת \"1.4 ל' PHEV בנזין\" בשגרת הטיפולים של צ'מפיון מוטורס (מנוע 1.4 TSI היברידי נטען). "
             "שמן תיבת DQ400E מוחלף כל 60,000, בדומה לטבלאות היצרן (0DD כל 60,000). "
             "בדיקות רכיבי מתח גבוה נעשות לפי מערכת השירות של היצרן ואינן מפורטות כאן.")
    return dict(rows=rows, li=li, notes=notes, srcs=['CH', 'OCT4', 'VWTS_ENG'],
                interval_note="לפי טבלת צ'מפיון: טיפול כל 15,000 ק\"מ; תקרת שנה לפי מרווח QI4 של היצרן", status='reviewed')

def T_CH_BEV(o):
    rows = BRAKES_CH + [
        (lambda km: km % 30000 != 0, it('cabin_filter', 'inspect')),
        (every(30000), it('cabin_filter', 'replace', 'או כל שנה, המוקדם' + ('; באאודי e-tron כל 15,000 או שנה' if o.get('etron') else ''))),
    ]
    if o.get('etron'):
        rows.append((every(15000), it('coolant', 'replace', 'מיכל עודפי נוזל הקירור של המנוע האחורי; לפי היבואן רק באאודי e-tron')))
    li = [
        {"item": "brake_fluid", "action": "replace", "every_months": 24},
        {"item": "cabin_filter", "action": "replace", "every_months": 12},
    ]
    notes = ("הלוח הועתק מטבלת 'BEV חשמלי' בשגרת הטיפולים של צ'מפיון מוטורס: מסנן מזגן, נוזל בלמים ובדיקת בלמים בלבד. "
             "בדיקות מערכת המתח הגבוה, המצבר והצמיגים נעשות לפי מערכת השירות של היצרן.")
    return dict(rows=rows, li=li, notes=notes, srcs=['CH'], inspections=True,
                interval_note="לפי טבלת צ'מפיון: ביקור כל 15,000 ק\"מ; תקרת שנה לפי סדר החלפת מסנן המזגן", status='reviewed')

def T_FAC(o):
    """Factory tables, 'dust-rich countries' column (Israel is listed). o: brand ('skoda'|'vw'), belt ('yes'|'no'|'cond'),
       plugs90 (list of engine labels with 90k/6y plugs), old_skoda (bool: Skoda <= MY2016 tables), note_extra"""
    brand = o['brand']; belt = o.get('belt', 'cond'); old = o.get('old_skoda', False)
    rows = OIL + BRAKES_FAC
    li = []
    if old:
        if o.get('cabin60'):
            rows += [(every(60000), it('cabin_filter', 'replace', 'או כל שנתיים, המוקדם'))]
        else:
            rows += [(every(30000), it('cabin_filter', 'replace', 'או כל שנתיים, המוקדם'))]
        li += [
            {"item": "air_filter", "action": "replace", "every_km": 90000, "every_months": 72, "note": "בטבלת סקודה עד שנת דגם 2016 אין שורה נפרדת למדינות מאובקות"},
            {"item": "cabin_filter", "action": "replace", "every_months": 24},
            {"item": "brake_fluid", "action": "replace", "first_months": 36, "then_every_months": 24, "note": "ראשון אחרי 3 שנים ואז כל שנתיים"},
        ]
    else:
        rows += [
            (every(30000), it('air_filter', 'replace', 'או כל שנתיים, המוקדם')),
            (every(30000), it('cabin_filter', 'replace', 'או כל שנה, המוקדם')),
            (every(60000), it('drive_belt', 'replace', 'רצועת אביזרים')),
        ]
        li += [
            {"item": "air_filter", "action": "replace", "every_months": 24},
            {"item": "cabin_filter", "action": "replace", "every_months": 12},
            {"item": "brake_fluid", "action": "replace", "every_months": 24, "note": "טבלאות היצרן לשווקים מחוץ לאירופה במרווח קבוע"},
        ]
    plug_note = 'או כל 4 שנים, המוקדם'
    if o.get('plugs90'):
        plug_note += '. במנועי ' + ', '.join(o['plugs90']) + ' לפי היצרן כל 90,000 ק\"מ או 6 שנים'
    if o.get('plugs90_only'):
        li.append({"item": "spark_plugs", "action": "replace", "every_km": 90000, "every_months": 72})
    else:
        rows.append((every(60000), it('spark_plugs', 'replace', plug_note)))
        li.append({"item": "spark_plugs", "action": "replace", "every_months": 48})
    if belt in ('yes', 'cond'):
        n = 'רצועת תזמון עם מותחן, וכן רצועת השיניים של משאבת המים אם קיימת; לפי עמודת המדינות המאובקות'
        if belt == 'cond':
            n = 'רק במנוע עם רצועת תזמון (' + o.get('belt_engines', 'ראו הערות') + '); ' + n
        rows.append((at(120000), it('timing_belt', 'replace', n)))
    if o.get('coolant_pump_belt_ea888'):
        li.append({"item": "timing_belt", "action": "replace", "every_km": 120000,
                   "note": "רצועת השיניים של משאבת המים במנועי 1.8/2.0 TSI: בטבלת סקודה עד שנת דגם 2016 כל 120,000 במדינות מאובקות; משנת דגם 2017 השורה לא חלה על מנועים אלה"})
    if o.get('drums'):
        li.append({"item": "brake_drums", "action": "clean", "every_months": 24, "note": "ניקוי בלמי התוף האחוריים, רק ברכב שמצויד בהם"})
    li.append({"item": "dct_oil", "action": "replace", "every_km": 60000,
               "note": "רק בתיבת DSG רטובה 6 הילוכים (02E/0D9) או DQ500 (0DL/0BH); DQ381 (0GC) כל 120,000; בתיבה יבשה 7 הילוכים (0AM/0CW) אין החלפה"})
    li.append({"item": "transmission_oil", "action": "replace", "every_km": 60000,
               "note": "רק בתיבה אוטומטית רגילה (09G ודומותיה): ישראל ברשימת המדינות החמות"})
    if o.get('awd', True):
        li.append({"item": "differential_oil", "action": "replace", "every_months": 36,
                   "note": "שמן מצמד ההנעה הכפולה (הלדקס), רק בגרסאות 4x4"})
    base = {'skoda': ('OCT3', 'RAPID', 'FAB3', 'KOD'), 'vw': ('GOLF7', 'TIG1', 'PASSAT7', 'LEON3')}[brand]
    srcs = list(o.get('srcs', base)) + ['SK_OM' if brand == 'skoda' else 'GOLF7', 'VWTS_ENG']
    srcs = list(dict.fromkeys(srcs))
    if old:
        notes = ("אין לוח טיפולים ישראלי למנועים אלה (בשגרת צ'מפיון מופיעים רק מנועי 1.0/1.5/2.0 מהשנים האחרונות). הלוח נבנה מטבלאות מדריך השירות של סקודה, "
                 "פרק 'עבודות נוספות עד שנת דגם 2016': שמן ומסנן כל 15,000 ק\"מ או שנה (QI4), מסנן מזגן כל שנתיים או " + ('60,000' if o.get('cabin60') else '30,000') + ", מסנן אוויר כל 90,000 או 6 שנים, "
                 "נוזל בלמים אחרי 3 שנים ואז כל שנתיים, רצועת תזמון (במנוע עם רצועה) כל 120,000 במדינות מאובקות (ישראל ברשימה). "
                 "לשם השוואה, בטבלאות משנת דגם 2017 ובשגרת צ'מפיון העדכנית מסנני האוויר והמזגן מוחלפים כל 30,000 ורצועת האביזרים כל 60,000; ייתכן שמוסכי היבואן עובדים כך גם ברכבים ישנים. ")
    else:
        notes = ("אין לוח טיפולים ישראלי למנועים אלה (בשגרת צ'מפיון מופיעים רק מנועי 1.0/1.5/2.0 מהשנים האחרונות). הלוח נבנה מטבלאות מדריך השירות של היצרן, "
                 "בעמודת 'מדינות עם אבק רב' שבה ישראל רשומה: שמן ומסנן כל 15,000 ק\"מ או שנה (QI4), מסנן אוויר כל 30,000 או שנתיים, מסנן מזגן כל 30,000 או שנה, "
                 "רצועת אביזרים כל 60,000, רצועת תזמון ורצועת משאבת המים (במנוע עם רצועה) כל 120,000, מצתים כל 60,000 או 4 שנים, ונוזל בלמים כל שנתיים (שווקים מחוץ לאירופה). "
                 "אותם ערכים מופיעים בשגרת צ'מפיון העדכנית למנועי 1.0/1.5. ")
    if brand == 'vw':
        notes += "טבלאות פולקסווגן/סיאט במהדורות 2018-2021 חלות גם על דגמים ישנים (למשל Tiguan 2008 ו-Passat 2011) ולכן שימשו לכל הדגמים בקובץ. "
    notes += ("שורות ה-DSG, התיבה האוטומטית וההנעה הכפולה בלוח ארוך הטווח חלות רק על רכב שמצויד בהן. "
              "בדיקות בכל 30,000/60,000 ק\"מ לפי היקף הבדיקה (Inspection) במדריך היצרן. ")
    notes += o.get('note_extra', '')
    return dict(rows=rows, li=li, notes=notes.strip(), srcs=srcs,
                interval_note="מרווח קבוע QI4 של היצרן: החלפת שמן כל 15,000 ק\"מ או שנה, בדיקה כל 30,000 ק\"מ", status='draft')

def T_CH_T61(o):
    rows = [(every(20000), it('engine_oil', 'replace')), (every(20000), it('oil_filter', 'replace')),
            (every(20000), it('brake_pads', 'inspect', 'קדמיות ואחוריות, כולל מצב הדיסקים')), (every(20000), it('brake_discs', 'inspect')),
            (every(120000), it('fuel_filter', 'replace', 'מסנן סולר')),
            (every(60000), it('transmission_oil', 'replace', 'שמן תיבת הילוכים ומסנן')),
            (every(60000), it('drive_belt', 'replace', 'רצועת מנוע')),
            (lambda km: km % 80000 == 40000, it('timing_belt', 'inspect', 'בדיקת רצועת תזמון, מותחן וגלגלת סרק')),
            (every(80000), it('timing_belt', 'replace', 'רצועת תזמון עם מותחן וגלגלת סרק')),
            (every(40000), it('battery_12v')), (every(40000), it('lights')), (every(40000), it('tires')), (every(40000), it('brake_lines')), (every(40000), it('cooling_system')),
           ]
    li = [
        {"item": "air_filter", "action": "replace", "every_km": 30000, "every_months": 24, "note": "כולל ניקוי בית המסנן"},
        {"item": "cabin_filter", "action": "replace", "every_km": 30000, "every_months": 12},
        {"item": "brake_fluid", "action": "replace", "every_months": 24, "note": "נוזל בלמים ומצמד"},
        {"item": "differential_oil", "action": "replace", "every_months": 24, "note": "שמן מצמד ההנעה הכפולה (הלדקס), רק ב-4MOTION"},
    ]
    notes = ("הלוח הועתק מטבלת 'Transporter T6.1' בשגרת הטיפולים של צ'מפיון מוטורס (רכב מסחרי): טיפול כל 20,000 ק\"מ עד 240,000. "
             "לפי הערת היבואן, נתוני רצועת התזמון מותאמים לקוד מנוע DNAA (נכון לאוקטובר 2024). מסנני האוויר והמזגן מוחלפים לפי 30,000 ק\"מ ולכן מופיעים בלוח ארוך הטווח. "
             "בדיקות המצבר, התאורה, הצמיגים, מערכת הבלמים והקירור כל 40,000 ק\"מ הוספו כהערכה כללית של בדיקת רכב ואינן בטבלת היבואן.")
    return dict(rows=rows, li=li, notes=notes, srcs=['CH', 'VWTS_DSL'], inspections=False,
                interval_note="לפי טבלת צ'מפיון לרכב מסחרי T6.1: טיפול כל 20,000 ק\"מ", status='reviewed', step=20000, cycle=240000)

def T_CH_CADDY5(o):
    rows = OIL + BRAKES_CH + [
        (every(30000), it('air_filter', 'replace', 'כולל ניקוי בית המסנן; לפי ק\"מ או שנתיים')),
        (every(30000), it('cabin_filter', 'replace', 'לפי ק\"מ או שנתיים')),
        (at(180000), it('fuel_filter', 'replace', 'מסנן סולר')),
        (every(120000), it('transmission_oil', 'replace', 'שמן תיבת הילוכים ומסנן')),
        (every(60000), it('drive_belt', 'replace', 'רצועת מנוע')),
        (at(240000), it('coolant', 'replace')),
    ]
    li = [
        {"item": "brake_fluid", "action": "replace", "every_months": 24},
        {"item": "air_filter", "action": "replace", "every_months": 24},
        {"item": "cabin_filter", "action": "replace", "every_months": 24},
    ]
    notes = ("הלוח הועתק מטבלת 'Caddy Gen 5' בשגרת הטיפולים של צ'מפיון מוטורס (15,000 עד 240,000 ק\"מ, דיזל 2.0 TDI). "
             "בטבלה אין שורת רצועת תזמון. בדיקות בכל 30,000/60,000 ק\"מ נוספו מהיקף הבדיקה במדריכי היצרן.")
    return dict(rows=rows, li=li, notes=notes, srcs=['CH', 'VWTS_DSL'],
                interval_note="לפי טבלת צ'מפיון: טיפול כל 15,000 ק\"מ", status='reviewed', cycle=240000)

def T_T5_2010(o):
    rows = [(every(20000), it('engine_oil', 'replace')), (every(20000), it('oil_filter', 'replace')),
            (every(20000), it('brake_pads', 'inspect', 'עובי רפידות ומצב דיסקים')), (every(20000), it('brake_discs', 'inspect')),
            (every(40000), it('timing_belt', 'inspect', 'בדיקת רצועת תזמון באזורים מאובקים: כל 40,000 ק\"מ או שנתיים')),
            (every(60000), it('cabin_filter', 'replace', 'או כל שנתיים')),
            (every(120000), it('air_filter', 'replace', 'או כל 6 שנים')),
            (every(120000), it('fuel_filter', 'replace', 'או כל 6 שנים')),
            (every(120000), it('timing_belt', 'replace', 'רצועת תזמון ומותחן, באזורים מאובקים')),
            (every(120000), it('drive_belt', 'inspect')),
           ] + [(every(40000), it(x)) for x in ['battery_12v', 'lights', 'wipers', 'tires', 'brake_lines', 'cooling_system', 'cv_boots', 'suspension', 'exhaust', 'body_underside']]
    li = [
        {"item": "cabin_filter", "action": "replace", "every_months": 24},
        {"item": "timing_belt", "action": "inspect", "every_months": 24},
        {"item": "dct_oil", "action": "replace", "every_km": 60000, "every_months": 36, "note": "רק בתיבת DSG"},
        {"item": "differential_oil", "action": "replace", "every_km": 60000, "every_months": 36, "note": "שמן מצמד ההנעה הכפולה, רק ב-4MOTION"},
        {"item": "brake_fluid", "action": "replace", "first_months": 36, "then_every_months": 24},
    ]
    notes = ("אין לוח ישראלי לדור זה (בשגרת צ'מפיון מופיעה רק T6.1). הלוח לפי מדריך השירות של טרנספורטר 2004/2010, עבודות משנת דגם 2010 לדיזל 2.0 TDI: "
             "החלפת שמן קבועה כל 20,000 ק\"מ או שנה (בדומה לטבלת צ'מפיון ל-T6.1), מסנן מזגן כל 60,000 או שנתיים, מסנן אוויר ומסנן סולר כל 120,000 או 6 שנים, "
             "בדיקת רצועת תזמון כל 40,000 או שנתיים והחלפתה עם המותחן ב-120,000 באזורים מאובקים (ישראל ברשימה), נוזל בלמים אחרי 3 שנים ואז כל שנתיים. "
             "בדיקות רכב כלליות כל 40,000 לפי מרווח הבדיקה לדיזל. בטבלת 2010 אין שורות נפרדות למסנני אוויר/מזגן באזורים מאובקים.")
    return dict(rows=rows, li=li, notes=notes, srcs=['T5', 'CH', 'VWTS_DSL'], inspections=False,
                interval_note="מרווח קבוע לדיזל לפי מדריך היצרן: החלפת שמן כל 20,000 ק\"מ או שנה", status='draft', step=20000, cycle=240000)

def T_T6(o):
    rows = [(every(20000), it('engine_oil', 'replace')), (every(20000), it('oil_filter', 'replace')),
            (every(20000), it('brake_pads', 'inspect', 'עובי רפידות ומצב דיסקים')), (every(20000), it('brake_discs', 'inspect')),
            (every(40000), it('timing_belt', 'inspect', 'בדיקת רצועת תזמון באזורים מאובקים')),
            (every(60000), it('dct_oil', 'replace', 'רק בתיבת DSG')),
            (every(120000), it('timing_belt', 'replace', 'רצועת תזמון, באזורים מאובקים')),
            (every(120000), it('fuel_filter', 'replace', 'או כל 6 שנים')),
           ] + [(every(40000), it(x)) for x in ['battery_12v', 'lights', 'wipers', 'tires', 'brake_lines', 'cooling_system', 'cv_boots', 'suspension', 'exhaust', 'body_underside', 'drive_belt']]
    li = [
        {"item": "air_filter", "action": "replace", "every_km": 30000, "every_months": 24, "note": "באזורים מאובקים"},
        {"item": "cabin_filter", "action": "replace", "every_km": 30000, "every_months": 12, "note": "באזורים מאובקים"},
        {"item": "fuel_filter", "action": "replace", "every_months": 72},
        {"item": "differential_oil", "action": "replace", "every_months": 36, "note": "שמן מצמד ההנעה הכפולה, רק ב-4MOTION"},
        {"item": "brake_fluid", "action": "replace", "first_months": 36, "then_every_months": 24},
    ]
    notes = ("אין לוח ישראלי לדור זה (בשגרת צ'מפיון מופיעה רק T6.1). הלוח לפי מדריך השירות של טרנספורטר 2016 (T6), עמודת 'אזורים מאובקים' (ישראל ברשימה): "
             "החלפת שמן קבועה כל 20,000 ק\"מ או שנה (QI5), בדיקה כל 40,000, מסנן אוויר כל 30,000 או שנתיים ומסנן מזגן כל 30,000 או שנה (בלוח ארוך הטווח כי אינם על רשת ה-20,000), "
             "בדיקת רצועת תזמון כל 40,000 והחלפתה ב-120,000, מסנן סולר כל 120,000 או 6 שנים, שמן DSG כל 60,000, נוזל בלמים אחרי 3 שנים ואז כל שנתיים.")
    return dict(rows=rows, li=li, notes=notes, srcs=['T6', 'CH', 'VWTS_DSL'], inspections=False,
                interval_note="מרווח קבוע QI5 לפי מדריך היצרן: החלפת שמן כל 20,000 ק\"מ או שנה", status='draft', step=20000, cycle=240000)

def T_T5_OLD(o):
    rows = OIL + BRAKES_FAC + [
        (every(30000), it('timing_belt', 'inspect', 'בדיקת רצועת תזמון במנועי 1.9 TDI')),
        (every(60000), it('cabin_filter', 'replace', 'או כל שנתיים')),
        (every(120000), it('air_filter', 'replace', 'או כל 6 שנים')),
        (every(120000), it('fuel_filter', 'replace', 'או כל 6 שנים')),
        (every(120000), it('timing_belt', 'replace', 'רק 1.9 TDI עם קוד BRR/BRS (בלי המותחן); ב-AXB/AXC כל 90,000')),
    ]
    li = [
        {"item": "timing_belt", "action": "replace", "every_km": 90000, "note": "רק 1.9 TDI עם קוד מנוע AXB/AXC"},
        {"item": "differential_oil", "action": "replace", "every_km": 60000, "note": "שמן מצמד ההנעה הכפולה, רק ב-4MOTION"},
        {"item": "cabin_filter", "action": "replace", "every_months": 24},
        {"item": "brake_fluid", "action": "replace", "first_months": 36, "then_every_months": 24, "note": "מ-2008 כחלק מטיפול הבדיקה; עד 2007 כל שנתיים"},
    ]
    notes = ("אין לוח ישראלי לדור זה. הלוח לפי מדריך השירות של טרנספורטר 2004, עבודות לפי זמן/ק\"מ עד שנת דגם 2009: החלפת שמן כל 15,000 ק\"מ או שנה, "
             "טיפול ביניים כל 30,000 או שנתיים, בדיקת רצועת תזמון (1.9 TDI) כל 30,000, מסנן מזגן כל 60,000, מסנן אוויר ומסנן סולר כל 120,000, "
             "רצועת תזמון 1.9 TDI: AXB/AXC כל 90,000, BRR/BRS כל 120,000. במנועי 2.5 TDI (AXD/BNZ) המדריך מפרט החלפת גלגלי חופש וצימודים במערכת העזר ב-150,000/180,000 ואינו מפרט רצועת תזמון.")
    return dict(rows=rows, li=li, notes=notes, srcs=['T5', 'VWTS_DSL'],
                interval_note="מרווח קבוע לפי מדריך היצרן: החלפת שמן כל 15,000 ק\"מ או שנה", status='draft')

def T_CADDY3(o):
    rows = OIL + BRAKES_FAC + [
        (every(30000), it('timing_belt', 'inspect', 'בדיקת רצועת תזמון במנועי דיזל במדינות מאובקות (גם כל שנתיים); במנועי בנזין 1.4/1.6 MPI מ-90,000 ואז כל 30,000')),
        (every(30000), it('drive_belt', 'inspect')),
        (every(60000), it('cabin_filter', 'replace', 'או כל שנתיים')),
        (every(60000), it('spark_plugs', 'replace', 'בנזין בלבד; או כל 4 שנים')),
        (every(60000), it('dct_oil', 'replace', 'רק בתיבת DSG 02E')),
        (every(90000), it('fuel_filter', 'replace', 'דיזל בלבד')),
        (every(90000), it('air_filter', 'replace', 'או כל 6 שנים')),
        (every(120000), it('timing_belt', 'replace', 'רק 1.9 TDI עם מזרקי יחידה (BLS), כולל מותחן')),
    ]
    li = [
        {"item": "timing_belt", "action": "replace", "every_km": 210000, "note": "1.6/2.0 TDI קומון-רייל (CAY), כולל מותחן"},
        {"item": "cabin_filter", "action": "replace", "every_months": 24},
        {"item": "air_filter", "action": "replace", "every_months": 72},
        {"item": "differential_oil", "action": "replace", "every_months": 36, "note": "רק ב-4MOTION"},
        {"item": "brake_fluid", "action": "replace", "first_months": 36, "then_every_months": 24},
    ]
    notes = ("אין לוח ישראלי לדור זה. הלוח לפי מדריך השירות של קאדי 2004/2011: החלפת שמן כל 15,000 ק\"מ או שנה, מסנן מזגן ומצתים כל 60,000, "
             "מסנן סולר ומסנן אוויר כל 90,000, רצועת תזמון 1.9 TDI (BLS) כל 120,000 ו-1.6/2.0 TDI (CAY) כל 210,000, עם בדיקת רצועה כל 30,000 במדינות מאובקות (ישראל ברשימה). "
             "הקובץ משמש גם לגרסת הבנזין 1.2 TSI (CBZ, שרשרת); שורות הדיזל לא חלות עליה.")
    return dict(rows=rows, li=li, notes=notes, srcs=['CADDY3', 'VWTS_DSL', 'VWTS_ENG'],
                interval_note="מרווח קבוע לפי מדריך היצרן: החלפת שמן כל 15,000 ק\"מ או שנה", status='draft')

def T_CADDY4(o):
    rows = OIL + BRAKES_FAC + [
        (every(30000), it('air_filter', 'replace', 'או כל שנתיים')),
        (every(30000), it('cabin_filter', 'replace', 'או כל שנה')),
        (every(60000), it('drive_belt', 'inspect')),
        (every(60000), it('dct_oil', 'replace', 'רק בתיבת DSG 02E')),
        (every(60000), it('spark_plugs', 'replace', 'בנזין בלבד; או כל 4 שנים')),
        (every(90000), it('fuel_filter', 'replace', 'דיזל בלבד')),
        (at(120000), it('timing_belt', 'replace', 'רצועת תזמון ומותחן, באזורים מאובקים')),
    ]
    li = [
        {"item": "air_filter", "action": "replace", "every_months": 24},
        {"item": "cabin_filter", "action": "replace", "every_months": 12},
        {"item": "differential_oil", "action": "replace", "every_months": 36, "note": "רק ב-4MOTION"},
        {"item": "brake_fluid", "action": "replace", "first_months": 36, "then_every_months": 24},
    ]
    notes = ("אין לוח ישראלי לדור זה (בשגרת צ'מפיון מופיע רק Caddy Gen 5). הלוח לפי מדריך השירות של קאדי 2016, כולל שורות 'באזורים מאובקים' (ישראל ברשימה): "
             "החלפת שמן כל 15,000 ק\"מ או שנה, מסנן אוויר כל 30,000 או שנתיים, מסנן מזגן כל 30,000 או שנה, בדיקת רצועת אביזרים כל 60,000, "
             "רצועת תזמון ומותחן כל 120,000, מסנן סולר כל 90,000, נוזל בלמים אחרי 3 שנים ואז כל שנתיים. הקובץ משמש גם לגרסאות הבנזין 1.4 TSI (CZC/DJK).")
    return dict(rows=rows, li=li, notes=notes, srcs=['CADDY4', 'VWTS_DSL', 'VWTS_ENG'],
                interval_note="מרווח קבוע QI4 לפי מדריך היצרן: החלפת שמן כל 15,000 ק\"מ או שנה, בדיקה כל 30,000", status='draft')

def T_CH_D30(o):
    rows = OIL + BRAKES_CH + [
        (every(30000), it('air_filter', 'replace')),
        (every(30000), it('fuel_filter', 'replace', 'מסנן סולר')),
        (every(30000), it('cabin_filter', 'replace', 'או כל שנה, המוקדם')),
        (at(120000), it('drive_belt', 'replace', 'רצועת אביזרים')),
    ]
    li = [
        {"item": "brake_fluid", "action": "replace", "every_months": 24},
        {"item": "cabin_filter", "action": "replace", "every_months": 12},
    ]
    notes = ("הלוח הועתק מטבלת \"3.0 ל' דיזל\" בשגרת הטיפולים של צ'מפיון מוטורס (V6 TDI). לפי הטבלה אין הוראת החלפה לשמן תיבת ההילוכים. "
             "בדיקות בכל 30,000/60,000 ק\"מ נוספו מהיקף הבדיקה במדריכי היצרן.")
    return dict(rows=rows, li=li, notes=notes, srcs=['CH', 'VWTS_DSL'],
                interval_note="לפי טבלת צ'מפיון: טיפול כל 15,000 ק\"מ; תקרת שנה לפי מרווח QI4 של היצרן", status='reviewed')

def T_FAC_D(o):
    old = o.get('old_skoda', False); fkm = o.get('fuel_km', 90000)
    rows = OIL + BRAKES_FAC
    li = []
    if old:
        rows += [(every(30000), it('cabin_filter', 'replace', 'או כל שנתיים, המוקדם'))]
        li += [{"item": "air_filter", "action": "replace", "every_km": 90000, "every_months": 72},
               {"item": "cabin_filter", "action": "replace", "every_months": 24},
               {"item": "brake_fluid", "action": "replace", "first_months": 36, "then_every_months": 24}]
    else:
        rows += [(every(30000), it('air_filter', 'replace', 'או כל שנתיים, המוקדם')),
                 (every(30000), it('cabin_filter', 'replace', 'או כל שנה, המוקדם')),
                 (every(60000), it('drive_belt', 'replace', 'רצועת אביזרים'))]
        li += [{"item": "air_filter", "action": "replace", "every_months": 24},
               {"item": "cabin_filter", "action": "replace", "every_months": 12},
               {"item": "brake_fluid", "action": "replace", "every_months": 24}]
    if fkm == 60000:
        rows.append((every(60000), it('fuel_filter', 'replace', 'מסנן סולר')))
    else:
        li.append({"item": "fuel_filter", "action": "replace", "every_km": fkm, "note": "מסנן סולר"})
    rows.append((at(120000), it('timing_belt', 'replace', 'רצועת תזמון ומותחן, לפי עמודת המדינות המאובקות')))
    li.append({"item": "dct_oil", "action": "replace", "every_km": 60000, "note": "רק בתיבת DSG רטובה 6 הילוכים (02E/0D9); בתיבה יבשה 7 הילוכים (0AM) אין החלפה"})
    li.append({"item": "differential_oil", "action": "replace", "every_months": 36, "note": "רק בהנעה כפולה"})
    base = {'skoda': ['OCT3', 'RAPID', 'KOD'], 'vw': ['GOLF7', 'TIG1', 'PASSAT7']}[o['brand']]
    notes = ("אין לוח ישראלי למנועי 1.6 TDI (בשגרת צ'מפיון רק 2.0/3.0 דיזל). הלוח נבנה מטבלאות מדריך השירות של היצרן"
             + (" (פרק 'עד שנת דגם 2016'): מסנן מזגן כל שנתיים, מסנן אוויר כל 90,000 או 6 שנים, נוזל בלמים אחרי 3 שנים ואז כל שנתיים" if old else
                ", עמודת 'מדינות עם אבק רב' (ישראל ברשימה): מסנן אוויר כל 30,000 או שנתיים, מסנן מזגן כל 30,000 או שנה, רצועת אביזרים כל 60,000, נוזל בלמים כל שנתיים")
             + ", רצועת תזמון בדיזל קומון-רייל כל 120,000 במדינות מאובקות, מסנן סולר כל " + f"{fkm:,}" + " ק\"מ. " + o.get('note_extra', ''))
    return dict(rows=rows, li=li, notes=notes.strip(), srcs=base + ['VWTS_DSL'],
                interval_note="מרווח קבוע QI4 של היצרן: החלפת שמן כל 15,000 ק\"מ או שנה", status='draft')

TEMPLATES = {'CH_SMALL': T_CH_SMALL, 'CH_20': T_CH_20, 'CH_D20': T_CH_D20, 'CH_PHEV': T_CH_PHEV, 'CH_BEV': T_CH_BEV, 'FAC': T_FAC, 'CH_T61': T_CH_T61, 'CH_CADDY5': T_CH_CADDY5, 'T5_2010': T_T5_2010, 'T6': T_T6, 'T5_OLD': T_T5_OLD, 'CADDY3': T_CADDY3, 'CADDY4': T_CADDY4, 'CH_D30': T_CH_D30, 'FAC_D': T_FAC_D}

# ---------------------------------------------------------------- registry helpers
MAKE_EN = {'סקודה': 'Skoda', 'סיאט': 'Seat', 'פולקסווגן': 'Volkswagen', 'אאודי': 'Audi', 'קופרה': 'קופרה'}

def reg_rows(make_prefix, names, codes, years=None):
    rows = []
    for r in REG['model_year_fuel_engine']:
        if not r['make'].startswith(make_prefix): continue
        if r['model'] not in names: continue
        if r['engine'] not in codes: continue
        y = int(r['year'])
        if years and not (years[0] <= y <= years[1]): continue
        rows.append(r)
    return rows

# ---------------------------------------------------------------- specs
SPECS = []
def S(**k): SPECS.append(k)

SK, SE, VW, AU, CU = 'סקודה', 'סיאט', 'פולקסווגן', 'אאודי', 'קופרה'
TSI10 = ['CHZ', 'DKR', 'DKJ', 'DKL', 'DLA', 'DUS']
TSI15 = ['DAD', 'DPC', 'DFY', 'DXD']
from specs import load_specs, load_specs_commercial, load_specs_extra
load_specs(S, locals()); load_specs_commercial(S, locals()); load_specs_extra(S, locals())

# ---------------------------------------------------------------- build
os.makedirs(OUT, exist_ok=True)
rules = []; report = []
for sp in SPECS:
    t = TEMPLATES[sp['template']](sp.get('opts', {}))
    step = sp.get('step', t.get('step', 15000)); cycle = sp.get('cycle', t.get('cycle', 120000))
    services = assemble(t['rows'], step, cycle, t.get('inspections', True))
    rr = []
    for (mk, names) in sp['reg']:
        rr += reg_rows(mk, names, sp['codes'], sp.get('reg_years'))
    n = sum(r['n'] for r in rr)
    ys = sorted(int(r['year']) for r in rr)
    yr = sp.get('years') or [ys[0], ys[-1]]
    fuels = sorted(set(r['fuel'] for r in rr))
    notes = sp.get('notes_pre', '') + t['notes'] + (' ' + sp['notes_post'] if sp.get('notes_post') else '')
    srcs = [dict(SRC[s]) for s in (sp.get('srcs_pre', []) + t['srcs'] + sp.get('srcs_post', []))]
    seen = set(); srcs2 = []
    for s in srcs:
        if s['url'] in seen: continue
        seen.add(s['url']); srcs2.append(s)
    doc = {
        "id": sp['id'], "make": sp['make'], "make_he": sp['make_he'], "model": sp['model'], "model_he": sp['model_he'],
        "generation": sp['generation'], "years": yr, "engines": sp['engines'], "fuel": sp.get('fuel', 'petrol'),
        "importer": IMP,
        "interval": {"km": step, "months": 12, "note": t['interval_note']},
        "cycle_km": cycle, "services": services, "long_interval": t['li'], "time_based": [],
        "specs": {"_note": "טיוטה: ערכים כלליים ממדריכי היצרן; לאמת מול ספר הרכב", **sp.get('specs', {})} if sp.get('specs') else {},
        "sources": srcs2, "status": sp.get('status', t['status']), "notes": notes,
    }
    if not doc['specs']: del doc['specs']
    json.dump(doc, open(os.path.join(OUT, sp['id'] + '.json'), 'w'), ensure_ascii=False, indent=2)
    # registry rules: one per make prefix group
    bymake = collections.defaultdict(lambda: {'names': set(), 'years': []})
    for r in rr:
        mk = MAKE_EN[[p for p in MAKE_EN if r['make'].startswith(p)][0]]
        bymake[mk]['names'].add(r['model']); bymake[mk]['years'].append(int(r['year']))
    for mk, v in bymake.items():
        rule = {"make": mk, "names": sorted(v['names']), "years": sp.get('reg_years') or [min(v['years']), max(v['years'])],
                "fuel": fuels, "engine_codes": sp['codes'], "schedule": sp['id']}
        rules.append(rule)
    report.append((sp['id'], n, doc['status'], sorted(set(r['engine'] for r in rr))))

json.dump(rules, open(os.path.join(OUT, 'registry_rules.json'), 'w'), ensure_ascii=False, indent=1)
tot = 0
for r in sorted(report, key=lambda x: -x[1]):
    tot += r[1]; print(f"{r[1]:6d} {r[2]:8s} {r[0]}  {' '.join(r[3])}")
print('TOTAL', tot, 'files', len(report))
