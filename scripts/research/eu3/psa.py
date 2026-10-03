# PSA (Peugeot / Citroen) DV6 1.6 HDi/BlueHDi, EP6 1.6 THP and EB2F 1.2 VTi plans.
# Every number below was read from the official Peugeot France "PLAN D'ENTRETIEN" sheets
# (personalised plans printed from the Peugeot dealer system, mirrored on forum-peugeot.com)
# and the Peugeot "Carnet d'entretien et de garanties" 03-2014 (list of systematic operations,
# definition of severe conditions). The SEVERE column is used (see NOTE_SEV).
from gen import *

LUB = 'דוד לובינסקי'
FP = 'https://www.forum-peugeot.com/wp-content/uploads/'
CARNET = 'https://www.autojm.fr/pdf/notices/PEUGEOT/carnet-entretien-peugeot.pdf'
OPEL_F_URL = 'https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf'
LUB_WARRANTY = 'https://media-peugeot.lubit.co.il/wp-content/uploads/2023/06/Warranty-Peugeot-3Y-01.2024_Web-%D7%9E%D7%95%D7%A0%D7%92%D7%A9.pdf'

SRC_CARNET = {'url': CARNET, 'kind': 'manufacturer',
              'note': 'Peugeot France, Carnet d\'entretien et de garanties (03-2014, 14CPE0010A), עמ\' 11-12 (PDF 13-14): רשימת הפעולות הקבועות בכל טיפול, והגדרת תנאי שימוש קשים (כולל שהייה ממושכת בארץ מאובקת)'}
SRC_LUB = {'url': LUB_WARRANTY, 'kind': 'importer',
           'note': 'חוברת האחריות של לובינסקי: אין בה טבלת ק"מ; תכנית הטיפולים האישית נמסרת עם הרכב. ספרי הרכב ב-lubinski.clearmash.com חסומים (Cloudflare 403), ואתרי peugeot.co.il / citroen.co.il מחזירים 403'}
SRC_OPEL_F = {'url': OPEL_F_URL, 'kind': 'importer',
              'note': 'ספר הנהג העברי של אופל קורסה F (לובינסקי), עמ\' 205: ישראל בקבוצת מדינות שבה הטיפול כל 15,000 ק"מ או שנה למנועי PSA (EB2, DV5) - תואם את עמודת "תנאים קשים" של PSA'}

def plan_src(path, title):
    return {'url': FP + path, 'kind': 'manufacturer',
            'note': f'Peugeot France, PLAN D\'ENTRETIEN אישי ל-{title} (עותק סרוק של דף היצרן באתר forum-peugeot.com); עמודת "Conditions d\'utilisation sévères"'}

NOTE_SEV = ('לוח היבואן (לובינסקי) לא פורסם ולא נמצא. הלוח נבנה מדף "תכנית אחזקה" רשמי של פיג\'ו צרפת לאותו מנוע, '
            'לפי עמודת תנאי שימוש קשים: חוברת האחריות והאחזקה של פיג\'ו מגדירה שהייה ממושכת בארץ מאובקת, נסיעות עירוניות ונסיעות קצרות כתנאים קשים, '
            'וזה המצב בישראל. ')
NOTE_BASE = ('בכל טיפול לפי חוברת פיג\'ו: החלפת שמן ומסנן שמן, בדיקות בתוך הרכב (צופר, בלם חניה), בדיקות בטיחות מתחת לרכב (בלמים, היגוי) ובדיקת אטימות מערכות ותיבת הילוכים, '
             'בדיקת צמיגים ותאורה, בדיקות מתחת למכסה המנוע עם השלמת נוזלים, קריאת מחשבים ואיפוס מחוון הטיפול. ')

BASE = [R('engine_oil'), R('oil_filter'),
        I('parking_brake', 'כולל צופר ובדיקות בתוך הרכב'),
        I('brake_pads', 'בדיקת בטיחות של מערכת הבלמים'), I('steering'),
        I('body_underside', 'בדיקת אטימות מערכות ותיבת ההילוכים מתחת לרכב'),
        I('tires'), I('lights'),
        I('washer_fluid', 'השלמה לפי הצורך'), I('coolant', 'מפלס, השלמה לפי הצורך'), I('brake_fluid', 'מפלס'),
        I('diagnostics', 'קריאת מחשבים ואיפוס מחוון הטיפול')]
