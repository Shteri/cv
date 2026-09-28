import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/dl/japan-b')
from gen import *
API = 'https://books.union-motors.co.il/LexusApp/api/files/{}/download'
PAGE = 'https://www.lexus.co.il/owners/maintenance/owner-books'
IMP = 'יוניון מוטורס'
E30 = '-I-I-I'

def lx(id_, model, model_he, gen, years, engines, fuel='hybrid', note=None):
    return S(id_, 'Lexus', 'לקסוס', model, model_he, gen, years, engines, fuel, IMP, 15000, 12,
             note or 'לפי לוח האחזקה בספר הרכב העברי: טיפול כל 15,000 ק"מ או 12 חודשים, המוקדם', 90000)

COOL_NOTE = 'בספר מופיע "בדיקה ראשונה ב-150,000 ק\"מ ואחר כך כל 90,000"; בספרי לקסוס אחרים (RX450h, NX300) אותה שורה מנוסחת כהחלפה'

def hybrid_common(s, oil_by_reminder, air, canister, cabin):
    if oil_by_reminder:
        s.every('engine_oil', 'replace', 15000, 'כאשר מופיעה נורית תזכורת התחזוקה, ולכל המאוחר כל 15,000 ק"מ או 12 חודשים')
        s.every('oil_filter', 'replace', 15000, 'יחד עם שמן המנוע')
    else:
        s.every('engine_oil', 'replace', 15000); s.every('oil_filter', 'replace', 15000)
    s.pat('cooling_system', E30, 15000)
    s.pat('coolant', E30, 15000, 'בדיקת נוזל קירור המנוע')
    s.pat('hybrid_system', E30, 15000, 'בדיקת נוזל הקירור של הממיר (Inverter)')
    s.every('exhaust', 'inspect', 15000)
    s.every('battery_12v', 'inspect', 15000)
    s.pat('air_filter', air, 15000, 'בדיקה כל 24 חודשים, החלפה כל 48 חודשים')
    s.pat('fuel_lines', E30, 15000, 'מכסה מיכל הדלק, צינורות, חיבורים ושסתום בקרת אידוי')
    s.pat('evap_system', canister, 15000, 'מיכל פחם')
    s.every('pedals', 'inspect', 15000, 'דוושת בלם ובלם חניה')
    s.every('brake_pads', 'inspect', 15000); s.every('brake_discs', 'inspect', 15000)
    s.pat('brake_fluid', 'IRIRIR', 15000, 'בדיקה כל 12 חודשים, החלפה כל 24 חודשים')
    s.every('brake_lines', 'inspect', 15000)
    s.every('steering', 'inspect', 15000, 'גלגל הגה, מוטות קישור ותיבת הגה')
    s.every('cv_boots', 'inspect', 15000)
    s.every('suspension', 'inspect', 15000, 'מתלים קדמיים ואחוריים, מפרקים כדוריים וכיסויי אבק')
    s.pat('transmission_oil', E30, 15000, 'בדיקת נוזל תיבת ההילוכים')
    s.every('tires', 'inspect', 15000, 'צמיגים ולחץ ניפוח')
    s.every('lights', 'inspect', 15000, 'אורות, צופר, מגבים ומתזים')
    s.pat('cabin_filter', cabin, 15000)
    s.every('body_underside', 'inspect', 15000, 'בדיקת חלודה; בדיקת שטיח הרצפה')
    s.add(90000, 'spark_plugs', 'replace', 'מצתי אירידיום/פלטינה')
    s.li('spark_plugs', 'replace', every_km=90000)
    s.li('fuel_filter', 'replace', every_km=120000, every_months=144)
    s.li('coolant', 'replace', first_km=150000, then_every_km=90000, note=COOL_NOTE)
    s.li('hybrid_system', 'replace', first_km=240000, then_every_km=90000, note='נוזל קירור הממיר (Inverter): החלפה ראשונה ב-240,000 ק"מ ואחר כך כל 90,000')

def drive_belt(s):
    s.li('drive_belt', 'inspect', first_km=105000, then_every_km=15000, first_months=72, then_every_months=12)

HY_SPECS = {}

