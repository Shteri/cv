import sys, re
sys.path.insert(0, '../gm')
from boxparse import boxes
from lib import write
GM = '../gm/'
CDN = 'https://cdn.dealereprocess.org/cdn/servicemanuals/'
MAP = [  # (regex, item, action, note)
 (r'^Change the engine oil', [('engine_oil','replace',None),('oil_filter','replace',None)]),
 (r'^Rotate', [('tire_rotation','rotate',None)]),
 (r'Dusty or off-road', [('air_filter','inspect','בתנאי אבק או שטח')]),
 (r'^Replace the engine air cleaner', [('air_filter','replace',None)]),
 (r'air conditioning filter', [('cabin_filter','replace',None)]),
 (r'brake linings', [('brake_pads','inspect','חיפויי בלמים')]),
 (r'CV [Jj]oints', [('cv_boots','inspect','מפרקי CV')]),
 (r'exhaust', [('exhaust','inspect',None)]),
 (r'front suspension', [('suspension','inspect','מתלה קדמי, קצוות מוטות היגוי ואטמים')]),
 (r'parking brake', [('parking_brake','adjust','בבלמי דיסק בארבעת הגלגלים')]),
 (r'^Replace the spark plugs', [('spark_plugs','replace',None)]),
 (r'spark plugs \(3\.3L, 3\.8L', [('spark_plugs','replace','מנועי 3.3/3.8')]),
 (r'ignition cables', [('spark_plugs','inspect','החלפת כבלי הצתה (3.3/3.8)')]),
 (r'PCV', [('pcv_valve','inspect',None)]),
 (r'PTU', [('transfer_case_oil','replace','יחידת PTU, הנעה כפולה')]),
 (r'RDA', [('differential_oil','replace','יחידת הנעה אחורית RDA, הנעה כפולה')]),
 (r'accessory drive belt', [('drive_belt','replace',None)]),
 (r'^Change the automatic transmission fluid( &| and) filter\.?$', [('transmission_oil','replace','והחלפת מסנן')]),
]
SKIP = [r'if using your vehicle for any of the following: police', r'manual transmission fluid if', r'coolant', r'timing belt \(4\.0L', r'transmission fluid & filter if', r'transmission fluid and filter if']
def build(f, interval_km, cycle):
    pr, out = boxes(GM + f)
    services = []
    for km, mo, items in out:
        if km > cycle or km % interval_km: continue
        its = []
        for t in items:
            if any(re.search(s, t, re.I) for s in SKIP): continue
            hit = False
            for rx, lst in MAP:
                if re.search(rx, t):
                    for it, ac, note in lst:
                        d = {'item': it, 'action': ac}
                        if note: d['note'] = note
                        its.append(d)
                    hit = True; break
            if not hit: print('UNMAPPED', km, t[:90])
        services.append({'km': km, 'items': its})
    return pr, services

# Grand Voyager / T&C 2008-2010 3.8 (EGL)
pr, svc = build('chrysler_2010-townandcountry.pdf', 10000, 250000)
for s in svc: 
    for it in s['items']:
        if it['item']=='engine_oil': it['note']='לפי מחוון החלפת השמן, ולא יותר מ-10,000 ק"מ או 6 חודשים'
write(dict(id='chrysler-grand-voyager-2008-2010-3.8', make='Chrysler', make_he='קרייזלר', model='Grand Voyager / Town & Country', model_he='גרנד וויאג\'ר', generation='RT', years=[2008,2011],
 engines=['3.8 V6 (EGL)'], fuel='petrol', importer='סמלת',
 interval=dict(km=10000, months=6, note='לפי ספר הנהג האמריקאי 2010: שמן ומסנן לפי מחוון החלפת השמן, ולא יותר מ-10,000 ק"מ או 6 חודשים'),
 cycle_km=250000, services=svc,
 long_interval=[dict(item='coolant', action='replace', first_months=60, first_km=170000, then_every_km=170000, then_every_months=60, note='5 שנים או 170,000 ק"מ, המוקדם'),
                dict(item='transmission_oil', action='replace', every_km=100000, note='שימוש משטרה, מונית, צי או גרירה תכופה; בשימוש רגיל ב-200,000')],
 time_based=[],
 specs=dict(_note='טיוטה'),
 sources=[dict(url=CDN+'chrysler/2010-townandcountry.pdf', kind='manufacturer', note=f'2010 Chrysler Town & Country Owner\'s Manual (ארה"ב), Maintenance Schedules (עמודי PDF {pr[0]}-{pr[1]}): טיפולים כל 6,000 מייל (10,000 ק"מ) עד 250,000 ק"מ')],
 status='draft', notes='טיוטה מספר הנהג האמריקאי של Town & Country 2010 (מנוע 3.8, קוד רישוי EGL). לא נמצא ספר עברי. שמן וסבב צמיגים כל 10,000 ק"מ; מסנן מיזוג, בלמים ומתלה כל 20,000; מפרקי CV ופליטה ב-20,000 ואז כל 40,000; מסנן אוויר כל 50,000; PCV ב-150,000; מצתים וכבלים ב-170,000; רצועות ושמן גיר ב-200,000; נוזל קירור 5 שנים או 170,000.'))

