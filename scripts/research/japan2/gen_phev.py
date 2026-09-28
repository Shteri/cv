import json
OUT='/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/japan2/'
KMS=list(range(15000,210001,15000))
T={k:[] for k in KMS}
def add(key,action,cols,note=None):
    for k in cols:
        e={"item":key,"action":action}
        if note: e["note"]=note
        T[k].append(e)
ALL=KMS; E30=[k for k in KMS if k%30000==0]; E45=[k for k in KMS if k%45000==0]
add("engine_oil","replace",ALL); add("oil_filter","replace",ALL)
add("drive_belt","inspect",ALL)
add("cooling_system","inspect",ALL,"מפלס נוזל קירור במיכל")
add("coolant_hoses","inspect",E30)
add("air_filter","inspect",[k for k in ALL if k not in E45])
add("air_filter","replace",E45)
add("brake_fluid","inspect",[k for k in ALL if k not in E30],"מפלס במיכל הבלמים והמצמד")
add("brake_fluid","replace",E30)
add("battery_12v","inspect",ALL)
add("hybrid_system","inspect",ALL,"דליפת שמן קירור של המנוע החשמלי הקדמי; בכל 30,000 גם כבלי מתח גבוה ומפלס נוזל קירור של המנוע האחורי")
add("suspension","inspect",ALL,"כולל מפרקים כדוריים; ב-60,000, 120,000 ו-180,000 גם מסבי גלגלים")
add("cv_boots","inspect",ALL)
add("steering","inspect",ALL)
add("transmission_oil","inspect",ALL,"שמן תמסורת קדמית (גיר הפחתה): בדיקת דליפה; בתנאים קשים החלפה כל 30,000 ק\"מ")
add("differential_oil","inspect",ALL,"שמן תמסורת אחורית: בדיקת דליפה; בתנאים קשים החלפה כל 30,000 ק\"מ")
add("exhaust","inspect",E30)
add("pedals","inspect",ALL); add("parking_brake","inspect",ALL)
add("cabin_filter","replace",ALL,"מסנן מטהר אוויר")
add("wheel_alignment","inspect",E30,"בדיקה חזותית לפי בלאי הצמיגים")
add("brake_lines","inspect",ALL)
add("brake_pads","inspect",ALL); add("brake_discs","inspect",ALL)
add("fuel_lines","inspect",E30)
d={"id":"mitsubishi-outlander-phev-2017-2021-2.0-2.4-phev","make":"Mitsubishi","make_he":"מיצובישי","model":"Outlander PHEV","model_he":"אאוטלנדר PHEV",
"generation":"ZK/ZL (GG2W/GG3W)","years":[2017,2021],"engines":["2.0 MIVEC PHEV (4B11)","2.4 MIVEC PHEV (4B12)"],"fuel":"plug-in-hybrid","importer":"כלמוביל",
"interval":{"km":15000,"months":12,"note":"לפי לוח התחזוקה של מיצובישי אוסטרליה ל-Outlander PHEV MY19: טיפול כל 15,000 ק\"מ או 12 חודשים; בתנאים קשים שמן ומסנן כל 7,500 ק\"מ"},
"cycle_km":210000,"services":[{"km":k,"items":T[k]} for k in KMS],
"long_interval":[
 {"item":"spark_plugs","action":"replace","every_km":90000,"note":"מצתים עם קצה פלטינה"},
 {"item":"valve_clearance","action":"inspect","every_km":90000,"note":"וגם בכל עת שיש רעש שסתומים"},
 {"item":"coolant","action":"replace","first_km":165000,"first_months":96,"then_every_km":105000,"then_every_months":60},
 {"item":"fuel_filter","action":"replace","every_km":150000,"every_months":120}],
"time_based":[{"item":"coolant","action":"replace","every_months":240,"note":"נוזל קירור של המנוע החשמלי האחורי כל 20 שנה"},
 {"item":"body_underside","action":"inspect","every_months":12,"note":"בדיקת מצב המרכב פעם בשנה"}],
"specs":{},
"sources":[
 {"url":"https://www.mitsubishi-motors.com.au/content/dam/mmal/pdfs/maintenance-schedules/OUTLANDER-PHEV-MY19_Maintenance%20Schedule.pdf","kind":"manufacturer","note":"Mitsubishi Motors Australia, Periodic Inspection and Maintenance Schedule 19 MY PHEV, עמ' 1-2; נקרא מתמונת העמודים"},
 {"url":"https://www.mitsubishi-motors.com.au/content/dam/mmal/pdfs/maintenance-schedules/20MY-Outlander-PHEV_Maintenance%20Schedule.pdf","kind":"manufacturer","note":"לוח 20MY PHEV: אותה טבלה"},
 {"url":"https://www.mitsubishi-motors.com.au/content/dam/mmal/pdfs/maintenance-schedules/OUTLANDER-PHEV-MY18_Maintenance%20Schedule.pdf","kind":"manufacturer","note":"לוח 18MY ZK PHEV (מנוע 2.0): אותם פריטים ומועדים עד 300,000 ק\"מ; בלוח זה מסומן במפורש שהחלפת שמן התמסורות כל 30,000 ק\"מ היא לתנאים קשים בלבד"},
 {"url":"https://www.mitsubishi-motors.com.au/owners/service/maintenance-schedule.html","kind":"manufacturer","note":"רשימת לוחות התחזוקה של מיצובישי אוסטרליה; ספרי כלמוביל העבריים שנבדקו בסבב הקודם אינם כוללים לוח תחזוקה לדגם זה"}],
"status":"draft",
"notes":"טיוטה מלוח התחזוקה של מיצובישי אוסטרליה (Outlander PHEV דגמי 2018-2020, מנועי 2.0 ו-2.4), לא מספר ישראלי. טיפול כל 15,000 ק\"מ או שנה עם שמן, מסנן שמן ומסנן מזגן. מסנן אוויר מוחלף כל 45,000 ק\"מ ונוזל בלמים כל 30,000 ק\"מ (שנתיים). החלפת שמן התמסורת הקדמית והאחורית כל 30,000 ק\"מ נדרשת רק בתנאים קשים. מצתים ובדיקת שסתומים כל 90,000 ק\"מ, מסנן דלק כל 150,000 ק\"מ, נוזל קירור ראשון ב-165,000 ק\"מ או 8 שנים. בדיקות למערכת ההיברידית (כבלי מתח גבוה, קירור המנועים החשמליים) נכללות בטיפולים."}
json.dump(d,open(OUT+d['id']+'.json','w'),ensure_ascii=False,indent=2)
