from lib import grid, write
CDN = 'https://cdn.dealereprocess.org/cdn/servicemanuals/'
UMI = 'יו.אם.איי'
OLM = 'לפי מחוון חיי השמן (הודעת CHANGE ENGINE OIL SOON), ולפחות פעם בשנה'
def base_rows(air_inspect=True, halfshaft=False):
    r = [('engine_oil','replace','all',OLM), ('oil_filter','replace','all'), ('tire_rotation','rotate','all'),
         ('coolant','inspect','all','מפלס'), ('washer_fluid','inspect','all'), ('wipers','inspect','all'), ('tires','inspect','all','לחץ ובלאי')]
    if air_inspect: r.append(('air_filter','inspect','all'))
    r += [('brake_pads','inspect','all','מערכת הבלמים'), ('brake_lines','inspect','all'), ('steering','inspect','all'), ('suspension','inspect','all','מתלים ושלדה')]
    if halfshaft: r.append(('cv_boots','inspect','all','גלי הנעה ומפרקים'))
    r += [('seat_belts','inspect','all','מערכות ריסון'), ('fuel_lines','inspect','all'), ('exhaust','inspect','all'), ('door_hinges','clean','all','סיכה של רכיבי מרכב'), ('parking_brake','inspect','all','כולל מנגנון P בגיר')]
    return r
INTERVAL = dict(km=12000, months=12, note='לפי ספר הנהג של GM (צפון אמריקה): כל 12,000 ק"מ סבב צמיגים ובדיקות; שמן ומסנן לפי מחוון חיי השמן ולפחות פעם בשנה')
NOTE_US = 'טיוטה מספר הנהג האמריקאי של GM (הספר מציג ק"מ ומייל). אתר היבואן (יו.אם.איי) חסום ולא נמצא ספר עברי. השמן מוחלף לפי מחוון חיי השמן ולפחות פעם בשנה; שאר הפריטים לפי טבלת השירותים הנוספים (נורמלי). '

def common_long(extra=()):
    return [dict(item='coolant', action='replace', every_km=240000, every_months=60, note='ניקוז ומילוי (DEX-COOL), 240,000 ק"מ או 5 שנים'),
            dict(item='drive_belt', action='inspect', every_km=240000, every_months=120, note='240,000 ק"מ או 10 שנים')] + list(extra)

# Cadillac XT5 2017-2019 3.6 LGX (2018 manual)
rows = base_rows() + [
 ('cabin_filter','replace',[36000,72000,108000,144000,180000,216000],'או כל שנתיים'),
 ('evap_system','inspect',[72000,144000,216000],'צנרת דלק ואדים'),
 ('air_filter','replace',[72000,144000,216000],'או כל 4 שנים'),
 ('spark_plugs','replace',[156000]),
]
write(dict(id='cadillac-xt5-2017-2019-3.6', make='Cadillac', make_he='קאדילאק', model='XT5', model_he='XT5', generation='C1UL', years=[2017,2019],
 engines=['3.6 V6 (LGX)'], fuel='petrol', importer=UMI, interval=INTERVAL, cycle_km=240000, services=grid(12000,240000,rows),
 long_interval=common_long([dict(item='transmission_oil', action='replace', every_km=72000, note='שימוש קשה בלבד (חום ופקקים, הרים, גרירה)')]),
 time_based=[dict(item='brake_fluid', action='replace', months=60, note='כל 5 שנים')],
 specs=dict(engine_oil='dexos2, לפי הספר', coolant='DEX-COOL', _note='טיוטה; לאמת מול ספר הנהג'),
 sources=[dict(url=CDN+'cadillac/2018-xt5.pdf', kind='manufacturer', note='2018 Cadillac XT5 Owner\'s Manual (GM, ארה"ב/קנדה), Maintenance Schedule עמ\' 330-334 (עמודי PDF 331-335): Required Services ו-Additional Required Services Normal/Severe'),
          dict(url=CDN+'cadillac/2017-xt5.pdf', kind='manufacturer', note='ספר 2017, אותו פרק')],
 status='draft', notes=NOTE_US + 'מסנן מיזוג כל 36,000 ק"מ, מסנן אוויר ומערכת אדי דלק כל 72,000, מצתים ב-156,000, נוזל קירור ובדיקת רצועות ב-240,000. נוזל בלמים כל 5 שנים. שמן גיר רק בשימוש קשה (כל 72,000).'))

