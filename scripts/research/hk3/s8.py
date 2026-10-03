from build import *
HY={'make':'Hyundai','make_he':'יונדאי','importer':'כלמוביל'}
A='IIIIIIII'; R8='RRRRRRRR'
rows=[('engine_oil',R8),('oil_filter',R8),('drive_belt','-----I-I'),('air_filter','IIIRIIIR'),('spark_plugs','----R---','החלפה ב-75,000'),
 ('evap_system','-I-I-I-I','צינור אדים ומכסה פתח הדלק'),('vacuum_hose','---I---I','צנרת ואקום ואוורור בית הארכובה'),('fuel_tank_air_filter','---I---I'),
 ('fuel_lines','---I---I'),('cooling_system','-I-I-I-I'),('intercooler_pipes','-IIIIIII'),('battery_12v',A),('electrical_system',A),('brake_lines',A),
 ('pedals',A),('parking_brake',A),('brake_fluid','IRIRIRIR'),('brake_pads',A),('brake_discs',A),('steering',A),('cv_boots',A),('tires',A),
 ('suspension',A),('cabin_filter','IIRIIRII'),('exhaust',A),('differential_oil','---I---I','4WD: שמן דיפרנציאל אחורי ותיבת העברה'),('propshaft',A,'4WD')]
write({**HY,'id':'hyundai-kona-2024-2026-1.6t-1.0t','model':'Kona','model_he':'קונה','generation':'SX2','years':[2024,2026],
 'engines':['1.6 T-GDI (Smartstream G1.6, G4FP)','1.0 T-GDI (Smartstream G1.0, G3LE)'],'fuel':'petrol',
 'interval':{'km':15000,'months':12,'note':'לפי לוח התחזוקה של היבואן: כל 15,000 ק"מ או 12 חודשים'},'cycle_km':120000,
 'long_interval':[],
 'sources':[{'url':'https://res.cloudinary.com/colmobil/images/v1716190836/ספר-רכב-קונה-2024/ספר-רכב-קונה-2024.pdf','kind':'importer','note':"ספר הרכב העברי של כלמוביל לקונה 2024 (קובץ סרוק), עמ' 9-9 עד 9-11 (עמודי PDF 510-512): 'לוח תחזוקה רגילה' ותחזוקה בתנאים קשים"}],
 'status':'reviewed',
 'notes':'הועתק מלוח התחזוקה הרגיל בספר היבואן (עמודות של 15,000 ק"מ עד 120,000). מסנן אוויר מוחלף כל 60,000, מסנן מזגן ב-45,000 וב-90,000, נוזל בלמים כל 30,000, מצתים ב-75,000. צנרת המצנן הביני (טורבו) נבדקת מ-30,000 בכל טיפול. שורת נוזל הקירור בלוח ריקה, ולכן אין לה מועד בקובץ. בתנאי הפעלה קשים: שמן ומסנן כל 5,000 ק"מ או 6 חודשים. במנוע 1.6 T-GDI הרכב עשוי להציג מועד החלפת שמן לפי מערכת ניהול חיי השמן.'},
 grid(15000,rows))
