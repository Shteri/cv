from common import *
# ---------- Spark M400 (2016-2023), Israeli books 2016-2017 / 2019-2020 / 2022 ----------
def m400_service(km):
    it = [
        I('engine_oil','replace','לפי הודעת "החלף שמן מנוע" במחשב הרכב, ולפחות פעם בשנה'),
        I('oil_filter','replace','יחד עם השמן'),
        I('cabin_filter','replace'),
        I('evap_system','inspect','מכל אדי דלק וצינורות האדים'),
        I('drive_belt','inspect'),
        I('coolant_hoses','inspect','צינורות וחיבורי מערכת הקירור'),
        I('fuel_lines','inspect'),
        I('exhaust','inspect','צינור הפליטה ותליותיו'),
        I('brake_pads','inspect','קדמיים ואחוריים'),
        I('brake_discs','inspect','קדמיים'),
        I('brake_drums','inspect','תופים ונעליים אחוריים (או דיסקים אחוריים, לפי הדגם)'),
        I('parking_brake','inspect','כבל בלם היד וחיבוריו'),
        I('brake_lines','inspect','כולל מגבר הבלמים'),
        I('body_underside','inspect','הידוק ברגים ואומים של השלדה והגחון'),
        I('tires','inspect','מצב ולחץ אוויר; הספר ממליץ לבדוק גם בכל תדלוק או לפחות פעם בחודש'),
        I('steering','inspect','ההגה ומוטות ההיגוי'),
        I('cv_boots','inspect','מגני גל ההינע'),
        I('seat_belts','inspect','חגורות, אבזמים ונקודות עיגון'),
        I('door_hinges','clean','סיכת מנעולים, צירים ותפס מכסה המנוע'),
    ]
    if km % 60000 == 0:
        it += [I('air_filter','replace'), I('spark_plugs','replace'),
               I('brake_fluid','replace','או כל שנתיים, המוקדם מביניהם')]
    return {'km': km, 'items': it}
