from gen import *
from psa import SAM, FIA, JEP, PEU, CIT, OPL, LUB, SRC_LUB, SRC_OPEL_F

U = 'https://samelet.com/wp-content/uploads/'
F500 = U + '2023/11/Fiat_500_500C_carbook_042021-1.pdf'
TIPO = U + '2023/11/Tipo-hebrew-4P-low.pdf'
X500 = U + '2023/11/Fiat-500X.pdf'
CMP21 = U + '2023/11/Jeep_Compass_carbook_042021.pdf'
CMP26 = U + '2023/11/260345-Jeep-Compass-OM-2026-8-6-26-S2.pdf'
WRG = U + '2024/02/../2023/11/Jeep_Wrangler_2022_-carbook_072022.pdf'
WRG = U + '2023/11/Jeep_Wrangler_2022_-carbook_072022.pdf'

def odd(step, k):  # 1st, 3rd, 5th ... service
    return (k // step) % 2 == 1

# ------------------------------------------------ Fiat 500 / Panda 1.2 8V (169A4000)
def g500():
    out = []
    for n in range(1, 9):
        km = 15000 * n
        its = [I('tires'), I('lights'), I('coolant', 'מפלס'), I('brake_fluid', 'מפלס'), I('washer_fluid'),
               I('battery_12v'), I('exhaust', 'פליטה/עשן'), I('diagnostics'), I('brake_pads'), I('brake_discs'), I('brake_drums')]
        if km % 30000 == 0:
            its += [I('body_underside', 'כולל צנרת וחלקי גומי'), I('fuel_lines'), I('brake_lines'), I('cv_boots'),
                    I('wipers'), C('door_hinges', 'מנעולי מכסה מנוע ותא מטען'), I('parking_brake'),
                    R('engine_oil'), R('oil_filter'), R('spark_plugs'), R('air_filter'), R('brake_fluid'), R('cabin_filter'),
                    I('drive_belt', 'בדיקת מתיחה')]
        else:
            its += [R('cabin_filter', 'מומלץ (לא חובה) בטיפולי הביניים')]
        if km % 60000 == 0:
            its += [I('timing_belt'), I('valve_clearance', 'בדיקה וכיוון')]
        out.append((km, its))
    return out

PLAN_500 = {
    'interval': {'km': 15000, 'months': 12, 'note': 'לפי ספר הרכב העברי: טיפול כל 15,000 ק"מ או שנה; שמן ומסנן כל 30,000 ק"מ, ובנסיעה עירונית או פחות מ-10,000 ק"מ בשנה - כל שנה'},
    'cycle_km': 120000, 'grid': g500(),
    'long': [LI('timing_belt', 'replace', every_km=120000, every_months=72, note='באזור מאובק או בתנאים קשים: 60,000 ק"מ או 4 שנים'),
             LI('drive_belt', 'replace', every_km=120000, every_months=72, note='באזור מאובק או בתנאים קשים: 60,000 ק"מ או 4 שנים'),
             LI('brake_fluid', 'replace', every_months=24)],
    'specs': {'fuel': 'בנזין 95 אוקטן לפחות, מיכל 35 ליטר', 'engine_oil': 'Selenia (Petronas) לפי טבלת הקיבולים בספר',
              'timing': 'רצועת תזמון: 120,000 ק"מ או 6 שנים (בתנאים קשים 60,000/4 שנים)'},
    'sources': [{'url': F500, 'kind': 'importer', 'note': 'ספר רכב עברי פיאט 500/500C (סמלת, 04/2021), תכנית טיפולים לגרסאות בנזין עמ\' 118-120 (PDF 119-121)'}],
    'status': 'reviewed',
    'notes': 'לפי ספר הרכב העברי של סמלת. בכל טיפול (15,000 ק"מ או שנה): בדיקות צמיגים, תאורה, נוזלים, בלמים וקריאת מחשב. כל 30,000: שמן ומסנן, מצתים, מסנן אוויר, מסנן מזגן ונוזל בלמים, ובדיקת גחון, צנרת ומגבים; מי שנוסע מעט או בעיר מחליף שמן כל שנה. ב-60,000 וב-120,000: בדיקת רצועת תזמון וכיוון שסתומים (מנוע 1.2 8V). רצועת תזמון ורצועת אביזרים: 120,000 ק"מ או 6 שנים. באזור מאובק מסנן מזגן כל 15,000.'
}

# ------------------------------------------------ Tipo 1.6 E.torQ (55268036)
def gtipo():
    out = []
    for n in range(1, 9):
        km = 15000 * n
        its = [I('tires'), I('lights'), I('coolant', 'מפלס'), I('brake_fluid', 'מפלס'), I('exhaust', 'פליטה/עשן'),
               I('diagnostics'), I('brake_pads'), I('brake_discs'), I('brake_drums'), I('drive_belt', 'מצב ומתיחה'),
               R('engine_oil'), R('oil_filter')]
        if km % 30000 == 0:
            its += [I('body_underside', 'כולל צנרת וחלקי גומי'), I('fuel_lines'), I('brake_lines'), I('cv_boots'), I('wipers'),
                    C('door_hinges', 'מנעולים'), I('parking_brake'), R('spark_plugs'), R('brake_fluid'), R('cabin_filter')]
        else:
            its += [R('cabin_filter', 'מומלץ (לא חובה) בטיפולי הביניים')]
        if km % 45000 == 0:
            its += [R('air_filter')]
        out.append((km, its))
    return out

PLAN_TIPO = {
    'interval': {'km': 15000, 'months': 12, 'note': 'לפי ספר הרכב העברי: טיפול כל 15,000 ק"מ או שנה; אחרי 120,000 ק"מ/8 שנים חוזרים על התכנית מתחילתה'},
    'cycle_km': 120000, 'grid': gtipo(),
    'long': [LI('drive_belt', 'replace', every_months=48, note='כל 4 שנים; באזור מאובק או בתנאים קשים לא יותר מ-60,000 ק"מ'),
             LI('brake_fluid', 'replace', every_months=24),
             LI('transmission_oil', 'replace', every_km=90000, every_months=24, note='רק בתיבה אוטומטית AT6 בתנאי שימוש קשים (עיר, נסיעות קצרות, גרירה)')],
    'specs': {'fuel': 'בנזין 95 אוקטן', 'timing': 'שרשרת תזמון (מנוע 1.6 E.torQ), אין החלפה מתוכננת בספר'},
    'sources': [{'url': TIPO, 'kind': 'importer', 'note': 'ספר רכב עברי פיאט טיפו 4 דלתות (סמלת), תכנית טיפולים למנועי בנזין עמ\' 129-131 (PDF 130-132), קוד מנוע 55268036 = 1.6 E.torQ בעמ\' 155'}],
    'status': 'reviewed',
    'notes': 'לפי ספר הרכב העברי של סמלת לטיפו עם מנוע 1.6 E.torQ. בכל טיפול: שמן ומסנן, בדיקת רצועת אביזרים, בלמים, צמיגים ותאורה. כל 30,000: מצתים, נוזל בלמים ומסנן מזגן, ובדיקת גחון וצנרת. מסנן אוויר כל 45,000. רצועת אביזרים כל 4 שנים. לגיר האוטומטי AT6 הספר מורה להחליף שמן ומסננים כל 90,000 ק"מ או שנתיים רק בשימוש קשה. בגרסת 1.4 16V 95 כ"ס (לא נפוצה בישראל) יש רצועת תזמון - 120,000 ק"מ/6 שנים.'
}

# ------------------------------------------------ 500X / Renegade / Compass 1.4 MultiAir
def g500x():
    out = []
    for n in range(1, 9):
        km = 15000 * n
        its = [I('tires'), I('lights'), I('coolant', 'מפלס'), I('brake_fluid', 'מפלס'), I('exhaust', 'פליטה/עשן'),
               I('diagnostics'), I('brake_pads'), I('brake_discs')]
        if km % 30000 == 0:
            its += [I('body_underside', 'כולל צנרת וחלקי גומי'), I('fuel_lines'), I('brake_lines'), I('cv_boots'),
                    C('door_hinges', 'מנעולים'), R('engine_oil'), R('oil_filter'), R('spark_plugs'), R('air_filter'),
                    R('brake_fluid'), R('cabin_filter')]
        else:
            its += [I('wipers'), R('cabin_filter', 'מומלץ (לא חובה) בטיפולי הביניים')]
        if km % 60000 == 0:
            its += [I('drive_belt'), I('timing_belt')]
        out.append((km, its))
    return out

PLAN_500X = {
    'interval': {'km': 15000, 'months': 12, 'note': 'לפי ספר הרכב העברי: טיפול כל 15,000 ק"מ או שנה; שמן ומסנן כל 30,000 ק"מ, ומי שנוסע פחות מ-10,000 ק"מ בשנה - כל שנה'},
    'cycle_km': 120000, 'grid': g500x(),
    'long': [LI('timing_belt', 'replace', every_km=120000, every_months=72, note='באזור מאובק או בתנאים קשים: 60,000 ק"מ או 4 שנים'),
             LI('drive_belt', 'replace', every_km=120000, every_months=72, note='באזור מאובק או בתנאים קשים: 60,000 ק"מ או 4 שנים'),
             LI('brake_fluid', 'replace', every_months=24)],
    'specs': {'oil_capacity': '3.2 ליטר (1.4 Turbo MultiAir)', 'coolant': 'Paraflu Up מהול 50%, 5.2 ליטר', 'fuel': 'בנזין 95, מיכל 48 ליטר',
              'timing': 'רצועת תזמון: 120,000 ק"מ או 6 שנים (בתנאים קשים 60,000/4 שנים)'},
    'sources': [{'url': X500, 'kind': 'importer', 'note': 'ספר רכב עברי פיאט 500X (סמלת), תכנית טיפולים ל-1.4 Turbo MultiAir עמ\' 158-160, קוד מנוע 55263624 בעמ\' 183'}],
    'status': 'reviewed',
    'notes': 'לפי ספר הרכב העברי של סמלת ל-500X עם מנוע 1.4 טורבו MultiAir. בכל טיפול (15,000/שנה): בדיקות צמיגים, תאורה, נוזלים, בלמים ומחשב. כל 30,000: שמן ומסנן, מצתים, מסנני אוויר ומזגן ונוזל בלמים. ב-60,000 וב-120,000 בדיקת רצועות. רצועת תזמון ורצועת אביזרים: 120,000 ק"מ או 6 שנים. מי שנוסע פחות מ-10,000 ק"מ בשנה מחליף שמן כל שנה.'
}

# ------------------------------------------------ Compass 2021-2024 1.3 T4 (55282328)
def gcmp():
    out = []
    for n in range(1, 17):
        km = 15000 * n
        its = [('tire_rotation', 'rotate', None), R('air_filter', 'באזור מאובק - כל 15,000'), I('diagnostics', 'מערכת ניהול מנוע, פליטה ובלאי שמן'),
               R('engine_oil', 'לפי מחוון השירות, ולא יותר משנה'), R('oil_filter')]
        if n % 2 == 1:
            its += [I('brake_pads'), I('suspension', 'מתלים קדמיים, מוטות וגומיות'), I('cv_boots'), R('cabin_filter')]
        else:
            its += [I('body_underside', 'כולל צנרת פליטה, דלק ובלמים וחלקי גומי'), I('exhaust'), I('fuel_lines'), I('brake_lines'),
                    R('brake_fluid', 'כל 24 חודשים')]
        if km % 60000 == 0:
            its += [R('spark_plugs')]
        if km in (60000, 180000):
            its += [I('drive_belt')]
        if km in (30000, 150000):
            its += [I('drive_belt', 'בדיקת מתיחה (דגמים בלי מותחן אוטומטי)')]
        if km in (120000, 240000):
            its += [I('dct_oil', 'מפלס שמן במפעיל האלקטרו-הידראולי (גיר כפול מצמד)')]
        out.append((km, its))
    return out

PLAN_CMP21 = {
    'interval': {'km': 15000, 'months': 12, 'note': 'לפי ספר הרכב העברי: טיפול כל 15,000 ק"מ או שנה; החלפת שמן לפי מחוון השירות ולא יאוחר משנה'},
    'cycle_km': 240000, 'grid': gcmp(),
    'long': [LI('drive_belt', 'replace', every_km=120000, every_months=72, note='באזור מאובק או בתנאים קשים: 60,000 ק"מ או 4 שנים'),
             LI('brake_fluid', 'replace', every_months=24)],
    'specs': {'oil_capacity': '4.5 ליטר (1.3 T4)', 'coolant': 'Paraflu Up מהול 50%, 7.5 ליטר', 'fuel': 'בנזין 95, מיכל 55 ליטר',
              'brake_fluid': 'DOT 4'},
    'sources': [{'url': CMP21, 'kind': 'importer', 'note': 'ספר רכב עברי ג\'יפ קומפאס (סמלת, 04/2021), תכנית טיפולים למנועי בנזין עמ\' 211-213 (PDF 212-214), קוד מנוע 55282328 בעמ\' 230'}],
    'status': 'reviewed',
    'notes': 'לפי ספר הרכב העברי של סמלת לקומפאס עם מנוע 1.3 טורבו (130/150 כ"ס). בכל טיפול (15,000 ק"מ/שנה): שמן ומסנן לפי מחוון השירות, מסנן אוויר, סבב צמיגים וקריאת מחשב. בטיפולים האי-זוגיים (15, 45, 75...): בדיקת רפידות, מתלים ומפרקים והחלפת מסנן מזגן. בטיפולים הזוגיים (30, 60...): בדיקת גחון וצנרת והחלפת נוזל בלמים (כל שנתיים). מצתים כל 60,000. רצועת אביזרים 120,000 ק"מ או 6 שנים. שמן מפעיל גיר כפול מצמד נבדק ב-120,000 וב-240,000.'
}

# ------------------------------------------------ EB2 1.2 turbo MHEV (Compass 2026 Israeli book)
MH_EVERY = [I('lights', 'כולל חלונות, מראות ועדשות'), I('wipers', 'כולל מתזים'), I('parking_brake'), I('pedals'),
            I('diagnostics', 'קריאת זיכרון תקלות ואיפוס מחוון'), R('cabin_filter'), I('brake_pads'), I('brake_discs'),
            I('brake_lines'), I('cv_boots', 'כולל מפרקים ומסרק הגה'), I('steering', 'חופשים במפרקים ובמוטות'),
            I('suspension', 'אטימות בולמים'), I('tires'), I('body_underside', 'כולל מגני גחון, חלקי גומי וצנרת'),
            I('exhaust'), I('fuel_lines'), I('coolant_hoses'), I('battery_12v'), R('engine_oil'), R('oil_filter'),
            I('washer_fluid'), I('brake_fluid', 'מפלס')]
PLAN_MHEV = {
    'interval': {'km': 15000, 'months': 12, 'note': 'לפי ספר הרכב העברי של קומפאס 2026 (סמלת), תכנית EB2T MHEV: טיפול כל 15,000 ק"מ או שנה'},
    'cycle_km': 180000, 'grid': grid(15000, 12, MH_EVERY),
    'long': [LI('tire_rotation', 'rotate', every_km=10000, note='או כשהפרש עומק החריצים 1.5 מ"מ ומעלה'),
             LI('spark_plugs', 'replace', every_km=20000, every_months=48),
             LI('air_filter', 'replace', every_km=20000, every_months=48),
             LI('coolant', 'inspect', first_km=120000, first_months=48, then_every_km=15000, then_every_months=12, note='בדיקת pH; החלפה מתחת ל-6.3'),
             LI('coolant', 'replace', every_km=160000, every_months=120),
             LI('brake_fluid', 'replace', every_months=24),
             LI('drive_belt', 'replace', first_km=120000, first_months=72, then_every_km=240000, then_every_months=144),
             LI('timing_belt', 'replace', every_km=240000, every_months=144, note='ערכת רצועות מנוע ואביזרים; רצועת משאבת המים מוחלפת כל 120,000 ק"מ או 6 שנים')],
    'specs': {'timing': 'לפי הספר: ערכת רצועות מנוע כל 240,000 ק"מ/12 שנים, רצועת משאבת מים כל 120,000/6 שנים'},
    'sources': [{'url': CMP26, 'kind': 'importer', 'note': 'ספר רכב עברי ג\'יפ קומפאס 2026 (סמלת, 06/2026), "EB2T MHEV - תוכנית טיפולים" עמ\' 198-200 (PDF 199-201)'}],
    'status': 'reviewed',
    'notes': 'לפי ספר הרכב העברי של סמלת לקומפאס 2026 עם מנוע 1.2 טורבו היברידי מתון (EB2T MHEV). בכל טיפול (15,000 ק"מ/שנה): שמן ומסנן, מסנן מזגן (מומלץ גם כל חצי שנה), ובדיקות בלמים, מתלים, צמיגים, גחון, מצבר וקריאת מחשב. מצתים ומסנן אוויר כל 20,000 ק"מ או 4 שנים, סבב צמיגים כל 10,000. נוזל קירור: בדיקת pH מ-120,000/4 שנים, החלפה 160,000/10 שנים. רצועת אביזרים לראשונה ב-120,000/6 שנים ואז כל 240,000; רצועת משאבת המים כל 120,000/6 שנים; ערכת רצועות המנוע כל 240,000/12 שנים. נוזל ומסנן גיר DCT מוחלפים פעם אחת בחיי הרכב, ב-90,000 ק"מ. נוזל בלמים כל שנתיים.'
}

# ------------------------------------------------ Wrangler JL 2.0 turbo (Israeli book)
def gwr():
    out = []
    for n in range(1, 21):
        km = 12000 * n
        its = [R('engine_oil'), R('oil_filter'), ('tire_rotation', 'rotate', None), I('door_hinges', 'סיכוך בריחי הדלתות'),
               I('air_filter', 'באזור מאובק או בשטח: בדיקה והחלפה לפי הצורך'), I('propshaft', 'מפרקים אוניברסליים / מהירות קבועה')]
        if km % 24000 == 0:
            its += [I('brake_pads'), I('body_underside', 'כולל צנרת פליטה, דלק ובלמים וחלקי גומי'), I('fuel_lines'), I('brake_lines'), R('brake_fluid', 'כל 24 חודשים')]
        if km % 36000 == 0:
            its += [I('exhaust'), I('suspension', 'מתלה קדמי, מוטות, אטמים ומתלה אחורי'), I('steering')]
        if km % 48000 == 0:
            its += [I('differential_oil', 'החלפה בשימוש קשה (שטח, גרירה, מונית)'), A('parking_brake', 'בלמי דיסק בארבעה גלגלים'), R('air_filter')]
        if km in (48000, 144000, 240000):
            its += [I('transfer_case_oil')]
        if km % 60000 == 0:
            its += [R('spark_plugs', 'מנוע 2.0')]
        if km == 192000:
            its += [R('drive_belt')]
        if km in (96000, 192000):
            its += [R('transfer_case_oil', 'רק בשימוש קשה (ניידת, מונית, גרירה תכופה)')]
        if km == 144000:
            its += [I('pcv_valve', 'מומלץ, לא חובה')]
        out.append((km, its))
    return out

PLAN_WR = {
    'interval': {'km': 12000, 'months': 12, 'note': 'לפי ספר הרכב העברי: עמודות של 12,000 ק"מ או 12 חודשים, המוקדם; בתנאים קשים שמן ומסנן כל 7,500 ק"מ או 6 חודשים'},
    'cycle_km': 240000, 'grid': gwr(),
    'long': [LI('cabin_filter', 'replace', every_km=19000),
             LI('coolant', 'replace', every_km=240000, every_months=120, note='שטיפה והחלפה, כולל נוזל הקירור של היחידה החשמלית'),
             LI('brake_fluid', 'replace', every_months=24)],
    'specs': {'brake_fluid': 'DOT 4'},
    'sources': [{'url': WRG, 'kind': 'importer', 'note': 'ספר רכב עברי ג\'יפ רנגלר 2022 (סמלת, 07/2022), תכנית תחזוקה עמ\' 391-394 (PDF 392-395)'}],
    'status': 'reviewed',
    'notes': 'לפי ספר הרכב העברי של סמלת לרנגלר JL. בכל 12,000 ק"מ או שנה: שמן ומסנן, סבב צמיגים ובדיקת מפרקים. כל 24,000: רפידות, גחון וצנרת, ונוזל בלמים (כל שנתיים). כל 36,000: מערכת פליטה ומתלים. כל 48,000: מסנן אוויר, בדיקת שמן סרנים וכיוון בלם חניה. מסנן מזגן כל 19,000. מצתים (מנוע 2.0) כל 60,000. רצועת אביזרים ב-192,000. נוזל קירור כל 10 שנים או 240,000. בשימוש קשה (שטח, גרירה) מחליפים שמן סרנים ותיבת העברה.'
}

# ---------------------------------------------------------------- write
write(dict(FIA, id='fiat-500-2008-2021-1.2', model='500', model_he='500', generation='312', years=[2008, 2021],
           engines=['1.2 8V 69 כ"ס (169A4000)'], fuel='petrol'), PLAN_500,
      [{'names': ['FIAT 500 1.2', 'FIAT 500', '500', '500C'], 'years': [2008, 2021], 'engine_codes': ['169A4000']}])
p = copy.deepcopy(PLAN_500); p['status'] = 'draft'
p['sources'] = [{'url': F500, 'kind': 'importer', 'note': 'ספר רכב עברי פיאט 500 (סמלת, 04/2021), תכנית טיפולים לבנזין עמ\' 118-120 - אותו מנוע 1.2 8V (169A4000)'},
                {'url': U + '2023/11/260617-QuickGuide-Fiat-Panda-Heb-AR-S3-SH.pdf', 'kind': 'importer', 'note': 'מדריך מקוצר עברי לפנדה החדשה (לא הדגם הישן, אין בו תכנית טיפולים); ספר עברי לפנדה 2011-2017 לא נמצא'}]
p['notes'] = 'לפנדה (2011-2017) לא נמצא ספר עברי, ולכן נלקחה תכנית הטיפולים מספר פיאט 500 העברי עם אותו מנוע 1.2 8V. ' + PLAN_500['notes']
write(dict(FIA, id='fiat-panda-2011-2017-1.2', model='Panda', model_he='פנדה', generation='319', years=[2011, 2017],
           engines=['1.2 8V 69 כ"ס (169A4000)'], fuel='petrol'), p,
      [{'names': ['PANDA'], 'years': [2008, 2019], 'engine_codes': ['169A4000']}])

write(dict(FIA, id='fiat-tipo-2016-2020-1.6', model='Tipo', model_he='טיפו', generation='356', years=[2016, 2020],
           engines=['1.6 E.torQ 110 כ"ס (55268036)'], fuel='petrol'), PLAN_TIPO,
      [{'names': ['FIAT TIPO', 'TIPO'], 'years': [2016, 2020], 'engine_codes': ['55268036']}])

write(dict(FIA, id='fiat-500x-2015-2019-1.4-multiair', model='500X', model_he='500X', generation='334', years=[2015, 2019],
           engines=['1.4 Turbo MultiAir 140 כ"ס (55263624)'], fuel='petrol'), PLAN_500X,
      [{'names': ['500X', 'FIAT 500X'], 'years': [2015, 2019], 'engine_codes': ['55263624']}])
for vid, model, mhe, yrs, names, codes, eng in [
    ('jeep-renegade-2015-2019-1.4-multiair', 'Renegade', 'רנגייד', [2015, 2019], ['RENEGADE'], ['55263624'], '1.4 Turbo MultiAir 140 כ"ס (55263624)'),
    ('jeep-compass-2018-2020-1.4-multiair', 'Compass', 'קומפאס', [2017, 2020], ['JEEP COMPASS', 'COMPASS'], ['55263623'], '1.4 Turbo MultiAir 170 כ"ס (55263623)')]:
    p = copy.deepcopy(PLAN_500X); p['status'] = 'draft'
    p['sources'] = [{'url': X500, 'kind': 'importer', 'note': 'ספר רכב עברי פיאט 500X (סמלת), תכנית טיפולים ל-1.4 Turbo MultiAir עמ\' 158-160 - רכב אח (פלטפורמה ומנוע משותפים)'},
                    {'url': 'https://samelet.com/wp-content/uploads/2023/11/Jeep_renegede_shortguide_151020.pdf', 'kind': 'importer', 'note': 'לרנגייד יש באתר סמלת רק מדריך מקוצר; ספר עברי מלא לא נמצא'}]
    p['notes'] = 'ספר עברי מלא לדגם זה לא נמצא, ולכן נלקחה תכנית 500X מספר סמלת (אותו מנוע 1.4 טורבו MultiAir ואותה פלטפורמה). ' + PLAN_500X['notes']
    write(dict(JEP, id=vid, model=model, model_he=mhe, years=yrs, engines=[eng], fuel='petrol'), p,
          [{'names': names, 'years': yrs, 'engine_codes': codes}])

write(dict(JEP, id='jeep-compass-2021-2024-1.3-turbo', model='Compass', model_he='קומפאס', generation='MP', years=[2021, 2024],
           engines=['1.3 T4 טורבו 130/150 כ"ס (55282328)'], fuel='petrol'), PLAN_CMP21,
      [{'names': ['COMPASS'], 'years': [2021, 2024], 'engine_codes': ['55282328']}])

write(dict(JEP, id='jeep-compass-2025-2026-1.2-mhev', model='Compass', model_he='קומפאס', generation='J4U', years=[2025, 2026],
           engines=['1.2 טורבו היברידי מתון (EB2T MHEV)'], fuel='hybrid'), PLAN_MHEV,
      [{'names': ['COMPASS'], 'years': [2025, 2026]}])

# HN09 (new generation 1.2 turbo, mostly mild-hybrid) -> Compass 2026 Israeli MHEV plan as sister engine
HN = [
 (PEU, 'peugeot-3008-2024-2026-1.2-hybrid', '3008', '3008', 'P64', [2024, 2026], ['3008']),
 (PEU, 'peugeot-5008-2025-2026-1.2-hybrid', '5008', '5008', 'P67', [2025, 2026], ['5008']),
 (PEU, 'peugeot-208-2025-2026-1.2-hybrid', '208', '208', 'P21', [2025, 2026], ['208']),
 (PEU, 'peugeot-2008-2025-2026-1.2-hybrid', '2008', '2008', 'P24', [2025, 2026], ['2008']),
 (OPL, 'opel-frontera-2025-2026-1.2-hybrid', 'Frontera', 'פרונטרה', 'P2QO', [2025, 2026], ['FRONTERA']),
 (OPL, 'opel-corsa-2025-2026-1.2-hybrid', 'Corsa', 'קורסה', 'F', [2025, 2026], ['CORSA']),
 (CIT, 'citroen-c3-2025-2026-1.2-hybrid', 'C3', 'C3', 'CC21', [2025, 2026], ['C3']),
 (CIT, 'citroen-c3-aircross-2025-2026-1.2-hybrid', 'C3 Aircross', 'C3 איירקרוס', 'CC24', [2025, 2026], ['C3 AIRCROSS']),
]
for base, vid, model, mhe, gen_, yrs, names in HN:
    p = copy.deepcopy(PLAN_MHEV); p['status'] = 'draft'
    p['sources'] = PLAN_MHEV['sources'] + [SRC_OPEL_F, SRC_LUB]
    p['notes'] = 'לובינסקי לא מפרסם לוח טיפולים. קוד המנוע HN09 ברישוי הוא דור חדש של מנוע 1.2 טורבו של סטלנטיס (ברובו בגרסה היברידית מתונה), ולכן נלקחה תכנית ה-EB2T MHEV מספר הקומפאס 2026 העברי של סמלת. יש לאמת מול מרכז השירות: בגרסאות לא-היברידיות ייתכנו מועדי רצועה שונים. ' + PLAN_MHEV['notes']
    write(dict(base, id=vid, model=model, model_he=mhe, generation=gen_, years=yrs,
               engines=['1.2 טורבו דור חדש (קוד HN09, ברובו היברידי מתון)'], fuel='hybrid'), p,
          [{'names': names, 'years': yrs, 'engine_codes': ['HN09']}])

write(dict(JEP, id='jeep-wrangler-2018-2026-2.0-turbo', model='Wrangler', model_he='רנגלר', generation='JL', years=[2018, 2026],
           engines=['2.0 טורבו (קוד N)'], fuel='petrol'), PLAN_WR,
      [{'names': ['WRANGLER', 'WRANGLER UNLIMI', 'WRANGLER UNLIM', 'WRANGLER UNLI', 'JEEP WRANGLER'], 'years': [2018, 2026], 'engine_codes': ['N']},
       {'names': ['WRANGLER', 'WRANGLER UNLIMI', 'WRANGLER UNLIM', 'WRANGLER UNLI', 'JEEP WRANGLER'], 'years': [2021, 2026]},
       {'make': 'Chrysler', 'names': ['WRANGLER', 'WRANGLER UNLIMI', 'JEEP WRANGLER'], 'years': [2018, 2026], 'engine_codes': ['N']}])
