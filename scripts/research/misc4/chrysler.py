from lib import grid, write
CDN = 'https://cdn.dealereprocess.org/cdn/servicemanuals/'
IMP = 'סמלת'
def every(n): return lambda k: k % n == 0

# Chrysler Grand Voyager / Town & Country 3.6 (2014 US manual)
cv = [48000,96000,144000,192000,240000]
fs = [32000,64000,96000,128000,160000,192000,224000]
rows = [
 ('engine_oil','replace','all','לפי מחוון החלפת השמן, ולא יותר מ-16,000 ק"מ או 12 חודשים'),
 ('oil_filter','replace','all'),
 ('tire_rotation','rotate','all'),
 ('battery_12v','inspect','all','ניקוי והידוק הדקים'),
 ('brake_pads','inspect','all','רפידות, דיסקים ותופים'),
 ('brake_lines','inspect','all'),
 ('parking_brake','inspect','all'),
 ('coolant','inspect','all','רמת הגנה'),
 ('coolant_hoses','inspect','all'),
 ('exhaust','inspect','all'),
 ('cv_boots','inspect',cv,'מפרקי CV'),
 ('suspension','inspect',fs,'מתלה קדמי, קצוות מוטות היגוי ואטמי גומי'),
 ('brake_pads','inspect',fs,'בדיקת עובי חיפויי בלמים'),
 ('air_filter','replace',cv),
 ('cabin_filter','replace',fs),
 ('spark_plugs','replace',[160000],'לפי ק"מ בלבד'),
 ('pcv_valve','inspect',[160000]),
 ('transmission_oil','replace',[192000],'והחלפת מסנן'),
]
write(dict(id='chrysler-grand-voyager-2011-2017-3.6', make='Chrysler', make_he='קרייזלר', model='Grand Voyager / Town & Country', model_he='גרנד וויאג\'ר', generation='RT', years=[2011,2017],
 engines=['3.6 V6 Pentastar'], fuel='petrol', importer=IMP,
 interval=dict(km=16000, months=12, note='לפי ספר הנהג האמריקאי: שמן ומסנן לפי מחוון החלפת השמן, ולא יותר מ-16,000 ק"מ או 12 חודשים; בשימוש קשה (אבק ושטח) כל 6,500 ק"מ'),
 cycle_km=240000, services=grid(16000,240000,rows),
 long_interval=[dict(item='coolant', action='replace', every_km=240000, every_months=120, note='10 שנים או 240,000 ק"מ, המוקדם (OAT)'),
                dict(item='transmission_oil', action='replace', every_km=96000, note='שימוש משטרה, מונית, צי או גרירה תכופה')],
 time_based=[],
 specs=dict(engine_oil='SAE 5W-20 לפי MS-6395', coolant='MOPAR OAT 10 שנים/150,000 מייל (MS-12106)', brake_fluid='DOT 3 (או DOT 4)', _note='מטבלת הנוזלים בספר 2014 (עמ\' 659-660)'),
 sources=[dict(url=CDN+'chrysler/2014-townandcountry.pdf', kind='manufacturer', note='2014 Chrysler Town & Country Owner\'s Manual (ארה"ב), Maintenance Schedules עמ\' 662-666 (עמודי PDF 664-668); הטבלה נקראה מתמונת העמודים')],
 status='draft', notes='טיוטה מספר הנהג האמריקאי של Town & Country (הגרנד וויאג\'ר האירופי/ישראלי הוא אותו רכב עם מנוע 3.6). לא נמצא ספר עברי של היבואן. הטבלה מתחילה ב-32,000 ק"מ; בכל טיפול: שמן, סבב צמיגים ובדיקות. מסנן מיזוג, מתלה ובלמים כל 32,000; מסנן אוויר ומפרקי CV כל 48,000; מצתים ובדיקת PCV ב-160,000; שמן גיר ב-192,000 (בשימוש קשה ב-96,000); נוזל קירור 10 שנים או 240,000.'))