# ---------- CT200h ----------
s = lx('lexus-ct200h-2011-2020-1.8-hybrid', 'CT 200h', 'CT 200h', 'ZWA10', (2011, 2020), ['1.8 hybrid (2ZR-FXE)'])
hybrid_common(s, False, 'IIIRII', '---I-I', 'CRCRCR')
s.pat('differential_oil', E30, 15000, 'שמן דיפרנציאל קדמי')
s.src(API.format(88), 'importer', 'ספר רכב CT בעברית (יוניון מוטורס), פרק 7-2 "תחזוקה", עמודים 87-88 (לוח 6 עמודות של 15,000 ק"מ)')
s.src(PAGE, 'importer', 'דף ספרי הרכב של לקסוס ישראל (אפליקציה books.union-motors.co.il/LexusApp)')
s.write('reviewed', 'הועתק מלוח האחזקה בספר הרכב העברי של CT (שנים 2014-2021 באתר). הלוח מכסה 90,000 ק"מ; מסנן מזגן מתחלף כל 30,000 ומנוקה ב-15,000 שביניהם. נוזל בלמים מתחלף כל 30,000 ק"מ או 24 חודשים. מסנן דלק כל 120,000 ק"מ.')
rule('Lexus', ['LEXUS CT200H', 'CT200H', 'CT 200H'], (2011, 2022), s.d['id'])

# ---------- NX300h ----------
s = lx('lexus-nx300h-2014-2021-2.5-hybrid', 'NX 300h', 'NX 300h', 'AZ10', (2014, 2021), ['2.5 hybrid (2AR-FXE)'])
hybrid_common(s, True, 'IIIRII', '--I--I', 'RRRRRR')
drive_belt(s)
s.pat('differential_oil', E30, 15000, 'שמן דיפרנציאל קדמי: בדיקה; בדגמי 4X4 גם דיפרנציאל אחורי ב-45,000 וב-90,000')
s.pat('differential_oil', '--I--I', 15000)
s.src(API.format(162), 'importer', 'ספר רכב NX300h בעברית, פרק 7-2, עמודים 98-99')
s.src(PAGE, 'importer', 'דף ספרי הרכב של לקסוס ישראל')
s.write('reviewed', 'הועתק מלוח האחזקה בספר הרכב העברי של NX300h (2014-2017; הדגם נמכר עד 2021 עם אותו מנוע). שמן ומסנן מתחלפים לפי נורית התזכורת ולא יאוחר מ-15,000 ק"מ או 12 חודשים. רצועת הינע: בדיקה ראשונה ב-105,000 ואחר כך כל 15,000. מסנן מזגן מוחלף בכל טיפול.')
rule('Lexus', ['LEXUS NX300H', 'NX300H'], (2014, 2021), s.d['id'])

# ---------- IS300h ----------
s = lx('lexus-is300h-2013-2020-2.5-hybrid', 'IS 300h', 'IS 300h', 'AVE30', (2013, 2020), ['2.5 hybrid (2AR-FSE)'])
hybrid_common(s, False, 'IIIRII', '---I-I', 'RRRRRR')
drive_belt(s)
s.pat('parking_brake', E30, 15000, 'סוליות ותופי בלם החניה')
s.pat('differential_oil', 'IRIRIR', 15000, 'שמן דיפרנציאל אחורי: בדיקה כל 12 חודשים, החלפה כל 48 חודשים')
s.src(API.format(114), 'importer', 'ספר רכב IS300 (היברידי, 2018-2020) בעברית, פרק 7-2, עמודים 89-90')
s.src(PAGE, 'importer', 'דף ספרי הרכב של לקסוס ישראל')
s.write('reviewed', 'הועתק מלוח האחזקה בספר הרכב העברי של IS300 (הדגם ההיברידי; בלוח מופיע נוזל קירור ממיר). הנעה אחורית: שמן דיפרנציאל אחורי מוחלף כל 30,000 ק"מ. נוזל הקירור כולל גם את מצנן הביניים.')
rule('Lexus', ['LEXUS IS300H', 'IS300H'], (2013, 2020), s.d['id'])

# ---------- GS300h ----------
s = lx('lexus-gs300h-2013-2018-2.5-hybrid', 'GS 300h', 'GS 300h', 'AWL10', (2013, 2018), ['2.5 hybrid (2AR-FSE)'])
hybrid_common(s, True, 'IIIRII', '--I--I', 'RRRRRR')
drive_belt(s)
s.pat('parking_brake', E30, 15000, 'סוליות ותופי בלם החניה')
s.pat('differential_oil', 'IRIRIR', 15000, 'שמן דיפרנציאל אחורי: בדיקה כל 12 חודשים, החלפה כל 48 חודשים')
s.src(API.format(107), 'importer', 'ספר רכב GS300 בעברית (2016-2018), פרק 6-2, הלוח "GS300h" בעמודים 106-107')
s.src(PAGE, 'importer', 'דף ספרי הרכב של לקסוס ישראל')
s.write('reviewed', 'הועתק מלוח ה-GS300h בספר הרכב העברי. שמן לפי נורית התזכורת ולא יאוחר מ-15,000 ק"מ או 12 חודשים. שמן דיפרנציאל אחורי מוחלף כל 30,000 ק"מ.')
rule('Lexus', ['LEXUS GS300H', 'GS300H'], (2013, 2018), s.d['id'])

