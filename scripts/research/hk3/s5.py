from build import *
KIA={'make':'Kia','make_he':'קיה','importer':'טלקאר'}
A8='IIIIIIII'; E8='-I-I-I-I'; R8='RRRRRRRR'
# ---- Soul AM 2012-2013 and Soul PS 2014 (Israeli books, 15k lists) ----
def soul(ps):
    base=[('engine_oil',R8),('oil_filter',R8),('air_filter','IIIRIIIR'),('ac_system',A8),('ac_refrigerant',A8),('battery_12v',A8),('brake_lines',A8),
     ('brake_fluid','IRIRIRIR','בטיפולים האי-זוגיים בדיקת מפלס'),('brake_pads',A8),('brake_discs',A8),('exhaust',A8),('suspension',A8,'מפרקים כדוריים קדמיים'),
     ('steering',A8),('tires',A8),('parking_brake','-I-I-I-I' if ps else 'II-I-I-I'),('cv_boots',E8),('vacuum_hose',E8,'צינור ואקום וצינורות אוורור בית הארכובה'),
     ('pedals',E8),('brake_drums',E8,'אם קיימים'),('cabin_filter','-R-R-R-R'),('drive_belt','-----I-I'),('valve_clearance','-----I--','מנוע 1.6'),
     ('cooling_system','---I-I-I','בדיקה ראשונה ב-60,000 ואחר כך כל 30,000'),('fuel_lines','-------I' if ps else '---I---I'),('manual_gearbox_oil','---I---I','אם קיים'),
     ('evap_system','---I---I','צינור אדים ומכסה מיכל הדלק'),('fuel_filter','---I---I'),('fuel_tank_air_filter','---I---I'),
     ('spark_plugs','---R---R','מצתי ניקל; עם מצתי אירידיום ההחלפה כל 150,000 ק"מ או 120 חודשים')]
    return grid(15000,base)
