from build import *
HY={'make':'Hyundai','make_he':'יונדאי','importer':'כלמוביל'}
A='IIIIIIII'; E='-I-I-I-I'; R8='RRRRRRRR'
rows=[('drive_belt','--IIIIII','בדיקה ראשונה ב-90,000 ק"מ או 72 חודשים ואחר כך כל 30,000'),('air_filter','IRIRIRIR'),('evap_system',E,'צינור אדים ומכסה פתח הדלק'),
 ('fuel_tank_air_filter',E),('fuel_filter',A),('fuel_lines',E),('cooling_system','-IIIIIII','בדיקה ראשונה ב-60,000 ואחר כך כל 30,000'),('valve_clearance','--I--I--'),
 ('battery_12v',A),('brake_lines',A),('parking_brake',A),('brake_fluid',R8),('brake_pads',A),('brake_discs',A),('steering',A),('cv_boots',A),('tires',A),
 ('suspension',A,'מפרקים כדוריים קדמיים'),('ac_refrigerant',A),('ac_system',A),('cabin_filter',R8),('manual_gearbox_oil',E,'אם קיים'),('exhaust',A)]
oil={km:lst(('engine_oil','R'),('oil_filter','R'),('intercooler_pipes','I')) for km in range(10000,240001,10000)}
write({**HY,'id':'hyundai-i30-2017-2020-1.4-turbo','model':'i30','model_he':'i30','generation':'PD','years':[2017,2020],
 'engines':['1.4 T-GDI (Kappa, G4LD)'],'fuel':'petrol',
 'interval':{'km':10000,'months':12,'note':'לפי הספר האירופי: שמן ומסנן ובדיקת צנרת מצנן הביניים כל 10,000 ק"מ או 12 חודשים; שאר הטבלה בעמודות של 30,000'},
 'cycle_km':240000,
 'long_interval':[{'item':'spark_plugs','action':'replace','every_km':75000,'every_months':60},
  {'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24},
  {'item':'transmission_oil','action':'inspect','every_km':90000,'note':'לפי הספר אין צורך בבדיקה או טיפול בגיר האוטומטי/DCT בתנאים רגילים'}],
 'sources':[{'url':'https://www.manualslib.com/manual/1363798/Hyundai-I30-2018.html?page=402','kind':'manufacturer','note':"ספר בעלים יונדאי i30 PD 2018 (אנגלית), פרק 7 עמ' 8-10 'Normal maintenance schedule (for Europe)' (עמודי manualslib 402-404); טבלת 'except Europe' בעמ' 407-410"}],
 'status':'draft',
 'notes':'הספר הישראלי של i30 PD לא נמצא. הרכב מיוצר באירופה, ולכן נלקחה הטבלה האירופית של מנוע הטורבו 1.4 T-GDI: שמן כל 10,000 ק"מ, ושאר הפריטים בעמודות של 30,000 עד 240,000. מסנן אוויר מוחלף כל 60,000; נוזל בלמים ומסנן מזגן כל 30,000; מצתים כל 75,000 ק"מ או 60 חודשים; מרווח שסתומים נבדק ב-90,000 וב-180,000.'},
 merge(oil,grid(30000,rows)))
