import json
OUT='/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/japan2/'
KMS=[15000,30000,45000,60000,75000,90000]
def add(tbl,key,action,cols,note=None):
    for k in cols:
        e={"item":key,"action":action}
        if note: e["note"]=note
        tbl.setdefault(k,[]).append(e)
T={}
ALL=KMS; EVEN=[30000,60000,90000]
add(T,"engine_oil","replace",ALL,"שמן API SH ומעלה; עם שמן API SG ההחלפה כל 12,000 ק\"מ או שנה")
add(T,"oil_filter","replace",ALL)
add(T,"air_filter","inspect",[15000,30000,60000,75000],"ניקוי ובדיקה")
add(T,"air_filter","replace",[45000,90000])
add(T,"drive_belt","inspect",ALL,"רצועת אלטרנטור, משאבת מים והגה כוח")
add(T,"fuel_lines","inspect",EVEN)
add(T,"spark_plugs","inspect",EVEN,"ניקוי ובדיקה רק במצתים רגילים (לא אירידיום)")
add(T,"evap_system","inspect",[45000,90000],"מיכל פחם (canister)")
add(T,"exhaust","inspect",EVEN)
add(T,"clutch","inspect",ALL)
add(T,"manual_gearbox_oil","inspect",[30000,60000],"גיר ידני")
add(T,"manual_gearbox_oil","replace",[90000],"גיר ידני")
add(T,"transmission_oil","inspect",[45000],"גיר אוטומטי, כולל צינורות מצנן השמן")
add(T,"transmission_oil","replace",[90000],"גיר אוטומטי; צינורות מצנן השמן נבדקים")
add(T,"propshaft","inspect",EVEN,"רק בהנעה כפולה")
add(T,"cv_boots","inspect",EVEN)
add(T,"suspension","inspect",EVEN)
add(T,"steering","inspect",EVEN)
add(T,"wheel_alignment","inspect",[45000,90000],"בדיקת כיוון (toe-in)")
add(T,"pedals","inspect",EVEN)
add(T,"parking_brake","inspect",EVEN)
add(T,"brake_pads","inspect",ALL)
add(T,"brake_discs","inspect",ALL)
add(T,"brake_lines","inspect",EVEN,"כולל מפלס נוזל ושסתום P&B")
add(T,"brake_drums","inspect",EVEN,"תופים, רפידות תוף וצילינדרים")
add(T,"body_underside","inspect",ALL,"הידוק אומי גלגלים וברגי מרכב")
services=[{"km":k,"items":T[k]} for k in KMS]
base=dict(make="Daihatsu",make_he="דייהטסו",importer="",fuel="petrol",
 interval={"km":15000,"months":12,"note":"לפי לוח התחזוקה בספר השירות של דייהטסו לסדרת M300: טיפול כל 15,000 ק\"מ או שנה; בתנאים קשים שמן ומסנן כל 7,500 ק\"מ וחצי שנה"},
 cycle_km=90000,services=services,
 long_interval=[{"item":"spark_plugs","action":"replace","every_km":90000,"note":"מצתי אירידיום"}],
 time_based=[{"item":"coolant","action":"replace","every_months":24,"note":"נוזל קירור Long Life כל שנתיים"},
             {"item":"brake_fluid","action":"replace","every_months":24,"note":"כל שנתיים"},
             {"item":"evap_system","action":"replace","every_months":96,"note":"צינורות אדי דלק כל 8 שנים"}],
 specs={},status="draft")
src=[{"url":"https://procarmanuals.com/wp-content/uploads/pdfs/manuals/DAIHATSU-SIRION-Model-M300-Series-Service-Manual-No.9890/daihatsu-sirion-model-m300-series-service-manual-no9890-maintenance.pdf","kind":"manufacturer","note":"ספר השירות של דייהטסו לסדרת M300 (Service Manual No.9890, לרכבים מנובמבר 2004), פרק A2 Maintenance, עמ' A2-2 עד A2-4 (עמודי PDF 3-5); עותק באתר procarmanuals.com; הטבלה נקראה מתמונת העמודים"},
     {"url":"https://procarmanuals.com/daihatsu-sirion-model-m300-series-service-manual-no-9890-maintenance/","kind":"other","note":"עמוד האתר שמציג את הפרק (קובץ ה-PDF מוטמע)"}]
d=dict(id="daihatsu-sirion-2005-2011-1.3",model="Sirion",model_he="סיריון",generation="M300 (דור 2)",years=[2005,2011],engines=["1.3 (K3-VE)"],**base,sources=src,
 notes="טיוטה מספר השירות הבינלאומי של דייהטסו לסדרת M300 (אנגלית), לא מספר ישראלי; לא נמצא ספר או לוח של היבואן. טיפול כל 15,000 ק\"מ או שנה עם החלפת שמן ומסנן. מסנן אוויר מוחלף כל 45,000 ק\"מ ונוקה בשאר הטיפולים. נוזל קירור ונוזל בלמים כל שנתיים. שמן גיר ידני ונוזל גיר אוטומטי מוחלפים ב-90,000 ק\"מ. מצתי אירידיום כל 90,000 ק\"מ. אחרי 90,000 ק\"מ חוזרים על אותו מחזור.")
d["importer"]="טלקאר"
d2={k:v for k,v in d.items()}
json.dump(d,open(OUT+d['id']+'.json','w'),ensure_ascii=False,indent=2)
