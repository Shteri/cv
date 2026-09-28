from sched import *
IMP = 'כלמוביל'
CL = 'https://res.cloudinary.com/colmobil/images/'
def hv_checks(s):
    s.all('hybrid_system', 'inspect', 'סוללת מתח גבוה: חלודה או עיוות, ברגי קיבוע, שסתום אוורור, מחברי מתח גבוה ונמוך ורתמות')

def j7phev(meta=None, extra_note='', rule=True, extra_src=None):
    # ---------------- Jaecoo 7 PHEV
    s = Sched(id='jaecoo-7-2025-2026-1.5t-phev', make='Jaecoo', make_he="ג'אקו", model='Jaecoo 7 PHEV', model_he="ג'אקו 7 פלאג-אין", generation='J7 SHS',
        years=[2025, 2026], engines=['1.5 TGDI PHEV (SQRH4J15) + DHT'], fuel='plug-in-hybrid', importer=IMP,
        interval={'km': 15000, 'months': 12, 'note': 'לפי ספר הרכב של היבואן: טיפול כל 15,000 ק"מ או שנה; בתנאים קשים כל 7,500 ק"מ או 6 חודשים'},
        cycle_km=240000, status='reviewed',
        notes='הועתק מתוכנית התחזוקה בספר הרכב העברי של כלמוביל לג\'אקו 7 PHEV (מהדורת ינואר 2026, עמ\' 276-277; 16 עמודות של 15,000 ק"מ). במהדורה הקודמת (ינואר 2025) נוזל הקירור הוחלף כל 30,000 ק"מ והמצתים כל 45,000 ק"מ; כאן לפי המהדורה החדשה (60,000 ק"מ לשניהם). מסנן הקניסטר, צינור הקניסטר וצינור מילוי הדלק ב-long_interval. אין שורה למסנן מזגן בטבלה.')
    s.all('electrical_system', 'inspect', 'לוח מחוונים ומולטימדיה'); s.all('diagnostics'); s.all('wipers'); s.all('ac_system')
    s.every('coolant', 'replace', 60000, 'החלפה כל 60,000 ק"מ (48 חודשים)', other='inspect')
    s.every('brake_fluid', 'replace', 30000, 'החלפה כל 30,000 ק"מ (24 חודשים)', other='inspect')
    s.all('engine_oil', 'replace', 'SN/SP 5W-30'); s.all('oil_filter', 'replace')
    s.every('transmission_oil', 'replace', 60000, 'שמן גיר ומסנן (תיבת DHT): החלפה כל 60,000 ק"מ', other='inspect')
    s.all('battery_12v'); s.all('suspension', 'inspect', 'חופשים במתלים'); s.all('cv_boots', 'inspect', 'חופשים בגל ההינע')
    s.all('body_underside', 'inspect', 'ברגי חיזוק מרכב ותחתית הרכב (צינורות ומכלולים)'); s.all('steering', 'inspect', 'חופשים במערכת ההיגוי')
    s.all('tires', 'inspect', 'לחץ אוויר, שחיקה וברגים')
    s.every('spark_plugs', 'replace', 60000, 'החלפה כל 60,000 ק"מ', other='inspect')
    s.all('brake_pads'); s.all('brake_discs')
    s.every('air_filter', 'replace', 30000, 'החלפה כל 30,000 ק"מ', other='inspect')
    s.all('drive_belt'); hv_checks(s)
    s.every('wheel_alignment', 'inspect', 30000, 'בדיקת/כיוון פרונט כל 30,000 ק"מ')
    s.li('evap_system', 'replace', 'מסנן מיכל הקניסטר: כל 45,000 ק"מ', every_km=45000)
    s.li('evap_system', 'replace', 'צינור הקניסטר: ב-150,000 ק"מ', every_km=150000)
    s.li('fuel_lines', 'replace', 'צינור מילוי הדלק: כל 75,000 ק"מ', every_km=75000)
    s.spec(engine_oil='SN 5W-30 או SP 5W-30', _note='מספר הרכב העברי של כלמוביל')
    s.src(CL + 'v1768203870/J7-PHEV-web/J7-PHEV-web.pdf', 'importer', 'ספר רכב עברי JAECOO 7 PHEV (כלמוביל, מהדורת ינואר 2026), עמ\' 276-277 תוכנית תחזוקה')
    s.src(CL + 'v1744109858/J7-PHEV-OM_web_36923d3ea/J7-PHEV-OM_web_36923d3ea.pdf', 'importer', 'מהדורה קודמת (ינואר 2025), עמ\' 276-277 - נוזל קירור כל 30,000 ומצתים כל 45,000')
    s.src('https://jaecoo.co.il/car-book/', 'importer', 'עמוד "ספר רכב" באתר ג\'אקו ישראל')
    if meta: s.d.update(meta)
    if extra_note: s.d['notes'] = extra_note + ' ' + s.d['notes']
    if extra_src: s.srcs.insert(0, extra_src)
    s.write()
    if rule: s.rule('Jaecoo', ['JAECOO7 PHEV', 'JAECOO 7 PHEV'], [2025, 2026])
    return s

