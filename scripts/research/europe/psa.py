from gen import *

LUB = 'דוד לובינסקי'
SAM = 'סמלת'
DOBLO_URL = 'https://samelet.com/wp-content/uploads/2024/02/Fiat_Doblo_carbook_062026.pdf'
CITY_URL = 'https://books.union-motors.co.il/app/api/files/1190/download'
OPEL_F_URL = 'https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf'
AVENGER_URL = 'https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf'
LUB_WARRANTY = 'https://media-peugeot.lubit.co.il/wp-content/uploads/2023/06/Warranty-Peugeot-3Y-01.2024_Web-%D7%9E%D7%95%D7%A0%D7%92%D7%A9.pdf'
PROACE_URL = 'https://books.union-motors.co.il/app/api/files/603/download'

SRC_LUB = {'url': LUB_WARRANTY, 'kind': 'importer',
           'note': 'חוברת אחריות ושירות של לובינסקי (פיג\'ו; זהה בסיטרואן/אופל): אין בה טבלת ק"מ; תכנית הטיפולים האישית נמסרת עם הרכב. דפי ספרי הרכב ב-lubinski.clearmash.com חסומים (Cloudflare 403)'}
SRC_OPEL_F = {'url': OPEL_F_URL, 'kind': 'importer',
              'note': 'ספר הנהג העברי של אופל קורסה F (2021), עמ\' 205: ישראל בקבוצת מדינות 4, טיפול כל 15,000 ק"מ או שנה למנועי EB2 1.2 ו-DV5 1.5'}

# ---------------------------------------------------------------- DV5 1.5 BlueHDi (Doblo K9 Israeli book)
DV5_EVERY = [R('engine_oil'), R('oil_filter'), I('coolant', 'מפלס'), I('brake_fluid', 'מפלס'),
             I('wipers', 'כולל כיוון מתזים'), I('washer_fluid'),
             I('body_underside'), I('exhaust'), I('fuel_lines'), I('brake_lines'), I('cv_boots'),
             I('parking_brake'), I('steering', 'חופשים במערכת ההיגוי'), I('adblue', 'מפלס'),
             I('brake_pads'), I('brake_discs'), I('tires'), I('lights'), I('battery_12v', 'ניקוי קטבים'),
             I('diagnostics', 'קריאת תקלות ואיפוס מחשב טיפולים'), I('suspension', 'אטימות בולמים'),
             I('drive_belt', 'בדיקת רצועה ומותחן')]
DV5_30 = [R('fuel_filter'), R('air_filter', 'באזור מאובק: כל 10,000 ק"מ'), R('cabin_filter'),
          C('door_hinges', 'ניקוי ושימון מנעולים ומסילות דלת הזזה')]
