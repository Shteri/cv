from common import *
from gmk12 import LIST_PAGE
def insp(air_note='בדיקה; לפי מחוון חיי המסנן אם קיים'):
    return [I('tire_rotation','rotate'),
        I('engine_oil','replace','לפי מחוון חיי השמן (בודקים בכל טיפול), ולפחות פעם בשנה'), I('oil_filter','replace','יחד עם השמן'),
        I('air_filter','inspect',air_note),
        I('coolant','inspect','מפלס'), I('washer_fluid','inspect','מפלס'),
        I('tires','inspect','לחץ ושחיקה'),
        I('body_underside','inspect','בדיקה חזותית לאיתור נזילות'),
        I('brake_pads','inspect'), I('brake_discs','inspect'), I('brake_lines','inspect'),
        I('steering','inspect','כולל הגה כוח; לפחות פעם בשנה'), I('suspension','inspect','לפחות פעם בשנה'),
        I('cv_boots','inspect','חצאי סרנים וגלי הינע'),
        I('seat_belts','inspect','רכיבי מערכת הריסון'),
        I('fuel_lines','inspect'), I('evap_system','inspect'), I('exhaust','inspect','כולל מגני חום'),
        I('door_hinges','clean','סיכת רכיבי המרכב'),
        I('parking_brake','inspect','כולל מנגנון מצב P'),
        I('pedals','inspect','דוושת ההאצה')]
def mpvi():
    return [I('tire_rotation','rotate'),
        I('engine_oil','replace','לפי מחוון חיי השמן (בודקים בכל טיפול), ולפחות פעם בשנה'), I('oil_filter','replace','יחד עם השמן'),
        I('air_filter','inspect','לפי מחוון חיי מסנן האוויר; מחליפים כשמוצגת הודעה'),
        I('diagnostics','inspect','ביקורת רב-נקודתית (MPVI): היסטוריית שירות וקריאות חוזרות'),
        I('lights','inspect'), I('wipers','inspect'), I('battery_12v','inspect'),
        I('body_underside','inspect','בדיקת נזילות: מנוע, גיר, סרן, תיבת העברה, קירור, הגה, דלק'),
        I('washer_fluid','inspect'), I('tires','inspect','לחץ, עומק חריצים ובלאי'),
        I('brake_pads','inspect'), I('brake_discs','inspect'),
        I('seat_belts','inspect'), I('exhaust','inspect'), I('pedals','inspect','דוושת ההאצה'),
        I('coolant_hoses','inspect','צינורות גמישים'), I('drive_belt','inspect'),
        I('suspension','inspect','בולמים ותמוכות'), I('steering','inspect'), I('cv_boots','inspect'),
        I('evap_system','inspect'), I('door_hinges','clean','סיכת רכיבי השלדה והמרכב')]
COMMON_TB = [T('engine_oil','replace',12,'לפחות פעם בשנה, גם אם המחוון לא הורה'),
             T('brake_fluid','replace',60,'כל 5 שנים'),
             T('ac_system','replace',84,'החלפת חומר הייבוש של המזגן כל 7 שנים')]
SPEC_GM = {'engine_oil':'שמן במפרט dexos1 (מומלץ סינתטי מלא) בצמיגות לפי הספר','coolant':'DEX-COOL מהול 50/50 במים נקיים','brake_fluid':'DOT 4'}
def note_intro(km):
    return f'לפי הספר מומלץ טיפול במרכז השירות כל {km:,} ק"מ: סבב צמיגים, בדיקת מפלס השמן ואחוז חיי השמן (החלפה לפי המחוון ולפחות פעם בשנה), ובדיקות כלליות. '

# ---- Equinox 2018-2023 (LYX) from Israeli 2022 book ----
def eq_svc(km):
    it = insp('בדיקה') + [I('cabin_filter','replace','או כל 12 חודשים')]
    if km % 20000 == 0: it.append(I('wipers','replace','קדמיים ואחורי; או כל 12 חודשים'))
    if km % 90000 == 0: it.append(I('spark_plugs','replace','כולל בדיקת מוליכי המצתים'))
    return {'km':km,'items':it}