def j8phev():
    # ---------------- Jaecoo 8 PHEV
    s = Sched(id='jaecoo-8-2025-2026-1.5t-phev', make='Jaecoo', make_he="ג'אקו", model='Jaecoo 8 PHEV', model_he="ג'אקו 8 פלאג-אין", generation='J8 SHS',
        years=[2025, 2026], engines=['1.5 TGDI PHEV (SQRH4J15) + DHT'], fuel='plug-in-hybrid', importer=IMP,
        interval={'km': 15000, 'months': 12, 'note': 'לפי ספר הרכב של היבואן: כל 15,000 ק"מ או שנה; בתנאים קשים כל 7,500 ק"מ או 6 חודשים'},
        cycle_km=120000, status='reviewed',
        notes='הועתק מתוכנית התחזוקה בספר הרכב העברי של כלמוביל לג\'אקו 8 PHEV (2025, עמ\' 277-279; 10 עמודות של 15,000 ק"מ). כל הפריטים חוזרים במחזור של 60,000 ק"מ ולכן המחזור כאן 120,000. בטבלה נוזל תיבת ההילוכים מסומן להחלפה ב-60,000 וב-120,000, אך בהערה לידו כתוב 4 שנים או 40,000 ק"מ - כדאי לוודא מול היבואן.')
    s.all('electrical_system', 'inspect', 'מחוונים, מולטימדיה, צנרת ורתמות חיווט'); s.all('diagnostics'); s.all('wipers', 'inspect', 'להבים קדמיים ואחורי')
    s.all('ac_system', 'inspect', 'יעילות קירור ומערכת מיזוג'); s.all('cabin_filter', 'inspect')
    s.every('coolant', 'replace', 60000, 'החלפה כל 60,000 ק"מ; בשאר הטיפולים מפלס ונקודת קפיאה', other='inspect')
    s.every('brake_fluid', 'replace', 30000, 'החלפה כל 30,000 ק"מ; בשאר הטיפולים מפלס וריכוז מים', other='inspect')
    s.all('engine_oil', 'replace'); s.all('oil_filter', 'replace')
    s.every('transmission_oil', 'replace', 60000, 'נוזל תיבת ההילוכים ומסנן חיצוני: בטבלה ב-60,000; בהערה - 4 שנים או 40,000 ק"מ', other='inspect')
    s.all('battery_12v'); s.all('suspension', 'inspect', 'בולמי זעזועים'); s.all('cv_boots', 'inspect', 'גל הינע וגומיות')
    s.all('body_underside', 'inspect', 'מומנט ברגי שלדה, עוקת שמן ובורג ניקוז, גוף תיבת ההילוכים')
    s.all('steering', 'inspect', 'תיבת הגה, עמוד הגה, מוטות ומפרקים כדוריים')
    s.all('tires', 'inspect', 'מראה, סוליה, לחץ (כולל גלגל חלופי) ומומנט ברגי גלגל')
    s.every('spark_plugs', 'replace', 60000, 'החלפה כל 60,000 ק"מ', other='inspect')
    s.all('brake_pads'); s.all('brake_discs')
    s.every('air_filter', 'replace', 30000, 'החלפה כל 30,000 ק"מ', other='inspect')
    s.all('drive_belt'); hv_checks(s)
    s.li('tire_rotation', 'rotate', 'סבב צמיגים מומלץ כל 10,000 ק"מ (אופטימלי 5,000-7,000)', every_km=10000)
    s.li('fuel_filter', 'replace', 'מסנן דלק חיצוני (אם קיים): כל 30,000 ק"מ; המסנן שבמשאבה אינו דורש תחזוקה', every_km=30000)
    s.src(CL + 'v1768203756/J8-PHEV_OM_2025-web/J8-PHEV_OM_2025-web.pdf', 'importer', 'ספר רכב עברי JAECOO 8 PHEV 2025 (כלמוביל), עמ\' 276-279')
    s.write(); s.rule('Jaecoo', ['JAECOO8 PHEV', 'JAECOO 8 PHEV'], [2025, 2026])