PLAN_DV5 = {
    'interval': {'km': 15000, 'months': 12, 'note': 'לפי ספר הרכב העברי של פיאט דובלו (סמלת, 2026, אותו רכב ומנוע כמו ברלינגו K9): טיפול כל 15,000 ק"מ או שנה. גם ספר אופל העברי מציין לישראל 15,000 ק"מ/שנה למנוע DV5'},
    'cycle_km': 120000,
    'grid': grid(15000, 8, DV5_EVERY, {30000: DV5_30}),
    'long': [
        LI('timing_belt', 'replace', every_km=120000, every_months=60, note='יחד עם משאבת המים'),
        LI('drive_belt', 'replace', every_km=120000, every_months=60, note='רצועה ומותחן'),
        LI('brake_fluid', 'replace', every_months=24, note='ללא קשר לק"מ'),
        LI('coolant', 'inspect', first_km=120000, first_months=48, then_every_km=15000, then_every_months=12,
           note='בדיקת pH; החלפה כשהערך נמוך מ-6.3'),
    ],
    'specs': {'engine_oil': 'SAE 5W-30 ACEA C3 (מפרט פיאט 9.55535/03)',
              'oil_capacity': 'כ-4 ליטר עם מסנן (נוסעים); 5.3 ליטר (מסחרי)',
              'coolant': 'Freecor DSC מהול 50% במים מזוקקים', 'brake_fluid': 'DOT 4',
              'timing': 'רצועת תזמון: החלפה כל 120,000 ק"מ או 5 שנים',
              '_note': 'נתוני נוזלים מספר הדובלו העברי; בברלינגו/פרטנר/קומבו הכמויות עשויות להיות שונות'},
    'sources': [{'url': DOBLO_URL, 'kind': 'importer', 'note': 'ספר רכב עברי פיאט דובלו (סמלת, 06/2026), תכנית טיפולים למנוע דיזל 1.5, עמ\' 252-254 (PDF 253-255). רכב אח של ברלינגו K9 עם אותו מנוע'},
                {'url': CITY_URL, 'kind': 'importer', 'note': 'לוח אחזקה של טויוטה פרואייס סיטי (יוניון מוטורס, 07/2021), מנוע DV5RD/DV5RC, עמודות 15,000 ק"מ עד 210,000'},
                SRC_OPEL_F, SRC_LUB],
    'status': 'draft',
    'notes': 'היבואן לובינסקי לא מפרסם לוח טיפולים (התכנית נמסרת אישית עם הרכב), ולכן הלוח נלקח מספר הרכב העברי של פיאט דובלו החדש, שהוא אותו רכב (פלטפורמת K9) עם אותו מנוע 1.5 BlueHDi. בכל טיפול: שמן ומסנן ובדיקות; כל 30,000: מסנני סולר, אוויר ומזגן. רצועת תזמון ומשאבת מים וגם רצועת אביזרים: 120,000 ק"מ או 5 שנים. לוח היבואן יוניון לטויוטה פרואייס סיטי (אותו רכב ומנוע) מחמיר פחות: רצועת תזמון 180,000 ק"מ/10 שנים ורצועת אביזרים לראשונה ב-120,000 ואחר כך כל 160,000. נוזל בלמים כל שנתיים. בדיקת סתימת מסנן חלקיקים מ-120,000 ק"מ או 5 שנים ובכל טיפול אחר כך.'
}

# ---------------------------------------------------------------- 1.2 PureTech turbo (EB2 turbo)
PT_EVERY = [R('engine_oil'), R('oil_filter'), R('cabin_filter'),
            I('battery_12v'), I('tires'), I('lights'), I('wipers', 'כולל פעולת מתזים'), I('washer_fluid'),
            I('body_underside', 'כולל מגני גחון וחלקי גומי'), I('exhaust'), I('fuel_lines'), I('brake_lines'),
            I('coolant_hoses'), I('brake_pads'), I('brake_discs'), I('suspension', 'אטימות בולמים'),
            I('cv_boots'), I('steering', 'חופשים במפרקים ובמוט ההגה'), I('pedals'), I('clutch'),
            I('parking_brake'), I('coolant', 'מפלס'), I('brake_fluid', 'מפלס'),
            I('diagnostics', 'קריאת זיכרון תקלות ואיפוס מחוון טיפול'),
            I('drive_belt', 'מצב ומתיחה'), I('timing_belt', 'מדידת רוחב הרצועה')]
