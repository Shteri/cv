import sys; sys.path.insert(0,'.')
from gen import *
IMP='כלמוביל'
URL_ZIP='https://mmc-manuals.ru/manuals/lancer_ix/maintenance/Lancer_MY2006_Service_Manual_eng.zip'
URL_PAGE='https://mmc-manuals.ru/Mitsubishi_Lancer_IX:_Service_Manuals'
URL_OUT='https://mmc-manuals.ru/manuals/outlander/maintenance/Outlander_Service_Manual_May2003.zip'
SRC_NOTE=('Mitsubishi Motors Europe B.V., "Pre-Delivery Inspection and Periodic Maintenance" (ספט׳ 2005), קבוצה 2 '
          '"Periodic Inspection and Maintenance Schedule" עמ׳ 2-3 עד 2-6 (קובץ PDI/GR00000300-2.pdf בתוך ארכיון ספר השירות של לנסר MY2006 לאירופה), '
          'שורות המסומנות "Applicable for LANCER"')

def build(s, gearbox_note):
    # A1 V-belt
    s.every('drive_belt','inspect',15000,'רצועת עזר: בדיקת סדקים ובלאי וכיוון מתיחה')
    # A3 ignition cables
    s.every('electrical_system','inspect',30000,'בדיקת כבלי הצתה')
    # A7 crankcase emission control
    s.every('pcv_valve','inspect',30000,'מערכת אוורור בית הארכובה')
    # A8 spark plugs (standard type 45,000; platinum/iridium 90,000)
    s.every('spark_plugs','replace',45000,'מצתים רגילים כל 45,000 ק"מ; מצתי פלטינה או אירידיום כל 90,000 ק"מ')
    # A9 radiator hoses
    s.every('coolant_hoses','inspect',30000,'צינורות מקרן וחיבוריהם')
    # A11 coolant change 60k/4y, A10 level check 30k
    s.every('coolant','replace',60000,'החלפה כל 60,000 ק"מ או 4 שנים')
    s.every('coolant','inspect',30000,'בדיקת מפלס במיכל העודפים')
    # A13 air cleaner replace 45k/3y, A12 inspect 15k/12m
    s.every('air_filter','replace',45000,'החלפה כל 45,000 ק"מ או 3 שנים')
    s.every('air_filter','inspect',15000,'בדיקה כל 15,000 ק"מ או שנה (בשימוש קשה כל 7,500)')
    # A15 brake fluid 30k/2y, A14 level 15k
    s.every('brake_fluid','replace',30000,'החלפה כל 30,000 ק"מ או שנתיים')
    s.every('brake_fluid','inspect',15000,'בדיקת מפלס נוזל בלמים ונוזל מצמד הידראולי')
    # A16 battery
    s.every('battery_12v','inspect',15000,'בדיקת מפלס אלקטרוליט')
    # B1/B2 suspension, D2 front wheel bearings 60k
    s.every('suspension','inspect',60000,'מתלים ומפרקים כדוריים; בנוסף בדיקת חופש מיסבי הגלגלים הקדמיים (כל 60,000 ק"מ או 4 שנים)')
    s.every('suspension','inspect',30000,'מתלים, מפרקים כדוריים וכיסויי אבק (כל 30,000 ק"מ או שנתיים)')
    # B4 drive shaft boots
    s.every('cv_boots','inspect',30000,'בשימוש קשה כל 7,500 ק"מ')
    # B5 steering linkage 60k/4y
    s.every('steering','inspect',60000,'מוטות היגוי, אטמים וכיסויים (כל 60,000 ק"מ או 4 שנים)')
    # B6 MT oil level 15k
    s.every('manual_gearbox_oil','inspect',15000,'גיר ידני: בדיקת מפלס')
    # B12 exhaust
    s.every('exhaust','inspect',30000,'דליפות גזים וחיבורי הצנרת')
    # C1 pedals, C2 parking brake, C3 air purifier filter
    s.every('pedals','inspect',15000,'חופש דוושת הבלם ודוושת המצמד')
    s.every('parking_brake','inspect',15000,'מהלך ידית בלם היד')
    s.every('cabin_filter','replace',15000,'מסנן מטהר האוויר (מזגן)')
    # D1 tyres
    s.every('tires','inspect',30000,'בלאי לא אחיד')
    # D3 brake hoses/pipes
    s.every('brake_lines','inspect',30000)
    # D4 pads/discs
    s.every('brake_pads','inspect',15000,'רפידות ודיסקים; בשימוש קשה כל 7,500 ק"מ')
    s.every('brake_discs','inspect',15000)
    # D5 drums
    s.every('brake_drums','inspect',30000,'נעלי בלם ותופים; בשימוש קשה כל 15,000 ק"מ')
    # D6 fuel hoses
    s.every('fuel_lines','inspect',30000)
    # E2 ATF change 2WD 90k/6y, E1 level 15k
    s.every('transmission_oil','replace',90000,gearbox_note)
    s.every('transmission_oil','inspect',15000,'גיר אוטומטי: בדיקת מפלס')
    # E3/E4 oil + filter
    s.every('engine_oil','replace',15000,'כל 15,000 ק"מ או 12 חודשים; בשימוש קשה כל 7,500 ק"מ')
    s.every('oil_filter','replace',15000)
    # E5/E6/E8 + F2
    s.every('diagnostics','inspect',15000,'בדיקת סל"ד סרק, ריכוז CO, מערכת EGR ונסיעת מבחן')
    # long interval
    s.li('timing_belt','replace',every_km=90000,note='רצועת תזמון כל 90,000 ק"מ (ללא מגבלת זמן בטבלה)')
    s.li('fuel_filter','replace',every_km=150000,every_months=120,note='מסנן דלק (בנזין) כל 150,000 ק"מ או 10 שנים')
    s.li('manual_gearbox_oil','replace',every_km=105000,every_months=84,note='גיר ידני בלבד: כל 105,000 ק"מ או 7 שנים; בשימוש קשה כל 45,000 ק"מ או 3 שנים')
    s.time('body_underside','inspect',12,'בדיקת נזקים במרכב פעם בשנה')

