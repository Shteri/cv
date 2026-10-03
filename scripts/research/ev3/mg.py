from lib import grid, write
ROWS = [
    ("engine_oil", "RRRRR", None),
    ("oil_filter", "RRRRR", "כולל אטם בורג הניקוז"),
    ("air_filter", "-R-R-", None),
    ("cabin_filter", "-R-R-", None),
    ("brake_fluid", "-R-R-", None),
    ("spark_plugs", "--R--", None),
    ("fuel_filter", "---R-", None),
    ("transmission_oil", "---R-", "שמן תיבת ההילוכים ההיברידית"),
    ("coolant", "----R", None),
]
UKSRC = {"url": "https://www.mg.co.uk/servicing", "kind": "manufacturer",
         "note": "MG Motor UK, Service Schedules - טבלת 'MG HS Plug-in Hybrid (2024 onwards)', 5 שנים/75,000 מייל"}
ILSRC = {"url": "https://mg-israel.co.il/guide-books/", "kind": "importer",
         "note": "עמוד ספרי הרכב של MG ישראל; הספרים נשלחים רק אחרי מילוי מספר טלפון בטופס ולא נפתחו (ב-REST של האתר נדרשת התחברות)"}
INTERVAL = {"km": 24000, "months": 12,
            "note": "לפי טבלת השירות של MG בריטניה ל-HS פלאג-אין (2024 ואילך): כל 15,000 מייל (כ-24,000 ק\"מ) או 12 חודשים"}
common = dict(make="MG", make_he="אם.ג'י", fuel="plug-in-hybrid", importer="קאר איסט (קבוצת לובינסקי)",
              interval=INTERVAL, cycle_km=120000, services=grid(24000, 5, ROWS), status="draft")

write(dict(common, id="mg-s9-2026-1.5t-phev", model="S9 PHEV", model_he="S9 פלאג-אין", generation="MGS9 PHEV (7 מושבים)",
    years=[2026, 2026], engines=["1.5T PHEV (15FKE)"],
    specs={"engine_oil": "0W-20, ACEA C5 / API SP", "oil_capacity": "4 ליטר",
           "coolant": "מנוע: 10 ליטר; מעגל יחידת הבקרה של מנוע ההנעה: 7 ליטר (גליקול OAT)",
           "brake_fluid": "DOT 4", "fuel": "בנזין 95 ומעלה",
           "tires": "245/50 R20 או 255/45 RF20", "tire_pressure": "2.4 בר מלפנים ומאחור",
           "battery": "סוללת הנעה BR065A21S1 (65Ah) + מצבר 12V",
           "_note": "טיוטה. מפרטים מספר הנהג האירופי של MGS9 PHEV (עמ' 348-356); תיבת ההילוכים: Castrol BOT794, 4.35 ליטר"},
    sources=[UKSRC,
             {"url": "https://cdn.mgmotor.eu/manuals/MGS9-PHEV-Owner-Manual-EN_compressed.pdf", "kind": "manufacturer",
              "note": "MGS9 PHEV Owner Manual (אירופה): אין בו טבלת טיפולים (מפנה לחוברת האחריות והתחזוקה); נתונים טכניים עמ' 348-356"},
             ILSRC],
    notes="לא נמצא ספר עברי (הספרים של MG ישראל נשלחים רק דרך טופס) ובספר הנהג האירופי של S9 אין טבלת טיפולים. "
          "לכן זו טיוטה לפי טבלת השירות של MG בריטניה לדגם האחות HS פלאג-אין (2024 ואילך), עם אותו מנוע 1.5 טורבו 15FKE ומערכת היברידית נטענת "
          "(גם EHS 2025-2026 ברישוי הישראלי נושא את קוד המנוע 15FKE). "
          "המרווח בבריטניה 15,000 מייל או שנה, הומר ל-24,000 ק\"מ. שמן ומסנן בכל טיפול; מסנן אוויר, מסנן מזגן ונוזל בלמים כל שנתיים; "
          "מצתים בטיפול השלישי; מסנן דלק ושמן תיבה בטיפול הרביעי; נוזל קירור בטיפול החמישי. בטבלה הבריטית מוחלפות גם סוללות המפתחות כל שנתיים."))

write(dict(common, id="mg-ehs-2025-2026-1.5t-phev", model="EHS PHEV", model_he="EHS פלאג-אין", generation="HS PHEV דור 2 (2024 ואילך)",
    years=[2025, 2026], engines=["1.5T PHEV (15FKE)"],
    specs={"_note": "טיוטה - לפי MG בריטניה, לא נבדק מול ספר היבואן"},
    sources=[UKSRC, ILSRC],
    notes="ספרי הנהג של MG ישראל נשלחים רק דרך טופס ולא נפתחו, ולכן זו טיוטה לפי טבלת השירות של MG בריטניה ל-HS פלאג-אין (2024 ואילך), "
          "שהוא ה-EHS מהדור החדש (קוד מנוע 15FKE ברישוי, שונה מ-15E4E של הדור הקודם). המרווח בבריטניה 15,000 מייל או שנה, הומר ל-24,000 ק\"מ. "
          "שמן ומסנן בכל טיפול; מסנן אוויר, מסנן מזגן ונוזל בלמים כל שנתיים; מצתים בטיפול השלישי; מסנן דלק ושמן תיבה בטיפול הרביעי; נוזל קירור בטיפול החמישי. "
          "בטבלה הבריטית מוחלפות גם סוללות המפתחות כל שנתיים."))