# Cadillac XT5 / XT6 2020-2026 3.6 LGX (2021 XT5 + 2022 XT6 manuals)
rows = base_rows(air_inspect=True, halfshaft=True) + [
 ('cabin_filter','replace',[36000,72000,108000,144000,180000,216000],'או כל שנתיים'),
 ('evap_system','inspect',[72000,144000,216000],'XT5'),
 ('wipers','replace',[24000*i for i in range(1,11)],'מגבים קדמיים ואחוריים, או כל 12 חודשים'),
 ('spark_plugs','replace',[156000]),
]
write(dict(id='cadillac-xt5-xt6-2020-2026-3.6', make='Cadillac', make_he='קאדילאק', model='XT5 / XT6', model_he='XT5 / XT6', generation='C1UL / C1TL', years=[2020,2026],
 engines=['3.6 V6 (LGX)'], fuel='petrol', importer=UMI, interval=INTERVAL, cycle_km=240000, services=grid(12000,240000,rows),
 long_interval=common_long([
   dict(item='differential_oil', action='replace', every_km=240000, note='סרן אחורי, הנעה כפולה; בשימוש קשה כל 120,000'),
   dict(item='transmission_oil', action='replace', every_km=72000, note='שימוש קשה בלבד'),
 ]),
 time_based=[dict(item='brake_fluid', action='replace', months=60, note='כל 5 שנים'), dict(item='ac_refrigerant', action='replace', months=84, note='החלפת סופח הלחות (desiccant) של המזגן כל 7 שנים')],
 specs=dict(engine_oil='dexos, לפי הספר', coolant='DEX-COOL', _note='טיוטה; לאמת מול ספר הנהג'),
 sources=[dict(url=CDN+'cadillac/2021-xt5.pdf', kind='manufacturer', note='2021 Cadillac XT5 Owner\'s Manual, Maintenance Schedule עמ\' 376-382 (עמודי PDF 377-383): מצתים 3.6 ב-156,000, 2.0 ב-96,000/192,000'),
          dict(url=CDN+'cadillac/2022-xt6.pdf', kind='manufacturer', note='2022 Cadillac XT6 Owner\'s Manual, Maintenance Schedule (עמודי PDF 382-388): אותה טבלה בלי שורת אדי הדלק')],
 status='draft', notes=NOTE_US + 'מ-2020 מסנן האוויר מוחלף לפי מחוון חיי המסנן ברכב. מסנן מיזוג כל 36,000 ק"מ, מגבים כל 24,000 או שנה, מצתים ב-156,000, שמן סרן אחורי ב-240,000 (הנעה כפולה), תומכי גז של מכסה המנוע/תא המטען ב-120,000 או 10 שנים, נוזל קירור ב-240,000 או 5 שנים, נוזל בלמים כל 5 שנים, סופח לחות במזגן כל 7 שנים.'))

# Cadillac XT4 / XT5 2.0T LSY 2019-2026
rows = base_rows(air_inspect=True, halfshaft=True) + [
 ('cabin_filter','replace',[36000,72000,108000,144000,180000,216000],'או כל שנתיים'),
 ('evap_system','inspect',[72000,144000,216000]),
 ('wipers','replace',[24000*i for i in range(1,11)],'מגבים קדמיים ואחוריים, או כל 12 חודשים'),
 ('spark_plugs','replace',[96000,192000]),
]
write(dict(id='cadillac-xt4-xt5-2019-2026-2.0t', make='Cadillac', make_he='קאדילאק', model='XT4 / XT5 2.0T', model_he='XT4 / XT5 2.0 טורבו', generation='E2 / C1UL', years=[2019,2026],
 engines=['2.0 טורבו (LSY)'], fuel='petrol', importer=UMI, interval=INTERVAL, cycle_km=240000, services=grid(12000,240000,rows),
 long_interval=common_long([
   dict(item='differential_oil', action='replace', every_km=240000, note='סרן אחורי, הנעה כפולה; בשימוש קשה כל 120,000'),
   dict(item='transmission_oil', action='replace', every_km=72000, note='שימוש קשה בלבד'),
 ]),
 time_based=[dict(item='brake_fluid', action='replace', months=60, note='כל 5 שנים'), dict(item='ac_refrigerant', action='replace', months=84, note='החלפת סופח הלחות של המזגן כל 7 שנים')],
 specs=dict(engine_oil='dexos, לפי הספר', coolant='DEX-COOL', _note='טיוטה; לאמת מול ספר הנהג'),
 sources=[dict(url=CDN+'cadillac/2021-xt4.pdf', kind='manufacturer', note='2021 Cadillac XT4 Owner\'s Manual, Maintenance Schedule (עמודי PDF 359-365)'),
          dict(url=CDN+'cadillac/2021-xt5.pdf', kind='manufacturer', note='2021 Cadillac XT5: שורת מצתים למנוע 2.0 (96,000/192,000) זהה')],
 status='draft', notes=NOTE_US + 'מסנן אוויר לפי מחוון חיי המסנן; מסנן מיזוג כל 36,000 ק"מ; מצתים כל 96,000; מגבים כל 24,000 או שנה; תומכי גז ב-120,000 או 10 שנים; נוזל קירור ב-240,000 או 5 שנים; נוזל בלמים כל 5 שנים.'))