spark16 = {
 'id':'chevrolet-spark-2016-2022-1.4','make':'Chevrolet','make_he':'שברולט','model':'Spark','model_he':'ספארק',
 'generation':'M400','years':[2016,2023],'engines':['1.0 (L5Q)','1.4 (LV7)'],'fuel':'petrol','importer':'יו.אם.איי',
 'interval':{'km':15000,'months':12,'note':'לפי ספר הנהג העברי של יו.אם.איי: טיפול כל 15,000 ק"מ או שנה, המוקדם מביניהם; שמן ומסנן לפי הודעת המחשב ולפחות פעם בשנה'},
 'cycle_km':60000,
 'services':[m400_service(k) for k in (15000,30000,45000,60000)],
 'long_interval':[
   L('brake_fluid','replace','לפי הלוח: כל 60,000 ק"מ או שנתיים', every_km=60000, every_months=24),
   L('coolant','replace', every_km=240000, every_months=60),
   L('drive_belt','replace','בספרי 2016-2020: החלפה כל 240,000 ק"מ או 10 שנים; בספר 2022 הסעיף מנוסח כבדיקה חזותית באותו מרווח', every_km=240000, every_months=120),
   L('manual_gearbox_oil','replace','לתיבה ידנית בלבד (מופיע בספרי 2016-2020)', every_km=160000, every_months=120),
   L('cvt_oil','replace','בתנאים רגילים אין צורך בבדיקה או החלפה; החלפה כל 72,000 ק"מ רק בנסיעה בעיקר בתנאים קשים (פקקים בחום של 30 מעלות ומעלה, דרכים הרריות, מונית/שירותי משלוחים)', every_km=72000),
   L('tire_rotation','rotate','סבב צמיגים כל 12,000 ק"מ (לא תלוי בלוח ה-15,000)', every_km=12000),
 ],
 'time_based':[
   T('engine_oil','replace',12,'שמן ומסנן לפחות פעם בשנה, או מוקדם יותר לפי הודעת המחשב'),
   T('brake_fluid','replace',24,'כל שנתיים, אם לא הגיעו ל-60,000 ק"מ'),
 ],
 'specs':{
   'engine_oil':'שמן במפרט dexos1, צמיגות SAE 5W-20 (בקור קיצוני מתחת ל-25- מעלות: 0W-20/0W-30)',
   'fuel':'בנזין 95 אוקטן',
   '_note':'נבדק מול ספר הנהג העברי של היבואן (2016-2017)'
 },
 'sources':[
   {'url':CHEV+'1b5hrpl4/ספארק-2016-2017.pdf','kind':'importer','note':'ספר נהג שברולט ספארק 2016-2017, יו.אם.איי (GMK-Localizing-Israel), טבלת "טיפול ותחזוקה" עמ\' 216-219, נתוני מנוע עמ\' 224'},
   {'url':CHEV+'biqhgacl/ספארק-2019-2020.pdf','kind':'importer','note':'ספר נהג ספארק 2019-2020, עמ\' 233-236 (אותה טבלה; נוספה הערה על מסנן המזגן)'},
   {'url':CHEV+'bszhpelj/ספארק-2022-new.pdf','kind':'importer','note':'ספר נהג ספארק 2022, עמ\' 181-184 (מנוע 1.4 בלבד, בלי שורת גיר ידני)'},
   {'url':'https://www.chevrolet.co.il/%D7%A9%D7%99%D7%A8%D7%95%D7%AA-%D7%A9%D7%91%D7%A8%D7%95%D7%9C%D7%98/%D7%A1%D7%A4%D7%A8-%D7%A8%D7%9B%D7%91/','kind':'importer','note':'דף ספרי הרכב באתר שברולט ישראל (נקרא דרך WebFetch; האתר חוסם curl)'}
 ],
 'status':'reviewed',
 'notes':'הלוח מועתק מספרי הנהג העבריים של יו.אם.איי לספארק מהדור M400 (2016-2022), שבהם טבלה של 4 עמודות: 15/30/45/60 אלף ק"מ או 1-4 שנים, והיא חוזרת על עצמה. בלוח עצמו אין סימון של שמן בכל עמודה: השמן והמסנן מוחלפים לפי הודעת המחשב ולפחות פעם בשנה, ולכן רשמנו אותם בכל טיפול שנתי עם הערה. מסנן המזגן מסומן להחלפה בכל עמודה; מסנן אוויר ומצתים בעמודת 60,000 בלבד. כיוון גלגלים: לפי הצורך. גיר CVT: אין החלפה בתנאים רגילים. הספר מכסה גם את מנוע 1.0 (L5Q) של 2016-2018. בתנאי נסיעה קשים (התנעות קרות, עצור-סע, אבק, הרים) הספר ממליץ לבצע חלק מהבדיקות לעתים קרובות יותר.'
}
write(spark16)

