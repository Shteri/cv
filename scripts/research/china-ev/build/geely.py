from sched import *
IMP = 'גיאו מוביליטי (קבוצת יוניון)'
def ev_common(s, extra_door_handles=False):
    s.all('hybrid_system', 'inspect', 'סוללת מתח גבוה: בדיקה חזותית של המארז, בדיקת בידוד ובדיקה במחשב אבחון')
    s.all('diagnostics', 'inspect', 'מערכת ההנעה החשמלית, המטען המובנה וכל הרכב - סריקה במחשב אבחון')
    s.all('electrical_system', 'inspect', 'בדיקה חזותית של מערכת ההנעה והמטען המובנה; חלונות וצופר')
    s.all('parking_brake', 'inspect', 'תפקוד מערכת הבלמים ובלם החניה')
    s.all('brake_pads'); s.all('brake_discs')
    s.every('brake_fluid', 'replace', 40000, 'החלפה כל 40,000 ק"מ (24 חודשים); בשאר הטיפולים בדיקת מפלס', other='inspect')
    s.all('coolant', 'inspect'); s.all('cooling_system', 'inspect')
    s.all('ac_system', 'inspect'); s.all('cabin_filter', 'replace')
    s.all('battery_12v'); s.all('lights'); s.all('wipers')
    s.all('door_hinges', 'inspect', 'שימון צירים ומנעולי דלתות' + (' וידיות הדלת החשמליות' if extra_door_handles else ''))
    s.all('cv_boots', 'inspect', 'צירי הנעה'); s.all('steering', 'inspect', 'תיבת הגה ומוטות קצה')
    s.all('body_underside', 'adjust', 'הידוק ברגים ואומים במרכב'); s.all('suspension', 'inspect', 'בולמי זעזועים'); s.all('tires')
    s.add(140000, 'hybrid_system', 'inspect', 'בדיקת אטימות אוויר של מארז הסוללה (בתשלום נוסף)')

G = 'https://geely.co.il/wp-content/uploads/'
# Geometry C GE13-J2
s = Sched(id='geely-geometry-c-2021-2025-ev', make='Geely', make_he="ג'ילי", model='Geometry C', model_he="ג'יאומטרי C", generation='GE13-J2',
    years=[2021, 2025], engines=['EV (TZ18), 53/70 kWh'], fuel='electric', importer=IMP,
    interval={'km': 20000, 'months': 12, 'note': 'לפי לוח האחזקה של היבואן: טיפול כל 20,000 ק"מ או 12 חודשים, המוקדם מביניהם'},
    cycle_km=200000, status='reviewed',
    notes='הועתק מלוח האחזקה העברי של גיאו מוביליטי לגיאומטרי C (GE13-J2, יוני 2023) ומתוכנית התחזוקה שבחוברת האחריות. אין שמן מנוע; מסנן המזגן מוחלף בכל טיפול. שמן תיבת ההפחתה ונוזל הקירור מופיעים ב-long_interval לפי הערות הלוח. L (שימון) נרשם כבדיקה.')
ev_common(s)
s.li('transmission_oil', 'replace', 'שמן תיבת הפחתה (MOTF-TS-1): החלפה ראשונה ב-20,000 ק"מ ואחר כך כל 60,000 ק"מ', first_km=20000, then_every_km=60000)
s.li('coolant', 'replace', 'נוזל קירור: כל 60,000 ק"מ או 48 חודשים, המוקדם', every_km=60000, every_months=48)
s.spec(brake_fluid='DOT4', coolant='נוזל קירור על בסיס אתילן גליקול שאושר ע"י Geely', _note='מתוך חוברת האחריות GE13-J2 (עמ\' 13); גז מזגן R1234yf; שמן תיבת הפחתה MOTF-TS-1', warranty='סוללה: 8 שנים או 150,000 ק"מ (לפי דף המפרט 2025)')
s.src(G + '2026/03/06.23-GE13-J2-לוח-אחזקה-עברית.pdf', 'importer', 'לוח אחזקה GE13-J2 בעברית (עמוד 1, 10 עמודות של 20,000 ק"מ)')
s.src(G + '2025/01/Warrenty-GEELY-GE13-J2-19_06_2023-3.pdf', 'importer', 'חוברת אחריות ושירות GE13-J2, עמ\' 10-13: תוכנית תחזוקה ונוזלים')
s.write(); s.rule('Geely', ['GEOMETRY C'], [2021, 2025])

