from build import *
HY={'make':'Hyundai','make_he':'יונדאי','importer':'כלמוביל'}
A='IIIIIIII'; E='-I-I-I-I'; R8='RRRRRRRR'
rows=[('engine_oil',R8),('oil_filter',R8),('drive_belt','---IIIII','בדיקה ראשונה ב-80,000 ק"מ או 48 חודשים ואחר כך כל 20,000 או 12 חודשים'),
 ('air_filter','IRIRIRIR'),('evap_system',E,'צינור אדים ומכסה פתח הדלק'),('vacuum_hose',A,'משאבת ואקום וצינורותיה, צינור השמן של המשאבה וצינורות EGR/מצערת'),
 ('fuel_filter','IIRIIRII','מחסנית מסנן הסולר; המרווח תלוי באיכות הסולר (EN590)'),('fuel_lines',A),('battery_12v',A),('electrical_system',E),('brake_lines',A),
 ('pedals',E),('parking_brake',E),('brake_fluid','IRIRIRIR'),('brake_pads',A),('brake_discs',A),('power_steering_fluid',A,'נוזל וצינורות הגה כוח'),('steering',A),
 ('propshaft',E),('tires',A),('suspension',A,'מפרקים כדוריים קדמיים'),('body_underside',A,'ברגים ואומים בשלדה ובמרכב'),('ac_refrigerant',A),('ac_system',A),
 ('cabin_filter',R8),('differential_oil',E,'שמן הסרן האחורי')]
write({**HY,'id':'hyundai-h1-2008-2021-2.5-diesel','model':'H-1','model_he':'H-1','generation':'TQ','years':[2008,2021],
 'engines':['2.5 CRDi (A2, D4CB)'],'fuel':'diesel',
 'interval':{'km':20000,'months':12,'note':'לפי הטבלה האירופית לסולר A2.5: כל 20,000 ק"מ או 12 חודשים. בטבלה שמחוץ לאירופה באותו ספר: שמן ומסנן כל 10,000 ק"מ או 12 חודשים'},
 'cycle_km':160000,
 'long_interval':[{'item':'coolant','action':'replace','first_km':210000,'first_months':120,'then_every_km':30000,'then_every_months':24},
  {'item':'manual_gearbox_oil','action':'inspect','every_km':60000,'every_months':48,'note':'אם קיים'},
  {'item':'transmission_oil','action':'inspect','every_km':60000,'every_months':48,'note':'גיר אוטומטי, אם קיים'}],
 'sources':[{'url':'https://www.manualslib.com/manual/739089/Hyundai-H-1.html?page=268','kind':'manufacturer','note':"ספר בעלים יונדאי H-1 TQ (אנגלית), פרק 7 עמ' 14-17 'Normal maintenance schedule (for Europe A2.5 diesel engine)' ולוח תנאים קשים (עמודי manualslib 268-271); טבלת 'except for Europe' בעמ' 9-13"}],
 'status':'draft',
 'notes':'הספר הישראלי של H-1 לא נמצא. נלקחה הטבלה האירופית למנוע הדיזל A2.5 (D4CB), בעמודות של 20,000 ק"מ עד 160,000. לפי הטבלה שמחוץ לאירופה בספר, השמן מוחלף כל 10,000 ק"מ ורצועת ההנעה נבדקת מ-80,000 כל 20,000. מחסנית מסנן הסולר מוחלפת כל 60,000; נוזל בלמים כל 40,000; מסנן אוויר כל 40,000. בתנאי הפעלה קשים (אירופה): שמן כל 10,000 ק"מ או 6 חודשים, שמן גיר ידני כל 120,000, שמן סרן אחורי כל 80,000.'},
 grid(20000,rows))
