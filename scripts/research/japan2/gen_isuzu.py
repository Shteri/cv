import json
OUT='/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/japan2/'
KMS=list(range(10000,100001,10000))
def build(eng):
    T={k:[] for k in KMS}
    def add(key,action,cols,note=None):
        for k in cols:
            e={"item":key,"action":action}
            if note: e["note"]=note
            T[k].append(e)
    ALL=KMS; E20=[k for k in KMS if k%20000==0]; E40=[40000,80000]
    add("engine_oil","replace",ALL)
    add("oil_filter","replace",ALL if eng=='4JH1' else E20)
    add("air_filter","inspect",[k for k in ALL if k not in E40]); add("air_filter","replace",E40)
    add("fuel_lines","inspect",ALL,"בדיקת דליפות דלק; מיכל הדלק נבדק כל 20,000 ק\"מ")
    if eng=='4JH1': add("valve_clearance","adjust",E20,"כיוון ראשון גם ב-5,000 ק\"מ")
    else:
        add("valve_clearance","adjust",E40)
        add("fuel_filter","inspect",E40,"מסנן משאבת הדלק שבמיכל")
    add("drive_belt","inspect",ALL,"מתיחות ונזק לרצועת המאוורר")
    add("exhaust","inspect",ALL)
    add("coolant","inspect",ALL,"ריכוז נוזל הקירור")
    add("cooling_system","inspect",ALL); add("coolant_hoses","inspect",ALL,"כל הצינורות בתא המנוע")
    add("clutch","inspect",ALL,"נוזל מצמד ומהלך הדוושה")
    add("transmission_oil","inspect",E20,"גיר אוטומטי")
    add("transfer_case_oil","inspect",E20,"הנעה כפולה")
    add("manual_gearbox_oil","replace",[10000,40000,80000]); add("manual_gearbox_oil","inspect",[20000,60000,100000])
    add("differential_oil","replace",[10000,40000,80000],"קדמי ואחורי"); add("differential_oil","inspect",[20000,60000,100000],"קדמי ואחורי")
    add("propshaft","inspect",ALL,"חיבורים ומפרקים; בהנעה כפולה גם גירוז מפרקים ושרוול החלקה")
    add("cv_boots","inspect",E20,"גומיות צירי הסרן הקדמי")
    add("power_steering_fluid","replace",E40); add("power_steering_fluid","inspect",[k for k in ALL if k not in E40])
    add("steering","inspect",ALL,"כולל צינור הגה כוח (מוחלף ב-80,000) ומפרקים כדוריים")
    add("wheel_alignment","inspect",E20)
    add("brake_fluid","inspect",E20)
    add("brake_lines","inspect",ALL); add("brake_pads","inspect",ALL); add("brake_discs","inspect",ALL); add("brake_drums","inspect",ALL)
    add("pedals","inspect",ALL); add("parking_brake","inspect",ALL)
    add("suspension","inspect",ALL,"קפיצים, בולמים ותותבים; מסבי גלגלים")
    add("tires","inspect",ALL,"לחץ ונזק; הידוק אומי גלגלים")
    add("body_underside","inspect",ALL,"הידוק ברגים ואומים בשלדה ובמרכב")
    return [{"km":k,"items":T[k]} for k in KMS]
src=[{"url":"https://procarmanuals.com/wp-content/uploads/pdfs/manuals/isuzu-kb-p190-2007-iworkshop-repair-manual.pdf","kind":"manufacturer","note":"ספר הסדנה של איסוזו KB P190 (דגם 2007, סדרת TF), פרק 0B 'Maintenance Schedule (For GENERAL EXPORT)', עמ' 0B-2 עד 0B-4 (עמודי PDF 20-22); עותק באתר procarmanuals.com; הטבלה נקראה מתמונת העמודים"},
     {"url":"https://procarmanuals.com/pdf-online-isuzu-kb-p190-2007-iworkshop-repair-manual/","kind":"other","note":"עמוד האתר שמציג את הקובץ"},
     {"url":"https://www.isuzu.co.il/","kind":"importer","note":"אתר איסוזו ישראל מחזיר 403; לא נמצא ספר עברי"}]
base=dict(make="Isuzu",make_he="איסוזו",model="D-Max",model_he="די-מקס",fuel="diesel",importer="יוניברסל מוטורס ישראל",
 interval={"km":10000,"months":12,"note":"לפי לוח היצוא הכללי (General Export) בספר הסדנה של איסוזו לסדרת TF: שמן מנוע כל 10,000 ק\"מ או 12 חודשים. בלוח יש גם בדיקות קלות כל 5,000 ק\"מ (סרעפת, דליפות, פעולת בלמים והגה)"},
 cycle_km=100000,specs={},status="draft",sources=src)
d1=dict(id="isuzu-d-max-2004-2007-3.0-diesel",generation="TF (דור 1)",years=[2004,2007],engines=["3.0 turbo diesel (4JH1-TC)"],**base,services=build('4JH1'),
 long_interval=[{"item":"fuel_filter","action":"replace","every_km":15000,"note":"בלוח: 15,000, 30,000, 45,000 וכן הלאה"},
   {"item":"door_hinges","action":"inspect","every_km":30000,"note":"גירוז מסבי הגלגלים הקדמיים (החלפת גריז) כל 30,000 ק\"מ"}],
 time_based=[],
 notes="טיוטה מספר הסדנה הבינלאומי של איסוזו KB/D-Max סדרת TF (לוח יצוא כללי), לא מספר ישראלי. מנוע 4JH1-TC: שמן ומסנן שמן כל 10,000 ק\"מ או שנה, מסנן סולר כל 15,000 ק\"מ, מסנן אוויר מוחלף כל 40,000 ק\"מ. שמן גיר ידני ושמן דיפרנציאל מוחלפים ב-10,000 ואחר כך ב-40,000 וב-80,000; נוזל הגה כוח ב-40,000 וב-80,000. כיוון שסתומים ב-5,000 ואחר כך כל 20,000 ק\"מ. הגריז במסבי הגלגלים הקדמיים מוחלף כל 30,000 ק\"מ.")
# fix: hub grease is not hinges; use suspension item instead
d1["long_interval"][1]={"item":"suspension","action":"replace","every_km":30000,"note":"החלפת גריז במסבי הגלגלים הקדמיים"}
d2=dict(id="isuzu-d-max-2007-2011-3.0-diesel",generation="TF (דור 1, מנוע 4JJ1)",years=[2007,2011],engines=["3.0 turbo diesel (4JJ1-TC)"],**base,services=build('4JJ1'),
 long_interval=[{"item":"suspension","action":"replace","every_km":30000,"note":"החלפת גריז במסבי הגלגלים הקדמיים"}],
 time_based=[{"item":"coolant","action":"replace","every_months":24,"note":"כל שנתיים"}],
 notes="טיוטה מספר הסדנה הבינלאומי של איסוזו KB/D-Max סדרת TF (לוח יצוא כללי), לא מספר ישראלי. מנוע 4JJ1: שמן כל 10,000 ק\"מ או שנה ומסנן שמן כל 20,000 ק\"מ. מסנן הסולר מוחלף כשנורית המסנן נדלקת. מסנן אוויר מוחלף כל 40,000 ק\"מ, נוזל קירור כל שנתיים. שמן גיר ידני ושמן דיפרנציאל מוחלפים ב-10,000 ואחר כך ב-40,000 וב-80,000; נוזל הגה כוח ב-40,000 וב-80,000; כיוון שסתומים ב-40,000 וב-80,000.")
for d in (d1,d2): json.dump(d,open(OUT+d['id']+'.json','w'),ensure_ascii=False,indent=2)
