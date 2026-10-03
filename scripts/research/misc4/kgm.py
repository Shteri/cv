from lib import grid, write
IMP = 'טלקאר מוטורס (KGM ישראל)'
KG = 'https://kgm.co.il/wp-content/uploads/'
def every(n_km):
    return lambda k: k % n_km == 0

# ---------- Rexton 2021-2026 (Y450/Y461) D22DTR, GEN table, 2024 Hebrew book ----------
rows = [
 ('drive_belt','inspect','all'),
 ('engine_oil','replace','all','שמן ACEA C2 0W-30; בדיקה ראשונה של המפלס ב-7,500 ק"מ'),
 ('oil_filter','replace','all'),
 ('coolant_hoses','inspect','all'),
 ('fuel_filter','replace',every(30000),'ניקוז מים ממסנן הדלק בכל החלפת שמן'),
 ('fuel_filter','inspect',lambda k: k%30000!=0,'ניקוז מים ממסנן הדלק'),
 ('fuel_lines','inspect','all'),
 ('air_filter','replace','all'),
 ('exhaust','inspect','all'),
 ('parking_brake','inspect','all'),
 ('brake_pads','inspect','all','רפידות קדמיות ואחוריות'),
 ('brake_lines','inspect','all'),
 ('pedals','inspect','all'),
 ('transfer_case_oil','replace',every(60000),'4x4'),
 ('transfer_case_oil','inspect',lambda k: k%60000!=0,'4x4'),
 ('differential_oil','replace',every(30000),'סרן קדמי ואחורי קשיח כל 30,000; סרן אחורי עם מתלים נפרדים (IRS) רק כל 60,000'),
 ('transmission_oil','inspect',every(60000),'בדיקה והוספה'),
 ('body_underside','inspect','all','חופש והידוק ברגים, דליפות משחה'),
 ('steering','inspect','all','גלגל ומוטות ההגה'),
 ('power_steering_fluid','inspect','all','נוזל וצינורות הגה כוח'),
 ('cv_boots','inspect','all','שרוולי גל הינע'),
 ('seat_belts','inspect','all'),
 ('propshaft','inspect','all','משחת סיכה בגל ההינע קדמי ואחורי ובמסבי הגלגלים'),
 ('cabin_filter','replace','all'),
]
write(dict(
 id='kgm-rexton-2021-2026-2.2-diesel', make='KGM', make_he='KGM (סאנגיונג)', model='Rexton', model_he='רקסטון',
 generation='Y450 / Y461 (2021 ואילך)', years=[2021,2026], engines=['2.2 טורבו דיזל (D22DTR, קוד רישוי 672980)'], fuel='diesel', importer=IMP,
 interval=dict(km=15000, months=12, note='טבלת D22DTR "GEN" (כללית, לא האירופית) בספר הנהג העברי: 15,000 ק"מ או 12 חודשים, המוקדם מביניהם. בתנאים קשים 7,500 ק"מ או 6 חודשים'),
 cycle_km=120000,
 services=grid(15000,120000,rows),
 long_interval=[
  dict(item='coolant', action='replace', every_km=200000, every_months=60, note='5 שנים או 200,000 ק"מ, המוקדם; בדיקת מפלס בכל טיפול'),
  dict(item='transmission_oil', action='replace', every_km=60000, note='בתנאים קשים בלבד; בתנאים רגילים בדיקה והוספה'),
 ],
 time_based=[dict(item='brake_fluid', action='replace', months=24, note='כל שנתיים; בדיקת מפלס לעתים קרובות')],
 specs=dict(engine_oil='שמן מקורי KG Mobility או ACEA C2 SAE 0W-30', oil_capacity='כ-6.0 ליטר', coolant='נוזל קירור מקורי SYC-1025 (חומצה אורגנית, כחול) 50:50, כ-10.2 ליטר', brake_fluid='DOT4', fuel='סולר; תמיסת אוריאה לפי DIN 70070 / ISO 22241 (כ-20 ליטר)', _note='מטבלת הנוזלים בספר הנהג העברי של רקסטון (עמ\' 2)'),
 sources=[dict(url=KG+'2024/04/240370_REXTON_OM_Y461-17-04-24-AllBookForWeb.pdf', kind='importer', note='ספר הנהג העברי של רקסטון (Y461, 04/2024), עמ\' 6-5 עד 6-7 (עמודי PDF 464-466): טבלת טיפולים D22DTR (GEN). הטבלה האירופית (עמ\' 6-2, 20,000 ק"מ) מיועדת למדינות האיחוד בלבד; שכבת הטקסט מקודדת ולכן נקרא מתמונת העמוד'),
          dict(url='https://kgm.co.il/ספרי-רכב/', kind='importer', note='עמוד ספרי הרכב באתר KGM ישראל')],
 status='reviewed',
 notes='הועתק מטבלת הטיפולים הכללית (GEN) של מנוע הדיזל D22DTR בספר הנהג העברי של רקסטון 2024. I = בדיקה (ותיקון/החלפה לפי הצורך), R = החלפה. מסנן דלק מוחלף כל 30,000 ק"מ, ומים מנוקזים ממנו בכל טיפול. שמן תיבת העברה כל 60,000; שמן סרנים קדמי ואחורי קשיח כל 30,000 (סרן אחורי עם מתלים נפרדים - כל 60,000). שמן גיר אוטומטי נבדק, ומוחלף כל 60,000 רק בתנאים קשים. רכבים מ-2021 עד 2023 נושאים את אותו קוד מנוע (672980); הטבלה נלקחה מספר 2024.'
))

