from lib import grid, write

MGUK = "https://www.mg.co.uk/servicing"
MG_IMP = "קאר איסט (קבוצת לובינסקי)"
MG_BLOCK = ("ספרי הנהג של היבואן באתר mg-israel.co.il/guide-books יושבים על lubinski.clearmash.com, שחסום מכאן (Cloudflare 403), ולכן זו טיוטה לפי טבלאות השירות של MG בריטניה. "
            "בבריטניה המרווח הוא 15,000 מייל או 12 חודשים; הומר ל-24,000 ק\"מ (15,000 מייל = כ-24,140 ק\"מ). ")
MG_ISR = {"url": "https://mg-israel.co.il/guide-books/", "kind": "importer", "note": "עמוד ספרי הרכב של MG ישראל; הקבצים ב-clearmash חסומים מכאן - לא נפתחו"}
OIL = [("engine_oil", "RRRRR"), ("oil_filter", "RRRRR", "כולל אטם בורג הניקוז")]

write({
    "id": "mg-zs-hybrid-2025-2026-1.5-hybrid",
    "make": "MG", "make_he": "אם.ג'י", "model": "ZS Hybrid+", "model_he": "ZS היברידי",
    "generation": "ZS (2024+) Hybrid+", "years": [2025, 2026], "engines": ["1.5 hybrid (15FHC)"], "fuel": "hybrid",
    "importer": MG_IMP,
    "interval": {"km": 24000, "months": 12, "note": "לפי טבלת השירות של MG בריטניה: כל 15,000 מייל (כ-24,000 ק\"מ) או 12 חודשים"},
    "cycle_km": 120000,
    "services": grid(24000, 5, OIL + [
        ("air_filter", "-R-R-"),
        ("cabin_filter", "-R-R-"),
        ("brake_fluid", "-R-R-"),
        ("spark_plugs", "--R--"),
        ("coolant", "----R"),
        ("fuel_filter", "---R-", "משאבת דלק עם מסנן משולב"),
        ("transmission_oil", "---R-", "שמן תיבת ההילוכים ההיברידית, כולל מסנן יניקה, מסנן לחץ ואטם"),
    ]),
    "specs": {"_note": "טיוטה - לפי MG בריטניה, לא נבדק מול ספר היבואן"},
    "sources": [{"url": MGUK, "kind": "manufacturer", "note": "MG Motor UK, Service Schedules - טבלת 'MG ZS Hybrid+ (2024 onwards)', 5 שנים/75,000 מייל"}, MG_ISR],
    "status": "draft",
    "notes": MG_BLOCK + "קוד המנוע 15FHC משותף ל-MG3 ההיברידית, ולכן ZS עם מנוע זה ברישוי (2025 ואילך) הוא גרסת Hybrid+. בטבלה הבריטית מוחלפות גם סוללות המפתחות כל שנתיים. נוזל הקירור מוחלף בשנה החמישית.",
})

write({
    "id": "mg-3-hybrid-2024-2026-1.5-hybrid",
    "make": "MG", "make_he": "אם.ג'י", "model": "MG3 Hybrid+", "model_he": "MG3 היברידית",
    "generation": "MG3 (2024+) Hybrid+", "years": [2024, 2026], "engines": ["1.5 hybrid (15FHC)"], "fuel": "hybrid",
    "importer": MG_IMP,
    "interval": {"km": 24000, "months": 12, "note": "לפי טבלת השירות של MG בריטניה: כל 15,000 מייל (כ-24,000 ק\"מ) או 12 חודשים"},
    "cycle_km": 120000,
    "services": grid(24000, 5, OIL + [
        ("air_filter", "-R-R-"),
        ("cabin_filter", "-R-R-"),
        ("brake_fluid", "-R-R-"),
        ("spark_plugs", "---R-"),
        ("coolant", "----R"),
        ("hybrid_battery_filter", "-R-R-", "מסנן יניקת האוויר של הסוללה ההיברידית"),
    ]),
    "specs": {"_note": "טיוטה - לפי MG בריטניה, לא נבדק מול ספר היבואן"},
    "sources": [{"url": MGUK, "kind": "manufacturer", "note": "MG Motor UK, Service Schedules - טבלת 'MG3 Hybrid+ (2024 onwards)', 5 שנים/75,000 מייל"},
                {"url": "https://cdn.mgmotor.eu/manuals/MG3-owner-manual-EN_compressed.pdf", "kind": "manufacturer", "note": "ספר הבעלים האירופי של MG3 Hybrid - מפנה לחוברת האחריות והתחזוקה, ללא טבלה"}, MG_ISR],
    "status": "draft",
    "notes": MG_BLOCK + "בטבלה הבריטית מוחלפות גם סוללות המפתחות כל שנתיים. נוזל הקירור מוחלף בשנה החמישית. MG3 עם מנוע 15FCD (בנזין בלבד) אינו בקובץ זה.",
})