# ---------- Spark M300 (2010-2015), Israeli book 2015 ----------
def m300_service(km):
    II = (km // 15000) % 2 == 0
    it = [
        I('engine_oil','replace'), I('oil_filter','replace'),
        I('body_underside','inspect','בדיקה לאיתור נזילות ונזקים'),
        I('air_filter','inspect'),
        I('tires','inspect','לחץ אוויר ובלאי'),
        I('brake_pads','inspect'), I('brake_discs','inspect'), I('brake_drums','inspect'), I('brake_lines','inspect'), I('parking_brake','inspect'),
        I('coolant','inspect','מפלס'), I('washer_fluid','inspect','מפלס'),
        I('suspension','inspect'), I('steering','inspect','כולל הגה כוח'),
        I('wipers','inspect'),
        I('drive_belt','inspect'),
        I('cabin_filter','replace','או פעם בשנה'),
        I('pedals','inspect','חופש דוושות המצמד והבלם'),
        I('transmission_oil','inspect','גיר אוטומטי: בדיקת השמן'),
    ]
    if II:
        it += [I('brake_fluid','replace'), I('cooling_system','inspect','כולל צינורות, בדיקת לחץ וניקוי המצנן ומעבה המזגן'),
               I('coolant_hoses','inspect'),
               I('seat_belts','inspect','רכיבי מערכת הריסון'), I('cv_boots','inspect','רכיבי מערכת ההינע'),
               I('door_hinges','clean','סיכת צירים, מנעולים ותפסים')]
    if km % 30000 == 0: it.append(I('spark_plugs','replace','או כל שנתיים'))
    if km % 45000 == 0: it.append(I('electrical_system','replace','החלפת כבלי ההצתה (ברכב ללא בקרת יציבות אלקטרונית), או כל 3 שנים'))
    if km % 60000 == 0: it.append(I('air_filter','replace','או כל 4 שנים'))
    # avoid duplicate air_filter inspect+replace is fine (different action)
    return {'km': km, 'items': it}
spark15 = {
 'id':'chevrolet-spark-2010-2015-1.0-1.2','make':'Chevrolet','make_he':'שברולט','model':'Spark','model_he':'ספארק',
 'generation':'M300','years':[2010,2015],'engines':['1.0 (B10D1/LMT)','1.2 (B12D1/LMU)'],'fuel':'petrol','importer':'יו.אם.איי',
 'interval':{'km':15000,'months':12,'note':'לפי ספר הנהג העברי של יו.אם.איי: טיפול כל 15,000 ק"מ או שנה; טיפול I וטיפול II לסירוגין'},
 'cycle_km':180000,
 'services':[m300_service(k) for k in range(15000,180001,15000)],
 'long_interval':[
   L('spark_plugs','replace', every_km=30000, every_months=24),
   L('electrical_system','replace','כבלי הצתה, ברכב ללא בקרת יציבות אלקטרונית', every_km=45000, every_months=36),
   L('air_filter','replace', every_km=60000, every_months=48),
   L('coolant','replace', every_km=240000, every_months=60),
   L('manual_gearbox_oil','replace', every_km=150000, every_months=120),
   L('transmission_oil','replace','גיר אוטומטי: בדיקה בכל טיפול; החלפה כל 75,000 ק"מ בתנאים קשים (פקקים בחום של 32 מעלות ומעלה, הרים, גרירה, מונית)', every_km=75000),
   L('timing_belt','replace','שרשרת תזמון (המפתח במאגר הוא "רצועת תזמון")', every_km=240000, every_months=120),
   L('valve_clearance','inspect','בדיקה וכיוון לפי הצורך', every_km=150000, every_months=120),
 ],
 'time_based':[T('cabin_filter','replace',12,'מסנן אבקנים פעם בשנה, אם לא הגיעו ל-15,000 ק"מ')],
 'specs':{'_note':'נבדק מול ספר הנהג העברי של היבואן (2015)'},
 'sources':[
   {'url':CHEV+'hdqneopi/ספארק-2015.pdf','kind':'importer','note':'ספר נהג שברולט ספארק 2015, יו.אם.איי (GMK-Localizing-Israel), פרק 11 "טיפול ותחזוקה" עמ\' 11-2 עד 11-6 (קובץ עמ\' 232-236), נתוני מנוע עמ\' 12-3'},
   {'url':'https://www.chevrolet.co.il/%D7%A9%D7%99%D7%A8%D7%95%D7%AA-%D7%A9%D7%91%D7%A8%D7%95%D7%9C%D7%98/%D7%A1%D7%A4%D7%A8-%D7%A8%D7%9B%D7%91/','kind':'importer','note':'דף ספרי הרכב באתר שברולט ישראל'}
 ],
 'status':'reviewed',
 'notes':'הלוח לקוח מספר הנהג העברי של יו.אם.איי לספארק 2015 (דור M300, מנועי 1.0 ו-1.2). כל 15,000 ק"מ או שנה מתבצע טיפול I או טיפול II לסירוגין: בשניהם החלפת שמן ומסנן ובדיקות כלליות; בטיפול II נוספים החלפת נוזל בלמים ובדיקת מערכת הקירור, מערכת הריסון ומערכת ההינע וסיכת המרכב. טבלת המרווחים: מסנן אבקנים בכל טיפול, מצתים כל 30,000, כבלי הצתה כל 45,000, מסנן אוויר כל 60,000. הלוח כולל גם בדיקת קריאות חוזרות (ריקול) וביצוע טיפולים נוספים לפי הצורך. הספר הוא של שנת 2015; לשנים 2010-2014 (אותו דור ומנועים) לא נמצא ספר עברי, ולכן הוחל אותו לוח. רצועת עזר: אם הוחלפה, יש לבדוק ולכוון את המתיחה תוך 6 חודשים או 5,000 ק"מ.'
}
write(spark15)