# Cadillac SRX 2013-2016 3.6 LFX (2014 manual)
rows = base_rows() + [
 ('cabin_filter','replace',[36000,72000,108000,144000,180000,216000],'או כל שנתיים'),
 ('evap_system','inspect',[72000,144000,216000]),
 ('air_filter','replace',[72000,144000,216000],'או כל 4 שנים'),
 ('spark_plugs','replace',[156000]),
 ('transmission_oil','replace',[156000],'והחלפת מסנן אם ניתן'),
]
write(dict(id='cadillac-srx-2013-2016-3.6', make='Cadillac', make_he='קאדילאק', model='SRX', model_he='SRX', generation='דור 2 (מתיחת פנים)', years=[2013,2016],
 engines=['3.6 V6 (LFX)'], fuel='petrol', importer=UMI, interval=INTERVAL, cycle_km=240000, services=grid(12000,240000,rows),
 long_interval=common_long([dict(item='transmission_oil', action='replace', every_km=72000, note='שימוש קשה; בשימוש רגיל ב-156,000'), dict(item='brake_fluid', action='replace', every_km=240000, every_months=120, note='240,000 ק"מ או 10 שנים')]),
 time_based=[],
 specs=dict(engine_oil='dexos, לפי הספר', coolant='DEX-COOL', _note='טיוטה; לאמת מול ספר הנהג'),
 sources=[dict(url=CDN+'cadillac/2014-srx.pdf', kind='manufacturer', note='2014 Cadillac SRX Owner\'s Manual, Maintenance Schedule עמ\' 11-3 עד 11-8 (עמודי PDF 355-360)')],
 status='draft', notes=NOTE_US + 'מסנן מיזוג כל 36,000 ק"מ, מסנן אוויר ובדיקת אדי דלק כל 72,000, מצתים ושמן גיר ב-156,000, נוזל קירור ורצועות ב-240,000. נוזל בלמים ב-240,000 או 10 שנים.'))

# Cadillac ATS / CTS 2.0T LTG (2016 ATS manual)
rows = base_rows() + [
 ('cabin_filter','replace',[36000,72000,108000,144000,180000,216000],'או כל שנתיים'),
 ('evap_system','inspect',[72000,144000,216000]),
 ('air_filter','replace',[72000,144000,216000],'או כל 4 שנים'),
 ('differential_oil','replace',[72000,144000,216000],'סרן אחורי עם דיפרנציאל מוגבל החלקה בלבד'),
 ('spark_plugs','replace',[96000,192000]),
]
write(dict(id='cadillac-ats-cts-2013-2019-2.0t', make='Cadillac', make_he='קאדילאק', model='ATS / CTS', model_he='ATS / CTS', generation='A1SL / A1LL', years=[2013,2019],
 engines=['2.0 טורבו (LTG)'], fuel='petrol', importer=UMI, interval=INTERVAL, cycle_km=240000, services=grid(12000,240000,rows),
 long_interval=common_long([dict(item='transmission_oil', action='replace', every_km=72000, note='שימוש קשה בלבד (גם שמן סרן, תיבת העברה)')]),
 time_based=[dict(item='brake_fluid', action='replace', months=60, note='כל 5 שנים')],
 specs=dict(engine_oil='dexos, לפי הספר', coolant='DEX-COOL', _note='טיוטה; לאמת מול ספר הנהג'),
 sources=[dict(url=CDN+'cadillac/2016-ats.pdf', kind='manufacturer', note='2016 Cadillac ATS Owner\'s Manual, Maintenance Schedule (עמודי PDF 379-386): מצתים למנוע 2.0 טורבו ב-96,000/192,000')],
 status='draft', notes=NOTE_US + 'מסנן מיזוג כל 36,000 ק"מ, מסנן אוויר ובדיקת אדי דלק כל 72,000, מצתים כל 96,000, נוזל קירור ורצועות ב-240,000. CTS עם אותו מנוע (LTG) מופה לאותה טבלה כטבלה אחות (ספר ה-CTS לא נבדק).'))

