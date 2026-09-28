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
add("engine_oil","replace",ALL,"בתנאים מחמירים (אבק, חום, נסיעות קצרות) כל 15,000 ק\"מ")
add("oil_filter","replace",ALL,"בתנאים מחמירים כל 15,000 ק\"מ")
add("drive_belt","inspect",ALL,"החלפה אם פגומה")
add("coolant","inspect",[30000,60000,120000],"בדיקת יחס התערובת")
add("cooling_system","inspect",ALL)
add("fuel_lines","inspect",ALL)
add("evap_system","inspect",ALL,"צנרת אדי דלק ומיכל פחם")
add("air_filter","replace",[60000,120000],"בתנאי אבק כל 30,000 ק\"מ")
add("lights","inspect",ALL,"כיוון פנסים")
add("brake_lines","inspect",ALL,"מערכת בלמים ומצמד: מפלסים ודליפות; גם צינורות ואקום של המגבר")
add("brake_fluid","replace",ALL,"בתנאים מחמירים כל 15,000 ק\"מ")
add("transmission_oil","inspect",ALL,"גיר אוטומטי: מפלס ודליפות; בגרירה או דרכים קשות החלפה כל 60,000 ק\"מ")
add("manual_gearbox_oil","inspect",ALL,"גיר ידני: מפלס ודליפות")
add("steering","inspect",ALL); add("suspension","inspect",ALL); add("cv_boots","inspect",ALL); add("exhaust","inspect",ALL)
add("wheel_alignment","inspect",ALL,"לפי הצורך גם סבב ואיזון גלגלים")
add("brake_pads","inspect",ALL); add("brake_discs","inspect",ALL)
add("pedals","inspect",ALL); add("parking_brake","inspect",ALL); add("clutch","inspect",ALL)
add("cabin_filter","replace",ALL)
d={"id":"nissan-tiida-2007-2011-1.6","make":"Nissan","make_he":"ניסאן","model":"Tiida","model_he":"טידה",
"generation":"C11","years":[2007,2011],"engines":["1.6 (HR16DE)"],"fuel":"petrol","importer":"פריסבי (קרסו)",
"interval":{"km":30000,"months":24,"note":"לפי ספר השירות האירופי של ניסאן לטידה C11 (מנוע HR16DE): טיפול כל 30,000 ק\"מ או 24 חודשים בתנאים רגילים; בתנאים מחמירים שמן ומסנן ונוזל בלמים כל 15,000 ק\"מ"},
"cycle_km":120000,"services":[{"km":k,"items":T[k]} for k in KMS],
"long_interval":[
 {"item":"spark_plugs","action":"replace","every_km":90000,"note":"מצתי פלטינה; בלוח מסומנת החלפה ב-90,000 ק\"מ"},
 {"item":"coolant","action":"replace","first_km":90000,"first_months":60,"then_every_km":60000,"then_every_months":48},
 {"item":"valve_clearance","action":"inspect","every_km":120000,"note":"אין בדיקה תקופתית; בודקים רק אם יש רעש שסתומים"}],
"time_based":[{"item":"body_underside","action":"inspect","every_months":12,"note":"בדיקת קורוזיה במרכב פעם בשנה"}],
"specs":{},
"sources":[
 {"url":"https://procarmanuals.com/wp-content/uploads/pdfs/manuals/nissan-tiida-c11-2008-service-repair-manual.pdf","kind":"manufacturer","note":"ספר השירות (ESM) של ניסאן טידה C11 לאירופה (2008), פרק MA 'Periodic Maintenance', עמ' MA-8 עד MA-10 (עמודי PDF 5833-5835, טבלאות HR ENGINE) ועמוד תנאים מחמירים (עמוד PDF 5842); עותק באתר procarmanuals.com"},
 {"url":"https://procarmanuals.com/pdf-online-nissan-tiida-c11-2008-service-repair-manual/","kind":"other","note":"עמוד האתר שמציג את הקובץ"},
 {"url":"https://www.nissan.co.il/service.html","kind":"importer","note":"ניסאן ישראל אינה מפרסמת ספרי רכב; service.freesbe.com ו-freesbe.com מחזירים 403"}],
"status":"draft",
"notes":"טיוטה מספר השירות האירופי של ניסאן לטידה C11 עם מנוע 1.6 HR16DE, לא מספר ישראלי (הטידה שנמכרה בישראל יוצרה במקסיקו). בתנאים רגילים טיפול כל 30,000 ק\"מ או שנתיים עם שמן, מסנן שמן, מסנן מזגן ונוזל בלמים. בתנאים מחמירים (אבק, חום, נסיעות עירוניות קצרות) הספר דורש שמן ומסנן ונוזל בלמים כל 15,000 ק\"מ ומסנן אוויר כל 30,000. מצתים ב-90,000 ק\"מ, נוזל קירור ראשון ב-90,000 ק\"מ או 5 שנים ואז כל 60,000 ק\"מ או 4 שנים. מסנן הדלק בתוך המיכל ואינו דורש החלפה."}
json.dump(d,open(OUT+d['id']+'.json','w'),ensure_ascii=False,indent=2)