PLAN_PT = {
    'interval': {'km': 15000, 'months': 12, 'note': 'ספר הנהג העברי של אופל קורסה F (אותו מנוע 1.2 PureTech) מציין לישראל טיפול כל 15,000 ק"מ או שנה. באירופה היצרן מתיר 20,000 ק"מ'},
    'cycle_km': 120000,
    'grid': grid(15000, 8, PT_EVERY),
    'long': [
        LI('air_filter', 'replace', every_km=20000, every_months=48, note='ערך "מחוץ לאירופה" בספר; באירופה 40,000 ק"מ/4 שנים'),
        LI('spark_plugs', 'replace', every_km=20000, every_months=48, note='ערך "מחוץ לאירופה" בספר; באירופה 40,000 ק"מ/4 שנים'),
        LI('timing_belt', 'replace', first_km=90000, first_months=72, then_every_km=180000, then_every_months=144,
           note='רצועה רטובה (בתוך שמן) + רצועת משאבת מים. באירופה בתנאים רגילים: 100,000 ק"מ/6 שנים ואז 200,000/12 שנים'),
        LI('drive_belt', 'replace', first_km=90000, first_months=72, then_every_km=180000, then_every_months=144,
           note='באירופה בתנאים רגילים: 100,000 ק"מ/6 שנים ואז 200,000/12 שנים'),
        LI('coolant', 'replace', every_km=160000, every_months=120, note='באירופה: 180,000 ק"מ או 10 שנים'),
        LI('coolant', 'inspect', first_km=120000, first_months=48, then_every_km=15000, then_every_months=12,
           note='בדיקת pH; החלפה כשהערך נמוך מ-6.3'),
        LI('brake_fluid', 'replace', every_months=24, note='ללא קשר לק"מ'),
        LI('fuel_filter', 'replace', every_km=40000, every_months=48, note='בספר: רק בשימוש מחוץ לאירופה'),
    ],
    'specs': {'engine_oil': 'SAE 0W-20 ACEA C6 / PSA B71 2010 (בספר אוונג\'ר 2022); בדגמים ישנים 0W-30 / 5W-30 לפי תקן PSA B71 2312 או B71 2290',
              'brake_fluid': 'DOT 4',
              'timing': 'רצועת תזמון רטובה: 100,000 ק"מ או 6 שנים (מחוץ לאירופה 90,000), אחר כך 200,000/12 שנים',
              '_note': 'מפרט השמן מספר הנהג של ג\'יפ אוונג\'ר; בדוק את מפרט השמן בספר הרכב הספציפי'},
    'sources': [{'url': AVENGER_URL, 'kind': 'manufacturer', 'note': 'Jeep Avenger Owner Handbook (EN, 12/2022), Service schedule for 1.2 gasoline engine, pp. 213-217: grid of 20,000 km/1 year (Europe) with footnotes for arduous use and use outside Europe'},
                SRC_OPEL_F, SRC_LUB],
    'status': 'draft',
    'notes': 'לוח לפי ספר הנהג האנגלי של ג\'יפ אוונג\'ר (סטלנטיס) למנוע בנזין 1.2 טורבו, עם מרווח ישראלי של 15,000 ק"מ או שנה מספר אופל העברי. בכל טיפול: שמן ומסנן, מסנן מזגן ורשימת בדיקות (בלמים, מתלים, צמיגים, תאורה, צנרת, קריאת מחשב, מדידת רוחב רצועת התזמון). לפריטים הארוכים נבחרו ערכי "שימוש מחוץ לאירופה" שבספר, כפי שסמלת עושה בתכנית הישראלית של קומפאס 2026: מצתים ומסנן אוויר כל 20,000 ק"מ או 4 שנים, רצועת תזמון ורצועת אביזרים ב-90,000 ק"מ או 6 שנים ואז כל 180,000, נוזל קירור 160,000/10 שנים. ערכי אירופה מופיעים בהערות. רצועת התזמון רצה בתוך השמן, ולכן חשוב להקפיד על שמן בתקן הנכון. נוזל בלמים כל שנתיים. המספרים לא נלקחו מספר של היבואן לובינסקי.'
}

# ---------------------------------------------------------------- 2.0 BlueHDi DW10FC/FE (Toyota Proace Israeli sheet)
PR_EVERY = [R('engine_oil'), R('oil_filter'), I('cooling_system', 'מקרן, צינורות, חיבורים'), I('coolant', 'השלמה'),
            I('exhaust', 'צנרת פליטה ותומכים, עשן'), I('fuel_lines', 'כולל מכסה מיכל'), I('adblue', 'מילוי'),
            I('pedals'), I('parking_brake'), I('brake_pads'), I('brake_discs'), I('brake_lines'),
            I('steering'), I('cv_boots'), I('suspension'), I('tires'), I('body_underside', 'בדיקת קורוזיה')]
