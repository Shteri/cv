import sys; sys.path.insert(0,'.')
from gen import *
IMP='יוניון מוטורס'
URL='https://www.yumpu.com/en/document/view/27164868/page-1-2008-6-23-maintenance-schedule-europe-15000-'
s=S('toyota-corolla-2001-2007-1.6','Toyota','טויוטה','Corolla / Corolla RunX','קורולה / קורולה RunX','E120 (ZZE121)',(2001,2007),['1.6 VVT-i (3ZZ-FE)'],'petrol',IMP,
    15000,12,'לפי טבלת התחזוקה של טויוטה אירופה: טיפול כל 15,000 ק"מ או 12 חודשים, המוקדם; בתנאי שימוש קשים שמן ומסנן שמן כל 7,500 ק"מ או 6 חודשים',90000)
s.every('engine_oil','replace',15000,'החלפה כל 15,000 ק"מ או 12 חודשים')
s.every('oil_filter','replace',15000)
s.pat('air_filter','IIIRII',15000,'בדיקה כל 24 חודשים, החלפה ב-60,000 ק"מ או 48 חודשים; בדרכי אבק בדיקה כל 7,500 ק"מ')
s.pat('cooling_system','-I-I-I',15000,'בדיקת מקרן, מעבה, צינורות וחיבורים (כל 24 חודשים)')
s.pat('coolant','-I-I-I',15000,'נוזל Super Long Life (ורוד): בדיקה; החלפה ראשונה ב-150,000 ק"מ')
s.pat('exhaust','-I-I-I',15000)
s.pat('fuel_lines','-I-I-I',15000,'מכסה מיכל, צנרת וחיבורי דלק ושסתום אדי דלק (כל 24 חודשים)')
s.pat('evap_system','--I--I',15000,'מיכל פחם פעיל (קניסטר)')
s.add(90000,'valve_clearance','inspect','בדיקה בשמיעה (רעשי טאפטים ורעידות) וכיוון לפי הצורך; כל 72 חודשים')
s.pat('pedals','-I-I-I',15000,'דוושת בלם ובלם חניה (כל 24 חודשים)')
s.pat('parking_brake','-I-I-I',15000)
s.pat('brake_drums','-I-I-I',15000,'תופים ורפידות תוף כולל רפידות בלם החניה, אם קיימים')
s.pat('brake_pads','IIIIII',15000,'רפידות ודיסקים: בדיקה כל 15,000 ק"מ או 12 חודשים')
s.pat('brake_discs','IIIIII',15000)
s.pat('brake_fluid','-R-R-R',15000,'החלפה כל 30,000 ק"מ או 24 חודשים (DOT4)')
s.pat('brake_lines','-I-I-I',15000)
s.pat('clutch','-I-I-I',15000,'בדיקת נוזל המצמד (גיר ידני)')
s.pat('power_steering_fluid','-I-I-I',15000,'אם ההגה הידראולי')
s.pat('steering','-I-I-I',15000,'גלגל הגה, מוטות והגה')
s.pat('cv_boots','-I-I-I',15000)
s.pat('suspension','-I-I-I',15000,'מפרקים כדוריים, כיסויי אבק ומתלים קדמיים ואחוריים')
s.add(60000,'manual_gearbox_oil','inspect','גיר ידני: בדיקה כל 48 חודשים')
s.pat('tires','-I-I-I',15000)
s.pat('cabin_filter','-R-R-R',15000,'מסנן מיזוג (חלקיקים)')
s.pat('body_underside','-I-I-I',15000,'בדיקת קורוזיה (כל 24 חודשים)')
s.li('coolant','replace',first_km=150000,then_every_km=90000,note='נוזל Super Long Life (ורוד). ברכב עם נוזל LLC אדום/ירוק ישן: החלפה ראשונה ב-60,000 ק"מ או 36 חודשים ואחר כך כל 30,000 ק"מ או 24 חודשים')
s.li('spark_plugs','replace',every_km=90000,note='מצתי איסיריום/פלטינה. אם הותקנו מצתים רגילים: בדיקה ב-30,000 והחלפה כל 60,000 ק"מ או 48 חודשים')
s.li('drive_belt','inspect',first_km=105000,first_months=72,then_every_km=15000,then_every_months=12,note='רצועת עזר: בדיקה ראשונה ב-105,000 ק"מ או 72 חודשים ואחר כך כל 15,000 ק"מ או 12 חודשים')
s.src(URL,'manufacturer','Toyota Motor Europe, "MAINTENANCE SCHEDULE - EUROPE 15,000 km/9,000 miles" (גרסה 2008-6-23, הועלה ליומפו מחשבון toyota.tech.eu). עמוד 1 מנוע בנזין, עמודים 3-4 שלדה ומרכב, עמודה Corolla Verso ZNR10 3ZZ-FE (1.6)')
s.src('https://www.toyota-tech.eu/MS/PDFS/','manufacturer','המקור המקורי באתר toyota-tech.eu חסום בהתחברות (Keycloak); נעשה שימוש בעותק ביומפו')
notes=('לא נמצא ספר עברי או גיליון של יוניון מוטורס לקורולה E120 (בגיליונות היבואן אין דגם לפני 2007). '
       'הלוח לקוח מטבלת התחזוקה הרשמית של טויוטה אירופה, מהעמודה של קורולה וורסו עם אותו מנוע 3ZZ-FE 1.6. לכן זו טיוטה לפי דגם אחות. '
       'הטבלה מסתיימת ב-90,000 ק"מ וחוזרת על עצמה. למנוע זה יש שרשרת תזמון, ולכן אין בטבלה החלפת רצועת תזמון. '
       'בטבלה של הוורסו אין שורת שמן לגיר אוטומטי, כי לוורסו אין גיר אוטומטי רגיל. רוב הקורולות בארץ אוטומטיות, ולכן יש לברר במוסך מתי לבדוק ולהחליף שמן גיר (ATF T-IV). '
       'בתנאי שימוש קשים (נסיעות קצרות, דרכי עפר, חום) שמן ומסנן כל 7,500 ק"מ, ובדיקת בלמים ומתלים כל 15,000 ק"מ. '
       'ייתכן שחלק מרכבי שנת 2001-2002 במאגר הם עדיין מהדור הקודם (E110), עם אותו מנוע 3ZZ-FE; הלוח מתאים לפי המנוע.')
s.specs={'engine_oil':'API SJ/SL/SM (ILSAC) לפי הטבלה','coolant':'Toyota Super Long Life Coolant (ורוד); בדגמים ישנים LLC אדום/ירוק','brake_fluid':'SAE J1704 / DOT4','timing':'שרשרת (אין שורת רצועת תזמון למנוע זה בטבלה)'}
s.write('draft',notes)
rule('Toyota',['COROLLA'],(2001,2007),'toyota-corolla-2001-2007-1.6',engine_codes=['3ZZ'])
rule('Toyota',['COROLLA RUNX'],(2002,2007),'toyota-corolla-2001-2007-1.6',engine_codes=['3ZZ'])
save_rules('rules_toyota.json')