eq = {
 'id':'chevrolet-equinox-2018-2023-1.5-turbo','make':'Chevrolet','make_he':'שברולט','model':'Equinox','model_he':'אקווינוקס',
 'generation':'3rd gen','years':[2017,2023],'engines':['1.5 טורבו (LYX)'],'fuel':'petrol','importer':'יו.אם.איי',
 'interval':{'km':10000,'months':12,'note':'לפי ספר הנהג העברי של יו.אם.איי (2022): סבב צמיגים ובדיקות כל 10,000 ק"מ; שמן ומסנן לפי מחוון חיי השמן ולפחות פעם בשנה'},
 'cycle_km':180000,
 'services':[eq_svc(k) for k in range(10000,180001,10000)],
 'long_interval':[
   L('cabin_filter','replace', every_km=10000, every_months=12),
   L('wipers','replace', every_km=20000, every_months=12),
   L('spark_plugs','replace', every_km=90000),
   L('differential_oil','replace','סרן אחורי, AWD בלבד (בשימוש מאומץ: כל 120,000)', every_km=240000),
   L('coolant','replace','ריקון ומילוי מערכת הקירור', every_km=240000, every_months=60),
   L('drive_belt','inspect','בדיקה חזותית; החלפה לפי הצורך', every_km=240000, every_months=120),
   L('transmission_oil','replace','שימוש מאומץ בלבד (פקקים בחום, הרים, נהיגה מהירה מאוד, מונית)', every_km=70000),
 ],
 'time_based': COMMON_TB,
 'specs': dict(SPEC_GM, _note='נבדק מול ספר הנהג העברי של היבואן (2022)'),
 'sources':[
   {'url':CHEV+'r5ff231y/newאקווינוקס-2022.pdf','kind':'importer','note':'ספר נהג שברולט אקווינוקס 2022, יו.אם.איי (GMNA-Localizing-Israel), "תכנית תחזוקה" עמ\' 283-287, נוזלים עמ\' 288'},
   {'url':CHEV+'mj5fqubb/אקווינוקס-2018.pdf','kind':'importer','note':'ספר נהג אקווינוקס 2018: אין בו לוח טיפולים (מפנה לחוברת תחזוקה נפרדת); מאשר החלפת שמן לפי המחוון ולפחות פעם בשנה'},
   LIST_PAGE],
 'status':'reviewed',
 'notes':'הלוח לקוח מספר הנהג העברי של יו.אם.איי לאקווינוקס 2022 (מנוע 1.5 טורבו), שבו המרווחים הותאמו לישראל: כל 10,000 ק"מ (ולא 12,000 כמו בספר האמריקאי). '+note_intro(10000)+'מסנן מזגן בכל טיפול (או כל 12 חודשים), מגבים כל 20,000 או שנה, מצתים כל 90,000, בוכנות הגז של מכסה המנוע כל 120,000 או 10 שנים (אין מפתח פריט במאגר), ב-240,000: נוזל קירור (או 5 שנים), שמן סרן אחורי ב-AWD ובדיקת רצועת העזר (או 10 שנים). נוזל בלמים כל 5 שנים, מייבש המזגן כל 7 שנים. ספרי 2018-2021 העבריים אינם כוללים לוח, ולכן הוחל הלוח של 2022 על כל הדור (אותו מנוע).'
}
write(eq)

# ---- Blazer 2019-2024 (LSY 2.0T / LGX 3.6) from Israeli 2023 book ----
def bl_svc(km):
    it = mpvi() + [I('cabin_filter','replace','או כל 12 חודשים')]
    if km % 90000 == 0: it.append(I('spark_plugs','replace','מנוע 2.0 טורבו בלבד; במנוע 3.6 V6 כל 150,000'))
    return {'km':km,'items':it}
