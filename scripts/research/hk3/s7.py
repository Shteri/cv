from build import *
KIA={'make':'Kia','make_he':'קיה','importer':'טלקאר'}
A8='IIIIIIII'; E8='-I-I-I-I'; R8='RRRRRRRR'
rows=[('air_filter','IRIRIRIR'),('ac_system',A8),('ac_refrigerant',A8),('battery_12v',A8),('brake_lines',A8),('pedals',A8),('brake_fluid',R8),('cabin_filter',R8),
 ('cooling_system','-IIIIIII','בדיקה ראשונה ב-60,000 ואחר כך כל 30,000'),('brake_pads',A8),('brake_discs',A8),('dct_oil',E8,'אם קיים'),('cv_boots',A8),
 ('drive_belt','--IIIIII','בדיקה ראשונה ב-90,000 ק"מ או 48 חודשים ואחר כך כל 30,000'),('exhaust',A8),('electrical_system',A8),('suspension',A8,'מפרקים כדוריים קדמיים'),
 ('fuel_filter','IRIRIRIR','מחסנית מסנן הסולר; המרווח תלוי באיכות הסולר (EN590)'),('fuel_lines',A8,'וגם מכסה פתח הסולר כל 60,000'),('manual_gearbox_oil',E8,'אם קיים'),
 ('parking_brake',A8),('steering',A8),('tires',A8)]
oil={km:lst(('engine_oil','R'),('oil_filter','R')) for km in range(15000,240001,15000)}
write({**KIA,'id':'kia-ceed-2012-2018-1.6-diesel','model':"Cee'd",'model_he':'סיד','generation':'JD','years':[2012,2018],
 'engines':['1.6 CRDi (U2, D4FB)'],'fuel':'diesel',
 'interval':{'km':15000,'months':12,'note':'לפי הספר האירופי: בטבלה הרגילה שמן ומסנן כל 30,000 ק"מ או 24 חודשים; בתנאי הפעלה קשים כל 15,000 ק"מ או 12 חודשים'},
 'cycle_km':240000,
 'long_interval':[{'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24},
  {'item':'transmission_oil','action':'inspect','every_km':90000,'note':'לפי הספר אין צורך בבדיקה או טיפול בגיר האוטומטי; בתנאי הפעלה קשים החלפה כל 90,000'}],
 'sources':[{'url':'https://www.manualslib.com/manual/2438705/Kia-Ceed-2017.html?page=530','kind':'manufacturer','note':"ספר בעלים קיה סיד JD מתיחת פנים 2017 (אנגלית), פרק 7 עמ' 12-16 'Normal maintenance schedule - for Europe (except Russia)' (עמודי manualslib 530-534); טבלת 'except Europe' בעמ' 18-22 מורה שמן דיזל כל 10,000"}],
 'status':'draft',
 'notes':'הספר הישראלי של סיד JD לא נמצא. הרכב מיוצר באירופה וספרי קיה ישראל לדגמים אירופיים הם תרגום של הטבלה האירופית, ולכן נלקחה הטבלה האירופית (שורות הדיזל UII). הקובץ בנוי על רשת 15,000 עם שמן ומסנן בכל טיפול (לפי לוח התנאים הקשים) והפריטים מהטבלה בטיפולים הזוגיים. בטבלה שמחוץ לאירופה באותו ספר: שמן דיזל כל 10,000 ק"מ או 12 חודשים ורצועת הנעה מ-80,000 כל 20,000. מחסנית מסנן הסולר מוחלפת כל 60,000; נוזל בלמים ומסנן מזגן כל 30,000.'},
 merge(oil,grid(30000,rows)))
