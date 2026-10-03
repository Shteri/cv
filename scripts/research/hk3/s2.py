from build import *
KIA={'make':'Kia','make_he':'קיה','importer':'טלקאר'}
HY={'make':'Hyundai','make_he':'יונדאי','importer':'כלמוביל'}
A='IIIIIIII'; E='-I-I-I-I'; R8='RRRRRRRR'
NOTE_ME='לפי הספר הבינלאומי (מחוץ לאירופה): כל 15,000 ק"מ או 12 חודשים; ב"מזרח התיכון" כהגדרת הספר (מדינות המפרץ, איראן, תימן) כל 10,000'

# ---------- ix35 petrol ----------
rows=[('engine_oil',R8),('oil_filter',R8),('air_filter','IIRIIRII'),('ac_system',A),('ac_refrigerant',A),('battery_12v',A),('brake_fluid',A),
 ('brake_lines',A),('brake_pads',A),('brake_discs',A),('suspension',A,'מפרקים כדוריים קדמיים'),('steering',A),('tires',A),('cabin_filter',R8),
 ('drive_belt',E),('cv_boots',E),('exhaust',E),('parking_brake',E),('propshaft',E,'4WD בלבד'),
 ('fuel_filter','-I-R-I-R'),('fuel_tank_air_filter','-I-R-I-R'),('cooling_system','---I-I-I','בדיקה ראשונה ב-60,000 ואחר כך כל 30,000'),
 ('fuel_lines','---I---I'),('manual_gearbox_oil','---I---I','אם קיים'),('differential_oil','---I---I','4WD בלבד'),('transfer_case_oil','---I---I','4WD בלבד'),
 ('evap_system','---I---I','צינור אדים ומכסה פתח הדלק')]
write({**HY,'id':'hyundai-ix35-2010-2015-2.0','model':'ix35','model_he':'ix35','generation':'LM (EL)','years':[2010,2015],
 'engines':['2.0 MPI (Theta II, G4KD)','2.0 MPI (Nu, G4NA)'],'fuel':'petrol',
 'interval':{'km':15000,'months':12,'note':NOTE_ME},'cycle_km':120000,
 'long_interval':[
  {'item':'spark_plugs','action':'replace','every_km':160000,'every_months':120,'note':'מנוע 2.0; במנוע 1.6 כל 150,000'},
  {'item':'coolant','action':'replace','first_km':200000,'first_months':120,'then_every_km':40000,'then_every_months':24},
  {'item':'transmission_oil','action':'inspect','every_km':100000,'note':'גיר אוטומטי: בתנאים רגילים אין צורך בבדיקה או טיפול; בתנאי הפעלה קשים החלפה כל 100,000'}],
 'sources':[{'url':'https://www.manualpdf.co.il/hyundai/ix35-2014/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=894','kind':'manufacturer','note':"ספר בעלים ix35 מתיחת פנים (EL FL, אנגלית, 2014), פרק 7 עמ' 29-38 'Normal maintenance schedule - except Europe' (עמודי צפייה 894-903)"}],
 'status':'draft',
 'notes':'הספר הישראלי של ix35 לא נמצא; הספר האירופי (2010-2011) מפנה לפנקס השירות. נלקחה התוכנית "מחוץ לאירופה" מהספר הבינלאומי של מתיחת הפנים (2014), שהיא רשימות מצטברות לכל 15,000 ק"מ, ונבנתה ממנה רשת. אותה תוכנית מיושמת גם על 2010-2013 (מנוע G4KD זהה). מסנן אוויר מוחלף ב-45,000 וב-90,000 ונבדק בשאר הטיפולים; מסנן דלק ומסנן אוויר של מיכל הדלק מוחלפים כל 60,000. בתנאי הפעלה קשים: שמן כל 7,500 ק"מ או 6 חודשים, וגל הינע (4WD) נבדק כל 15,000. דגמי הדיזל (2.0 CRDi) אינם בקובץ: לפי אותו ספר שמן כל 10,000 ק"מ.'},
 grid(15000,rows))

# ---------- i10 PA ----------
rows=[('engine_oil',R8),('oil_filter',R8),('air_filter','IIRIIRII'),('drive_belt',E),('valve_clearance',E,'מנוע 1.1 בלבד'),('evap_system','---I---I','צינור אדים ומכסה פתח הדלק'),
 ('vacuum_hose',E),('fuel_filter','-I-R-I-R'),('fuel_lines','---I---I'),('battery_12v',A),('electrical_system',E),('brake_lines',A),('pedals',E),
 ('parking_brake',E),('brake_fluid',A),('brake_pads',A),('brake_discs',A),('brake_drums',E,'אם קיימים'),('steering',A),('cv_boots',E),('tires',A),
 ('suspension',A,'מפרקים כדוריים קדמיים'),('body_underside',A,'ברגים ואומים בשלדה ובמרכב'),('ac_refrigerant',A),('ac_system',A),('cabin_filter',A,'בדיקה (לא החלפה) בטבלה שמחוץ לאירופה'),
 ('manual_gearbox_oil',A,'אם קיים'),('transmission_oil',A,'אם קיים')]