# ---------- Rexton 2018-2020 (Y400) D22DTR general table, 2018 Hebrew book ----------
rows = [
 ('engine_oil','replace','all','בדיקה ראשונה של המפלס ב-7,500 ק"מ'),
 ('oil_filter','replace','all'),
 ('drive_belt','inspect','all','בדיקה כל 20,000 ק"מ לפי הספר'),
 ('air_filter','clean',lambda k: k%30000!=0,'ניקוי לפי הספר כל 10,000 ק"מ'),
 ('air_filter','replace',every(30000)),
 ('fuel_filter','replace',every(45000),'ניקוז מים ומשקעים בכל 15,000'),
 ('fuel_filter','inspect',lambda k: k%45000!=0,'ניקוז מים ומשקעים'),
 ('fuel_lines','inspect','all'),
 ('vacuum_hose','inspect','all'),
 ('exhaust','inspect','all'),
 ('power_steering_fluid','inspect','all','בורג תושבת וצינורות ההגה (כל 10,000 לפי הספר)'),
 ('steering','inspect','all','חיבורים, תמסורת ושרוולים; מפרק כדורי חיצוני (כל 10,000 לפי הספר)'),
 ('brake_lines','inspect','all','אחרי 20,000 ק"מ או שנה ואילך'),
 ('brake_pads','inspect','all','רפידות ודיסקים (כל 10,000 לפי הספר)'),
 ('parking_brake','inspect','all'),
 ('transmission_oil','inspect',every(30000),'גיר אוטומטי 7 הילוכים: בדיקה והוספה'),
 ('manual_gearbox_oil','inspect',every(60000),'גיר ידני'),
 ('transfer_case_oil','replace',every(60000),'4x4'),
 ('differential_oil','replace',every(30000),'סרן קדמי ואחורי קשיח; סרן אחורי מתלים נפרדים - החלפה כל 60,000'),
 ('cv_boots','inspect','all','גלי הינע ושרוולים, גירוז (כל 10,000 לפי הספר)'),
 ('cabin_filter','replace','all','לפי הספר: בדיקה כל 10,000 והחלפה לפי הצורך'),
 ('tires','inspect',every(30000),'בלאי צמיגים'),
 ('tire_rotation','rotate','all','הספר: סבב כל 5,000 ק"מ'),
 ('wheel_alignment','inspect','all','איזון וכיוון גלגלים (כל 10,000 לפי הספר)'),
 ('body_underside','inspect','all','הידוק ברגי שלדה, מרכב ומפרקים כדוריים'),
 ('diagnostics','inspect','all'),
 ('lights','adjust',every(30000),'כיוון אלומות הפנסים'),
 ('door_hinges','inspect','all','סיכה של מכסה מנוע ודלתות'),
]
write(dict(
 id='ssangyong-rexton-2018-2021-2.2-diesel', make='SsangYong', make_he='סאנגיונג', model='Rexton', model_he='רקסטון',
 generation='Y400 (G4)', years=[2018,2021], engines=['2.2 טורבו דיזל (D22DTR, קוד רישוי 672960)'], fuel='diesel', importer=IMP,
 interval=dict(km=15000, months=12, note='הטבלה הכללית (לא האירופית) בספר הנהג העברי: החלפת שמן כל 15,000 ק"מ או שנה. בתנאים קשים 7,500 ק"מ או 6 חודשים'),
 cycle_km=180000,
 services=grid(15000,180000,rows),
 long_interval=[
  dict(item='coolant', action='replace', every_km=200000, every_months=60, note='5 שנים או 200,000 ק"מ'),
  dict(item='steering', action='replace', every_km=100000, note='מפרק כדורי חיצוני וזרועות: החלפה כל 100,000 ק"מ לפי הספר'),
  dict(item='transmission_oil', action='replace', every_km=60000, note='בתנאים קשים בלבד'),
  dict(item='manual_gearbox_oil', action='replace', every_km=100000, note='בתנאים קשים בלבד'),
 ],
 time_based=[dict(item='brake_fluid', action='replace', months=24, note='כל שנתיים')],
 specs=dict(engine_oil='שמן מקורי סאנגיונג SAE 5W-30 (MB 229.51)', oil_capacity='כ-5.0 ליטר', coolant='SYC-1025 (חומצה אורגנית, כחול) 50:50, כ-10.2 ליטר', brake_fluid='DOT4', fuel='סולר', _note='מטבלת הנוזלים בספר הנהג העברי 2018 (עמ\' 3)'),
 sources=[dict(url=KG+'2020/10/new_Rexton_OM_2018-.pdf', kind='importer', note='ספר הנהג העברי של רקסטון 2018, עמ\' 7-5 עד 7-7 (עמודי PDF 393-395): "D22DTR - מרווחי תחזוקה וטיפולים (כללי)". טבלת אירופה (7-2) היא 20,000 ק"מ')],
 status='reviewed',
 notes='הטבלה בספר בנויה לפי תדירות (כל 10,000, כל 15,000, כל 30,000 ק"מ) ולא לפי טיפולים. כאן הכול מסודר על טיפולי 15,000: פריטים של "כל 10,000" מופיעים בכל טיפול, ופריטי "כל 30,000" בכל טיפול שני. מסנן אוויר מנוקה ומוחלף כל 30,000; מסנן דלק כל 45,000 (ניקוז מים כל 15,000); שמן סרנים כל 30,000 ותיבת העברה כל 60,000. הספר ממליץ גם על סבב צמיגים כל 5,000 ק"מ.'
))

