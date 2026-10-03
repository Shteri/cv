import sys; sys.path.insert(0,'.')
from gen import *
API='https://books.union-motors.co.il/LexusApp/api/files/{}/download'
PAGE='https://www.lexus.co.il/owners/maintenance/owner-books'
IMP='יוניון מוטורס'
def ux(id_, model, model_he, years, engines, fuel, hybrid):
    s=S(id_,'Lexus','לקסוס',model,model_he,'MZA10/MZAH10',years,engines,fuel,IMP,15000,12,
        'לפי לוח האחזקה בספר הרכב העברי של UX200: טיפול כל 15,000 ק"מ או 12 חודשים, המוקדם; בתנאים מחמירים שמן ומסנן כל 7,500 ק"מ או 6 חודשים',150000)
    s.every('engine_oil','replace',15000); s.every('oil_filter','replace',15000)
    s.li('drive_belt','inspect',first_km=105000,then_every_km=15000,first_months=72,then_every_months=12)
    s.every('drive_belt','inspect',15000,'בדיקה ראשונה לאחר 105,000 ק"מ ומאז כל 15,000', start=105000)
    s.every('cooling_system','inspect',30000,'מערכת קירור וחימום; כולל בדיקת המצנן והמעבה')
    s.every('coolant','inspect',30000,'נוזל קירור מנוע (כולל אינטרקולר)')
    s.li('coolant','replace',first_km=160000,then_every_km=80000,note='החלפה ראשונה לאחר 160,000 ק"מ ומאז כל 80,000')
    s.every('battery_12v','inspect',15000); s.every('exhaust','inspect',15000)
    s.at('fuel_filter','replace',[75000,150000],'בלוח מסומנת החלפה ב-75,000 וב-150,000 (R:96 חודשים)')
    s.add(90000,'spark_plugs','replace','מצתי פלטינה/אירידיום'); s.li('spark_plugs','replace',every_km=90000)
    s.pat('air_filter','IIIRIIIRII',15000,'בתנאים מחמירים: בדיקה כל 7,500 ק"מ, החלפה כל 60,000')
    s.at('evap_system','clean',[75000,150000],'ניקוי מכלול מסנן הפחם')
    s.at('evap_system','inspect',[45000,90000,135000],'בדיקת מכלול מסנן הפחם')
    s.every('fuel_lines','inspect',30000,'צינורות דלק, חיבורים ומכסה מיכל הדלק')
    s.every('pedals','inspect',15000,'דוושת בלם')
    s.every('brake_pads','inspect',15000); s.every('brake_discs','inspect',15000)
    s.pat('brake_fluid','IRIRIRIRIR',15000,'בדיקה כל 12 חודשים, החלפה כל 24 חודשים')
    s.every('brake_lines','inspect',15000)
    s.every('steering','inspect',30000,'מסרק הגה, מוטות הגה וגלגל הגה; בתנאים מחמירים כל 7,500')
    s.every('cv_boots','inspect',30000,'בתנאים מחמירים כל 15,000')
    s.every('suspension','inspect',30000,'מחברים כדוריים, מגיני אבק, מתלים קדמיים ואחוריים; בתנאים מחמירים כל 15,000')
    if hybrid:
        s.every('transmission_oil','inspect',30000,'בדיקת נוזל תיבת ההינע (בלוח של UX200 הבדיקה כל 30,000)')
    else:
        s.every('transmission_oil','inspect',30000,'נוזל CVT; בתנאים מחמירים החלפה ב-60,000 וב-120,000')
    s.every('differential_oil','inspect',30000,'דיפרנציאל קדמי; בתנאים מחמירים החלפה ב-60,000 וב-120,000')
    s.every('tires','inspect',15000,'צמיגים ולחץ אוויר')
    s.every('lights','inspect',15000,'אורות, צופר, מגבים ומתזים')
    s.every('cabin_filter','replace',15000)
    s.every('body_underside','inspect',15000,'בדיקת חלודה; שטיחי רצפה בכל ביקור')
    s.li('vacuum_hose','inspect',every_km=200000,note='משאבת ואקום בלמים: בדיקה כל 200,000 ק"מ')
    return s