# Geometry C GE13-A1 (updated plan)
s = Sched(id='geely-geometry-c-2026-ev', make='Geely', make_he="ג'ילי", model='Geometry C', model_he="ג'יאומטרי C", generation='GE13-A1 (NEW GEOMETRY C)',
    years=[2026, 2026], engines=['EV (TZ18)'], fuel='electric', importer=IMP,
    interval={'km': 20000, 'months': 12, 'note': 'לפי לוח האחזקה המעודכן של היבואן: כל 20,000 ק"מ או 12 חודשים'},
    cycle_km=200000, status='reviewed',
    notes='לפי לוח האחזקה העברי המעודכן 2GE13-A1 של גיאו מוביליטי. ההבדל מ-GE13-J2: שמן תיבת ההפחתה כל 80,000 ק"מ ונוזל קירור כל 60,000 ק"מ או 36 חודשים, ושימון ידיות דלת חשמליות. שיוך השנים (2026 ואילך, "NEW GEOMETRY C") הוא הנחה - הלוח עצמו אינו מציין שנות ייצור.')
ev_common(s, True)
s.li('transmission_oil', 'replace', 'שמן תיבת הפחתה: כל 80,000 ק"מ', every_km=80000)
s.li('coolant', 'replace', 'נוזל קירור: כל 60,000 ק"מ או 36 חודשים, המוקדם', every_km=60000, every_months=36)
s.spec(brake_fluid='DOT4', _note='נוזלים לפי חוברת האחריות של GE13; הלוח המעודכן לא מפרט סוגי נוזלים')
s.src(G + '2026/03/עדכון-2GE13-A1-לוח-אחזקה-עברית-לוח-אחזקה-נקי-ללא-תוספות-.pdf', 'importer', 'לוח אחזקה מעודכן 2GE13-A1 (עמוד 1, 10 עמודות של 20,000 ק"מ)')
s.write(); s.rule('Geely', ['GEOMETRY C', 'NEW GEOMETRY C'], [2026, 2026])

# EX5 E245
s = Sched(id='geely-ex5-2025-2026-ev', make='Geely', make_he="ג'ילי", model='EX5', model_he='EX5', generation='E245',
    years=[2025, 2026], engines=['EV (TZ18 / TZ184XY101)'], fuel='electric', importer=IMP,
    interval={'km': 20000, 'months': 12, 'note': 'לפי לוח האחזקה של היבואן: כל 20,000 ק"מ או 12 חודשים'},
    cycle_km=200000, status='reviewed',
    notes='הועתק מלוח האחזקה העברי של גיאו מוביליטי ל-EX5 (E245, "עבור מרכזי השירות"). נוזל קירור ושמן תיבת הפחתה מוחלפים כל 80,000 ק"מ או 48 חודשים (ב-long_interval); בשאר הטיפולים בדיקת נוזל קירור.')
ev_common(s, True)
s.li('transmission_oil', 'replace', 'שמן תיבת הפחתה: כל 80,000 ק"מ או 48 חודשים', every_km=80000, every_months=48)
s.li('coolant', 'replace', 'נוזל קירור: כל 80,000 ק"מ או 48 חודשים', every_km=80000, every_months=48)
s.src(G + '2026/03/עבור-מרכזי-השירות-E245-לוח-אחזקה-עברית.pdf', 'importer', 'לוח אחזקה E245 (EX5) בעברית, עמוד 1')
s.src(G + '2025/12/חוברת-אחריות-פרטי-EX5-E245-J1-17092025.pdf', 'importer', 'חוברת אחריות פרטי EX5 E245-J1 (לא נבדקה לעומק)')
s.write(); s.rule('Geely', ['EX5'], [2025, 2026])