# ---------- Musso 2024-2026 D22DTR, Q300 2026 Hebrew book ----------
rows = [
 ('drive_belt','inspect','all'),
 ('engine_oil','replace','all','בדיקה ראשונה של המפלס ב-7,500 ק"מ'),
 ('oil_filter','replace','all'),
 ('coolant_hoses','inspect','all'),
 ('fuel_filter','replace',every(30000),'ניקוז מים בכל החלפת שמן'),
 ('fuel_filter','inspect',lambda k: k%30000!=0,'ניקוז מים'),
 ('fuel_lines','inspect','all'),
 ('air_filter','replace','all','בדיקה ראשונה וניקוי ב-7,500 ק"מ'),
 ('exhaust','inspect','all'),
 ('parking_brake','inspect','all'),
 ('brake_pads','inspect','all'),
 ('brake_lines','inspect','all'),
 ('pedals','inspect','all'),
 ('transfer_case_oil','replace',every(60000),'4x4'),
 ('transfer_case_oil','inspect',lambda k: k%60000!=0,'4x4'),
 ('differential_oil','replace',every(30000),'סרן קדמי ואחורי'),
 ('differential_oil','inspect',lambda k: k%30000!=0),
 ('transmission_oil','inspect',every(60000),'גיר אוטומטי: בדיקה והוספה (60,000 ק"מ או 3 שנים)'),
 ('manual_gearbox_oil','inspect',every(60000),'גיר ידני: בדיקה והוספה'),
 ('steering','inspect','all'),
 ('power_steering_fluid','inspect','all'),
 ('cv_boots','inspect','all'),
 ('seat_belts','inspect','all'),
 ('propshaft','inspect','all','משחת סיכה בגל ההינע ובמסבי הגלגלים'),
 ('cabin_filter','replace','all'),
]
write(dict(
 id='kgm-musso-2024-2026-2.2-diesel', make='KGM', make_he='KGM (סאנגיונג)', model='Musso', model_he='מוסו',
 generation='Q200 / Q300', years=[2024,2026], engines=['2.2 טורבו דיזל (D22DTR, קוד רישוי 672980)'], fuel='diesel', importer=IMP,
 interval=dict(km=15000, months=12, note='טבלת D22DTR (GEN) בספר הנהג העברי: 15,000 ק"מ או 12 חודשים; בתנאים קשים 7,500 ק"מ או 6 חודשים'),
 cycle_km=120000,
 services=grid(15000,120000,rows),
 long_interval=[
  dict(item='coolant', action='replace', every_km=200000, every_months=60, note='5 שנים או 200,000 ק"מ'),
  dict(item='transmission_oil', action='replace', every_km=60000, note='בתנאים קשים; בתנאים רגילים בדיקה בלבד'),
  dict(item='manual_gearbox_oil', action='replace', every_km=120000, note='בתנאים קשים בלבד'),
 ],
 time_based=[dict(item='brake_fluid', action='replace', months=24, note='כל שנתיים')],
 specs=dict(engine_oil='שמן מקורי KGM או ACEA C2 SAE 0W-30', oil_capacity='כ-6.0 ליטר', brake_fluid='DOT4', fuel='סולר', _note='מטבלת הנוזלים בספר הנהג העברי (עמ\' 2)'),
 sources=[dict(url=KG+'2026/08/260841-MUSSO-Q300-OM-S1-SH-20-08-26.pdf', kind='importer', note='ספר הנהג העברי של מוסו (Q300, 08/2026), עמ\' 6-5 עד 6-7 (עמודי PDF 453-455): "D22DTR - (GEN) טבלת טיפולים תקופתיים"')],
 status='draft',
 notes='טיוטה: הטבלה נלקחה מספר הנהג של מוסו החדש (2026). רכבי 2024-2025 בישראל הם מהדור הקודם עם אותו מנוע (672980), ולכן יש לאמת מול היבואן. שמן סרנים קדמי ואחורי כל 30,000 ק"מ, שמן תיבת העברה כל 60,000, מסנן דלק כל 30,000.'
))