write({**HY,'id':'hyundai-i10-2008-2013-1.1-1.2','model':'i10','model_he':'i10','generation':'PA','years':[2008,2013],
 'engines':['1.1 (Epsilon, G4HG)','1.2 (Kappa, G4LA)'],'fuel':'petrol',
 'interval':{'km':15000,'months':12,'note':NOTE_ME},'cycle_km':120000,
 'long_interval':[
  {'item':'timing_belt','action':'replace','every_km':135000,'every_months':108,'note':'מנוע 1.1 בלבד (במנוע 1.2 שרשרת). בהחלפה בודקים את משאבת המים'},
  {'item':'spark_plugs','action':'replace','every_km':40000},
  {'item':'coolant','action':'replace','first_km':200000,'first_months':120,'then_every_km':40000,'then_every_months':24}],
 'sources':[{'url':'https://www.manualpdf.co.il/hyundai/i10-2010/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=278','kind':'manufacturer','note':"ספר בעלים i10 (PA, אנגלית, 2010), פרק 7 עמ' 16-20 'Normal maintenance schedule - gasoline engine (except Europe)' (עמודי צפייה 278-282)"}],
 'status':'draft',
 'notes':'הספר הישראלי של i10 הדור הראשון לא נמצא; נלקחה טבלת "מחוץ לאירופה" מהספר הבינלאומי. בטבלה זו מסנן המזגן רק נבדק בכל טיפול, ונוזל הבלמים נבדק בכל טיפול ללא החלפה קבועה. בשורת מרווח השסתומים (1.1) יש ארבעה סימונים שהעמוד המקוון מציג לא במדויק; שובצו כל 30,000, כמו בטבלה האירופית של אותו ספר. בתנאי הפעלה קשים: שמן כל 7,500 ק"מ או 6 חודשים ורצועת תזמון (1.1) כל 90,000 ק"מ או 72 חודשים.'},
 grid(15000,rows))

# ---------- Kia Rio JB ----------
rows=[('engine_oil',R8),('oil_filter',R8),('drive_belt',E),('air_filter','IIRIIRII'),('evap_system',E,'צינור אדים ומכסה פתח הדלק'),('vacuum_hose',E),
 ('fuel_filter','---R---R'),('fuel_lines',A),('fuel_tank_air_filter','IIRIIRII'),('exhaust',A),('battery_12v',A),('electrical_system',E),('brake_lines',A),
 ('pedals',E),('parking_brake',E),('brake_fluid',A),('brake_pads',A),('brake_discs',A),('brake_drums',E),('power_steering_fluid',E,'נוזל וצינורות הגה כוח'),
 ('steering',A),('cv_boots',E),('tires',A),('suspension',A,'מפרקים כדוריים קדמיים'),('body_underside',A,'ברגים ואומים בשלדה ובמרכב'),('ac_refrigerant',A),('ac_system',A),
 ('cabin_filter',R8),('manual_gearbox_oil','---I---I','אם קיים'),('transmission_oil','---I---I','אם קיים')]
write({**KIA,'id':'kia-rio-2007-2012-1.4-1.6','model':'Rio','model_he':'ריו','generation':'JB','years':[2007,2012],
 'engines':['1.4 (Alpha II, G4EE)','1.6 (Alpha II, G4ED)'],'fuel':'petrol',
 'interval':{'km':15000,'months':12,'note':'לפי הספר הבינלאומי (מחוץ לאוסטרליה ולאירופה): כל 15,000 ק"מ או 12 חודשים'},'cycle_km':120000,
 'long_interval':[
  {'item':'timing_belt','action':'replace','every_km':135000,'every_months':108,'note':'לפי ספר 2010; ספר 2009 מורה בדיקה ב-60,000 והחלפה ב-90,000. בהחלפה בודקים את משאבת המים'},
  {'item':'spark_plugs','action':'replace','every_km':40000},
  {'item':'coolant','action':'replace','first_km':48000,'first_months':24,'then_every_km':40000,'then_every_months':24}],
 'sources':[{'url':'https://www.manualpdf.co.il/kia/rio-2010/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=264','kind':'manufacturer','note':"ספר בעלים ריו JB 2010 (אנגלית), פרק 7 עמ' 7-10 'Normal maintenance schedule - gasoline engine (except Australia & New Zealand)' (עמודי צפייה 264-267)"},
            {'url':'https://www.manualpdf.co.il/kia/rio-2009/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=251','kind':'manufacturer','note':"ספר בעלים ריו JB 2009, פרק 7 עמ' 7-10 'except Australia' (עמודי צפייה 251-254), להשוואה ולשורות שלא הוצגו בבירור בספר 2010"}],
 'status':'draft',
 'notes':'הספר הישראלי של ריו JB לא נמצא; נלקחו עמודות "מחוץ לאירופה" בטבלת ספר 2010 (מחוץ לאוסטרליה וניו זילנד). שורות צינור האדים וצינורות הוואקום מוצגות בעמוד המקוון של ספר 2010 לא במדויק, ולכן שובצו לפי ספר 2009 (כל 30,000). נוזל קירור: החלפה ראשונה ב-48,000 ק"מ או 24 חודשים ואחר כך כל 40,000. בספר 2009 רצועת ההנעה נבדקת בכל טיפול, שמן גיר ידני נבדק בכל טיפול, ורצועת התזמון מוחלפת כבר ב-90,000; כדאי לבדוק מול מדבקת המוסך.'},
 grid(15000,rows))
