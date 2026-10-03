# Jeep Grand Cherokee WK2 / WL and Wrangler JK (3.6 Pentastar, registry engine letter "G").
from gen import *

SAM = 'סמלת'
JEEP = dict(make='Jeep', make_he="ג'יפ", importer=SAM)
MIR = 'https://cdn.dealereprocess.org/cdn/servicemanuals/jeep/'
GC23 = 'https://samelet.com/wp-content/uploads/2023/11/Jeep_Grand_Cherokee-2023_carbook.pdf'

def every(step, start, end):
    return tuple(range(start, end + 1, step))

def grid16(every_list, rows, n=15, step=16000):
    g = []
    for k in range(1, n + 1):
        km = step * k
        its = list(every_list)
        for kms, lst in rows:
            if km in kms: its += lst
        g.append((km, its))
    return g

EVERY_US = [R('engine_oil', 'לפי מחוון החלפת השמן, ולא יותר מ-16,000 ק"מ או 12 חודשים'), R('oil_filter'),
            ('tire_rotation', 'rotate', None), I('battery_12v', 'ניקוי והידוק קטבים לפי הצורך'),
            I('brake_pads', 'רפידות ונעלי בלם'), I('brake_discs', 'דיסקים ותופים'), I('brake_lines'), I('parking_brake'),
            I('coolant', 'רמת ההגנה של נוזל הקירור'), I('coolant_hoses'), I('exhaust'),
            I('air_filter', 'בנסיעה באבק או בשטח')]

# ---------------------------------------------------------------- WK2 2011-2021, 3.6 V6 (US 2019 manual)
Y2 = every(32000, 32000, 224000)   # years 2,4,...,14
wk2_rows = [
    (every(48000, 48000, 240000), [I('cv_boots', 'מפרקים הומוקינטיים'), R('air_filter', 'או לפי הזמן בטבלה')]),
    (Y2, [I('suspension', 'מתלה קדמי וקצוות מוטות היגוי; החלפה לפי הצורך'), I('steering'),
          I('differential_oil', 'שמן סרן קדמי ואחורי; החלפה בשימוש קשה (מונית, צי, שטח, גרירה תכופה)'),
          I('brake_pads', 'בטנות בלם ותפקוד בלם חניה'), R('cabin_filter')]),
    ((48000, 96000, 144000, 240000), [I('transfer_case_oil')]),
    ((160000,), [R('spark_plugs', 'לפי ק"מ בלבד'), R('coolant', 'שטיפה והחלפה (או 10 שנים)'), I('pcv_valve', 'החלפה לפי הצורך')]),
    ((192000,), [R('transfer_case_oil')]),
    ((240000,), [R('coolant', 'שטיפה והחלפה')]),
]
PLAN_WK2 = {
    'interval': {'km': 16000, 'months': 12, 'note': 'לפי ספר הנהג האמריקאי של ג\'יפ: שמן ומסנן לפי מחוון החלפת השמן, ובשום מקרה לא יותר מ-16,000 ק"מ או 12 חודשים; בשימוש קשה (אבק ושטח, סרק ממושך) כל 6,500 ק"מ'},
    'cycle_km': 240000,
    'grid': grid16(EVERY_US, wk2_rows),
    'long': [LI('coolant', 'replace', every_km=240000, every_months=120, note='שטיפה והחלפה ב-10 שנים או 240,000 ק"מ, המוקדם'),
             LI('spark_plugs', 'replace', every_km=160000, note='לפי ק"מ בלבד')],
    'specs': {'_note': 'הטבלה מתחילה בשנה 2 (32,000 ק"מ); בטיפול הראשון מבוצעים רק פריטי "בכל החלפת שמן"'},
    'sources': [{'url': MIR + '2019-grandcherokee.pdf', 'kind': 'manufacturer',
                 'note': '2019 Jeep Grand Cherokee Owner\'s Manual (FCA US), Scheduled Servicing - Gasoline Engine, עמ\' 437-440 (PDF 439-442); עמודות במייל ובק"מ'},
                {'url': GC23, 'kind': 'importer', 'note': 'ספר הרכב העברי של סמלת לגרנד צ\'רוקי 2023 (דור WL) - לא לדור WK2; שימש להשוואה בלבד'}],
    'status': 'draft',
    'notes': 'ספר עברי לדור WK2 (2011-2021) לא נמצא, והלוח לקוח מספר הנהג האמריקאי של גרנד צ\'רוקי 2019 עם מנוע 3.6 V6 (אותו מנוע). '
             'שמן ומסנן לפי מחוון החלפת השמן, לכל היותר כל 16,000 ק"מ או שנה; בכל החלפה גם סבב צמיגים ובדיקת מצבר, בלמים, מערכת קירור ופליטה. '
             'כל שנתיים (32,000 ק"מ): מסנן מזגן, בדיקת מתלה קדמי ומוטות היגוי, שמן סרנים ובטנות בלם. כל 48,000 ק"מ: מסנן אוויר ובדיקת מפרקים הומוקינטיים. '
             'מצתים ב-160,000 ק"מ (לפי ק"מ בלבד); נוזל קירור ב-10 שנים או 240,000 ק"מ; שמן תיבת העברה ב-192,000 ק"מ. '
             'בשימוש קשה (מונית, צי, שטח או גרירה תכופה) מחליפים את שמן הסרנים בכל בדיקה. לא כולל את גרסת הדיזל 3.0.',
}
write({**JEEP, 'id': 'jeep-grand-cherokee-2011-2021-3.6', 'model': 'Grand Cherokee', 'model_he': "גרנד צ'רוקי", 'generation': 'WK2',
       'years': [2011, 2021], 'engines': ['3.6 V6 Pentastar (קוד רישוי G)'], 'fuel': 'petrol'}, PLAN_WK2,
      [{'make': 'Chrysler', 'names': ['GRAND CHEROKEE', 'JEEP GRAND CHER', 'JEEP GRAND CHEROKEE', 'GRAND CHEROKEE LAREDO', 'GRAND CHEROKEE LIMITED'], 'years': [2011, 2022], 'engine_codes': ['G']},
       {'names': ['GRAND CHEROKEE'], 'years': [2011, 2021], 'engine_codes': ['G']}])