# ---------- Torres 1.5T petrol (G15DTF) ----------
rows = [
 ('drive_belt','inspect','all'),
 ('engine_oil','replace','all','מומלץ להחליף את השמן הראשון כבר ב-10,000 ק"מ; בדיקת מפלס ראשונה ב-7,500'),
 ('oil_filter','replace','all'),
 ('coolant_hoses','inspect','all'),
 ('fuel_filter','inspect',every(30000),'בדיקה כל 30,000; החלפה כל 50,000 רק אם משתמשים בדלק באיכות נמוכה'),
 ('fuel_lines','inspect','all'),
 ('air_filter','replace',every(30000)),
 ('air_filter','inspect',lambda k: k%30000!=0),
 ('spark_plugs','inspect','all','תזמון הצתה'),
 ('evap_system','inspect',every(30000),'מסנן פחם פעיל וצנרת אדי דלק'),
 ('exhaust','inspect','all'),
 ('parking_brake','inspect','all'),
 ('brake_pads','inspect','all'),
 ('brake_lines','inspect','all'),
 ('pedals','inspect','all'),
 ('transfer_case_oil','replace',every(60000),'יחידת PTU, הנעה כפולה'),
 ('transfer_case_oil','inspect',lambda k: k%60000!=0,'הנעה כפולה'),
 ('differential_oil','inspect','all','סרן אחורי (הנעה כפולה); החלפה כל 100,000'),
 ('steering','inspect','all'),
 ('suspension','inspect','all','מפרק כדורי חיצוני; החלפה ב-90,000'),
 ('cv_boots','inspect','all'),
 ('seat_belts','inspect','all'),
 ('propshaft','inspect','all','משחת סיכה בגל ההינע ובמסבי הגלגלים'),
 ('cabin_filter','replace','all'),
]
svc = grid(15000,120000,rows)
for s in svc:
    if s['km']==90000: s['items'].append({'item':'suspension','action':'replace','note':'החלפת מפרק כדורי חיצוני (עמודת 90,000 בטבלה)'})
