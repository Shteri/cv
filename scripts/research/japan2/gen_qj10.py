import json
OUT='/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/japan2/'
KMS=[30000,60000,90000,120000]
T={k:[] for k in KMS}
def add(key,action,cols,note=None):
    for k in cols:
        e={"item":key,"action":action}
        if note: e["note"]=note
        T[k].append(e)
ALL=KMS
add("engine_oil","replace",ALL,"בתנאים מחמירים (אבק, חום, נסיעות קצרות) כל 15,000 ק\"מ או 12 חודשים")
add("oil_filter","replace",ALL,"בתנאים מחמירים כל 15,000 ק\"מ או 12 חודשים")
add("drive_belt","inspect",ALL,"החלפה אם פגומה או כשמותח הרצועה מגיע לגבול")
add("coolant","inspect",[30000,60000,120000],"בדיקת יחס התערובת")
add("cooling_system","inspect",ALL)
add("fuel_lines","inspect",ALL,"כולל צנרת אדי דלק (EVAP)")
add("air_filter","replace",[60000,120000],"בתנאי אבק כל 30,000 ק\"מ או 24 חודשים")
add("lights","inspect",ALL,"כיוון פנסים")
add("brake_lines","inspect",ALL,"מערכת בלמים ומצמד: מפלסים ודליפות; גם צינורות ואקום של המגבר")
add("brake_fluid","replace",ALL,"בתנאים מחמירים כל 15,000 ק\"מ או 12 חודשים")
add("cvt_oil","inspect",ALL,"מפלס ודליפות; ראו הערה על גרירה ודרכים קשות")
add("manual_gearbox_oil","inspect",ALL,"מפלס ודליפות")
add("differential_oil","inspect",ALL,"מפלס ודליפות (הנעה כפולה); בתנאים קשים החלפה כל 30,000 ק\"מ")
add("steering","inspect",ALL); add("suspension","inspect",ALL); add("cv_boots","inspect",ALL); add("exhaust","inspect",ALL)
add("wheel_alignment","inspect",ALL,"לפי הצורך גם סבב ואיזון גלגלים")
add("brake_pads","inspect",ALL); add("brake_discs","inspect",ALL)
add("pedals","inspect",ALL); add("parking_brake","inspect",ALL); add("clutch","inspect",ALL)
add("cabin_filter","replace",ALL,"בתנאי אבק כל 15,000 ק\"מ או 12 חודשים")
d={"id":"nissan-qashqai-2007-2014-2.0","make":"Nissan","make_he":"ניסאן","model":"Qashqai","model_he":"קשקאי",
"generation":"J10 (דור 1)","years":[2007,2014],"engines":["2.0 (MR20DE)"],"fuel":"petrol","importer":"פריסבי (קרסו)",
"interval":{"km":30000,"months":24,"note":"לפי ספר השירות האירופי של ניסאן לקשקאי J10 (מנוע MR20DE): טיפול כל 30,000 ק\"מ או 24 חודשים בתנאים רגילים. בתנאים מחמירים (אבק, חום קיצוני, נסיעות קצרות, עיר) שמן ומסנן, מסנן מזגן ונוזל בלמים כל 15,000 ק\"מ או 12 חודשים"},
"cycle_km":120000,"services":[{"km":k,"items":T[k]} for k in KMS],
"long_interval":[
 {"item":"spark_plugs","action":"replace","every_km":90000,"note":"מצתי פלטינה; בלוח מסומנת החלפה ב-90,000 (ב-30,000, 60,000 ו-120,000 רק ברוסיה ואוקראינה)"},
 {"item":"coolant","action":"replace","first_km":90000,"first_months":60,"then_every_km":60000,"then_every_months":48},
 {"item":"valve_clearance","action":"inspect","every_km":120000,"note":"אין בדיקה תקופתית; בודקים רק אם יש רעש שסתומים"},
 {"item":"transfer_case_oil","action":"inspect","every_km":15000,"every_months":12,"note":"רק בהנעה כפולה: מפלס ודליפות"},
 {"item":"propshaft","action":"inspect","every_km":15000,"every_months":12,"note":"רק בהנעה כפולה: גל הינע וצירי הנעה"}],
"time_based":[{"item":"body_underside","action":"inspect","every_months":12,"note":"בדיקת קורוזיה במרכב פעם בשנה"}],
"specs":{},
"sources":[
 {"url":"https://procarmanuals.com/wp-content/uploads/pdfs/manuals/nissan-qashqai-2007-2010-factory-service-manual.pdf","kind":"manufacturer","note":"ספר השירות (ESM) של ניסאן קשקאי J10 לאירופה, פרק MA 'Periodic Maintenance', עמ' MA-8 עד MA-10 (עמודי PDF 6175-6177, טבלאות MR20DE) ו-MA-13 (תנאים מחמירים, עמוד PDF 6180); עותק באתר procarmanuals.com (מקור cardiagn.com)"},
 {"url":"https://procarmanuals.com/pdf-online-nissan-qashqai-2007-2010-factory-service-manual/","kind":"other","note":"עמוד האתר שמציג את הקובץ"},
 {"url":"https://www.nissan.co.il/service.html","kind":"importer","note":"ניסאן ישראל אינה מפרסמת ספרי רכב; service.freesbe.com ו-freesbe.com מחזירים 403"}],
"status":"draft",
"notes":"טיוטה מספר השירות האירופי של ניסאן לקשקאי J10 עם מנוע 2.0 MR20DE, לא מספר ישראלי. בתנאים רגילים טיפול כל 30,000 ק\"מ או שנתיים עם שמן, מסנן שמן, מסנן מזגן ונוזל בלמים. בתנאים מחמירים (אבק, חום, נסיעות עירוניות קצרות, נפוץ בישראל) הספר דורש שמן ומסנן, מסנן מזגן ונוזל בלמים כל 15,000 ק\"מ או שנה ומסנן אוויר כל 30,000. מצתים ב-90,000 ק\"מ, נוזל קירור ראשון ב-90,000 ק\"מ או 5 שנים ואז כל 60,000 ק\"מ או 4 שנים. מסנן הדלק בתוך המיכל ואינו דורש החלפה."}
json.dump(d,open(OUT+d['id']+'.json','w'),ensure_ascii=False,indent=2)