# ---------------------------------------------------------------- WL 2022+ (Samelet Hebrew book 2023)
EVERY_WL = [R('engine_oil', 'לפי מחוון החלפת השמן, ולא יותר מ-16,000 ק"מ או 12 חודשים'), R('oil_filter'),
            ('tire_rotation', 'rotate', None), I('battery_12v', 'ניקוי והידוק קטבים לפי הצורך'), I('cv_boots', 'מפרקים אוניברסליים / ציריות'),
            I('brake_pads', 'רפידות ונעלי בלם'), I('brake_discs', 'דיסקים ותופים'), I('brake_lines'), I('parking_brake'),
            I('coolant', 'רמת ההגנה של נוזל הקירור'), I('coolant_hoses'), I('exhaust'),
            I('air_filter', 'בנסיעה באזורים מאובקים או בשטח: החלפה לפי הצורך')]
def y12(*years): return tuple(12000 * y for y in years)
wl_rows = [
    (y12(3, 6, 9, 12, 15, 18), [I('suspension', 'מתלים קדמיים והידוק אומים וברגים; החלפה לפי הצורך')]),
    (y12(4, 8, 12, 16, 20), [I('differential_oil', 'שמן סרנים; החלפה בתנאים חריגים'), I('transfer_case_oil'), A('parking_brake', 'בדיקה וכיוון לפי הצורך')]),
    (y12(2, 4, 6, 8, 10, 12, 14, 16, 18, 20), [R('brake_fluid', 'כל 24 חודשים'), R('air_filter')]),
    (y12(9, 18), [R('spark_plugs'), R('transfer_case_oil', 'רק בתנאים חריגים')]),
    (y12(10, 20), [R('coolant')]),
    (y12(16), [R('transfer_case_oil', 'שימוש רגיל')]),
    (y12(12), [I('pcv_valve', 'החלפה לפי הצורך')]),
    (y12(20), [R('drive_belt')]),
]
PLAN_WL = {
    'interval': {'km': 12000, 'months': 12, 'note': 'טבלת הטיפולים בספר העברי של סמלת בנויה על 12,000 ק"מ לשנה (שנים 1-20 עד 240,000 ק"מ). השמן מוחלף לפי מחוון החלפת השמן, ובשום מקרה לא יותר מ-16,000 ק"מ או 12 חודשים'},
    'cycle_km': 240000,
    'grid': grid16(EVERY_WL, wl_rows, n=20, step=12000),
    'long': [LI('brake_fluid', 'replace', every_months=24),
             LI('coolant', 'replace', every_km=120000, note='בשנה 10 ובשנה 20 לפי הטבלה'),
             LI('drive_belt', 'replace', every_km=240000)],
    'specs': {'_note': 'בספר שתי טבלאות: הראשונה (עמ\' 290) בנויה על 16,000 ק"מ לשנה (בדיקת מפרקים כל שנה, רפידות כל שנתיים, שמן סרנים כל 3 שנים), השנייה (עמ\' 291) על 12,000 ק"מ לשנה. הקובץ משתמש בטבלה השנייה; הבדיקות של הטבלה הראשונה כלולות ממילא ברשימת "בכל החלפת שמן"'},
    'sources': [{'url': GC23, 'kind': 'importer', 'note': 'ספר הרכב העברי של סמלת, ג\'יפ גרנד צ\'רוקי 2023: פרק שירות ותחזוקה, עמ\' 289-292 (PDF 290-293)'}],
    'status': 'draft',
    'notes': 'הלוח לקוח מספר הרכב העברי של היבואן (סמלת) לגרנד צ\'רוקי 2023 (דור WL). הוא מסומן כטיוטה משום שבספר שתי טבלאות שאינן מתיישבות: אחת לפי 16,000 ק"מ לשנה ואחת לפי 12,000 ק"מ לשנה; הקובץ משתמש בטבלה המפורטת לפי 12,000 ק"מ. '
             'בכל החלפת שמן (לפי המחוון, לכל היותר 16,000 ק"מ או שנה): שמן ומסנן, סבב צמיגים, בדיקת מצבר, מפרקים, בלמים, מערכת קירור ופליטה. '
             'כל שנתיים: נוזל בלמים ומסנן אוויר. כל 3 שנים: בדיקת מתלים קדמיים. כל 4 שנים: בדיקת שמן סרנים ותיבת העברה וכיוון בלם יד. '
             'מצתים בשנה 9 (108,000 ק"מ) ובשנה 18; נוזל קירור בשנה 10 (120,000 ק"מ) ובשנה 20; שסתום PCV בשנה 12; שמן תיבת העברה בשנה 16 (בתנאים חריגים בשנים 9 ו-18); רצועת אביזרים בשנה 20. '
             'תנאים חריגים לפי הספר: שטח קשה, רכב ביטחון, מונית, צי רכב או גרירה.',
}
write({**JEEP, 'id': 'jeep-grand-cherokee-2022-2026-3.6', 'model': 'Grand Cherokee', 'model_he': "גרנד צ'רוקי", 'generation': 'WL',
       'years': [2022, 2026], 'engines': ['3.6 V6 Pentastar (קוד רישוי G)'], 'fuel': 'petrol'}, PLAN_WL,
      [{'names': ['GRAND CHEROKEE', 'GRAND CHEROKEE L'], 'years': [2022, 2026], 'engine_codes': ['G']}])

