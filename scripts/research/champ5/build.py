import json, copy, os
SCH = '/home/user/cv/data/schedules/'
OUT = '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/champ5/'
R = json.load(open('/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/dl/champ5/routine_now.json'))
def load(i): return json.load(open(SCH + i + '.json'))
def save(d):
    json.dump(d, open(OUT + d['id'] + '.json', 'w'), ensure_ascii=False, indent=2)
    print('wrote', d['id'], d['status'])

CHAMP_URL = 'https://www.championmotors.co.il/service-routine/'
def champ_src(table, extra=''):
    return {"url": CHAMP_URL, "kind": "importer",
            "note": f"שגרת הטיפולים של צ'מפיון מוטורס, טבלת '{table}'. הדף חסום לבוטים ונקרא בדפדפן Playwright ב-3.10.2026; הטבלה זהה לגרסה שנשמרה ב-28.9.2026. סימוני ההחלפה/בדיקה פוענחו מקוד הדף לפי סוג הסמל בכל עמודה{extra}"}
VWTS_P = {"url": "https://vwts.ru/petrol-engine-vw-audi-skoda-repair-manual.html", "kind": "other",
          "note": "אינדקס ספרי תיקון מנועים של קבוצת פולקסווגן לפי קודי מנוע, לשיוך קוד המנוע לנפח ולמשפחה"}
VWTS_D = {"url": "https://vwts.ru/diesel-engine-vw-audi-skoda-repair-manual.html", "kind": "other",
          "note": "אינדקס ספרי תיקון מנועי דיזל של קבוצת פולקסווגן לפי קודי מנוע (CRLB/DFGA = 2.0 TDI EA288; DMZA = 2.0 TDI EA288 למסחריות)"}

# ---------------- A. clones of reviewed Champion-table files ----------------
def clone(src, **kw):
    d = copy.deepcopy(load(src))
    extra_note = kw.pop('extra_note', '')
    for k, v in kw.items(): d[k] = v
    if extra_note: d['notes'] = d['notes'] + ' ' + extra_note
    return d

save(clone('vw-tiguan-2019-2026-1.5-tsi', id='vw-passat-2020-2021-1.5-tsi', model='Passat', model_he='פאסאט',
           generation='B8 פייסליפט', years=[2020, 2021], engines=['1.5 TSI (DPC)'],
           extra_note="קובץ זה משייך את פאסאט B8 המחודשת עם מנוע 1.5 TSI (קוד DPC ברישיון) לאותה טבלת יבואן '1.5 ל' בנזין'; התוכן זהה לקובץ טיגואן 1.5."))
save(clone('vw-tiguan-2017-2026-2.0-tsi', id='vw-passat-2020-2022-2.0-tsi', model='Passat', model_he='פאסאט',
           generation='B8 פייסליפט', years=[2020, 2022], engines=['2.0 TSI (DKZ/DNN)'],
           extra_note="קובץ זה משייך את פאסאט B8 המחודשת עם מנוע 2.0 TSI (קודי DKZ/DNN ברישיון) לטבלת היבואן '2.0 ל' בנזין'; התוכן זהה לקובץ טיגואן 2.0."))
save(clone('vw-tiguan-2017-2026-2.0-tsi', id='vw-polo-gti-2019-2024-2.0-tsi', model='Polo GTI', model_he='פולו GTI',
           generation='AW', years=[2019, 2024], engines=['2.0 TSI (DKZ/DNN)'],
           extra_note="קובץ זה משייך את פולו GTI (קודי DKZ/DNN ברישיון) לטבלת היבואן '2.0 ל' בנזין'. בפולו GTI אין הנעה כפולה ולכן שורות הלדקס ונעילת הדיפרנציאל אינן רלוונטיות בדרך כלל."))
save(clone('vw-tiguan-2019-2026-1.5-tsi', id='vw-tayron-2025-2026-1.5-tsi', model='Tayron', model_he='טיירון',
           generation='CT', years=[2025, 2026], engines=['1.5 eTSI (DXD)'],
           extra_note="קובץ זה משייך את טיירון עם מנוע 1.5 eTSI (קוד DXD ברישיון) לטבלת היבואן '1.5 ל' בנזין'; התוכן זהה לקובץ טיגואן 1.5."))
