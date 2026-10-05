from lib import *
import copy
cols = [10000 * i for i in range(1, 17)]
M = lambda m: f"לפי הגיליון: או {m} חודשים"
F80 = "---" + "-" * 4 + "I-I-I-I-I"   # 80k then every 20k
assert len(F80) == 16
rows = [
    ("drive_belt", "-I-I-I-I-I-I-I-I", "בגיליון: או 24 חודשים"),
    ("engine_oil", "IIIIIIIIIIIIIIII", "הגיליון מסמן I (אבחון) בכל 10,000 ק\"מ או 12 חודשים; ההחלפה לפי מצב השמן"),
    ("oil_filter", "IIIIIIIIIIIIIIII", "כמו שמן המנוע: I בכל 10,000 ק\"מ או 12 חודשים"),
    ("cooling_system", F80, "אבחון ראשון ב-80,000 ק\"מ (או 48 חודשים) ואז כל 20,000 ק\"מ (או 12 חודשים)"),
    ("coolant", "---I---I---I---R", None),
    ("coolant_hoses", F80, "צינורות ומחברי מצנן שמן המנוע: אבחון ראשון ב-80,000 ק\"מ ואז כל 20,000"),
    ("exhaust", "-I-I-I-I-I-I-I-I", None),
    ("battery_12v", "IIIIIIIIIIIIIIII", None),
    ("fuel_filter", "-------R-------R", "כולל המסנן שבמיכל; או 96 חודשים"),
    ("air_filter", "-R-R-R-R-R-R-R-R".replace("-R-R", "-I-R"), None),
    ("fuel_lines", F80, "כולל מכסה מיכל הדלק: אבחון ראשון ב-80,000 ק\"מ ואז כל 20,000"),
    ("evap_system", "---I---I---I---I", "מסנן פחם; או 24 חודשים"),
    ("pedals", "IIIIIIIIIIIIIIII", None), ("parking_brake", "IIIIIIIIIIIIIIII", None),
    ("brake_drums", "-I-I-I-I-I-I-I-I", "תופים ורפידות כולל בלם החניה"),
    ("brake_pads", "IIIIIIIIIIIIIIII", None), ("brake_discs", "IIIIIIIIIIIIIIII", None),
    ("brake_fluid", "IIIRIIIRIIIRIIIR", None),
    ("brake_lines", "-I-I-I-I-I-I-I-I", None),
    ("power_steering_fluid", "IIIIIIIIIIIIIIII", None),
    ("steering", "IIIIIIIIIIIIIIII", None),
    ("propshaft", "IIIIIIIIIIIIIIII", "גלי הינע קדמי ואחורי: גירוז (L בגיליון) והידוק ברגים (T) בכל טיפול"),
    ("propshaft", "AAAAAAAAAAAAAAAA", "הידוק ברגי גלי ההינע"),
    ("cv_boots", "-I-I-I-I-I-I-I-I", None),
    ("suspension", "IIIIIIIIIIIIIIII", "מתלים, מחברים כדוריים ומגיני אבק"),
    ("transmission_oil", "---I---I---I---I", None),
    ("transfer_case_oil", "---I---I---I---I", None),
    ("differential_oil", "-I-R-I-R-I-R-I-R", "קדמי ואחורי"),
    ("tires", "IIIIIIIIIIIIIIII", None), ("lights", "IIIIIIIIIIIIIIII", None), ("wipers", "IIIIIIIIIIIIIIII", None),
    ("cabin_filter", "CRCRCRCRCRCRCRCR", None),
    ("ac_refrigerant", "-I-I-I-I-I-I-I-I", None),
]
rows = [(r[0], r[1], r[2]) if r[2] else (r[0], r[1]) for r in rows]
services = grid(cols, rows)
long_items = [
    L("spark_plugs", "replace", every_km=100000, note="בגיליון: החלפה כל 100,000 ק\"מ"),
    L("coolant", "replace", first_km=160000, then_every_km=80000, note="נוזל קירור מנוע SLLC: החלפה ראשונה ב-160,000 ואז כל 80,000"),
    L("cooling_system", "inspect", first_km=80000, first_months=48, then_every_km=20000, then_every_months=12, note="גם צינורות מצנן השמן וצנרת הדלק באותו מרווח"),
]
specs = {
    "engine_oil": "API SL/SM/SN (לפי טבלת הנוזלים בגיליון)", "oil_capacity": "6.1 ליטר (לפי הגיליון)",
    "coolant": "Toyota SLLC, 10.5 ליטר (לפי הגיליון)", "brake_fluid": "DOT 3 (SAE J1703 / FMVSS 116), לפי הגיליון",
    "fuel": "בנזין 95 אוקטן", "timing": "שרשרת, ללא החלפה מתוכננת",
    "_note": "שמנים ונוזלים לפי טבלת הנוזלים בגיליון: גיר אוטומטי Toyota ATF WS, תיבת העברה LF 75W (1.4 ליטר), דיפרנציאלים API GL-5 75W-85, הגה כוח ATF Dexron III",
}
SRC = {"url": "https://books.union-motors.co.il/app/api/files/599/download", "kind": "importer",
       "note": "לוח אחזקה של יוניון מוטורס 'לנד קרוזר בנזין 2009', מנוע 1GR-FE (מעודכן 20.02.2017): 16 עמודות של 10,000 ק\"מ עד 160,000 וטבלת נוזלים; נבדק מול תמונת הגיליון (קואורדינטות הטקסט)"}