# StarRay EM-i P145
s = Sched(id='geely-starray-em-i-2025-2026-1.5-phev', make='Geely', make_he="ג'ילי", model='Starray EM-i', model_he='סטארריי EM-i', generation='P145',
    years=[2025, 2026], engines=['1.5 PHEV (BHE15-DFN)'], fuel='plug-in-hybrid', importer=IMP,
    interval={'km': 15000, 'months': 12, 'note': 'לפי חוברת האחריות והלוח של היבואן: כל 15,000 ק"מ או 12 חודשים; בתנאים קשים שמן ומסנן כל 10,000 ק"מ'},
    cycle_km=150000, status='reviewed',
    notes='הועתק מלוח האחזקה העברי STAR RAY P145 ומתוכנית התחזוקה בחוברת האחריות (עמ\' 11-13). מסנן המזגן נבדק ומנוקה בכל טיפול ומוחלף לפי הצורך. למנוע יש מד איכות שמן - מחליפים גם כשהאיכות יורדת מתחת ל-10%.')
s.all('engine_oil', 'replace'); s.all('oil_filter', 'replace')
s.row('air_filter', 'IRIRIRIRIR'); s.all('cooling_system')
s.all('coolant', 'inspect')
s.all('fuel_lines', 'inspect', 'מיכל, צנרת וחיבורים')
s.all('evap_system', 'inspect', 'מסנן פחם פעיל (קניסטר) - החלפה לפי long_interval')
s.row('spark_plugs', 'IRIRIRIRIR', 'החלפה כל 30,000 ק"מ')
s.all('hybrid_system', 'inspect', 'סוללת מתח גבוה: בדיקה חזותית, בדיקת בידוד ובדיקה במחשב')
s.all('diagnostics', 'inspect', 'מנוע, יחידת ההנעה החשמלית, המטען וכל הרכב - סריקה במחשב אבחון')
s.all('electrical_system', 'inspect', 'יחידת ההנעה והמטען: בדיקה חזותית; חלונות וצופר')
s.all('parking_brake', 'inspect', 'תפקוד בלמים ובלם חניה'); s.all('brake_pads'); s.all('brake_discs')
s.row('brake_fluid', 'IRIRIRIRIR', 'החלפה כל 30,000 ק"מ (24 חודשים)')
s.all('ac_system'); s.all('cabin_filter', 'inspect', 'ניקוי בכל טיפול והחלפה לפי הצורך')
s.all('battery_12v'); s.all('lights'); s.all('wipers')
s.all('door_hinges', 'inspect', 'שימון צירים, מנעולים וידיות דלת חשמליות')
s.all('cv_boots', 'inspect', 'גלי הינע'); s.all('steering'); s.all('body_underside', 'adjust', 'הידוק ברגי מרכב')
s.all('suspension', 'inspect', 'בולמי זעזועים'); s.all('exhaust'); s.all('tires')
s.add(150000, 'hybrid_system', 'inspect', 'בדיקת אטימות אוויר של מארז הסוללה')
s.li('coolant', 'replace', 'נוזל קירור מנוע: כל 90,000 ק"מ או 48 חודשים', every_km=90000, every_months=48)
s.li('transmission_oil', 'replace', 'שמן תיבת הפחתה (Shell E-Fluids E6 iDHTF): כל 90,000 ק"מ או 48 חודשים', every_km=90000, every_months=48)
s.li('evap_system', 'replace', 'מסנן פחם פעיל: כל 60,000 ק"מ או 36 חודשים', every_km=60000, every_months=36)
s.spec(engine_oil='API SP 0W-20', brake_fluid='DOT4', coolant='נוזל קירור על בסיס גליקול שאושר ע"י Geely', _note='מתוך חוברת האחריות StarRay EM-i (עמ\' 13)')
s.src(G + '2026/03/STAR-RAY-P145-לוח-אחזקה-עברית.pdf', 'importer', 'לוח אחזקה P145 בעברית (2 עמודים, 10 עמודות של 15,000 ק"מ)')
s.src(G + '2025/12/STARRAYEM-i_Warranty-Booklet-HEB.pdf', 'importer', 'חוברת אחריות StarRay EM-i, עמ\' 2 ו-11-13')
s.write(); s.rule('Geely', ['STARRAY EM-I', 'STARRAY'], [2025, 2026])
save_rules('geely')