long=[{'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24},
      {'item':'transmission_oil','action':'inspect','every_km':90000,'note':'לפי הספר אין צורך בבדיקה או טיפול בגיר האוטומטי; בתנאי הפעלה קשים החלפה כל 90,000'}]
NOTE_S='לפי ספר היבואן: כל 15,000 ק"מ או 12 חודשים'
write({**KIA,'id':'kia-soul-2012-2013-1.6-gdi','model':'Soul','model_he':'סול','generation':'AM facelift','years':[2012,2013],
 'engines':['1.6 GDI (Gamma, G4FD)'],'fuel':'petrol','interval':{'km':15000,'months':12,'note':NOTE_S},'cycle_km':120000,'long_interval':long,
 'sources':[{'url':'https://cdnmedia.kia-israel.co.il/www/cars-book/Soul-AM-2012-2013.pdf','kind':'importer','note':"ספר הרכב העברי של קיה ישראל לסול 2012-2013, פרק 7 עמ' 10-20 (עמודי PDF 328-338): תוכנית תחזוקה רגילה למנוע בנזין, רשימות לכל 15,000 ק\"מ"}],
 'status':'reviewed',
 'notes':'נבנה מרשימות התחזוקה המצטברות בספר היבואן (מנוע בנזין). מסנן אוויר נבדק בכל טיפול ומוחלף כל 60,000; מסנן מזגן ונוזל בלמים מוחלפים כל 30,000 (בטיפולים שביניהם נבדק מפלס נוזל הבלמים). מצתי ניקל מוחלפים כל 60,000; מצתי אירידיום כל 150,000 ק"מ או 120 חודשים. רצועת הנעה נבדקת ב-90,000 וב-120,000. הספר ממליץ להוסיף תוסף דלק אם אין בנזין איכותי. אין צורך בטיפול בגיר האוטומטי. דגמי דיזל אינם בקובץ.'},
 soul(False))
write({**KIA,'id':'kia-soul-2014-2018-1.6','model':'Soul','model_he':'סול','generation':'PS','years':[2014,2018],
 'engines':['1.6 GDI (Gamma, G4FD)','1.6 MPI (Gamma, G4FG)'],'fuel':'petrol','interval':{'km':15000,'months':12,'note':NOTE_S},'cycle_km':120000,'long_interval':long,
 'sources':[{'url':'https://cdnmedia.kia-israel.co.il/www/cars-book/Soul-PS-2014.pdf','kind':'importer','note':"ספר הרכב העברי של קיה ישראל לסול 2014, פרק 7 עמ' 12-20 (עמודי PDF 517-526): תוכנית תחזוקה רגילה למנוע בנזין (הטקסט בקובץ מקודד, נקרא מתמונות העמודים)"}],
 'status':'reviewed',
 'notes':'נבנה מרשימות התחזוקה המצטברות בספר היבואן לסול PS. מסנן אוויר מוחלף כל 60,000; מסנן מזגן ונוזל בלמים כל 30,000. מצתי ניקל כל 60,000, מצתי אירידיום כל 150,000 ק"מ או 120 חודשים. מרווח שסתומים (1.6) נבדק ב-90,000; רצועת הנעה ב-90,000 וב-120,000. אם אין שמן מהמפרט המומלץ הספר מורה להחליף שמן כל 20,000 ק"מ או 12 חודשים. אין צורך בטיפול בגיר האוטומטי.'},
 soul(True))

# ---- Carens RP (Israeli book, 30k lists) ----
common=[('air_filter','IRIRIRIR'),('ac_system',A8),('ac_refrigerant',A8),('battery_12v',A8),('brake_lines',A8),('pedals',A8),('electrical_system',A8),
 ('brake_pads',A8),('brake_discs',A8),('cv_boots',A8),('exhaust',A8),('suspension',A8,'מפרקים כדוריים קדמיים'),('parking_brake',A8),('steering',A8),('tires',A8),
 ('manual_gearbox_oil',E8,'אם קיים'),('evap_system',E8,'צינור אדים ומכסה מיכל הדלק'),('brake_fluid',R8),('cabin_filter',R8),
 ('cooling_system','-IIIIIII','בדיקה ראשונה ב-60,000 ואחר כך כל 30,000'),('drive_belt','--IIIIII','בדיקה ראשונה ב-90,000 ואחר כך כל 30,000')]
petrol=[('fuel_filter',E8),('fuel_tank_air_filter',E8,'אם קיים'),('fuel_lines',E8),('spark_plugs','-R-R-R-R','מצתי ניקל; מצתי אירידיום כל 150,000')]
diesel=[('fuel_filter','IRIRIRIR','מחסנית מסנן הסולר'),('fuel_lines',A8)]
oil={km:lst(('engine_oil','R'),('oil_filter','R')) for km in range(15000,240001,15000)}
COOL={'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24}
AT={'item':'transmission_oil','action':'inspect','every_km':90000,'note':'לפי הספר אין צורך בבדיקה או טיפול בגיר האוטומטי; בתנאי הפעלה קשים החלפה כל 90,000'}
SRC=[{'url':'https://cdnmedia.kia-israel.co.il/www/cars-book/Carens-RP-2013.pdf','kind':'importer','note':"ספר הרכב העברי של קיה ישראל לקרנס 2013, פרק 7 עמ' 11-20 (עמודי PDF 563-572): רשימות לכל 30,000 ק\"מ ולוח תנאים קשים (הטקסט מקודד, נקרא מתמונות העמודים)"}]
write({**KIA,'id':'kia-carens-2013-2018-2.0','model':'Carens','model_he':'קרנס','generation':'RP','years':[2013,2018],
 'engines':['2.0 GDI (Nu, G4NC)'],'fuel':'petrol',
 'interval':{'km':15000,'months':12,'note':'בספר רשימות לכל 30,000 ק"מ או 24 חודשים; שמן ומסנן כל 15,000 ק"מ או 12 חודשים בתנאי הפעלה קשים, ובמנוע GDI גם כשאין שמן מהמפרט המומלץ'},
 'cycle_km':240000,'long_interval':[COOL,{'item':'spark_plugs','action':'replace','every_km':150000,'note':'מצתי אירידיום'},AT],
 'sources':SRC,'status':'reviewed',
 'notes':'נבנה מספר היבואן העברי של קרנס RP. הספר נותן רשימות מצטברות לכל 30,000 ק"מ עד 240,000; הקובץ בנוי על רשת 15,000 עם שמן ומסנן בכל טיפול והפריטים מהרשימות בטיפולים הזוגיים. מסנן אוויר מוחלף כל 60,000; נוזל בלמים ומסנן מזגן כל 30,000. בדיקת מרווח שסתומים בספר אינה חלה על מנוע Nu 2.0 ולכן לא נכללה. אין צורך בטיפול בגיר האוטומטי.'},
 merge(oil,grid(30000,common+petrol)))
write({**KIA,'id':'kia-carens-2013-2019-1.7-diesel','model':'Carens','model_he':'קרנס','generation':'RP','years':[2013,2019],
 'engines':['1.7 CRDi (U2, D4FD)'],'fuel':'diesel',
 'interval':{'km':15000,'months':12,'note':'בספר רשימות לכל 30,000 ק"מ או 24 חודשים; שמן ומסנן כל 15,000 ק"מ או 12 חודשים בתנאי הפעלה קשים (ואם אין שמן מומלץ: כל 20,000)'},
 'cycle_km':240000,'long_interval':[COOL,AT],'sources':SRC,'status':'reviewed',
 'notes':'נבנה מספר היבואן העברי של קרנס RP, שורות הדיזל. רשימות לכל 30,000 ק"מ; הקובץ בנוי על רשת 15,000 עם שמן ומסנן בכל טיפול. מחסנית מסנן הסולר נבדקת ב-30,000 ומוחלפת כל 60,000 (המרווח תלוי באיכות הסולר, EN590). רצועת ההנעה נבדקת לראשונה ב-90,000 ק"מ או 48 חודשים.'},
 merge(oil,grid(30000,common+diesel)))