s=ux('lexus-ux200-2019-2021-2.0','UX 200','UX 200',(2019,2021),['2.0 (M20A-FKS)'],'petrol',False)
s.src(API.format(74),'importer','ספר רכב UX200 בעברית (יוניון מוטורס), סעיף 6-3 "לוחות אחזקה - UX200 MZA-A10", עמודים 395-396 (לוח 10 עמודות של 15,000 ק"מ עד 150,000)')
s.src(PAGE,'importer','דף ספרי הרכב של לקסוס ישראל (אפליקציה books.union-motors.co.il/LexusApp)')
s.write('reviewed','הועתק מלוח האחזקה בספר הרכב העברי של UX200 (בכותרת הלוח כתוב מנוע M20A-FXS, אך טבלת הנוזלים מציינת נוזל CVT FE של גיר הבנזין). טיפול כל 15,000 ק"מ או שנה; מסנן מזגן בכל טיפול; מסנן אוויר מוחלף ב-60,000 וב-120,000; נוזל בלמים כל 30,000 או שנתיים; מצתים כל 90,000; נוזל קירור לראשונה ב-160,000 ואחר כך כל 80,000; מסנן דלק ב-75,000 וב-150,000.',
  {'engine_oil':'0W-16 או 5W-30; 4.6 ליטר עם מסנן','coolant':'Toyota Super Long Life Coolant, 6.5 ליטר','brake_fluid':'DOT 4','_note':'מטבלת הנוזלים בספר UX200'})
rule('Lexus',['LEXUS UX200','UX200','UX 200'],(2019,2022),'lexus-ux200-2019-2021-2.0')

s=ux('lexus-ux250h-2019-2026-2.0-hybrid','UX 250h / UX 300h','UX 250h / UX 300h',(2019,2026),['2.0 hybrid (M20A-FXS)'],'hybrid',True)
s.src(API.format(74),'importer','ספר רכב UX200 בעברית (יוניון מוטורס), לוחות אחזקה עמ\' 395-396; הלוח שימש כאחות כי בספרי UX250h ו-UX300h אין לוח')
s.src(API.format(77),'importer','ספר רכב UX250h בעברית: פרק 6 בלי לוח תחזוקה (נבדק)')
s.src(API.format(70),'importer','ספר רכב UX300h בעברית: פרק 6 בלי לוח תחזוקה (נבדק)')
s.write('draft','טיוטה: בספרי הרכב העבריים של UX250h ו-UX300h אין לוח אחזקה, ולכן נלקח הלוח מספר UX200 (אותו דגם ואותה משפחת מנוע M20A, טיפול כל 15,000 ק"מ או שנה). בלוח הזה חסרים פריטים ייחודיים להיברידי, כמו נוזל קירור הממיר ומסנן אוורור הסוללה ההיברידית, ויש לבדוק אותם מול המוסך. בגרסה ההיברידית אין גיר CVT רגיל; הבדיקה של נוזל התיבה נשארה כמו בלוח.')
rule('Lexus',['LEXUS UX250H','UX250H','UX 250H','LEXUS UX300H','UX300H','LEXUS UX 250H'],(2019,2026),'lexus-ux250h-2019-2026-2.0-hybrid')