save(clone('skoda-octavia-2015-2024-2.0-tdi', id='vw-passat-2015-2018-2.0-tdi', make='Volkswagen', make_he='פולקסווגן',
           model='Passat', model_he='פאסאט', generation='B8', years=[2015, 2018], engines=['2.0 TDI (CRL/DFG)'],
           extra_note="קובץ זה משייך את פאסאט B8 עם מנוע 2.0 TDI ממשפחת EA288 (קודי CRL/DFG ברישיון, לפי אינדקס ספרי התיקון) לטבלת היבואן '2.0 ל' דיזל'; התוכן זהה לקובץ אוקטביה 2.0 TDI."))
d = clone('skoda-superb-2021-2024-1.4-phev', id='skoda-octavia-2021-2023-1.4-phev', model='Octavia', model_he='אוקטביה',
          generation='IV (NX), iV היברידי נטען', years=[2021, 2023], engines=['1.4 TSI PHEV (DGE)'],
          extra_note="קובץ זה משייך את אוקטביה iV (קוד DGE ברישיון, שם רישוי OCTAVIA IV) לטבלת היבואן ל-1.4 PHEV; התוכן זהה לקובץ סופרב iV.")
save(d)
idsrc = load('vw-id4-id5-2022-2026-ev')
save(clone('vw-id4-id5-2022-2026-ev', id='vw-id7-2024-2026-ev', model='ID.7', model_he='ID.7', generation='ED', years=[2024, 2026],
           engines=['חשמלי (EDF)'], extra_note="קובץ זה משייך את ID.7 לטבלת היבואן 'BEV חשמלי' (הטבלה כללית לכל הרכבים החשמליים של צ'מפיון)."))
save(clone('vw-id4-id5-2022-2026-ev', id='cupra-tavascan-2025-2026-ev', make='Cupra', make_he='קופרה', model='Tavascan', model_he='טבסקן',
           generation='KR', years=[2025, 2026], engines=['חשמלי (EDD/EDF)'],
           extra_note="קובץ זה משייך את קופרה טבסקן (מיובאת ע\"י צ'מפיון) לטבלת היבואן 'BEV חשמלי'."))

# ---------------- B. new files built straight from a Champion table ----------------
def grid(table):
    t = R[table]; rows = {r[0]: (r[1], r[2]) for r in t['rows']}
    return t, rows
def kms(step, n): return [step * (i + 1) for i in range(n)]

def build_from(table, step, n, mapping, base, li, notes, srcs):
    """mapping: list of (row_name, item, note_or_None); marks R->replace I->inspect."""
    t, rows = grid(table)
    K = kms(step, n)
    services = {k: [] for k in K}
    used = set()
    for row, item, note in mapping:
        tip, cells = rows[row]; used.add(row)
        if len(cells) == 1 and cells[0].startswith('['): continue  # whole-row text -> long_interval (given in li)
        assert len(cells) == n, (row, len(cells))
        for k, c in zip(K, cells):
            if c in 'RI':
                it = {"item": item, "action": "replace" if c == 'R' else "inspect"}
                if note: it["note"] = note
                services[k].append(it)
    missing = [r for r in rows if r not in used]
    assert not missing, ('rows not mapped', table, missing)
    d = dict(base)
    d['services'] = [{"km": k, "items": v} for k, v in services.items()]
    d['long_interval'] = li; d['time_based'] = []
    d['notes'] = notes; d['sources'] = srcs; d['status'] = 'reviewed'
    return d

