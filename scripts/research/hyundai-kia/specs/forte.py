import sys; sys.path.insert(0,'.')
from gen import build, KIA
A8='IIIIIIII'; Q='.I.I.I.I'; H='...I...I'
build(dict(KIA, id="kia-forte-2014-2018-1.6", model="Forte", model_he="פורטה", generation="YD (Cerato)",
  years=[2014,2018], engines=["1.6 MPI (Gamma, G4FG)"], fuel="petrol",
  interval={"km":15000,"months":12,"note":"לפי הספר הבינלאומי: מנוע Gamma 1.6 MPI כל 15,000 ק\"מ או 12 חודשים (ב'מזרח התיכון' כהגדרתו בספר, כלומר צפון אפריקה ואיראן, כל 10,000)"},
  cycle_km=120000,
  sources=[{"url":"https://www.manualslib.com/manual/1996633/Kia-Cerato.html?page=534","kind":"manufacturer","note":"ספר בעלים בינלאומי באנגלית של Kia Cerato (YD), עמודים 532-538 (7-10 עד 7-16): טבלת 'Normal maintenance schedule' עם עמודות לפי שוק; נלקחו ערכי 'מחוץ לאירופה'"}],
  status="draft",
  notes="לא נמצא ספר רכב עברי של קיה פורטה בספריית טלקאר. הקובץ מבוסס על ספר הבעלים הבינלאומי של Cerato YD (שם הדגם מחוץ לישראל), עמודות 15,000 ק\"מ, ערכי 'מחוץ לאירופה'. באירופה לפי אותו ספר: מסנן מזגן מוחלף כל 30,000 ורצועת הינע נבדקת לראשונה ב-90,000. מצתים (בנזין נטול עופרת) מוחלפים כל 60,000. מרווח שסתומים נבדק ב-90,000. תוסף דלק כל 10,000 ק\"מ או 6 חודשים מחוץ לאירופה (אין פריט ברשימה). גיר אוטומטי: ללא בדיקה וללא טיפול בתנאים רגילים. נוזל בלמים נבדק בכל טיפול ואינו מוחלף בטבלה."),
 [("engine_oil","RRRRRRRR"),("oil_filter","RRRRRRRR"),("drive_belt",Q),("valve_clearance",".....I.."),("vacuum_hose",A8),
  ("spark_plugs",H),("manual_gearbox_oil",H),("dct_oil",Q,"אם קיים"),("cv_boots",Q),("fuel_lines",H),
  ("fuel_tank_air_filter",".I.R.I.R"),("evap_system",H),("air_filter","IIRIIRII"),("exhaust",Q),
  ("ac_system",A8),("ac_refrigerant",A8),("cabin_filter","RRRRRRRR"),("brake_pads",A8),("brake_discs",A8),
  ("brake_lines",A8),("brake_fluid",A8),("parking_brake",Q),("steering",A8),("suspension",A8),("tires",A8),("battery_12v",A8)],
 long_interval=[{"item":"coolant","action":"replace","first_km":210000,"first_months":120,"then_every_km":30000,"then_every_months":24},
  {"item":"cooling_system","action":"inspect","first_km":60000,"first_months":48,"then_every_km":30000,"then_every_months":24}])