# Buick LaCrosse 2010-2011 (2011 manual, text schedule)
rows = base_rows() + [('evap_system','inspect',[80000,160000,240000])] 
# 80,000 is not on the 12,000 grid -> keep evap/air as long_interval instead
rows = base_rows()
write(dict(id='buick-lacrosse-2010-2012-2.4-3.0-3.6', make='Buick', make_he='ביואיק', model='LaCrosse', model_he='לה קרוס', generation='דור 2', years=[2010,2012],
 engines=['2.4 (LAF)', '3.0 V6 (LF1)', '3.6 V6 (LLT)'], fuel='petrol', importer=UMI, interval=INTERVAL, cycle_km=240000, services=grid(12000,240000,rows),
 long_interval=common_long([
   dict(item='cabin_filter', action='replace', every_km=40000, every_months=24, note='בהחלפת השמן הראשונה אחרי כל 40,000 ק"מ, או כל 24 חודשים'),
   dict(item='air_filter', action='replace', every_km=80000, note='בהחלפת השמן הראשונה אחרי כל 80,000 ק"מ'),
   dict(item='evap_system', action='inspect', every_km=80000),
   dict(item='transmission_oil', action='replace', every_km=160000, note='שימוש רגיל; בשימוש קשה כל 80,000'),
   dict(item='transfer_case_oil', action='replace', every_km=160000, note='הנעה כפולה; בשימוש קשה כל 80,000'),
   dict(item='spark_plugs', action='replace', every_km=160000),
 ]),
 time_based=[],
 specs=dict(engine_oil='dexos', coolant='DEX-COOL', brake_fluid='DOT 3', _note='מטבלת הנוזלים בספר 2011 (עמ\' 11-7)'),
 sources=[dict(url=CDN+'buick/2011-lacrosse.pdf', kind='manufacturer', note='2011 Buick LaCrosse Owner Manual (GM, ארה"ב/קנדה), Scheduled Maintenance עמ\' 11-2 עד 11-6 (עמודי PDF 414-418)')],
 status='draft', notes=NOTE_US + 'בספר 2011 הלוח בנוי לפי "החלפת השמן הראשונה אחרי כל X ק"מ": מסנן מיזוג 40,000 (או שנתיים), מסנן אוויר ובדיקת אדי דלק 80,000, שמן גיר, תיבת העברה ומצתים 160,000, נוזל קירור ורצועות 240,000. סבב צמיגים כל 12,000.'))

# Buick LaCrosse 2012-2016 (2012 manual chart)
rows = base_rows() + [
 ('cabin_filter','replace',[36000,72000,108000,144000,180000,216000],'או כל שנתיים'),
 ('evap_system','inspect',[72000,144000,216000]),
 ('air_filter','replace',[72000,144000,216000],'או כל 4 שנים'),
 ('spark_plugs','replace',[156000]),
 ('transmission_oil','replace',[156000],'והחלפת מסנן אם ניתן'),
 ('transfer_case_oil','replace',[156000],'הנעה כפולה'),
 ('hsg_belt','replace',[120000],'רצועת עזר בגרסת eAssist בלבד'),
]
write(dict(id='buick-lacrosse-2012-2016-2.4-3.6', make='Buick', make_he='ביואיק', model='LaCrosse', model_he='לה קרוס', generation='דור 2 (2012 ואילך)', years=[2012,2016],
 engines=['3.6 V6 (LFX)', '2.4 eAssist (LUK)'], fuel='petrol', importer=UMI, interval=INTERVAL, cycle_km=240000, services=grid(12000,240000,rows),
 long_interval=common_long([dict(item='transmission_oil', action='replace', every_km=72000, note='שימוש קשה (גם תיבת העברה)')]),
 time_based=[],
 specs=dict(engine_oil='dexos', coolant='DEX-COOL', _note='טיוטה'),
 sources=[dict(url=CDN+'buick/2012-lacrosse.pdf', kind='manufacturer', note='2012 Buick LaCrosse Owner Manual, Maintenance Schedule עמ\' 11-3 עד 11-8 (עמודי PDF 433-438); הטבלאות הן תמונות ונקראו מהעמוד')],
 status='draft', notes=NOTE_US + 'מסנן מיזוג כל 36,000 ק"מ, מסנן אוויר ובדיקת אדי דלק כל 72,000, מצתים, שמן גיר ותיבת העברה ב-156,000, נוזל קירור ורצועות ב-240,000. רכבי 2013-2014 נושאים אותו מנוע (LFX); נלקחה טבלת 2012.'))

