from lib import *
import copy
cols = [15000 * i for i in range(1, 9)]
A = "I" * 8; E = "-I" * 4; Q = "---I---I"
rows = [("drive_belt", E, "בדיקת רצועה, מותחן, גלגלת ביניים וגלגלת אלטרנטור"), ("air_filter", "IIRIIRII"),
        ("evap_system", Q, "צינור אדים ומכסה פתח המילוי"), ("fuel_tank_air_filter", Q), ("fuel_lines", Q),
        ("cooling_system", A), ("electrical_system", A), ("battery_12v", A),
        ("brake_lines", A), ("pedals", E), ("parking_brake", E), ("brake_fluid", "-R" * 4),
        ("brake_pads", A), ("brake_discs", A), ("steering", A), ("cv_boots", E), ("tires", A), ("tire_rotation", "T" * 8),
        ("suspension", A, "מפרקים כדוריים של המתלה הקדמי"), ("ac_refrigerant", A), ("ac_system", A, "מדחס המזגן"),
        ("cabin_filter", "IR" * 4), ("transmission_oil", E), ("exhaust", E),
        ("differential_oil", Q, "דיפרנציאל קדמי (AWD) ואחורי: בדיקה"), ("propshaft", E)]
SRC = {"url": "https://www.manualslib.com/manual/4105563/Genesis-Gv70-Jk1-2025.html?page=601", "kind": "manufacturer",
       "note": "ספר הנהג באנגלית של Genesis GV70 (JK1, 2025), פרק Maintenance, עמודי האתר 601-605 (עמודי ספר 593-597): 'Normal maintenance schedule (Petrol engine)' בק\"מ, 8 עמודות של 15,000 עד 120,000, וטבלת תנאים קשים. השוק לא מצוין; הניסוח ('authorised Genesis repairer', שמן כל 10,000 ק\"מ) תואם לספרי בריטניה/אוסטרליה. נקרא מצילומי העמודים"}
base = {"make": "Genesis", "make_he": "ג'נסיס", "fuel": "petrol", "importer": "כלמוביל",
 "interval": {"km": 15000, "months": 12, "note": "לפי הספר: שמן ומסנן שמן (ותוסף דלק) כל 10,000 ק\"מ או 12 חודשים - ראו long_interval; שאר הבדיקות בטבלה של 15,000 ק\"מ או 12 חודשים. ייתכן שהרכב מצויד במערכת חיי שמן שמתריעה מוקדם יותר. בתנאים קשים שמן כל 5,000 ק\"מ או 6 חודשים"},
 "cycle_km": 120000, "services": grid(cols, rows),
 "long_interval": [L("engine_oil", "replace", every_km=10000, every_months=12, note="שמן מנוע סינתטי מלא API SN PLUS ומעלה; כל 10,000 ק\"מ או 12 חודשים"),
                   L("oil_filter", "replace", every_km=10000, every_months=12),
                   L("spark_plugs", "replace", every_km=75000, note="מצתים: כל 75,000 ק\"מ"),
                   L("coolant", "replace", first_km=195000, first_months=120, then_every_km=30000, then_every_months=24, note="החלפה ראשונה ב-195,000 ק\"מ או 120 חודשים, אחר כך כל 30,000 ק\"מ או 24 חודשים")],
 "time_based": [], "specs": {"engine_oil": "API SN PLUS ומעלה, סינתטי מלא", "fuel": "בנזין 95 אוקטן"},
 "status": "draft"}
d = copy.deepcopy(base); d.update({"id": "genesis-gv70-2021-2026-2.5-turbo", "model": "GV70", "model_he": "GV70", "generation": "JK1",
 "years": [2021, 2026], "engines": ["2.5 T-GDI (Smartstream G2.5T, G4KR)"], "sources": [SRC],
 "notes": "טיוטה מספר הנהג הבינלאומי באנגלית של GV70 2025 (לא ספר ישראלי; ספר עברי של היבואן לא נמצא באתר כלמוביל). הטבלה היא למנועי הבנזין. שמן כל 10,000 ק\"מ או שנה; מסנן אוויר מוחלף כל 45,000, מסנן מזגן כל 30,000, נוזל בלמים כל 30,000 ק\"מ או 24 חודשים, מצתים כל 75,000. תיבת העברה ודיפרנציאל e-LSD: ללא טיפול לפי הספר. ייתכן שהלוח של דגמי 2021-2024 (לפני מתיחת הפנים) שונה מעט."})
write(d)
d = copy.deepcopy(base); d.update({"id": "genesis-g80-2021-2026-2.5-turbo", "model": "G80", "model_he": "G80", "generation": "RG3",
 "years": [2021, 2026], "engines": ["2.5 T-GDI (Smartstream G2.5T, G4KR)"],
 "sources": [dict(SRC, note=SRC["note"] + ". מקור אח: GV70 על אותה פלטפורמה (M3) ועם אותו מנוע G4KR")],
 "notes": "טיוטה ממקור אח: הלוח של GV70 2025 (ספר בינלאומי באנגלית), שבנוי על אותה פלטפורמה ועם אותו מנוע 2.5 טורבו G4KR כמו ה-G80. לא נמצא ספר ישראלי ולא ספר G80 עם לוח בק\"מ. שמן כל 10,000 ק\"מ או שנה, מסנן אוויר כל 45,000, מצתים כל 75,000, נוזל בלמים כל 30,000 ק\"מ או 24 חודשים."})
write(d)
