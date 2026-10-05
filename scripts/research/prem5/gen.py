import json, os
OUT='/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/prem5'
os.makedirs(OUT+'/registry', exist_ok=True)

def write(d):
    with open(f"{OUT}/{d['id']}.json",'w',encoding='utf-8') as f:
        json.dump(d,f,ensure_ascii=False,indent=2)

def grid(step, cycle, rules):
    """rules: list of (item, action, predicate(km) or list of km, note)"""
    services=[]
    for km in range(step, cycle+1, step):
        items=[]; seen=set()
        for r in rules:
            item,action,when=r[0],r[1],r[2]; note=r[3] if len(r)>3 else None
            ok = when(km) if callable(when) else (km in when)
            if not ok or item in seen: continue
            seen.add(item)
            it={'item':item,'action':action}
            if note: it['note']=note
            items.append(it)
        services.append({'km':km,'items':items})
    return services

every=lambda km: True
def mult(n): return lambda km: km % n == 0

# ---------------- TESLA ----------------
TCN='https://www.tesla.cn/ownersmanual/{m}/zh_cn/GUID-E95DAAD9-646E-4249-9930-B109ED7B1D91.html'
tesla_common_note=("טסלה אינה מגדירה טיפול תקופתי קבוע; ספר הבעלים מונה רק פריטים בודדים עם מרווח. הפריט היחיד לפי ק\"מ הוא סבב צמיגים כל 10,000 ק\"מ "
    "(או מוקדם יותר אם הפרש עומק החריץ בין הצמיגים מגיע ל-1.5 מ\"מ), ולכן הוא משמש כאן כמרווח הבסיסי. "
    "הערכים לקוחים מספר הבעלים הרשמי העדכני של טסלה (מהדורת התוכנה 2026.26, באתר tesla.cn - אותה מהדורה משמשת לרכבים מתוצרת שנחאי שמגיעים לישראל), "
    "כי tesla.com חסום מסביבת העבודה. ניקוי ושימון קליפרים (כל שנה או 20,000 ק\"מ) נדרש רק באזורים שמפזרים בהם מלח על הכבישים - לא רלוונטי בישראל. "
    "נוזל הקירור של הסוללה בדרך כלל אינו מוחלף לאורך חיי הרכב. רפידות, מצבר עזר ונוזלים מוחלפים לפי מצב.")

def tesla(id_, model, model_he, gen, years, engines, m_url, extra_tb, extra_note, old_sources):
    d={'id':id_,'make':'Tesla','make_he':'טסלה','model':model,'model_he':model_he,'generation':gen,'years':years,
       'engines':engines,'fuel':'electric','importer':'טסלה מוטורס ישראל',
       'interval':{'km':10000,'months':12,'note':'אין טיפול תקופתי קבוע; המרווח הוא סבב הצמיגים כל 10,000 ק"מ. 12 החודשים הם ערך תצוגה בלבד - בספר אין מרווח זמן לטיפול כללי'},
       'cycle_km':10000,
       'services':[{'km':10000,'items':[{'item':'tire_rotation','action':'rotate'},{'item':'tires','action':'inspect','note':'בדיקת לחץ ובלאי; הפרש עומק חריץ של 1.5 מ"מ מחייב סבב גם לפני 10,000 ק"מ'}]}],
       'long_interval':[],
       'time_based':[
          {'item':'cabin_filter','action':'replace','months':12,'note':'מסנן המזגן לתא הנוסעים - פעם בשנה (במהדורות ישנות של הספר: כל שנתיים)'},
          *extra_tb,
          {'item':'wipers','action':'replace','months':12,'note':'החלפת להבי מגבים פעם בשנה'},
          {'item':'brake_fluid','action':'inspect','months':48,'note':'בדיקת מצב נוזל הבלמים כל 4 שנים והחלפה לפי הצורך; בגרירה, בירידות ארוכות ובנהיגה ספורטיבית באקלים חם ולח - בתדירות גבוהה יותר'},
       ],
       'specs':{'battery':'סוללת מתח גבוה + סוללה/מצבר עזר במתח נמוך','_note':'טיוטה: ספר הבעלים הרשמי של טסלה (מהדורת סין), לא מסמך עברי של טסלה ישראל'},
       'sources':[{'url':m_url,'kind':'manufacturer','note':'ספר הבעלים הרשמי של טסלה (מהדורה סינית, גרסת תוכנה 2026.26.200.11), פרק "מרווחי שירות" (维修服务间隔); נפתח ישירות ב-curl ב-5.10.2026'}]+old_sources,
       'status':'draft',
       'notes':tesla_common_note+' '+extra_note}
    write(d)

