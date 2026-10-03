from build import *
HY={'make':'Hyundai','make_he':'יונדאי','importer':'כלמוביל'}
A='IIIIIIII'; E='-I-I-I-I'; R8='RRRRRRRR'
rows=[('engine_oil',R8),('oil_filter',R8),('cabin_filter',R8),('air_filter','IIRIIRII'),('ac_system',A),('ac_refrigerant',A),('battery_12v',A),('brake_lines',A),
 ('brake_fluid',A),('brake_pads',A),('brake_discs',A),('cv_boots',A),('exhaust',A),('suspension',A,'מפרקים כדוריים קדמיים'),('parking_brake',A),('steering',A),
 ('tires',A),('vacuum_hose',A),('drive_belt',E),('fuel_filter','-I-R-I-R'),('fuel_tank_air_filter','-I-R-I-R','אם קיים'),('fuel_lines','---I---I'),
 ('manual_gearbox_oil','---I---I','אם קיים'),('evap_system','---I---I','צינור אדים ומכסה פתח הדלק'),('cooling_system','---I-I-I','בדיקה ראשונה ב-60,000 ואחר כך כל 30,000')]
write({**HY,'id':'hyundai-veloster-2011-2017-1.6','model':'Veloster','model_he':'ולוסטר','generation':'FS','years':[2011,2017],
 'engines':['1.6 GDI (Gamma, G4FD)'],'fuel':'petrol',
 'interval':{'km':15000,'months':12,'note':'לפי הספר הבינלאומי (מחוץ לאירופה): כל 15,000 ק"מ או 12 חודשים; ב"מזרח התיכון" כהגדרת הספר (מדינות המפרץ, איראן, תימן) כל 10,000'},
 'cycle_km':120000,
 'long_interval':[{'item':'spark_plugs','action':'replace','every_km':160000,'every_months':120,'note':'מנוע GDI'},
  {'item':'valve_clearance','action':'inspect','every_km':90000,'every_months':48},
  {'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24},
  {'item':'transmission_oil','action':'replace','every_km':100000,'note':'בתנאים רגילים אין צורך בטיפול בגיר האוטומטי/DCT; בתנאי הפעלה קשים החלפה כל 100,000'}],
 'sources':[{'url':'https://www.manualpdf.co.il/hyundai/veloster-2012/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=303','kind':'manufacturer','note':"ספר בעלים ולוסטר (אנגלית, 2012), פרק 7 עמ' 20-30 'Normal maintenance schedule - except Europe' (עמודי צפייה 303-313): רשימות מצטברות לכל 15,000 ק\"מ"}],
 'status':'draft',
 'notes':'הספר הישראלי של ולוסטר לא נמצא; נלקחה התוכנית "מחוץ לאירופה" מהספר הבינלאומי ונבנתה ממנה רשת. מסנן אוויר מוחלף ב-45,000 וב-90,000; מסנן דלק ומסנן אוויר של מיכל הדלק מוחלפים כל 60,000; נוזל הבלמים נבדק בכל טיפול. ברשימות מופיעה החלפת מצתים ב-60,000 וב-120,000, אך הספר מציין שבמנוע GDI ההחלפה ב-160,000 ק"מ או 120 חודשים, וכך נרשם. דגם הטורבו (T-GDI) אינו בקובץ: לפי אותו ספר שמן כל 8,000 ק"מ.'},
 grid(15000,rows))