# ---------------- Lancer CS 4G18 ----------------
s=S('mitsubishi-lancer-2004-2009-1.6','Mitsubishi','מיצובישי','Lancer','לנסר','CS (Lancer IX / Lancer Classic)',(2004,2009),['1.6 (4G18)'],'petrol',IMP,
    15000,12,'לפי לוח התחזוקה של מיצובישי אירופה: טיפול כל 15,000 ק"מ או 12 חודשים, המוקדם; בשימוש קשה שמן ומסנן כל 7,500 ק"מ',180000)
build(s,'גיר אוטומטי (הנעה קדמית): החלפה כל 90,000 ק"מ או 6 שנים; בשימוש קשה כל 45,000 ק"מ או 3 שנים')
s.src(URL_ZIP,'manufacturer',SRC_NOTE)
s.src(URL_PAGE,'other','דף האתר mmc-manuals.ru שמקשר לספרי השירות של לנסר IX לאירופה (MY2004, MY2005, MY2006)')
s.specs={'engine_oil':'ACEA A1/A2/A3 או API SG ומעלה','timing':'רצועת תזמון, החלפה כל 90,000 ק"מ'}
notes=('לא נמצא ספר עברי של כלמוביל ללנסר הדור הזה (CS, מנוע 1.6 4G18). '
       'הלוח לקוח מספר הבדיקות והתחזוקה של מיצובישי אירופה מספטמבר 2005, מהשורות שמסומנות ללנסר. '
       'הטבלה כתובה כמרווחים ("כל X ק"מ או Y שנים") ולא כגריד, ולכן הגריד נבנה מהמרווחים עד 180,000 ק"מ. '
       'מהדורת אוגוסט 2003 של אותו ספר (גריד עד 300,000 ק"מ) מראה את אותם מרווחים. '
       'ברשימה גם בדיקת כבלי הצתה, סל"ד סרק, CO ו-EGR. רצועת התזמון מוחלפת כל 90,000 ק"מ. '
       'בשימוש קשה (אבק, דרכים משובשות, עיר בחום מעל 32 מעלות, מוניות, גרירה) שמן ומסנן כל 7,500 ק"מ, בדיקת מסנן אוויר ובלמים כל 7,500, שמן גיר ידני כל 45,000 ונוזל גיר אוטומטי כל 45,000 ק"מ.')