def j5hev(meta=None, extra_note='', rule=True, extra_src=None):
    # ---------------- Jaecoo 5 HEV
    s = Sched(id='jaecoo-5-2025-2026-1.5-hev', make='Jaecoo', make_he="ג'אקו", model='Jaecoo 5 HEV', model_he="ג'אקו 5 היברידי", generation='J5 HEV',
        years=[2025, 2026], engines=['1.5 hybrid (SQRH4J15) + DHT 130HHB'], fuel='hybrid', importer=IMP,
        interval={'km': 10000, 'months': 12, 'note': 'לפי ספר הרכב של היבואן: טבלת התחזוקה בעמודות של 10,000 ק"מ או 12 חודשים'},
        cycle_km=120000, status='reviewed',
        notes='הועתק מתוכנית התחזוקה בספר הרכב העברי של כלמוביל לג\'אקו 5 HEV (2025, עמ\' 230-231; 10 עמודות של 10,000 ק"מ). פריטים שמרווחם נתון בטקסט (נוזל בלמים 40,000, נוזל גיר 60,000, מצתים 30,000) שובצו בטבלה; נוזל קירור (4 שנים או 80,000) ב-long_interval.')
    s.all('ac_system'); s.all('cabin_filter', 'inspect'); s.all('coolant', 'inspect', 'מפלס ונקודת קפיאה')
    s.every('brake_fluid', 'replace', 40000, 'החלפה כל שנתיים או 40,000 ק"מ; בשאר הטיפולים מפלס וריכוז מים', other='inspect')
    s.all('engine_oil', 'replace'); s.all('oil_filter', 'replace')
    s.every('transmission_oil', 'replace', 60000, 'נוזל תיבת הילוכים 130HHB: כל 4 שנים או 60,000 ק"מ; בשאר הטיפולים מפלס', other='inspect')
    s.all('battery_12v', 'inspect', 'מתח מצבר'); s.all('suspension', 'inspect', 'בולמי זעזועים'); s.all('cv_boots', 'inspect', 'גל הינע וגומיות')
    s.all('body_underside', 'inspect', 'מומנט ברגי שלדה, עוקת שמן ובורג ניקוז, גוף תיבת ההילוכים')
    s.all('steering', 'inspect', 'תיבת הגה, עמוד הגה, מוטות ומפרקים כדוריים')
    s.all('tires', 'inspect', 'מראה, סוליה, לחץ (כולל חלופי) ומומנט ברגי גלגל')
    s.every('spark_plugs', 'replace', 30000, 'החלפה כל 30,000 ק"מ')
    s.all('brake_pads'); s.all('brake_discs'); s.all('air_filter', 'inspect'); s.all('drive_belt')
    s.all('electrical_system', 'inspect', 'צנרת נוזלים ורתמות חיווט'); hv_checks(s)
    s.li('coolant', 'replace', 'נוזל קירור: כל 4 שנים או 80,000 ק"מ', every_km=80000, every_months=48)
    s.li('transmission_oil', 'replace', 'נוזל תיבת הילוכים 130HHB: כל 4 שנים (אם לא הגיע ל-60,000 ק"מ)', every_months=48)
    s.li('brake_fluid', 'replace', 'נוזל בלמים: כל שנתיים (אם לא הגיע ל-40,000 ק"מ)', every_months=24)
    s.li('tire_rotation', 'rotate', 'סבב צמיגים מומלץ כל 10,000 ק"מ', every_km=10000)
    s.src(CL + 'v1768203261/J5-HEV_OM-2025_web/J5-HEV_OM-2025_web.pdf', 'importer', 'ספר רכב עברי JAECOO 5 HEV 2025 (כלמוביל), עמ\' 230-231')
    if meta: s.d.update(meta)
    if extra_note: s.d['notes'] = extra_note + ' ' + s.d['notes']
    if extra_src: s.srcs.insert(0, extra_src)
    s.write()
    if rule: s.rule('Jaecoo', ['JAECOO 5 HEV', 'JAECOO5 HEV'], [2025, 2026])
    return s

