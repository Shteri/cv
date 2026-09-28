import json
OUT='/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/japan2/'
KMS=[15000,30000,45000,60000,75000,90000]
T={k:[] for k in KMS}
def add(key,action,cols,note=None):
    for k in cols:
        e={"item":key,"action":action}
        if note: e["note"]=note
        T[k].append(e)
ALL=KMS; E30=[30000,60000,90000]; E45=[45000,90000]
add("engine_oil","replace",ALL); add("oil_filter","replace",ALL)
add("drive_belt","inspect",[45000]); add("drive_belt","replace",[90000])
add("valve_clearance","inspect",E30)
add("coolant","replace",E45)
add("exhaust","inspect",E30)
add("spark_plugs","replace",E45,"מצתי ניקל ברכב עם חיישן חמצן; מצתי אירידיום (מומלצים) כל 105,000 ק\"מ")
add("air_filter","inspect",[15000,30000,60000,75000],"בדרכים סלולות; בתנאי אבק לפי לוח התנאים הקשים")
add("air_filter","replace",E45)
add("fuel_lines","inspect",E30)
add("fuel_lines","inspect",[45000,90000],"בדיקת מיכל הדלק")
add("pcv_valve","inspect",[90000]); add("evap_system","inspect",[90000])
add("brake_pads","inspect",ALL); add("brake_discs","inspect",ALL)
add("brake_drums","inspect",E30); add("brake_lines","inspect",E30)
add("brake_fluid","replace",E30)
add("parking_brake","inspect",[15000],"רק בטיפול הראשון")
add("clutch","inspect",E30,"דליפה ומפלס נוזל")
add("tires","inspect",ALL,"בלאי, נזק וסבב; מצב החישוקים")
add("suspension","inspect",E30); add("steering","inspect",E30)
add("cv_boots","inspect",E45)
add("manual_gearbox_oil","inspect",[15000],"גיר ידני: בדיקת מפלס ודליפה בטיפול הראשון בלבד")
add("manual_gearbox_oil","replace",E45,"גיר ידני")
add("transmission_oil","inspect",E30,"גיר אוטומטי: מפלס; צינור הנוזל נבדק ב-60,000")
add("door_hinges","inspect",E30)
add("cabin_filter","inspect",[30000,75000],"אם מותקן")
add("cabin_filter","replace",E45,"אם מותקן")
d={"id":"suzuki-swift-2005-2010-1.5","make":"Suzuki","make_he":"סוזוקי","model":"Swift","model_he":"סוויפט",
"generation":"RS (דור 2, 2005-2010)","years":[2005,2010],"engines":["1.5 (M15A)"],"fuel":"petrol","importer":"מכשירי תנועה",
"interval":{"km":15000,"months":12,"note":"לפי ספר השירות של סוזוקי לסוויפט RS (2005): טיפול כל 15,000 ק\"מ או 12 חודשים; בתנאים קשים (נסיעות קצרות, אבק, גרירה) שמן ומסנן כל 7,500 ק\"מ או 6 חודשים"},
"cycle_km":90000,"services":[{"km":k,"items":T[k]} for k in KMS],
"long_interval":[
 {"item":"spark_plugs","action":"replace","every_km":105000,"every_months":84,"note":"מצתי אירידיום"},
 {"item":"fuel_filter","action":"replace","every_km":105000},
 {"item":"transmission_oil","action":"replace","every_km":165000,"note":"נוזל גיר אוטומטי"}],
"time_based":[],"specs":{},
"sources":[
 {"url":"https://procarmanuals.com/wp-content/uploads/pdfs/manuals/suzuki-swift-2005-rs-series-service-manual.pdf","kind":"manufacturer","note":"ספר השירות של סוזוקי לסוויפט RS (2005, קוד S4RS), פרק 0B 'Maintenance and Lubrication', עמ' 0B-1 עד 0B-2 (עמודי PDF 32-33); עותק באתר procarmanuals.com; הטבלה נקראה מתמונת העמוד"},
 {"url":"https://procarmanuals.com/pdf-online-suzuki-swift-2005-rs-series-service-manual/","kind":"other","note":"עמוד האתר שמציג את הקובץ"},
 {"url":"https://suzuki.co.il/content/%D7%A1%D7%A4%D7%A8%D7%99-%D7%A0%D7%94%D7%92-%D7%A1%D7%95%D7%96%D7%95%D7%A7%D7%99","kind":"importer","note":"בספריית ספרי הנהג של מכשירי תנועה אין ספר לסוויפט 2005-2010 עם מנוע M15A (נבדק בסבב הקודם)"}],
"status":"draft",
"notes":"טיוטה מספר השירות הבינלאומי של סוזוקי לסוויפט RS (דגמי 2005 ואילך, מנועי 1.3/1.5), לא מספר ישראלי. טיפול כל 15,000 ק\"מ או שנה עם שמן ומסנן. מסנן אוויר ונוזל קירור מוחלפים כל 45,000 ק\"מ, נוזל בלמים כל 30,000 ק\"מ, שמן גיר ידני ב-45,000 וב-90,000. מצתי ניקל כל 45,000 ק\"מ (אירידיום כל 105,000), מסנן דלק כל 105,000 ק\"מ. רצועת אביזרים נבדקת ב-45,000 ומוחלפת ב-90,000. אחרי 90,000 ק\"מ חוזרים על אותו מחזור."}
json.dump(d,open(OUT+d['id']+'.json','w'),ensure_ascii=False,indent=2)