# Cadillac SRX 2010-2012 (2011 manual text schedule, same structure as LaCrosse 2011)
write(dict(id='cadillac-srx-2010-2012-3.0', make='Cadillac', make_he='קאדילאק', model='SRX', model_he='SRX', generation='דור 2', years=[2010,2012],
 engines=['3.0 V6 (LF1)'], fuel='petrol', importer=UMI, interval=INTERVAL, cycle_km=240000, services=grid(12000,240000,base_rows()),
 long_interval=common_long([
   dict(item='cabin_filter', action='replace', every_km=40000, every_months=24, note='בהחלפת השמן הראשונה אחרי כל 40,000 ק"מ, או כל 24 חודשים'),
   dict(item='air_filter', action='replace', every_km=80000, note='בהחלפת השמן הראשונה אחרי כל 80,000 ק"מ'),
   dict(item='evap_system', action='inspect', every_km=80000),
   dict(item='transmission_oil', action='replace', every_km=160000, note='שימוש רגיל; בשימוש קשה כל 80,000'),
   dict(item='transfer_case_oil', action='replace', every_km=160000, note='הנעה כפולה; בשימוש קשה כל 80,000'),
   dict(item='spark_plugs', action='replace', every_km=160000),
 ]),
 time_based=[],
 specs=dict(engine_oil='dexos', coolant='DEX-COOL', _note='טיוטה'),
 sources=[dict(url=CDN+'cadillac/2011-srx.pdf', kind='manufacturer', note='2011 Cadillac SRX Owner Manual (GM, ארה"ב/קנדה), Scheduled Maintenance עמ\' 11-2 עד 11-6 (עמודי PDF 454-458)'),
          dict(url=CDN+'cadillac/2012-srx.pdf', kind='manufacturer', note='ספר 2012 הורד לבדיקה')],
 status='draft', notes=NOTE_US + 'בספר 2011 הלוח בנוי לפי "החלפת השמן הראשונה אחרי כל X ק"מ": מסנן מיזוג 40,000 (או שנתיים), מסנן אוויר ובדיקת אדי דלק 80,000, שמן גיר, תיבת העברה ומצתים 160,000, נוזל קירור ורצועות 240,000 (או 5/10 שנים). סבב צמיגים כל 12,000.'))

# Chevrolet Traverse 2025-2026 2.5T LK0 (2025 manual)
rows = base_rows(air_inspect=True, halfshaft=True) + [
 ('cabin_filter','replace',[36000,72000,108000,144000,180000,216000],'או כל 24 חודשים'),
 ('spark_plugs','replace',[96000,192000]),
]
write(dict(id='chevrolet-traverse-2025-2026-2.5t', make='Chevrolet', make_he='שברולט', model='Traverse', model_he='טראוורס', generation='דור 3', years=[2025,2026],
 engines=['2.5 טורבו (LK0)'], fuel='petrol', importer=UMI, interval=INTERVAL, cycle_km=240000, services=grid(12000,240000,rows),
 long_interval=[
   dict(item='coolant', action='replace', every_km=240000, every_months=72, note='240,000 ק"מ או 6 שנים'),
   dict(item='differential_oil', action='replace', every_km=240000, note='סרן אחורי, הנעה כפולה; בשימוש קשה כל 120,000'),
   dict(item='transmission_oil', action='replace', every_km=72000, note='שימוש קשה בלבד'),
 ],
 time_based=[dict(item='brake_fluid', action='replace', months=60, note='כל 5 שנים'), dict(item='ac_refrigerant', action='replace', months=84, note='החלפת סופח הלחות של המזגן כל 7 שנים')],
 specs=dict(engine_oil='dexos1 סינתטי', coolant='DEX-COOL', brake_fluid='DOT 4', _note='מטבלת הנוזלים בספר 2025 (עמ\' 335)'),
 sources=[dict(url=CDN+'chevrolet/2025-traverse.pdf', kind='manufacturer', note='2025 Chevrolet Traverse Owner\'s Manual, Maintenance Schedule עמ\' 330-333 (עמודי PDF 331-334)'),
          dict(url=CDN+'chevrolet/2026-traverse.pdf', kind='manufacturer', note='ספר 2026 הורד לבדיקה')],
 status='draft', notes=NOTE_US + 'מסנן האוויר מוחלף לפי מחוון חיי המסנן ברכב. מסנן מיזוג כל 36,000 ק"מ או שנתיים, מצתים כל 96,000, תומכי גז ב-161,000 או 10 שנים, שמן סרן אחורי ונוזל קירור ב-240,000 (נוזל קירור או 6 שנים), נוזל בלמים כל 5 שנים.'))

