from lib import *
import copy
cols = [10000 * i for i in range(1, 17)]
def x(p8):  # 8 columns of 20k -> 16 columns of 10k
    return "".join("-" + c for c in p8)
A = "IIIIIIII"
rows = [("engine_oil", "R" * 16), ("oil_filter", "R" * 16),
        ("air_filter", x("IRIRIRIR")), ("evap_system", x("--I--I--"), "צינור אדים ומכסה מיכל הדלק"),
        ("fuel_filter", x("IIRIIRII"), "מחסנית מסנן סולר; תלוי באיכות הסולר (EN590)"), ("fuel_lines", x(A)),
        ("battery_12v", x(A)), ("electrical_system", x(A)), ("brake_lines", x(A)), ("pedals", x(A)), ("parking_brake", x(A)), ("brake_fluid", x(A)),
        ("brake_pads", x(A)), ("brake_discs", x(A)), ("power_steering_fluid", x(A)), ("steering", x(A)), ("cv_boots", x(A)), ("tires", x(A)),
        ("suspension", x(A), "מפרקים כדוריים קדמיים"), ("body_underside", x(A), "ברגים ואומים בשלדה ובמרכב"), ("ac_refrigerant", x(A)), ("ac_system", x(A)),
        ("cabin_filter", x("RRRRRRRR")), ("transfer_case_oil", x("--I--I--"), "4x4"), ("differential_oil", x("--I--I--"), "דיפרנציאל אחורי (4x4)"),
        ("propshaft", x("-I-I-I-I"), "4x4"), ("exhaust", x("-I-I-I-I"))]
base = {"make": "Kia", "make_he": "קיה", "importer": "טלקאר", "fuel": "diesel",
 "interval": {"km": 10000, "months": 12, "note": "לפי ספר היבואן: שמן ומסנן כל 10,000 ק\"מ או 12 חודשים (למעט אירופה); שאר הטבלה בעמודות של 20,000 ק\"מ / 12 חודשים"},
 "cycle_km": 160000, "services": grid(cols, rows),
 "long_interval": [L("drive_belt", "inspect", first_km=80000, first_months=48, then_every_km=20000, then_every_months=12, note="רצועות הנעה (אלטרנטור, הגה כוח, משאבת מים, מזגן)"),
                   L("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24, note="בנוסף: בדיקת מפלס ודליפות כל יום"),
                   L("coolant", "replace", first_km=200000, first_months=120, then_every_km=40000, then_every_months=24),
                   L("manual_gearbox_oil", "inspect", every_km=60000, every_months=48, note="גיר ידני; גיר אוטומטי - ללא בדיקה וללא טיפול")],
 "time_based": [], "specs": {"fuel": "סולר (EN590)"}}
SRC = {"url": "https://cdnmedia.kia-israel.co.il/www/cars-book/Sportage-SL-2011-2015.pdf", "kind": "importer",
       "note": "ספר רכב ספורטאז' 2011-2015 של קיה ישראל, פרק 7 עמ' 15-18 (עמודי PDF 295-298): 'תכנית תחזוקה רגילה - מנוע דיזל', 8 עמודות של 20,000 ק\"מ / 12 חודשים עד 160,000; הפונט מקודד, נקרא מתמונות העמודים"}
d = copy.deepcopy(base); d.update({"id": "kia-sportage-2011-2015-2.0-diesel", "model": "Sportage", "model_he": "ספורטאז'", "generation": "SL",
  "years": [2010, 2015], "engines": ["2.0 CRDi (R, D4HA)"], "sources": [SRC], "status": "reviewed",
  "notes": "הועתק מטבלת הדיזל בספר הרכב העברי של קיה ישראל לספורטאז' SL. שמן ומסנן כל 10,000 ק\"מ או שנה (למעט אירופה); מסנן אוויר מוחלף כל 40,000 (בסין, הודו והמזרח התיכון כל 15,000); מחסנית מסנן הסולר כל 60,000; מסנן מזגן כל 20,000; נוזל הבלמים נבדק בכל טיפול. רצועות הנעה: בדיקה ראשונה ב-80,000 ואחר כך כל 20,000. גיר אוטומטי ללא טיפול."})
write(d)
d = copy.deepcopy(base); d.update({"id": "hyundai-ix35-2010-2015-2.0-diesel", "make": "Hyundai", "make_he": "יונדאי", "importer": "כלמוביל", "model": "ix35", "model_he": "ix35", "generation": "LM",
  "years": [2010, 2015], "engines": ["2.0 CRDi (R, D4HA)"], "sources": [dict(SRC, note=SRC["note"] + ". מקור אח: ספורטאז' SL ו-ix35 חולקים פלטפורמה ומנוע D4HA")], "status": "draft",
  "notes": "טיוטה ממקור אח: הלוח הועתק מטבלת הדיזל בספר העברי של קיה ספורטאז' SL, התאומה של ix35 עם אותו מנוע 2.0 CRDi (D4HA). גם הספר הבינלאומי של ix35 קובע לדיזל מחוץ לאירופה שמן כל 10,000 ק\"מ. מסנן אוויר כל 40,000; מסנן סולר כל 60,000; מסנן מזגן כל 20,000."})
write(d)