HUB = {"url": "https://www.toyota.co.il/owners/parts-and-accessories/owners-manuals", "kind": "importer",
       "note": "מרכז ספרות הרכב של טויוטה ישראל; המסמכים נשלפים מ-books.union-motors.co.il (דגם Land Cruiser, id 11)"}
base_notes = ("לפי גיליון האחזקה של יוניון מוטורס ל-1GR-FE: 16 עמודות של 10,000 ק\"מ. בגיליון שמן ומסנן שמן מסומנים I (אבחון) בכל 10,000 ק\"מ או 12 חודשים, "
              "מצתים מוחלפים כל 100,000, מסנן אוויר נבדק כל 20,000 ומוחלף כל 40,000 (בתנאים קשים בדיקה כל 10,000), "
              "מערכת הקירור, צינורות מצנן השמן וצנרת הדלק נבדקים לראשונה ב-80,000 ואז כל 20,000, נוזל קירור מוחלף ב-160,000 ואז כל 80,000. "
              "שורות 'מחמירה' (שטח/אבק): בלמים, הגה, מתלים וצירים כל 5,000 ק\"מ או 3 חודשים, שמן גיר אוטומטי החלפה כל 80,000, שמן תיבת העברה החלפה כל 40,000, שמן דיפרנציאלים החלפה כל 20,000, הידוק ברגי מתלים ושלדה בכל טיפול.")
d = {"id": "toyota-land-cruiser-2009-2019-4.0", "make": "Toyota", "make_he": "טויוטה", "model": "Land Cruiser", "model_he": "לנד קרוזר",
     "generation": "J150 petrol", "years": [2009, 2019], "engines": ["4.0 V6 (1GR-FE)"], "fuel": "petrol", "importer": "יוניון מוטורס",
     "interval": {"km": 10000, "months": 12, "note": "לפי הגיליון: כל 10,000 ק\"מ; לכל פריט מצוין בגיליון גם מרווח בחודשים (שמן 12, בלמים ומתלים 6)"},
     "cycle_km": 160000, "services": services, "long_interval": long_items, "time_based": [], "specs": specs,
     "sources": [SRC, HUB], "status": "reviewed",
     "notes": base_notes + " גרסה מתוקנת: בגרסה הקודמת חסרו המצתים ומסנן האוויר ושורות 80,000+20,000 נקראו לא נכון."}
write(copy.deepcopy(d))
d2 = copy.deepcopy(d)
d2.update(id="toyota-land-cruiser-2003-2008-4.0", generation="J120 (Prado) petrol", years=[2003, 2008], status="draft",
          notes="טיוטה: ליוניון מוטורס אין גיליון לדור J120 בנזין (ה-API מחזיר ללנד קרוזר רק גיליונות מ-2009). הלוח לקוח מגיליון הלנד קרוזר J150 בנזין עם אותו מנוע 1GR-FE. " + base_notes)
d2["sources"][0] = dict(SRC, note=SRC["note"] + " — גיליון של הדור הבא (J150) עם אותו מנוע; לא גיליון ייעודי ל-J120")
write(d2)