PADS = "קדמיות ואחוריות, כולל מצב הדיסקים"
# 2.5 TFSI (RS3 / RSQ3)
m25 = [("שמן מנוע", "engine_oil", None), ("מסנן שמן מנוע", "oil_filter", None),
       ("מסנן אוויר", "air_filter", "או כל שנתיים, המוקדם"), ("מסנן אבקנים (מיזוג)", "cabin_filter", "או כל שנה, המוקדם"),
       ("מצתים", "spark_plugs", "או כל 4 שנים, המוקדם"),
       ("שמן תיבת הילוכים", "dct_oil", "תיבת DSG רטובה 7 הילוכים (DQ500)"),
       ("שמן Bevel Box", "transfer_case_oil", None), ("שמן מצמד הנעה כפולה (הלדקס)", "differential_oil", None),
       ("נוזל בלמים", "brake_fluid", None),
       ("רפידות וצלחות בלמים קדמיות", "brake_pads", PADS), ("רפידות וצלחות בלמים אחוריות", "brake_discs", None)]
base = {"id": "audi-rs3-rsq3-2016-2026-2.5-tfsi", "make": "Audi", "make_he": "אאודי", "model": "RS3 / RS Q3", "model_he": "RS3 / RS Q3",
        "generation": "RS3 8V/8Y, RS Q3 F3", "years": [2016, 2026], "engines": ["2.5 TFSI R5 (CZG/DAZ/DNW)"], "fuel": "petrol",
        "importer": "צ'מפיון מוטורס",
        "interval": {"km": 15000, "months": 12, "note": "לפי טבלת צ'מפיון: טיפול כל 15,000 ק\"מ; מסנן המזגן מוחלף לפחות פעם בשנה"},
        "cycle_km": 120000}
li = [{"item": "transfer_case_oil", "action": "replace", "every_months": 36, "note": "שמן ממסרת הזווית (Bevel Box) של ההנעה הכפולה: לפי היבואן כל 3 שנים"},
      {"item": "differential_oil", "action": "replace", "every_months": 24, "note": "שמן מצמד ההנעה הכפולה (הלדקס): לפי היבואן כל שנתיים"},
      {"item": "air_filter", "action": "replace", "every_months": 24}, {"item": "cabin_filter", "action": "replace", "every_months": 12},
      {"item": "spark_plugs", "action": "replace", "every_months": 48}]
notes = ("הלוח הועתק מטבלת '2.5 ל' בנזין' בשגרת הטיפולים של צ'מפיון מוטורס, יבואנית אאודי. המנוע היחיד בנפח 2.5 ליטר בדגמי אאודי בישראל הוא ה-2.5 TFSI בעל 5 הצילינדרים "
         "של RS3 ו-RS Q3 (קודי CZG/DAZ/DNW ברישיון; DAZ ו-DNW הם דור EA855 evo). לפי הטבלה: שמן ומסנן בכל טיפול, מסנני אוויר ומזגן כל 30,000, מצתים ונוזל בלמים ב-60,000 וב-120,000, "
         "שמן תיבת DSG רטובה (DQ500) ב-120,000, שמן ממסרת הזווית כל 3 שנים ושמן הלדקס כל שנתיים. בטבלה אין שורת רצועת תזמון (שרשרת) ואין רצועת אביזרים. "
         "רפידות ודיסקים נבדקים בכל טיפול. היבואן מציין שהטבלה כללית לדגמים נפוצים מהשנים האחרונות; ה-RS3 משנת 2016 (CZG) משויך אליה לפי נפח המנוע.")
d = build_from('1-5', 15000, 8, m25, base, li, notes, [champ_src("2.5 ל' בנזין"), VWTS_P,
    {"url": "https://www.proxyparts.com/car-parts-stock/information/engine-code/dnwa/part/engine/partid/17839339/", "kind": "other",
     "note": "שיוך קוד המנוע DNWA למנוע 2.5 TFSI של RS3 (מאגר חלקי חילוף)"}])
# brake discs: the table row is 'pads and discs'; emit discs alongside pads for every inspect mark
for s in d['services']:
    s['items'] = [i for i in s['items'] if not (i['item'] == 'brake_discs')]
    if any(i['item'] == 'brake_pads' for i in s['items']):
        s['items'].append({"item": "brake_discs", "action": "inspect"})
