import sys, json, os, io, contextlib
sys.argv = ['x']
with contextlib.redirect_stdout(io.StringIO()):
    import bs
ST = "/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/tail4"
bs.OUT = ST
T = bs
T.TY_MAP.append((r"^ומכסה מיכל הדלק", ["fuel_lines"]))
T.TY_MAP.insert(0, (r"סוללה היברידית", ["hybrid_battery_filter"]))
T.TY_MAP.insert(0, (r"נוזל קירור מערכת היברידית", ["coolant"]))
# new-generation C-HR hybrid (2024+): Union returns sheet 362 for C-HR Hybrid 2023-2025 and the 2024 car book is 'C-HR HEV 2024'
T.toyota("toyota-c-hr-2024-2026-1.8-hybrid", 362, "C-HR", "C-HR", "AX20 hybrid (דור שני)", [2024, 2026], ["1.8 hybrid (2ZR-FXE)"], "hybrid", extra_sheets=(361,),
         specs=dict(T.TY_OIL_NEW, spare="ערכת תיקון", **T.HYB),
         notes_extra="הגיליון (דצמבר 2023) הוא מה שהיבואן מחזיר ל-C-HR היברידי 2024-2025 (ספר הרכב 'C-HR HEV 2024'); גיליון 361 ('c-hr') זהה. נוזל קירור מנוע: בדיקה כל 30,000 והחלפה ב-150,000; מצתים ב-90,000; מסנן דלק ב-120,000.")
T.toyota("toyota-aygo-x-2026-1.5-hybrid", 366, "Aygo X", "איגו X", "AB70 hybrid", [2026, 2026], ["1.5 hybrid (M15A-FXE)"], "hybrid",
         specs=dict(T.TY_OIL_NEW, spare="ערכת תיקון", **T.HYB),
         notes_extra="הגיליון כולל 18 עמודות עד 270,000; כאן מוצג מחזור של 150,000. בגיליון: מצתים כל 90,000, מסנן דלק כל 75,000, נוזל קירור מנוע החלפה ב-150,000, נוזל בלמים כל 30,000.")
# J120 Prado 4.0 V6 petrol: no Union sheet for the J120 petrol; same 1GR-FE engine as the J150 petrol sheet 300 -> draft
T.toyota("toyota-land-cruiser-2003-2008-4.0", 300, "Land Cruiser", "לנד קרוזר", "J120 (Prado) petrol", [2003, 2008], ["4.0 V6 (1GR-FE)"], "petrol",
         notes_extra="טיוטה: ליוניון מוטורס אין גיליון לדור J120 בנזין. הלוח לקוח מגיליון הלנד קרוזר J150 בנזין (2009-2019) עם אותו מנוע 1GR-FE; לגבי הדיזל, היבואן מחזיק גיליונות כמעט זהים לשני הדורות (297/298). " + T.TY_4X4_NOTE,
         specs=dict(T.TY_OIL_OLD, fuel="בנזין 95 אוקטן"))
p = os.path.join(ST, "toyota-land-cruiser-2003-2008-4.0.json"); d = json.load(open(p)); d["status"] = "draft"
d["sources"][0]["note"] += " — גיליון של הדור הבא (J150) עם אותו מנוע; לא גיליון ייעודי ל-J120"
json.dump(d, open(p, "w"), ensure_ascii=False, indent=2)
# tidy: within one service drop an inspect of an item that is replaced in the same service
import glob
for p in glob.glob(os.path.join(ST, "toyota-*.json")):
    d = json.load(open(p))
    for s in d["services"]:
        rep = {e["item"] for e in s["items"] if e["action"] == "replace"}
        s["items"] = [e for e in s["items"] if not (e["item"] in rep and e["action"] != "replace")]
    json.dump(d, open(p, "w"), ensure_ascii=False, indent=2)