# Dodge Journey 2.4 / 3.6 (2012 US manual)
rows = [
 ('engine_oil','replace','all','לפי מחוון החלפת השמן, ולא יותר מ-13,000 ק"מ או 6 חודשים'),
 ('oil_filter','replace','all'),
 ('tire_rotation','rotate','all'),
 ('cabin_filter','replace',every(26000)),
 ('brake_pads','inspect',every(26000),'חיפויי בלמים'),
 ('suspension','inspect',every(26000),'מתלה קדמי, קצוות מוטות היגוי ואטמים'),
 ('air_filter','inspect',lambda k: k%26000==0 and k%52000!=0,'בתנאי אבק/שטח'),
 ('air_filter','replace',every(52000)),
 ('spark_plugs','replace',every(52000),'מנוע 2.4'),
 ('cv_boots','inspect',every(39000),'מפרקי CV'),
 ('exhaust','inspect',lambda k: k==26000 or k%39000==0),
 ('differential_oil','replace',[104000,208000],'יחידת הנעה אחורית (RDA), הנעה כפולה'),
 ('transfer_case_oil','replace',[104000,208000],'יחידת העברת כוח (PTU), הנעה כפולה'),
 ('spark_plugs','replace',[156000],'מנוע 3.6'),
 ('pcv_valve','inspect',[156000]),
 ('transmission_oil','replace',[195000],'והחלפת מסננים'),
]
write(dict(id='dodge-journey-2008-2014-2.4-3.6', make='Chrysler', make_he='דודג\' (קרייזלר)', model='Journey', model_he='ג\'רני', generation='JC', years=[2008,2014],
 engines=['2.4 (World Engine)', '3.6 V6 Pentastar'], fuel='petrol', importer=IMP,
 interval=dict(km=13000, months=6, note='לפי ספר הנהג האמריקאי 2012: שמן ומסנן לפי מחוון החלפת השמן, ולא יותר מ-13,000 ק"מ (8,000 מייל) או 6 חודשים'),
 cycle_km=247000, services=grid(13000,247000,rows),
 long_interval=[dict(item='coolant', action='replace', first_months=60, first_km=169000, then_every_km=169000, then_every_months=60, note='5 שנים או 169,000 ק"מ (104,000 מייל), המוקדם'),
                dict(item='transmission_oil', action='replace', every_km=104000, note='שימוש משטרה, מונית, צי או גרירה תכופה')],
 time_based=[],
 specs=dict(engine_oil='לפי MS-6395', brake_fluid='DOT 3 (או DOT 4)', _note='מטבלת הנוזלים בספר 2012'),
 sources=[dict(url=CDN+'dodge/2012-journey.pdf', kind='manufacturer', note='2012 Dodge Journey Owner\'s Manual (ארה"ב), Maintenance Schedules עמ\' 552-575 (עמודי PDF 554-580): טיפולים כל 8,000 מייל (13,000 ק"מ) עד 247,000 ק"מ')],
 status='draft', notes='טיוטה מספר הנהג האמריקאי של דודג\' ג\'רני 2012; לא נמצא ספר עברי. הק"מ כפי שמופיעים בספר (13,000, 26,000...). מסנן מיזוג, בלמים ומתלה כל 26,000; מסנן אוויר ומצתים (2.4) כל 52,000; מפרקי CV ומערכת פליטה כל 39,000; שמן PTU ו-RDA ב-104,000 (הנעה כפולה); מצתים 3.6 ו-PCV ב-156,000; שמן גיר ב-195,000; נוזל קירור 5 שנים או 169,000. טבלת 2012 משמשת גם לשנים 2008-2014 (לא נבדק).'))

# Chrysler Pacifica 3.6 (2019 US manual)
e32 = [32000*i for i in range(1,8)]
rows = [
 ('engine_oil','replace','all','לפי מחוון החלפת השמן, ולא יותר מ-16,000 ק"מ או 12 חודשים'),
 ('oil_filter','replace','all'),
 ('tire_rotation','rotate','all'),
 ('battery_12v','inspect','all','ניקוי והידוק הדקים'),
 ('brake_pads','inspect','all','רפידות, דיסקים, צינורות ובלם חניה'),
 ('coolant','inspect','all','רמת הגנה'),
 ('coolant_hoses','inspect','all'),
 ('exhaust','inspect','all'),
 ('cv_boots','inspect',e32,'מפרקי CV'),
 ('suspension','inspect',e32,'מתלה קדמי, אטמים וקצוות מוטות היגוי'),
 ('parking_brake','inspect',e32),
 ('air_filter','replace',[48000,96000,144000,192000,240000]),
 ('cabin_filter','replace',e32),
 ('spark_plugs','replace',[160000],'לפי ק"מ בלבד'),
 ('pcv_valve','inspect',[160000]),
 ('drive_belt','inspect',[240000],'כולל מותח וגלגלת'),
]
write(dict(id='chrysler-pacifica-2017-2026-3.6', make='Chrysler', make_he='קרייזלר', model='Pacifica', model_he='פסיפיקה', generation='RU', years=[2017,2026],
 engines=['3.6 V6 Pentastar'], fuel='petrol', importer=IMP,
 interval=dict(km=16000, months=12, note='לפי ספר הנהג האמריקאי 2019: שמן ומסנן לפי מחוון החלפת השמן, ולא יותר מ-16,000 ק"מ או 12 חודשים; בשימוש קשה כל 6,500 ק"מ'),
 cycle_km=240000, services=grid(16000,240000,rows),
 long_interval=[dict(item='coolant', action='replace', every_km=240000, every_months=120, note='10 שנים או 240,000 ק"מ, המוקדם')],
 time_based=[],
 specs=dict(_note='טיוטה'),
 sources=[dict(url=CDN+'chrysler/2019-pacifica.pdf', kind='manufacturer', note='2019 Chrysler Pacifica Owner\'s Manual (ארה"ב), Scheduled Servicing / Maintenance Plan עמ\' 509-511 (עמודי PDF 511-513); הטבלה נקראה מתמונת העמוד')],
 status='draft', notes='טיוטה מספר הנהג האמריקאי של פסיפיקה (בנזין, לא היברידית); לא נמצא ספר עברי. הטבלה מתחילה ב-32,000 ק"מ. מסנן מיזוג, מפרקי CV, מתלה ובלמים כל 32,000; מסנן אוויר כל 48,000; מצתים ו-PCV ב-160,000; רצועת עזר ונוזל קירור ב-240,000 (נוזל קירור או 10 שנים).'))
