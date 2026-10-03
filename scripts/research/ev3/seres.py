from lib import write
S = [
    {"item": "brake_pads", "action": "inspect", "note": "בלמים: רפידות, דיסקים קדמיים ואחוריים, צינורות, מהלך דוושת הבלם ובלם החניה"},
    {"item": "brake_discs", "action": "inspect"},
    {"item": "brake_lines", "action": "inspect"},
    {"item": "brake_fluid", "action": "inspect", "note": "בדיקת מפלס"},
    {"item": "steering", "action": "inspect", "note": "גלגל ההגה ותיבת ההגה, סיבובי הצירים וגבולות ההיגוי"},
    {"item": "door_hinges", "action": "inspect", "note": "ניקוי וסיכה של מנעולי הדלתות, צירים ומוטות התמיכה של מכסה המנוע והדלת האחורית"},
    {"item": "suspension", "action": "inspect", "note": "זרועות התלייה, בולמי זעזועים, מומנט ברגי השלדה והגחון"},
    {"item": "tires", "action": "inspect", "note": "לחץ ניפוח, אומי גלגלים, איזון (לפי הצורך)"},
    {"item": "cv_boots", "action": "inspect", "note": "שרוולי גלי ההינע"},
    {"item": "transmission_oil", "action": "inspect", "note": "מפלס שמן תיבת ההפחתה"},
    {"item": "wheel_alignment", "action": "inspect", "note": "כיוון גלגלים לפי הצורך"},
    {"item": "seat_belts", "action": "inspect"},
    {"item": "lights", "action": "inspect", "note": "תאורה ואמצעי איתות, מערכת השטיפה (מגבים ומיכל)"},
    {"item": "battery_12v", "action": "inspect"},
    {"item": "ac_system", "action": "inspect"},
    {"item": "hybrid_system", "action": "inspect", "note": "סוללת ההנעה: קיבול, כבל הכוח, תושבת ההתקנה, ניקוי מעטפת; רתמות מתח גבוה (מיזוג PTC, מנוע, מטען); מערכת הטעינה AC/DC"},
    {"item": "electrical_system", "action": "inspect", "note": "מנוע ההנעה ובקר המנוע: ברגי התקנה, כבלי הארקה, צינורות קירור, ניקוי חיצוני"},
    {"item": "cabin_filter", "action": "replace"},
]
write(dict(
    id="seres-5-m5-2023-2025-ev", make="Seres", make_he="סרס", model="SERES 5 / M5", model_he="סרס 5 / M5", generation="SERES 5 (M5 EV)",
    years=[2023, 2025], engines=["EV (SE200 / SE165+SE200 / SEP201)"], fuel="electric", importer="טלקאר מוטורס",
    interval={"km": 20000, "months": 12, "note": "לפי ספר הנהג העברי של SERES M5: בדיקה תקופתית כל שנה או 20,000 ק\"מ"},
    cycle_km=20000,
    services=[{"km": 20000, "items": S}],
    long_interval=[
        {"item": "brake_fluid", "action": "replace", "every_km": 60000, "every_months": 36, "note": "נוזל בלמים: כל 3 שנים או 60,000 ק\"מ"},
        {"item": "coolant", "action": "replace", "every_km": 100000, "every_months": 48, "note": "נוזל הקירור של סוללת ההנעה: כל 4 שנים או 100,000 ק\"מ"},
        {"item": "transmission_oil", "action": "replace", "every_km": 100000, "every_months": 60, "note": "שמן תיבת ההפחתה (Castrol 805C EV): בדיקה בכל טיפול, החלפה כל 5 שנים או 100,000 ק\"מ"},
    ],
    specs={"battery": "סוללת הנעה + מצבר 12V", "_note": "שמן תיבת ההפחתה: Castrol 805C EV (ספר הנהג עמ' 205)"},
    sources=[
        {"url": "https://seres.co.il/wp-content/uploads/2024/10/SERES_M5_EV_OM_24-09-24-S1-Sh-LowRes.pdf", "kind": "importer",
         "note": "ספר נהג SERES M5 בעברית (24.09.2024): מרווחי הטיפולים עמ' 206 בקובץ (205 בספר), פירוט הבדיקות עמ' 207 (206 בספר). שכבת הטקסט מקודדת בגופן מוזז; נקרא מתמונת העמוד"},
        {"url": "https://seres.co.il/wp-content/uploads/2023/09/seres5_חוברת.pdf", "kind": "importer",
         "note": "חוברת אחריות ושירות SERES 5 (סרוקה): מפנה לספר הנהג לגבי תכנית התחזוקה"},
    ],
    status="reviewed",
    notes="לפי ספר הנהג העברי של SERES M5 (בגוף הספר הרכב נקרא EV SERES 5). בדיקה תקופתית כל שנה או 20,000 ק\"מ של הבלמים, ההיגוי, המתלים, הצמיגים, החשמל, סוללת ההנעה ומערכת הטעינה, עם החלפת מסנן מזגן. "
          "נוזל בלמים כל 3 שנים/60,000 ק\"מ, נוזל קירור הסוללה כל 4 שנים/100,000 ק\"מ ושמן תיבת ההפחתה כל 5 שנים/100,000 ק\"מ. "
          "שיוך רכבי 'SERES' משנים 2023-2024 (מנוע SEP201) לאותו ספר הוא הנחה: זה השם הקודם של אותו דגם.",
))
