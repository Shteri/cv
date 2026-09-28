from build import build
A='I'*8
meta={'make':'Kia','make_he':'קיה','model':'Rio','model_he':'ריו','generation':'UB','id':'kia-rio-2011-2017-1.25-1.4',
 'years':[2011,2017],'engines':['1.25 MPI (Kappa, G4LA)','1.4 MPI (Gamma, G4FA)'],'fuel':'petrol','importer':'טלקאר',
 'interval':{'km':15000,'months':12,'note':'לפי ספר הבעלים הבינלאומי, טבלת "מחוץ לאירופה": 15,000 ק"מ או 12 חודשים; למזרח התיכון הספר מציין שמן ומסנן כל 10,000 ק"מ או 12 חודשים'},
 'cycle_km':120000,
 'long_interval':[
  {'item':'spark_plugs','action':'replace','every_km':60000},
  {'item':'valve_clearance','action':'inspect','every_km':90000,'every_months':48},
  {'item':'cooling_system','action':'inspect','first_km':60000,'first_months':48,'then_every_km':30000,'then_every_months':24},
  {'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24}],
 'sources':[{'url':'https://www.manualslib.com/manual/740114/Kia-Rio.html?page=382','kind':'other','note':"ספר הבעלים הבינלאומי באנגלית של Kia Rio (UB), עמודי manualslib 382-391 (ספר 7-20 עד 7-28), 'Normal maintenance schedule - except Europe', רשימות לפי 15,000 ק\"מ"}],
 'status':'draft',
 'notes':"לא נמצא ספר רכב עברי של ריו UB. הקובץ מבוסס על ספר הבעלים הבינלאומי באנגלית, טבלת 'מחוץ לאירופה'. במזרח התיכון (לפי הספר) שמן ומסנן כל 10,000 ק\"מ ומסנן אוויר מוחלף בכל טיפול; בשאר השווקים מסנן אוויר מוחלף ב-45,000 וב-90,000. מסנן מזגן בכל טיפול. מסנן דלק מוחלף ב-60,000 וב-120,000. מצתים כל 60,000 ק\"מ. נוזל בלמים נבדק בכל טיפול ואינו מוחלף בטבלה. תוסף דלק כל 5,000 ק\"מ או 6 חודשים אם הדלק ללא תוספים."}
rows=[('engine_oil','R'*8),('oil_filter','R'*8),('air_filter','IIRIIRII'),('ac_refrigerant',A),('ac_system',A),('battery_12v',A),
 ('brake_lines',A),('brake_fluid',A),('brake_pads',A),('brake_discs',A),('drive_belt','-I-I-I-I'),('cv_boots',A),('exhaust',A),('suspension',A),
 ('fuel_filter','-I-R-I-R'),('fuel_lines','---I---I'),('parking_brake',A),('steering',A),('tires',A),('transmission_oil','---I---I','גיר אוטומטי'),
 ('manual_gearbox_oil','---I---I'),('evap_system','---I---I','צינור אדים ומכסה מילוי הדלק'),('cabin_filter','R'*8)]
build(meta,15000,rows)
