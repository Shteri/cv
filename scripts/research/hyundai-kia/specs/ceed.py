import sys; sys.path.insert(0,'.')
from gen import build, KIA
A8='IIIIIIII'; Q='.I.I.I.I'; H='...I...I'
build(dict(KIA, id="kia-ceed-2012-2018-1.6", model="Ceed", model_he="סיד", generation="JD",
  years=[2012,2018], engines=["1.6 GDI (Gamma, G4FD)","1.6 MPI (Gamma, G4FC)"], fuel="petrol",
  interval={"km":15000,"months":12,"note":"לפי הספר הבינלאומי (מחוץ לאירופה): מנועי Gamma MPI/GDI כל 15,000 ק\"מ או 12 חודשים; מנוע T-GDI כל 10,000 ק\"מ או 6 חודשים"},
  cycle_km=120000,
  sources=[{"url":"https://www.kceed.com/normal_maintenance_schedule_except_europe-640.html","kind":"other","note":"אתר מראה של ספר הבעלים הבינלאומי (אנגלית) של Kia Cee'd JD: טבלת 'Normal maintenance schedule - except Europe' (3 תמונות עמוד)"}],
  status="draft",
  notes="לא נמצא ספר רכב עברי של קיה סיד בספריית טלקאר. הקובץ מבוסס על ספר הבעלים הבינלאומי של Cee'd JD, טבלת 'מחוץ לאירופה' בעמודות 15,000 ק\"מ. במזרח התיכון (כהגדרת הספר) מסנן אוויר מוחלף בכל טיפול. מצתי ניקל (MPI) כל 60,000; מצתי אירידיום במנוע GDI כל 150,000 ק\"מ או 120 חודשים; T-GDI כל 75,000 ק\"מ או 60 חודשים. תוסף דלק כל 10,000 ק\"מ או 6 חודשים (אין פריט ברשימה). גיר אוטומטי ללא טיפול. נוזל בלמים נבדק בכל טיפול ואינו מוחלף בטבלה זו. שורות הדיזל לא נכללו."),
 [("air_filter","IIRIIRII"),("ac_refrigerant",A8),("ac_system",A8),("battery_12v",A8),("brake_lines",A8),("pedals",Q),
  ("brake_fluid",A8),("cabin_filter","RRRRRRRR"),("brake_pads",A8),("brake_discs",A8),("cv_boots",Q),("drive_belt",Q),
  ("exhaust",Q),("engine_oil","RRRRRRRR"),("oil_filter","RRRRRRRR"),("electrical_system",Q),("suspension",A8),
  ("fuel_filter",".I.R.I.R"),("fuel_tank_air_filter",".I.R.I.R"),("fuel_lines",H),("manual_gearbox_oil",H),
  ("parking_brake",Q),("spark_plugs",H,"מצתי ניקל (MPI)"),("steering",A8),("tires",A8),("valve_clearance",".....I.."),("evap_system",H)],
 long_interval=[{"item":"cooling_system","action":"inspect","first_km":60000,"first_months":48,"then_every_km":30000,"then_every_months":24},
  {"item":"coolant","action":"replace","first_km":210000,"first_months":120,"then_every_km":30000,"then_every_months":24}])
