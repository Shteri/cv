import json
OUT='/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/japan2/'
def I(k,a,n=None):
    e={"item":k,"action":a}
    if n: e["note"]=n
    return e
common=[I("engine_oil","replace"),I("oil_filter","replace"),I("tires","inspect","מצב הצמיגים ולחץ אוויר כולל גלגל חילוף"),
 I("lights","inspect"),I("drive_belt","adjust","בדיקה וכיוון מתיחות לפי הצורך"),I("battery_12v","inspect"),I("wipers","inspect"),
 I("door_hinges","inspect","סיכת תפסים, צירים ומנעולים"),I("steering","inspect"),I("suspension","inspect"),I("body_underside","inspect")]
A=common+[I("differential_oil","inspect","בדיקת כל מפלסי הנוזלים כולל שני הדיפרנציאלים")]
B=common+[I("tire_rotation","rotate"),I("cooling_system","inspect","נוזל קירור"),I("coolant_hoses","inspect","צינורות גמישים וחבקים"),
 I("air_filter","inspect","החלפה לפי הצורך"),I("cabin_filter","inspect","החלפה לפי הצורך"),I("clutch","inspect","אם יש")]
C=common+[I("tire_rotation","rotate"),I("brake_pads","inspect","ביקורת ושירות בלמים קדמיים ואחוריים"),I("brake_discs","inspect"),
 I("cooling_system","inspect","נוזל קירור"),I("coolant_hoses","inspect","צינורות גמישים וחבקים"),
 I("air_filter","inspect","החלפה לפי הצורך"),I("cabin_filter","inspect","החלפה לפי הצורך"),I("brake_fluid","replace"),
 I("fuel_lines","inspect","שירות מזרקי דלק"),I("exhaust","inspect","צנרת גמישה הקשורה לפליטה"),I("pcv_valve","inspect","החלפה לפי הצורך")]
D=common+[I("tire_rotation","rotate"),I("brake_pads","inspect","ביקורת ושירות בלמים קדמיים ואחוריים"),I("brake_discs","inspect"),
 I("cooling_system","inspect","נוזל קירור"),I("coolant_hoses","inspect","צינורות גמישים וחבקים"),
 I("air_filter","inspect","החלפה לפי הצורך"),I("cabin_filter","inspect","החלפה לפי הצורך"),I("spark_plugs","replace"),
 I("cvt_oil","replace","החלפת שמן תיבת ההילוכים"),I("differential_oil","replace","החלפת שמן הדיפרנציאל; בדיקת כל מפלסי הנוזלים")]
plan={10000:A,20000:B,30000:A,40000:B,50000:A,60000:C,70000:A,80000:B,90000:A,100000:D}
d={"id":"subaru-forester-2025-2026-2.5","make":"Subaru","make_he":"סובארו","model":"Forester","model_he":"פורסטר",
"generation":"SL (דור 6, 25MY)","years":[2025,2026],"engines":["2.5 (FB25)"],"fuel":"petrol","importer":"יפנאוטו (סובארו, קבוצת סמלת)",
"interval":{"km":10000,"months":12,"note":"לפי 'תכנית תחזוקה' בספר הרכב העברי (סמלת) לפורסטר 25MY: שירות כל 10,000 ק\"מ או 12 חודשים לפי סבב A/B/C/D; אחרי 100,000 ק\"מ חוזרים לתחילת הטבלה"},
"cycle_km":100000,"services":[{"km":k,"items":v} for k,v in plan.items()],
"long_interval":[],"time_based":[],"specs":{"engine_oil":"שמן סינתטי 0W-20"},
"sources":[
 {"url":"https://samelet.com/ebooks/Subaru_Forester_25MY_carbook_082024.pdf","kind":"importer","note":"מדריך תפעול סובארו פורסטר 25MY (סמלת, 08/2024), פרק 11-1 'תכנית תחזוקה' עמ' 431-432 (עמודי PDF 435-436): טבלת שירותים A/B/C/D ורשימת הפעולות לכל שירות"},
 {"url":"https://samelet.com/ebooks/","kind":"importer","note":"תיקיית ספרי הרכב הפתוחה של קבוצת סמלת (יבואנית סובארו)"}],
"status":"reviewed",
"notes":"לפי ספר הרכב העברי של היבואן לפורסטר 25MY. שירות כל 10,000 ק\"מ או שנה: A ב-10, 30, 50, 70, 90 אלף; B ב-20, 40, 80 אלף (גם סבב צמיגים ובדיקת מסנני אוויר); C ב-60,000 (גם שירות בלמים והחלפת נוזל בלמים); D ב-100,000 (גם החלפת מצתים ושמן תיבת הילוכים ודיפרנציאל). הספר מציין שבתנאי נהיגה קשים (חום, אבק, נסיעות קצרות) חלק מהפעולות נדרשות בתדירות גבוהה יותר, ושמנוע סובארו עשוי לצרוך עד ליטר שמן לכל 6,000 ק\"מ."}
json.dump(d,open(OUT+d['id']+'.json','w'),ensure_ascii=False,indent=2)
