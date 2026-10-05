from lib import *
cols = [15000 * i for i in range(1, 7)]
A = "IIIIII"; E = "-I-I-I"
rows = [("engine_oil", "RRRRRR"), ("oil_filter", "RRRRRR"),
        ("drive_belt", "--I--R"), ("valve_clearance", E), ("coolant", "--R--R"), ("exhaust", E),
        ("spark_plugs", "--R--R", "מצתי ניקל ברכב עם חיישן חמצן (HO2S); מצתי אירידיום: כל 105,000 ק\"מ (long_interval)"),
        ("air_filter", "IIRIIR"), ("fuel_lines", "-I-I-I"), ("pcv_valve", "-----I"), ("evap_system", "-----I"),
        ("brake_pads", A), ("brake_discs", A), ("brake_drums", E), ("brake_lines", E), ("brake_fluid", "-R-R-R"),
        ("parking_brake", "I-----", "ידית וכבל בלם החניה: בדיקה ב-15,000 הראשונים בלבד"),
        ("clutch", E), ("tires", A), ("suspension", E), ("steering", E), ("cv_boots", "--I--I"),
        ("manual_gearbox_oil", "I-R--R", "גיר ידני: בדיקה ב-15,000 הראשונים בלבד, החלפה ב-45,000 וב-90,000"),
        ("transmission_oil", E, "גיר אוטומטי: בדיקת מפלס; החלפה כל 165,000 ק\"מ"), ("door_hinges", E)]
svc = grid(cols, rows)
for s in svc:
    if s["km"] in (45000, 90000):
        if not any(e["item"] == "fuel_lines" for e in s["items"]): s["items"].append({"item": "fuel_lines", "action": "inspect", "note": "בדיקת מיכל הדלק"})
        else:
            for e in s["items"]:
                if e["item"] == "fuel_lines": e["note"] = "כולל בדיקת מיכל הדלק"
write({"id": "suzuki-ignis-2001-2007-1.3", "make": "Suzuki", "make_he": "סוזוקי", "model": "Ignis", "model_he": "איגניס",
 "generation": "FH (HT51S / RG413)", "years": [2001, 2007], "engines": ["1.3 (M13A)"], "fuel": "petrol", "importer": "מכשירי תנועה",
 "interval": {"km": 15000, "months": 12, "note": "לפי ספר השירות של סוזוקי לאיגניס: 15,000 ק\"מ או 12 חודשים, המוקדם"},
 "cycle_km": 90000, "services": svc,
 "long_interval": [L("fuel_filter", "replace", every_km=105000, note="מסנן דלק: כל 105,000 ק\"מ"),
                   L("spark_plugs", "replace", every_km=105000, every_months=84, note="חלופה: מצתי אירידיום ברכב עם חיישן חמצן - כל 105,000 ק\"מ או 84 חודשים"),
                   L("transmission_oil", "replace", every_km=165000, note="נוזל גיר אוטומטי: החלפה כל 165,000 ק\"מ")],
 "time_based": [],
 "specs": {"fuel": "בנזין נטול עופרת", "_note": "מצתים לפי הספר: ניקל NGK BKR6E-11 / DENSO K20PR-U11; אירידיום NGK IFR5E11"},
 "sources": [{"url": "https://www.manualslib.com/manual/1586259/Suzuki-Ignis.html?page=36", "kind": "manufacturer",
              "note": "ספר השירות של סוזוקי לאיגניס (פרק 0B Maintenance and Lubrication), עמודי האתר 36-37 (עמודי ספר 0B-2 עד 0B-3): טבלת תנאים רגילים עד 90,000 ק\"מ; נקרא מצילום העמוד"}],
 "status": "draft",
 "notes": "טיוטה מספר השירות הבינלאומי של סוזוקי לאיגניס הדור הראשון, לא מספר ישראלי (לא נמצא ספר של היבואן). אחרי 90,000 ק\"מ חוזרים על אותו מחזור. נוזל קירור ומסנן אוויר מוחלפים כל 45,000, נוזל בלמים כל 30,000, רצועת אביזרים נבדקת ב-45,000 ומוחלפת ב-90,000, חופש שסתומים נבדק כל 30,000. ברכבי 4x4 יש גם בדיקות שמן תיבת העברה ודיפרנציאל אחורי לפי הספר."})
