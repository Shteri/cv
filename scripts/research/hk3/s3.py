from build import *
KIA={'make':'Kia','make_he':'קיה','importer':'טלקאר'}
A='IIIIIIII'; E='-I-I-I-I'; R8='RRRRRRRR'
SOUL_SRC={'url':'https://www.manualpdf.co.il/kia/soul-2009/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=269','kind':'manufacturer','note':"ספר בעלים קיה סול AM 2009 (אנגלית), פרק 7 עמ' 21-24 'Normal maintenance schedule - gasoline engine (except Australia & New Zealand)', עמודות 'Except Europe' (עמודי צפייה 269-272)"}
soul_rows=[('engine_oil',R8),('oil_filter',R8),('drive_belt',A),('air_filter','IIRIIRII'),('evap_system','---I---I','צינור אדים ומכסה פתח הדלק; בעמוד המקוון מופיעים שני סימונים שמיקומם לא ברור, שובצו ב-60,000 וב-120,000'),
 ('vacuum_hose',A,'צינורות ואקום, אוורור בית הארכובה וצינורות EGR/מצערת'),('fuel_filter','-I-R-I-R'),('fuel_lines','---I---I','שני סימונים בטבלה; שובצו ב-60,000 וב-120,000'),
 ('fuel_tank_air_filter','-I-R-I-R','אם קיים'),('battery_12v',A),('electrical_system',E),('brake_lines',A),('pedals',E),('parking_brake',E),('brake_fluid',A),
 ('brake_pads',A),('brake_discs',A),('brake_drums',E,'אם קיימים'),('steering',A),('cv_boots',E),('tires',A),('suspension',A,'מפרקים כדוריים קדמיים'),
 ('body_underside',A,'ברגים ואומים בשלדה ובמרכב'),('ac_refrigerant',A),('ac_system',A),('cabin_filter',R8),('manual_gearbox_oil',A,'אם קיים'),('transmission_oil',A,'אם קיים')]
soul_long=[{'item':'spark_plugs','action':'replace','every_km':40000},
  {'item':'valve_clearance','action':'inspect','every_km':96000,'every_months':48},
  {'item':'coolant','action':'replace','first_km':48000,'first_months':24,'then_every_km':40000,'then_every_months':24}]
NOTE='לפי הספר הבינלאומי (מחוץ לאירופה, אוסטרליה וניו זילנד): כל 15,000 ק"מ או 12 חודשים'
write({**KIA,'id':'kia-soul-2009-2011-1.6','model':'Soul','model_he':'סול','generation':'AM','years':[2009,2011],
 'engines':['1.6 MPI (Gamma, G4FC)'],'fuel':'petrol','interval':{'km':15000,'months':12,'note':NOTE},'cycle_km':120000,
 'long_interval':soul_long,'sources':[SOUL_SRC],'status':'draft',
 'notes':'הספר הישראלי של סול הדור הראשון לא נמצא; נלקחו עמודות "מחוץ לאירופה" מהטבלה הבינלאומית (שאינה לאוסטרליה וניו זילנד). מנוע 1.6 Gamma עם שרשרת תזמון; רצועת התזמון בטבלה שייכת למנוע 2.0 בלבד. נוזל הבלמים נבדק בכל טיפול ללא החלפה קבועה. נוזל קירור: החלפה ראשונה ב-48,000 ק"מ או 24 חודשים ואחר כך כל 40,000. דגמי 1.6 GDI (מ-2012) אינם בקובץ.'},
 grid(15000,soul_rows))