tesla('tesla-model-3-2021-2026-ev','Model 3','מודל 3','Model 3 / Model 3 Highland',[2021,2026],['EV (3D1 / 3D3 / 3D5 / 3D6 / 3D7)'],
      TCN.format(m='model3'),
      [{'item':'ac_system','action':'replace','months':72,'note':'החלפת שקית הייבוש של מערכת המיזוג כל 6 שנים - מופיע רק במהדורות הקודמות של הספר (העתקים אירופי וצפון-אמריקאי, ראו מקורות); אינו מופיע במהדורה הנוכחית'}],
      'שינויים לעומת הטיוטה הקודמת: מסנן המזגן עבר משנתיים לשנה אחת, ונוספה החלפת מגבים שנתית - שניהם לפי המהדורה הרשמית הנוכחית. בדיקת נוזל הבלמים כל 4 שנים (במהדורה צפון-אמריקאית ישנה: כל שנתיים).',
      [{'url':'https://hamphi.com/en-eu/pages/tesla-original-guides/model-3-serviceintervall-for-fordon','kind':'other','note':'העתק מתורגם של פרק מרווחי הטיפול מהמהדורה האירופית הקודמת: שקית ייבוש 6 שנים, מסנן מזגן שנתיים'},
       {'url':'https://www.manualslib.com/manual/1765784/Tesla-Model-3.html?page=163','kind':'other','note':'מהדורה צפון-אמריקאית ישנה (עמ\' 162-163): נוזל בלמים כל שנתיים, שקית ייבוש 6 שנים'}])

tesla('tesla-model-y-2022-2026-ev','Model Y','מודל Y','Model Y / Model Y Juniper',[2022,2026],['EV (3D3 / 3D6 / 3D7 / 4D1 / 4D3)'],
      TCN.format(m='modely'),
      [{'item':'cabin_filter','action':'replace','months':12,'note':'שני מסנני HEPA ושני מסנני פחם פעיל (ברכב שמצויד בהם) - פעם בשנה'},
       {'item':'ac_system','action':'replace','months':48,'note':'החלפת שקית הייבוש של מערכת המיזוג כל 4 שנים - מופיע רק בהעתק של ספר 2023 (ראו מקורות); אינו מופיע במהדורה הנוכחית'}],
      'שינויים לעומת הטיוטה הקודמת: מסנן המזגן ומסנני HEPA/פחם - פעם בשנה (בספר 2023: שנתיים/3 שנים), בדיקת נוזל בלמים כל 4 שנים (בספר 2023: שנתיים), ונוספה החלפת מגבים שנתית. המהדורה הנוכחית כוללת גם את גרסת Juniper.',
      [{'url':'https://www.mycarusermanual.com/tesla/model-y/suv/2023/maintenance--maintenance-service-intervals','kind':'other','note':'העתק של ספר Model Y 2023: נוזל בלמים שנתיים, שקית ייבוש 4 שנים, מסנן מזגן שנתיים, HEPA שלוש שנים'}])

