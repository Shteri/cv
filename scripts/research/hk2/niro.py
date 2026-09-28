import json
from build import build, OUT
# 1) Niro DE PHEV 2019-2022: same Israeli book table as the HEV (Niro-2019.pdf p549-550)
src=json.load(open('/home/user/cv/data/schedules/kia-niro-2016-2022-1.6-hybrid.json'))
d=dict(src)
d.update({'id':'kia-niro-2019-2022-1.6-plug-in-hybrid','model':'Niro PHEV','model_he':'נירו פלאג-אין','generation':'DE PHEV',
 'years':[2019,2022],'engines':['1.6 GDI plug-in hybrid (Kappa, G4LE)'],'fuel':'plug-in-hybrid',
 'sources':[{'url':'https://cdnmedia.kia-israel.co.il/www/cars-book/Niro-2019.pdf','kind':'importer','note':"ספר הרכב העברי של קיה ישראל לנירו 2019 ואילך (משותף להיברידי ולפלאג-אין), פרק 7 עמ' 13-14 (עמודי PDF 549-550), טבלה אחת לרכב עם מנוע בנזין"}],
 'status':'reviewed',
 'notes':"ספר נירו 2019 של היבואן מכסה גם את גרסת הפלאג-אין ומציג טבלת תחזוקה אחת לכל הגרסאות עם מנוע בנזין, לכן לוח הזמנים זהה לנירו ההיברידית. עמודות של 15,000 ק\"מ או 12 חודשים. נוזל בלמים ונוזל מפעיל מצמד מוחלפים כל 30,000; מסנן אוויר מוחלף ב-45,000 וב-90,000; מסנן מזגן כל 30,000; רצועת HSG נבדקת בכל טיפול ומוחלפת ב-105,000. תוסף דלק כל 15,000 ק\"מ אם הדלק ללא תוספים. בתנאי הפעלה קשים שמן כל 7,500 ק\"מ."})
d.pop('services'); 
json.dump(dict(d,services=src['services']),open(OUT+d['id']+'.json','w'),ensure_ascii=False,indent=2)
print('wrote',d['id'])

# 2) Niro SG2 HEV 2024-2026 from NIRO_PHEV_General_Heb book 'except Europe' table p456-458
BOOK='https://cdnmedia.kia-israel.co.il/www/cars-book/NIRO_PHEV_General_Heb_01_%D7%A4%D7%9C%D7%90%D7%92%D7%90%D7%99%D7%9F.pdf'
meta={'make':'Kia','make_he':'קיה','model':'Niro HEV','model_he':'נירו היברידי','generation':'SG2','id':'kia-niro-2024-2026-1.6-hybrid',
 'years':[2024,2026],'engines':['1.6 GDI hybrid (Smartstream G1.6, G4LL)'],'fuel':'hybrid','importer':'טלקאר',
 'interval':{'km':15000,'months':12,'note':'לפי טבלת "למעט אירופה" בספר היבואן: 15,000 ק"מ או 12 חודשים (המוקדם). לאזור המזרח התיכון הספר מציין שמן ומסנן כל 10,000 ק"מ או 12 חודשים; בתנאי הפעלה קשים כל 7,500 ק"מ או 6 חודשים'},
 'cycle_km':120000,
 'long_interval':[
  {'item':'coolant','action':'replace','first_km':180000,'first_months':120,'then_every_km':30000,'then_every_months':24,'note':'נוזל קירור מנוע'},
  {'item':'coolant','action':'replace','first_km':180000,'first_months':120,'then_every_km':30000,'then_every_months':24,'note':'נוזל קירור ממיר המתח (HEV)'},
  {'item':'hsg_belt','action':'inspect','every_km':15000,'every_months':12,'note':'במזרח התיכון לפי הספר: בדיקה כל 10,000 ק"מ'},
  {'item':'hsg_belt','action':'replace','every_km':105000,'every_months':48,'note':'במזרח התיכון לפי הספר: החלפה כל 100,000 ק"מ או 48 חודשים'},
  {'item':'spark_plugs','action':'replace','every_km':150000},
  {'item':'clutch_actuator_fluid','action':'replace','every_km':40000,'every_months':24}],
 'specs':{'fuel':'בנזין נטול עופרת RON 91 ומעלה (מחוץ לאירופה)','brake_fluid':'DOT 4','battery':'מצבר עזר 12V וסוללת מתח גבוה','_note':'לפי ספר הרכב של היבואן'},
 'sources':[{'url':BOOK,'kind':'importer','note':"ספר הרכב העברי של קיה ישראל 'נירו הייבריד/פלאג-אין' (ספר משותף ל-HEV ול-PHEV), טבלת 'למעט באירופה - תוכנית תחזוקה רגילה', עמודי PDF 456-458"}],
 'status':'reviewed',
 'notes':"הספר העברי של נירו החדשה משותף לגרסה ההיברידית ולפלאג-אין; השורות הייחודיות ל-HEV נלקחו ממנו. נבחרה טבלת 'למעט אירופה' בעמודות 15,000 ק\"מ. מסנן אוויר מוחלף ב-45,000 וב-90,000 (במזרח התיכון, הודו וסין: בכל טיפול). מסנן מזגן בכל טיפול. נוזל בלמים מוחלף ב-45,000 וב-90,000. נוזל מפעיל מצמד המנוע כל 40,000 ק\"מ או 24 חודשים. גיר DCT ללא טיפול (בתנאים קשים החלפה כל 120,000). תוסף דלק כל 15,000 ק\"מ (במזרח התיכון כל 10,000). מסנן דלק רק לסין וברזיל."}
rows=[('engine_oil','RRRRRRRR'),('oil_filter','RRRRRRRR'),
 ('clutch_actuator_fluid','IIIIIIII','בדיקת צינור וקו מפעיל המצמד'),
 ('cv_boots','-I-I-I-I'),('fuel_lines','---I---I'),('fuel_tank_air_filter','-I-R-I-R'),('evap_system','---I---I'),
 ('air_filter','IIRIIRII'),('exhaust','-I-I-I-I'),('cooling_system','IIIIIIII'),('ac_refrigerant','IIIIIIII'),('ac_system','IIIIIIII'),
 ('cabin_filter','RRRRRRRR'),('brake_pads','-I-I-I-I'),('brake_discs','-I-I-I-I'),('brake_lines','-I-I-I-I'),('brake_fluid','IIRIIRII'),
 ('steering','IIIIIIII'),('suspension','IIIIIIII'),('tires','IIIIIIII'),('battery_12v','IIIIIIII'),('hsg_belt','IIIIIIII')]
build(meta,15000,rows)
