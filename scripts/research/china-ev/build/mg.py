from sched import *
IMP = 'קאר איסט (קבוצת לובינסקי)'
EU = 'https://cdn.mgmotor.eu/'
NOTE_IL = ('ספרי הנהג של היבואן מוצגים באתר mg-israel.co.il/guide-books דרך lubinski.clearmash.com, אבל השרת חוסם את הסביבה הזו (Cloudflare 403), ולכן זו טיוטה לפי מסמך השירות האירופי של MG '
           '(ק"מ, אירופה). כדאי לאמת מול ספר השירות הישראלי.')
IL_SRC = ('https://mg-israel.co.il/guide-books/', 'importer', 'עמוד ספרי הרכב של MG ישראל (ספר נהג לפי דגם ושנה); הקבצים ב-clearmash חסומים מכאן - לא נפתחו')
def ev_common(s):
    for it, n in [('parking_brake', None), ('lights', 'פנסים, צופר ונוריות אזהרה'), ('wipers', 'מגבים ומתזים'), ('seat_belts', None), ('ac_system', None),
                  ('door_hinges', 'מנעולים, צירים ומעצורי דלת - ניקוי ושימון לפי הצורך'), ('battery_12v', None), ('washer_fluid', None),
                  ('brake_fluid', 'מפלס'), ('transmission_oil', 'מפלס שמן תיבת ההינע החשמלית'), ('coolant', 'מפלס וריכוז'), ('cooling_system', 'צנרת, מצנן, מאוורר וחבקי צינורות'),
                  ('hybrid_system', 'סוללת מתח גבוה: ברגי עיגון, מארז, שסתום אוורור, כבל הארקה, מחברים ורתמות מתח גבוה/נמוך; מצב איזון התאים'),
                  ('brake_pads', None), ('brake_discs', None), ('brake_lines', None), ('suspension', 'מסבי גלגלים, מתלים'), ('steering', None), ('cv_boots', 'שרוולי גל הינע'),
                  ('tires', 'עומק חריץ, לחץ, בדיקת זוויות ורוטציה לפי הצורך'), ('body_underside', 'ברגי שלדה ותחתית'), ('diagnostics', 'קריאת תקלות, איפוס מד טיפולים ועדכון תוכנה')]:
        s.all(it, 'inspect', n)
def ev(id, model, model_he, gen, years, engines, doc, doc_note, trans_km, cabin='B', extra=None, notes_extra=''):
    s = Sched(id=id, make='MG', make_he="אם.ג'י", model=model, model_he=model_he, generation=gen, years=years, engines=engines, fuel='electric', importer=IMP,
        interval={'km': 24000, 'months': 12, 'note': 'לפי מסמך השירות האירופי של MG: טיפול A כל 24,000 ק"מ או 12 חודשים, וטיפול B (מורחב) כל 48,000 ק"מ או 24 חודשים'},
        cycle_km=96000, status='draft', notes=NOTE_IL + ' טיפולי A ו-B מתחלפים; שמן תיבת ההינע, נוזל בלמים ונוזל קירור ב-long_interval.' + notes_extra)
    ev_common(s)
    if cabin == 'B': s.every('cabin_filter', 'replace', 48000, 'החלפה בטיפול B (כל 48,000 ק"מ או 24 חודשים)')
    s.li('transmission_oil', 'replace', f'שמן תיבת ההינע החשמלית: כל {trans_km:,} ק"מ', every_km=trans_km)
    s.li('brake_fluid', 'replace', 'נוזל בלמים: כל שנתיים (בנהיגה הררית/לחה: כל 40,000 ק"מ או שנה)', every_months=24)
    s.li('coolant', 'replace', 'נוזל קירור: כל 4 שנים או 96,000 ק"מ', every_km=96000, every_months=48)
    if extra: extra(s)
    s.src(EU + doc, 'manufacturer', doc_note)
    s.src(*IL_SRC)
    s.write(); return s

s = ev('mg-zs-ev-2020-2024-ev', 'ZS EV', 'ZS EV', 'ZS EV / ZS EV MCE', [2020, 2024], ['EV (TZ204XS1152 / TZ204XS1481)'],
       'images/hero-image/2.3.-ZS-EV_Service-Manual-vehicles-registered-from-2021.pdf', 'MG ZS EV Service Manual (אירופה, רכבים מ-2021), עמ\' 4-9; המסמך לרכבים לפני 2021 זהה במרווחים',
       80000, cabin=None, notes_extra=' מסנן המזגן: לפי הפריטים המיוחדים - כל שנתיים או 48,000 ק"מ.')
s.every('cabin_filter', 'replace', 48000, 'כל שנתיים או 48,000 ק"מ'); s.write()
s.rule('MG', ['ZS EV'], [2020, 2024])
s = ev('mg-4-2023-2026-ev', 'MG4', 'MG4', 'MG4 Electric', [2023, 2026], ['EV (TZ180XS0951 / TZ204XS1351)'],
       'manuals/MG4_Service_Portfolio_EN.pdf', 'MG4 Service Portfolio (אירופה), עמ\' 4-10', 96000)
