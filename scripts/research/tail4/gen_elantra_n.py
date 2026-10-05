from lib import *
cols = [15000 * i for i in range(1, 17)]
A = "I" * 16; E = "-I" * 8
rows = [("engine_oil", "R" * 16), ("oil_filter", "R" * 16),
        ("cooling_system", "II-I-I-I-I-I-I-I"),
        ("fuel_filter", "---R---R---R---R"), ("spark_plugs", "----R----R------"),
        ("battery_12v", E), ("electrical_system", E),
        ("brake_lines", A), ("pedals", A), ("parking_brake", A),
        ("brake_fluid", "IIRIIRIIRIIRIIRI"), ("brake_pads", A), ("brake_discs", A),
        ("steering", A), ("cv_boots", E, "בדיקת חופשים בגלי ההינע"), ("tires", A), ("suspension", A),
        ("ac_refrigerant", E), ("ac_system", E, "מדחס המזגן"), ("cabin_filter", "-R" * 8)]
write({"id": "hyundai-elantra-n-2025-2026-2.0-turbo", "make": "Hyundai", "make_he": "יונדאי", "model": "Elantra N", "model_he": "אלנטרה N",
 "generation": "CN7 N", "years": [2025, 2026], "engines": ["2.0 T-GDI (Theta III, G4KH)"], "fuel": "petrol", "importer": "כלמוביל",
 "interval": {"km": 15000, "months": 12, "note": "לפי לוח התחזוקה בספר הנהג העברי: 15,000 ק\"מ או 12 חודשים, המוקדם; ייתכן שהרכב מצויד במערכת חיי שמן"},
 "cycle_km": 240000, "services": grid(cols, rows),
 "long_interval": [L("coolant", "replace", first_km=210000, first_months=168, then_every_km=30000, then_every_months=24, note="החלפה ראשונה ב-210,000 ק\"מ או 168 חודשים, אחר כך כל 30,000 ק\"מ או 24 חודשים")],
 "time_based": [{"item": "ecall_battery", "action": "replace", "months": 36, "note": "החלפת סוללת E-CALL כל 3 שנים"}],
 "specs": {"fuel": "בנזין 95 אוקטן (RON 95)", "brake_fluid": "DOT 4"},
 "sources": [{"url": "https://res.cloudinary.com/colmobil/images/v1777979411/elantra-n-2025-all-webreduced_307404cd83/elantra-n-2025-all-webreduced_307404cd83.pdf",
              "kind": "importer", "note": "ספר הוראות תפעול לנהג אלנטרה N 2025 (כלמוביל), PDF עמ' 407 (עמוד ספר 9-8): 'לוח תחזוקה רגילה (המשך)', 16 עמודות של 15,000 ק\"מ עד 240,000; הטבלה מסובבת ונקראה מתמונה"},
             {"url": "https://www.hyundaimotors.co.il/maintenance/", "kind": "importer", "note": "מרכז ספרי הרכב של כלמוביל"}],
 "status": "draft",
 "notes": "נלקח מספר הנהג העברי של כלמוביל. בקובץ ה-PDF שבאתר מופיע רק העמוד שכותרתו 'לוח תחזוקה רגילה (המשך)'; שורות כמו מסנן אוויר, רצועת עזר, צינור אדי דלק ונוזל גיר כפול מצמד לא נמצאו בעותק, ולכן הן חסרות כאן (טיוטה עד שיימצא העמוד החסר). מצתים ב-75,000 וב-150,000, מסנן דלק כל 60,000, נוזל בלמים כל 45,000 (36 חודשים), מסנן מזגן כל 30,000."})
