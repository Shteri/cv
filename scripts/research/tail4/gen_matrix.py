from lib import *
import copy
cols = [15000 * i for i in range(1, 9)]
A = "I" * 8; E = "-I" * 4
rows = [("engine_oil", "R" * 8), ("oil_filter", "R" * 8),
        ("drive_belt", "-I-I-I-I", "רצועת משאבת מים, אלטרנטור ומזגן"), ("fuel_filter", "---R---R"), ("fuel_lines", A),
        ("timing_belt", "---I-R--", "בדיקה ב-60,000 והחלפה ב-90,000"), ("evap_system", E, "צינור אדים ומכסה פתח המילוי"),
        ("vacuum_hose", E, "צינורות אוורור בית הארכובה"), ("air_filter", "IIRIIRII"),
        ("spark_plugs", "-IR-IR-I"),
        ("cooling_system", A), ("manual_gearbox_oil", A), ("transmission_oil", A, "גיר אוטומטי (מחוץ לקהילה האירופית): בדיקה"),
        ("brake_lines", A), ("brake_fluid", E), ("brake_drums", E, "תופים ורפידות אחוריים ובלם חניה"), ("parking_brake", E),
        ("brake_pads", A), ("brake_discs", A), ("exhaust", A), ("suspension", A, "ברגי תושבות המתלים"),
        ("steering", A, "תיבת הגה, מוטות, גומיות ומפרק תחתון"), ("power_steering_fluid", A, "משאבת הגה כוח, רצועה וצינורות"),
        ("cv_boots", E), ("ac_refrigerant", A), ("cabin_filter", "R" * 8)]
SRC = {"url": "https://www.manualslib.com/manual/1215243/Hyundai-Matrix.html?page=197", "kind": "manufacturer",
       "note": "ספר הנהג הבינלאומי (GAT, General) של יונדאי מטריקס, פרק 5 'Vehicle maintenance requirements', עמודי האתר 197-199 (עמודי ספר 5-4 עד 5-6): טבלאות מנוע בנזין וכללית ב-8 עמודות של 15,000 ק\"מ עד 120,000; עמודות 'Except European Community'. נקרא מצילומי העמודים"}
base = {"make": "Hyundai", "make_he": "יונדאי", "fuel": "petrol", "importer": "כלמוביל",
 "interval": {"km": 15000, "months": 12, "note": "לפי הספר הבינלאומי: 15,000 ק\"מ או 12 חודשים, המוקדם"},
 "cycle_km": 120000, "services": grid(cols, rows),
 "long_interval": [L("coolant", "replace", every_km=45000, every_months=24, note="מחוץ לקהילה האירופית: נוזל קירור כל 45,000 ק\"מ או 24 חודשים (באירופה: לראשונה ב-90,000 או 60 חודשים, ואחר כך כל 45,000 או 24 חודשים)"),
                   L("valve_clearance", "inspect", every_km=90000, every_months=48, note="מנוע 1.8 DOHC בלבד")],
 "time_based": [], "specs": {"fuel": "בנזין נטול עופרת", "timing": "רצועת תזמון: בדיקה ב-60,000, החלפה ב-90,000"},
 "status": "draft"}
d = copy.deepcopy(base); d.update({"id": "hyundai-matrix-2001-2010-1.6-1.8", "model": "Matrix", "model_he": "מטריקס", "generation": "FC",
  "years": [2001, 2010], "engines": ["1.6 (Alpha II, G4ED)", "1.8 (Beta, G4GB)"], "sources": [SRC],
  "notes": "טיוטה מספר הנהג הבינלאומי של מטריקס (לא ספר ישראלי). נלקחו עמודות 'מחוץ לקהילה האירופית'. שמן כל 15,000 ק\"מ; מסנן אוויר מוחלף כל 45,000; מצתים כל 45,000; מסנן דלק כל 60,000; רצועת תזמון נבדקת ב-60,000 ומוחלפת ב-90,000; נוזל בלמים נבדק כל 30,000; מסנן מזגן בכל טיפול; נוזל קירור כל 45,000 ק\"מ או 24 חודשים."})
write(d)
d = copy.deepcopy(base); d.update({"id": "hyundai-elantra-2001-2006-1.6", "model": "Elantra", "model_he": "אלנטרה", "generation": "XD",
  "years": [2001, 2007], "engines": ["1.6 (Alpha II, G4ED)"], "sources": [dict(SRC, note=SRC["note"] + ". מקור אח: המטריקס בנויה על פלטפורמת אלנטרה XD עם אותו מנוע G4ED")],
  "notes": "טיוטה ממקור אח: הלוח הועתק מספר הנהג הבינלאומי של יונדאי מטריקס, שבנויה על פלטפורמת אלנטרה XD ומשתמשת באותו מנוע 1.6 G4ED. לא נמצא ספר של אלנטרה XD עם לוח בק\"מ. שמן כל 15,000; מסנן אוויר ומצתים כל 45,000; רצועת תזמון מוחלפת ב-90,000; נוזל קירור כל 45,000 ק\"מ או 24 חודשים."})
write(d)