bl = {
 'id':'chevrolet-blazer-2019-2024-2.0-3.6','make':'Chevrolet','make_he':'שברולט','model':'Blazer','model_he':'בלייזר',
 'generation':'3rd gen','years':[2019,2024],'engines':['2.0 טורבו (LSY)','3.6 V6 (LGX)'],'fuel':'petrol','importer':'יו.אם.איי',
 'interval':{'km':10000,'months':12,'note':'לפי ספר הנהג העברי של יו.אם.איי (2023): סבב צמיגים וביקורת רב-נקודתית כל 10,000 ק"מ; שמן ומסנן לפי מחוון חיי השמן ולפחות פעם בשנה'},
 'cycle_km':90000,
 'services':[bl_svc(k) for k in range(10000,90001,10000)],
 'long_interval':[
   L('cabin_filter','replace', every_km=10000, every_months=12),
   L('spark_plugs','replace','מנוע 2.0 טורבו (LSY)', every_km=90000),
   L('spark_plugs','replace','מנוע 3.6 V6 (LGX)', every_km=150000),
   L('differential_oil','replace','סרן אחורי, AWD בלבד (בשימוש מאומץ: כל 120,000)', every_km=240000),
   L('coolant','replace','ריקון ומילוי מערכת הקירור', every_km=240000, every_months=72),
   L('transmission_oil','replace','שימוש מאומץ בלבד (פקקים בחום, הרים, גרירה, מונית)', every_km=70000),
 ],
 'time_based': COMMON_TB,
 'specs': dict(SPEC_GM, _note='נבדק מול ספר הנהג העברי של היבואן (2023)'),
 'sources':[
   {'url':CHEV+'yrlos5wo/2023-בלייזר.pdf','kind':'importer','note':'ספר נהג שברולט בלייזר 2023, יו.אם.איי (GMNA-Localizing-Israel), "תכנית תחזוקה" ו-MPVI עמ\' 314-318, נוזלים עמ\' 319'},
   {'url':CHEV+'bjchxiwl/בלייזר-2019.pdf','kind':'importer','note':'ספר נהג בלייזר 2019: אין בו לוח טיפולים'},
   LIST_PAGE],
 'status':'reviewed',
 'notes':'הלוח לקוח מספר הנהג העברי של יו.אם.איי לבלייזר 2023, שבו המרווחים הותאמו לישראל: כל 10,000 ק"מ. בכל טיפול: סבב צמיגים, ביקורת רב-נקודתית (MPVI: אבחון וקריאות חוזרות, שמן, תאורה, מגבים, מצבר, נזילות, צמיגים, בלמים, חגורות, פליטה, צינורות, רצועות, בולמים, היגוי, שרוולי סרן, מערכת אדים), סיכת השלדה, בדיקת השמן ואחוז חיי השמן (החלפה לפי המחוון ולפחות פעם בשנה), מסנן אוויר לפי מחוון חיי המסנן, ומסנן מזגן (או כל 12 חודשים). מצתים: 2.0 טורבו כל 90,000, 3.6 V6 כל 150,000. בוכנות הגז כל 160,000 או 10 שנים (אין מפתח פריט במאגר). ב-240,000: נוזל קירור (או 6 שנים) ושמן סרן אחורי ב-AWD. נוזל בלמים כל 5 שנים, מייבש המזגן כל 7 שנים. ספר 2019 העברי אינו כולל לוח, ולכן הוחל לוח 2023 על כל הדור.'
}
write(bl)

# ---- Traverse 2018-2024 (LFY) from Israeli 2022 book ----
def tr_svc(km):
    it = insp('לפי מחוון חיי מסנן האוויר; החלפה לפי הצורך') + [I('cabin_filter','replace','או כל 12 חודשים')]
    if km % 20000 == 0: it.append(I('wipers','replace','קדמיים ואחורי; או כל 12 חודשים'))
    if km % 150000 == 0: it.append(I('spark_plugs','replace','כולל בדיקת מוליכי המצתים'))
    if km == 240000: it += [I('coolant','replace','או כל 5 שנים'), I('differential_oil','replace','סרן אחורי, AWD בלבד'), I('drive_belt','inspect','או כל 10 שנים')]
    return {'km':km,'items':it}
tr = {
 'id':'chevrolet-traverse-2018-2026-3.6','make':'Chevrolet','make_he':'שברולט','model':'Traverse','model_he':'טראוורס',
 'generation':'C1XX','years':[2018,2026],'engines':['3.6 V6 (LFY)'],'fuel':'petrol','importer':'יו.אם.איי',
 'interval':{'km':10000,'months':12,'note':'לפי ספר הנהג העברי של יו.אם.איי (2022): סבב צמיגים ובדיקות כל 10,000 ק"מ; שמן ומסנן לפי מחוון חיי השמן ולפחות פעם בשנה'},
 'cycle_km':300000,
 'services':[tr_svc(k) for k in range(10000,300001,10000)],
 'long_interval':[
   L('cabin_filter','replace', every_km=10000, every_months=12),
   L('wipers','replace', every_km=20000, every_months=12),
   L('spark_plugs','replace', every_km=150000),
   L('differential_oil','replace','סרן אחורי, AWD בלבד (בשימוש מאומץ: כל 120,000)', every_km=240000),
   L('coolant','replace','ריקון ומילוי מערכת הקירור', every_km=240000, every_months=60),
   L('drive_belt','inspect','בדיקה חזותית; החלפה לפי הצורך', every_km=240000, every_months=120),
   L('transmission_oil','replace','שימוש מאומץ בלבד (פקקים בחום, הרים, גרירה, מונית)', every_km=70000),
 ],
 'time_based': COMMON_TB,
 'specs': dict(SPEC_GM, _note='נבדק מול ספר הנהג העברי של היבואן (2022)'),
 'sources':[
   {'url':CHEV+'53cebdpu/טרוורס-2022new.pdf','kind':'importer','note':'ספר נהג שברולט טראוורס 2022, יו.אם.איי (GMNA-Localizing-Israel), "תכנית תחזוקה" עמ\' 333-337'},
   {'url':CHEV+'r0jdzkhu/טראוורס-2019.pdf','kind':'importer','note':'ספר נהג טראוורס 2019: אין בו לוח טיפולים'},
   LIST_PAGE],
 'status':'reviewed',
 'notes':'הלוח לקוח מספר הנהג העברי של יו.אם.איי לטראוורס 2022 (3.6 V6), שבו המרווחים הותאמו לישראל: כל 10,000 ק"מ. '+note_intro(10000)+'מסנן מזגן בכל טיפול (או כל 12 חודשים), מגבים כל 20,000 או שנה, בוכנות הגז של מכסה המנוע כל 120,000 או 10 שנים (אין מפתח פריט במאגר), מצתים כל 150,000, ב-240,000 נוזל קירור (או 5 שנים), שמן סרן אחורי ב-AWD ובדיקת רצועת העזר. נוזל בלמים כל 5 שנים, מייבש המזגן כל 7 שנים. המחזור כאן 300,000 כדי שהמגבים והמצתים ייפלו נכון. ספר 2019 העברי אינו כולל לוח, ולכן הוחל לוח 2022 על כל הדור עם מנוע LFY.'
}
write(tr)