tesla('tesla-model-s-x-2021-2026-ev','Model S / Model X','מודל S / מודל X','Model S / Model X (Palladium, 2021 ואילך)',[2021,2026],['EV (3D8 / 5D1)'],
      TCN.format(m='models'),
      [{'item':'cabin_filter','action':'replace','months':12,'note':'מסנן HEPA (ב-Model X גם מסנן פחם פעיל) - פעם בשנה'}],
      'הלוח זהה ל-Model S ול-Model X; ההבדל היחיד הוא שב-Model X מוחלף בנוסף מסנן פחם פעיל. במקור נבדקו גם עמוד ה-Model X באותו ספר.',
      [{'url':TCN.format(m='modelx'),'kind':'manufacturer','note':'ספר הבעלים של Model X (אותה מהדורה): אותם מרווחים, ובנוסף מסנן פחם פעיל שנתי'}])

# ---------------- MITSUBISHI GRANDIS ----------------
ev=every; m30=mult(30000); m45=mult(45000); m60=mult(60000); m90=mult(90000)
GR='https://jdmfsm.info/Auto/Japan/Mitsubishi/Grandis/Manuals/Predelivery%20and%20Periodic%20Maintenance/5850NA4W_06_003ENG.pdf'
gr_rules=[
 ('engine_oil','replace',ev),('oil_filter','replace',ev),
 ('drive_belt','inspect',ev),
 ('air_filter','replace',m45,'מסנן אוויר: החלפה כל 45,000 ק"מ או 3 שנים'),('air_filter','inspect',ev),
 ('brake_fluid','replace',m30,'החלפה כל 30,000 ק"מ או שנתיים'),('brake_fluid','inspect',ev,'בדיקת מפלס'),
 ('battery_12v','inspect',ev),
 ('pedals','inspect',ev),('parking_brake','inspect',ev),
 ('cabin_filter','replace',ev),
 ('brake_pads','inspect',ev),('brake_discs','inspect',ev),
 ('transmission_oil','replace',m90,'החלפת נוזל גיר אוטומטי כל 90,000 ק"מ או 6 שנים (בתנאים קשים כל 45,000 או 3 שנים)'),('transmission_oil','inspect',ev,'בדיקת מפלס'),
 ('timing_belt','replace',m90,'רצועת תזמון (כולל רצועה B) כל 90,000 ק"מ'),
 ('spark_plugs','replace',m90,'מצתי פלטינה/אירידיום'),
 ('coolant','replace',m60,'החלפה כל 60,000 ק"מ או 4 שנים'),('coolant','inspect',m30,'בדיקת מפלס'),
 ('pcv_valve','inspect',m30),('coolant_hoses','inspect',m30),
 ('suspension','inspect',m30,'כולל מפרקים כדוריים'),('cv_boots','inspect',m30,'בתנאים קשים כל 7,500 ק"מ'),
 ('steering','inspect',m60),
 ('exhaust','inspect',m30),('tires','inspect',m30,'בדיקת בלאי לא אחיד'),
 ('brake_lines','inspect',m30),('brake_drums','inspect',m30,'בתנאים קשים כל 15,000'),('fuel_lines','inspect',m30),
]
write({'id':'mitsubishi-grandis-2005-2011-2.4','make':'Mitsubishi','make_he':'מיצובישי','model':'Grandis','model_he':'גרנדיס','generation':'NA4W',
 'years':[2005,2011],'engines':['2.4 MIVEC (4G69)'],'fuel':'petrol','importer':'כלמוביל',
 'interval':{'km':15000,'months':12,'note':'לפי לוח התחזוקה האירופי של מיצובישי לגרנדיס: 15,000 ק"מ או 12 חודשים, המוקדם; בתנאי שימוש קשים שמן ומסנן כל 7,500 ק"מ'},
 'cycle_km':180000,'services':grid(15000,180000,gr_rules),
 'long_interval':[{'item':'fuel_filter','action':'replace','every_km':150000,'every_months':120,'note':'מנוע בנזין'}],
 'time_based':[{'item':'body_underside','action':'inspect','months':12,'note':'בדיקת נזקים במרכב פעם בשנה'}],
 'specs':{'_note':'טיוטה: מסמך היצרן לשוק האירופי, לא ספר עברי של כלמוביל'},
 'sources':[{'url':GR,'kind':'manufacturer','note':'Mitsubishi Grandis (NA4W) Pre-delivery Inspection and Periodic Maintenance, מהדורת 2006, קבוצה 2 "Periodic Inspection and Maintenance Schedule" עמ\' 2-3 עד 2-6 (עמודי PDF 27-30); עותק במאגר jdmfsm.info'},
            {'url':'https://jdmfsm.info/Auto/Japan/Mitsubishi/Grandis/Manuals/Predelivery%20and%20Periodic%20Maintenance/5850NA4W_04_003ENG.pdf','kind':'manufacturer','note':'מהדורת 2004 של אותו מסמך: אותם מרווחים למנוע 4G69, ובנוסף בדיקת מערכת כריות האוויר אחרי 10 שנים'},
            {'url':'https://www.mitsubishi-israel.co.il/car_books/','kind':'importer','note':'בספריית ספרי הרכב של מיצובישי ישראל אין ספר לגרנדיס'}],
 'status':'draft',
 'notes':('טיוטה ממסמך היצרן (מיצובישי, שוק אירופה) לגרנדיס, לא ממסמך של כלמוביל. טיפול כל 15,000 ק"מ או שנה עם שמן, מסנן שמן ומסנן מזגן. '
  'מסנן אוויר מוחלף כל 45,000 ק"מ, נוזל בלמים כל 30,000 ק"מ או שנתיים, נוזל קירור כל 60,000 ק"מ או 4 שנים, רצועת תזמון ומצתים כל 90,000 ק"מ, '
  'נוזל גיר אוטומטי כל 90,000 ק"מ או 6 שנים, מסנן דלק כל 150,000 ק"מ או 10 שנים. בתנאים קשים: שמן ומסנן כל 7,500 ק"מ, בדיקת מסנן אוויר ובלמים כל 7,500. '
  'שורות הדיזל (מנוע BSY) והגיר הידני בטבלה לא הועתקו - בישראל נמכרה גרנדיס בנזין עם גיר אוטומטי. בדיקת מיסבי גלגל קדמיים כל 60,000 ק"מ, סל"ד סרק, CO, מערכת EGR ונסיעת מבחן מופיעות בטבלה ולא מופו לפריטים. '
  'בדיקת חופש שסתומים בטבלה חלה רק על מנועים ללא מכווני שסתומים הידראוליים, ולכן לא נכללה (ל-4G69 יש מכוונים הידראוליים). '
  'רכבי גפ"מ (הסבה) מכוסים באותו לוח; טיפול במערכת הגז אינו חלק מהלוח. גרסה זו מחליפה את הטיוטה הקודמת, שנבנתה מהטבלה הכללית של מיצובישי אירופה (שורות לנסר/אאוטלנדר), '
  'בלוח שנכתב לגרנדיס עצמה; היא גם עונה על השאלה שנשארה פתוחה שם: נוזל הגיר האוטומטי בגרנדיס (הנעה קדמית) מוחלף כל 90,000 ק"מ או 6 שנים.')})