PLAN_PROACE = {
    'interval': {'km': 20000, 'months': 12, 'note': 'לוח האחזקה של טויוטה פרואייס (יוניון מוטורס, 2017) למנועי DW10FC/DW10FE: טיפול כל 20,000 ק"מ או 12 חודשים'},
    'cycle_km': 160000,
    'grid': [(km, its + ([] if km % 40000 == 0 else [C('cabin_filter')])) for km, its in
             grid(20000, 8, PR_EVERY, {40000: [R('air_filter'), R('fuel_filter'), R('cabin_filter')]})],
    'long': [
        LI('drive_belt', 'replace', every_km=120000, every_months=72, note='רצועה ומותחן'),
        LI('timing_belt', 'replace', every_km=140000, every_months=120, note='כולל מותחן ומשאבת מים'),
        LI('brake_fluid', 'replace', every_months=24),
        LI('coolant', 'inspect', first_km=120000, first_months=48, then_every_km=20000, then_every_months=12, note='בדיקת pH'),
    ],
    'specs': {'engine_oil': '0W-30 ACEA C2', 'oil_capacity': '6 ליטר', 'brake_fluid': 'DOT 4 / DOT 4+',
              'coolant': 'Premium long life coolant', 'timing': 'רצועת תזמון: 140,000 ק"מ או 10 שנים',
              '_note': 'לפי לוח הפרואייס של יוניון מוטורס'},
    'sources': [{'url': PROACE_URL, 'kind': 'importer', 'note': 'לוח אחזקה פרואייס 2017 (יוניון מוטורס, 26/07/2017), מנועי DW10FC/DW10FE, עמודות 10,000 עד 160,000 ק"מ עם סימונים כל 20,000'}, SRC_LUB],
    'status': 'draft',
    'notes': 'טויוטה פרואייס (2016 ואילך) הוא אותו רכב כמו סיטרואן ג\'אמפי ופיג\'ו אקספרט עם מנוע 2.0 BlueHDi, ולכן נלקח לוח האחזקה הישראלי של יוניון מוטורס. טיפול כל 20,000 ק"מ או שנה: שמן ומסנן ובדיקות; כל 40,000: מסנני אוויר, סולר ומזגן (בטיפולי הביניים מנקים את מסנן המזגן). רצועת אביזרים 120,000 ק"מ/6 שנים, רצועת תזמון עם משאבת מים 140,000 ק"מ/10 שנים. תוסף מסנן חלקיקים (Eolys) ב-80,000 וב-160,000, ובדיקת סתימת מסנן החלקיקים מ-160,000. נוזל בלמים כל שנתיים.'
}

def V(**kw): return kw

CIT = dict(make='Citroen', make_he='סיטרואן', importer=LUB)
PEU = dict(make='Peugeot', make_he="פיג'ו", importer=LUB)
OPL = dict(make='Opel', make_he='אופל', importer=LUB)
FIA = dict(make='Fiat', make_he='פיאט', importer=SAM)
JEP = dict(make='Jeep', make_he="ג'יפ", importer=SAM)
DS_ = dict(make='DS', make_he='די אס', importer=LUB)

DV5_ENG = ['1.5 BlueHDi (DV5RC/DV5RD, קוד YH01)']
PT_ENG = ['1.2 PureTech טורבו (EB2DT/EB2DTS, קודי HN01/HN02/HN05)']

# ---- DV5 vehicles
dv5 = [
 (CIT, 'citroen-berlingo-2018-2026-1.5-bluehdi', 'Berlingo', 'ברלינגו', 'K9', [2018, 2026], ['BERLINGO']),
 (PEU, 'peugeot-partner-rifter-2019-2026-1.5-bluehdi', 'Partner / Rifter', "פרטנר / ריפטר", 'K9', [2019, 2026], ['PARTNER', 'RIFTER', 'NEW PARTNER']),
 (OPL, 'opel-combo-2019-2026-1.5-diesel', 'Combo', 'קומבו', 'E (K9)', [2019, 2026], ['COMBO']),
 (PEU, 'peugeot-3008-2017-2025-1.5-bluehdi', '3008', '3008', 'P84', [2017, 2025], ['3008']),
 (PEU, 'peugeot-5008-2018-2025-1.5-bluehdi', '5008', '5008', 'P87', [2018, 2025], ['5008']),
 (PEU, 'peugeot-2008-2020-2026-1.5-bluehdi', '2008', '2008', 'P24', [2020, 2026], ['2008']),
 (CIT, 'citroen-c5-aircross-2019-2026-1.5-bluehdi', 'C5 Aircross', 'C5 איירקרוס', 'C84', [2019, 2026], ['C5 AIRCROSS']),
 (CIT, 'citroen-c4-spacetourer-2018-2022-1.5-bluehdi', 'C4 SpaceTourer', 'C4 ספייסטורר', 'B78', [2018, 2022], ['C4 SPACETOURER']),
 (CIT, 'citroen-c4-2021-2026-1.5-bluehdi', 'C4 / C4 X', 'C4 / C4 X', 'C41', [2021, 2026], ['C4', 'C4X']),
 (OPL, 'opel-grandland-2018-2025-1.5-diesel', 'Grandland X', 'גרנדלנד X', 'A18', [2018, 2025], ['GRANDLAND X', 'GRANDLAND - X', 'GRANDLAND']),
]
for base, vid, model, mhe, gen_, yrs, names in dv5:
    v = dict(base, id=vid, model=model, model_he=mhe, generation=gen_, years=yrs, engines=DV5_ENG, fuel='diesel')
    write(v, PLAN_DV5, [{'names': names, 'years': yrs, 'engine_codes': ['YH01']}])

