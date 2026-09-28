from build import build
A='I'*8; E='-I'*4
meta={'make':'Hyundai','make_he':'יונדאי','model':'Accent','model_he':'אקסנט','generation':'MC','id':'hyundai-accent-2006-2011-1.4-1.6',
 'years':[2006,2011],'engines':['1.4 (Alpha II, G4EE)','1.6 (Alpha II, G4ED)'],'fuel':'petrol','importer':'כלמוביל',
 'interval':{'km':15000,'months':12,'note':'לפי ספר הבעלים הבינלאומי (בריטניה/אוסטרליה): כל 15,000 ק"מ או 12 חודשים (המוקדם)'},
 'cycle_km':120000,
 'long_interval':[
  {'item':'timing_belt','action':'replace','every_km':90000,'note':'בדיקה ב-60,000 ק"מ, החלפה ב-90,000 ק"מ'},
  {'item':'spark_plugs','action':'replace','every_km':40000},
  {'item':'coolant','action':'replace','first_km':100000,'first_months':60,'then_every_km':40000,'then_every_months':24}],
 'sources':[{'url':'https://www.carmanualsonline.info/hyundai-accent-2009-owner-s-manual-rhd-uk-australia/175','kind':'other','note':"ספר הבעלים באנגלית של Hyundai Accent MC 2009 לשווקי הגה ימני (בריטניה/אוסטרליה), עמודים 5-4 ו-5-5 (תמונות עמוד 175-176 באתר), 'Regular servicing'"}],
 'status':'draft',
 'notes':"לא נמצא ספר רכב עברי של אקסנט MC. הקובץ מבוסס על ספר הבעלים באנגלית לשוק בריטניה/אוסטרליה. רצועת תזמון נבדקת ב-60,000 ומוחלפת ב-90,000 ק\"מ. רצועת עזר מוחלפת ב-60,000 וב-120,000. מצתים כל 40,000 ק\"מ. מסנן אוויר ומסנן אוויר של מיכל הדלק מוחלפים ב-45,000 וב-90,000; מסנן דלק ב-60,000 וב-120,000; מסנן מזגן בכל טיפול. נוזל גיר אוטומטי מוחלף ב-90,000. נוזל בלמים נבדק כל 30,000 ואינו מוחלף בטבלה. נוזל קירור: החלפה ראשונה ב-100,000 ק\"מ או 60 חודשים ואז כל 40,000 ק\"מ או 24 חודשים."}
rows=[('engine_oil','R'*8),('oil_filter','R'*8),('drive_belt','IIIRIIIR'),('fuel_filter','---R---R'),('fuel_lines',A),('timing_belt','---I----'),
 ('evap_system',E,'צינור אדים ומכסה מילוי הדלק'),('vacuum_hose',A),('pcv_valve','--I--I--','צינור אוורור בית הארכובה'),('air_filter','IIRIIRII'),('fuel_tank_air_filter','IIRIIRII'),
 ('cooling_system',A),('manual_gearbox_oil',A),('transmission_oil','IIIIIRII','גיר אוטומטי'),('brake_lines',A),('brake_fluid',E),
 ('brake_drums',E),('parking_brake',E),('brake_pads',E),('brake_discs',E),('exhaust',A),('suspension',A),('steering',A),
 ('power_steering_fluid',A,'משאבת הגה כוח, רצועה וצינורות'),('cv_boots',E),('ac_refrigerant',A),('cabin_filter','R'*8)]
build(meta,15000,rows)