def turbo8ar(id_, model, model_he, gen, years, air_pat, plugs_note, belt):
    s=S(id_,'Lexus','לקסוס',model,model_he,gen,years,['2.0 turbo (8AR-FTS)'],'petrol',IMP,15000,12,
        'לפי לוח האחזקה בספר הרכב העברי: שמן ומסנן כשנדלקת נורית התחזוקה, ולכל המאוחר כל 15,000 ק"מ או 12 חודשים; שאר הלוח בעמודות של 15,000 ק"מ',150000)
    s.every('engine_oil','replace',15000,'כשנדלקת נורית התחזוקה, ולכל המאוחר כל 15,000 ק"מ או 12 חודשים')
    s.every('oil_filter','replace',15000,'יחד עם שמן המנוע')
    if belt:
        s.every('drive_belt','inspect',15000,'בדיקה ראשונה לאחר 105,000 ק"מ ומאז כל 15,000',start=105000)
        s.li('drive_belt','inspect',first_km=105000,first_months=72,then_every_km=15000,then_every_months=12)
    s.every('cooling_system','inspect',30000,'מערכת קירור וחימום')
    s.every('coolant','inspect',30000)
    s.li('coolant','replace',first_km=150000,then_every_km=90000,note='החלפה ראשונה לאחר 150,000 ק"מ ומאז כל 90,000 (כולל מעגל האינטרקולר)')
    s.every('exhaust','inspect',30000)
    s.every('spark_plugs','replace',60000,plugs_note)
    s.pat('air_filter',air_pat,15000,'בתנאים מחמירים: בדיקה כל 7,500 ק"מ, החלפה כל 60,000')
    s.every('fuel_lines','inspect',30000,'צינורות דלק, חיבורים ומכסה מיכל הדלק')
    s.at('evap_system','inspect',[45000,90000,135000],'מכלול מסנן פחם')
    s.every('pedals','inspect',30000,'דוושת בלם')
    s.every('brake_pads','inspect',15000,'בתנאים מחמירים כל 7,500'); s.every('brake_discs','inspect',15000)
    s.every('brake_fluid','replace',30000,'כל 30,000 ק"מ או 24 חודשים')
    s.every('brake_lines','inspect',30000)
    s.li('vacuum_hose','inspect',every_km=195000,every_months=120,note='משאבת ואקום ומגביר בלם')
    s.every('steering','inspect',30000,'בתנאים מחמירים כל 15,000')
    s.every('cv_boots','inspect',30000,'בתנאים מחמירים כל 15,000')
    s.every('suspension','inspect',30000,'מתלים, מחברים כדוריים ומגיני אבק; בתנאים מחמירים כל 15,000 והידוק ברגי מתלים ושלדה')
    s.at('transmission_oil','inspect',[60000,120000],'נוזל גיר אוטומטי; בתנאים מחמירים בדיקה ב-45,000 וב-135,000 והחלפה ב-90,000')
    s.at('differential_oil','inspect',[60000,120000],'דיפרנציאל קדמי; בתנאים מחמירים החלפה ב-90,000')
    s.every('differential_oil','replace',30000,'דיפרנציאל אחורי (4X4): החלפה כל 30,000 ק"מ (R:48 חודשים)')
    s.every('tires','inspect',30000,'צמיגים ולחץ אוויר; בתנאים מחמירים כל 15,000')
    s.every('lights','inspect',30000,'אורות, צופר, מגבים ומתזים')
    s.every('cabin_filter','replace',15000)
    s.time('engine_oil','replace',12,'לכל המאוחר כל 12 חודשים')
    return s