write(dict(
 id='kgm-torres-2024-2026-1.5t', make='KGM', make_he='KGM (סאנגיונג)', model='Torres', model_he='טורס',
 generation='J100', years=[2024,2026], engines=['1.5 טורבו בנזין (G15DTF, קוד רישוי 175950)'], fuel='petrol', importer=IMP,
 interval=dict(km=15000, months=12, note='15,000 ק"מ או 12 חודשים, המוקדם; בתנאים קשים 7,500 ק"מ או 6 חודשים'),
 cycle_km=120000, services=svc,
 long_interval=[
  dict(item='spark_plugs', action='replace', every_km=60000),
  dict(item='coolant', action='replace', every_km=200000, every_months=60, note='5 שנים או 200,000 ק"מ'),
  dict(item='fuel_filter', action='replace', every_km=50000, note='רק כשמשתמשים בדלק באיכות נמוכה'),
  dict(item='differential_oil', action='replace', every_km=100000, note='סרן אחורי, הנעה כפולה'),
  dict(item='transmission_oil', action='replace', every_km=100000, note='בתנאים קשים בלבד'),
  dict(item='manual_gearbox_oil', action='inspect', every_km=60000, every_months=36, note='גיר ידני; בתנאים קשים החלפה כל 120,000'),
 ],
 time_based=[dict(item='brake_fluid', action='replace', months=24, note='כל שנתיים')],
 specs=dict(engine_oil='שמן מקורי KG Mobility או ACEA C2 SAE 0W-30', oil_capacity='כ-4.5 ליטר', coolant='SYC-1025 (חומצה אורגנית, כחול) 50:50, כ-7.0 ליטר', brake_fluid='DOT4', fuel='בנזין', _note='מטבלת הנוזלים בספר הנהג העברי (עמ\' 2)'),
 sources=[dict(url=KG+'2025/02/241583-Torres-gasoline-OM-AllBookOptRF-03-02-25.pdf', kind='importer', note='ספר הנהג העברי של טורס בנזין (02/2025), עמ\' 6-2 עד 6-4 (עמודי PDF 420-422): "טבלת טיפולים תקופתיים - מנוע בנזין"; עמ\' 6-5 עד 6-7 לתנאים קשים')],
 status='reviewed',
 notes='הועתק מטבלת הטיפולים של מנוע הבנזין בספר הנהג העברי של טורס. מסנן אוויר מוחלף כל 30,000 ק"מ, מצתים כל 60,000, שמן תיבת העברה (PTU) כל 60,000 בהנעה כפולה. היצרן ממליץ להחליף את השמן הראשון ב-10,000 ק"מ. אותו מנוע (175950) מותקן גם בטיבולי וקוראנדו 1.5 טורבו.'
))

