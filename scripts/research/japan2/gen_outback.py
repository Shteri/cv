import json
OUT='/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/japan2/'
KMS=list(range(15000,120001,15000))
T={k:[] for k in KMS}
def add(key,action,cols,note=None):
    for k in cols:
        e={"item":key,"action":action}
        if note: e["note"]=note
        T[k].append(e)
ALL=KMS; E30=[30000,60000,90000,120000]
add("engine_oil","replace",ALL,"בתנאי נהיגה קשים בתדירות גבוהה יותר")
add("oil_filter","replace",ALL)
add("drive_belt","inspect",ALL,"החלפה כל 160,000 ק\"מ")
add("coolant_hoses","inspect",E30,"מערכת הקירור, צינורות וחיבורים")
add("fuel_lines","inspect",E30,"מערכת הדלק, צינורות וחיבורים")
add("air_filter","inspect",[15000,30000,60000,75000,105000,120000],"בתנאי אבק החלפה בתדירות גבוהה יותר")
add("air_filter","replace",[45000,90000])
add("differential_oil","inspect",[30000,90000],"שמן תיבת הילוכים ודיפרנציאל קדמי/אחורי")
add("differential_oil","replace",[60000,120000],"שמן תיבת הילוכים ודיפרנציאל קדמי/אחורי")
add("cvt_oil","inspect",E30,"בתנאי גרירה ומטען כבד החלפה כל 45,000 ק\"מ")
add("brake_fluid","replace",E30,"באזורי לחות גבוהה או הרים כל 15,000 ק\"מ או 12 חודשים")
add("brake_pads","inspect",ALL); add("brake_discs","inspect",ALL); add("brake_lines","inspect",ALL)
add("parking_brake","inspect",E30,"רפידות ותופי בלם החניה")
add("pedals","adjust",E30,"בדיקת פעולת בלם החניה ובלם השירות וכיוון")
add("clutch","inspect",E30,"חופש דוושה נבדק כבר ב-1,600 ק\"מ")
add("steering","inspect",E30); add("suspension","inspect",E30)
add("suspension","inspect",[120000],"מסבי גלגלים קדמיים ואחוריים (מומלץ)")
d={"id":"subaru-outback-2015-2020-2.5","make":"Subaru","make_he":"סובארו","model":"Outback","model_he":"אאוטבק",
"generation":"BS (דור 5)","years":[2015,2020],"engines":["2.5 (FB25)"],"fuel":"petrol","importer":"יפנאוטו (סובארו, קבוצת סמלת)",
"interval":{"km":15000,"months":12,"note":"לפי 'תכנית תחזוקה' בספר הרכב העברי (סמלת): טיפול כל 15,000 ק\"מ או 12 חודשים; אחרי 120,000 ק\"מ חוזרים על הלוח מההתחלה"},
"cycle_km":120000,"services":[{"km":k,"items":T[k]} for k in KMS],
"long_interval":[
 {"item":"coolant","action":"replace","first_km":220000,"first_months":132,"then_every_km":120000,"then_every_months":72,"note":"נוזל SUBARU Super Coolant"},
 {"item":"fuel_filter","action":"replace","every_km":90000,"note":"מנוע בנזין"},
 {"item":"spark_plugs","action":"replace","every_km":105000},
 {"item":"drive_belt","action":"replace","every_km":160000},
 {"item":"cabin_filter","action":"replace","every_km":12000,"every_months":12}],
"time_based":[],"specs":{},
"sources":[
 {"url":"https://samelet.com/ebooks/Car_Book_outback.pdf","kind":"importer","note":"מדריך תפעול סובארו לגאסי/אאוטבק 2014 (סמלת), פרק 11 'תכנית תחזוקה' עמ' 11-3 עד 11-6 (עמודי PDF 453-456); הטבלה נקראה מתמונת העמודים"},
 {"url":"https://samelet.com/ebooks/","kind":"importer","note":"תיקיית ספרי הרכב הפתוחה של קבוצת סמלת (יבואנית סובארו)"}],
"status":"reviewed",
"notes":"לפי ספר הרכב העברי של היבואן לאאוטבק (דור BS). טיפול כל 15,000 ק\"מ או שנה עם שמן ומסנן ובדיקת בלמים. מסנן אוויר מוחלף כל 45,000 ק\"מ, נוזל בלמים כל 30,000 ק\"מ, שמן גיר ודיפרנציאל ב-60,000 וב-120,000. מסנן דלק כל 90,000 ק\"מ, מצתים כל 105,000 ק\"מ, רצועות כל 160,000 ק\"מ. נוזל קירור ראשון אחרי 220,000 ק\"מ או 11 שנים. מסנן המזגן מוחלף כל 12,000 ק\"מ או שנה. הספר כולל גם מנוע 3.6, שלא נכלל כאן."}
json.dump(d,open(OUT+d['id']+'.json','w'),ensure_ascii=False,indent=2)