DIESEL_EXTRA = [C('fuel_filter', 'ניקוז מים ממסנן הסולר (לפי ציוד)')]

# ------------------------------------------------------------------ DV6 1.6 HDi / BlueHDi
DV6_SRC = [plan_src('2016/08/planentretien3081.6hdi92.pdf', '308 T9 1.6 HDi 92 FAP'),
           plan_src('2016/09/planentretien3008hdi100.pdf', '3008 P84 1.6 BlueHDi 100'),
           plan_src('2016/09/planentretien3008bluehdi120eat.pdf', '3008 P84 1.6 BlueHDi 120 EAT6'),
           plan_src('2016/08/planentretien3081.6hdi115.pdf', '308 T9 1.6 e-HDi 115 FAP'),
           SRC_CARNET, SRC_OPEL_F, SRC_LUB]
PLAN_DV6 = {
    'interval': {'km': 15000, 'months': 12,
                 'note': 'תכנית פיג\'ו למנוע 1.6 HDi/BlueHDi: בתנאים קשים טיפול כל 15,000 ק"מ או שנה (בתנאים רגילים באירופה 25,000 ק"מ או שנה). גם ספר אופל העברי מציין לישראל 15,000 ק"מ/שנה למנועי PSA'},
    'cycle_km': 120000,
    'grid': grid(15000, 8, BASE + DIESEL_EXTRA + [R('cabin_filter', 'או כל שנה')],
                 {30000: [R('fuel_filter', 'או כל 4 שנים'), R('air_filter', 'או כל 4 שנים')]}),
    'long': [
        LI('brake_fluid', 'replace', every_months=24, note='כל שנתיים ללא קשר לק"מ'),
        LI('coolant', 'inspect', first_km=120000, first_months=48, then_every_km=15000, then_every_months=12, note='בדיקת pH של נוזל הקירור'),
        LI('exhaust', 'inspect', first_km=90000, then_every_km=15000, note='בדיקת מפלס התוסף של מסנן החלקיקים (FAP)'),
        LI('exhaust', 'inspect', first_km=150000, then_every_km=15000, note='בדיקת סתימה של מסנן החלקיקים'),
        LI('timing_belt', 'replace', every_km=165000, every_months=120, note='ערכת רצועת תזמון יחד עם משאבת המים'),
        LI('drive_belt', 'replace', every_km=165000, every_months=120, note='ערכת רצועת אביזרים (רצועה ומותחנים)'),
        LI('drive_belt', 'replace', every_km=120000, every_months=72, note='החלפת רצועת האביזרים בלבד - בגרסאות e-HDi 115 ו-BlueHDi 120 (לא בגרסאות 75-100 כ"ס)'),
    ],
    'specs': {'engine_oil': '0W-30 בתקן PSA B71 2312 (ACEA C1/C2); החוברת מתירה גם 5W-30 B71 2290',
              'timing': 'רצועת תזמון: 165,000 ק"מ או 10 שנים בתנאים קשים (175,000 ק"מ בתנאים רגילים)',
              '_note': 'ערכים מדפי תכנית האחזקה של פיג\'ו צרפת (2016) לאותו מנוע. בדפים ישנים יותר (לפני 2012) הופיעו מרווחים אחרים, למשל רצועת תזמון 240,000 ק"מ'},
    'sources': DV6_SRC,
    'status': 'draft',
}
DV6_NOTES = (NOTE_SEV + NOTE_BASE +
             'כל טיפול (15,000 ק"מ או שנה): גם מסנן מזגן וניקוז מים ממסנן הסולר. כל 30,000 ק"מ או 4 שנים: מסנן סולר ומסנן אוויר. '
             'נוזל בלמים כל שנתיים. בדיקת pH של נוזל הקירור לראשונה ב-120,000 ק"מ או 4 שנים ואחר כך בכל טיפול. '
             'מסנן חלקיקים: בדיקת מפלס התוסף מ-90,000 ק"מ ובדיקת סתימה מ-150,000 ק"מ, ואחר כך בכל טיפול. '
             'רצועת תזמון עם משאבת מים וערכת רצועת אביזרים: 165,000 ק"מ או 10 שנים; בגרסאות 115/120 כ"ס רצועת האביזרים מוחלפת גם ב-120,000 ק"מ או 6 שנים. '
             'הדפים שנמצאו הם של דגמי פיג\'ו; סיטרואן משתמשת באותם מנועים ובאותה תכנית של קבוצת PSA. ')