write({
    "id": "mg-3-2025-2026-1.5",
    "make": "MG", "make_he": "אם.ג'י", "model": "MG3", "model_he": "MG3",
    "generation": "MG3 (2024+) petrol", "years": [2025, 2026], "engines": ["1.5 (15FCD)"], "fuel": "petrol",
    "importer": MG_IMP,
    "interval": {"km": 24000, "months": 12, "note": "לפי טבלת השירות של MG בריטניה: כל 15,000 מייל (כ-24,000 ק\"מ) או 12 חודשים"},
    "cycle_km": 120000,
    "services": grid(24000, 5, OIL + [
        ("air_filter", "-R-R-"),
        ("cabin_filter", "-R-R-"),
        ("brake_fluid", "-R-R-"),
        ("spark_plugs", "-R-R-"),
        ("coolant", "----R"),
    ]),
    "specs": {"_note": "טיוטה - לפי MG בריטניה, לא נבדק מול ספר היבואן"},
    "sources": [{"url": MGUK, "kind": "manufacturer", "note": "MG Motor UK, Service Schedules - טבלת 'MG3 (2024 onwards)'"}, MG_ISR],
    "status": "draft",
    "notes": MG_BLOCK + "השיוך של קוד המנוע 15FCD לגרסת הבנזין בלבד הוא הסקה (קוד 15FHC הוא ההיברידי). בטבלה הבריטית מוחלפות גם סוללות המפתחות כל שנתיים.",
})

write({
    "id": "mg-zs-2018-2021-1.0t",
    "make": "MG", "make_he": "אם.ג'י", "model": "ZS", "model_he": "ZS",
    "generation": "ZS (2017-2020)", "years": [2018, 2021], "engines": ["1.0T (10E4E)"], "fuel": "petrol",
    "importer": MG_IMP,
    "interval": {"km": 24000, "months": 12, "note": "לפי טבלת השירות של MG בריטניה: כל 15,000 מייל (כ-24,000 ק\"מ) או 12 חודשים"},
    "cycle_km": 120000,
    "services": grid(24000, 5, OIL + [
        ("fuel_filter", "-R-R-"),
        ("air_filter", "-R-R-"),
        ("cabin_filter", "-R-R-"),
        ("spark_plugs", "-R-R-"),
        ("brake_fluid", "-R-R-"),
        ("coolant", "---R-"),
        ("transmission_oil", "--R--", "רק בגיר אוטומטי"),
    ]),
    "specs": {"_note": "טיוטה - לפי MG בריטניה, לא נבדק מול ספר היבואן"},
    "sources": [{"url": MGUK, "kind": "manufacturer", "note": "MG Motor UK, Service Schedules - טבלת 'MG ZS (2017-2020)'; בטבלת 'MG ZS (2020-2024)' מצתי 1.0T מוחלפים רק בשנה השלישית"}, MG_ISR],
    "status": "draft",
    "notes": MG_BLOCK + "לפי הטבלה הבריטית לדגם שלפני מתיחת הפנים. בטבלה המאוחרת (2020-2024) מצתי מנוע 1.0T מוחלפים בשנה השלישית ונוזל הקירור בשנה החמישית - ייתכן שזה מתאים יותר לרכבי 2021. בטבלה מוחלפות גם סוללות המפתחות כל שנתיים.",
})

