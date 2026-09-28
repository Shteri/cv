from build import build
A='I'*8; E='-I'*4
meta={'make':'Hyundai','make_he':'יונדאי','model':'Getz','model_he':'גטס','generation':'TB','id':'hyundai-getz-2003-2010-1.3-1.6',
 'years':[2003,2010],'engines':['1.3 (Alpha, G4EA)','1.4 (Alpha II, G4EE)','1.6 (Alpha II, G4ED)'],'fuel':'petrol','importer':'כלמוביל',
 'interval':{'km':15000,'months':12,'note':'לפי ספר הבעלים הבינלאומי (אנגלית): כל 15,000 ק"מ או 12 חודשים (המוקדם)'},
 'cycle_km':120000,
 'long_interval':[
  {'item':'timing_belt','action':'replace','every_km':90000,'note':'בדיקה ב-60,000 ק"מ, החלפה ב-90,000 ק"מ'},
  {'item':'spark_plugs','action':'replace','every_km':40000},
  {'item':'coolant','action':'replace','first_km':100000,'first_months':60,'then_every_km':45000,'then_every_months':24}],
 'sources':[{'url':'https://www.manualslib.com/manual/752940/Hyundai-Getz.html?page=179','kind':'other','note':"ספר הבעלים הבינלאומי באנגלית של Hyundai Getz, עמודי manualslib 179 ו-181 (ספר 5-4, 5-6), טבלאות 'Scheduled maintenance' לבנזין ו'General maintenance'"}],
 'status':'draft',
 'notes':"לא נמצא ספר רכב עברי של גטס. הקובץ מבוסס על ספר הבעלים הבינלאומי באנגלית (טבלה משותפת לכל השווקים, עם שורות נפרדות לאירופה). רצועת תזמון נבדקת ב-60,000 ומוחלפת ב-90,000 ק\"מ. מצתים כל 40,000 ק\"מ. מסנן אוויר מוחלף כל 30,000 ק\"מ ומסנן מזגן בכל טיפול. מסנן דלק מוחלף ב-60,000 וב-120,000. נוזל בלמים נבדק כל 30,000 ואינו מוחלף בטבלה. נוזל גיר אוטומטי נבדק בכל טיפול (מחוץ לאירופה). נוזל קירור: החלפה ראשונה ב-100,000 ק\"מ או 60 חודשים ואז כל 45,000 ק\"מ או 24 חודשים. בדיקת חופש שסתומים בטבלה מיועדת למנוע 1.1 בלבד ולכן לא נכללה."}
rows=[('engine_oil','R'*8),('oil_filter','R'*8),('drive_belt',A),('fuel_filter','---R---R'),('fuel_lines',A),('timing_belt','---I----'),
 ('evap_system',E,'צינור אדים ומכסה מילוי הדלק'),('vacuum_hose',E),('air_filter','IR'*4),
 ('cooling_system',A),('manual_gearbox_oil',A),('transmission_oil',A,'גיר אוטומטי'),('brake_lines',A),('brake_fluid',E),
 ('brake_drums',E),('parking_brake',E),('brake_pads',A),('brake_discs',A),('exhaust',A),('suspension',A),('steering',A),
 ('power_steering_fluid',A,'משאבת הגה כוח, רצועה וצינורות'),('cv_boots',E),('ac_refrigerant',A),('cabin_filter','R'*8)]
build(meta,15000,rows)
