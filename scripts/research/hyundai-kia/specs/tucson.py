import sys; sys.path.insert(0,'..'); sys.path.insert(0,'.')
from gen import build, HY
A8='IIIIIIII'
cool=[{"item":"cooling_system","action":"inspect","first_km":60000,"first_months":48,"then_every_km":30000,"then_every_months":24}]
# ---- Tucson TL 2016-2020 (Israeli Hebrew book via manualpdf.co.il mirror)
build(dict(HY, id="hyundai-tucson-2015-2020-1.6-2.0", model="Tucson", model_he="טוסון", generation="TL",
  years=[2015,2020], engines=["2.0 MPI (Nu, G4NA)","1.6 GDI (Gamma, G4FD)","1.6 T-GDI (Gamma, G4FJ)"], fuel="petrol",
  interval={"km":15000,"months":12,"note":"לפי ספר הרכב בעברית: כל 15,000 ק\"מ או 12 חודשים. בתנאי נהיגה קשים שמן ומסנן כל 7,500 ק\"מ או 6 חודשים במנועי 1.6 T-GDI ו-2.0 MPI"},
  cycle_km=120000,
  sources=[{"url":"https://www.manualpdf.co.il/hyundai/tucson-2016/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=544","kind":"other","note":"עותק מקוון של ספר הרכב העברי של טוסון 2016 (הוצאת כלמוביל), עמודים 544-549 במראה (7-11 עד 7-16 בספר): תוכנית אחזקה רגילה ותנאים קשים"},
           {"url":"https://www.hyundaimotors.co.il/maintenance/","kind":"importer","note":"ספריית ספרי הרכב של כלמוביל; ספר טוסון 2016-2020 אינו מופיע בה כקובץ"}],
  status="reviewed",
  notes="הטבלה נלקחה מהספר העברי של טוסון TL (אתר מראה שמציג את שכבת הטקסט של ה-PDF). מיקום העמודות שוחזר מקואורדינטות הטקסט ומקווי הטבלה. בשתי שורות (מסנן אוויר של מיכל הדלק וצנרת דלק) הסימנים דבוקים לכותרת השורה ולכן רק מספרם ידוע (4 מתוך 8): הונח שהם בכל 30,000. נוזל בלמים מסומן בספר להחלפה בכל עמודה (כל 15,000). שורות הדיזל (D4HA) לא נכללו כי בישראל כמעט אין טוסון TL דיזל. רצועת הינע: בדיקה ראשונה ב-90,000 ק\"מ או 72 חודשים ואחר כך כל 30,000. נוזל גיר אוטומטי: בתנאים רגילים אין צורך בבדיקה; בתנאים קשים (כולל חום מעל 32 מעלות בפקקים) החלפה כל 100,000. גיר ידני/DCT, תיבת העברה ודיפרנציאל: להחליף אם שקעו במים. בתנאים קשים: שמן גיר ידני/DCT ודיפרנציאל כל 120,000 ק\"מ."),
 [("engine_oil","RRRRRRRR"),("oil_filter","RRRRRRRR"),("air_filter","IRIRIRIR"),
  ("evap_system",".I.I.I.I"),("fuel_tank_air_filter",".I.I.I.I","מיקום העמודות משוחזר, ראה notes"),("fuel_filter",A8),
  ("fuel_lines",".I.I.I.I","מיקום העמודות משוחזר, ראה notes"),("battery_12v",A8),("brake_lines",A8),("parking_brake",A8),
  ("brake_fluid","RRRRRRRR"),("brake_pads",A8),("brake_discs",A8),("steering",A8),("cv_boots",A8),("tires",A8),
  ("suspension",A8),("ac_refrigerant",A8),("ac_system",A8),("cabin_filter","RRRRRRRR"),
  ("manual_gearbox_oil",".I.I.I.I"),("dct_oil",".I.I.I.I"),("transfer_case_oil",".I.I.I.I","4WD בלבד"),
  ("differential_oil",".I.I.I.I","4WD בלבד, דיפרנציאל אחורי"),("propshaft",A8,"4WD בלבד"),
  ("valve_clearance","..I..I..","מנוע 1.6 בלבד"),("exhaust",A8)],
 long_interval=[{"item":"drive_belt","action":"inspect","first_km":90000,"first_months":72,"then_every_km":30000,"then_every_months":24},
  {"item":"spark_plugs","action":"replace","every_km":150000,"note":"מנועי 1.6; במנוע 2.0 כל 165,000 ק\"מ"},
  {"item":"coolant","action":"replace","first_km":210000,"first_months":120,"then_every_km":30000,"then_every_months":24}]+cool+
  [{"item":"transmission_oil","action":"replace","every_km":100000,"note":"בתנאים רגילים ללא טיפול; בתנאי נהיגה קשים החלפה כל 100,000"}])