# ---------------------------------------------------------------- Wrangler JK 3.6 (2012-2018), US 2016 manual
EVERY_JK = EVERY_US + [I('transmission_oil', 'גיר אוטומטי עם מדיד'), C('door_hinges', 'גירוז מנעולי הדלתות לפי הצורך')]
jk_rows = [
    (Y2, [I('cv_boots', 'מפרקים הומוקינטיים ואוניברסליים'), I('suspension', 'מתלה קדמי וקצוות מוטות היגוי; החלפה לפי הצורך'), I('steering'),
          I('brake_pads', 'בטנות בלם; החלפה לפי הצורך'), A('parking_brake', 'בגרסאות עם בלמי דיסק בארבעת הגלגלים'), R('cabin_filter')]),
    ((32000, 96000, 160000, 224000), [I('differential_oil', 'שמן סרן קדמי ואחורי')]),
    ((48000, 144000, 240000), [I('transfer_case_oil')]),
    (every(48000, 48000, 240000), [R('air_filter')]),
    ((160000,), [R('spark_plugs', 'לפי ק"מ בלבד'), R('coolant', 'שטיפה והחלפה (או 10 שנים)'), I('pcv_valve', 'החלפה לפי הצורך')]),
    ((192000,), [R('transmission_oil', 'גיר אוטומטי, שמן ומסנן')]),
    ((240000,), [R('coolant', 'שטיפה והחלפה')]),
]
PLAN_JK = {
    'interval': PLAN_WK2['interval'],
    'cycle_km': 240000,
    'grid': grid16(EVERY_JK, jk_rows),
    'long': [LI('coolant', 'replace', every_km=240000, every_months=120, note='שטיפה והחלפה ב-10 שנים או 240,000 ק"מ, המוקדם'),
             LI('spark_plugs', 'replace', every_km=160000, note='לפי ק"מ בלבד')],
    'specs': {'_note': 'הטבלה מתחילה בשנה 2 (32,000 ק"מ); בטיפול הראשון מבוצעים רק פריטי "בכל החלפת שמן"'},
    'sources': [{'url': MIR + '2016-wrangler.pdf', 'kind': 'manufacturer',
                 'note': '2016 Jeep Wrangler Owner\'s Manual (FCA US), Maintenance Schedules, עמ\' 665-670 (PDF 667-672); עמודות במייל ובק"מ'}],
    'status': 'draft',
    'notes': 'ספר עברי לרנגלר JK לא נמצא; הלוח לקוח מספר הנהג האמריקאי של רנגלר 2016 עם מנוע 3.6 V6. '
             'שמן ומסנן לפי מחוון החלפת השמן, לכל היותר כל 16,000 ק"מ או שנה (בשימוש באבק ובשטח כל 6,500 ק"מ); בכל החלפה גם סבב צמיגים ובדיקת מצבר, בלמים, מערכת קירור, פליטה ושמן גיר. '
             'כל שנתיים (32,000 ק"מ): מסנן מזגן, בדיקת מפרקים, מתלה קדמי, בטנות בלם. מסנן אוויר כל 48,000 ק"מ. מצתים ב-160,000 ק"מ; נוזל קירור ב-10 שנים או 240,000 ק"מ; שמן גיר אוטומטי ב-192,000 ק"מ. '
             'בשימוש קשה (מונית, צי, שטח, גרירה, נסיעה מהירה ממושכת בחום) הספר מקדים את החלפת שמן הגיר, תיבת ההעברה והסרנים (למשל גיר אוטומטי ב-96,000 ק"מ, שמן סרנים ב-64,000 ק"מ).',
}
write({**JEEP, 'id': 'jeep-wrangler-2012-2018-3.6', 'model': 'Wrangler', 'model_he': 'רנגלר', 'generation': 'JK',
       'years': [2012, 2018], 'engines': ['3.6 V6 Pentastar (קוד רישוי G)'], 'fuel': 'petrol'}, PLAN_JK,
      [{'make': 'Chrysler', 'names': ['WRANGLER', 'WRANGLER UNLIMI', 'WRANGLER UNLIM', 'WRANGLER UNLI', 'JEEP WRANGLER'], 'years': [2012, 2018], 'engine_codes': ['G']},
       {'names': ['WRANGLER', 'WRANGLER UNLIMI', 'WRANGLER UNLIM', 'JEEP WRANGLER'], 'years': [2012, 2018], 'engine_codes': ['G']}])