# Fiat Doblo K9 itself: Israeli book of the importer -> reviewed
p = copy.deepcopy(PLAN_DV5)
p['status'] = 'reviewed'
p['sources'] = [{'url': DOBLO_URL, 'kind': 'importer', 'note': 'ספר רכב עברי פיאט דובלו (סמלת, 06/2026), תכנית טיפולים למנוע דיזל 1.5, עמ\' 252-254 (PDF 253-255), מפרטי נוזלים עמ\' 254'}]
p['interval'] = {'km': 15000, 'months': 12, 'note': 'לפי ספר הרכב העברי של סמלת: טיפול כל שנה או 15,000 ק"מ, המוקדם; מחוון השירות עשוי להקדים את החלפת השמן'}
p['notes'] = 'לוח מתוך ספר הרכב העברי של סמלת לדובלו החדש (מנוע 1.5 דיזל). בכל טיפול: שמן ומסנן ובדיקות (בלמים, צמיגים, תאורה, AdBlue, מצבר, קריאת מחשב). כל 30,000: מסנני סולר, אוויר ומזגן, וניקוי ושימון מנעולים ומסילות. רצועת תזמון ומשאבת מים, וגם רצועת אביזרים עם המותחן: 120,000 ק"מ או 5 שנים (בתנאים קשים 80,000 ק"מ או 4 שנים). נוזל בלמים כל שנתיים. בדיקת pH לנוזל הקירור מ-120,000 ק"מ/4 שנים ובכל טיפול אחר כך. בדיקת מסנן חלקיקים מ-120,000 ק"מ/5 שנים. באזור מאובק מחליפים שמן ומסנן אוויר כל 10,000 ק"מ.'
p['specs'] = dict(p['specs']); p['specs']['_note'] = 'מתוך ספר הדובלו העברי'
write(dict(FIA, id='fiat-doblo-2023-2026-1.5-diesel', model='Doblo', model_he='דובלו', generation='K9', years=[2023, 2026],
           engines=DV5_ENG, fuel='diesel'), p, [{'names': ['DOBLO', 'FIAT DOBLO'], 'years': [2023, 2026], 'engine_codes': ['YH01']}])

