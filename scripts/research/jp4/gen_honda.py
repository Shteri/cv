import sys; sys.path.insert(0,'.')
from gen import *
IMP='מאיר (הונדה ישראל)'
URL='https://www.manua.ls/honda/jazz-2010/manual?p=324'
s=S('honda-jazz-2008-2014-1.2-1.3','Honda','הונדה','Jazz',"ג'אז",'GE (דור שני)',(2008,2014),['1.2 i-VTEC (L12B1)','1.3 i-VTEC (L13Z1)'],'petrol',IMP,
    10000,12,'לפי לוח "On vehicles without Service Book": שמן מנוע כל 10,000 ק"מ או שנה; בתנאים קשים (כולל נסיעה בחום מעל 35 מעלות) שמן כל 5,000 ק"מ או 6 חודשים ומסנן כל 10,000',200000)
s.every('engine_oil','replace',10000,'כל 10,000 ק"מ או שנה')
s.every('oil_filter','replace',20000,'בתנאים קשים כל 10,000 ק"מ או 6 חודשים')
s.every('air_filter','replace',30000)
s.every('valve_clearance','inspect',40000)
s.at('fuel_filter','replace',[80000,160000])
s.every('spark_plugs','replace',100000,'מצתי אירידיום')
s.every('drive_belt','inspect',40000)
s.at('diagnostics','inspect',[120000],'בדיקת סיבובי סרק')
s.every('cvt_oil','replace',40000,'גיר CVT בלבד')
s.every('brake_pads','inspect',10000,'בלמים קדמיים ואחוריים')
s.every('brake_discs','inspect',10000)
s.at('parking_brake','adjust',[20000,40000,80000,120000,160000,200000],'בדיקת כיוון בלם החניה')
s.every('cabin_filter','replace',20000,'מסנן אבק ואבקנים')
s.every('tire_rotation','rotate',10000)
s.every('steering','inspect',10000,'קצוות מוטות הגה, תיבת הגה וגומיות (או כל 6 חודשים)')
s.every('suspension','inspect',10000,'או כל 6 חודשים')
s.every('cv_boots','inspect',10000,'או כל 6 חודשים')
s.every('brake_lines','inspect',20000,'כולל צנרת ABS')
s.every('exhaust','inspect',20000)
s.every('fuel_lines','inspect',20000)
s.li('coolant','replace',first_km=200000,first_months=120,then_every_km=100000,then_every_months=60)
s.li('manual_gearbox_oil','replace',every_km=120000,every_months=72,note='גיר ידני; בתנאים קשים (חום מעל 35 מעלות, גרירה או הרים) כל 60,000 ק"מ')
s.time('brake_fluid','replace',36,'כל 3 שנים, בלי קשר לק"מ')
s.src(URL,'manufacturer','Honda Jazz owner\'s manual (אירופה, 32TF0630, 2010), "Maintenance Schedule (On vehicles without Service Book)", עמודי ספר 319-322 (manua.ls p.324-327). באותו ספר יש גם לוח לרוסיה (p.326) במרווח 15,000 ק"מ')
s.src('https://honda.co.il/guide_books/','importer','honda.co.il חסום ב-Cloudflare (403); לא נמצא ספר ישראלי')
notes=('טיוטה מלוח "לרכבים ללא ספר שירות" בספר הבעלים האירופי של ג\'אז דור שני (2010). '
       'שמן כל 10,000 ק"מ או שנה, מסנן שמן ומסנן מזגן כל 20,000, מסנן אוויר כל 30,000, בדיקת שסתומים ורצועת עזר כל 40,000, נוזל CVT כל 40,000, מסנן דלק ב-80,000 וב-160,000, '
       'מצתי אירידיום כל 100,000, נוזל בלמים כל 3 שנים ונוזל קירור לראשונה ב-200,000 ק"מ או 10 שנים. '
       'הספר מגדיר נסיעה בחום מעל 35 מעלות, נסיעות קצרות ועמידה ממושכת בפקקים כתנאים קשים, ואז שמן כל 5,000 ק"מ או 6 חודשים ומסנן כל 10,000. בקיץ הישראלי כדאי לשקול זאת.')
s.write('draft',notes)
rule('Honda',['JAZZ'],(2008,2015),'honda-jazz-2008-2014-1.2-1.3',engine_codes=['L13Z1','L-13-Z-1','L12B1','L-12-B-1'])
save_rules('rules_honda.json')