# ---- Traverse 2025-2026 (LK0) from Israeli 2025 book (PATAC-localized) ----
tr25 = {
 'id':'chevrolet-traverse-2025-2026-2.5t','make':'Chevrolet','make_he':'שברולט','model':'Traverse','model_he':'טראוורס',
 'generation':'דור 3','years':[2025,2026],'engines':['2.5 טורבו (LK0)'],'fuel':'petrol','importer':'יו.אם.איי',
 'interval':{'km':12000,'months':12,'note':'לפי ספר הנהג העברי של יו.אם.איי (2025): סבב צמיגים וביקורת רב-נקודתית כל 12,000 ק"מ; שמן ומסנן לפי מחוון חיי השמן ולפחות פעם בשנה'},
 'cycle_km':12000,
 'services':[{'km':12000,'items': mpvi() + [I('cabin_filter','replace','או כל 12 חודשים')]}],
 'long_interval':[
   L('spark_plugs','replace','כולל בדיקת מוליכי המצתים', every_km=90000),
   L('differential_oil','replace','סרן אחורי, AWD בלבד (בשימוש מאומץ: כל 120,000)', every_km=240000),
   L('coolant','replace','ריקון ומילוי מערכת הקירור', every_km=240000, every_months=72),
   L('transmission_oil','replace','שימוש מאומץ בלבד (פקקים בחום, הרים, גרירה, מונית)', every_km=70000),
 ],
 'time_based': COMMON_TB,
 'specs': dict(SPEC_GM, _note='נבדק מול ספר הנהג העברי של היבואן (2025)'),
 'sources':[
   {'url':CHEV+'elxny4sy/24_chev_traverse_om_he_il_i_il_bh31124_2024feb07_hi_compressed-1.pdf','kind':'importer','note':'ספר נהג שברולט טראוורס 2025, יו.אם.איי (PATAC-localized-Israel), "תכנית תחזוקה" ו-MPVI עמ\' 307-311'},
   LIST_PAGE],
 'status':'reviewed',
 'notes':'הלוח לקוח מספר הנהג העברי של יו.אם.איי לטראוורס 2025 (2.5 טורבו). הפתיח בספר ממליץ על ביקור כל 10,000 ק"מ, אבל טבלת התחזוקה עצמה בנויה על 12,000 ק"מ: סבב צמיגים, ביקורת רב-נקודתית (MPVI), סיכת השלדה, בדיקת השמן ואחוז חיי השמן (החלפה לפי המחוון ולפחות פעם בשנה), מסנן אוויר לפי מחוון חיי המסנן, ומסנן מזגן (או כל 12 חודשים). מצתים כל 90,000 (לא נופל על כפולה של 12,000 ולכן מופיע רק ברשימת הפריטים ארוכי הטווח), בוכנות הגז כל 160,000 או 10 שנים (אין מפתח פריט במאגר), ב-240,000 נוזל קירור (או 6 שנים) ושמן סרן אחורי ב-AWD. נוזל בלמים כל 5 שנים, מייבש המזגן כל 7 שנים.'
}
write(tr25)