# ---- PureTech turbo vehicles
PTC = ['HN01', 'HN02', 'HN05']
pt = [
 (PEU, 'peugeot-3008-2017-2025-1.2-puretech', '3008', '3008', 'P84', [2017, 2025], ['3008']),
 (PEU, 'peugeot-5008-2018-2025-1.2-puretech', '5008', '5008', 'P87', [2018, 2025], ['5008']),
 (PEU, 'peugeot-2008-2014-2026-1.2-puretech', '2008', '2008', 'A94 / P24', [2014, 2026], ['2008']),
 (PEU, 'peugeot-208-2013-2026-1.2-puretech', '208', '208', 'A9 / P21', [2013, 2026], ['208']),
 (PEU, 'peugeot-308-2014-2021-1.2-puretech', '308', '308', 'T9', [2014, 2021], ['308', '308 SW']),
 (PEU, 'peugeot-408-2023-2026-1.2-puretech', '408', '408', 'P54', [2023, 2026], ['408']),
 (CIT, 'citroen-c3-2017-2026-1.2-puretech', 'C3', 'C3', 'B618', [2017, 2026], ['C3']),
 (CIT, 'citroen-c3-aircross-2018-2026-1.2-puretech', 'C3 Aircross', 'C3 איירקרוס', 'A88', [2018, 2026], ['C3 AIRCROSS']),
 (CIT, 'citroen-c4-cactus-2015-2020-1.2-puretech', 'C4 Cactus', 'C4 קקטוס', 'E3', [2015, 2020], ['C4 CACTUS']),
 (CIT, 'citroen-c4-spacetourer-2014-2022-1.2-puretech', 'C4 Picasso / SpaceTourer', 'C4 פיקאסו / ספייסטורר', 'B78', [2014, 2022], ['C4 SPACETOURER', 'C4 PICASSO', 'GRAND C4 PICASSO']),
 (CIT, 'citroen-c4-2021-2026-1.2-puretech', 'C4 / C4 X', 'C4 / C4 X', 'C41', [2021, 2026], ['C4', 'C4X']),
 (CIT, 'citroen-c5-aircross-2019-2026-1.2-puretech', 'C5 Aircross', 'C5 איירקרוס', 'C84', [2019, 2026], ['C5 AIRCROSS']),
 (OPL, 'opel-corsa-2020-2026-1.2', 'Corsa', 'קורסה', 'F', [2020, 2026], ['CORSA']),
 (OPL, 'opel-mokka-2021-2026-1.2', 'Mokka', 'מוקה', 'B', [2021, 2026], ['MOKKA']),
 (OPL, 'opel-combo-2019-2026-1.2', 'Combo', 'קומבו', 'E (K9)', [2019, 2026], ['COMBO']),
 (OPL, 'opel-grandland-2018-2026-1.2', 'Grandland', 'גרנדלנד', 'A18', [2018, 2026], ['GRANDLAND X', 'GRANDLAND - X', 'GRANDLAND']),
 (OPL, 'opel-crossland-2018-2024-1.2', 'Crossland X', 'קרוסלנד X', 'P17', [2018, 2024], ['CROSSLAND X', 'CROSSLAND']),
 (OPL, 'opel-frontera-2025-2026-1.2', 'Frontera', 'פרונטרה', 'P2QO', [2025, 2026], ['FRONTERA']),
 (JEP, 'jeep-avenger-2023-2026-1.2', 'Avenger', "אוונג'ר", '619', [2023, 2026], ['AVENGER']),
 (DS_, 'ds-ds3-ds4-ds7-2019-2026-1.2-puretech', 'DS3 / DS4 / DS7', 'DS3 / DS4 / DS7', '', [2019, 2026], ['DS3', 'DS3 CROSSBACK', 'DS4', 'DS7', 'DS7 CROSSBACK']),
]
for base, vid, model, mhe, gen_, yrs, names in pt:
    v = dict(base, id=vid, model=model, model_he=mhe, generation=gen_, years=yrs, engines=PT_ENG, fuel='petrol')
    rules = [{'names': names, 'years': yrs, 'engine_codes': PTC}]
    if base is JEP:
        rules = [{'names': names, 'years': yrs, 'engine_codes': ['HN09']}]
        v['sources'] = [{'url': AVENGER_URL, 'kind': 'manufacturer', 'note': 'Jeep Avenger Owner Handbook (EN, 12/2022), Service schedule for 1.2 gasoline engine, pp. 213-217'},
                        {'url': 'https://samelet.com/wp-content/uploads/2023/11/AVENGER-HOVERET-2026-WEB.pdf', 'kind': 'importer', 'note': 'חוברת אחריות ושירות אוונג\'ר של סמלת: מפנה לספר הרכב, אין בה טבלת ק"מ; ספר רכב עברי מלא לאוונג\'ר לא נמצא באתר סמלת (רק מדריך מקוצר להיברידי)'},
                        SRC_OPEL_F]
    write(v, PLAN_PT, rules)

# ---- 2.0 BlueHDi vans
for base, vid, model, mhe, yrs, names in [
    (CIT, 'citroen-jumpy-2016-2026-2.0-bluehdi', 'Jumpy', "ג'אמפי", [2016, 2026], ['JUMPY', 'JUMPY HDI', 'SPACETOURER']),
    (FIA, 'fiat-scudo-2023-2026-2.0-diesel', 'Scudo', 'סקודו', [2023, 2026], ['SCUDO'])]:
    v = dict(base, id=vid, model=model, model_he=mhe, generation='K0', years=yrs, engines=['2.0 BlueHDi (DW10FC/DW10FE, קוד AH01)'], fuel='diesel')
    write(v, PLAN_PROACE, [{'names': names, 'years': yrs, 'engine_codes': ['AH01']}])
