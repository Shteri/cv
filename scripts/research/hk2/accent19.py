from build import build
meta={'make':'Hyundai','make_he':'יונדאי','model':'Accent','model_he':'אקסנט','generation':'HC','id':'hyundai-accent-2019-2023-1.4-1.6',
 'years':[2019,2023],'engines':['1.4 MPI (Kappa, G4LC)','1.6 MPI (Gamma, G4FG)'],'fuel':'petrol','importer':'כלמוביל',
 'interval':{'km':15000,'months':12,'note':'לפי ספר הבעלים הבינלאומי (אנגלית): 15,000 ק"מ או 12 חודשים; לאזור המזרח התיכון הספר מציין שמן ומסנן כל 10,000 ק"מ או 12 חודשים'},
 'cycle_km':120000,
 'long_interval':[
  {'item':'spark_plugs','action':'replace','every_km':60000},
  {'item':'cooling_system','action':'inspect','first_km':60000,'first_months':48,'then_every_km':30000,'then_every_months':24},
  {'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24}],
 'sources':[{'url':'https://www.manualslib.com/manual/1958374/Hyundai-Accent-Hci-2019.html?page=358','kind':'other','note':"ספר הבעלים הבינלאומי באנגלית של Hyundai Accent HCi 2019 (שוקי ייצוא, כולל מזרח תיכון), עמודי manualslib 358-361 (ספר 7-10 עד 7-13), 'Normal maintenance schedule (Gasoline Engine)'"}],
 'status':'draft',
 'notes':"לא נמצא ספר רכב עברי של אקסנט 2019-2023. הקובץ מבוסס על ספר הבעלים הבינלאומי באנגלית (שוקי ייצוא), מנועי 1.4 ו-1.6 MPI. במזרח התיכון לפי הספר: שמן ומסנן כל 10,000 ק\"מ, מסנן אוויר בכל טיפול ובדיקת מצבר כל 10,000 ק\"מ או 6 חודשים. מסנן מזגן מוחלף בכל טיפול. מסנן דלק מוחלף ב-60,000 וב-120,000. מצתים כל 60,000 ק\"מ. נוזל בלמים נבדק בכל טיפול ואינו מוחלף בטבלה. גיר אוטומטי ללא טיפול. בדיקת חופש שסתומים ב-90,000 רק במנוע 1.6. תוסף דלק כל 15,000 ק\"מ אם הדלק ללא תוספים."}
rows=[('engine_oil','RRRRRRRR'),('oil_filter','RRRRRRRR'),('drive_belt','-I-I-I-I'),('air_filter','IIRIIRII'),
 ('valve_clearance','-----I--','מנוע 1.6 MPI בלבד'),('evap_system','IIRIIRII','מיכל פחם (קניסטר); צינור אדים ומכסה מילוי נבדקים ב-60,000 וב-120,000'),
 ('vacuum_hose','IIIIIIII'),('fuel_filter','-I-R-I-R'),('fuel_lines','---I---I'),('fuel_tank_air_filter','IIRIIRII'),
 ('battery_12v','IIIIIIII'),('electrical_system','-I-I-I-I'),('brake_lines','IIIIIIII'),('pedals','-I-I-I-I'),('parking_brake','-I-I-I-I'),
 ('brake_fluid','IIIIIIII'),('brake_pads','IIIIIIII'),('brake_discs','IIIIIIII'),('steering','IIIIIIII'),('cv_boots','IIIIIIII'),('tires','IIIIIIII'),
 ('suspension','IIIIIIII'),('exhaust','-I-I-I-I'),('ac_refrigerant','IIIIIIII'),('ac_system','IIIIIIII'),('cabin_filter','RRRRRRRR'),('manual_gearbox_oil','---I---I')]
build(meta,15000,rows)