# ---------- NX200t ----------
s = lx('lexus-nx200t-2014-2017-2.0-turbo', 'NX 200t', 'NX 200t', 'AGZ10', (2014, 2017), ['2.0 turbo (8AR-FTS)'], fuel='petrol')
s.every('engine_oil', 'replace', 15000, 'כאשר מופיעה נורית תזכורת התחזוקה, ולכל המאוחר כל 15,000 ק"מ או 12 חודשים')
s.every('oil_filter', 'replace', 15000, 'יחד עם שמן המנוע')
drive_belt(s)
s.pat('cooling_system', E30, 15000)
s.pat('coolant', E30, 15000, 'בדיקת נוזל קירור')
s.every('exhaust', 'inspect', 15000)
s.every('battery_12v', 'inspect', 15000)
s.add(60000, 'spark_plugs', 'replace')
s.li('spark_plugs', 'replace', every_km=60000)
s.add(75000, 'fuel_filter', 'replace', 'בלוח: החלפה ב-75,000 ק"מ או 96 חודשים')
s.pat('air_filter', 'IIIRII', 15000, 'בדיקה כל 24 חודשים, החלפה כל 48 חודשים')
s.pat('fuel_lines', E30, 15000, 'מכסה מיכל הדלק, צינורות, חיבורים ושסתום בקרת אידוי')
s.pat('evap_system', '--I--I', 15000, 'מיכל פחם')
s.every('pedals', 'inspect', 15000, 'דוושת בלם ובלם חניה')
s.every('brake_pads', 'inspect', 15000); s.every('brake_discs', 'inspect', 15000)
s.pat('brake_fluid', 'IRIRIR', 15000, 'בדיקה כל 12 חודשים, החלפה כל 24 חודשים')
s.every('brake_lines', 'inspect', 15000)
s.li('vacuum_hose', 'inspect', every_km=200000, note='משאבת ריק (ואקום) למגבר הבלמים: בדיקה כל 200,000 ק"מ')
s.every('steering', 'inspect', 15000, 'גלגל הגה, מוטות קישור ותיבת הגה')
s.every('cv_boots', 'inspect', 15000)
s.every('suspension', 'inspect', 15000, 'מתלים, מפרקים כדוריים וכיסויי אבק')
s.pat('transmission_oil', E30, 15000, 'בדיקת נוזל תיבת הילוכים אוטומטית')
s.pat('transfer_case_oil', '-R-R-R', 15000, 'אם קיימת (4X4): החלפה כל 30,000 ק"מ או 48 חודשים')
s.pat('differential_oil', E30, 15000, 'דיפרנציאל קדמי: בדיקה; דיפרנציאל אחורי (אם קיים): החלפה כל 30,000 ק"מ או 48 חודשים')
s.pat('differential_oil', '-R-R-R', 15000)
s.every('tires', 'inspect', 15000, 'צמיגים ולחץ ניפוח')
s.every('lights', 'inspect', 15000, 'אורות, צופר, מגבים ומתזים')
s.every('cabin_filter', 'replace', 15000)
s.every('body_underside', 'inspect', 15000, 'בדיקת חלודה; בדיקת שטיח הרצפה')
s.src(API.format(154), 'importer', 'ספר רכב NX200t בעברית (2014-2017), פרק 7-2, עמודים 92-93')
s.src(PAGE, 'importer', 'דף ספרי הרכב של לקסוס ישראל')
s.write('reviewed', 'הועתק מלוח האחזקה בספר הרכב העברי של NX200t (מנוע טורבו 2.0). מצתים כל 60,000 ק"מ. מסנן דלק מסומן בלוח ב-75,000 ק"מ (או 96 חודשים). בגרסת 4X4 שמן תיבת העברה ודיפרנציאל אחורי מוחלפים כל 30,000 ק"מ.')
rule('Lexus', ['LEXUS NX200T', 'NX200T'], (2014, 2017), s.d['id'])

