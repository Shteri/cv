from build import *
KIA={'make':'Kia','make_he':'קיה','importer':'טלקאר'}
HY={'make':'Hyundai','make_he':'יונדאי','importer':'כלמוביל'}

# ---------- Kia Sportage QL 2019-2022 1.6 CRDi diesel (Israeli book) ----------
E8='-I-I-I-I'; A8='IIIIIIII'
rows30=[('air_filter','IRIRIRIR'),('fuel_filter','IRIRIRIR'),('fuel_lines',A8),('adblue',A8,'אם קיימת מערכת אוריאה: צנרת, חיבורים ומכסה המיכל'),
 ('exhaust',A8),('ac_system',A8),('ac_refrigerant',A8),('cabin_filter','RRRRRRRR'),('brake_pads',A8),('brake_discs',A8),('brake_lines',A8),
 ('brake_fluid','RRRRRRRR'),('parking_brake',A8),('steering',A8),('suspension',A8,'מפרקים כדוריים של המתלה'),('tires',A8),('battery_12v',A8),
 ('cv_boots',A8),('manual_gearbox_oil',E8,'אם קיימת'),('dct_oil',E8,'אם קיימת'),('differential_oil',E8,'הנעה כפולה בלבד'),
 ('transfer_case_oil',E8,'הנעה כפולה בלבד'),('propshaft',A8,'הנעה כפולה בלבד'),('cooling_system','-IIIIIII','בדיקה ראשונה ב-60,000 ואחר כך כל 30,000')]