# ------------------------------------------------------------------ EP6 1.6 THP
THP_SRC = [plan_src('2016/09/planentretien3008thp165.pdf', '3008 P84 1.6 THP 165 EAT6'),
           plan_src('2016/07/planentretien5008thp165.pdf', '5008 1.6 THP 165 EAT6'),
           plan_src('2016/08/planentretien3081.6thp155.pdf', '308 T9 1.6 THP 155'),
           SRC_CARNET, SRC_LUB]
PLAN_THP = {
    'interval': {'km': 20000, 'months': 12,
                 'note': 'תכנית פיג\'ו למנוע 1.6 THP: בתנאים קשים טיפול כל 20,000 ק"מ או שנה (בתנאים רגילים באירופה 30,000 ק"מ או שנה)'},
    'cycle_km': 120000,
    'grid': grid(20000, 6, BASE + [R('cabin_filter', 'או כל שנה')],
                 {40000: [R('air_filter', 'או כל 4 שנים'), R('spark_plugs', 'או כל 4 שנים')]}),
    'long': [
        LI('brake_fluid', 'replace', every_months=24, note='כל שנתיים ללא קשר לק"מ'),
        LI('coolant', 'inspect', first_km=120000, first_months=48, then_every_km=20000, then_every_months=12, note='בדיקת pH של נוזל הקירור'),
        LI('drive_belt', 'replace', every_km=180000, every_months=120, note='ערכת רצועת אביזרים'),
    ],
    'specs': {'engine_oil': '0W-30 בתקן PSA B71 2312 (ACEA C1/C2)',
              'timing': 'בתכנית אין החלפה מתוכננת של מערכת התזמון',
              '_note': 'ערכים מדפי תכנית האחזקה של פיג\'ו צרפת (2016) למנוע 1.6 THP 155/165'},
    'sources': THP_SRC,
    'status': 'draft',
}
THP_NOTES = (NOTE_SEV + NOTE_BASE +
             'בכל טיפול (20,000 ק"מ או שנה) מוחלף גם מסנן המזגן. כל 40,000 ק"מ או 4 שנים: מסנן אוויר ומצתים. נוזל בלמים כל שנתיים. '
             'בדיקת pH של נוזל הקירור לראשונה ב-120,000 ק"מ או 4 שנים ואחר כך בכל טיפול. ערכת רצועת אביזרים: 180,000 ק"מ או 10 שנים. '
             'הדפים שנמצאו הם למנוע THP 155/165 (דגמי פיג\'ו 2016); גרסאות 180 כ"ס עם תיבת EAT8 מ-2019 הן התפתחות של אותו מנוע ולא נמצא להן דף נפרד. ')

# ------------------------------------------------------------------ EB2F 1.2 VTi 82 (naturally aspirated)
EB2F_SRC = [plan_src('2019/05/planentretien208puretech82.pdf', '208 1.2 PureTech 82 S&S BVM5 (2019)'),
            plan_src('2016/06/planentretien1.2PureTech82BVM5.pdf', '108 1.2 PureTech 82 BVM5 (2016)'),
            SRC_CARNET, SRC_OPEL_F, SRC_LUB]