# ---------------- MITSUBISHI OUTLANDER CW (upgrade) ----------------
OL='https://jdmfsm.info/Auto/Japan/Mitsubishi/Outlander/Manuals/2007/Service%20Manual%20PDF/Pre-Delivery%20Inspection/GR00000300-2.pdf'
ol_rules=[
 ('engine_oil','replace',ev),('oil_filter','replace',ev),
 ('drive_belt','inspect',ev),
 ('air_filter','replace',m45,'החלפה כל 45,000 ק"מ או 3 שנים'),('air_filter','inspect',ev),
 ('brake_fluid','replace',m30,'החלפה כל 30,000 ק"מ או שנתיים'),('brake_fluid','inspect',ev,'בדיקת מפלס'),
 ('battery_12v','inspect',ev),
 ('transfer_case_oil','inspect',ev,'4X4 בלבד - בדיקת מפלס'),
 ('pedals','inspect',ev),('parking_brake','inspect',ev),
 ('cabin_filter','replace',ev),
 ('brake_pads','inspect',ev),('brake_discs','inspect',ev),
 ('cvt_oil','replace',m90,'בטבלה: החלפת נוזל תיבה אוטומטית (4X4) כל 90,000 ק"מ או 6 שנים, בתנאים קשים כל 45,000; בישראל תיבת CVT'),('cvt_oil','inspect',ev,'בדיקת מפלס'),
 ('valve_clearance','inspect',ev,'לפי הטבלה - רק במנוע ללא מכווני שסתומים הידראוליים'),
 ('spark_plugs','replace',m90,'מצתי פלטינה/אירידיום'),
 ('coolant','replace',m60,'החלפה כל 60,000 ק"מ או 4 שנים'),('coolant','inspect',m30,'בדיקת מפלס'),
 ('differential_oil','replace',m90,'4X4: החלפה כל 90,000 ק"מ או 6 שנים (בתנאים קשים כל 45,000)'),('differential_oil','inspect',m30,'4X4 - דיפרנציאל קדמי ואחורי'),
 ('pcv_valve','inspect',m30),('coolant_hoses','inspect',m30),
 ('suspension','inspect',m30,'כולל מפרקים כדוריים'),('cv_boots','inspect',m30,'בתנאים קשים כל 7,500 ק"מ'),
 ('steering','inspect',m60),
 ('exhaust','inspect',m30),('tires','inspect',m30,'בדיקת בלאי לא אחיד'),
 ('brake_lines','inspect',m30),('brake_drums','inspect',m30,'בתנאים קשים כל 15,000'),('fuel_lines','inspect',m30),
]
write({'id':'mitsubishi-outlander-2007-2012-2.0-2.4','make':'Mitsubishi','make_he':'מיצובישי','model':'Outlander','model_he':'אאוטלנדר','generation':'CW (דור 2)',
 'years':[2007,2012],'engines':['2.0 MIVEC (4B11)','2.4 MIVEC (4B12)'],'fuel':'petrol','importer':'כלמוביל',
 'interval':{'km':15000,'months':12,'note':'לפי לוח התחזוקה האירופי של מיצובישי לאאוטלנדר 2007: 15,000 ק"מ או 12 חודשים, המוקדם; בתנאי שימוש קשים שמן ומסנן כל 7,500 ק"מ'},
 'cycle_km':180000,'services':grid(15000,180000,ol_rules),
 'long_interval':[
   {'item':'fuel_filter','action':'replace','every_km':150000,'every_months':120,'note':'מנוע בנזין'},
   {'item':'transfer_case_oil','action':'replace','every_km':75000,'every_months':60,'note':'4X4 בלבד'}],
 'time_based':[{'item':'body_underside','action':'inspect','months':12,'note':'בדיקת נזקים במרכב פעם בשנה'}],
 'specs':{'_note':'טיוטה: מסמך היצרן לשוק האירופי (אותו דור), לא ספר עברי של כלמוביל'},
 'sources':[{'url':OL,'kind':'manufacturer','note':'Mitsubishi Outlander 2007 (CW, אירופה) Pre-Delivery Inspection and Periodic Maintenance, קבוצה 2 "Periodic Inspection and Maintenance Schedule" עמ\' 2-3 עד 2-6 (עמודי PDF 3-6); עותק במאגר jdmfsm.info'},
            {'url':'https://jdmfsm.info/Auto/Japan/Mitsubishi/Outlander/Manuals/2007/Service%20Manual%20PDF/Pre-Delivery%20Inspection/PDI_PrefaceForEUR.pdf','kind':'manufacturer','note':'עמוד השער של אותו מסמך (גרסה לאירופה)'},
            {'url':'https://www.mitsubishi-israel.co.il/car_books/','kind':'importer','note':'ספרי הרכב העבריים של כלמוביל לאאוטלנדר 2010 ו-2012 (res.cloudinary.com/colmobil) נבדקו שוב: אין בהם לוח טיפולים ואין מרווחי ק"מ בטקסט'}],
 'status':'draft',
 'notes':('טיוטה ממסמך היצרן לאאוטלנדר מהדור הזה (CW, שוק אירופה), במקום ההעתקה הקודמת מלוח הדור הבא. טיפול כל 15,000 ק"מ או שנה עם שמן, מסנן שמן ומסנן מזגן. '
  'מסנן אוויר כל 45,000 ק"מ, נוזל בלמים כל 30,000 ק"מ או שנתיים, נוזל קירור כל 60,000 ק"מ או 4 שנים, מצתים כל 90,000 ק"מ, נוזל תיבה ושמן דיפרנציאלים (4X4) כל 90,000 ק"מ או 6 שנים, '
  'שמן תיבת העברה כל 75,000 ק"מ או 5 שנים, מסנן דלק כל 150,000 ק"מ או 10 שנים. למנועי 4B11/4B12 שרשרת תזמון, ולכן שורת רצועת התזמון לא חלה. '
  'בתנאים קשים: שמן ומסנן כל 7,500 ק"מ, בדיקת מסנן אוויר ובלמים כל 7,500. שורות הדיזל, הטורבו והגיר הידני לא הועתקו. '
  'בדיקת כבלי הצתה, מיסבי גלגל (60,000), סל"ד סרק, CO, EGR ונסיעת מבחן מופיעות בטבלה ולא מופו לפריטים.')})

