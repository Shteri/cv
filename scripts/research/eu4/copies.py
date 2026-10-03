# Toyota Proace / City Van (Union Motors Israeli sheets), VAG clones, PSA registry-only sister rules.
import json, copy
from gen import *
SCH = '/home/user/cv/data/schedules/'
def load(i): return json.load(open(SCH + i + '.json'))
UNION = 'יוניון מוטורס'

def proace():
    s = load('citroen-jumpy-2016-2026-2.0-bluehdi')
    s['id'] = 'toyota-proace-2016-2026-2.0-diesel'
    s['make'] = 'Toyota'; s['make_he'] = 'טויוטה'; s['model'] = 'Proace / Proace Verso'; s['model_he'] = 'פרואייס / פרואייס ורסו'
    s['generation'] = 'K0'; s['importer'] = UNION; s['years'] = [2016, 2026]
    s['engines'] = ['2.0 D-4D (PSA DW10FC/DW10FE, קוד AH01)']
    s['sources'] = [{'url': 'https://books.union-motors.co.il/app/api/files/603/download', 'kind': 'importer',
                     'note': 'לוח אחזקה פרואייס 2017 של יוניון מוטורס (26/07/2017), מנועי DW10FC/DW10FE: עמודות 10,000 עד 160,000 ק"מ עם טיפול כל 20,000. נבדק מחדש מול הקובץ שבמאגר (citroen-jumpy-2016-2026-2.0-bluehdi) שנבנה מאותו לוח'}]
    s['status'] = 'reviewed'
    s['notes'] = ('לוח האחזקה הישראלי של יוניון מוטורס לטויוטה פרואייס עם מנוע 2.0 דיזל. טיפול כל 20,000 ק"מ או שנה: שמן ומסנן, השלמת נוזלים ואוריאה, ובדיקות מנוע, בלמים, היגוי, מתלים ומרכב; מסנן המזגן מנוקה בטיפולי הביניים. '
                  'כל 40,000 ק"מ: מסנני אוויר, סולר ומזגן. בדיקת pH לנוזל הקירור מ-120,000 ק"מ או 4 שנים, תוסף מסנן חלקיקים ב-80,000 וב-160,000 ובדיקת סתימה מ-160,000. '
                  'רצועת אביזרים ב-120,000 ק"מ או 6 שנים, רצועת תזמון עם משאבת מים ב-140,000 ק"מ או 10 שנים, נוזל בלמים כל שנתיים.')
    write(s, [{'make': 'Toyota', 'names': ['PROACE', 'PROACE VERSO'], 'years': [2016, 2026], 'engine_codes': ['AH01'], 'fuel': ['דיזל']}])

