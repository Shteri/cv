# Renault Malaysia (TC Euro Cars / Tan Chong, official Renault distributor) "Renault Regular Maintenance Schedule" PDFs,
# linked from https://www.renault.com.my/ownership . 12 columns: 6 months / 10,000 km ... 72 months / 120,000 km.
from gen import *
MY = 'https://www.renault.com.my/storage/images/'
IMP = 'פריסבי (קרסו)'
BLOCK = {'url': 'https://www.renault.co.il/', 'kind': 'importer', 'note': 'אתרי renault.co.il ו-dacia.co.il עדיין חסומים מסביבת הענן (403); לוח היבואן לא נמצא'}
def cols(*c): return set(c)
ALL = 'all'
EVERY2 = {2, 4, 6, 8, 10, 12}; EVERY3 = {3, 6, 9, 12}; EVERY4 = {4, 8, 12}; EVERY6 = {6, 12}
MY_INT = {'km': 10000, 'months': 6, 'note': 'לפי לוח רנו מלזיה: טיפול כל 10,000 ק"מ או 6 חודשים (שוק טרופי); מרווח היבואן בישראל לא נמצא'}

def main():
    # Fluence 2.0 (M4R) - page "Renault FLUENCE"
    g = [
        (ALL, it('engine_oil', 'replace', 'שמן סינתטי מלא, 4 ליטר; כולל אטם בורג הניקוז')),
        (ALL, it('oil_filter', 'replace')),
        (ALL, it('diagnostics', 'inspect', 'קריאת מחשב (CLIP) ובדיקה כללית של 25 נקודות')),
        (EVERY2, it('air_filter', 'replace')),
        (EVERY2, it('cabin_filter', 'replace')),
        (EVERY6, it('coolant', 'replace', '5 ליטר')),
        (EVERY6, it('drive_belt', 'replace', 'רצועת אלטרנטור')),
        (EVERY4, it('brake_fluid', 'replace')),
        (EVERY4, it('brake_pads', 'inspect', 'שירות בלמים קדמיים ואחוריים')),
        ({12}, it('spark_plugs', 'replace')),
    ]
    write({'id': 'renault-fluence-2010-2016-2.0', 'make': 'Renault', 'make_he': 'רנו', 'model': 'Fluence / Megane / Scenic', 'model_he': 'פלואנס / מגאן / סניק',
           'generation': 'L30 (פלואנס), מגאן III, סניק III', 'years': [2010, 2016], 'engines': ['2.0 16V (M4R)'], 'fuel': 'petrol', 'importer': IMP,
           'interval': MY_INT, 'cycle_km': 120000, 'services': build(10000, 12, g), 'long_interval': [],
           'specs': {'engine_oil': 'שמן סינתטי מלא', 'oil_capacity': '4 ליטר (לפי לוח רנו מלזיה)', 'timing': 'שרשרת תזמון (מנוע M4R); אין החלפה בלוח'},
           'sources': [{'url': MY + 'Renault_Malaysia_Fluence___ClioGTLine_Periodic_Maintenance_Service-1603198170.pdf', 'kind': 'manufacturer', 'note': 'Renault Malaysia (TC Euro Cars), "Renault Regular Maintenance Schedule", page 1 "Renault FLUENCE" (the Malaysian Fluence is the 2.0 M4R with CVT): 12 columns, 10,000 km / 6 months each, to 120,000 km. Linked from https://www.renault.com.my/ownership'},
                       {'url': 'https://paultan.org/2014/10/28/renault-fluence-20-review', 'kind': 'other', 'note': 'סקירה מלזית: הפלואנס המקומי הוא 2.0 ליטר M4R עם תיבת CVT ושרשרת תזמון'}, BLOCK],
           'status': 'draft',
           'notes': 'לוח היבואן בישראל לא נמצא. הלוח לקוח מרנו מלזיה לפלואנס 2.0 (מנוע M4R, אותו מנוע שבפלואנס, מגאן וסניק 2.0 בישראל), שוק חם עם מרווח קצר: טיפול כל 10,000 ק"מ או חצי שנה עם שמן, מסנן שמן וקריאת מחשב. כל 20,000 ק"מ: מסנני אוויר ומזגן. כל 40,000 ק"מ: נוזל בלמים ושירות בלמים. כל 60,000 ק"מ: נוזל קירור ורצועת אלטרנטור. מצתים ב-120,000 ק"מ. אין בלוח שורה לשמן תיבת ה-CVT. טיוטה: לוח של שוק אחר; מגאן וסניק משויכים לפי אותו מנוע.'},
          [{'make': 'Renault', 'names': ['FLUENCE'], 'years': [2009, 2016], 'engine_codes': ['M4R', 'M4RK7'], 'fuel': ['בנזין']},
           {'make': 'Renault', 'names': ['SCENIC', 'GRAND SCENIC', 'GEREND SCENIC', 'MEGANE'], 'years': [2009, 2016], 'engine_codes': ['M4R', 'M4RK7'], 'fuel': ['בנזין']}])
    # Koleos 2.5 (first generation) - page "Renault KOLEOS 2.5 (4x2 and 4x4)"
    g = [
        (ALL, it('engine_oil', 'replace', 'שמן סינתטי מלא, 6 ליטר; כולל אטם בורג הניקוז')),
        (ALL, it('oil_filter', 'replace')),
        (ALL, it('brake_pads', 'inspect', 'שירות בלמים קדמיים ואחוריים; בדיקה כללית של 25 נקודות')),
        (ALL, it('wheel_alignment', 'adjust', 'כיוון ארבעה גלגלים ואיזון')),
        (ALL, it('tire_rotation', 'rotate')),
        (EVERY2, it('air_filter', 'replace')),
        (EVERY3, it('cabin_filter', 'replace')),
        (EVERY3, it('brake_fluid', 'replace')),
        (EVERY6, it('coolant', 'replace', '5 ליטר')),
        (EVERY6, it('drive_belt', 'replace', 'רצועת אלטרנטור')),
        ({8}, it('spark_plugs', 'replace')),
    ]
    write({'id': 'renault-koleos-2009-2011-2.5', 'make': 'Renault', 'make_he': 'רנו', 'model': 'Koleos', 'model_he': 'קולאוס',
           'generation': 'HY (דור ראשון)', 'years': [2009, 2011], 'engines': ['2.5 (2TR)'], 'fuel': 'petrol', 'importer': IMP,
           'interval': MY_INT, 'cycle_km': 120000, 'services': build(10000, 12, g),
           'long_interval': [],
           'specs': {'engine_oil': 'שמן סינתטי מלא', 'oil_capacity': '6 ליטר (לפי לוח רנו מלזיה)'},
           'sources': [{'url': MY + 'Renault_Malaysia_Captur___Koleos_Periodic_Maintenance_Service-1603198170.pdf', 'kind': 'manufacturer', 'note': 'Renault Malaysia (TC Euro Cars), "Renault Regular Maintenance Schedule", page 3 "Renault KOLEOS 2.5 (4x2 and 4x4)" (first-generation Koleos; page 2 is the later KOLEOS II HZG): 12 columns, 10,000 km / 6 months each, to 120,000 km'}, BLOCK],
           'status': 'draft',
           'notes': 'לוח היבואן בישראל לא נמצא. הלוח לקוח מרנו מלזיה לקולאוס 2.5 מהדור הראשון, שוק חם עם מרווח קצר: טיפול כל 10,000 ק"מ או חצי שנה עם שמן ומסנן, שירות בלמים, כיוון ואיזון גלגלים וסבב צמיגים. מסנן אוויר כל 20,000 ק"מ; מסנן מזגן ונוזל בלמים כל 30,000; נוזל קירור ורצועת אלטרנטור כל 60,000; מצתים ב-80,000. טיוטה: לוח של שוק אחר.'},
          [{'make': 'Renault', 'names': ['KOLEOS'], 'years': [2008, 2012], 'engine_codes': ['2TR', '2TRA7'], 'fuel': ['בנזין']}])
    # ZOE (electric)
    g = [
        (ALL, it('diagnostics', 'inspect', 'קריאת מחשב (CLIP) ובדיקה כללית של 25 נקודות')),
        (ALL, it('brake_pads', 'inspect', 'שירות בלמים קדמיים ואחוריים')),
        (EVERY2, it('cabin_filter', 'replace')),
        (EVERY2, it('brake_fluid', 'replace', 'בלוח: "Brake Fluid (1.0L)" עם כמות, כלומר מילוי חדש')),
        (EVERY4, it('battery_12v', 'inspect', 'בלוח מופיעה שורת מצבר 12 וולט ללא פועל; כאן כבדיקה')),
        (EVERY6, it('coolant', 'inspect', 'בלוח מופיעה שורת נוזל קירור ללא פועל; כאן כבדיקה')),
    ]
    write({'id': 'renault-zoe-2017-2021-ev', 'make': 'Renault', 'make_he': 'רנו', 'model': 'Zoe', 'model_he': 'זואי',
           'generation': 'X10', 'years': [2017, 2021], 'engines': ['electric (5AQ)'], 'fuel': 'electric', 'importer': IMP,
           'interval': MY_INT, 'cycle_km': 120000, 'services': build(10000, 12, g), 'long_interval': [],
           'sources': [{'url': MY + 'Renault_Malaysia_Zoe___Twizy_Periodic_Maintenance_Service-1603198170.pdf', 'kind': 'manufacturer', 'note': 'Renault Malaysia (TC Euro Cars), "Renault Regular Maintenance Schedule", page 1 "Renault ZOE": 12 columns, 10,000 km / 6 months each, to 120,000 km'}, BLOCK],
           'status': 'draft',
           'notes': 'לוח היבואן בישראל לא נמצא. הלוח לקוח מרנו מלזיה לזואי: ביקורת כל 10,000 ק"מ או חצי שנה עם קריאת מחשב ושירות בלמים. מסנן מזגן ונוזל בלמים כל 20,000 ק"מ; בדיקת מצבר 12 וולט כל 40,000; בדיקת נוזל קירור כל 60,000. בשורות המצבר ונוזל הקירור הלוח אינו אומר אם להחליף, ולכן הן מוצגות כבדיקה. טיוטה: לוח של שוק אחר.'},
          [{'make': 'Renault', 'names': ['ZOE'], 'years': [2013, 2022], 'fuel': ['חשמל']}])
    # registry-only: same engine as existing files
    rule_only({'make': 'Renault', 'names': ['MEGANE'], 'years': [2013, 2015], 'engine_codes': ['H5F'], 'fuel': ['בנזין'], 'schedule': 'renault-megane-2016-2019-1.2-tce'})
    rule_only({'make': 'Renault', 'names': ['KANGOO 2', 'KANGOO'], 'years': [2008, 2012], 'engine_codes': ['K9KB8'], 'fuel': ['דיזל'], 'schedule': 'renault-kangoo-2008-2021-1.5-dci'})
