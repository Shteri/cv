from build import *
HY={'make':'Hyundai','make_he':'יונדאי','importer':'כלמוביל'}
A8='IIIIIIII'; E8='-I-I-I-I'
common=[('air_filter','IRIRIRIR'),('ac_system',A8),('ac_refrigerant',A8),('battery_12v',A8),('brake_lines','IIIII-II'),('electrical_system',A8),
 ('brake_pads',A8),('brake_discs',A8),('cv_boots',A8),('exhaust',A8),('suspension',A8,'מפרקים כדוריים קדמיים'),('parking_brake',A8),
 ('power_steering_fluid',A8,'נוזל וצינורות הגה כוח'),('propshaft',A8,'אם קיים'),('steering',A8),('tires',A8),('manual_gearbox_oil',E8,'אם קיים'),
 ('transfer_case_oil',E8,'הנעה כפולה'),('differential_oil',E8,'הנעה כפולה'),('evap_system',E8,'צינור אדי דלק ופתח מילוי הדלק'),
 ('brake_fluid','RRRRRRRR'),('cabin_filter','RRRRRRRR'),('cooling_system','-IIIIIII','בדיקה ראשונה ב-60,000 ואחר כך כל 30,000'),
 ('drive_belt','--IIIIII','בדיקה ראשונה ב-90,000 ואחר כך כל 30,000')]
petrol=[('fuel_filter','-I-IIII-I'[:0] or '-I-III-I'),('fuel_tank_air_filter',E8,'אם קיים'),('fuel_lines','----IIII'),
 ('vacuum_hose',A8,'צינור ואקום ל-EGR ולגוף המצערת'),('valve_clearance','--I--I--')]
diesel=[('fuel_filter','IRIRIRIR','מחסנית מסנן הסולר; המרווח תלוי באיכות הסולר (EN590)'),('fuel_lines',A8),('vacuum_hose','I-------','צינור ואקום ל-EGR ולגוף המצערת (בספר מופיע בטיפול 30,000 בלבד)')]
oil={km:lst(('engine_oil','R'),('oil_filter','R')) for km in range(15000,240001,15000)}
SRC=[{'url':'https://www.hyundaimotors.co.il/maintenance/','kind':'importer','note':"ספר הרכב העברי של כלמוביל לסנטה פה 2013-2018 (קובץ מקומי hy-santafe-2013-2018.pdf, 'SANTA FE-0', 2013), פרק 7 עמ' 10-21 (עמודי PDF 409-420): רשימות מצטברות לכל 30,000 ק\"מ ולוח תנאים קשים"}]
COOL={'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24}
write({**HY,'id':'hyundai-santa-fe-2012-2018-2.4','model':'Santa Fe','model_he':'סנטה פה','generation':'DM','years':[2012,2018],
 'engines':['2.4 GDI (Theta II, G4KJ)','3.3 V6 (Lambda II)'],'fuel':'petrol',
 'interval':{'km':15000,'months':12,'note':'בספר רשימות לכל 30,000 ק"מ או 24 חודשים; שמן ומסנן כל 15,000 ק"מ או 12 חודשים בתנאי הפעלה קשים, ובמנוע 2.4 גם כשאין שמן מהמפרט המומלץ'},
 'cycle_km':240000,
 'long_interval':[COOL,{'item':'spark_plugs','action':'replace','every_km':160000,'every_months':120,'note':'מצתי אירידיום, מנועי 2.4 ו-3.3'},
  {'item':'transmission_oil','action':'inspect','every_km':90000,'note':'לפי הספר אין צורך בבדיקה או טיפול בגיר האוטומטי; בתנאי הפעלה קשים החלפה כל 90,000'}],
 'sources':SRC,'status':'reviewed',
 'notes':'נבנה מספר היבואן העברי של סנטה פה DM. הספר נותן רשימת פעולות מצטברת לכל 30,000 ק"מ (עד 240,000); הקובץ בנוי על רשת 15,000 עם שמן ומסנן בכל טיפול, והפריטים מהרשימות בטיפולים הזוגיים. מסנן אוויר מוחלף כל 60,000, נוזל בלמים ומסנן מזגן כל 30,000, מרווח שסתומים נבדק ב-90,000 וב-180,000. בטיפול 180,000 הרשימה בספר לא כוללת את קווי הבלמים (כך הועתק). רצועת ההנעה נבדקת לראשונה ב-90,000 ק"מ או 72 חודשים. בגיר אוטומטי אין צורך בטיפול.'},
 merge(oil,grid(30000,common+petrol)))
write({**HY,'id':'hyundai-santa-fe-2013-2018-2.2-diesel','model':'Santa Fe','model_he':'סנטה פה','generation':'DM','years':[2013,2018],
 'engines':['2.2 CRDi (R, D4HB)'],'fuel':'diesel',
 'interval':{'km':15000,'months':12,'note':'בספר רשימות לכל 30,000 ק"מ או 24 חודשים; שמן ומסנן כל 15,000 ק"מ או 12 חודשים בתנאי הפעלה קשים (ואם אין שמן מהמפרט המומלץ: כל 20,000)'},
 'cycle_km':240000,
 'long_interval':[COOL,{'item':'transmission_oil','action':'inspect','every_km':90000,'note':'לפי הספר אין צורך בבדיקה או טיפול בגיר האוטומטי; בתנאי הפעלה קשים החלפה כל 90,000'}],
 'sources':SRC,'status':'reviewed',
 'notes':'נבנה מספר היבואן העברי של סנטה פה DM, שורות הדיזל (R 2.2). רשימות לכל 30,000 ק"מ; הקובץ בנוי על רשת 15,000 עם שמן ומסנן בכל טיפול. מחסנית מסנן הסולר נבדקת ב-30,000 ומוחלפת כל 60,000. רצועת ההנעה נבדקת לראשונה ב-90,000 ק"מ או 48 חודשים ואחר כך כל 30,000. מנוע R עם שרשרת תזמון. בתנאים קשים הספר מקצר שמן ל-15,000 ק"מ או 12 חודשים (ואם אין שמן מומלץ, 10,000 ק"מ או 6 חודשים).'},
 merge(oil,grid(30000,common+diesel)))