g30=grid(30000,rows30)
oil={km:lst(('engine_oil','R'),('oil_filter','R')) for km in range(15000,240001,15000)}
svc=merge(oil,g30)
write({**KIA,'id':'kia-sportage-2019-2022-1.6-diesel','model':'Sportage','model_he':"ספורטאז'",'generation':'QL facelift (diesel)','years':[2019,2022],
 'engines':['1.6 CRDi (Smartstream D1.6, D4FE)'],'fuel':'diesel',
 'interval':{'km':15000,'months':12,'note':'בטבלה הרגילה של הספר שמן כל 30,000 ק"מ או 24 חודשים; בתנאי הפעלה קשים (חום, אבק, עצור-וסע) כל 15,000 או 12 חודשים, וזו גם תדירות הטיפולים של היבואן'},
 'cycle_km':240000,
 'long_interval':[
  {'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24},
  {'item':'timing_belt','action':'replace','every_km':240000,'note':'מנוע D1.6: בדיקת רצועת תזמון כל 120,000 ק"מ; החלפת ערכת התזמון (רצועה, רצועת משאבת שמן, מותחן וגלגלת) כל 240,000'},
  {'item':'manual_gearbox_oil','action':'replace','every_km':120000,'note':'רק בתנאי הפעלה קשים'},
  {'item':'transmission_oil','action':'inspect','every_km':90000,'note':'לפי הספר אין צורך בטיפול בגיר אוטומטי בתנאים רגילים; בתנאי הפעלה קשים החלפה כל 90,000'}],
 'sources':[{'url':'https://cdnmedia.kia-israel.co.il/www/cars-book/Sportage-QLe-2019-2021.pdf','kind':'importer','note':"ספר הרכב העברי של קיה ישראל לספורטאז' 2019-2021, פרק 8 עמ' 13-21 (עמודי PDF 546-553): עמודות 'דיזל / Smartstream D1.6'"},
            {'url':'https://kia-israel.co.il/wp-content/uploads/2020/11/ספר-רכב-Sportage_PE_OM_4-3-2019_OPT.pdf','kind':'importer','note':'אותו ספר באתר קיה ישראל'}],
 'status':'reviewed',
 'notes':"נבנה מטבלת התחזוקה של ספר היבואן לספורטאז' QL מתיחת פנים, שורות הדיזל (Smartstream D1.6). הטבלה בעמודות של 30,000 ק\"מ; הקובץ בנוי על רשת 15,000 עם החלפת שמן ומסנן בכל טיפול (לפי לוח התנאים הקשים), ושאר הפריטים בטיפולים הזוגיים. בדיזל מסנן הדלק נבדק ב-30,000 ומוחלף כל 60,000, ובספר יש הערה שהמרווח תלוי באיכות הסולר (EN590). אם אין שמן מהמפרט המומלץ, הספר מורה להחליף כל 20,000 ק\"מ. רצועת ההנעה לא מופיעה בטבלה עבור מנוע D1.6 (רק עבור R 2.0), ולכן לא נכללה. נוזל בלמים ומסנן מזגן מוחלפים כל 30,000. רישומי 2022 עם מנוע D4FE הם ככל הנראה מלאי QL."},
 svc)

# ---------- Hyundai Tucson JM petrol 2.0/2.7 ----------
A='IIIIIIII'; E='-I-I-I-I'
rows=[('engine_oil','RRRRRRRR'),('oil_filter','RRRRRRRR'),('drive_belt',A,'מנוע 2.0; במנוע V6 2.7 בדיקה כל 30,000 בלבד'),
 ('fuel_filter','---R---R'),('fuel_lines',A),('timing_belt','---I-R--','בהחלפה בודקים גם את משאבת המים'),('evap_system',E,'צינור אדים ומכסה הדלק'),
 ('vacuum_hose','--I--I--'),('air_filter','IIRIIRII'),('fuel_tank_air_filter','IIRIIRII'),
 ('cooling_system',A),('manual_gearbox_oil',A,'אם קיים'),('transmission_oil',A,'אם קיים'),('brake_lines',A),('brake_fluid',E),
 ('brake_drums',E,'בלמי תוף אחוריים ובלם חניה'),('parking_brake',E),('brake_pads',A),('brake_discs',A),('exhaust',A),('suspension',A,'כולל ברגי חיבור המתלים'),
 ('steering',A),('power_steering_fluid',A,'משאבת הגה כוח וצינורות'),('cv_boots',E),('ac_refrigerant',A),('cabin_filter','RRRRRRRR'),('propshaft',E,'4WD: גירוז במידת הצורך')]
svc=grid(15000,rows)
NOTE_ME='לפי הספר הכללי: כל 15,000 ק"מ או 12 חודשים (עמודת "מחוץ למזרח התיכון"; הגדרת המזרח התיכון בספר היא מדינות המפרץ, איראן ותימן, שם 10,000)'
write({**HY,'id':'hyundai-tucson-2005-2010-2.0-2.7','model':'Tucson','model_he':'טוסון','generation':'JM','years':[2005,2010],
 'engines':['2.0 DOHC (Beta, G4GC)','2.7 V6 (Delta, G6BA)'],'fuel':'petrol',
 'interval':{'km':15000,'months':12,'note':NOTE_ME},'cycle_km':120000,
 'long_interval':[
  {'item':'spark_plugs','action':'replace','every_km':40000,'note':'מצתים רגילים כל 40,000; מצתי פלטינה כל 100,000; מצתי אירידיום כל 160,000 ק"מ או 120 חודשים'},
  {'item':'coolant','action':'replace','first_km':48000,'first_months':24,'then_every_km':40000,'then_every_months':24,'note':'מחוץ לאיחוד האירופי'},
  {'item':'valve_clearance','action':'inspect','every_km':90000,'every_months':48,'note':'מנוע 2.0 בלבד'},
  {'item':'transfer_case_oil','action':'replace','every_km':100000,'note':'4WD: בדיקה כל 40,000, החלפה כל 100,000'},
  {'item':'differential_oil','action':'inspect','every_km':40000,'note':'4WD: שמן הסרן האחורי'}],
 'sources':[{'url':'https://www.manualpdf.co.il/hyundai/tucson-2007/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=251','kind':'manufacturer','note':'ספר בעלים כללי (GAT, אנגלית) של טוסון JM 2007, פרק 5 עמ\' 4-7 (עמודי צפייה 251-254): טבלת בנזין, טבלת תחזוקה כללית ותנאים קשים'}],
 'status':'draft',
 'notes':'מקור: הספר הכללי לייצוא (לא הספר הישראלי, שלא נמצא). נלקחו העמודות שאינן לאירופה ושאינן למזרח התיכון. רצועת תזמון: בדיקה ב-60,000 והחלפה ב-90,000; בהחלפה בודקים את משאבת המים. בתנאי הפעלה קשים הספר מקצר: שמן כל 7,500 ק"מ או 6 חודשים, רצועת תזמון כל 60,000 ק"מ או 48 חודשים, שמן גיר אוטומטי כל 40,000 ושמן גיר ידני כל 100,000. נוזל בלמים נבדק כל 30,000 (אין החלפה קבועה בטבלה).'},
 svc)

# ---------- Hyundai Tucson JM 2.0 CRDi diesel ----------
rows=[('engine_oil','RRRRRRRR'),('oil_filter','RRRRRRRR'),('air_filter','IIRIIRII'),('fuel_filter','-R-R-R-R','מחסנית מסנן הסולר; המרווח תלוי באיכות הסולר (EN590)'),
 ('timing_belt','-------R'),('drive_belt','-I-I-R-I'),('vacuum_hose',A,'משאבת ואקום, צינורות ואקום וצינור השמן של המשאבה, צינורות EGR ומצערת'),
 ('fuel_lines',A),('fuel_tank_air_filter','IIRIIRII'),
 ('cooling_system',A),('manual_gearbox_oil',A,'אם קיים'),('transmission_oil',A,'אם קיים'),('brake_lines',A),('brake_fluid',E),
 ('brake_drums',E,'בלמי תוף אחוריים ובלם חניה'),('parking_brake',E),('brake_pads',A),('brake_discs',A),('exhaust',A),('suspension',A,'כולל ברגי חיבור המתלים'),
 ('steering',A),('power_steering_fluid',A,'משאבת הגה כוח וצינורות'),('cv_boots',E),('ac_refrigerant',A),('cabin_filter','RRRRRRRR'),('propshaft',E,'4WD: גירוז במידת הצורך')]
svc=grid(15000,rows)
write({**HY,'id':'hyundai-tucson-2005-2009-2.0-diesel','model':'Tucson','model_he':'טוסון','generation':'JM','years':[2005,2009],
 'engines':['2.0 CRDi (D4EA)'],'fuel':'diesel',
 'interval':{'km':15000,'months':12,'note':'לפי הספר הכללי: שמן ומסנן כל 15,000 ק"מ או 12 חודשים'},'cycle_km':120000,
 'long_interval':[
  {'item':'coolant','action':'replace','first_km':48000,'first_months':24,'then_every_km':40000,'then_every_months':24,'note':'מחוץ לאיחוד האירופי'},
  {'item':'transfer_case_oil','action':'replace','every_km':100000,'note':'4WD: בדיקה כל 40,000, החלפה כל 100,000'},
  {'item':'differential_oil','action':'inspect','every_km':40000,'note':'4WD: שמן הסרן האחורי'}],
 'sources':[{'url':'https://www.manualpdf.co.il/hyundai/tucson-2007/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=252','kind':'manufacturer','note':'ספר בעלים כללי (GAT, אנגלית) של טוסון JM 2007, פרק 5 עמ\' 5-7 (עמודי צפייה 252-254): טבלת דיזל וטבלה כללית'}],
 'status':'draft',
 'notes':'מקור: הספר הכללי לייצוא, טבלת מנוע הדיזל; עמודות "מחוץ לאיחוד האירופי". רצועת התזמון מוחלפת ב-120,000 ורצועת ההנעה ב-90,000. בתנאי הפעלה קשים: שמן כל 7,500 ק"מ או 6 חודשים.'},
 svc)