write({**KIA,'id':'kia-forte-2009-2013-1.6','model':'Forte','model_he':'פורטה','generation':'TD','years':[2009,2013],
 'engines':['1.6 MPI (Gamma, G4FC)'],'fuel':'petrol','interval':{'km':15000,'months':12,'note':NOTE+'. הטבלה לקוחה מספר קיה סול AM עם אותו מנוע'},'cycle_km':120000,
 'long_interval':soul_long,'sources':[SOUL_SRC,
  {'url':'https://www.manualpdf.co.il/kia/forte-2010/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=258','kind':'manufacturer','note':"ספר פורטה TD 2010 (אנגלית, G040100ATD-EC) עמ' 7-6: טבלה בעמודות של 8,000 ק\"מ / 4 חודשים לשוק אחר; לא שימשה, להשוואה בלבד"}],
 'status':'draft',
 'notes':'לא נמצא ספר ישראלי ולא ספר בינלאומי עם טבלת "מחוץ לאירופה" לפורטה TD: ספר 2010 שנמצא הוא לשוק עם טיפול כל 8,000 ק"מ, וספר 2011 בערבית (מפרץ). לכן הטבלה נלקחה מספר קיה סול AM 2009 מאותה תקופה ועם אותו מנוע Gamma 1.6 MPI (G4FC), עמודות "מחוץ לאירופה". זה מקור חלופי (דגם אחות לפי מנוע), יש לאמת מול היבואן. שרשרת תזמון, ללא החלפה מתוכננת. נוזל הבלמים נבדק בכל טיפול; מסנן הדלק ומסנן האוויר של מיכל הדלק מוחלפים כל 60,000.'},
 grid(15000,soul_rows))

# Ceed ED (European book)
rows=[('engine_oil',R8),('oil_filter',R8),('drive_belt',A),('air_filter','IIRIIRII'),('spark_plugs','--R--R--','מנועי 1.4/1.6; במנוע 2.0 כל 30,000'),
 ('evap_system',E,'צינור אדים ומכסה פתח הדלק'),('fuel_tank_air_filter','---I---I'),('vacuum_hose',A,'צינורות ואקום, אוורור בית הארכובה וצינורות EGR/מצערת'),
 ('fuel_filter','---I---I'),('fuel_lines',A),('battery_12v',A),('electrical_system',E),('brake_lines',A),('pedals',E),('parking_brake',E),
 ('brake_fluid','IRIRIRIR'),('brake_pads',A),('brake_discs',A),('steering',A),('cv_boots',A),('tires',A),('suspension',A,'מפרקים כדוריים קדמיים'),
 ('body_underside',A,'ברגים ואומים בשלדה ובמרכב'),('ac_refrigerant',A),('ac_system',A),('cabin_filter',R8),('manual_gearbox_oil',A,'אם קיים'),('transmission_oil','IIIIIRII','אם קיים')]
write({**KIA,'id':'kia-ceed-2007-2011-1.4-1.6','model':"Cee'd",'model_he':"סיד",'generation':'ED','years':[2007,2011],
 'engines':['1.4 (Gamma, G4FA)','1.6 (Gamma, G4FC)'],'fuel':'petrol','interval':{'km':15000,'months':12,'note':'לפי הספר האירופי: כל 15,000 ק"מ או 12 חודשים'},'cycle_km':120000,
 'long_interval':[{'item':'valve_clearance','action':'inspect','every_km':90000,'every_months':48},
  {'item':'coolant','action':'replace','first_km':90000,'first_months':60,'then_every_km':45000,'then_every_months':24},
  {'item':'timing_belt','action':'replace','every_km':135000,'every_months':72,'note':'מנוע 2.0 בלבד (בדיקה כל 90,000 ק"מ או 48 חודשים); במנועי 1.4/1.6 שרשרת'}],
 'sources':[{'url':'https://www.manualpdf.co.il/kia/ceed-2008/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=286','kind':'manufacturer','note':"ספר בעלים קיה סיד ED 2008 (אנגלית, אירופה), פרק 7 עמ' 4-7 'Normal maintenance schedule - gasoline engine' (עמודי צפייה 286-289)"}],
 'status':'draft',
 'notes':'הספר הישראלי של סיד ED לא נמצא. הרכב יוצר באירופה, והספר שנמצא הוא הספר האירופי עם טבלה אחת למנועי הבנזין. נוזל בלמים מוחלף כל 30,000; מצתים (1.4/1.6) כל 45,000; נוזל קירור ראשון ב-90,000 ק"מ או 60 חודשים ואחר כך כל 45,000. שמן גיר אוטומטי מוחלף ב-90,000. מסנן דלק נבדק כל 60,000 ומוחלף רק בבעיית התנעה או אספקת דלק.'},
 grid(15000,rows))
