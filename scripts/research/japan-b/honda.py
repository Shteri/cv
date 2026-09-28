import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/dl/japan-b')
from gen import *
IMP = 'מאיר (הונדה ישראל)'
BLOCK = 'honda.co.il (כולל /guide_books/ ו-wp-json) חסום ב-Cloudflare (403); לא נמצא ספר ישראלי, לכן לוח "Except EU" מספר בעלים באנגלית'
def hs(id_, model, model_he, gen, years, engines, cycle=200000):
    s = S(id_, 'Honda', 'הונדה', model, model_he, gen, years, engines, 'petrol', IMP, 10000, 12,
          'לפי לוח "Maintenance Schedule (Except EU)": שמן מנוע כל 10,000 ק"מ או שנה; בתנאים מחמירים כל 5,000 ק"מ או 6 חודשים', cycle)
    s.every('engine_oil', 'replace', 10000)
    for k in range(10000, cycle + 1, 10000):
        for it in ('brake_pads', 'brake_discs', 'steering', 'suspension', 'cv_boots'): s.add(k, it, 'inspect')
        s.add(k, 'tire_rotation', 'rotate', 'סבב צמיגים כל 10,000 ק"מ')
    for k in range(20000, cycle + 1, 20000):
        for it in ('brake_lines', 'exhaust', 'fuel_lines'): s.add(k, it, 'inspect')
    s.time('brake_fluid', 'replace', 36, 'כל 3 שנים, בלי קשר לק"מ')
    s.li('coolant', 'replace', first_km=200000, first_months=120, then_every_km=100000, then_every_months=60)
    return s
ML = 'https://www.manualslib.com/manual/{}/x.html?page={}'

# Civic 8th gen (FN hatch manual; FD sedan same R18A engine)
s = hs('honda-civic-2006-2011-1.8', 'Civic', 'סיוויק', 'FD/FN (דור 8)', (2006, 2011), ['1.8 i-VTEC (R18A)'])
s.every('oil_filter', 'replace', 20000, 'בתנאים מחמירים כל 10,000 ק"מ')
s.every('air_filter', 'replace', 20000, 'מסנן מסוג יבש: ניקוי כל 10,000 ק"מ')
s.every('valve_clearance', 'inspect', 40000)
s.add(160000, 'fuel_filter', 'replace', 'מסומן ב-160,000 ק"מ')
s.add(100000, 'spark_plugs', 'replace'); s.li('spark_plugs', 'replace', every_km=100000, note='מצתי אירידיום')
s.every('drive_belt', 'inspect', 40000)
s.add(120000, 'diagnostics', 'inspect', 'בדיקת סל"ד סרק')
s.add(120000, 'manual_gearbox_oil', 'replace', 'גיר ידני / i-SHIFT: בתנאים רגילים ב-120,000; בתנאים מחמירים ב-60,000, 120,000, 180,000')
s.every('parking_brake', 'inspect', 20000); s.every('cabin_filter', 'replace', 20000, 'מסנן אבק ואבקנים')
s.src(ML.format(822871, 360), 'manufacturer', 'Honda Civic 5D owner\'s manual (32SMG610, 2006), "Maintenance Schedule for Petrol Models (Except EU)", עמודי ספר 357-359 (manualslib עמודים 360-362); עותק עם סימן מים שמסתיר חלק מהנקודות בשורות בלם החניה ומסנן האבק')
s.src('https://honda.co.il/guide_books/', 'importer', BLOCK)
s.write('draft', 'טיוטה מלוח "Except EU" בספר הבעלים הבינלאומי של סיוויק 5 דלתות (2006). הסדאן (FD, מתוצרת טורקיה/יפן) חולקת את המנוע R18A, ולכן הלוח משמש גם לה. שמן כל 10,000 ק"מ או שנה, מסנן שמן ומסנן אוויר כל 20,000, בדיקת שסתומים כל 40,000, מצתים כל 100,000, נוזל בלמים כל 3 שנים, נוזל קירור ב-200,000 או 10 שנים. בשורות בלם החניה ומסנן האבק חלק מהנקודות מוסתרות; נרשם כל 20,000 לפי הנקודות הרצופות שנראות.')
rule('Honda', ['CIVIC', 'CIVIC HYBRID'], (2006, 2011), s.d['id'], engine_codes=['R-18-A-2', 'R18A2', 'R-18-A-1', 'R18A1', 'R18A'])

