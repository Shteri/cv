# Fiat owner's handbooks (EN): Punto 2012 (aftersales.fiat.com eLum), Qubo (manualslib 1883346), Doblo 2016 (manualslib 2151994).
from gen import *
IMP = 'סמלת'
PUNTO = 'https://aftersales.fiat.com/eLumData/EN/00/199_PUNTO2012/00_199_PUNTO2012_603.47.010_EN_03_07.17_L_EL/00_199_PUNTO2012_603.47.010_EN_03_07.17_L_EL.pdf'
QUBO = 'https://www.manualslib.com/manual/1883346/Fiat-Qubo.html?page=132'
DOBLO = 'https://www.manualslib.com/manual/2151994/Fiat-Doblo-2016.html?page=180'
SAM = {'url': 'https://samelet.com/wp-content/uploads/2023/11/Fiat_500_500C_carbook_042021-1.pdf', 'kind': 'importer',
       'note': 'ספר הרכב העברי של סמלת לפיאט 500 (אותו פורמט תכנית טיפולים של פיאט); לפונטו, קובו ודובלו מדור זה לא נמצא ספר עברי (סבב 3 סרק 219 קבצים באתר סמלת)'}
BELT_NOTE = 'באזור מאובק או בשימוש קשה (עיר, סרק ממושך): לכל היותר 60,000 ק"מ, ולכל המאוחר כל 4 שנים'
ALL = 'all'