s.rule('MG', ['MG4'], [2023, 2026])
s = ev('mg-marvel-r-2023-2024-ev', 'Marvel R', 'מארוול R', 'Marvel R', [2023, 2024], ['EV (TZ204XS1155)'],
       'manuals/2.-Marvel-R_Service-Manual_ENG.pdf', 'MG Marvel R Service Manual (אירופה), עמ\' 4-9', 80000,
       notes_extra=' בנוסף המסמך מציין כיול מיקום הסנכרונייזר (תיבת ההינע) כל 20,000 ק"מ.')
s.li('diagnostics', 'adjust', 'כיול מיקום הסנכרונייזר בתיבת ההינע: כל 20,000 ק"מ', every_km=20000); s.write()
s.rule('MG', ['MARVEL R'], [2023, 2024])
s = ev('mg-5-2023-2024-ev', 'MG5 Electric', 'MG5 חשמלית', 'MG5 EV', [2023, 2024], ['EV (TZ204XS1152)'],
       'manuals/2.-MG5_Service-Manual_ENG-20210514.pdf', 'MG5 Electric Service Manual (אירופה, מאי 2021), עמ\' 4-9', 80000)
s.rule('MG', ['MG5'], [2023, 2024], fuel=['חשמל'])

# EHS PHEV
s = Sched(id='mg-ehs-2021-2024-1.5t-phev', make='MG', make_he="אם.ג'י", model='EHS PHEV', model_he='EHS פלאג-אין', generation='EHS PHEV',
    years=[2021, 2024], engines=['1.5T PHEV (15E4E) + EDU'], fuel='plug-in-hybrid', importer=IMP,
    interval={'km': 24000, 'months': 12, 'note': 'לפי מסמך השירות האירופי של MG EHS: טיפול A כל 24,000 ק"מ או 12 חודשים, וטיפול B כל 48,000 ק"מ או 24 חודשים; בתנאים קשים שמן ומסנן כל 5,000 ק"מ'},
    cycle_km=96000, status='draft',
    notes=NOTE_IL + ' לפי המסמך האירופי שמן המנוע ומסנן השמן מוחלפים בכל טיפול (24,000 ק"מ או 12 חודשים); מסנן אוויר, מסנן מזגן ומצתים בטיפול B. יש לבצע טעינת איזון לסוללה לפחות פעם בחודש.')
ev_common(s)
s.all('engine_oil', 'replace'); s.all('oil_filter', 'replace'); s.all('drive_belt', 'inspect'); s.all('fuel_lines', 'inspect')
s.every('cabin_filter', 'replace', 48000, 'החלפה בטיפול B'); s.every('air_filter', 'replace', 48000, 'החלפה בטיפול B')
s.every('spark_plugs', 'replace', 48000, 'החלפה כל 48,000 ק"מ')
s.every('exhaust', 'inspect', 48000, 'מערכת פליטה, תושבות ומגני חום (טיפול B)')
s.every('evap_system', 'inspect', 48000, 'צנרת אדי דלק ומכל פחם (טיפול B)')
s.every('intercooler_pipes', 'inspect', 48000, 'סעפת יניקה (טיפול B)')
s.every('body_underside', 'inspect', 48000, 'תושבות מנוע (טיפול B)')
s.li('transmission_oil', 'replace', 'שמן תיבת ההינע החשמלית (EDU): כל 80,000 ק"מ', every_km=80000)
s.li('brake_fluid', 'replace', 'נוזל בלמים: כל שנתיים', every_months=24)
s.li('coolant', 'replace', 'נוזל קירור: כל 4 שנים או 96,000 ק"מ', every_km=96000, every_months=48)
s.li('drive_belt', 'replace', 'רצועת עזר: כל 3 שנים או 100,000 ק"מ', every_km=100000, every_months=36)
s.li('fuel_filter', 'replace', 'מסנן דלק (במשאבה): כל 8 שנים או 100,000 ק"מ', every_km=100000, every_months=96)
s.li('fuel_tank_air_filter', 'replace', 'מסנן אוויר של מודול אבחון דליפות במיכל הדלק: כל 4 שנים או 80,000 ק"מ', every_km=80000, every_months=48)
s.src('https://a.storyblok.com/f/325761/x/e6c09aa3f8/mg-ehs-service-portfolio-en-20201023.pdf', 'manufacturer', 'MG EHS Plug-in Hybrid Service Portfolio (אירופה, אוקטובר 2020), עמ\' 4-11; אותו מסמך גם ב-cdn.mgmotor.eu/manuals/2.-EHS_Service-Manial-EN-20201023-Final-Version.pdf')
s.src(*IL_SRC)
s.write(); s.rule('MG', ['EHS PHEV'], [2021, 2024])
save_rules('mg')