# ---- Tucson NX4 2021+ (Colmobil Hebrew book, 2021)
build(dict(HY, id="hyundai-tucson-2021-2026-1.6t-2.0", model="Tucson", model_he="טוסון", generation="NX4",
  years=[2021,2026], engines=["Smartstream G1.6 T-GDI (G4FP)","Smartstream G2.0 MPI (G4NL)"], fuel="petrol",
  interval={"km":15000,"months":12,"note":"לפי ספר הרכב של היבואן: 15,000 ק\"מ או 12 חודשים. בתנאי נהיגה קשים שמן ומסנן כל 5,000 ק\"מ (1.6 T-GDI) או 8,000 ק\"מ (2.0), או 6 חודשים"},
  cycle_km=120000,
  sources=[{"url":"https://prodmedia.colmobil.co.il/media/sites/2/2023/06/%D7%99%D7%95%D7%93%D7%90%D7%99-%D7%98%D7%95%D7%A1%D7%95%D7%9F-%D7%A1%D7%A4%D7%A8-%D7%A8%D7%9B%D7%91.pdf","kind":"importer","note":"ספר רכב טוסון (NX4, הפקה 2021) של כלמוביל, עמודי PDF 475-478 (9-8 עד 9-11)"}],
  status="reviewed",
  notes="טבלת עמודות של 15,000 ק\"מ / 12 חודשים. מסנן אוויר ומסנן מזגן מוחלפים בכל טיפול. מצתים: 1.6 T-GDI כל 75,000 ק\"מ או 60 חודשים, 2.0 כל 160,000 ק\"מ. במנוע 1.6 T-GDI הספר מוסיף תוסף דלק כל 10,000 ק\"מ או 6 חודשים (אין לו פריט ברשימה). צינור אדים/מכסה מילוי וצנרת דלק מסומנים לבדיקה רק ב-60,000. בדיקת מרווח שסתומים (רעש/רעידות) ב-90,000 במנוע 1.6 T-GDI. נוזל גיר DCT נבדק ב-60,000 ו-120,000; גיר אוטומטי כל 30,000; בתנאים קשים החלפת גיר אוטומטי כל 100,000 ו-DCT כל 120,000. סוללת eCall מוחלפת כל 3 שנים. הספר הוא מהדורת 2021; לשנים 2024-2026 (מתיחת פנים) לא נמצא ספר נפרד."),
 [("drive_belt",".I.I.I.I"),("engine_oil","RRRRRRRR"),("oil_filter","RRRRRRRR"),("intercooler_pipes",A8,"1.6 T-GDI"),
  ("air_filter","RRRRRRRR"),("evap_system","...I...."),("fuel_tank_air_filter",".I.R.I.R"),("fuel_filter",".I.R.I.R"),
  ("fuel_lines","...I...."),("electrical_system",".I.I.I.I"),("battery_12v",A8),("brake_lines",A8),("parking_brake",".I.I.I.I"),
  ("brake_fluid","IIRIIRII"),("brake_pads",A8),("brake_discs",A8),("steering",A8),("cv_boots",".I.I.I.I"),
  ("tires",A8),("suspension",A8),("ac_refrigerant",A8),("ac_system",A8),("cabin_filter","RRRRRRRR"),
  ("dct_oil","...I...I"),("transmission_oil",".I.I.I.I"),("valve_clearance",".....I..","1.6 T-GDI"),("exhaust",".I.I.I.I")],
 long_interval=[{"item":"spark_plugs","action":"replace","every_km":75000,"every_months":60,"note":"1.6 T-GDI; במנוע 2.0 כל 160,000 ק\"מ"}]+cool,
 time_based=[{"item":"ecall_battery","action":"replace","months":36,"note":"אם קיים"}])