s=turbo8ar('lexus-nx300-2018-2021-2.0-turbo','NX 300','NX 300','AGZ10/AGZ15',(2018,2021),'IIIRIIIRII','מצתי פלטינה/אירידיום כל 60,000',True)
s.every('propshaft','adjust',30000,'4X4: הידוק ברגי גל ההינע (T:48); בתנאים מחמירים כל 15,000')
s.every('transfer_case_oil','replace',30000,'4X4: שמן תיבת העברה כל 30,000 (R:48)')
s.every('body_underside','inspect',15000,'בדיקת חלודה; שטיחי רצפה בכל ביקור')
s.src(API.format(161),'importer','ספר רכב NX300 בעברית (יוניון מוטורס), "לוח אחזקה NX300 8AR-FTS", עמודים 479-480 (לוח 10 עמודות של 15,000 ק"מ עד 150,000) וטבלת נוזלים')
s.src(PAGE,'importer','דף ספרי הרכב של לקסוס ישראל (אפליקציה books.union-motors.co.il/LexusApp)')
s.write('reviewed','הועתק מלוח האחזקה בספר הרכב העברי של NX300 (מנוע 2.0 טורבו 8AR-FTS, 2018-2021). שמן ומסנן לפי נורית התחזוקה ולכל המאוחר כל 15,000 ק"מ או שנה; מסנן מזגן בכל טיפול; מסנן אוויר ב-60,000 וב-120,000; מצתים ונוזל בלמים: מצתים כל 60,000, נוזל בלמים כל 30,000; ב-4X4 שמן דיפרנציאל אחורי ותיבת העברה כל 30,000; נוזל קירור לראשונה ב-150,000 ואחר כך כל 90,000.',
  {'engine_oil':'0W-20 או 5W-30; 4.9 ליטר עם מסנן','coolant':'Toyota Super Long Life Coolant, 7.9 ליטר (אינטרקולר 2.9)','brake_fluid':'DOT 3 או DOT 4','_note':'מטבלת הנוזלים בספר NX300'})
rule('Lexus',['LEXUS NX300','NX300','NX 300'],(2017,2022),'lexus-nx300-2018-2021-2.0-turbo',engine_codes=['8AR','8AR-FTS'])

s=turbo8ar('lexus-rx300-2017-2022-2.0-turbo','RX 300','RX 300','AGL20/AGL25',(2017,2022),'IIRIIRIIRI','מצתי פלטינה/אירידיום: בגיליון מסומנת החלפה ב-60,000 וב-120,000',False)
s.every('body_underside','inspect',30000,'בדיקת חלודה; שטיחי רצפה בכל ביקור')
s.src(API.format(148),'importer','ספר רכב RX300/RX350/RX350L בעברית (יוניון מוטורס), "לוח אחזקה - RX300 8AR-FTS" (גיליון מיום 26.4.18), עמוד 730 בספר (עמוד PDF 730)')
s.src(PAGE,'importer','דף ספרי הרכב של לקסוס ישראל (אפליקציה books.union-motors.co.il/LexusApp)')
s.write('reviewed','הועתק מגיליון האחזקה של RX300 (מנוע 2.0 טורבו 8AR-FTS) שבסוף ספר הרכב העברי. שמן ומסנן לפי נורית התחזוקה ולכל המאוחר כל 15,000 ק"מ או שנה; מסנן מזגן בכל טיפול; מסנן אוויר מוחלף ב-45,000, 90,000 ו-135,000 כפי שמסומן בגיליון; מצתים ב-60,000 וב-120,000; נוזל בלמים ושמן דיפרנציאל אחורי כל 30,000; נוזל קירור לראשונה ב-150,000 ואחר כך כל 90,000. בגיליון אין שורה לרצועת ההינע. הגיליון לא חל על RX350 (מנוע V6).',
  {'engine_oil':'0W-20 או 5W-30; 4.9 ליטר עם מסנן','coolant':'Toyota Super Long Life Coolant, 8.7 ליטר (אינטרקולר 3.2)','brake_fluid':'DOT 3 או DOT 4','_note':'מטבלת הנוזלים בגיליון'})
rule('Lexus',['LEXUS RX300','RX300','RX 300'],(2017,2023),'lexus-rx300-2017-2022-2.0-turbo',engine_codes=['8AR','8AR-FTS'])
# UX200, UX250h/UX300h and RX300 were merged into the repo by group prem3 while this ran: drop ours
import os
DROP={'lexus-ux200-2019-2021-2.0','lexus-ux250h-2019-2026-2.0-hybrid','lexus-rx300-2017-2022-2.0-turbo'}
RULES[:]=[r for r in RULES if r['schedule'] not in DROP]
for i in DROP:
    f=os.path.join(OUT,i+'.json')
    if os.path.exists(f): os.remove(f)
save_rules('rules_lexus.json')
