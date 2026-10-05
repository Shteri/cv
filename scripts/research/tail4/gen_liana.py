from lib import *
cols = [15000 * i for i in range(1, 7)]
A = "IIIIII"; E = "-I-I-I"
rows = [("engine_oil", "RRRRRR"), ("oil_filter", "RRRRRR"),
        ("drive_belt", "--I--R"), ("valve_clearance", E), ("coolant", "--R--R"), ("exhaust", E),
        ("spark_plugs", "--R--R", "מצתי ניקל ברכב עם חיישן חמצן (HO2S); מצתי אירידיום: כל 105,000 ק\"מ (long_interval)"),
        ("air_filter", "IIRIIR"), ("fuel_lines", E), ("fuel_tank_air_filter", "------"),
        ("pcv_valve", "-----I"), ("evap_system", "-----I"),
        ("brake_pads", A), ("brake_discs", A), ("brake_drums", E), ("brake_lines", E), ("brake_fluid", "-R-R-R"),
        ("parking_brake", "I-----", "ידית וכבל בלם החניה: בדיקה ב-15,000 הראשונים בלבד"),
        ("clutch", E), ("tires", A), ("suspension", E), ("steering", E), ("cv_boots", "--I--I"),
        ("manual_gearbox_oil", "I-R--R", "גיר ידני: בדיקה ב-15,000 הראשונים בלבד, החלפה ב-45,000 וב-90,000"),
        ("transmission_oil", E, "גיר אוטומטי: בדיקת מפלס; החלפה כל 165,000 ק\"מ"),
        ("door_hinges", E), ("power_steering_fluid", A)]
rows = [r for r in rows if r[0] != "fuel_tank_air_filter"]
svc = grid(cols, rows)
# fuel tank inspection at 45k and 90k -> note on fuel_lines at those services
for s in svc:
    if s["km"] in (45000, 90000):
        s["items"].append({"item": "fuel_lines", "action": "inspect", "note": "בדיקת מיכל הדלק"}) if not any(e["item"] == "fuel_lines" for e in s["items"]) else None
        for e in s["items"]:
            if e["item"] == "fuel_lines": e["note"] = "כולל בדיקת מיכל הדלק"
    if s["km"] == 60000:
        for e in s["items"]:
            if e["item"] == "transmission_oil": e["note"] = "גיר אוטומטי: בדיקת מפלס ובדיקת צינורות מצנן השמן"
write({"id": "suzuki-liana-2002-2008-1.6", "make": "Suzuki", "make_he": "סוזוקי", "model": "Liana", "model_he": "ליאנה",
 "generation": "RH416 (ER)", "years": [2002, 2008], "engines": ["1.6 (M16A)"], "fuel": "petrol", "importer": "מכשירי תנועה",
 "interval": {"km": 15000, "months": 12, "note": "לפי ספר השירות של סוזוקי לליאנה: 15,000 ק\"מ או 12 חודשים, המוקדם; בתנאים קשים שמן ומסנן כל 5,000 ק\"מ או 4 חודשים"},
 "cycle_km": 90000, "services": svc,
 "long_interval": [L("fuel_filter", "replace", every_km=105000, note="מסנן דלק: כל 105,000 ק\"מ"),
                   L("spark_plugs", "replace", every_km=105000, every_months=84, note="חלופה: מצתי אירידיום ברכב עם חיישן חמצן - כל 105,000 ק\"מ או 84 חודשים"),
                   L("transmission_oil", "replace", every_km=165000, note="נוזל גיר אוטומטי: החלפה כל 165,000 ק\"מ")],
 "time_based": [],
 "specs": {"fuel": "בנזין נטול עופרת", "_note": "מצתים לפי הספר: ניקל NGK BKR6E-11 / DENSO K20PR-U11; אירידיום NGK IFR6E11 / IFR6J11"},
 "sources": [{"url": "https://www.manualslib.com/manual/1292260/Suzuki-Liana-Rh413.html?page=33", "kind": "manufacturer",
              "note": "ספר השירות של סוזוקי לליאנה (Liana RH413, קוד S3RH0A), פרק Maintenance and Lubrication, עמודי האתר 33-34: טבלת 'Normal Condition Schedule' עד 90,000 ק\"מ וטבלת תנאים קשים; נקרא מצילום העמוד"},
             {"url": "https://www.manualslib.com/manual/1292254/Suzuki-Liana-Rh418.html", "kind": "manufacturer", "note": "מוסף ספר השירות (RH418) - נבדק התוכן בלבד"}],
 "status": "draft",
 "notes": "טיוטה מספר השירות הבינלאומי של סוזוקי לליאנה, לא מספר ישראלי (לא נמצא ספר של היבואן). הטבלה של הספר משותפת לכל מנועי הליאנה ואינה תלויה במנוע. אחרי 90,000 ק\"מ חוזרים על אותו מחזור. נוזל קירור ומסנן אוויר מוחלפים כל 45,000, נוזל בלמים כל 30,000, רצועת אביזרים נבדקת ב-45,000 ומוחלפת ב-90,000, חופש שסתומים נבדק כל 30,000. בתנאי אבק: מסנן אוויר נבדק כל 2,500 ק\"מ ומוחלף כל 30,000. ברכבי 4x4 יש גם בדיקות שמן תיבת העברה ודיפרנציאל אחורי לפי הספר."})
