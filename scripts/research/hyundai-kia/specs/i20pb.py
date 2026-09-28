import sys; sys.path.insert(0,'.')
from gen import build, HY
A8='IIIIIIII'; Q='.I.I.I.I'; H='...I...I'
build(dict(HY, id="hyundai-i20-2009-2014-1.25-1.4", model="i20", model_he="i20", generation="PB",
  years=[2009,2014], engines=["1.4 MPI (Gamma, G4FA)","1.25 MPI (Kappa, G4LA)"], fuel="petrol",
  interval={"km":15000,"months":12,"note":"לפי הספר הבינלאומי (מחוץ לאירופה): 15,000 ק\"מ או 12 חודשים, המוקדם מביניהם"},
  cycle_km=120000,
  sources=[{"url":"https://www.manualpdf.co.il/hyundai/i20-2011/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=319","kind":"manufacturer","note":"ספר בעלים באנגלית של i20 (PB) 2011 באתר מראה, עמודים 319-322 (7-15 עד 7-18): 'Normal maintenance schedule - gasoline engine (except Europe)'"}],
  status="draft",
  notes="לא נמצא ספר רכב עברי של i20 הדור הראשון (PB). הקובץ מבוסס על ספר בעלים בינלאומי באנגלית, טבלת 'מחוץ לאירופה' בעמודות של 15,000 ק\"מ. בשורת צינור האדים ומכסה המילוי שני הסימנים דבוקים לכותרת במראה ולכן הונח שהם ב-60,000 וב-120,000 (כמו בטבלת i30 מאותה תקופה). בסין ובהודו הספר מחליף מסנן אוויר בכל טיפול. מצתים כל 40,000 ק\"מ. מרווח שסתומים (1.4) כל 95,000 ק\"מ או 48 חודשים. שמן גיר ידני: בדיקה כל 60,000 ק\"מ או 48 חודשים. נוזל קירור: החלפה ראשונה ב-48,000 ק\"מ או 24 חודשים ואחר כך כל 40,000 ק\"מ או 24 חודשים."),
 [("drive_belt",A8),("engine_oil","RRRRRRRR"),("oil_filter","RRRRRRRR"),("air_filter","IIRIIRII"),
  ("evap_system",H,"מיקום משוחזר, ראה notes"),("vacuum_hose",Q),("fuel_filter",".I.R.I.R"),("fuel_lines",H),
  ("battery_12v",A8),("electrical_system",Q),("brake_lines",A8),("pedals",Q),("parking_brake",Q),("brake_fluid",A8),
  ("brake_pads",A8),("brake_discs",A8),("brake_drums",Q),("steering",A8),("cv_boots",A8),("tires",A8),("suspension",A8),
  ("body_underside",A8,"הידוק ברגים ואומים בשלדה ובמרכב"),("ac_refrigerant",A8),("ac_system",A8),("cabin_filter","RRRRRRRR"),
  ("transmission_oil",A8)],
 long_interval=[{"item":"spark_plugs","action":"replace","every_km":40000},
  {"item":"valve_clearance","action":"inspect","every_km":95000,"every_months":48,"note":"מנוע 1.4"},
  {"item":"manual_gearbox_oil","action":"inspect","every_km":60000,"every_months":48},
  {"item":"coolant","action":"replace","first_km":48000,"first_months":24,"then_every_km":40000,"then_every_months":24}])