def city_van():
    # Union Motors sheet 1190 (01/07/2021) "לוח אחזקה (M1)CITY (גיר אוטומטי) דגם BKYMA", engine DV5Rd/DV5RC. 14 columns 15..210 x1000 km.
    ALL = 'all'; E2 = {2, 4, 6, 8, 10, 12, 14}; ODD = {1, 3, 5, 7, 9, 11, 13}
    g = [
        (ALL, it('engine_oil', 'replace')), (ALL, it('oil_filter', 'replace')),
        (E2, it('cooling_system', 'inspect', 'מערכת קירור וחימום, כולל ניקיון המקרן')),
        (ALL, it('coolant', 'inspect', 'השלמה לפי הצורך')),
        (ALL, it('exhaust', 'inspect', 'צנרת פליטה ותומכים')),
        (ALL, it('vacuum_hose', 'inspect', 'צנרת, אטמים ובתי מסננים: בדיקה חזותית לדליפות')),
        (ALL, it('fuel_lines', 'inspect', 'צנרת דלק, חיבורים ומכסה מיכל; גם בדיקת עשן')),
        (E2, it('air_filter', 'replace')), (ODD, it('air_filter', 'inspect')),
        (E2, it('fuel_filter', 'replace', 'מסנן סולר')),
        (ALL, it('adblue', 'inspect', 'מילוי אוריאה (AdBlue)')),
        (ALL, it('body_underside', 'inspect', 'קורוזיה בגוף הרכב')),
        (ALL, it('parking_brake', 'inspect', 'דוושת בלם ובלם חניה')),
        (ALL, it('brake_pads', 'inspect', 'כולל פירוק גלגלים; גם קליפרים')),
        (ALL, it('brake_discs', 'inspect')), (ALL, it('brake_lines', 'inspect')),
        (ALL, it('brake_fluid', 'inspect')),
        (ALL, it('steering', 'inspect', 'מפרקים כדוריים וכיסויי אבק')),
        (ALL, it('suspension', 'inspect', 'אטימות בולמי זעזועים')),
        (ALL, it('cv_boots', 'inspect')),
        (ALL, it('tires', 'inspect', 'לחץ, תאריך ייצור וגלגל חלופי')),
        (ALL, it('lights', 'inspect', 'אורות, צופר, חלונות ומראות')),
        (ALL, it('wipers', 'inspect')), (ALL, it('washer_fluid', 'inspect')),
        (ALL, it('battery_12v', 'inspect')),
        (E2, it('cabin_filter', 'replace')), (ODD, it('cabin_filter', 'clean', 'בדיקה וניקוי')),
    ]
    s = {'id': 'toyota-city-van-2022-2026-1.5-diesel', 'make': 'Toyota', 'make_he': 'טויוטה', 'model': 'Proace City (City Van)', 'model_he': 'פרואייס סיטי',
         'generation': 'K9', 'years': [2020, 2026], 'engines': ['1.5 D-4D (PSA DV5RD/DV5RC, קוד YH01)'], 'fuel': 'diesel', 'importer': UNION,
         'interval': {'km': 15000, 'months': 12, 'note': 'לוח יוניון מוטורס: טיפול כל 15,000 ק"מ; שמן ומסנן כל שנה'},
         'cycle_km': 210000, 'services': build(15000, 14, g),
         'long_interval': [
             LI('coolant', 'inspect', first_km=120000, first_months=48, then_every_km=15000, then_every_months=12, note='בדיקת pH'),
             LI('drive_belt', 'replace', first_km=120000, then_every_km=160000, note='בכל החלפה בודקים גם את המותחנים'),
             LI('drive_belt', 'replace', every_km=180000, every_months=120, note='מותחני רצועת האביזרים'),
             LI('timing_belt', 'replace', every_km=180000, every_months=120, note='כולל מותחנים ומשאבת מים'),
             LI('diagnostics', 'inspect', first_km=160000, then_every_km=15000, note='בדיקת סתימת מסנן חלקיקים במחשב'),
             LI('brake_fluid', 'replace', every_months=24),
             LI('air_filter', 'replace', every_months=48), LI('fuel_filter', 'replace', every_months=48)],
         'specs': {'engine_oil': '5W-30 ACEA C2, תקן PSA B71 2297', 'oil_capacity': '3.5 ליטר', 'coolant': 'Premium long life coolant', 'brake_fluid': 'DOT 4',
                   'timing': 'רצועת תזמון: 180,000 ק"מ או 10 שנים'},
         'sources': [{'url': 'https://books.union-motors.co.il/app/api/files/1190/download', 'kind': 'importer',
                      'note': 'לוח אחזקה של יוניון מוטורס (01/07/2021) ל-CITY (M1, גיר אוטומטי, דגם BKYMA), מנוע DV5Rd/DV5RC: 14 עמודות מ-15,000 עד 210,000 ק"מ, וטבלת נוזלים'}],
         'status': 'reviewed',
         'notes': ('לוח היבואן הישראלי לטויוטה פרואייס סיטי עם מנוע 1.5 דיזל. בכל טיפול (15,000 ק"מ או שנה): שמן ומסנן, מילוי אוריאה, בדיקות נוזלים, צנרת, בלמים (עם פירוק גלגלים), היגוי, מתלים, צמיגים, תאורה ומצבר; מסנני אוויר ומזגן נבדקים ומנוקים. '
                   'כל 30,000 ק"מ: מסנני אוויר, סולר ומזגן ובדיקת מערכת הקירור. רצועת אביזרים ראשונה ב-120,000 ואז כל 160,000; רצועת תזמון עם משאבת מים ומותחני רצועת האביזרים כל 180,000 ק"מ או 10 שנים. נוזל בלמים כל שנתיים. '
                   'הלוח נכתב לגרסת הנוסעים האוטומטית; לגרסת המסחרית לא נמצא לוח נפרד.')}
    write(s, [{'make': 'Toyota', 'names': ['TOYOTA CITY VAN', 'PROACE CITY', 'PROACE CITY VERSO', 'CITY VAN'], 'years': [2020, 2026], 'engine_codes': ['YH01'], 'fuel': ['דיזל']}])

