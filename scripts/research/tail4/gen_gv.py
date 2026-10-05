from lib import *
cols = [15000 * i for i in range(1, 7)]
A = "IIIIII"; E = "-I-I-I"
rows = [("engine_oil", "RRRRRR"), ("oil_filter", "RRRRRR"),
        ("drive_belt", "--I--R", "רצועה שטוחה (V-rib); ברצועת V: בדיקה ב-15/45/75 אלף והחלפה ב-30/60/90 אלף"),
        ("valve_clearance", E, "מנוע G16 בלבד"), ("coolant", "--R--R"), ("exhaust", E),
        ("spark_plugs", "--R--R", "מצתי ניקל ברכב עם חיישן חמצן (HO2S); אירידיום: כל 105,000 ק\"מ"),
        ("air_filter", "IIRIIR"), ("fuel_lines", E), ("pcv_valve", "-----I"), ("evap_system", "-----I"),
        ("clutch", E), ("brake_pads", A), ("brake_discs", A), ("brake_drums", E), ("brake_lines", E), ("brake_fluid", "-R-R-R"),
        ("parking_brake", "I-----", "ידית וכבל בלם החניה: בדיקה ב-15,000 הראשונים בלבד"),
        ("tires", A), ("suspension", E), ("propshaft", "--I--I", "גלי הינע קדמיים ואחוריים"), ("cv_boots", "--I--I"),
        ("manual_gearbox_oil", "I-R--R", "גיר ידני: בדיקה ב-15,000 הראשונים בלבד, החלפה ב-45,000 וב-90,000"),
        ("transmission_oil", E, "גיר אוטומטי: בדיקת מפלס; צינור הנוזל מוחלף ב-60,000; החלפת נוזל כל 165,000"),
        ("transfer_case_oil", "I-I-I-"), ("differential_oil", "R-I-I-", "החלפה או בדיקה ב-15,000 הראשונים, אחר כך בדיקה"),
        ("steering", E), ("power_steering_fluid", A), ("door_hinges", E), ("cabin_filter", "-IR-IR", "מסנן מזגן (אם קיים)")]
svc = grid(cols, rows)
for s in svc:
    if s["km"] in (45000, 90000):
        if not any(e["item"] == "fuel_lines" for e in s["items"]): s["items"].append({"item": "fuel_lines", "action": "inspect", "note": "בדיקת מיכל הדלק"})
        else:
            for e in s["items"]:
                if e["item"] == "fuel_lines": e["note"] = "כולל בדיקת מיכל הדלק"
write({"id": "suzuki-grand-vitara-1998-2005-1.6-2.0", "make": "Suzuki", "make_he": "סוזוקי", "model": "Grand Vitara", "model_he": "גרנד ויטרה",
 "generation": "FT/GT (SQ416 / SQ420)", "years": [1998, 2006], "engines": ["1.6 (G16B)", "2.0 (J20A)"], "fuel": "petrol", "importer": "מכשירי תנועה",
 "interval": {"km": 15000, "months": 12, "note": "לפי ספר השירות של סוזוקי: 15,000 ק\"מ או 12 חודשים; במנוע G16 בלי חיישן חמצן או בגרסאות SE/SF שמן כל 10,000 ק\"מ או 8 חודשים"},
 "cycle_km": 90000, "services": svc,
 "long_interval": [L("timing_belt", "replace", every_km=100000, note="רצועת תזמון - מנוע G16 בלבד: כל 100,000 ק\"מ (מותר להחליף כבר ב-90,000)"),
                   L("fuel_filter", "replace", every_km=105000, note="מסנן דלק: כל 105,000 ק\"מ"),
                   L("transmission_oil", "replace", every_km=165000, note="נוזל גיר אוטומטי: החלפה כל 165,000 ק\"מ")],
 "time_based": [],
 "specs": {"fuel": "בנזין נטול עופרת", "timing": "G16: רצועת תזמון כל 100,000 ק\"מ; J20: שרשרת", "_note": "מצתים: ניקל BKR6E-11 / K20PR-U11; אירידיום IFR6E11 (G16), IFR5J11 (J20)"},
 "sources": [{"url": "https://www.manualslib.com/manual/1212471/Suzuki-Sq-416-420-625.html?page=29", "kind": "manufacturer",
              "note": "ספר השירות של סוזוקי לויטרה/גרנד ויטרה SQ416/SQ420/SQ625, פרק 0B, עמודי האתר 29-30: 'Maintenance schedule under normal driving conditions' עד 90,000 ק\"מ; נקרא מצילום העמוד"}],
 "status": "draft",
 "notes": "טיוטה מספר השירות הבינלאומי של סוזוקי לגרנד ויטרה הדור הראשון (מנועי G16 ו-J20), לא מספר ישראלי. אחרי 90,000 ק\"מ חוזרים על אותו מחזור. רצועת תזמון (G16 בלבד) כל 100,000 ק\"מ; נוזל קירור ומסנן אוויר כל 45,000; נוזל בלמים כל 30,000; שמן גיר ידני ב-45,000 וב-90,000; שמן תיבת העברה ודיפרנציאל נבדקים כל 30,000 החל מ-15,000."})
