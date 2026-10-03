import sys; sys.path.insert(0,'.')
from gen import *
IMP='יפנאוטו (סובארו, קבוצת סמלת)'
URL='https://www.manualslib.com/manual/1585126/Subaru-Legacy-2005.html?page=105'
def ej(id_, model, model_he, gen, years, engines, two_only, extra_note):
    s=S(id_,'Subaru','סובארו',model,model_he,gen,years,engines,'petrol',IMP,15000,12,
        'לפי טבלת התחזוקה לאזור אירופה בספר השירות של סובארו: 15,000 ק"מ או 12 חודשים, המוקדם; בתנאי שימוש קשים חלק מהבדיקות וההחלפות כל 15,000 ק"מ (טבלה 2)',120000)
    for it in ('engine_oil','oil_filter'): s.pat(it,'RRRRRRRR',15000)
    s.pat('spark_plugs','-R-R-R-R',15000,'מנוע 2.0: החלפה כל 30,000 ק"מ' if two_only else 'מנוע 2.0: כל 30,000 ק"מ; מנוע 2.5: ב-105,000 ק"מ')
    s.pat('drive_belt','IIIIIIII',15000)
    s.add(105000,'timing_belt','replace','החלפת רצועת תזמון ב-105,000 ק"מ (או 84 חודשים)')
    s.pat('fuel_lines','-I-I-I-I',15000)
    s.pat('air_filter','IRIRIRIR',15000,'בתנאי אבק קיצוניים להחליף לעתים קרובות יותר')
    s.pat('cooling_system','-I-I-I-I',15000)
    s.pat('coolant','-R-R-R-R',15000)
    s.pat('clutch','-I-I-I-I',15000,'מערכת מצמד (גיר ידני)')
    s.pat('manual_gearbox_oil','-I-R-I-R',15000)
    s.pat('transmission_oil','-I-R-I-R',15000,'גיר אוטומטי (ATF)')
    s.pat('differential_oil','-I-R-I-R',15000,'דיפרנציאל קדמי ואחורי')
    s.pat('brake_lines','-I-I-I-I',15000)
    s.pat('brake_fluid','-R-R-R-R',15000)
    s.pat('brake_pads','IIIIIIII',15000,'רפידות ודיסקים')
    s.pat('brake_discs','IIIIIIII',15000)
    s.pat('parking_brake','-I-I-I-I',15000)
    s.pat('suspension','-I-I-I-I',15000)
    s.add(120000,'suspension','inspect','בדיקת מיסבי גלגלים מומלצת ב-120,000 ק"מ')
    s.pat('cv_boots','IIIIIIII',15000)
    s.pat('steering','-I-I-I-I',15000)
    s.li('cabin_filter','replace',every_km=12000,every_months=12,note='מסנן מיזוג (אם מותקן): כל 12,000 ק"מ או 12 חודשים')
    if not two_only:
        s.li('spark_plugs','replace',every_km=105000,note='מנוע 2.5 בלבד (בספר: "Others"); מנוע 2.0 כל 30,000 ק"מ')
    s.li('timing_belt','replace',every_km=105000,every_months=84)
    s.src(URL,'manufacturer','Subaru Legacy 2005 (BL/BP) service manual, PM-3 "Maintenance Schedule 1 - Europe area" (manualslib p.105) ו-PM-5 "Maintenance Schedule 2" לתנאים קשים (p.107)')
    s.src('https://samelet.com/ebooks/','importer','תיקיית ספרי הרכב של סמלת (יבואנית סובארו): יש בה רק ספרים לדורות עם מנועי FB/FA, אין ספר לדגמי EJ')
    notes=('לא נמצא ספר עברי לדגם זה (בספריית סמלת יש רק ספרים לדורות עם מנועי FB). הלוח לקוח מטבלת התחזוקה לאזור אירופה בספר השירות של סובארו לגאסי 2005, '
           'שבו מופיע אותו מנוע בוקסר EJ ברצועת תזמון. מחזור הטבלה 120,000 ק"מ או 96 חודשים וחוזר על עצמו. '
           'בטבלה נוזל הקירור ונוזל הבלמים מוחלפים כל 30,000 ק"מ (24 חודשים) ורצועת התזמון ב-105,000 ק"מ. '
           'בתנאי שימוש קשים (נסיעות קצרות, דרכים משובשות, גרירה) הספר מורה על החלפת שמנים ונוזל בלמים ובדיקת בלמים, מתלים והיגוי כל 15,000 ק"מ או שנה. '+extra_note)
    return s.write('draft',notes)
ej('subaru-b4-2003-2013-2.0-2.5','B4 (Legacy)','B4 (לגאסי)','BL/BM (EJ)',(2003,2013),['2.0 (EJ20)','2.5 (EJ25)'],False,
   'הטבלה נכתבה לדור BL/BP; לדור BM (2010 ואילך) עם מנוע EJ20 זו הערכה, ויש לאמת מול המוסך.')
rule('Subaru',['B4'],(2000,2013),'subaru-b4-2003-2013-2.0-2.5',engine_codes=['EJ 20','EJ20','EJ 25','EJ25'])
ej('subaru-forester-2003-2012-2.0','Forester','פורסטר','SG/SH (EJ20)',(2003,2012),['2.0 (EJ20)'],True,
   'הטבלה לקוחה מספר השירות של הלגאסי (דגם אחות עם אותו מנוע EJ20 ואותה מערכת הנעה כפולה), ולכן הלוח הוא טיוטה לפורסטר.')
rule('Subaru',['FORESTER'],(2001,2012),'subaru-forester-2003-2012-2.0',engine_codes=['EJ 20','EJ20'])
ej('subaru-impreza-2005-2011-2.0','Impreza','אימפרזה','GD/GH (EJ20)',(2005,2011),['2.0 (EJ20)'],True,
   'הטבלה לקוחה מספר השירות של הלגאסי (דגם אחות עם אותו מנוע EJ20), ולכן הלוח הוא טיוטה לאימפרזה 2.0.')
rule('Subaru',['IMPREZA','IMPREZA B3'],(2005,2012),'subaru-impreza-2005-2011-2.0',engine_codes=['EJ 20','EJ20'])
rule('Subaru',['FORESTER'],(2011,2012),'subaru-forester-2013-2018-2.0-2.5',engine_codes=['FB 20','FB20'])
RULES[:]=RULES[:-1]
save_rules('rules_subaru.json')