# ---------- RX450h AL20 ----------
s = lx('lexus-rx450h-2016-2022-3.5-hybrid', 'RX 450h', 'RX 450h', 'AL20', (2016, 2022), ['3.5 V6 hybrid (2GR-FXS)'],
       note='לפי לוח האחזקה בספר הרכב: שמן כשנדלקת נורית ההחלפה, ולכל המאוחר כל 15,000 ק"מ או 12 חודשים')
s.d['cycle_km'] = 150000
C = 15000
s.every('engine_oil', 'replace', C, 'כאשר נדלקת נורית החלפת השמן, ולכל המאוחר כל 15,000 ק"מ או 12 חודשים; בתנאים מחמירים כל 7,500 ק"מ או 6 חודשים')
s.every('oil_filter', 'replace', C)
P30 = '-I-I-I-I-I'
for it, n in [('cooling_system', None), ('coolant', 'בדיקת נוזל קירור המנוע'), ('hybrid_system', 'בדיקת נוזל קירור הממיר (Inverter)'),
              ('exhaust', None), ('fuel_lines', 'צינורות דלק, חיבורים ומכסה מיכל הדלק'), ('pedals', 'דוושת בלם'),
              ('brake_lines', None), ('steering', 'מסרק הגה, מוטות הגה וגלגל ההגה'), ('cv_boots', None),
              ('suspension', 'מתלים, מחברים כדוריים ומגיני אבק'), ('tires', 'צמיגים ולחץ ניפוח'),
              ('lights', 'אורות, צופר, מגבים ומתזים'), ('body_underside', 'בדיקת חלודה')]:
    s.pat(it, P30, C, n)
s.pat('air_filter', 'IIRIIRIIRI', C, 'בדיקה כל 24 חודשים, החלפה כל 48 חודשים')
s.pat('evap_system', '--I--I--I-', C, 'מכלול מסנן פחם')
s.every('brake_pads', 'inspect', C); s.every('brake_discs', 'inspect', C)
s.pat('brake_fluid', '-R-R-R-R-R', C, 'החלפה כל 30,000 ק"מ או 24 חודשים')
s.pat('transmission_oil', '---I---I--', C, 'בדיקה כל 60,000 ק"מ או 48 חודשים')
s.pat('differential_oil', '---I---I--', C, 'דיפרנציאל קדמי: בדיקה כל 60,000 ק"מ; דיפרנציאל אחורי: בדיקה ב-45,000/90,000/135,000')
s.pat('differential_oil', '--I--I--I-', C)
s.every('cabin_filter', 'replace', C, 'בתנאים מחמירים כל 7,500 ק"מ')
s.add(90000, 'spark_plugs', 'replace', 'מצתי אירידיום/פלטינה')
s.li('spark_plugs', 'replace', every_km=90000)
s.li('coolant', 'replace', first_km=150000, then_every_km=90000)
s.li('hybrid_system', 'replace', first_km=240000, then_every_km=90000, note='נוזל קירור הממיר (Inverter)')
s.src(API.format(150), 'importer', 'ספר רכב RX450h/RX450L בעברית (2016-2019), עמוד 746: "לוח אחזקה RX450h \\ RX450h Long 2GR-FXS" מתאריך 26.4.18, 10 עמודות של 15,000 ק"מ')
s.src(PAGE, 'importer', 'דף ספרי הרכב של לקסוס ישראל')
s.write('reviewed', 'הועתק מלוח האחזקה הישראלי של RX450h (דור AL20). בתנאים מחמירים: שמן ומסנן כל 7,500 ק"מ, בדיקות מתלים והגה כל 15,000, נוזל גיר ושמני דיפרנציאל מוחלפים כל 90,000 ק"מ (72 חודשים). הלוח כולל גם טבלת נוזלים: שמן 0W-20, כ-5.4 ליטר עם מסנן.',
        specs={'engine_oil': '0W-20 / 5W-30 / 10W-30 (API SL/SM/SN או ILSAC)', 'oil_capacity': '5.4 ליטר עם מסנן, 5.3 ליטר בלי', 'coolant': 'Toyota Super Long Life Coolant; 9.8 ליטר (RX450h), 12.2 ליטר (RX450h Long); ממיר 1.9 ליטר', 'brake_fluid': 'DOT 3 / DOT 4'})
rule('Lexus', ['LEXUS RX450H', 'RX450H', 'LEXUS RX450H P'], (2016, 2022), s.d['id'])
save_rules('rules_lexus.json')