s.write('draft',notes)
rule('Mitsubishi',['LANCER'],(2004,2009),'mitsubishi-lancer-2004-2009-1.6',engine_codes=['4G18'])

# ---------------- Grandis 4G69 (sister) ----------------
g=S('mitsubishi-grandis-2005-2011-2.4','Mitsubishi','מיצובישי','Grandis','גרנדיס','NA',(2005,2011),['2.4 MIVEC (4G69)'],'petrol',IMP,
    15000,12,'לפי לוח התחזוקה הכללי של מיצובישי אירופה: טיפול כל 15,000 ק"מ או 12 חודשים, המוקדם; בשימוש קשה שמן ומסנן כל 7,500 ק"מ',180000)
build(g,'גיר אוטומטי: החלפה כל 90,000 ק"מ או 6 שנים (שורת הנעה קדמית בטבלה); בשימוש קשה כל 45,000 ק"מ או 3 שנים')
g.src(URL_ZIP,'manufacturer',SRC_NOTE+'. הטבלה משותפת לכל דגמי מיצובישי אירופה; לגרנדיס לא נמצאה מהדורה משלה')
g.src(URL_OUT,'manufacturer','אותה טבלה במהדורה של אאוטלנדר CU (מאי 2003, קובץ CHASSIS/PDI_03/pdi-engels-02.pdf עמ׳ 2-3 עד 2-6, גריד עד 300,000 ק"מ), עם מנועי 4G6 כולל 4G69: אותם מרווחים לשורות המנוע')
g.src('https://mmc-manuals.ru/Mitsubishi_Grandis:_Service_Manuals','other','ספר השירות של גרנדיס 2004 (WM) וספר השירות 2008 באתר אינם כוללים לוח תחזוקה; גם ספר הבעלים האירופי (procarmanuals, OXPE10E1) מפנה לתחנת השירות בלי לוח')
g.specs={'engine_oil':'ACEA A1/A2/A3 או API SG ומעלה','timing':'רצועת תזמון, החלפה כל 90,000 ק"מ'}
gnotes=('לא נמצא ספר עברי של כלמוביל לגרנדיס, וגם לא לוח תחזוקה ייעודי לגרנדיס. '
        'הלוח לקוח מטבלת הבדיקות והתחזוקה הכללית של מיצובישי אירופה (ספטמבר 2005), שמכסה את כל הדגמים ומסמנת לכל דגם את השורות שלו. '
        'נלקחו השורות של לנסר עם הנעה קדמית וגיר אוטומטי, והושוו לגרסת אאוטלנדר של אותה טבלה עם מנוע 4G69. לכן זו טיוטה לפי דגם אחות. '
        'למנוע 4G69 יש רצועת תזמון (כל 90,000 ק"מ) ומכווני שסתומים הידראוליים, ולכן אין בדיקת שסתומים. '
        'יש לברר במוסך את מרווח נוזל הגיר האוטומטי של הגרנדיס. '
        'בשימוש קשה שמן ומסנן כל 7,500 ק"מ, בדיקת מסנן אוויר ובלמים כל 7,500 ונוזל גיר אוטומטי כל 45,000 ק"מ.')
g.write('draft',gnotes)
rule('Mitsubishi',['GRANDIS'],(2005,2011),'mitsubishi-grandis-2005-2011-2.4',engine_codes=['4G69'])
save_rules('rules_mitsubishi.json')