PLAN_EB2F = {
    'interval': {'km': 15000, 'months': 12,
                 'note': 'תכנית פיג\'ו למנוע 1.2 בנזין 82 כ"ס ללא טורבו (EB2F): בתנאים קשים טיפול כל 15,000 ק"מ או שנה (25,000 בתנאים רגילים). תואם את 15,000 ק"מ/שנה שספר אופל העברי מציין לישראל למנועי EB2'},
    'cycle_km': 90000,
    'grid': grid(15000, 6, BASE + [R('cabin_filter', 'או כל שנה')],
                 {45000: [R('air_filter', 'או כל 4 שנים'), R('spark_plugs', 'או כל 4 שנים')]}),
    'long': [
        LI('brake_fluid', 'replace', every_months=24, note='כל שנתיים ללא קשר לק"מ'),
        LI('brake_drums', 'inspect', every_km=75000, note='פירוק והרכבה של תופי הבלם האחוריים לבדיקה'),
        LI('coolant', 'inspect', first_km=120000, first_months=48, then_every_km=15000, then_every_months=12, note='בדיקת pH של נוזל הקירור'),
        LI('timing_belt', 'replace', first_km=105000, first_months=72, then_every_km=105000, then_every_months=72,
           note='רצועת תזמון רטובה: החלפת רצועה ב-105,000 ק"מ או 6 שנים, החלפת ערכה מלאה ב-210,000 ק"מ או 12 שנים, וחוזר חלילה'),
        LI('drive_belt', 'replace', first_km=105000, first_months=72, then_every_km=105000, then_every_months=72,
           note='רצועת אביזרים ב-105,000 ק"מ או 6 שנים; ערכה מלאה ב-210,000 ק"מ או 12 שנים'),
    ],
    'specs': {'engine_oil': '0W-30 בתקן PSA B71 2312 (ACEA C1/C2); מותרים גם 5W-30 B71 2290 ו-5W-40 B71 2296',
              'timing': 'רצועת תזמון טבולה בשמן: 105,000 ק"מ או 6 שנים (תכנית 2019, תנאים קשים)',
              '_note': 'תכנית 2019 של פיג\'ו 208 1.2 PureTech 82. בדף 2016 של פיג\'ו 108 (אותו מנוע) הופיעה החלפת ערכת תזמון רק ב-165,000 ק"מ או 10 שנים; הדף החדש מחמיר וגובר'},
    'sources': EB2F_SRC,
    'status': 'draft',
}
EB2F_NOTES = (NOTE_SEV + NOTE_BASE +
              'בכל טיפול (15,000 ק"מ או שנה) מוחלף גם מסנן המזגן. כל 45,000 ק"מ או 4 שנים: מסנן אוויר ומצתים. כל 75,000 ק"מ: פירוק תופי הבלם האחוריים לבדיקה. '
              'נוזל בלמים כל שנתיים. בדיקת pH של נוזל הקירור לראשונה ב-120,000 ק"מ או 4 שנים ואחר כך בכל טיפול. '
              'רצועת התזמון (טבולה בשמן) ורצועת האביזרים: 105,000 ק"מ או 6 שנים, וערכות מלאות ב-210,000 ק"מ או 12 שנים. ')

PEU = dict(make='Peugeot', make_he="פיג'ו", importer=LUB)
CIT = dict(make='Citroen', make_he='סיטרואן', importer=LUB)

def P(plan, notes):
    p = dict(plan); p['notes'] = notes; return p

DV6_B9 = ['9HX', '9HW', '9HP', '9HN', '9H06', '9H02', '9HF', 'BH02', 'BH01']

write({**CIT, 'id': 'citroen-berlingo-2008-2019-1.6-hdi', 'model': 'Berlingo', 'model_he': 'ברלינגו', 'generation': 'B9',
       'years': [2008, 2019], 'engines': ['1.6 HDi / e-HDi (DV6, קודים 9HX, 9HW, 9HP, 9HN, 9H06, 9H02, 9HF)', '1.6 BlueHDi (DV6F, קודים BH02, BH01)'],
       'fuel': 'diesel'}, P(PLAN_DV6, DV6_NOTES + 'ברלינגו B9 (2008-2019) עם מנוע 1.6 דיזל; מ-2019 ברלינגו K9 עם 1.5 BlueHDi מכוסה בקובץ אחר.'),
      [{'names': ['BERLINGO'], 'years': [2008, 2019], 'engine_codes': DV6_B9}])

