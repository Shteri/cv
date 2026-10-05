from lib import *
import copy
cols = [10000 * i for i in range(1, 17)]
A = "I" * 16; E = "-I" * 8; Q = "---I" * 4
DB = "---------I-I-I-I"   # first 100k then every 20k
CS40 = "---I---I-I-I-I-I"  # 40k, 80k, then every 20k
AIR = "IIRIIRIIRIIRIIRI"   # inspect every 10k, replace every 30k
SEP = "מפריד מים במערכת הדלק: בדיקה בכל טיפול"
OIL = [L("engine_oil", "replace", every_km=30000, every_months=24, note="לפי נורת ההתראה של מערכת הטיפולים, או 30,000 ק\"מ / 24 חודשים, המוקדם מביניהם; מסנן השמן מוחלף בכל החלפת שמן"),
       L("oil_filter", "replace", every_km=30000, every_months=24)]
COOL = L("coolant", "replace", first_km=160000, then_every_km=80000, note="נוזל קירור SLLC: החלפה ראשונה ב-160,000 ואז כל 80,000")
BELT = L("drive_belt", "inspect", first_km=100000, first_months=72, then_every_km=20000, then_every_months=12, note="בדיקה ראשונה ב-100,000 ק\"מ (או 72 חודשים) ואז כל 20,000 (או 12 חודשים); החלפה לפי הצורך")
AIRL = L("air_filter", "replace", every_km=30000, every_months=36, note="בדיקה כל 10,000 ק\"מ (או 6 חודשים); בתנאי אבק בדיקה כל 2,500 ק\"מ")
SEV = ("שורות 'מחמירה' בגיליון (שטח, אבק, גרירה): רפידות/תופים, צנרת בלמים, מסרק הגה, גירוז והידוק גלי הינע, מתלים ושרוולי ציריות בדיקה כל 5,000 ק\"מ או 3 חודשים; "
       "נוזל גיר אוטומטי החלפה כל 80,000, שמן תיבת העברה כל 40,000, שמן דיפרנציאלים כל 20,000; הידוק ברגי מתלים ושלדה בכל טיפול.")
common_chassis = [
    ("pedals", A), ("parking_brake", A),
    ("brake_pads", A), ("brake_discs", A), ("brake_fluid", "IIIRIIIRIIIRIIIR"), ("brake_lines", E),
    ("power_steering_fluid", A),
    ("propshaft", A, "גלי הינע קדמי ואחורי: גירוז (L בגיליון)"), ("propshaft", "A" * 16, "הידוק ברגי גלי ההינע (T בגיליון)"),
    ("cv_boots", E), ("transfer_case_oil", Q), ("differential_oil", "-I-R-I-R-I-R-I-R", "קדמי ואחורי"),
    ("tires", A), ("lights", A), ("wipers", A), ("cabin_filter", "CRCRCRCRCRCRCRCR"), ("ac_refrigerant", E),
]
def build(rid, rows, long_items, time_based, srcs, notes):
    d = json.load(open(f"/home/user/cv/data/schedules/{rid}.json"))
    d["services"] = grid(cols, rows)
    d["long_interval"] = long_items
    d["time_based"] = time_based
    d["sources"] = srcs + [s for s in d["sources"] if "toyota.co.il" in s["url"]]
    d["notes"] = notes
    d["interval"] = {"km": 10000, "months": 6, "note": "לפי הגיליון: כל 10,000 ק\"מ; לכל פריט מצוין בגיליון מרווח בחודשים (בלמים, הגה ומתלים 6, רוב השאר 12-48). שמן ומסנן לפי נורת ההתראה או 30,000 ק\"מ / 24 חודשים"}
    d["status"] = "reviewed"
    write(d)
U = "https://books.union-motors.co.il/app/api/files/{}/download"
# ---- LC J120 1KD (sheet 297, conn 173) ----
rows297 = [("timing_belt", "--------------R-"), ("valve_clearance", Q), ("drive_belt", DB),
    ("cooling_system", Q), ("coolant", "---I---I---I---R"), ("exhaust", E), ("battery_12v", A),
    ("fuel_filter", "-R-R-R-R-R-R-R-R", "מסנן סולר: החלפה כל 20,000 (או 24 חודשים)"), ("fuel_filter", A, SEP),
    ("air_filter", AIR), ("exhaust", Q, "בדיקת עשן סמיך"), ("fuel_lines", Q),
    ("brake_drums", E), ("steering", A), ("suspension", A, "מתלים, מחברים כדוריים ומגיני אבק"), ("transmission_oil", Q)] + common_chassis