# ---------------- ECLIPSE CROSS PHEV ----------------
EC='https://www.mitsubishi-motors.com.au/content/dam/mmal/pdfs/maintenance-schedules/24MY%20YB%20ECLIPSE%20CROSS%20PLUG-IN%20HYBRID%20INSPECTION%20AND%20MAINTENANCE%20SCHEDULE%20WEB.pdf'
ec_rules=[
 ('engine_oil','replace',ev),('oil_filter','replace',ev),
 ('drive_belt','inspect',m30),
 ('spark_plugs','replace',m90),
 ('valve_clearance','inspect',m90,'בדיקה מלאה; בשאר הטיפולים בדיקת רעש בלבד'),
 ('coolant_hoses','inspect',m30),('coolant','inspect',ev,'בדיקת מפלס'),
 ('air_filter','replace',m45),('air_filter','inspect',ev),
 ('brake_fluid','replace',m30),('brake_fluid','inspect',ev,'בדיקת מפלס'),
 ('battery_12v','inspect',ev),
 ('hybrid_system','inspect',ev,'דליפת שמן קירור המנוע החשמלי הקדמי ומפלס נוזל קירור המנוע האחורי; כבלי מתח גבוה כל 30,000'),
 ('suspension','inspect',ev,'כולל מפרקים כדוריים'),('cv_boots','inspect',ev),('steering','inspect',ev),
 ('transmission_oil','inspect',ev,'בדיקת דליפות בתמסורת הקדמית'),('differential_oil','inspect',ev,'בדיקת דליפות בתמסורת האחורית'),
 ('exhaust','inspect',m30),
 ('pedals','inspect',ev),('cabin_filter','replace',ev),('lights','inspect',ev),
 ('wheel_alignment','inspect',m30),('tires','inspect',ev,'לחץ אוויר'),
 ('brake_lines','inspect',m30,'בתנאים קשים בכל טיפול'),('brake_pads','inspect',ev),('brake_discs','inspect',ev),
 ('fuel_lines','inspect',m30),('body_underside','inspect',ev),
]
write({'id':'mitsubishi-eclipse-cross-phev-2021-2026-2.4-phev','make':'Mitsubishi','make_he':'מיצובישי','model':'Eclipse Cross PHEV','model_he':'אקליפס קרוס PHEV','generation':'YB',
 'years':[2021,2026],'engines':['2.4 MIVEC PHEV (4B12)'],'fuel':'plug-in-hybrid','importer':'כלמוביל',
 'interval':{'km':15000,'months':12,'note':'לפי לוח התחזוקה של מיצובישי אוסטרליה לאקליפס קרוס פלאג-אין 24MY: 15,000 ק"מ או 12 חודשים, המוקדם; בתנאים קשים שמן ומסנן כל 7,500 ק"מ'},
 'cycle_km':180000,'services':grid(15000,180000,ec_rules),
 'long_interval':[
   {'item':'fuel_filter','action':'replace','every_km':150000},
   {'item':'coolant','action':'replace','first_km':165000,'first_months':96,'then_every_km':105000,'then_every_months':60,'note':'נוזל קירור המנוע'},
   {'item':'coolant','action':'replace','every_km':400000,'every_months':240,'note':'נוזל קירור המנוע החשמלי האחורי'},
   {'item':'transmission_oil','action':'replace','every_km':195000,'every_months':120,'note':'שמן התמסורת הקדמית; בתנאים קשים כל 30,000 ק"מ'},
   {'item':'differential_oil','action':'replace','every_km':195000,'every_months':120,'note':'שמן התמסורת האחורית; בתנאים קשים כל 30,000 ק"מ'}],
 'time_based':[],
 'specs':{'_note':'טיוטה: לוח היצרן לשוק האוסטרלי, לא ספר עברי של כלמוביל'},
 'sources':[{'url':EC,'kind':'manufacturer','note':'Mitsubishi Motors Australia, "24MY YB Eclipse Cross Plug-in Hybrid Inspection and Maintenance Schedule" עמ\' 1-2 (נקרא מתמונות העמודים)'},
            {'url':'https://www.mitsubishi-motors.com.au/content/dam/mmal/pdfs/maintenance-schedules/ECLIPSE-CROSS-22MY_Plug-In%20Hybrid%20Maintenance%20Schedule.pdf','kind':'manufacturer','note':'לוח 22MY לאותו דגם (לא נקרא שורה-שורה, רק לאימות שקיים לוח לשנים מוקדמות)'},
            {'url':'https://res.cloudinary.com/colmobil/images/v1722237048/ספר-רכב-אקליפס-קרוס-PHEV_1255280d7d/ספר-רכב-אקליפס-קרוס-PHEV_1255280d7d.pdf','kind':'importer','note':'ספר הרכב העברי של כלמוביל לאקליפס קרוס PHEV: אין בו לוח טיפולים'}],
 'status':'draft',
 'notes':('טיוטה מלוח התחזוקה של מיצובישי אוסטרליה (Eclipse Cross Plug-in Hybrid דגם 2024, מנוע 2.4 עם שני מנועים חשמליים), לא ממסמך של כלמוביל. '
  'טיפול כל 15,000 ק"מ או שנה: שמן, מסנן שמן ומסנן מזגן, ובדיקות למערכת ההיברידית. מסנן אוויר כל 45,000 ק"מ, נוזל בלמים כל 30,000 ק"מ (שנתיים), מצתים ובדיקת שסתומים מלאה כל 90,000 ק"מ, '
  'מסנן דלק ב-150,000 ק"מ, נוזל קירור המנוע ראשון ב-165,000 ק"מ או 8 שנים ואחר כך כל 105,000 ק"מ או 5 שנים. שמן התמסורות הקדמית והאחורית: כל 195,000 ק"מ או 10 שנים, ובתנאים קשים כל 30,000 ק"מ. '
  'בדיקת מיסבי גלגלים (ב-60,000, 120,000 ו-180,000), מערכת EGR, איפוס תזכורת טיפול ונסיעת מבחן מופיעות בטבלה ולא מופו לפריטים.')})

# ---------------- registry rules ----------------
rules=[
 {'make':'Tesla','names':['MODEL S','MODEL X'],'years':[2021,2026],'schedule':'tesla-model-s-x-2021-2026-ev'},
 {'make':'Mitsubishi','names':['ECLIPSE CROSS'],'years':[2021,2026],'fuel':['חשמל/בנזין'],'engine_codes':['4B12'],'schedule':'mitsubishi-eclipse-cross-phev-2021-2026-2.4-phev'},
]
json.dump(rules,open(OUT+'/registry/registry_rules.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('ok')