write({**PEU, 'id': 'peugeot-partner-2008-2018-1.6-hdi', 'model': 'Partner', 'model_he': 'פרטנר', 'generation': 'B9',
       'years': [2008, 2018], 'engines': ['1.6 HDi / e-HDi (DV6, קודים 9HX, 9HW, 9HP, 9HN, 9H06, 9H02)', '1.6 BlueHDi (DV6F, קוד BH02)'],
       'fuel': 'diesel'}, P(PLAN_DV6, DV6_NOTES + 'פרטנר B9 (2008-2018) עם מנוע 1.6 דיזל.'),
      [{'names': ['PARTNER', 'NEW PARTNER', 'PARTNER TEPEE'], 'years': [2008, 2018], 'engine_codes': DV6_B9}])

write({**PEU, 'id': 'peugeot-3008-5008-2016-2019-1.6-bluehdi', 'model': '3008 / 5008 / 208 / 2008 / 301', 'model_he': '3008 / 5008 / 208 / 2008 / 301',
       'years': [2016, 2019], 'engines': ['1.6 BlueHDi 100/120 (DV6F, קודים BH01, BH02)'],
       'fuel': 'diesel'}, P(PLAN_DV6, DV6_NOTES + 'בעיקר 3008/5008 דור שני (P84/P87) עם 1.6 BlueHDi 120 ותיבה אוטומטית EAT6, וגם 208/2008/301 עם 1.6 BlueHDi.'),
      [{'names': ['3008'], 'years': [2016, 2019], 'engine_codes': ['BH01', 'BH02']},
       {'names': ['5008'], 'years': [2017, 2019], 'engine_codes': ['BH01', 'BH02']},
       {'names': ['208', '2008', '301', '308', '308 SW'], 'years': [2015, 2019], 'engine_codes': ['BH01', 'BH02']}])

write({**CIT, 'id': 'citroen-c3-c4-picasso-cactus-2010-2018-1.6-hdi', 'model': 'C3 Picasso / C4 Picasso / C4 Cactus / C3 / C4', 'model_he': 'C3 פיקאסו / C4 פיקאסו / C4 קקטוס / C3 / C4',
       'years': [2010, 2018], 'engines': ['1.6 HDi / e-HDi (DV6, קודים 9HP, 9H06, 9HR, 9H05)', '1.6 BlueHDi (DV6F, קודים BH01, BH02)'],
       'fuel': 'diesel'}, P(PLAN_DV6, DV6_NOTES + 'דגמי סיטרואן נוסעים עם מנוע 1.6 דיזל: C3 פיקאסו, C4 פיקאסו/ספייסטורר (BlueHDi), C4 קקטוס, C3 ו-C4.'),
      [{'names': ['C3 PICASSO'], 'years': [2009, 2018], 'engine_codes': ['9HP', '9H06', '9HN', 'BH02', 'BH01']},
       {'names': ['C4 PICASSO', 'C4 SPACETOURER', 'C4 GD PICASSO', 'GRAND C4 PICASSO'], 'years': [2014, 2018], 'engine_codes': ['BH01', 'BH02']},
       {'names': ['C4 CACTUS'], 'years': [2014, 2018], 'engine_codes': ['BH01', 'BH02', '9H06']},
       {'names': ['C3', 'C4', 'C-ELYSEE', 'DS3'], 'years': [2010, 2018], 'engine_codes': ['9HP', '9H06', '9HR', '9H05', 'BH01', 'BH02']}])