build("toyota-land-cruiser-2003-2009-3.0-diesel", rows297, OIL + [COOL, BELT, AIRL,
      L("timing_belt", "replace", every_km=150000, note="בתנאים קשים גם בדיקה כל 30,000, ובדיקת גלגלת וניקוי מכסה התזמון")], [],
  [{"url": U.format(173), "kind": "importer", "note": "לוח אחזקה של יוניון מוטורס 'לנד קרוזר 2002-2009', מנוע 1KD-FTV (20.03.2016, fileId 297): 16 עמודות של 10,000 ק\"מ וטבלת נוזלים; נקרא לפי קואורדינטות הטקסט ונבדק מול תמונת הגיליון"}],
  "לפי גיליון האחזקה של יוניון מוטורס ל-1KD-FTV (16 עמודות של 10,000 ק\"מ). רצועת תזמון מוחלפת ב-150,000; מסנן סולר כל 20,000; מסנן אוויר נבדק כל 10,000 ומוחלף כל 30,000; רצועת הינע נבדקת לראשונה ב-100,000 ואז כל 20,000; מרווח שסתומים כל 40,000; מד זרימת האוויר מנוקה בנשיפת אוויר כל 60,000 (או 72 חודשים); משאבת הוואקום נבדקת כל 200,000. " + SEV + " גרסה מתוקנת: בגרסה הקודמת חסר מסנן האוויר, ורצועת ההינע ונוזל הקירור נקראו בעמודות שגויות.")
# ---- LC J150 1KD (sheet 298, conn 175) ----
rows298 = [("timing_belt", "--------------R-"), ("valve_clearance", Q), ("drive_belt", E),
    ("cooling_system", CS40, "בדיקה ב-40,000 וב-80,000 ואז כל 20,000"), ("coolant", "---I---I---I---R"), ("exhaust", E), ("battery_12v", A),
    ("fuel_filter", "-R-R-R-R-R-R-R-R", "מסנן סולר: החלפה כל 20,000 (או 24 חודשים)"), ("fuel_filter", A, SEP),
    ("air_filter", AIR), ("exhaust", Q, "בדיקת עשן סמיך"), ("fuel_lines", CS40, "בדיקה ב-40,000 וב-80,000 ואז כל 20,000"),
    ("brake_drums", E), ("steering", A), ("suspension", A, "מתלים, מחברים כדוריים ומגיני אבק"), ("transmission_oil", Q)] + common_chassis
build("toyota-land-cruiser-2010-2015-3.0-diesel", rows298, OIL + [COOL, AIRL,
      L("timing_belt", "replace", every_km=150000, note="בתנאים קשים גם בדיקה כל 30,000, ובדיקת גלגלת וניקוי מכסה התזמון")],
  [{"item": "exhaust", "action": "replace", "months": 36, "note": "צינורות גמישים של מכלול ה-DPF: החלפה כל 36 חודשים"}],
  [{"url": U.format(175), "kind": "importer", "note": "לוח אחזקה של יוניון מוטורס 'לנד קרוזר 2009-2015', מנוע 1KD-FTV (fileId 298): 16 עמודות של 10,000 ק\"מ וטבלת נוזלים; נקרא לפי קואורדינטות הטקסט ונבדק מול תמונת הגיליון"}],
  "לפי גיליון האחזקה של יוניון מוטורס ל-1KD-FTV עם DPF (16 עמודות של 10,000 ק\"מ). רצועת תזמון מוחלפת ב-150,000; רצועת הינע נבדקת כל 20,000; מסנן סולר כל 20,000; מסנן אוויר נבדק כל 10,000 ומוחלף כל 30,000; מערכת הקירור וצנרת הדלק נבדקות ב-40,000 וב-80,000 ואז כל 20,000; צינורות ה-DPF הגמישים מוחלפים כל 36 חודשים; מד זרימת האוויר מנוקה כל 60,000; משאבת הוואקום נבדקת כל 200,000. " + SEV + " גרסה מתוקנת: בגרסה הקודמת חסר מסנן האוויר, ומערכת הקירור, צנרת הדלק ונוזל הקירור נקראו בעמודות שגויות.")
# ---- LC J150 1GD (sheet 299, conn 199) ----
rows299 = [("drive_belt", DB), ("cooling_system", Q), ("coolant", "---I---I---I---R"), ("exhaust", E), ("battery_12v", A),
    ("fuel_filter", A, SEP), ("air_filter", AIR), ("exhaust", Q, "בדיקת עשן סמיך"), ("fuel_lines", Q),
    ("steering", A), ("suspension", A, "מתלים, מחברים כדוריים ומגיני אבק"),
    ("transmission_oil", Q, "כולל צינורות וחיבורי מצנן נוזל הגיר")] + [r for r in common_chassis if r[0] != "parking_brake"] + [("parking_brake", E, "מכלול בלם החניה: בדיקה כל 20,000 (בתנאים קשים כל 10,000)")]