def audi_ea888():
    s = load('audi-q5-2009-2017-2.0-tfsi')
    s['id'] = 'audi-a4-a5-a6-2008-2016-1.8-2.0-tfsi'
    s['model'] = 'A4 / A5 / A6'; s['model_he'] = 'A4 / A5 / A6'; s['generation'] = 'B8 (A4/A5), C7 (A6)'; s['years'] = [2008, 2016]
    s['engines'] = ['1.8 TFSI (CDH/CAB, EA888 דור 2)', '2.0 TFSI (CDN, EA888 דור 2; CJE, EA888 דור 3)']
    s['sources'] = s['sources'] + [{'url': 'https://vwts.ru/petrol-engine-vw-audi-skoda-repair-manual.html', 'kind': 'other',
        'note': 'אינדקס ספרי התיקון של קבוצת פולקסווגן: קודים CDHA/CDHB/CABx/CDNx בספר "1.8L and 2.0L 4V TFSI Engine (EA 888 Generation II)" לאאודי A4 2008 ואילך, וקודי CJEx בספר "2.0 ltr 4V TFSI (EA 888 Gen. III)"; שניהם מנועי שרשרת'}]
    s['notes'] = ('עותק של קובץ ה-Q5 2.0 TFSI שבמאגר (אותה משפחת מנוע EA888 עם שרשרת תזמון ואותה תבנית שירות של קבוצת פולקסווגן), עם שיוך לאאודי A4/A5 מדור B8 ו-A6 מדור C7 לפי קוד המנוע. '
                  'טיפול כל 15,000 ק"מ או שנה; מסנני אוויר ומזגן, מצתים, נוזל בלמים ושמן מצמד הלדקס לפי הלוח הארוך. '
                  'ב-A4 עם תיבת מולטיטרוניק (CVT) אין בתבנית שורה לשמן התיבה, ולא נמצא מסמך שקובע לה מרווח. טיוטה: התבנית לא נכתבה במקור לדגמים אלה.')
    write(s, [{'make': 'Audi', 'names': ['A4', 'AUDI A4', 'A4 AVANT'], 'years': [2008, 2016], 'engine_codes': ['CDH', 'CAB', 'CJE', 'CDN'], 'fuel': ['בנזין']},
              {'make': 'Audi', 'names': ['A5', 'A5 SPORTBACK', 'A5 COUPE'], 'years': [2008, 2016], 'engine_codes': ['CDH', 'CAB', 'CJE', 'CDN'], 'fuel': ['בנזין']},
              {'make': 'Audi', 'names': ['A6'], 'years': [2011, 2016], 'engine_codes': ['CDN', 'CJE'], 'fuel': ['בנזין']}])

def tdi19(id_, make, make_he, model, model_he, gen, years, rules):
    s = load('skoda-octavia-2011-2017-1.6-tdi')
    s['id'] = id_; s['make'] = make; s['make_he'] = make_he; s['model'] = model; s['model_he'] = model_he; s['generation'] = gen; s['years'] = years
    s['engines'] = ['1.9 TDI PD (BXE/BLS)', '2.0 TDI PD (BKD)']
    for sv in s['services']:
        sv['items'] = [i for i in sv['items'] if i['item'] != 'timing_belt']
    s['long_interval'] = [l for l in s['long_interval'] if l['item'] != 'timing_belt'] + [
        LI('timing_belt', 'replace', every_km=150000, note='מנועי TDI עם מזרקי יחידה (PD) משנת דגם 2007; לפני 2007 כל 120,000'),
        LI('timing_belt', 'replace', every_km=300000, note='גלגלת המתיחה של רצועת התזמון (משנת דגם 2007)')]
    s['sources'] = [{'url': 'https://vwts.ru/vw/g5/golf_2004_golf_plus_2005_maintenance_eng.pdf', 'kind': 'manufacturer',
                     'note': 'VW Golf 2004 / Golf Plus 2005 Maintenance, מהדורה 11.2009, עמ\' 12-13 (16-17 בקובץ): טבלת רצועות תזמון שמונה את BXE בין מנועי TDI-PD; משנת דגם 2007 רצועה כל 150,000 ק"מ וגלגלת מתיחה כל 300,000; מסנן סולר (EN 590) כל 90,000, מסנן אוויר כל 90,000 או 6 שנים, מסנן אבק ואבקנים כל 60,000 או שנתיים, שמן DSG 02E כל 60,000'}] + s['sources']
    s['notes'] = ('נבנה מתבנית קובץ ה-1.6 TDI של אוקטביה שבמאגר (אותה פלטפורמה ואותן טבלאות שירות של קבוצת פולקסווגן), בשינוי מרווח רצועת התזמון למנוע 1.9 TDI עם מזרקי יחידה (BXE, וגם BLS ו-2.0 BKD שמופיעים באותה שורה בטבלה) לפי מדריך השירות של גולף 5: החלפה כל 150,000 ק"מ ושל גלגלת המתיחה כל 300,000. '
                  'טיפול כל 15,000 ק"מ או שנה: שמן ומסנן ובדיקת בלמים; כל 30,000: מסנן מזגן ובדיקות מרכב ונוזלים. מסנני אוויר וסולר כל 90,000 ק"מ, נוזל בלמים אחרי 3 שנים ואז כל שנתיים. '
                  'בטבלאות חדשות יותר של היצרן למדינות מאובקות (ישראל ברשימה) רצועות של מנועי דיזל קומון-רייל מוחלפות כבר ב-120,000; למנוע BXE לא נמצאה טבלה כזו. טיוטה.')
    write(s, rules)