THP_CODES = ['5FV', '5G01', '5G06']
write({**PEU, 'id': 'peugeot-3008-5008-508-2010-2023-1.6-thp', 'model': '3008 / 5008 / 508', 'model_he': '3008 / 5008 / 508',
       'years': [2010, 2023], 'engines': ['1.6 THP 150-180 (EP6 טורבו, קודים 5FV, 5G01, 5G06)'],
       'fuel': 'petrol'}, P(PLAN_THP, THP_NOTES + 'בעיקר 3008 ו-5008 עם 1.6 THP ותיבה אוטומטית (165 כ"ס EAT6 עד 2018, 180 כ"ס EAT8 מ-2019), וגם 508, RCZ ו-308. לא כולל את גרסת ההיבריד הנטענת (3008 HYBRID4).'),
      [{'names': ['3008', '5008', '508', 'RCZ', '208', '308', '308 SW'], 'years': [2010, 2023], 'fuel': ['בנזין'], 'engine_codes': THP_CODES}])

write({**CIT, 'id': 'citroen-c4-picasso-c5-aircross-2011-2023-1.6-thp', 'model': 'C4 Picasso / C4 SpaceTourer / C5 Aircross', 'model_he': 'C4 פיקאסו / C4 ספייסטורר / C5 איירקרוס',
       'years': [2011, 2023], 'engines': ['1.6 THP 155-180 (EP6 טורבו, קודים 5FV, 5G01, 5G06)'],
       'fuel': 'petrol'}, P(PLAN_THP, THP_NOTES + 'C4 פיקאסו/גרנד פיקאסו ו-C4 ספייסטורר עם 1.6 THP 165 (2014-2019), C5 איירקרוס עם 1.6 THP 180 (2019-2023), וגם C5 ו-C4 עם 1.6 THP 156. לא כולל גרסאות היבריד נטענות.'),
      [{'names': ['C4 PICASSO', 'C4 GD PICASSO', 'GRAND C4 PICASSO', 'C4 SPACETOURER', 'C5 AIRCROSS', 'C5', 'C4', 'DS4', 'DS5'], 'years': [2011, 2023], 'fuel': ['בנזין'], 'engine_codes': THP_CODES}])
RULES.append({'make': 'DS', 'names': ['DS4', 'DS 4', 'DS7', 'DS 7'], 'years': [2018, 2024], 'fuel': ['בנזין'], 'engine_codes': ['5G06'], 'schedule': 'citroen-c4-picasso-c5-aircross-2011-2023-1.6-thp'})

write({**PEU, 'id': 'peugeot-208-2008-301-2013-2017-1.2-vti', 'model': '208 / 2008 / 301', 'model_he': '208 / 2008 / 301',
       'years': [2013, 2017], 'engines': ['1.2 VTi / PureTech 72-82 ללא טורבו (EB2, קודים HM01, HMZ, HM02)'],
       'fuel': 'petrol'}, P(PLAN_EB2F, EB2F_NOTES + 'פיג\'ו 208, 2008 ו-301 עם מנוע 1.2 שלושה צילינדרים ללא טורבו. דגמי 1.2 טורבו (HN01/HN02/HN05) מכוסים בקבצים אחרים.'),
      [{'names': ['208', '2008', '301'], 'years': [2012, 2017], 'engine_codes': ['HM01', 'HMZ-HM01', 'HMZ', 'HM02', 'HM05']}])

write({**CIT, 'id': 'citroen-c4-cactus-c3-2014-2017-1.2-vti', 'model': 'C4 Cactus / C3 / C-Elysee', 'model_he': 'C4 קקטוס / C3 / C-אליזה',
       'years': [2014, 2017], 'engines': ['1.2 VTi / PureTech 72-82 ללא טורבו (EB2, קודים HM01, HMZ, HM02)'],
       'fuel': 'petrol'}, P(PLAN_EB2F, EB2F_NOTES + 'סיטרואן C4 קקטוס, C3 ו-C-אליזה עם מנוע 1.2 שלושה צילינדרים ללא טורבו; הדפים שנמצאו הם של פיג\'ו 208/108 עם אותו מנוע.'),
      [{'names': ['C4 CACTUS', 'C3', 'C-ELYSEE', 'C ELYSEE', 'DS3'], 'years': [2013, 2017], 'engine_codes': ['HM01', 'HMZ-HM01', 'HMZ', 'HM02', 'HM05']}])