def main():
    # ---- Punto petrol 1.2/1.4 8V: plan pp.112-117 (PDF 114-119); 15,000 km / 1 year columns; repeat after 120,000 km / 8 years
    ODD = {1, 3, 5, 7}; EVEN = {2, 4, 6, 8}
    g = [
        (ALL, it('tires', 'inspect', 'מצב ולחץ, וערכת תיקון אם קיימת')),
        (ALL, it('lights', 'inspect', 'כל מערכת התאורה ונוריות הלוח')),
        (ALL, it('coolant', 'inspect', 'בדיקה והשלמת נוזלים')),
        (ALL, it('brake_fluid', 'inspect')),
        (ALL, it('washer_fluid', 'inspect')),
        (ALL, it('exhaust', 'inspect', 'פליטת מזהמים ועשן')),
        (ALL, it('diagnostics', 'inspect', 'מערכות הזנה וניהול מנוע דרך שקע האבחון')),
        (ALL, it('brake_pads', 'inspect', 'רפידות קדמיות ואחוריות ומחוון הבלאי')),
        (ALL, it('brake_drums', 'inspect', 'תופי בלם אחוריים, בגרסאות שיש בהן')),
        (ALL, it('engine_oil', 'replace', 'בטיפולים 15/45/75/105 אלף מומלץ, ב-30/60/90/120 אלף חובה; בנסיעה עירונית או פחות מ-10,000 ק"מ בשנה - כל שנה')),
        (ALL, it('oil_filter', 'replace')),
        (ALL, it('cabin_filter', 'replace', 'בטיפולים האי-זוגיים מומלץ, בזוגיים חובה')),
        (ODD, it('body_underside', 'inspect', 'מרכב והגנת תחתית')),
        (ODD, it('fuel_lines', 'inspect')), (ODD, it('brake_lines', 'inspect')),
        (ODD, it('cv_boots', 'inspect', 'גומיות, שרוולים ותותבים')),
        (ODD, it('wipers', 'inspect', 'מגבים ומתזים; כיוון מתזים לפי הצורך')),
        (EVEN, it('door_hinges', 'clean', 'ניקוי ושימון מנעולי מכסה מנוע ותא מטען')),
        (EVEN, it('parking_brake', 'adjust', 'מהלך ידית בלם החניה')),
        (EVEN, it('spark_plugs', 'replace')),
        (EVEN, it('air_filter', 'replace', 'באזור מאובק כל 15,000 ק"מ')),
        (EVEN, it('transmission_oil', 'inspect', 'מפלס שמן בתיבת Dualogic בלבד')),
        ({4}, it('drive_belt', 'inspect', 'מצב ומתיחה')),
        ({4}, it('timing_belt', 'inspect')),
        ({4, 8}, it('valve_clearance', 'adjust', 'מנועי 1.2 8V ו-1.4 8V')),
    ]
    write({'id': 'fiat-punto-2007-2014-1.2-1.4-8v', 'make': 'Fiat', 'make_he': 'פיאט', 'model': 'Punto / Grande Punto', 'model_he': 'פונטו / גרנדה פונטו',
           'generation': '199 (Grande Punto, Punto Evo, Punto 2012)', 'years': [2007, 2014], 'engines': ['1.2 8V (199A4000/169A4000)', '1.4 8V (350A1000)'], 'fuel': 'petrol', 'importer': IMP,
           'interval': {'km': 15000, 'months': 12, 'note': 'לפי ספר הנהג האנגלי של פונטו 2012: טיפול כל 15,000 ק"מ או שנה; אחרי 120,000 ק"מ או 8 שנים חוזרים להתחלה'},
           'cycle_km': 120000, 'services': build(15000, 8, g),
           'long_interval': [LI('timing_belt', 'replace', every_km=120000, every_months=72, note=BELT_NOTE),
                             LI('drive_belt', 'replace', every_km=120000, every_months=72, note=BELT_NOTE),
                             LI('brake_fluid', 'replace', every_months=24, note='ללא קשר לק"מ')],
           'sources': [{'url': PUNTO, 'kind': 'manufacturer', 'note': 'Fiat Punto (2012) owner handbook EN 603.47.010 ed. 07/2017, "Scheduled servicing plan (petrol versions)", printed pp. 112-117 (PDF pages 114-119), periodic checks and demanding use p. 111. Covers the 1.2 8V and 1.4 8V engines (tappet row)'}, SAM],
           'status': 'draft',
           'notes': 'לפונטו לא נמצא ספר עברי; הלוח לפי ספר הנהג האנגלי של פיאט לפונטו 2012 (אותם מנועי 1.2 ו-1.4 8V כמו בגרנדה פונטו ופונטו אבו). בכל טיפול (15,000 ק"מ או שנה): שמן ומסנן, מסנן מזגן, בדיקות צמיגים, תאורה, נוזלים, בלמים וקריאת מחשב. כל 30,000: מצתים ומסנן אוויר, ניקוי מנעולים ובלם חניה; בטיפולים האי-זוגיים בדיקות מרכב, צנרת וגומיות. ב-60,000: בדיקת רצועות; ב-60,000 וב-120,000 כיוון שסתומים. רצועת תזמון ורצועת אביזרים כל 120,000 ק"מ או 6 שנים, ובאזור מאובק עד 60,000 או 4 שנים. נוזל בלמים כל שנתיים. באזור מאובק מסנני אוויר ומזגן כל 15,000. טיוטה: ספר יצרן לשוק האירופי.'},
          [{'make': 'Fiat', 'names': ['PUNTO 1.4', 'PUNTO1.4', 'PUNTO 1.2', 'GRANDE PUNTO1.2', 'GRANDE PUNTO1.4', 'GRANDE PUNTO', 'PUNTO', 'PUNTO EVO'], 'years': [2006, 2015], 'engine_codes': ['350A1000', '199A4000', '169A4000'], 'fuel': ['בנזין']}])

    # ---- Qubo petrol (Euro 6 handbook) pp.130-133: 30,000 km / 2 years; repeat after 180,000 km / 12 years
    E = {2, 4, 6}
    g = [
        (ALL, it('battery_12v', 'inspect', 'מצב טעינה')),
        (ALL, it('tires', 'inspect', 'מצב ולחץ, וערכת תיקון אם קיימת')),
        (ALL, it('lights', 'inspect')),
        (ALL, it('coolant', 'inspect', 'בדיקה והשלמת נוזלים')), (ALL, it('brake_fluid', 'inspect')), (ALL, it('washer_fluid', 'inspect')),
        (ALL, it('exhaust', 'inspect', 'פליטת מזהמים')),
        (ALL, it('diagnostics', 'inspect', 'מערכות הזנה וניהול מנוע דרך שקע האבחון')),
        (ALL, it('body_underside', 'inspect', 'מרכב והגנת תחתית')), (ALL, it('fuel_lines', 'inspect')), (ALL, it('brake_lines', 'inspect')),
        (ALL, it('cv_boots', 'inspect', 'גומיות, שרוולים ותותבים')),
        (ALL, it('wipers', 'inspect', 'מגבים ומתזים')),
        (ALL, it('door_hinges', 'clean', 'מנעולי מכסה מנוע ומסילות הדלת הזזה')),
        (ALL, it('parking_brake', 'adjust')), (ALL, it('pedals', 'adjust', 'דוושת מצמד')),
        (ALL, it('brake_pads', 'inspect', 'רפידות קדמיות ומחוון הבלאי')),
        (ALL, it('engine_oil', 'replace', 'כל 12 חודשים אם נוסעים פחות מ-10,000 ק"מ בשנה, בעיר או באזור מאובק')), (ALL, it('oil_filter', 'replace')),
        (ALL, it('spark_plugs', 'replace')),
        (ALL, it('air_filter', 'replace', 'באזור מאובק כל 15,000 ק"מ')),
        (ALL, it('cabin_filter', 'replace', 'באזור מאובק כל 15,000 ק"מ')),
        (E, it('brake_drums', 'inspect')), (E, it('drive_belt', 'inspect')),
        ({1, 5}, it('drive_belt', 'adjust', 'רק בגרסאות בלי מותחן אוטומטי (או כל שנתיים)')),
    ]
    write({'id': 'fiat-qubo-2009-2018-1.4', 'make': 'Fiat', 'make_he': 'פיאט', 'model': 'Qubo', 'model_he': 'קובו', 'generation': '225',
           'years': [2009, 2018], 'engines': ['1.4 8V (350A1000)'], 'fuel': 'petrol', 'importer': IMP,
           'interval': {'km': 30000, 'months': 24, 'note': 'לפי ספר הנהג האנגלי של קובו: טיפול כל 30,000 ק"מ או שנתיים; באזור מאובק או בנסיעה מועטה שמן כל שנה ומסננים כל 15,000'},
           'cycle_km': 180000, 'services': build(30000, 6, g),
           'long_interval': [LI('engine_oil', 'replace', every_months=12, note='בנסיעה עירונית, פחות מ-10,000 ק"מ בשנה או באזור מאובק'),
                             LI('timing_belt', 'replace', every_km=120000, every_months=72, note=BELT_NOTE),
                             LI('drive_belt', 'replace', every_km=120000, every_months=72, note=BELT_NOTE),
                             LI('brake_fluid', 'replace', every_months=24, note='ללא קשר לק"מ')],
           'sources': [{'url': QUBO, 'kind': 'manufacturer', 'note': 'Fiat Qubo owner handbook EN (manualslib 1883346, Euro 6 edition): "Service schedule - Euro 6 petrol versions - Natural Power versions", printed pp. 130-133 (site pages 132-135); demanding use p. 137 (site page 139)'}, SAM],
           'status': 'draft',
           'notes': 'לקובו לא נמצא ספר עברי; הלוח לפי ספר הנהג האנגלי של פיאט (מהדורת יורו 6). טיפול כל 30,000 ק"מ או שנתיים: שמן ומסנן, מצתים, מסנני אוויר ומזגן, ובדיקות מצבר, צמיגים, תאורה, נוזלים, בלמים, צנרת, גומיות ומחשב. כל 60,000: בדיקת תופי בלם ורצועת אביזרים. רצועת תזמון ורצועת אביזרים כל 120,000 ק"מ או 6 שנים, ובאזור מאובק עד 60,000 או 4 שנים. נוזל בלמים כל שנתיים. הספר מורה להחליף שמן כל שנה ומסנני אוויר ומזגן כל 15,000 ק"מ באזור מאובק או בנסיעה עירונית - כדאי לבדוק עם המוסך. טיוטה: ספר יצרן לשוק האירופי.'},
          [{'make': 'Fiat', 'names': ['QUBO'], 'years': [2009, 2018], 'engine_codes': ['350A1000'], 'fuel': ['בנזין']}])

    # ---- Qubo diesel 1.3 Multijet (Euro 6 handbook) pp.134-136: 35,000 km / 2 years
    g = [
        (ALL, it('battery_12v', 'inspect', 'מצב טעינה')), (ALL, it('tires', 'inspect')), (ALL, it('lights', 'inspect')),
        (ALL, it('coolant', 'inspect', 'בדיקה והשלמת נוזלים')), (ALL, it('brake_fluid', 'inspect')), (ALL, it('washer_fluid', 'inspect')),
        (ALL, it('exhaust', 'inspect', 'פליטת מזהמים')), (ALL, it('diagnostics', 'inspect', 'שקע האבחון; גם מצב השמן')),
        (ALL, it('body_underside', 'inspect')), (ALL, it('fuel_lines', 'inspect')), (ALL, it('brake_lines', 'inspect')), (ALL, it('cv_boots', 'inspect')),
        (ALL, it('wipers', 'inspect', 'מגבים ומתזים')), (ALL, it('door_hinges', 'clean', 'מנעולי מכסה מנוע ומסילות הדלת הזזה')),
        (ALL, it('parking_brake', 'adjust')), (ALL, it('brake_pads', 'inspect')),
        (ALL, it('engine_oil', 'replace', 'לפי הודעת המחוון ולכל המאוחר כל 24 חודשים; בנסיעה עירונית כל 12 חודשים')), (ALL, it('oil_filter', 'replace')),
        (ALL, it('air_filter', 'replace')), (ALL, it('cabin_filter', 'replace')),
        ({2, 4}, it('brake_drums', 'inspect')), ({2, 4}, it('fuel_filter', 'replace', 'בדלק באיכות נמוכה מהתקן: כל 35,000')),
        ({2, 5}, it('drive_belt', 'inspect')), ({3}, it('manual_gearbox_oil', 'inspect')),
        (ALL, it('transmission_oil', 'inspect', 'רק בגרסת 80 כ"ס עם תיבת Dualogic')),
    ]
    write({'id': 'fiat-qubo-2013-2018-1.3-multijet', 'make': 'Fiat', 'make_he': 'פיאט', 'model': 'Qubo', 'model_he': 'קובו', 'generation': '225',
           'years': [2013, 2018], 'engines': ['1.3 Multijet (199A9000/225A2000)'], 'fuel': 'diesel', 'importer': IMP,
           'interval': {'km': 35000, 'months': 24, 'note': 'לפי ספר הנהג האנגלי של קובו (דיזל יורו 6): טיפול כל 35,000 ק"מ או שנתיים; שמן לפי מחוון'},
           'cycle_km': 175000, 'services': build(35000, 5, g),
           'long_interval': [LI('engine_oil', 'replace', every_months=12, note='בנסיעה עירונית בעיקר'),
                             LI('drive_belt', 'replace', every_km=120000, every_months=72, note=BELT_NOTE),
                             LI('brake_fluid', 'replace', every_months=24, note='ללא קשר לק"מ')],
           'sources': [{'url': 'https://www.manualslib.com/manual/1883346/Fiat-Qubo.html?page=136', 'kind': 'manufacturer', 'note': 'Fiat Qubo owner handbook EN (manualslib 1883346): "Diesel Euro 6 versions", printed pp. 134-136 (site pages 136-138), repeat after 175,000 km / 10 years'}, SAM],
           'status': 'draft',
           'notes': 'הלוח לפי ספר הנהג האנגלי של קובו לגרסאות דיזל יורו 6 (מנוע 1.3 מולטיג\'ט, עם שרשרת תזמון ולכן אין שורת רצועת תזמון). טיפול כל 35,000 ק"מ או שנתיים: מסנני אוויר ומזגן ובדיקות; השמן מוחלף לפי המחוון ולכל המאוחר כל שנתיים (בעיר כל שנה). כל 70,000: מסנן סולר ותופי בלם; ב-105,000 בדיקת שמן תיבה ידנית. רצועת אביזרים כל 120,000 ק"מ או 6 שנים (באזור מאובק עד 60,000 או 4 שנים). נוזל בלמים כל שנתיים. גרסאות יורו 5 (199A9000) קודמות למהדורה זו. טיוטה.'},
          [{'make': 'Fiat', 'names': ['QUBO'], 'years': [2012, 2018], 'engine_codes': ['199A9000', '225A2000'], 'fuel': ['דיזל']}])

    # ---- Doblo diesel with DPF (1.3/1.6/2.0 Multijet), Doblo 2016 handbook pp.176-177: 35,000 km / 24 months
    g = [
        (ALL, it('tires', 'inspect')), (ALL, it('lights', 'inspect')), (ALL, it('wipers', 'inspect', 'מגבים ומתזים')),
        (ALL, it('brake_pads', 'inspect', 'רפידות קדמיות ומחוון הבלאי')),
        (ALL, it('body_underside', 'inspect')), (ALL, it('fuel_lines', 'inspect')), (ALL, it('brake_lines', 'inspect')), (ALL, it('cv_boots', 'inspect')),
        (ALL, it('door_hinges', 'clean', 'מנעולי מכסה מנוע ותא מטען, מסילות הדלת הזזה')),
        (ALL, it('coolant', 'inspect', 'בדיקה והשלמת נוזלים')), (ALL, it('brake_fluid', 'inspect')), (ALL, it('washer_fluid', 'inspect')), (ALL, it('battery_12v', 'inspect')),
        (ALL, it('parking_brake', 'adjust')), (ALL, it('exhaust', 'inspect', 'פליטה ועשן')), (ALL, it('diagnostics', 'inspect')),
        (ALL, it('engine_oil', 'replace', 'לפי הודעת המחוון ולכל המאוחר כל 24 חודשים; בנסיעה עירונית כל 12 חודשים')), (ALL, it('oil_filter', 'replace')),
        (ALL, it('air_filter', 'replace')), (ALL, it('cabin_filter', 'replace', 'או כל 24 חודשים')),
        ({2, 4}, it('brake_drums', 'inspect')), ({2, 4}, it('fuel_filter', 'replace', 'בדלק באיכות נמוכה מהתקן: כל 35,000')),
        ({2, 4}, it('brake_fluid', 'replace', 'או כל 24 חודשים')),
        ({1, 4}, it('drive_belt', 'adjust', 'מתיחה, רק בלי מותחן אוטומטי')), ({2, 5}, it('drive_belt', 'inspect')),
        ({3}, it('drive_belt', 'replace')), ({4}, it('timing_belt', 'replace', 'רק במנועי 1.6 ו-2.0 מולטיג\'ט')),
    ]
    write({'id': 'fiat-doblo-2010-2022-1.3-1.6-multijet', 'make': 'Fiat', 'make_he': 'פיאט', 'model': 'Doblo', 'model_he': 'דובלו', 'generation': '263',
           'years': [2010, 2022], 'engines': ['1.3 Multijet', '1.6 Multijet', '2.0 Multijet'], 'fuel': 'diesel', 'importer': IMP,
           'interval': {'km': 35000, 'months': 24, 'note': 'לפי ספר הנהג האנגלי של דובלו 2016 (דיזל עם מסנן חלקיקים): טיפול כל 35,000 ק"מ או 24 חודשים; שמן לפי מחוון'},
           'cycle_km': 175000, 'services': build(35000, 5, g),
           'long_interval': [LI('engine_oil', 'replace', every_months=12, note='בנסיעה עירונית בעיקר'),
                             LI('timing_belt', 'replace', every_km=140000, every_months=60, note='רק 1.6/2.0 מולטיג\'ט; בשימוש קשה (עיר, סרק, קור) כל 4 שנים'),
                             LI('brake_fluid', 'replace', every_months=24), LI('cabin_filter', 'replace', every_months=24)],
           'sources': [{'url': DOBLO, 'kind': 'manufacturer', 'note': 'Fiat Doblo 2016 owner handbook EN (manualslib 2151994): "Diesel versions with DPF (1.3 MultiJet - 1.6 MultiJet - 2.0 MultiJet)", printed pp. 176-177 (site pages 180-181); without-DPF table pp. 174-175'}, SAM],
           'status': 'draft',
           'notes': 'לדובלו מדור 263 לא נמצא ספר עברי; הלוח לפי ספר הנהג האנגלי של פיאט (2016) לגרסאות דיזל עם מסנן חלקיקים. טיפול כל 35,000 ק"מ או שנתיים: מסנני אוויר ומזגן ובדיקות; שמן לפי המחוון ולכל המאוחר כל שנתיים (בעיר כל שנה). כל 70,000: מסנן סולר, נוזל בלמים ותופי בלם. רצועת אביזרים ב-105,000. רצועת תזמון במנועי 1.6 ו-2.0 ב-140,000 או 5 שנים (בשימוש קשה 4 שנים); במנוע 1.3 אין רצועה. קודי המנוע ברישוי לא אומתו מול מסמך פיאט, והשיוך לפי שם הדגם ושנות הייצור. טיוטה.'},
          [{'make': 'Fiat', 'names': ['DOBLO', 'FIAT DOBLO', 'DOBLO1.3', 'DOBLO 1.3 COMBI', 'DOBLO 1.6 COMBY', 'DOBLO 1.6 VAN'], 'years': [2010, 2022],
            'engine_codes': ['263A2000', '198A3000', '263A5000', '263A8000', '330A1000', '55280444', '55283775', '199A9000'], 'fuel': ['דיזל']}])
