from build import *
HY={'make':'Hyundai','make_he':'יונדאי','importer':'כלמוביל'}
A='IIIIIIII'; E='-I-I-I-I'; R8='RRRRRRRR'
SRC={'url':'https://www.manualslib.com/manual/3393691/Hyundai-Santa-Fe-Cm.html?page=306','kind':'manufacturer','note':"ספר בעלים סנטה פה CM (אנגלית, בינלאומי), פרק 7 עמ' 9-20 (עמודי manualslib 306-317): טבלאות בנזין ודיזל עם עמודות 'For Europe' / 'Except Europe'"}
rows=[('engine_oil',R8),('oil_filter',R8),('drive_belt',E),('air_filter','IIRIIRII'),('spark_plugs','-R-R-R-R','מנוע 2.4; במנוע 3.5 כל 150,000'),
 ('evap_system','---I---I','צינור אדים ומכסה פתח הדלק'),('fuel_tank_air_filter','-I-R-I-R','אם קיים'),('vacuum_hose',A,'צינור ואקום ל-EGR ולגוף המצערת, אם קיים'),
 ('fuel_filter','-I-R-I-R'),('fuel_lines','---I---I'),('cooling_system','---I-I-I','בדיקה ראשונה ב-60,000 ואחר כך כל 30,000'),('battery_12v',A),('electrical_system',E),
 ('brake_lines',A),('pedals',E),('parking_brake',E),('brake_fluid',A),('brake_pads',A),('brake_discs',A),('power_steering_fluid',A,'נוזל וצינורות הגה כוח'),
 ('steering',A),('cv_boots',E),('tires',A),('suspension',A,'מפרקים כדוריים קדמיים'),('body_underside',A,'ברגים ואומים בשלדה ובמרכב'),('ac_refrigerant',A),('ac_system',A),
 ('cabin_filter',R8),('manual_gearbox_oil','---I---I','אם קיים'),('transfer_case_oil','---I---I','4WD'),('differential_oil','---I---I','4WD'),('propshaft',E,'אם קיים'),('exhaust',E)]
write({**HY,'id':'hyundai-santa-fe-2010-2012-2.4','model':'Santa Fe','model_he':'סנטה פה','generation':'CM facelift','years':[2010,2012],
 'engines':['2.4 (Theta II, G4KE)'],'fuel':'petrol',
 'interval':{'km':15000,'months':12,'note':'לפי הספר הבינלאומי (מחוץ לאירופה, סין והמזרח התיכון): כל 15,000 ק"מ או 12 חודשים; ב"מזרח התיכון" כהגדרת הספר כל 10,000'},'cycle_km':120000,
 'long_interval':[{'item':'valve_clearance','action':'inspect','every_km':90000,'every_months':48},
  {'item':'coolant','action':'replace','first_km':200000,'first_months':120,'then_every_km':40000,'then_every_months':24},
  {'item':'transmission_oil','action':'replace','every_km':100000,'note':'בתנאים רגילים אין צורך בטיפול בגיר האוטומטי; בתנאי הפעלה קשים החלפה כל 100,000'}],
 'sources':[SRC],'status':'draft',
 'notes':'הספר הישראלי של סנטה פה CM לא נמצא (בספריית כלמוביל יש רק 2013 ואילך). נלקחו עמודות "מחוץ לאירופה" מהטבלה הבינלאומית של מנוע הבנזין. מצתים (2.4) כל 30,000; מסנן דלק ומסנן אוויר של מיכל הדלק מוחלפים כל 60,000; נוזל הבלמים נבדק בכל טיפול. בתנאי הפעלה קשים: שמן כל 7,500 ק"מ או 6 חודשים, שמן גיר ידני/דיפרנציאל/תיבת העברה כל 120,000. מנוע V6 2.7 (2007-2009) אינו בספר זה ואינו בקובץ.'},
 grid(15000,rows))
d30=[('drive_belt','--IIIIII','בדיקה ראשונה ב-90,000 ק"מ או 48 חודשים ואחר כך כל 30,000'),('evap_system',E,'צינור אדים ומכסה פתח הדלק'),
 ('fuel_filter','IRIRIRIR','מחסנית מסנן הסולר; המרווח תלוי באיכות הסולר (EN590)'),('fuel_lines',A),('cooling_system','-IIIIIII'),('battery_12v',A),('brake_lines',A),
 ('parking_brake',A),('brake_fluid',R8),('brake_pads',A),('brake_discs',A),('power_steering_fluid',A,'נוזל וצינורות הגה כוח'),('steering',A),('cv_boots',A),('tires',A),
 ('suspension',A,'מפרקים כדוריים קדמיים'),('ac_refrigerant',A),('ac_system',A),('cabin_filter',R8),('manual_gearbox_oil',E,'אם קיים'),('transfer_case_oil',E,'4WD'),
 ('differential_oil',E,'4WD'),('propshaft','I-I-I-I-','אם קיים'),('exhaust',A)]
oil={km:lst(('engine_oil','R'),('oil_filter','R')) for km in range(15000,240001,15000)}
write({**HY,'id':'hyundai-santa-fe-2010-2012-2.2-diesel','model':'Santa Fe','model_he':'סנטה פה','generation':'CM facelift','years':[2010,2012],
 'engines':['2.2 CRDi (R, D4HB)'],'fuel':'diesel',
 'interval':{'km':15000,'months':12,'note':'לפי הטבלה האירופית: שמן ומסנן כל 30,000 ק"מ או 24 חודשים, ובתנאי הפעלה קשים כל 15,000 ק"מ (או 6 חודשים); כאן לפי 15,000'},
 'cycle_km':240000,
 'long_interval':[{'item':'air_filter','action':'replace','every_km':40000,'every_months':24,'note':'בדיקה כל 20,000 ק"מ או 12 חודשים'},
  {'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24},
  {'item':'transmission_oil','action':'replace','every_km':90000,'note':'בתנאים רגילים אין צורך בטיפול בגיר האוטומטי; בתנאי הפעלה קשים החלפה כל 90,000'}],
 'sources':[SRC],'status':'draft',
 'notes':'הספר הישראלי של סנטה פה CM לא נמצא. בדיזל נלקחו עמודות "For Europe" (כמו בספר הישראלי של הדור הבא, DM, שבנוי לפי התוכנית האירופית בעמודות של 30,000), כי בעמודות שמחוץ לאירופה שמן הדיזל כל 10,000 ק"מ, מסנן אוויר נבדק כל 20,000 ומסנן המזגן מוחלף כל 15,000. מחסנית מסנן הסולר מוחלפת כל 60,000; נוזל בלמים ומסנן מזגן כל 30,000.'},
 merge(oil,grid(30000,d30)))
