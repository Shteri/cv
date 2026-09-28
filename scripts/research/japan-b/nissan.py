import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/dl/japan-b')
from gen import *
IMP = 'פריסבי (קרסו מוטורס)'
ZA = 'https://www.nissan-cdn.net/content/dam/Nissan/za/Maintenance/{}.pdf'
ZA2 = 'https://www.nissan.co.za/content/dam/Nissan/za/Maintenance/{}.pdf'
BLOCK = 'אתרי ניסאן ישראל (nissan.co.il) ו-service.freesbe.com לא מפרסמים ספרי רכב או לוחות טיפולים (service.freesbe.com ו-freesbe.com מחזירים 403); לכן זהו לוח בינלאומי'
def ns(id_, model, model_he, gen, years, engines, fuel, cycle, note, step=15000):
    return S(id_, 'Nissan', 'ניסאן', model, model_he, gen, years, engines, fuel, IMP, step, 12, note, cycle)

def za_chassis(s, n, cvt=False, mt=True, awd=False, drums=False, hinges=False):
    P30 = '-R' * (n // 2); I30 = '-I' * (n // 2)
    s.every('brake_fluid', 'inspect', 15000, 'בדיקת מפלס ודליפות של נוזל הבלמים והמצמד')
    s.pat('brake_fluid', P30, 15000, 'החלפת נוזל בלמים כל 30,000 ק"מ או 24 חודשים')
    s.pat('vacuum_hose', I30, 15000, 'צינורות ואקום של מגבר הבלמים, חיבורים ושסתום')
    if cvt: s.every('cvt_oil', 'inspect', 15000, 'בדיקת נזילות; בגרירה, גגון או דרכים קשות: בדיקת בלאי נוזל ה-CVT אצל ניסאן כל 90,000 ק"מ')
    if mt: s.every('manual_gearbox_oil', 'inspect', 15000, 'בגיר ידני: בדיקת נזילות')
    s.pat('steering', I30, 15000, 'תיבת הגה ומוטות, חלקי סרן ומתלים, צירי הנעה קדמיים')
    s.pat('suspension', I30, 15000); s.pat('cv_boots', I30, 15000)
    s.every('wheel_alignment', 'inspect', 15000, 'כיוון פרונט; לפי הצורך סבב ואיזון גלגלים')
    s.every('exhaust', 'inspect', 15000, 'מערכות בלמים, מצמד ופליטה')
    s.every('brake_pads', 'inspect', 15000); s.every('brake_discs', 'inspect', 15000)
    if drums: s.every('brake_drums', 'inspect', 15000)
    s.every('pedals', 'inspect', 15000, 'דוושת בלם, בלם חניה ומצמד: חופש, מהלך ותפקוד')
    s.every('seat_belts', 'inspect', 15000)
    s.pat('cabin_filter', P30, 15000, 'אם זרימת האוויר נחלשת או שהחלונות מתערפלים, להחליף מוקדם יותר')
    if awd:
        s.every('transfer_case_oil', 'inspect', 15000, 'בגרסת 4X4: בדיקת מפלס ונזילות')
        s.every('differential_oil', 'inspect', 15000, 'בדיקת מפלס ונזילות')
    if hinges: s.every('door_hinges', 'inspect', 15000, 'סיכה של מנעולים, צירים ותפס מכסה המנוע')

SEV = 'בתנאים מחמירים (אבק, נסיעות קצרות, חום קיצוני) חלק מהפריטים מתבצעים בתדירות כפולה, לפי טבלת התנאים המחמירים בגיליון.'

# ---------- Qashqai J11 1.2 DIG-T ----------
s = ns('nissan-qashqai-2014-2019-1.2-turbo', 'Qashqai', 'קשקאי', 'J11', (2014, 2019), ['1.2 DIG-T (HRA2DDT)'], 'petrol', 150000,
       'לפי הגיליון של ניסאן דרום אפריקה: טיפול כל 15,000 ק"מ או 12 חודשים')
s.every('engine_oil', 'replace', 15000); s.every('oil_filter', 'replace', 15000)
s.every('cooling_system', 'inspect', 15000)
s.pat('fuel_lines', '-I' * 5, 15000); s.pat('evap_system', '-I' * 5, 15000, 'צינורות אדי דלק ומיכל פחם')
s.pat('air_filter', '-R' * 5, 15000)
s.at('spark_plugs', 'replace', [60000, 120000], 'מצתי אירידיום, מסומנים בגיליון ב-60,000 וב-120,000')
s.li('spark_plugs', 'replace', every_km=60000)
s.li('drive_belt', 'replace', every_km=120000, every_months=72, note='רצועת אביזרים וגלגלות')
s.li('coolant', 'replace', first_km=150000, first_months=96, then_every_km=75000, then_every_months=48, note='בדיקת יחס התערובת כל 30,000 ק"מ או 24 חודשים')
s.li('valve_clearance', 'inspect', every_km=300000, note='אין טיפול תקופתי; לבדוק רק אם רעש השסתומים גובר. (שרשרת תזמון: החלפה כל 300,000 ק"מ)')
za_chassis(s, 10, cvt=True)
s.src(ZA.format('Qashqai'), 'manufacturer', 'Nissan South Africa, "NISSAN QASHQAI 1.2ℓ TURBO PETROL - PERIODIC MAINTENANCE", עמודים 7-9 (מנוע, שלדה, תנאים מחמירים); 10 עמודות של 15,000 ק"מ')
s.src('https://www.nissan.co.il/service.html', 'importer', BLOCK)
s.write('draft', 'טיוטה מלוח ניסאן דרום אפריקה (שוק ק"מ, אקלים חם) לקשקאי J11 עם מנוע 1.2 טורבו; לא נמצא ספר ישראלי. שרשרת תזמון כל 300,000 ק"מ, רצועת אביזרים כל 120,000 ק"מ או 6 שנים, מצתים ב-60,000 וב-120,000. דלק: מסנן בתוך המיכל ללא טיפול. ' + SEV)
rule('Nissan', ['QASHQAI'], (2014, 2019), s.d['id'], engine_codes=['HRA2', 'HRA2DDT', 'H5F', 'H5FT'])

# ---------- Qashqai J11 1.6 dCi / X-Trail T32 1.6 dCi (R9M) ----------
def r9m(id_, model, model_he, gen, years, fname, pages, extra_note):
    s = ns(id_, model, model_he, gen, years, ['1.6 dCi (R9M)'], 'diesel', 150000, 'לפי הגיליון של ניסאן דרום אפריקה: טיפול כל 15,000 ק"מ או 12 חודשים; שמן גם כשמופיעה התראת החלפת שמן')
    s.every('engine_oil', 'replace', 15000, 'אם מופיעה התראת החלפת שמן, להחליף בהקדם'); s.every('oil_filter', 'replace', 15000)
    s.every('drive_belt', 'inspect', 15000, 'רצועות הינע וגלגלת גל הארכובה')
    s.li('drive_belt', 'replace', every_km=160000, every_months=72)
    s.li('timing_belt', 'replace', every_km=300000, every_months=120, note='שרשרת תזמון: בגיר ידני כל 300,000 ק"מ או 120 חודשים; בגיר CVT כל 160,000 ק"מ או 240 חודשים. גלגלת גל ארכובה: החלפה כל 300,000')
    s.every('cooling_system', 'inspect', 15000)
    s.li('coolant', 'replace', first_km=150000, first_months=96, then_every_km=75000, then_every_months=48, note='בדיקת יחס התערובת כל 30,000 ק"מ או 24 חודשים')
    s.every('fuel_filter', 'inspect', 15000, 'ניקוז מים ממסנן הסולר (וגם כשנורית חיישן המים נדלקת)')
    s.pat('fuel_filter', '-R' * 5, 15000, 'החלפת מסנן סולר כל 30,000 ק"מ')
    s.pat('air_filter', '-R' * 5, 15000)
    za_chassis(s, 10, cvt=(model == 'Qashqai'), awd=True, hinges=(model == 'X-Trail'))
    s.src(ZA.format(fname), 'manufacturer', f'Nissan South Africa, "{model.upper()} 1.6ℓ DIESEL - PERIODIC MAINTENANCE", עמודים {pages}')
    s.src('https://www.nissan.co.il/service.html', 'importer', BLOCK)
    s.write('draft', f'טיוטה מלוח ניסאן דרום אפריקה ל-{model} עם מנוע 1.6 דיזל (R9M). {extra_note} ' + SEV)
    return s
s = r9m('nissan-qashqai-2014-2021-1.6-diesel', 'Qashqai', 'קשקאי', 'J11', (2014, 2021), 'Qashqai', '1-3', 'מסנן הסולר מנוקז בכל טיפול ומוחלף כל 30,000 ק"מ.')
rule('Nissan', ['QASHQAI'], (2014, 2021), s.d['id'], engine_codes=['R9M'])
s = r9m('nissan-x-trail-2014-2021-1.6-diesel', 'X-Trail', 'אקס-טרייל', 'T32', (2014, 2021), 'X-Trail', '1-3',
        'בגיליון של האקס-טרייל שורת מסנן האוויר מודפסת עם סימוני ניקוז (D) ושורת מסנן הסולר עם החלפה כל 30,000; בגיליון הקשקאי עם אותו מנוע מסנן האוויר מוחלף כל 30,000 ק"מ ומסנן הסולר מנוקז בכל טיפול, וכך נרשם כאן.')
rule('Nissan', ['X-TRAIL', 'X TRAIL', 'XTRAIL'], (2014, 2022), s.d['id'], engine_codes=['R9M'])

# ---------- Qashqai 1.5 dCi (K9K) ----------
s = ns('nissan-qashqai-2014-2021-1.5-diesel', 'Qashqai', 'קשקאי', 'J11', (2014, 2021), ['1.5 dCi (K9K)'], 'diesel', 150000,
       'לפי הגיליון של ניסאן דרום אפריקה: בדיקות כל 15,000 ק"מ; שמן, מסנן שמן ומסנן סולר כל 30,000 ק"מ או 12 חודשים')
s.every('engine_oil', 'replace', 30000, 'כל 30,000 ק"מ או 12 חודשים; מוקדם יותר אם מופיעה התראת שירות שמן')
s.every('oil_filter', 'replace', 30000)
s.every('fuel_filter', 'replace', 30000, 'כל 30,000 ק"מ או 12 חודשים')
s.li('timing_belt', 'replace', every_km=90000, every_months=48, note='רצועת תזמון וגלגלות: מרווח מקסימלי; להחליף מיד אם באה במגע עם דלק')
s.li('drive_belt', 'replace', every_km=90000, every_months=48, note='רצועת אביזרים וגלגלות')
s.every('cooling_system', 'inspect', 15000)
s.li('coolant', 'replace', first_km=150000, first_months=96, then_every_km=75000, then_every_months=48, note='בדיקת יחס התערובת כל 30,000 ק"מ או 24 חודשים')
s.pat('air_filter', '-R' * 5, 15000)
s.every('fuel_lines', 'inspect', 15000)
za_chassis(s, 10, cvt=False)
s.src(ZA.format('Qashqai'), 'manufacturer', 'Nissan South Africa, "NISSAN QASHQAI 1.5ℓ DIESEL - PERIODIC MAINTENANCE", עמודים 4-6')
s.src('https://www.nissan.co.il/service.html', 'importer', BLOCK)
s.write('draft', 'טיוטה מלוח ניסאן דרום אפריקה לקשקאי 1.5 דיזל (K9K). בגיליון הזה השמן והמסננים מתחלפים כל 30,000 ק"מ או שנה, ורצועת התזמון כל 90,000 ק"מ או 4 שנים. ' + SEV)
rule('Nissan', ['QASHQAI'], (2014, 2021), s.d['id'], engine_codes=['K9K'])

# ---------- Qashqai J12 1.3 (HR13) ----------
s = ns('nissan-qashqai-2019-2026-1.3-turbo', 'Qashqai', 'קשקאי', 'J12 (ו-J11 עם 1.3)', (2019, 2026), ['1.3 DIG-T / mild hybrid (HR13DDT)'], 'petrol', 120000,
       'לפי הגיליון של ניסאן דרום אפריקה ל-New Qashqai J12: טיפול כל 15,000 ק"מ או 12 חודשים')
s.every('engine_oil', 'replace', 15000); s.every('oil_filter', 'replace', 15000)
s.li('valve_clearance', 'inspect', every_km=300000, note='אין טיפול תקופתי לשסתומים; שרשרת תזמון: החלפה כל 300,000 ק"מ')
s.li('drive_belt', 'replace', every_km=90000, every_months=48, note='רצועת אביזרים וגלגלות')
s.li('coolant', 'replace', first_km=80000, first_months=48, then_every_km=60000, then_every_months=48, note='בדיקת יחס התערובת בכל מועד')
s.every('cooling_system', 'inspect', 15000)
s.pat('fuel_lines', '-I' * 4, 15000); s.pat('evap_system', '-I' * 4, 15000, 'צינורות אדי דלק ומיכל פחם')
s.every('air_filter', 'replace', 15000, 'מסנן נייר יבש: החלפה בכל טיפול; ניקוי כל 5,000 ק"מ')
s.at('spark_plugs', 'replace', [60000, 120000], 'מצתי אירידיום; להחליף מוקדם יותר אם המרווח עולה על 1.05 מ"מ')
s.li('spark_plugs', 'replace', every_km=60000)
s.every('brake_fluid', 'inspect', 15000, 'בדיקת מפלס ודליפות')
s.pat('brake_fluid', '-R' * 4, 15000, 'החלפה כל 30,000 ק"מ או 24 חודשים')
s.pat('vacuum_hose', '-I' * 4, 15000, 'צינורות ואקום של מגבר הבלמים')
s.every('cvt_oil', 'inspect', 15000, 'בגרירה או בדרכים קשות: בדיקת בלאי כל 90,000 ק"מ, ואם הבדיקה לא נעשית - החלפה כל 90,000')
s.every('manual_gearbox_oil', 'inspect', 15000, 'בגיר ידני: בדיקת נזילות')
s.pat('steering', '-I' * 4, 15000, 'הגה, סרן ומתלים, צירי הנעה'); s.pat('suspension', '-I' * 4, 15000); s.pat('cv_boots', '-I' * 4, 15000)
s.every('exhaust', 'inspect', 15000); s.every('brake_lines', 'inspect', 15000, 'מערכות בלמים ומצמד')
s.every('brake_pads', 'inspect', 15000); s.every('brake_discs', 'inspect', 15000)
s.every('pedals', 'inspect', 15000, 'דוושת בלם, בלם חניה ומצמד')
s.pat('cabin_filter', '-R' * 4, 15000)
s.src(ZA2.format('New-Qashqai-Maintenance-Schedule'), 'manufacturer', 'Nissan South Africa, "NISSAN NEW QASHQAI (J12) 1.3L - PERIODIC MAINTENANCE" (HR13), 3 עמודים, 8 עמודות של 15,000 ק"מ')
s.src('https://www.nissan.co.il/service.html', 'importer', BLOCK)
s.write('draft', 'טיוטה מלוח ניסאן דרום אפריקה לקשקאי J12 1.3. המנוע HR13 הותקן גם בקשקאי J11 מ-2019, ולכן הקובץ משמש גם לשנים 2019-2021 (בלי גיליון ייעודי לדור הקודם). מסנן אוויר מוחלף בכל טיפול; נוזל קירור: החלפה ראשונה ב-80,000 ק"מ ואחר כך כל 60,000. ' + SEV)
rule('Nissan', ['QASHQAI', 'QASHQAI HYBRID'], (2019, 2026), s.d['id'], engine_codes=['HR13', 'HR13DDT'])

# ---------- Juke F15 1.6 ----------
s = ns('nissan-juke-2010-2019-1.6', 'Juke', "ג'וק", 'F15', (2010, 2019), ['1.6 (HR16DE)'], 'petrol', 150000,
       'לפי הגיליון של ניסאן דרום אפריקה: טיפול כל 15,000 ק"מ או 12 חודשים')
s.every('engine_oil', 'replace', 15000); s.every('oil_filter', 'replace', 15000)
s.pat('drive_belt', '-I' * 5, 15000, 'רצועת אביזרים')
s.li('drive_belt', 'replace', every_km=300000, note='בגיליון, ליד שורת רצועת האביזרים: "החלף כל 300,000 ק"מ"')
s.every('cooling_system', 'inspect', 15000)
s.li('coolant', 'replace', first_km=150000, first_months=96, then_every_km=75000, then_every_months=48, note='בדיקת יחס התערובת כל 30,000 ק"מ או 24 חודשים')
s.pat('fuel_lines', '-I' * 5, 15000); s.pat('evap_system', '-I' * 5, 15000, 'צינורות אדי דלק ומיכל פחם')
s.pat('air_filter', '-R' * 5, 15000)
s.add(90000, 'spark_plugs', 'replace', 'מצתי אירידיום; מסומן בגיליון רק ב-90,000')
s.li('spark_plugs', 'replace', every_km=90000)
s.every('brake_fluid', 'inspect', 15000, 'בדיקת מפלס ודליפות')
s.pat('brake_fluid', '-R' * 5, 15000, 'החלפה כל 30,000 ק"מ או 24 חודשים')
s.pat('vacuum_hose', '-I' * 5, 15000, 'צינורות ואקום של מגבר הבלמים')
s.every('cvt_oil', 'inspect', 15000, 'בדיקת נזילות; בגרירה או בדרכים קשות בדיקת בלאי כל 90,000 ק"מ')
s.pat('steering', '-I' * 5, 15000, 'הגה, סרן ומתלים, צירי הנעה'); s.pat('suspension', '-I' * 5, 15000); s.pat('cv_boots', '-I' * 5, 15000)
s.every('wheel_alignment', 'inspect', 15000, 'לפי הצורך סבב ואיזון גלגלים')
s.every('brake_lines', 'inspect', 15000, 'מערכת הבלמים'); s.pat('exhaust', '-I' * 5, 15000)
s.every('brake_pads', 'inspect', 15000); s.every('brake_discs', 'inspect', 15000)
s.every('pedals', 'inspect', 15000, 'דוושת בלם ובלם חניה')
s.pat('cabin_filter', '-R' * 5, 15000); s.every('seat_belts', 'inspect', 15000)
s.src(ZA.format('Juke'), 'manufacturer', 'Nissan South Africa, "NISSAN JUKE 1.6ℓ PETROL ENGINE - PERIODIC MAINTENANCE" (HR16DE), עמודים 1-3')
s.src('https://www.nissan.co.il/service.html', 'importer', BLOCK)
s.write('draft', "טיוטה מלוח ניסאן דרום אפריקה לג'וק 1.6 (HR16DE, דור F15). מצתים מסומנים ב-90,000; מסנן אוויר, מסנן מזגן ונוזל בלמים כל 30,000 ק\"מ. " + SEV)
rule('Nissan', ['JUKE'], (2010, 2019), s.d['id'], engine_codes=['HR16', 'HR16DE'])

# ---------- Micra K13 1.2 (HR12) ----------
s = ns('nissan-micra-2011-2019-1.2', 'Micra', 'מיקרה', 'K13', (2011, 2019), ['1.2 (HR12DE)'], 'petrol', 150000,
       'לפי הגיליון של ניסאן דרום אפריקה: טיפול כל 15,000 ק"מ או 12 חודשים')
s.every('engine_oil', 'replace', 15000); s.every('oil_filter', 'replace', 15000)
s.pat('drive_belt', '-I' * 5, 15000, 'להחליף אם נמצאה פגומה')
s.every('cooling_system', 'inspect', 15000)
s.li('coolant', 'replace', first_km=75000, first_months=60, then_every_km=45000, then_every_months=36, note='בדיקת יחס התערובת באמצע כל מרווח')
s.pat('fuel_lines', '-I' * 5, 15000); s.pat('evap_system', '-I' * 5, 15000, 'צינורות אדי דלק ומיכל פחם')
s.pat('air_filter', '-R' * 5, 15000)
s.pat('spark_plugs', '-R' * 5, 15000, 'מצתי ניקל (מנוע HR12): החלפה כל 30,000 ק"מ')
za_chassis(s, 10, cvt=False, drums=True)
s.src(ZA.format('Micra'), 'manufacturer', 'Nissan South Africa, "NISSAN MICRA 1.2ℓ & 1.5ℓ PETROL - PERIODIC MAINTENANCE", עמודים 1-3 (שורת מצתי ניקל למנוע HR12)')
s.src('https://www.nissan.co.il/service.html', 'importer', BLOCK)
s.write('draft', 'טיוטה מלוח ניסאן דרום אפריקה למיקרה K13 (אותו דור ואותו מנוע HR12 כמו המיקרה מהודו שנמכרה בישראל). מצתי ניקל מוחלפים כל 30,000 ק"מ; נוזל קירור: החלפה ראשונה ב-75,000 ק"מ או 5 שנים ואחר כך כל 45,000 או 3 שנים. ' + SEV)
rule('Nissan', ['MICRA'], (2011, 2019), s.d['id'], engine_codes=['HR12', 'HR12DE'])

# ---------- NV200 1.5 dCi ----------
s = ns('nissan-nv200-2012-2019-1.5-diesel', 'NV200', 'NV200', 'M20', (2012, 2019), ['1.5 dCi (K9K)'], 'diesel', 150000,
       'לפי הגיליון של ניסאן דרום אפריקה: טיפול כל 15,000 ק"מ או 12 חודשים')
s.every('engine_oil', 'replace', 15000); s.every('oil_filter', 'replace', 15000)
s.li('timing_belt', 'replace', every_km=90000, every_months=48, note='רצועת תזמון וגלגלות: מרווח מקסימלי')
s.li('drive_belt', 'replace', every_km=90000, every_months=48, note='רצועת אביזרים וגלגלות')
s.pat('drive_belt', '-I' * 5, 15000)
s.pat('cooling_system', '-I' * 5, 15000)
s.li('coolant', 'replace', first_km=150000, first_months=96, then_every_km=75000, then_every_months=48, note='בדיקת יחס התערובת כל 30,000 ק"מ או 24 חודשים')
s.every('air_filter', 'replace', 15000); s.every('fuel_filter', 'replace', 15000)
s.pat('fuel_lines', '-I' * 5, 15000)
s.every('brake_fluid', 'inspect', 15000, 'בדיקת מפלס ודליפות')
s.pat('brake_fluid', '-R' * 5, 15000, 'החלפה כל 30,000 ק"מ או 24 חודשים')
s.pat('vacuum_hose', '-I' * 5, 15000)
s.every('brake_lines', 'inspect', 15000, 'מערכות בלמים ומצמד'); s.pat('exhaust', '-I' * 5, 15000)
s.every('manual_gearbox_oil', 'inspect', 15000, 'בדיקת נזילות'); s.add(90000, 'manual_gearbox_oil', 'replace', 'מסומן בגיליון ב-90,000 בלבד')
s.pat('steering', '-I' * 5, 15000, 'הגה, סרן ומתלים, צירי הנעה'); s.pat('suspension', '-I' * 5, 15000); s.pat('cv_boots', '-I' * 5, 15000)
s.every('brake_pads', 'inspect', 15000); s.every('brake_discs', 'inspect', 15000)
s.every('pedals', 'inspect', 15000, 'דוושת בלם, בלם חניה ומצמד')
s.pat('cabin_filter', '-R' * 5, 15000)
s.src(ZA.format('NV200'), 'manufacturer', 'Nissan South Africa, "NISSAN NV200 1.5ℓ DIESEL - PERIODIC MAINTENANCE", עמודים 4-6')
s.src('https://www.nissan.co.il/service.html', 'importer', BLOCK)
s.write('draft', 'טיוטה מלוח ניסאן דרום אפריקה ל-NV200 דיזל. מסנן אוויר ומסנן סולר מוחלפים בכל טיפול; רצועת תזמון ורצועת אביזרים כל 90,000 ק"מ או 4 שנים. ' + SEV)
rule('Nissan', ['NV200', 'NV 200'], (2010, 2021), s.d['id'], engine_codes=['K9K'])

# ---------- Almera N17 (sister: SA 1.5 HR15 -> Israeli 1.6 HR16) ----------
s = ns('nissan-almera-2012-2016-1.5-1.6', 'Almera', 'אלמרה', 'N17', (2012, 2016), ['1.6 (HR16DE)', '1.5 (HR15DE)'], 'petrol', 120000,
       'לפי הגיליון של ניסאן דרום אפריקה לאלמרה 1.5: טיפול כל 15,000 ק"מ או 12 חודשים')
s.every('engine_oil', 'replace', 15000); s.every('oil_filter', 'replace', 15000)
s.pat('drive_belt', '-I' * 4, 15000, 'להחליף אם נמצאה פגומה')
s.every('cooling_system', 'inspect', 15000)
s.li('coolant', 'replace', first_km=150000, first_months=96, then_every_km=75000, then_every_months=48, note='בדיקת יחס התערובת כל 30,000 ק"מ או 24 חודשים')
s.pat('fuel_lines', '-I' * 4, 15000); s.pat('evap_system', '-I' * 4, 15000)
s.pat('air_filter', '-R' * 4, 15000)
s.add(90000, 'spark_plugs', 'replace', 'מצתי אירידיום; מסומן ב-90,000'); s.li('spark_plugs', 'replace', every_km=90000)
za_chassis(s, 8, cvt=False, drums=True, hinges=True)
s.svc  # cabin filter: the Almera sheet has no A/C filter row
for k in list(s.svc): s.svc[k] = [x for x in s.svc[k] if x['item'] != 'cabin_filter']
s.every('transmission_oil', 'inspect', 15000, 'גיר אוטומטי: בדיקת נזילות')
s.src(ZA.format('Almera'), 'manufacturer', 'Nissan South Africa, "NISSAN ALMERA 1.5ℓ PETROL - PERIODIC MAINTENANCE", עמודים 1-3')
s.src('https://www.nissan.co.il/service.html', 'importer', BLOCK)
s.write('draft', 'טיוטה: לוח ניסאן דרום אפריקה לאלמרה N17 עם מנוע 1.5 (HR15DE). האלמרה שנמכרה בישראל (מתוצרת מקסיקו) היא אותו דור עם מנוע 1.6 מאותה משפחה (HR16DE), ולכן זה דגם אחות. בגיליון אין שורה למסנן מזגן. ' + SEV)
rule('Nissan', ['ALMERA'], (2012, 2016), s.d['id'], engine_codes=['HR16', 'HR16DE', 'HR15'])

# ---------- Sentra (US owner's manuals, km column) ----------
USN = 'לוח אמריקאי (Nissan USA). הטבלה מציגה מייל וגם ק"מ; נלקחו ערכי הק"מ של הספר (5,000 מייל = 8,000 ק"מ)'
s = ns('nissan-sentra-2016-2019-1.8', 'Sentra', 'סנטרה', 'B17', (2016, 2019), ['1.8 (MRA8DE)'], 'petrol', 96000,
       'לפי ספר הבעלים האמריקאי: שמן ומסנן כל 8,000 ק"מ (5,000 מייל) או 6 חודשים', step=8000)
s.every('engine_oil', 'replace', 8000); s.every('oil_filter', 'replace', 8000)
s.at('air_filter', 'replace', [48000, 96000])
s.at('evap_system', 'inspect', [32000, 64000, 96000]); s.at('fuel_lines', 'inspect', [32000, 64000, 96000])
s.at('drive_belt', 'inspect', [64000, 80000, 96000], 'אחרי 64,000 ק"מ או 48 חודשים: בדיקה כל 16,000 ק"מ או 12 חודשים')
s.li('spark_plugs', 'replace', every_km=168000, note='מצתי אירידיום/פלטינה; להחליף מוקדם יותר אם המרווח עולה על 1.35 מ"מ')
s.li('coolant', 'replace', first_km=168000, first_months=84, then_every_km=120000, then_every_months=60)
for k in range(16000, 96001, 16000):
    for it in ('brake_lines', 'brake_pads', 'brake_discs', 'cvt_oil', 'manual_gearbox_oil', 'cv_boots'): s.add(k, it, 'inspect')
for k in (32000, 64000, 96000):
    s.add(k, 'brake_fluid', 'replace', 'כל 32,000 ק"מ או 24 חודשים'); s.add(k, 'steering', 'inspect', 'הגה, סרן ומתלים'); s.add(k, 'suspension', 'inspect'); s.add(k, 'exhaust', 'inspect')
for k in (24000, 48000, 72000, 96000): s.add(k, 'cabin_filter', 'replace', 'כל 24,000 ק"מ או 18 חודשים')
s.every('tire_rotation', 'rotate', 8000, 'סבב צמיגים כל 8,000 ק"מ')
s.src('https://www.nissanusa.com/content/dam/Nissan/us/manuals-and-guides/sentra/2019/2019-Nissan-Sentra-owner-manual.pdf', 'manufacturer',
      '2019 Sentra Owner\'s Manual and Maintenance Information (ארה"ב), פרק 9 "Maintenance and schedules", עמודי PDF 417-422 (טבלאות 9-8 עד 9-12)')
s.src('https://www.nissan.co.il/service.html', 'importer', BLOCK)
s.write('draft', 'טיוטה מספר הבעלים האמריקאי של סנטרה 2019 (דור B17, מנוע 1.8 MRA8DE; בישראל הסנטרה מיובאת ממקסיקו). ' + USN + '. המרווחים קצרים מהמקובל בישראל; בתנאים מחמירים נוזל בלמים כל 16,000 ק"מ ובדיקות מתלים ובלמים כל 8,000.')
rule('Nissan', ['SENTRA'], (2016, 2019), s.d['id'], engine_codes=['MRA8DE', 'MRA8'])

s = ns('nissan-sentra-2020-2026-2.0', 'Sentra', 'סנטרה', 'B18', (2020, 2026), ['2.0 (MR20DD)'], 'petrol', 192000,
       'לפי ספר הבעלים האמריקאי: שמן ומסנן כל 16,000 ק"מ (10,000 מייל) או 12 חודשים, או מוקדם יותר לפי מחוון השמן (OCS)', step=8000)
for k in range(16000, 192001, 16000):
    s.add(k, 'engine_oil', 'replace', 'או כשמופיע מחוון החלפת השמן'); s.add(k, 'oil_filter', 'replace')
    for it in ('brake_lines', 'brake_pads', 'brake_discs', 'cvt_oil', 'manual_gearbox_oil', 'cv_boots'): s.add(k, it, 'inspect')
for k in range(32000, 192001, 32000):
    s.add(k, 'brake_fluid', 'replace', 'כל 32,000 ק"מ או 24 חודשים')
    for it in ('evap_system', 'fuel_lines', 'exhaust', 'steering', 'suspension'): s.add(k, it, 'inspect')
for k in range(24000, 192001, 24000): s.add(k, 'cabin_filter', 'replace', 'כל 24,000 ק"מ או 18 חודשים')
for k in range(48000, 192001, 48000): s.add(k, 'air_filter', 'replace')
for k in range(64000, 192001, 16000): s.add(k, 'drive_belt', 'inspect', 'מ-64,000 ק"מ ואילך')
s.every('tire_rotation', 'rotate', 8000, 'סבב צמיגים כל 8,000 ק"מ')
s.every('diagnostics', 'inspect', 8000, 'בדיקות כלליות בכל ביקור: תאורה ומגבים, מפלסי נוזלים, רצועות וצינורות, מסנן אוויר, מתלים, מצבר, צמיגים')
s.add(168000, 'spark_plugs', 'replace'); s.li('spark_plugs', 'replace', every_km=168000, note='להחליף מוקדם יותר אם המרווח עולה על 1.35 מ"מ')
s.add(168000, 'coolant', 'replace'); s.li('coolant', 'replace', first_km=168000, first_months=84, then_every_km=120000, then_every_months=60)
s.src('https://cdn.dealereprocess.org/cdn/servicemanuals/nissan/2022-sentra.pdf', 'manufacturer',
      '2022 Sentra Owner\'s Manual and Maintenance Information (ארה"ב; עותק של הספר הרשמי), פרק 9, "2.0L 4 CYLINDER (MR20DD)", עמודי PDF 489-497')
s.src('https://www.nissan.co.il/service.html', 'importer', BLOCK)
s.write('draft', 'טיוטה מספר הבעלים האמריקאי של סנטרה 2022 (דור B18, מנוע 2.0 MR20DD). ' + USN + '. הספר רשום כרשימת פעולות לכל ביקור של 8,000 ק"מ; בתנאים מחמירים נוזל בלמים כל 16,000 ק"מ ושמן גיר ידני כל 32,000.')
rule('Nissan', ['SENTRA'], (2020, 2026), s.d['id'], engine_codes=['MR20DD', 'MR20'])
save_rules('rules_nissan.json')