save(d)

# 3.0 TFSI V6 (EA839): Q7/Q8 55 TFSI, SQ5, S5, A8
m30 = [("שמן מנוע", "engine_oil", None), ("מסנן שמן מנוע", "oil_filter", None),
       ("מסנן אוויר", "air_filter", "או כל שנתיים, המוקדם"), ("מסנן אבקנים (מיזוג)", "cabin_filter", "או כל שנה, המוקדם"),
       ("מצתים", "spark_plugs", "או כל 4 שנים, המוקדם"),
       ("שמן תיבת הילוכים", "transmission_oil", "תיבת הילוכים אוטומטית"),
       ("נוזל בלמים", "brake_fluid", None), ("רצועת אביזרים", "drive_belt", None),
       ("רפידות וצלחות בלמים קדמיות", "brake_pads", PADS), ("רפידות וצלחות בלמים אחוריות", "brake_discs", None)]
base = {"id": "audi-q7-q8-sq5-s5-2018-2026-3.0-tfsi", "make": "Audi", "make_he": "אאודי", "model": "Q7 / Q8 / SQ5 / S5 / A8", "model_he": "Q7 / Q8 / SQ5 / S5 / A8",
        "generation": "Q7 4M, Q8 4M, SQ5 FY, S5 F5, A8 D5", "years": [2018, 2026], "engines": ["3.0 TFSI V6 EA839 (CWG/CZS/DCB)"], "fuel": "petrol",
        "importer": "צ'מפיון מוטורס",
        "interval": {"km": 15000, "months": 12, "note": "לפי טבלת צ'מפיון: טיפול כל 15,000 ק\"מ; מסנן המזגן מוחלף לפחות פעם בשנה"},
        "cycle_km": 120000}
li = [{"item": "brake_fluid", "action": "replace", "every_months": 24, "note": "לפי היבואן: כל שנתיים"},
      {"item": "air_filter", "action": "replace", "every_months": 24}, {"item": "cabin_filter", "action": "replace", "every_months": 12},
      {"item": "spark_plugs", "action": "replace", "every_months": 48}]
notes = ("הלוח הועתק מטבלת '3.0 ל' בנזין' בשגרת הטיפולים של צ'מפיון מוטורס. קודי המנוע CWG/CZS/DCB הם מנוע 3.0 TFSI V6 ממשפחת EA839 (לפי אינדקס ספרי התיקון). "
         "לפי הטבלה: שמן ומסנן בכל טיפול, מסנני אוויר ומזגן כל 30,000, רצועת אביזרים ב-60,000 וב-120,000, שמן תיבת ההילוכים ב-120,000 ונוזל בלמים כל שנתיים. "
         "המצתים מסומנים בטבלה ב-30,000, 60,000 ו-90,000 ולא ב-120,000; הסימון הועתק כמו שהוא, וכדאי לוודא במוסך את המרווח לרכב הספציפי. "
         "רפידות ודיסקים נבדקים בכל טיפול. הקובץ חל על גרסאות הבנזין בלבד; גרסאות ההיברידי הנטען (TFSI e) אינן בטבלה זו.")
d = build_from('1-6', 15000, 8, m30, base, li, notes, [champ_src("3.0 ל' בנזין"), VWTS_P])
for s in d['services']:
    s['items'] = [i for i in s['items'] if not (i['item'] == 'brake_discs')]
    if any(i['item'] == 'brake_pads' for i in s['items']):
        s['items'].append({"item": "brake_discs", "action": "inspect"})
save(d)