def j5(meta=None, extra_note='', rule=True, extra_src=None):
    # ---------------- Jaecoo 5 petrol
    s = Sched(id='jaecoo-5-2025-2026-1.6t', make='Jaecoo', make_he="ג'אקו", model='Jaecoo 5', model_he="ג'אקו 5", generation='J5',
        years=[2025, 2026], engines=['1.6 TGDI (SQRF4J16C / SQRFJ16F) + DCT 730DHB'], fuel='petrol', importer=IMP,
        interval={'km': 15000, 'months': 12, 'note': 'לפי ספר הרכב של היבואן: טבלת תחזוקה בעמודות של 15,000 ק"מ או 12 חודשים; טיפול ראשון ב-15,000 ק"מ או 12 חודשים'},
        cycle_km=120000, status='reviewed',
        notes='הועתק מתוכנית התחזוקה בספר הרכב העברי של כלמוביל לג\'אקו 5 (בנזין, עמ\' 216-218). מסנן אוויר ומסנן מזגן: החלפה כל שנה או 10,000 ק"מ - ולכן בכל טיפול. נוזל בלמים כל שנתיים או 40,000 ק"מ (ב-long_interval).')
    s.all('electrical_system', 'inspect', 'מחוונים ומולטימדיה'); s.all('diagnostics'); s.all('wipers', 'inspect', 'להבים קדמיים ואחורי')
    s.all('ac_system', 'inspect', 'יעילות קירור ומערכת מיזוג'); s.all('cabin_filter', 'replace', 'כל שנה או 10,000 ק"מ - בכל טיפול')
    s.all('coolant', 'inspect', 'מפלס ונקודת קפיאה'); s.all('brake_fluid', 'inspect', 'מפלס וריכוז מים')
    s.all('engine_oil', 'replace'); s.all('oil_filter', 'replace')
    s.every('dct_oil', 'replace', 60000, 'נוזל תיבת הילוכים 730DHB: כל 60,000 ק"מ; בשאר הטיפולים מפלס', other='inspect')
    s.all('battery_12v', 'inspect', 'מתח מצבר'); s.all('suspension', 'inspect', 'בולמי זעזועים'); s.all('cv_boots', 'inspect', 'גל הינע וגומיות')
    s.all('body_underside', 'inspect', 'מומנט ברגי שלדה, עוקת שמן ובורג ניקוז, גוף תיבת ההילוכים')
    s.all('steering', 'inspect', 'תיבת הגה, עמוד הגה, מוטות ומפרקים כדוריים')
    s.all('tires', 'inspect', 'מראה, סוליה, לחץ (כולל חלופי) ומומנט ברגי גלגל')
    s.every('spark_plugs', 'replace', 30000, 'החלפה כל 30,000 ק"מ')
    s.all('brake_pads'); s.all('brake_discs'); s.all('air_filter', 'replace', 'כל שנה או 10,000 ק"מ - בכל טיפול'); s.all('drive_belt')
    s.li('brake_fluid', 'replace', 'נוזל בלמים: כל שנתיים או 40,000 ק"מ', every_km=40000, every_months=24)
    s.li('fuel_filter', 'replace', 'מסנן דלק חיצוני (אם קיים): כל 30,000 ק"מ; המסנן שבמשאבה אינו דורש תחזוקה', every_km=30000)
    s.li('tire_rotation', 'rotate', 'סבב צמיגים מומלץ כל 10,000 ק"מ', every_km=10000)
    s.src(CL + 'v1760942734/J5_OM_web/J5_OM_web.pdf', 'importer', 'ספר רכב עברי JAECOO 5 (כלמוביל, ספטמבר 2025), עמ\' 216-218')
    if meta: s.d.update(meta)
    if extra_note: s.d['notes'] = extra_note + ' ' + s.d['notes']
    if extra_src: s.srcs.insert(0, extra_src)
    s.write()
    if rule: s.rule('Jaecoo', ['JAECOO 5', 'JAECOO5'], [2025, 2026])
    return s

if __name__ == '__main__':
    j7phev(); j8phev(); j5hev(); j5()
    save_rules('jaecoo')
