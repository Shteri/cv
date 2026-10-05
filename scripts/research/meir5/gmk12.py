from common import *
# Service I / II tables of the Korean/European-built Chevrolets in the Israeli books (Cruze J300, Trax, Orlando)
def svc(km, extra, diesel=False, lights=True):
    II = (km // 15000) % 2 == 0
    it = [
        I('engine_oil','replace', 'דיזל: פעם בשנה או כשמוצג קוד 82 (חיי שמן) במחשב' if diesel else None), I('oil_filter','replace'),
        I('body_underside','inspect','בדיקה לאיתור נזילות ונזקים'),
        I('air_filter','inspect'),
        I('tires','inspect','לחץ אוויר ובלאי'),
        I('brake_pads','inspect'), I('brake_discs','inspect'), I('brake_lines','inspect'), I('parking_brake','inspect'),
        I('coolant','inspect','מפלס'), I('washer_fluid','inspect','מפלס'),
        I('suspension','inspect'), I('steering','inspect','כולל הגה כוח'),
        I('wipers','inspect'),
        I('drive_belt','inspect'),
    ]
    if lights: it.append(I('lights','inspect','תאורה חיצונית'))
    if II:
        it += [I('brake_fluid','replace'), I('cooling_system','inspect','כולל בדיקת לחץ וניקוי חיצוני של המצנן ומעבה המזגן'),
               I('coolant_hoses','inspect'),
               I('seat_belts','inspect','רכיבי מערכת הריסון'), I('cv_boots','inspect','רכיבי מערכת ההינע'),
               I('door_hinges','clean','סיכת צירים, מנעולים ותפסים')]
    for every, items in extra:
        if km % every == 0: it += items
    return {'km': km, 'items': it}
LIST_PAGE = {'url':'https://www.chevrolet.co.il/%D7%A9%D7%99%D7%A8%D7%95%D7%AA-%D7%A9%D7%91%D7%A8%D7%95%D7%9C%D7%98/%D7%A1%D7%A4%D7%A8-%D7%A8%D7%9B%D7%91/','kind':'importer','note':'דף ספרי הרכב באתר שברולט ישראל (נקרא דרך WebFetch; האתר חוסם curl)'}
IV = {'km':15000,'months':12,'note':'לפי ספר הנהג העברי של יו.אם.איי: טיפול כל 15,000 ק"מ או שנה, המוקדם מביניהם; טיפול I וטיפול II לסירוגין'}
INTRO = 'כל 15,000 ק"מ או שנה מתבצע טיפול I או טיפול II לסירוגין. בשניהם: החלפת שמן ומסנן, ובדיקת נזילות, מסנן אוויר, צמיגים, בלמים, מפלסי נוזלים, מתלים והיגוי, מגבים ותאורה ורצועות; וכן ביצוע טיפולים נוספים לפי הצורך ובדיקת קריאות חוזרות (ריקול). בטיפול II נוספים: החלפת נוזל בלמים, בדיקת מערכת הקירור, מערכת הריסון ורכיבי ההינע, וסיכת המרכב. אם המחשב מציג את קוד 82 (חיי שמן) והטיפול האחרון היה לפני 10 חודשים או יותר, מקדימים את הטיפול.'

# ---------------- Cruze J300 ----------------
cab = [I('cabin_filter','replace','או כל שנתיים')]
af  = [I('air_filter','replace','או כל 4 שנים'), I('spark_plugs','replace','או כל 4 שנים')]
cruze = {
 'id':'chevrolet-cruze-2009-2016-1.4-1.6-1.8','make':'Chevrolet','make_he':'שברולט','model':'Cruze','model_he':'קרוז',
 'generation':'J300','years':[2009,2016],'engines':['1.4 טורבו (A14NET/B14NET, LUJ)','1.6 (F16D4, LDE)','1.8 (F18D4, 2H0)'],'fuel':'petrol','importer':'יו.אם.איי',
 'interval':IV,'cycle_km':180000,
 'services':[svc(k,[(45000,cab),(60000,af)]) for k in range(15000,180001,15000)],
 'long_interval':[
   L('cabin_filter','replace', every_km=45000, every_months=24),
   L('air_filter','replace', every_km=60000, every_months=48),
   L('spark_plugs','replace', every_km=60000, every_months=48),
   L('coolant','replace', every_km=240000, every_months=60),
   L('transmission_oil','replace','גיר אוטומטי, תנאים רגילים', every_km=150000, every_months=120),
   L('transmission_oil','replace','גיר אוטומטי, תנאים קשים (פקקים בחום של 32 מעלות ומעלה, הרים, גרירה, מונית)', every_km=75000, every_months=60),
   L('drive_belt','replace','מנועי 1.6 ו-1.8 (LDE, 2H0) עם מותחן רצועה', every_km=90000, every_months=120),
   L('timing_belt','replace','מנועי 1.6 ו-1.8 (LDE, 2H0): רצועת תזמון', every_km=150000, every_months=120),
   L('valve_clearance','inspect','מנועי 1.6 ו-1.8 (LDE, 2H0); כיוון לפי הצורך', every_km=150000, every_months=120),
   L('timing_belt','replace','מנוע 1.4 טורבו (LUJ): שרשרת תזמון', every_km=240000, every_months=120),
 ],
 'specs':{'engine_oil':'שמן במפרט dexos2, צמיגות SAE 5W-30','_note':'נבדק מול ספר הנהג העברי של היבואן (2015)'},
 'sources':[
   {'url':CHEV+'rw4i4teg/קרוז-2015.pdf','kind':'importer','note':'ספר נהג שברולט קרוז 2015 (Cruze EU he-IL), יו.אם.איי, "טיפול ותחזוקה" עמ\' 205-210'},
   {'url':CHEV+'ixwpdatt/קרוז-2016.pdf','kind':'importer','note':'ספר נהג קרוז 2016: עמודי התחזוקה זהים לספר 2015'},
   LIST_PAGE],
 'status':'reviewed',
 'notes':'הלוח לקוח מספרי הנהג העבריים של יו.אם.איי לקרוז 2015-2016 (דור J300; קודי GM בספר: LUJ = 1.4 טורבו, LDE = 1.6, 2H0 = 1.8). '+INTRO+' טבלת המרווחים: מסנן אבקנים כל 45,000 או שנתיים, מסנן אוויר ומצתים כל 60,000 או 4 שנים, נוזל קירור כל 240,000 או 5 שנים, שמן גיר אוטומטי כל 150,000 (75,000 בתנאים קשים). במנועי 1.6/1.8 יש רצועת תזמון (150,000) ובדיקת מרווח שסתומים; ב-1.4 טורבו שרשרת (240,000). לשנים 2009-2014 לא נמצא ספר עברי ולכן הוחל לוח 2015-2016 של אותו דור ומנועים. שורות הדיזל שבספר (מסנן סולר, מנוע LNP) לא נכללו כי קרוז דיזל לא נמצא במאגר הרישוי.'
}
write(cruze)

# ---------------- Trax 1.4T and 1.8 ----------------
af60 = [I('cabin_filter','replace','או כל שנתיים'), I('air_filter','replace','או כל 4 שנים'), I('spark_plugs','replace','או כל 4 שנים')]
trax_common_long = [
   L('cabin_filter','replace','בספר 2020: 30,000 ק"מ רק לרוסיה; בישראל 60,000', every_km=60000, every_months=24),
   L('air_filter','replace', every_km=60000, every_months=48),
   L('spark_plugs','replace', every_km=60000, every_months=48),
   L('coolant','replace', every_km=240000, every_months=60),
   L('drive_belt','replace', every_km=90000, every_months=120),
   L('valve_clearance','inspect','כיוון לפי הצורך', every_km=150000, every_months=120),
]
trax14 = {
 'id':'chevrolet-trax-2013-2020-1.4-turbo','make':'Chevrolet','make_he':'שברולט','model':'Trax','model_he':'טראקס',
 'generation':'U200','years':[2013,2020],'engines':['1.4 טורבו (A14NET/B14NET)'],'fuel':'petrol','importer':'יו.אם.איי',
 'interval':IV,'cycle_km':60000,
 'services':[svc(k,[(60000,af60)]) for k in range(15000,60001,15000)],
 'long_interval': trax_common_long + [
   L('timing_belt','replace','שרשרת תזמון (מנוע 1.4 טורבו); הספר מציין גם רצועה כל 150,000 למנועים עם רצועה', every_km=240000, every_months=120),
   L('transmission_oil','replace','גיר אוטומטי, תנאים רגילים: לפי ספר 2015 בלבד; בספר 2020 אין החלפה בתנאים רגילים', every_km=150000, every_months=120),
   L('transmission_oil','replace','גיר אוטומטי, תנאים קשים (פקקים בחום של 32 מעלות ומעלה, הרים, גרירה, מונית): ספר 2015 75,000 או 5 שנים; ספר 2020 72,420 ק"מ', every_km=72420),
   L('transfer_case_oil','replace','דגמי הנעה כפולה (AWD), לפי ספר 2020', every_km=156000),
 ],
 'time_based':[T('ac_system','replace',84,'החלפת חומר הייבוש של המזגן כל 7 שנים (ספר 2020)')],
 'specs':{'_note':'נבדק מול ספרי הנהג העבריים של היבואן (2015, 2020)'},
 'sources':[
   {'url':CHEV+'v4zjjnqv/טראקס-2015.pdf','kind':'importer','note':'ספר נהג שברולט טראקס 2015, יו.אם.איי, פרק 11 עמ\' 11-2 עד 11-6 (קובץ עמ\' 252-256)'},
   {'url':CHEV+'ibtcfztg/טראקס-2020.pdf','kind':'importer','note':'ספר נהג טראקס 2020, עמ\' 271-276 (אותו לוח I/II; שינויים בגיר האוטומטי, תיבת העברה ומייבש המזגן)'},
   {'url':CHEV+'xj0bmqz3/טראקס-2018.pdf','kind':'importer','note':'ספר נהג טראקס 2018, עמ\' 282: מאשר טיפול כל 15,000 ק"מ או שנה (אין בו טבלה)'},
   LIST_PAGE],
 'status':'reviewed',
 'notes':'הלוח לקוח מספרי הנהג העבריים של יו.אם.איי לטראקס 2015 ו-2020. '+INTRO+' טבלת המרווחים בספר: מסנן אבקנים כל 60,000 או שנתיים, מסנן אוויר ומצתים כל 60,000 או 4 שנים, נוזל קירור כל 240,000 או 5 שנים, רצועת עזר כל 90,000 או 10 שנים, בדיקת מרווח שסתומים כל 150,000. הספר מונה גם רצועת תזמון (150,000) וגם שרשרת (240,000) בלי לציין מנוע; לפי ספר הקרוז של אותו יבואן, מנוע 1.4 טורבו (LUJ) הוא בעל שרשרת, ולכן נרשמה כאן השרשרת. ספר 2018 אינו כולל טבלה ומפנה למוסך.'
}
write(trax14)
trax18 = dict(trax14)
trax18.update({
 'id':'chevrolet-trax-2013-2016-1.8','years':[2013,2016],'engines':['1.8 (F18D4)'],
 'long_interval': trax_common_long + [
   L('timing_belt','replace','רצועת תזמון (מנוע 1.8)', every_km=150000, every_months=120),
   L('transmission_oil','replace','גיר אוטומטי, תנאים רגילים', every_km=150000, every_months=120),
   L('transmission_oil','replace','גיר אוטומטי, תנאים קשים (פקקים בחום של 32 מעלות ומעלה, הרים, גרירה, מונית)', every_km=75000, every_months=60),
 ],
 'time_based':[],
 'specs':{'_note':'נבדק מול ספר הנהג העברי של היבואן (2015)'},
 'sources':[
   {'url':CHEV+'v4zjjnqv/טראקס-2015.pdf','kind':'importer','note':'ספר נהג שברולט טראקס 2015, יו.אם.איי, פרק 11 עמ\' 11-2 עד 11-6 (קובץ עמ\' 252-256); נתוני מנוע 1.8 בספר'},
   LIST_PAGE],
 'notes':'הלוח לקוח מספר הנהג העברי של יו.אם.איי לטראקס 2015, שמכסה גם את מנוע 1.8. '+INTRO+' טבלת המרווחים: מסנן אבקנים כל 60,000 או שנתיים, מסנן אוויר ומצתים כל 60,000 או 4 שנים, נוזל קירור כל 240,000 או 5 שנים, שמן גיר אוטומטי כל 150,000 (75,000 בתנאים קשים), רצועת עזר כל 90,000, רצועת תזמון ובדיקת מרווח שסתומים כל 150,000. השיוך של רצועת התזמון למנוע 1.8 מבוסס על ספר הקרוז של אותו יבואן (2H0 = רצועה). לשנים 2013-2014 הוחל ספר 2015 (אותו דור ומנוע).'
})
write(trax18)

# ---------------- Orlando ----------------
ocab=[I('cabin_filter','replace','או כל שנתיים')]
oaf=[I('air_filter','replace','או כל 4 שנים'), I('spark_plugs','replace','או כל 4 שנים')]
orl_src=[
   {'url':CHEV+'vwapt4hx/אורלנדו-2015.pdf','kind':'importer','note':'ספר נהג שברולט אורלנדו 2015, יו.אם.איי, "טיפול ותחזוקה" עמ\' 210-216; נתוני מנוע עמ\' 221-226 (LUJ, 2H0, LNP)'},
   {'url':CHEV+'pvpj4zwa/אורלנדו-2018.pdf','kind':'importer','note':'ספר נהג אורלנדו 2018, עמ\' 211-215: אותו לוח'},
   LIST_PAGE]
orl = {
 'id':'chevrolet-orlando-2014-2018-1.4-turbo','make':'Chevrolet','make_he':'שברולט','model':'Orlando','model_he':'אורלנדו',
 'generation':'J309','years':[2014,2018],'engines':['1.4 טורבו (A14NET/B14NET, LUJ)'],'fuel':'petrol','importer':'יו.אם.איי',
 'interval':IV,'cycle_km':180000,
 'services':[svc(k,[(45000,ocab),(60000,oaf)]) for k in range(15000,180001,15000)],
 'long_interval':[
   L('cabin_filter','replace', every_km=45000, every_months=24),
   L('air_filter','replace', every_km=60000, every_months=48),
   L('spark_plugs','replace', every_km=60000, every_months=48),
   L('coolant','replace', every_km=240000, every_months=60),
   L('transmission_oil','replace','גיר אוטומטי, תנאים רגילים', every_km=150000),
   L('transmission_oil','replace','גיר אוטומטי, תנאים קשים', every_km=75000),
   L('drive_belt','replace','ברכב עם רצועה נמתחת', every_km=90000, every_months=120),
   L('timing_belt','replace','שרשרת תזמון למנוע 1.4 טורבו (LUJ), לפי ספר הקרוז של היבואן. ספר האורלנדו כותב באופן כללי "מנוע בנזין: רצועת תזמון כל 150,000 ק\"מ / 10 שנים", שמתאים למנוע 1.8 (2H0)', every_km=240000, every_months=120),
 ],
 'specs':{'oil_capacity':'מנוע 1.4 טורבו (LUJ): 4.0 ליטר כולל מסנן','tire_pressure':'2.4 בר מלפנים ומאחור (2.7 בר במצב ECO)','_note':'נבדק מול ספר הנהג העברי של היבואן (2015)'},
 'sources':orl_src,'status':'reviewed',
 'notes':'הלוח לקוח מספרי הנהג העבריים של יו.אם.איי לאורלנדו 2015 ו-2018 (זהים). '+INTRO+' טבלת המרווחים: מסנן אבקנים כל 45,000 או שנתיים, מסנן אוויר ומצתים כל 60,000 או 4 שנים, נוזל קירור כל 240,000 או 5 שנים, שמן גיר אוטומטי כל 150,000 (75,000 בתנאים קשים), רצועת עזר כל 90,000. סטייה מהספר: הספר רושם לכל מנועי הבנזין רצועת תזמון כל 150,000, אבל ספר הקרוז של אותו יבואן מציין שבמנוע LUJ יש שרשרת (240,000), ולכן רשמנו שרשרת. בדיקת מרווח שסתומים בספר היא רק למנוע 2H0 ולכן לא נכללה. לשנים 2011-2014 הוחל ספר 2015.'
}
write(orl)
orld = {
 'id':'chevrolet-orlando-2012-2015-2.0-diesel','make':'Chevrolet','make_he':'שברולט','model':'Orlando','model_he':'אורלנדו',
 'generation':'J309','years':[2012,2015],'engines':['2.0 דיזל (Z20D1, LNP)'],'fuel':'diesel','importer':'יו.אם.איי',
 'interval':IV,'cycle_km':180000,
 'services':[svc(k,[(45000,ocab),(60000,[I('air_filter','replace','או כל 4 שנים'), I('fuel_filter','replace','או כל שנתיים')])],diesel=True) for k in range(15000,180001,15000)],
 'long_interval':[
   L('cabin_filter','replace', every_km=45000, every_months=24),
   L('air_filter','replace', every_km=60000, every_months=48),
   L('fuel_filter','replace','בביו-דיזל, אבק, שטח או גרירה ממושכת ייתכן שיידרש לעתים קרובות יותר', every_km=60000, every_months=24),
   L('coolant','replace', every_km=240000, every_months=60),
   L('transmission_oil','replace','גיר אוטומטי, תנאים רגילים', every_km=150000),
   L('transmission_oil','replace','גיר אוטומטי, תנאים קשים', every_km=75000),
   L('drive_belt','replace','ברכב עם רצועה נמתחת', every_km=90000, every_months=120),
   L('timing_belt','replace','מנוע דיזל: שרשרת תזמון', every_km=240000, every_months=120),
 ],
 'time_based':[T('engine_oil','replace',12,'במנוע דיזל: פעם בשנה או כשמוצג קוד 82 במחשב, המוקדם מביניהם')],
 'specs':{'oil_capacity':'מנוע 2.0 דיזל (LNP): 5.4 ליטר כולל מסנן','tire_pressure':'2.4 בר מלפנים ומאחור (2.7 בר במצב ECO)','_note':'נבדק מול ספר הנהג העברי של היבואן (2015)'},
 'sources':orl_src,'status':'reviewed',
 'notes':'הלוח לקוח מספרי הנהג העבריים של יו.אם.איי לאורלנדו 2015 ו-2018, שמכסים גם את מנוע 2.0 דיזל (קוד GM: LNP; ברישוי Z20D1). '+INTRO+' בדיזל השמן מוחלף פעם בשנה או כשמוצג קוד 82 במחשב, המוקדם מביניהם. טבלת המרווחים: מסנן אבקנים כל 45,000 או שנתיים, מסנן אוויר כל 60,000 או 4 שנים, מסנן סולר כל 60,000 או שנתיים, נוזל קירור כל 240,000 או 5 שנים, שמן גיר אוטומטי כל 150,000 (75,000 בתנאים קשים), רצועת עזר כל 90,000, שרשרת תזמון בדיזל כל 240,000. לשנים 2012-2014 הוחל ספר 2015.'
}
write(orld)
