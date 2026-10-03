from build import *
KIA={'make':'Kia','make_he':'קיה','importer':'טלקאר'}
A='IIIIIIII'; E='-I-I-I-I'; R8='RRRRRRRR'
rows=[('vacuum_hose',A,'צינורות ואקום ואוורור בית הארכובה'),('cv_boots',A),('propshaft',A,'הנעה כפולה'),('fuel_lines',E),('fuel_tank_air_filter',E),
 ('evap_system',E,'צינור אדים ומכסה מיכל הדלק'),('air_filter','IRIRIRIR'),('exhaust',A),('cooling_system','-IIIIIII'),('ac_system',A),('ac_refrigerant',A),
 ('cabin_filter',R8),('brake_pads',A),('brake_discs',A),('brake_lines',A),('brake_fluid',R8),('steering',A),('differential_oil',E,'AWD'),('transfer_case_oil',E,'AWD'),
 ('suspension',A,'מפרקים כדוריים'),('tires',A),('battery_12v',A)]
every15={km:lst(('engine_oil','R'),('oil_filter','R'),('hsg_belt','I'),('intercooler_pipes','I'),('brake_fluid','I')) for km in range(15000,240001,15000)}
write({**KIA,'id':'kia-sorento-2021-2026-1.6-hybrid','model':'Sorento','model_he':'סורנטו','generation':'MQ4 HEV/PHEV','years':[2021,2026],
 'engines':['1.6 T-GDI HEV/PHEV (Smartstream G1.6, G4FT)'],'fuel':'hybrid',
 'interval':{'km':15000,'months':12,'note':'לפי ספר היבואן: שמן ומסנן כל 15,000 ק"מ או 12 חודשים; שאר הטבלה בעמודות של 30,000'},
 'cycle_km':240000,
 'long_interval':[{'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24,'note':'נוזל קירור של המנוע'},
  {'item':'coolant','action':'replace','every_km':60000,'every_months':36,'note':'נוזל הקירור של המערכת ההיברידית (מעגל נפרד)'},
  {'item':'hsg_belt','action':'replace','every_km':105000,'every_months':84,'note':'בדיקה כל 15,000 ק"מ או 12 חודשים'},
  {'item':'spark_plugs','action':'replace','every_km':75000},
  {'item':'ecall_battery','action':'replace','every_months':36,'note':'סוללת מערכת eCall'}],
 'sources':[{'url':'https://cdnmedia.kia-israel.co.il/www/cars-book/Sorento-MQ4-HEV-PHEV-2021.pdf','kind':'importer','note':"ספר הרכב העברי של קיה ישראל לסורנטו היברידי ופלאג-אין 2021, פרק 8 עמ' 11-13 (עמודי PDF 611-613): תכנית תחזוקה רגילה ותנאים קשים"}],
 'status':'reviewed',
 'notes':'נבנה מטבלת התחזוקה בספר היבואן לסורנטו HEV/PHEV (אותו ספר לשתי הגרסאות). בכל 15,000: שמן ומסנן, בדיקת רצועת HSG, בדיקת צנרת המצנן הביני ובדיקת נוזל בלמים; בכל 30,000 נוזל הבלמים ומסנן המזגן מוחלפים ושאר פריטי הטבלה נבדקים. מסנן אוויר כל 60,000; מצתים כל 75,000; נוזל הקירור של המערכת ההיברידית כל 60,000 ק"מ או 36 חודשים. בתנאים קשים: שמן כל 7,500 ק"מ או 6 חודשים.'},
 merge(every15,grid(30000,rows)))