# Crafter 2.0 TDI (20,000 km grid to 240,000)
mcr = [("שמן מנוע", "engine_oil", None), ("מסנן שמן מנוע", "oil_filter", None),
       ("מסנן אוויר וניקוי בית מסנן", "air_filter", None), ("מסנן אבקנים (מיזוג)", "cabin_filter", None),
       ("מסנן סולר", "fuel_filter", None), ("שמן תיבת הילוכים + מסנן", "transmission_oil", "כולל מסנן"),
       ("רצועת תזמון + מותחן + גלגלת סרק", "timing_belt", "כולל מותחן וגלגלת סרק; בדגמים מתאריך ייצור 1.2.2022, לפי קוד המנוע"),
       ("רצועת מנוע", "drive_belt", "ברכב עם מדחס או אלטרנטור נוסף שהותקנו בארץ מחליפים גם מותחן וגלגלות"),
       ("רפידות וצלחות בלמים קדמיות", "brake_pads", "רפידות ודיסקים קדמיים"), ("רפידות וצלחות בלמים אחוריות", "brake_pads", "רפידות ודיסקים אחוריים")]
base = {"id": "vw-crafter-2022-2026-2.0-tdi", "make": "Volkswagen", "make_he": "פולקסווגן", "model": "Crafter", "model_he": "קראפטר",
        "generation": "SY/SZ", "years": [2022, 2026], "engines": ["2.0 TDI EA288 (DMZ)"], "fuel": "diesel",
        "importer": "צ'מפיון מוטורס",
        "interval": {"km": 20000, "months": 12, "note": "לפי טבלת צ'מפיון לרכב מסחרי Crafter: טיפול כל 20,000 ק\"מ. הטבלה לפי ק\"מ בלבד; 12 החודשים הם ערך ברירת מחדל של האפליקציה ולא מהטבלה"},
        "cycle_km": 240000}
li = [{"item": "air_filter", "action": "replace", "every_km": 30000, "every_months": 24, "note": "כולל ניקוי בית המסנן"},
      {"item": "cabin_filter", "action": "replace", "every_km": 30000, "every_months": 12}]
notes = ("הלוח הועתק מטבלת 'Crafter' בשגרת הטיפולים של צ'מפיון מוטורס (רכב מסחרי): טיפול כל 20,000 ק\"מ עד 240,000. קוד המנוע DMZ הוא 2.0 TDI EA288 למסחריות. "
         "לפי הטבלה: שמן ומסנן בכל טיפול; מסנני אוויר ומזגן לפי 30,000 ק\"מ (ולכן בלוח ארוך הטווח); מסנן סולר ב-100,000 וב-200,000; שמן תיבת ההילוכים עם מסנן ב-200,000; "
         "רצועת אביזרים ב-60,000, 120,000 ו-180,000; רצועת התזמון נבדקת ב-40,000, 120,000 ו-200,000 ומוחלפת ב-80,000, 160,000 ו-240,000. "
         "לפי הערת היבואן משטר רצועת התזמון תלוי בקוד המנוע וחל מתאריך ייצור 1.2.2022, ולכן הקובץ משויך לשנים 2022 ואילך. "
         "הרפידות והדיסקים נבדקים בכל טיפול, ובטבלה הרפידות הקדמיות מסומנות להחלפה ב-240,000. בטבלה אין שורת נוזל בלמים.")
d = build_from('2-3', 20000, 12, mcr, base, li, notes, [champ_src("Crafter"), VWTS_D])
save(d)

# Amarok 2023 (20,000 km grid to 320,000)
mam = [("שמן מנוע", "engine_oil", None), ("מסנן שמן מנוע", "oil_filter", None),
       ("מסנן אוויר וניקוי בית מסנן", "air_filter", "כולל ניקוי בית המסנן; או כל שנתיים"), ("מסנן אבקנים (מיזוג)", "cabin_filter", None),
       ("מסנן סולר", "fuel_filter", "או כל 10 שנים"), ("שמן תיבת הילוכים + מסנן", "transmission_oil", "כולל מסנן, לפי קוד התיבה; או כל 10 שנים"),
       ("שמן סרנים קדמי + אחורי", "differential_oil", "סרן קדמי ואחורי; או כל 10 שנים"), ("שמן תיבת העברה", "transfer_case_oil", "או כל 10 שנים"),
       ("רצועת תזמון + מותחן + גלגלת סרק", "timing_belt", "כולל מותחן וגלגלת סרק; או כל 10 שנים"), ("רצועת מנוע", "drive_belt", "או כל 10 שנים"),
       ("נוזל קירור", "coolant", "או כל 10 שנים"), ("שמן בלמים", "brake_fluid", None),
       ("רפידות וצלחות בלמים קדמיות", "brake_pads", PADS), ("רפידות וצלחות בלמים אחוריות", "brake_discs", None)]
