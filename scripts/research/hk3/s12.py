from build import *
HY={'make':'Hyundai','make_he':'יונדאי','importer':'כלמוביל'}
A='IIIIIIII'; E='-I-I-I-I'; R8='RRRRRRRR'
rows=[('drive_belt','--IIIIII','בדיקה ראשונה ב-90,000 ק"מ או 48 חודשים ואחר כך כל 30,000'),('air_filter','IRIRIRIR'),('fuel_lines',A),
 ('fuel_filter','IRIRIRIR','מחסנית מסנן הסולר; המרווח תלוי באיכות הסולר (EN590)'),('evap_system',E,'מכסה פתח הסולר'),('cooling_system','-IIIIIII'),
 ('battery_12v',A),('electrical_system',A),('brake_lines',A),('parking_brake',A),('brake_fluid',R8),('brake_pads',A),('brake_discs',A),('steering',A),
 ('cv_boots',A),('tires',A),('ac_refrigerant',A),('ac_system',A),('cabin_filter',R8),('manual_gearbox_oil',E,'אם קיים'),('exhaust',A),
 ('differential_oil',E,'4WD'),('transfer_case_oil',E,'4WD'),('propshaft',A,'אם קיים')]
oil={km:lst(('engine_oil','R'),('oil_filter','R')) for km in range(15000,240001,15000)}
write({**HY,'id':'hyundai-staria-2022-2024-2.2-diesel','model':'Staria','model_he':'סטאריה','generation':'US4','years':[2022,2024],
 'engines':['2.2 CRDi (Smartstream D2.2, D4HB)'],'fuel':'diesel',
 'interval':{'km':15000,'months':12,'note':'לפי הטבלה האירופית: שמן ומסנן כל 30,000 ק"מ או 24 חודשים, ובתנאי הפעלה קשים כל 15,000 ק"מ או 12 חודשים; כאן לפי 15,000'},
 'cycle_km':240000,
 'long_interval':[{'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24},
  {'item':'timing_belt','action':'replace','every_km':240000,'note':'בדיקת רצועת תזמון כל 120,000; החלפת ערכת התזמון (רצועה, משאבת מים, מותחן וגלגלת) כל 240,000'},
  {'item':'suspension','action':'inspect','every_km':10000,'note':'מפרקים כדוריים של המתלים: בדיקה כל 10,000 ק"מ'},
  {'item':'transmission_oil','action':'inspect','every_km':90000,'note':'לפי הספר אין צורך בבדיקה או טיפול בגיר האוטומטי בתנאים רגילים'},
  {'item':'ecall_battery','action':'replace','every_months':36,'note':'אם קיימת מערכת eCall'}],
 'sources':[{'url':'https://www.manualslib.com/manual/2356247/Hyundai-Staria-Us4-2021.html?page=678','kind':'manufacturer','note':"ספר בעלים יונדאי סטאריה US4 2021 (אנגלית), פרק 9 עמ' 18-22 'Normal maintenance schedule (for Europe)' - פריטי דיזל ופריטים כלליים, ותנאים קשים (עמודי manualslib 678-682)"}],
 'status':'draft',
 'notes':'הספר הישראלי של סטאריה לא נמצא. נלקחה הטבלה האירופית (כמו בספרי כלמוביל לדגמים אחרים, שבנויים לפי הטבלה האירופית בעמודות של 30,000). הקובץ בנוי על רשת 15,000 עם שמן ומסנן בכל טיפול (לפי לוח התנאים הקשים), ושאר הפריטים בטיפולים הזוגיים. מסנן אוויר ומחסנית מסנן הסולר מוחלפים כל 60,000; נוזל בלמים ומסנן מזגן כל 30,000. אם אין שמן 0W-30 הספר מורה להחליף כל 20,000 ק"מ או 12 חודשים.'},
 merge(oil,grid(30000,rows)))