# Jeep Patriot / Dodge Caliber 2.0/2.4 World Engine (2010 manuals, identical schedules)
pr, svc = build('jeep_2010-patriot.pdf', 10000, 250000)
pr2, svc2 = build('dodge_2010-caliber.pdf', 10000, 250000)
same = [[(i['item'],i['action']) for i in a['items']] for a in svc] == [[(i['item'],i['action']) for i in a['items']] for a in svc2]
print('patriot vs caliber identical apart from AWD PTU/RDA rows:', same)
for s in svc:
    for it in s['items']:
        if it['item']=='engine_oil': it['note']='לפי מחוון החלפת השמן, ולא יותר מ-10,000 ק"מ או 6 חודשים'
write(dict(id='jeep-patriot-dodge-caliber-2007-2012-2.0-2.4', make='Chrysler', make_he='ג\'יפ / דודג\' (קרייזלר)', model='Patriot / Caliber', model_he='פטריוט / קאליבר', generation='MK / PM', years=[2007,2012],
 engines=['2.0 (World Engine, ECN)', '2.4 (World Engine, ED3)'], fuel='petrol', importer='סמלת',
 interval=dict(km=10000, months=6, note='לפי ספרי הנהג האמריקאיים 2010: שמן ומסנן לפי מחוון החלפת השמן, ולא יותר מ-10,000 ק"מ או 6 חודשים'),
 cycle_km=250000, services=svc,
 long_interval=[dict(item='coolant', action='replace', first_months=60, first_km=170000, then_every_km=170000, then_every_months=60, note='5 שנים או 170,000 ק"מ, המוקדם'),
                dict(item='transmission_oil', action='replace', every_km=100000, note='אוטומטי/CVT בשימוש משטרה, מונית, צי או גרירה; בשימוש רגיל ב-200,000'),
                dict(item='manual_gearbox_oil', action='replace', every_km=80000, note='גיר ידני רק בשימוש קשה (גרירה, עומס, מונית)')],
 time_based=[],
 specs=dict(_note='טיוטה'),
 sources=[dict(url=CDN+'jeep/2010-patriot.pdf', kind='manufacturer', note=f'2010 Jeep Patriot Owner\'s Manual (ארה"ב), Maintenance Schedules (עמודי PDF {pr[0]}-{pr[1]})'),
          dict(url=CDN+'dodge/2010-caliber.pdf', kind='manufacturer', note=f'2010 Dodge Caliber Owner\'s Manual (ארה"ב), Maintenance Schedules (עמודי PDF {pr2[0]}-{pr2[1]}) - אותו לוח')],
 status='draft', notes='טיוטה מספרי הנהג האמריקאיים 2010 של פטריוט וקאליבר (לוח זהה, מנועי World Engine 2.0/2.4). לא נמצא ספר עברי. שמן וסבב צמיגים כל 10,000 ק"מ; מסנן מיזוג, בלמים ומתלה כל 20,000; מפרקי CV ופליטה ב-20,000 ואז כל 40,000; מסנן אוויר ומצתים כל 50,000; שמן PTU/RDA ב-100,000 (הנעה כפולה); PCV ב-150,000; רצועות ושמן גיר ב-200,000; נוזל קירור 5 שנים או 170,000.'))