# ---------- Torres Hybrid ----------
rows = [
 ('engine_oil','replace','all','מומלץ להחליף את השמן הראשון ב-10,000 ק"מ; בדיקת מפלס ראשונה ב-7,500'),
 ('oil_filter','replace','all'),
 ('coolant_hoses','inspect','all'),
 ('fuel_filter','inspect',every(30000),'בדיקה כל 30,000; החלפה כל 50,000 רק עם דלק באיכות נמוכה'),
 ('fuel_lines','inspect','all'),
 ('air_filter','replace',every(30000),'בדיקה ראשונה ב-5,000 ק"מ'),
 ('air_filter','inspect',lambda k: k%30000!=0),
 ('exhaust','inspect','all'),
 ('parking_brake','inspect','all'),
 ('brake_pads','inspect','all'),
 ('brake_lines','inspect','all'),
 ('pedals','inspect','all'),
 ('steering','inspect','all'),
 ('suspension','inspect','all','מפרק כדורי, אום, שרוול'),
 ('cv_boots','inspect','all'),
 ('seat_belts','inspect','all'),
 ('propshaft','inspect','all','משחת סיכה בגל ההינע ובמסבי הגלגלים'),
 ('cabin_filter','replace','all'),
]
write(dict(
 id='kgm-torres-hybrid-2025-2026-1.5t-hev', make='KGM', make_he='KGM (סאנגיונג)', model='Torres Hybrid', model_he='טורס היברידי',
 generation='J100 HEV', years=[2025,2026], engines=['1.5 טורבו בנזין היברידי (G15DTF, קוד רישוי 177910)'], fuel='hybrid', importer=IMP,
 interval=dict(km=10000, months=12, note='טבלת HEV בספר הנהג העברי: 10,000 ק"מ או 12 חודשים, המוקדם; בתנאים קשים 5,000 ק"מ'),
 cycle_km=80000,
 services=grid(10000,80000,rows),
 long_interval=[
  dict(item='spark_plugs', action='replace', every_km=60000),
  dict(item='coolant', action='replace', every_months=60, note='נוזל קירור מנוע ונוזל קירור סוללת המתח הגבוה: בטבלה כתוב "20,000 ק"מ או 5 שנים" (בטבלת הבנזין באותו ספר: 200,000); נרשם רק לפי הזמן, לאמת מול היבואן'),
  dict(item='fuel_filter', action='replace', every_km=50000, note='רק עם דלק באיכות נמוכה'),
  dict(item='transmission_oil', action='replace', every_km=60000, note='מסנן שמן תיבת ההילוכים ההיברידית: בתנאים קשים בלבד'),
 ],
 time_based=[dict(item='brake_fluid', action='replace', months=24, note='כל שנתיים')],
 specs=dict(engine_oil='שמן מקורי KGM או API SP 0W-16 (מנוע HEV)', oil_capacity='כ-4.0 ליטר (HEV)', coolant='SYC-1025 50:50; מעגל נפרד לסוללת המתח הגבוה (כ-6.2 ליטר)', brake_fluid='DOT4', fuel='בנזין', _note='מטבלת הנוזלים בספר הנהג העברי של טורס היברידי (עמ\' 1); בספר גם שמן מנוע ההנעה החשמלי EHSF-2LV כ-4.7 ליטר'),
 sources=[dict(url=KG+'2026/03/251095-TORRES-HYBRID-2025-OM-Print.pdf', kind='importer', note='ספר הנהג העברי של טורס היברידי 2025, עמ\' 6-8 עד 6-10 (עמודי PDF 490-492): "טבלת טיפולים תקופתיים - HEV"; עמ\' 6-11 עד 6-13 לתנאים קשים'),
          dict(url='https://data.gov.il/api/3/action/datastore_search?resource_id=142afde2-6228-49f9-8a29-9b6c3a0cbe40&q=E0A1R', kind='other', note='מאגר דגמי הרכב: דגם E0A1R (קוד מנוע 177910) מסומן "היברידי רגיל", 204 כ"ס')],
 status='reviewed',
 notes='הועתק מטבלת HEV בספר הנהג העברי של טורס היברידי. מרווח 10,000 ק"מ או שנה (קצר מהגרסת הבנזין). מסנן אוויר כל 30,000, מצתים כל 60,000. בשורת נוזל הקירור הודפס 20,000 ק"מ או 5 שנים, כנראה טעות דפוס (בטבלת הבנזין 200,000) - נרשם 5 שנים בלבד. רכבי TORRES עם קוד מנוע 177910 ברישוי הם הגרסה ההיברידית.'
))