# Civic 9th gen FB/FK
s = hs('honda-civic-2012-2016-1.8', 'Civic', 'סיוויק', 'FB/FK (דור 9)', (2012, 2016), ['1.8 i-VTEC (R18Z1/R18Z4)'])
s.every('oil_filter', 'replace', 20000, 'בתנאים מחמירים כל 10,000 ק"מ או 6 חודשים')
s.every('air_filter', 'replace', 30000, 'כל 30,000 ק"מ')
s.every('valve_clearance', 'inspect', 40000)
s.at('fuel_filter', 'replace', [80000, 160000])
s.add(100000, 'spark_plugs', 'replace'); s.li('spark_plugs', 'replace', every_km=100000)
s.every('drive_belt', 'inspect', 40000)
s.add(120000, 'diagnostics', 'inspect', 'בדיקת סל"ד סרק')
s.add(120000, 'manual_gearbox_oil', 'replace', 'גיר ידני: ב-120,000 (בתנאים מחמירים ב-60,000, 120,000, 180,000)')
s.li('transmission_oil', 'replace', first_km=120000, first_months=72, then_every_km=80000, then_every_months=48, note='גיר אוטומטי; בתנאים מחמירים לראשונה ב-60,000 או 3 שנים ואחר כך כל 40,000 או שנתיים')
s.at('parking_brake', 'inspect', [20000, 40000, 80000, 120000, 160000, 200000])
s.every('cabin_filter', 'replace', 20000, 'מסנן אבק ואבקנים')
s.src(ML.format(2119749, 313), 'manufacturer', 'Honda Civic 4D owner\'s manual (32TR0600, 2011), "Maintenance Schedule - Except European, South African and New Zealand models", עמודי ספר 312-313 (manualslib 313-314)')
s.src('https://honda.co.il/guide_books/', 'importer', BLOCK)
s.write('draft', 'טיוטה מלוח "חוץ מאירופה, דרום אפריקה וניו זילנד" בספר הבעלים של סיוויק 4 דלתות (2012). ההאצ\'בק FK והטורר (R18Z4) הם אותו דור ואותה משפחת מנוע. מסנן אוויר כל 30,000, מסנן דלק ב-80,000 וב-160,000, גיר אוטומטי לראשונה ב-120,000 ואחר כך כל 80,000.')
rule('Honda', ['CIVIC', 'CIVIC TOURER'], (2012, 2017), s.d['id'], engine_codes=['R18Z1', 'R18Z4', 'R18Z'])

# Jazz GK
s = hs('honda-jazz-2015-2020-1.3', 'Jazz', "ג'אז", 'GK (דור 3)', (2015, 2020), ['1.3 i-VTEC (L13B)'])
s.every('oil_filter', 'replace', 20000, 'כל 20,000 ק"מ או שנתיים; בתנאים מחמירים כל 10,000 או שנה')
s.every('air_filter', 'replace', 30000)
s.li('valve_clearance', 'inspect', every_km=120000, note='בדיקה לפי רעש; כיוון ב-120,000 אם יש רעש')
s.at('fuel_filter', 'replace', [80000, 160000])
s.add(100000, 'spark_plugs', 'replace'); s.li('spark_plugs', 'replace', every_km=100000)
s.every('drive_belt', 'inspect', 40000)
s.every('cvt_oil', 'replace', 40000, 'גיר CVT')
s.li('manual_gearbox_oil', 'replace', every_km=120000, every_months=72, note='גיר ידני')
s.at('parking_brake', 'inspect', [20000, 40000, 80000, 120000, 160000, 200000])
s.every('cabin_filter', 'replace', 20000, 'מסנן אבק ואבקנים')
s.src(ML.format(1445713, 485), 'manufacturer', 'Honda Fit/Jazz 2018 owner\'s manual (32T5A6100), "Maintenance Schedule - Models without Service Book", עמודי ספר 484-485 (manualslib 485-486)')
s.src('https://honda.co.il/guide_books/', 'importer', BLOCK)
s.write('draft', "טיוטה מלוח \"דגמים ללא ספר שירות\" בספר הבעלים הבינלאומי של ג'אז 2018 (דור GK). שמן כל 10,000 ק\"מ או שנה, מסנן שמן כל 20,000, מסנן אוויר כל 30,000, נוזל CVT כל 40,000, מסנן דלק ב-80,000 וב-160,000.")
rule('Honda', ['JAZZ'], (2014, 2020), s.d['id'], engine_codes=['L13B2', 'L13B', 'L15B'])
save_rules('rules_honda.json')