build("toyota-land-cruiser-2016-2019-2.8-diesel", rows299, OIL + [COOL, BELT, AIRL],
  [{"item": "exhaust", "action": "replace", "months": 36, "note": "צינורות גמישים של מכלול ה-DPF: החלפה כל 36 חודשים"}],
  [{"url": U.format(199), "kind": "importer", "note": "לוח אחזקה של יוניון מוטורס 'Land Cruiser' 2016-2019, מנוע 1GD-FTV (fileId 299): 16 עמודות של 10,000 ק\"מ וטבלת נוזלים; נקרא לפי קואורדינטות הטקסט ונבדק מול תמונת הגיליון"}],
  "לפי גיליון האחזקה של יוניון מוטורס ל-1GD-FTV (16 עמודות של 10,000 ק\"מ). בגיליון אין שורת החלפת מסנן סולר (רק בדיקת מפריד המים בכל טיפול) ואין רצועת תזמון (שרשרת). מסנן אוויר נבדק כל 10,000 ומוחלף כל 30,000; רצועת הינע נבדקת לראשונה ב-100,000 ואז כל 20,000; צינורות ה-DPF הגמישים מוחלפים כל 36 חודשים; משאבת הוואקום נבדקת כל 200,000; מסנן המזגן בתנאים קשים מוחלף כל 15,000. " + SEV + " גרסה מתוקנת: בגרסה הקודמת חסרו מסנן האוויר, הרפידות והדיסקיות, שרוולי הציריות והדיפרנציאלים, ורצועת ההינע ונוזל הקירור נקראו בעמודות שגויות.")
# ---- Hilux Vigo 2KD manual (295, conn 385) + 1KD automatic (296, conn 386) ----
rowsHX = [("timing_belt", "--I--I--I--I--R-", "בדיקה כל 30,000 והחלפה ב-150,000; גלגלת התזמון נבדקת ומכסה התזמון מנוקה באותם מועדים"),
    ("valve_clearance", Q), ("drive_belt", DB), ("cooling_system", Q), ("coolant", "---I---I---I---R"), ("exhaust", E), ("battery_12v", A),
    ("fuel_filter", A, SEP), ("air_filter", AIR), ("exhaust", Q, "בדיקת עשן סמיך"), ("fuel_lines", Q),
    ("brake_drums", E), ("clutch", A, "נוזל מצמד"), ("steering", E), ("suspension", A, "מחברים כדוריים ומגיני אבק"), ("suspension", E, "מתלים קדמי ואחורי"),
    ("manual_gearbox_oil", Q, "גיר ידני (גיליון 295)"), ("transmission_oil", Q, "גיר אוטומטי (גיליון 296)")] + common_chassis
build("toyota-hilux-2005-2015-2.5-3.0-diesel", rowsHX, OIL + [COOL, BELT, AIRL, L("timing_belt", "replace", every_km=150000)],
  [{"item": "exhaust", "action": "replace", "months": 36, "note": "צינורות גמישים של מכלול ה-DPF (אם קיים): החלפה כל 36 חודשים"}],
  [{"url": U.format(385), "kind": "importer", "note": "לוח אחזקה של יוניון מוטורס 'Hilux Manual Euro5 2005-2015', מנוע 2KD-FTV (fileId 295): 16 עמודות של 10,000 ק\"מ; נקרא לפי קואורדינטות הטקסט ונבדק מול הגיליון"},
   {"url": U.format(386), "kind": "importer", "note": "לוח אחזקה 'Hilux Automatic Euro5 2005-2015', מנוע 1KD-FTV (fileId 296): אותו לוח, עם נוזל גיר אוטומטי במקום שמן גיר ידני; בו גלגלת התזמון ומכסה התזמון מסומנים כשורות 'מחמירה'"}],
  "לפי גיליונות האחזקה של יוניון מוטורס להילוקס ויגו (2KD-FTV ידני, 1KD-FTV אוטומטי), 16 עמודות של 10,000 ק\"מ. רצועת תזמון נבדקת כל 30,000 ומוחלפת ב-150,000; מרווח שסתומים כל 40,000; רצועת הינע נבדקת לראשונה ב-100,000 ואז כל 20,000; מסנן אוויר נבדק כל 10,000 ומוחלף כל 30,000; בגיליונות אין שורת החלפת מסנן סולר (רק בדיקת מפריד המים); מסרק ההגה והמתלים נבדקים כל 20,000 (המחברים הכדוריים כל טיפול); מד זרימת האוויר מנוקה כל 60,000; משאבת הוואקום נבדקת כל 200,000. "
  "שורות 'מחמירה': בלמים, הגה, מתלים וגלי הינע כל 5,000 ק\"מ; שמן גיר ידני ותיבת העברה כל 40,000; נוזל גיר אוטומטי כל 80,000; דיפרנציאלים כל 20,000. גרסה מתוקנת: בגרסה הקודמת החלפת רצועת התזמון ב-150,000 נקראה כנוזל קירור, רצועת ההינע נקראה בעמודה שגויה, והמתלים ומסרק ההגה סומנו בכל טיפול במקום כל 20,000.")
