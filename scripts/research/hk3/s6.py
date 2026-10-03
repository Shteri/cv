from build import *
KIA={'make':'Kia','make_he':'קיה','importer':'טלקאר'}
A8='IIIIIIII'; E8='-I-I-I-I'; R8='RRRRRRRR'
rows=[('drive_belt','--IIIIII','בדיקה ראשונה ב-90,000 ק"מ או 48 חודשים ואחר כך כל 30,000'),('vacuum_hose',A8,'צינורות ואקום ואוורור בית הארכובה'),
 ('manual_gearbox_oil',E8,'אם קיים'),('dct_oil',E8,'אם קיים'),('cv_boots',A8),('fuel_lines',E8),('fuel_tank_air_filter',E8),('evap_system',E8,'צינור אדים ומכסה הדלק'),
 ('air_filter','IRIRIRIR'),('exhaust',A8),('cooling_system','-IIIIIII'),('ac_system',A8),('ac_refrigerant',A8),('cabin_filter',R8),('brake_pads',A8),('brake_discs',A8),
 ('brake_lines',A8),('brake_fluid',R8),('parking_brake',A8),('steering',A8),('suspension',A8,'מפרקים כדוריים'),('tires',A8),('battery_12v',A8)]
oil={km:lst(('engine_oil','R'),('oil_filter','R'),('intercooler_pipes','I')) for km in range(15000,240001,15000)}
write({**KIA,'id':'kia-ceed-xceed-2019-2021-1.4-turbo','model':"Ceed / XCeed",'model_he':"סיד / אקסיד",'generation':'CD','years':[2019,2021],
 'engines':['1.4 T-GDI (Kappa, G4LD)'],'fuel':'petrol',
 'interval':{'km':15000,'months':12,'note':'לפי הספר האירופי: שמן ומסנן כל 15,000 ק"מ או 12 חודשים; שאר הטבלה בעמודות של 30,000 ק"מ או 24 חודשים'},
 'cycle_km':240000,
 'long_interval':[{'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24},
  {'item':'spark_plugs','action':'replace','every_km':75000,'note':'מנוע 1.4 T-GDI'},
  {'item':'transmission_oil','action':'inspect','every_km':90000,'note':'לפי הספר אין צורך בבדיקה או טיפול בגיר האוטומטי בתנאים רגילים'},
  {'item':'ecall_battery','action':'replace','every_months':36,'note':'אם קיימת מערכת eCall'}],
 'sources':[{'url':'https://www.manualslib.com/manual/1799825/Kia-Xceed-2020.html?page=566','kind':'manufacturer','note':"ספר בעלים קיה XCeed 2020 (אנגלית, אירופה), פרק 8 עמ' 16-19 'Normal maintenance schedule - for Europe (except Russia)' (עמודי manualslib 566-569)"}],
 'status':'draft',
 'notes':'הספר הישראלי של סיד/אקסיד CD לא נמצא (ספרייתם של קיה ישראל אינה כוללת אותם). הרכב מיוצר באירופה, וספרי קיה ישראל לדגמים אירופיים (כמו ספורטאז\') הם תרגום של הטבלה האירופית, ולכן נלקחה הטבלה האירופית מספר XCeed 2020; סיד CD חולק אותו מנוע ואותה טבלה. שמן ומסנן ובדיקת צנרת מצנן הביניים (טורבו) כל 15,000; מסנן אוויר מוחלף כל 60,000; נוזל בלמים ומסנן מזגן כל 30,000; מצתים כל 75,000. מנוע 1.5 T-GDI (G4LK, מ-2021) אינו בספר 2020 ולכן אינו בקובץ.'},
 merge(oil,grid(30000,rows)))