# ---------------- Chery FX EV = Omoda E5 ----------------
write({
    "id": "chery-fx-ev-2024-2026-ev",
    "make": "Chery", "make_he": "צ'רי", "model": "FX EV", "model_he": "FX EV",
    "generation": "FX EV (Omoda E5)", "years": [2024, 2026], "engines": ["EV (TZ210XS129 / TZ180SMZB0)"], "fuel": "electric",
    "importer": "פריסבי",
    "interval": {"km": 15000, "months": 12, "note": "לפי לוח השירות של צ'רי מלזיה ל-Omoda E5: כל 15,000 ק\"מ או 12 חודשים"},
    "cycle_km": 90000,
    "services": grid(15000, 6, [
        ("cabin_filter", "RRRRRR"),
        ("coolant", "--R--R", "נוזל קירור של מערכת ההנעה החשמלית"),
        ("brake_fluid", "--R--R"),
        ("transmission_oil", "--R--R", "שמן תיבת ההפחתה"),
        ("wipers", "-R-R-R", "פריט מומלץ"),
    ]),
    "long_interval": [
        {"item": "brake_pads", "action": "replace", "every_km": 75000, "every_months": 60, "note": "פריט מומלץ: רפידות קדמיות ואחוריות ב-75,000 ק\"מ (60 חודשים) וב-150,000 ק\"מ"},
    ],
    "specs": {"_note": "טיוטה - לפי צ'רי מלזיה, לא נבדק מול ספר היבואן"},
    "sources": [
        {"url": "https://www.chery.my/wp-content/uploads/2026/05/Chery_Service_Maintenance_Schedule_E5_2026-2.pdf", "kind": "manufacturer",
         "note": "Chery Malaysia, OMODA E5 Service Schedule & Pricing Guide (מאי 2026) - פריטי החלפה חובה ומומלצים לפי חודשים/ק\"מ"},
        {"url": "https://cdn.cworigin.com/omja/46593bd9b73f2b8bcc630b351d7cdfd10b69156c.pdf", "kind": "manufacturer",
         "note": "ספר הבעלים הבריטי של Omoda E5 (omodaauto.co.uk/downloads): קודי המנוע TZ210XS129 ו-TZ180SMZB0 זהים לרישוי הישראלי; הספר מפנה ללוח השירות ללא טבלה; סבב צמיגים כל 10,000 ק\"מ"},
    ],
    "status": "draft",
    "notes": "FX EV הוא הגרסה הישראלית של Omoda E5 (אותם קודי מנוע כמו בספר הבריטי). אתר היבואן cheryisrael.co.il חסום (Imperva) ולא נמצא ספר עברי; ספרי Omoda בבריטניה אינם כוללים טבלת טיפולים, ולכן זו טיוטה לפי לוח השירות של צ'רי מלזיה (אקלים חם). בלוח המלזי מופיעים רק פריטים להחלפה: מסנן מזגן בכל טיפול, ונוזל קירור, נוזל בלמים ושמן תיבת ההפחתה כל 45,000 ק\"מ או 36 חודשים. באוסטרליה המרווח המוצהר הוא 12 חודשים או 20,000 ק\"מ. הספר הבריטי ממליץ על סבב צמיגים כל 10,000 ק\"מ.",
})

# ---------------- Chery Tiggo 4 Hybrid = Tiggo Cross 1.5 DHT ----------------
write({
    "id": "chery-tiggo-4-hybrid-2025-2026-1.5-hev",
    "make": "Chery", "make_he": "צ'רי", "model": "Tiggo 4 Hybrid", "model_he": "טיגו 4 היברידי",
    "generation": "Tiggo 4 CSH (Tiggo Cross HEV)", "years": [2025, 2026], "engines": ["1.5 + DHT hybrid (SQRG4G15)"], "fuel": "hybrid",
    "importer": "פריסבי",
    "interval": {"km": 10000, "months": 6, "note": "לפי לוח השירות של צ'רי מלזיה ל-Tiggo Cross 1.5 DHT: כל 10,000 ק\"מ או 6 חודשים"},
    "cycle_km": 120000,
    "services": grid(10000, 12, [
        ("engine_oil", "RRRRRRRRRRRR"),
        ("oil_filter", "RRRRRRRRRRRR", "כולל אטם בורג הניקוז"),
        ("air_filter", "-R-R-R-R-R-R", "'Element air filter' בלוח - כנראה מסנן האוויר של המנוע"),
        ("spark_plugs", "--R--R--R--R"),
        ("brake_fluid", "---R---R---R"),
        ("transmission_oil", "---R---R---R", "שמן תיבת DHT"),
        ("coolant", "---R---R---R", "פריט מומלץ"),
        ("wipers", "-R-R-R-R-R-R", "פריט מומלץ"),
        ("brake_pads", "-----R-----R", "פריט מומלץ: קדמיות ואחוריות"),
        ("wheel_alignment", "IIIIIIIIIIII", "כיוון ואיזון מומלצים כל 10,000 ק\"מ"),
    ]),
    "specs": {"_note": "טיוטה - לפי צ'רי מלזיה, לא נבדק מול ספר היבואן"},
    "sources": [
        {"url": "https://www.chery.my/wp-content/uploads/2026/09/3Chery-Service-Maintenance-Schedule_TIGGO-CROSS_2026.pdf", "kind": "manufacturer",
         "note": "Chery Malaysia, TIGGO CROSS Service Schedule & Pricing Guide (ספטמבר 2026), עמודים 1-2: גרסת 1.5L + DHT (HEV)"},
    ],
    "status": "draft",
    "notes": "אתר היבואן cheryisrael.co.il חסום (Imperva) ולא נמצא ספר עברי. Tiggo Cross במלזיה הוא Tiggo 4 בשווקים אחרים, וגרסת 1.5 DHT שלו היא אותה מערכת היברידית; לכן זו טיוטה לפי לוח השירות המלזי (אקלים חם, מרווח קצר: 10,000 ק\"מ או חצי שנה). בלוח: שמן ומסנן בכל טיפול, מסנן אוויר כל 20,000, מצתים כל 30,000, נוזל בלמים ושמן גיר כל 40,000 ק\"מ; נוזל קירור, מגבים ורפידות הם פריטים מומלצים. הלוח לא מתייחס למסנן המזגן בנפרד.",
})
