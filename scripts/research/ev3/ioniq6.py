from lib import grid, write
I8 = "IIIIIIII"
ROWS = [
    ("cooling_system", I8, None),
    ("transmission_oil", "-I-I-I-I", "נוזל תיבת ההפחתה - בדיקה"),
    ("battery_12v", I8, None),
    ("electrical_system", I8, "כל מערכת החשמל"),
    ("brake_lines", I8, "צינורות וחיבורים"),
    ("pedals", I8, "דוושת בלמים"),
    ("parking_brake", I8, None),
    ("brake_fluid", "RRRRRRRR", None),
    ("brake_pads", I8, "צלחות ורפידות"),
    ("steering", I8, "מנגנון היגוי, מוטות קישור וגומיות הגנה"),
    ("cv_boots", I8, "גלי הינע וגומיות ההגנה"),
    ("tires", I8, "לחץ ושחיקת סוליה"),
    ("suspension", I8, "מפרקי המתלה"),
    ("body_underside", I8, "ברגים ואומים על השלדה והגוף"),
    ("ac_refrigerant", I8, None),
    ("ac_system", I8, "מדחס מיזוג אוויר"),
    ("cabin_filter", "RRRRRRRR", None),
]
write(dict(
    id="hyundai-ioniq-6-2023-2026-ev", make="Hyundai", make_he="יונדאי", model="Ioniq 6", model_he="איוניק 6", generation="CE",
    years=[2023, 2026], engines=["EV (EM17)"], fuel="electric", importer="כלמוביל",
    interval={"km": 30000, "months": 24, "note": "לפי ספר הרכב העברי: כל 30,000 ק\"מ או 24 חודשים"},
    cycle_km=240000,
    services=grid(30000, 8, ROWS),
    long_interval=[
        {"item": "coolant", "action": "replace", "first_km": 200000, "first_months": 120, "then_every_km": 40000, "then_every_months": 24,
         "note": "נוזל קירור: החלפה ראשונה ב-200,000 ק\"מ או 10 שנים, אחר כך כל 40,000 ק\"מ או 24 חודשים"},
    ],
    time_based=[{"item": "ecall_battery", "action": "replace", "months": 36, "note": "סוללת מערכת eCall (אם קיימת) - כל 3 שנים"}],
    specs={"brake_fluid": "DOT 4", "battery": "סוללת הנעה + מצבר 12V"},
    sources=[
        {"url": "https://res.cloudinary.com/colmobil/images/v1716387969/ספר-רכב-איוניק-6-2023/ספר-רכב-איוניק-6-2023.pdf", "kind": "importer",
         "note": "ספר רכב איוניק 6 בעברית (2023; קובץ 2024 זהה), לוח תחזוקה רגילה עמ' 533-534 בקובץ, תנאים קשים עמ' 535"},
        {"url": "https://res.cloudinary.com/colmobil/images/v1782805535/Ioniq6-2026-OM-web/Ioniq6-2026-OM-web.pdf", "kind": "importer",
         "note": "ספר רכב איוניק 6 2026 בעברית: אותה טבלה בעמ' 480-481, תנאים קשים עמ' 483"},
    ],
    status="reviewed",
    notes="לפי ספרי הרכב העבריים של כלמוביל (2023/2024 ו-2026, הטבלה זהה). טיפול כל 30,000 ק\"מ או שנתיים: החלפת נוזל בלמים ומסנן מזגן ובדיקות של מערכות הקירור, החשמל, הבלמים, ההיגוי, המתלים, הצמיגים והמיזוג; "
          "נוזל תיבת ההפחתה נבדק כל 60,000 ק\"מ (בתנאים קשים מוחלף כל 120,000 ק\"מ). נוזל הקירור מוחלף לראשונה ב-200,000 ק\"מ או 10 שנים ואחר כך כל 40,000 ק\"מ או שנתיים. סוללת eCall מוחלפת כל 3 שנים.",
))