# Chevrolet Aveo (F14D3) / Optra (F16D3), from 2008 US Aveo (1.6 E-TEC II) long-trip schedule
def ev(n): return lambda k: k % n == 0
rows = [
 ('engine_oil','replace','all','או כל 12 חודשים; בנסיעות קצרות/עירוניות כל 5,000 ק"מ או 3 חודשים'),
 ('oil_filter','replace','all'),
 ('tire_rotation','rotate','all','זמן טוב גם לבדיקת הבלמים'),
 ('cabin_filter','replace',ev(25000)),
 ('air_filter','inspect',lambda k: k%25000==0 and k%50000!=0),
 ('air_filter','replace',ev(50000)),
 ('drive_belt','inspect',ev(25000)),
 ('spark_plugs','replace',ev(50000)),
 ('evap_system','inspect',ev(50000),'מיכל פחם, צנרת אדים ושסתום אוורור'),
 ('pcv_valve','inspect',ev(50000)),
]
svc = grid(12500,150000,rows)
for s in svc:
    if s['km'] == 150000:
        s['items'] += [{'item':'fuel_filter','action':'replace'}]
write(dict(id='chevrolet-aveo-optra-2004-2010-1.4-1.6', make='Chevrolet', make_he='שברולט', model='Aveo / Optra', model_he='אווו / אופטרה', generation='T200/T250 (Aveo), J200 (Optra)', years=[2004,2010],
 engines=['1.4 (F14D3)', '1.6 (F16D3)'], fuel='petrol', importer=UMI,
 interval=dict(km=12500, months=12, note='לוח "נסיעות ארוכות/כביש" בספר הנהג האמריקאי של אווו 2008: כל 12,500 ק"מ או 12 חודשים. לוח "נסיעות קצרות/עיר" (רוב הנסיעות קצרות, עמידה בפקקים, מונית): שמן כל 5,000 ק"מ או 3 חודשים'),
 cycle_km=150000, services=svc,
 long_interval=[
  dict(item='timing_belt', action='replace', every_km=100000),
  dict(item='evap_system', action='replace', every_km=100000, note='החלפת שסתום הסולנואיד של מערכת אדי הדלק; באותו מועד גם החלפת כבלי המצתים'),
  dict(item='coolant', action='replace', every_km=240000, note='ניקוז, שטיפה ומילוי (DEX-COOL)'),
  dict(item='transmission_oil', action='replace', every_km=62500, note='גיר אוטומטי, רק בשימוש קשה (חום ופקקים, הרים, מונית)'),
 ],
 time_based=[],
 specs=dict(timing='רצועת תזמון - החלפה כל 100,000 ק"מ', _note='טיוטה'),
 sources=[dict(url=CDN+'chevrolet/2008-aveo.pdf', kind='manufacturer', note='2008 Chevrolet Aveo Owner Manual (GM, ארה"ב/קנדה), Maintenance Schedule עמ\' 6-4 עד 6-17 (עמודי PDF 328-341): סיכום מרווחים בעמ\' 6-5/6-6 ולוח Long Trip/Highway. המנוע האמריקאי הוא 1.6 E-TEC II (F16D3)')],
 status='draft', notes='טיוטה מספר הנהג האמריקאי של אווו 2008 (מנוע 1.6 E-TEC II, אותו מנוע של אופטרה F16D3 ומאותה משפחה של ה-1.4 F14D3 באווו הישראלית). לא נמצא ספר עברי (אתר יו.אם.איי חסום). לוח כביש: שמן וסבב צמיגים כל 12,500 ק"מ; מסנן מיזוג ובדיקת רצועות כל 25,000; מסנן אוויר, מצתים, אדי דלק ו-PCV כל 50,000; רצועת תזמון וכבלי מצתים ב-100,000; מסנן דלק ב-150,000; נוזל קירור ב-240,000. בנהיגה עירונית הספר דורש שמן כל 5,000 ק"מ או 3 חודשים.'))