base = {"id": "vw-amarok-2023-2026-diesel", "make": "Volkswagen", "make_he": "פולקסווגן", "model": "Amarok", "model_he": "אמרוק",
        "generation": "דור 2 (2023)", "years": [2023, 2026], "engines": ["דיזל (קוד BF ברישיון)"], "fuel": "diesel",
        "importer": "צ'מפיון מוטורס",
        "interval": {"km": 20000, "months": 12, "note": "לפי טבלת צ'מפיון 'Amarok 2023': טיפול כל 20,000 ק\"מ. הטבלה לפי ק\"מ בלבד; 12 החודשים הם ערך ברירת מחדל של האפליקציה ולא מהטבלה"},
        "cycle_km": 320000}
li = [{"item": "brake_fluid", "action": "replace", "every_months": 36, "note": "לפי היבואן: כל 3 שנים"},
      {"item": "air_filter", "action": "replace", "every_months": 24},
      {"item": "fuel_filter", "action": "replace", "every_months": 120},
      {"item": "timing_belt", "action": "replace", "every_months": 120, "note": "או לפי ק\"מ (240,000), המוקדם"},
      {"item": "coolant", "action": "replace", "every_months": 120, "note": "או לפי ק\"מ (320,000), המוקדם"}]
notes = ("הלוח הועתק מטבלת 'Amarok 2023' בשגרת הטיפולים של צ'מפיון מוטורס (אמרוק מהדור השני): טיפול כל 20,000 ק\"מ עד 320,000. "
         "לפי הטבלה: שמן ומסנן בכל טיפול; מסנן אוויר כל 40,000 (או שנתיים); מסנן סולר כל 60,000; שמן תיבת ההילוכים עם מסנן, שמן הסרנים, שמן תיבת ההעברה, רצועת התזמון ורצועת המנוע ב-240,000; "
         "נוזל קירור ב-320,000; כל אלה 'או 10 שנים'. נוזל בלמים כל 3 שנים. "
         "סימוני מסנן המזגן בטבלה אינם סדירים אחרי 160,000 (מסומן ב-160,000 וגם ב-180,000, וב-260,000 וגם ב-280,000); הם הועתקו כמו שהם. "
         "לפי הערת היבואן נתוני רצועת התזמון מותאמים לקוד מנוע מסוים נכון לאוקטובר 2024, ולכן כדאי לוודא במוסך לפי קוד המנוע של הרכב. רפידות ודיסקים נבדקים בכל טיפול. "
         "הקובץ משויך לאמרוק משנת 2023 (קוד BF ברישיון); לאמרוק מהדור הקודם (V6 TDI) אין טבלה אצל היבואן.")
d = build_from('2-2', 20000, 16, mam, base, li, notes, [champ_src("Amarok 2023")])
for s in d['services']:
    s['items'] = [i for i in s['items'] if not (i['item'] == 'brake_discs')]
    if any(i['item'] == 'brake_pads' for i in s['items']):
        s['items'].append({"item": "brake_discs", "action": "inspect"})
save(d)

# ---------------- C. small clones ----------------
save(clone('skoda-superb-2021-2024-1.4-phev', id='audi-q3-sportback-2023-2024-1.4-phev', make='Audi', make_he='אאודי', model='Q3 Sportback TFSI e', model_he='Q3 ספורטבק היברידי נטען',
           generation='F3', years=[2023, 2024], engines=['1.4 TFSI PHEV (DGE)'],
           extra_note="קובץ זה משייך את Q3 ספורטבק 45 TFSI e (קוד DGE ברישיון) לטבלת היבואן ל-1.4 PHEV, יחד עם סקודה סופרב/אוקטביה iV עם אותו מנוע."))