# ---------- Korando C300 1.6 diesel D16DTF (also Tivoli diesel, same engine) ----------
rows = [
 ('drive_belt','inspect','all'),
 ('engine_oil','replace','all','בדיקת מפלס ראשונה ב-7,500 ק"מ'),
 ('oil_filter','replace','all'),
 ('coolant_hoses','inspect','all'),
 ('fuel_filter','replace',every(30000),'ניקוז מים כשנורת האזהרה נדלקת'),
 ('fuel_filter','inspect',lambda k: k%30000!=0),
 ('fuel_lines','inspect','all'),
 ('air_filter','replace',every(30000)),
 ('air_filter','inspect',lambda k: k%30000!=0),
 ('exhaust','inspect','all'),
 ('parking_brake','inspect','all'),
 ('brake_pads','inspect','all'),
 ('brake_lines','inspect','all'),
 ('pedals','inspect','all'),
 ('transfer_case_oil','replace',every(60000),'הנעה כפולה'),
 ('transfer_case_oil','inspect',lambda k: k%60000!=0,'הנעה כפולה'),
 ('differential_oil','inspect','all','סרן אחורי (הנעה כפולה); החלפה כל 100,000'),
 ('steering','inspect','all'),
 ('suspension','inspect','all','מפרק כדורי חיצוני; החלפה ב-90,000'),
 ('cv_boots','inspect','all'),
 ('seat_belts','inspect','all'),
 ('propshaft','inspect','all','משחת סיכה בגל ההינע ובמסבי הגלגלים'),
 ('cabin_filter','replace','all'),
]
svc = grid(15000,120000,rows)
for s in svc:
    if s['km']==90000: s['items'].append({'item':'suspension','action':'replace','note':'החלפת מפרק כדורי חיצוני (עמודת 90,000 בטבלה)'})
write(dict(
 id='ssangyong-korando-tivoli-2018-2023-1.6-diesel', make='SsangYong', make_he='סאנגיונג', model='Korando / Tivoli', model_he='קוראנדו / טיבולי',
 generation='C300 / X100', years=[2018,2023], engines=['1.6 טורבו דיזל (D16DTF, קוד רישוי 673910)'], fuel='diesel', importer=IMP,
 interval=dict(km=15000, months=12, note='הטבלה הכללית (לא האירופית) למנוע דיזל: 15,000 ק"מ או 12 חודשים; בתנאים קשים 7,500 ק"מ או 6 חודשים'),
 cycle_km=120000, services=svc,
 long_interval=[
  dict(item='coolant', action='replace', every_km=200000, every_months=60, note='5 שנים או 200,000 ק"מ'),
  dict(item='differential_oil', action='replace', every_km=100000, note='סרן אחורי, הנעה כפולה'),
  dict(item='transmission_oil', action='replace', every_km=100000, note='בתנאים קשים בלבד'),
  dict(item='manual_gearbox_oil', action='inspect', every_km=60000, every_months=36, note='גיר ידני; בתנאים קשים החלפה כל 120,000'),
 ],
 time_based=[dict(item='brake_fluid', action='replace', months=24, note='כל שנתיים')],
 specs=dict(engine_oil='שמן מקורי סאנגיונג או ACEA C2 SAE 0W-30 (DPF)', oil_capacity='כ-5.0 ליטר (D16DTF)', brake_fluid='DOT4', fuel='סולר', _note='מטבלת הנוזלים בספר הנהג העברי של קוראנדו (עמ\' 3)'),
 sources=[dict(url=KG+'2020/10/Ssangyong_Korando.pdf', kind='importer', note='ספר הנהג העברי של קוראנדו (C300), עמ\' 6-5 עד 6-7 (עמודי PDF 433-435): "טבלת טיפולים תקופתיים - מנוע דיזל (כללי)"; טבלת אירופה (6-2) היא 20,000 ק"מ'),
          dict(url=KG+'2020/10/Ssangyong_Tivoli_Diesel.pdf', kind='importer', note='נספח לספר הנהג של טיבולי דיזל (54 עמ\'); אין בו טבלת טיפולים')],
 status='draft',
 notes='טבלת הדיזל הכללית מספר הנהג העברי של קוראנדו. מסנן דלק ומסנן אוויר מוחלפים כל 30,000 ק"מ, שמן תיבת העברה כל 60,000 (הנעה כפולה). טיוטה כי הקובץ משמש גם לטיבולי XLV דיזל עם אותו מנוע (673910), שספר הנהג המלא שלו לא נמצא.'
))
