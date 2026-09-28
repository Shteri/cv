from build import build
meta={'make':'Kia','make_he':'קיה','model':'Carnival','model_he':'קרניבל','generation':'YP','id':'kia-carnival-2015-2020-3.3',
 'years':[2015,2020],'engines':['3.3 GDI V6 (Lambda II, G6DH)'],'fuel':'petrol','importer':'טלקאר',
 'interval':{'km':12000,'months':12,'note':'לפי ספר היבואן: כל 12,000 ק"מ או 12 חודשים (המוקדם); בתנאי הפעלה קשים שמן ומסנן כל 6,000 ק"מ או 6 חודשים'},
 'cycle_km':180000,
 'long_interval':[
  {'item':'drive_belt','action':'inspect','first_km':96000,'first_months':72,'then_every_km':24000,'then_every_months':24},
  {'item':'spark_plugs','action':'replace','every_km':156000},
  {'item':'valve_clearance','action':'inspect','every_km':96000,'every_months':72,'note':'בדיקת רעש שסתומים ורעידות מנוע, כוונון לפי הצורך'},
  {'item':'coolant','action':'replace','first_km':192000,'first_months':120,'then_every_km':48000,'then_every_months':24}],
 'sources':[{'url':'https://cdnmedia.kia-israel.co.il/www/cars-book/Carnival-YP-2016-2020.pdf','kind':'importer','note':"ספר הרכב העברי של קיה ישראל לקרניבל 2016-2020, פרק 7 עמ' 11-13 (עמודי PDF 493-495), 'תכנית תחזוקה רגילה - עבור רכב ללא מגדש טורבו', עמודות של 12,000 ק\"מ"}],
 'status':'reviewed',
 'notes':"הטבלה בספר היבואן בנויה בעמודות של 12,000 ק\"מ או 12 חודשים עד 180,000 ק\"מ. שמן, מסנן שמן ומסנן מזגן מוחלפים בכל טיפול; מסנן אוויר מוחלף כל 48,000 ק\"מ; סבב צמיגים כל 12,000. נוזל בלמים נבדק כל 24,000 ק\"מ ואינו מוחלף בטבלה. גיר אוטומטי ללא טיפול. תוסף דלק כל 12,000 ק\"מ או 12 חודשים אם הדלק אינו מסוג TOP TIER. בתנאים קשים שמן כל 6,000 ק\"מ ונוזל גיר אוטומטי כל 96,000 ק\"מ."}
E='-I'*7+'-'
rows=[('engine_oil','R'*15),('oil_filter','R'*15),('air_filter','IIIRIIIRIIIRIII'),('tire_rotation','T'*15),('cabin_filter','R'*15),
 ('vacuum_hose','I'*15),('battery_12v','I'*15),('brake_lines','I'*15),('brake_pads','I'*15),('brake_discs','I'*15),
 ('power_steering_fluid','I'*15),('steering','I'*15),('cv_boots','I'*15),('suspension','I'*15),('ac_system','I'*15),('ac_refrigerant','I'*15),('exhaust','I'*15),
 ('cooling_system','---I-I-I-I-I-I-'),('evap_system',E),('fuel_tank_air_filter',E),('fuel_lines','---I---I---I---'),('parking_brake',E),('brake_fluid',E)]
build(meta,12000,rows)
