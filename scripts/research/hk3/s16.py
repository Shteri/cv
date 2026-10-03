from build import *
KIA={'make':'Kia','make_he':'קיה','importer':'טלקאר'}
A8='IIIIIIII'; E8='-I-I-I-I'; R8='RRRRRRRR'
rows=[('drive_belt','--IIIIII','בדיקה ראשונה ב-90,000 ק"מ או 48 חודשים ואחר כך כל 30,000'),('manual_gearbox_oil',E8,'אם קיים'),('dct_oil',E8,'אם קיים'),
 ('cv_boots',A8),('fuel_lines',A8,'וגם מכסה פתח הסולר כל 60,000'),('adblue',A8,'אם קיימת: צנרת וחיבורי תמיסת האוריאה; מכסה המיכל כל 60,000'),
 ('fuel_filter','IRIRIRIR','מחסנית מסנן הסולר; המרווח תלוי באיכות הסולר (EN590)'),('air_filter','IRIRIRIR'),('exhaust',A8),('cooling_system','-IIIIIII'),
 ('ac_system',A8),('ac_refrigerant',A8),('cabin_filter',R8),('brake_pads',A8),('brake_discs',A8),('brake_lines',A8),('brake_fluid',R8),('parking_brake',A8),
 ('steering',A8),('suspension',A8,'מפרקים כדוריים'),('tires',A8),('battery_12v',A8)]
oil={km:lst(('engine_oil','R'),('oil_filter','R')) for km in range(15000,240001,15000)}
write({**KIA,'id':'kia-ceed-2019-2023-1.6-diesel','model':"Ceed",'model_he':'סיד','generation':'CD','years':[2019,2023],
 'engines':['1.6 CRDi (Smartstream D1.6, D4FE)'],'fuel':'diesel',
 'interval':{'km':15000,'months':12,'note':'לפי הספר האירופי: בטבלה הרגילה שמן דיזל כל 30,000 ק"מ או 24 חודשים; בתנאי הפעלה קשים כל 15,000 ק"מ או 12 חודשים'},
 'cycle_km':240000,
 'long_interval':[{'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24},
  {'item':'timing_belt','action':'replace','every_km':240000,'note':'בדיקת רצועת תזמון כל 120,000; החלפת ערכת התזמון (רצועה, רצועת שמן, מותחן, גלגלת) כל 240,000'},
  {'item':'transmission_oil','action':'inspect','every_km':90000,'note':'לפי הספר אין צורך בבדיקה או טיפול בגיר האוטומטי בתנאים רגילים; בתנאים קשים החלפה כל 90,000'},
  {'item':'ecall_battery','action':'replace','every_months':36,'note':'אם קיימת מערכת eCall'}],
 'sources':[{'url':'https://www.manualslib.com/manual/1799825/Kia-Xceed-2020.html?page=566','kind':'manufacturer','note':"ספר בעלים קיה XCeed 2020 (אנגלית, אירופה), פרק 8 עמ' 16-20 'Normal maintenance schedule - for Europe (except Russia)', שורות הדיזל SmartStream D1.6 ותנאים קשים (עמודי manualslib 566-570)"}],
 'status':'draft',
 'notes':'הספר הישראלי של סיד CD לא נמצא. נלקחה הטבלה האירופית מספר XCeed 2020, שחולק עם סיד CD את מנוע הדיזל 1.6 (D4FE). הקובץ בנוי על רשת 15,000 עם שמן ומסנן בכל טיפול (לפי לוח התנאים הקשים) ושאר הפריטים בטיפולים הזוגיים. מסנן אוויר ומחסנית מסנן הסולר מוחלפים כל 60,000; נוזל בלמים ומסנן מזגן כל 30,000.'},
 merge(oil,grid(30000,rows)))