def psa_rules():
    J = 'citroen-jumpy-2016-2026-2.0-bluehdi'
    rule_only({'make': 'Citroen', 'names': ['C4 PICASSO', 'C4 GD PICASSO', 'GRAND C4 PICASSO', 'C4 SPACETOURER'], 'years': [2014, 2019], 'engine_codes': ['AH01'], 'fuel': ['דיזל'], 'schedule': J})
    rule_only({'make': 'DS', 'names': ['DS7', 'DS 7', 'DS7 CROSSBACK'], 'years': [2018, 2022], 'engine_codes': ['AH01'], 'fuel': ['דיזל'], 'schedule': J})
    rule_only({'make': 'Peugeot', 'names': ['3008', '5008', '508'], 'years': [2017, 2022], 'engine_codes': ['AH01'], 'fuel': ['דיזל'], 'schedule': J})
    rule_only({'make': 'Citroen', 'names': ['JUMPY HDI', 'JUMPY'], 'years': [2007, 2016], 'engine_codes': ['9HU'], 'fuel': ['דיזל'], 'schedule': 'citroen-berlingo-2008-2019-1.6-hdi'})
    rule_only({'make': 'Citroen', 'names': ['JUMPY'], 'years': [2019, 2022], 'engine_codes': ['YH01'], 'fuel': ['דיזל'], 'schedule': 'citroen-berlingo-2018-2026-1.5-bluehdi'})

def main():
    audi_ea888()  # proace()/city_van() dropped: tail4 and japan-b already cover them
    tdi19('skoda-octavia-2007-2010-1.9-tdi', 'Skoda', 'סקודה', 'Octavia', 'אוקטביה', 'II (1Z)', [2007, 2010],
          [{'make': 'Skoda', 'names': ['OCTAVIA', 'OCTAVIA COMBI', 'OCTAVIA SCOUT'], 'years': [2006, 2010], 'engine_codes': ['BXE', 'BKD'], 'fuel': ['דיזל']}])
    tdi19('vw-jetta-golf-2007-2010-1.9-tdi', 'Volkswagen', 'פולקסווגן', 'Jetta / Golf Plus / Touran', 'ג\'טה / גולף פלוס / טוראן', '5 (1K)', [2007, 2010],
          [{'make': 'Volkswagen', 'names': ['JETTA', 'GOLF PLUS', 'GOLF'], 'years': [2006, 2010], 'engine_codes': ['BXE', 'BKD'], 'fuel': ['דיזל']},
           {'make': 'Volkswagen', 'names': ['TOURAN'], 'years': [2006, 2010], 'engine_codes': ['BXE', 'BLS', 'BKD'], 'fuel': ['דיזל']}])
    rule_only({'make': 'Volkswagen', 'names': ['CADDY', 'CADDY KOMBI', 'CADDY MAXI'], 'years': [2004, 2007], 'engine_codes': ['BJB'], 'fuel': ['דיזל'], 'schedule': 'vw-caddy-2008-2015-1.6-1.9-tdi-1.2-tsi'})
    psa_rules()
