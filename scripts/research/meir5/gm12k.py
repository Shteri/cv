from common import *
from gmk12 import LIST_PAGE
# ---------- Trax 2024 (LIH), Israeli book 2024: text schedule, 12,000 km ----------
def trax_svc(km):
    it=[I('tire_rotation','rotate'),
        I('engine_oil','replace','לפי מחוון חיי השמן (בדיקה בכל 12,000 ק"מ), ולפחות פעם בשנה'),
        I('oil_filter','replace','יחד עם השמן'),
        I('air_filter','inspect','לפי מחוון חיי מסנן האוויר; מחליפים כשמוצגת הודעה'),
        I('door_hinges','clean','סיכת רכיבי המרכב')]
    if km%36000==0: it.append(I('cabin_filter','replace','או כל 24 חודשים'))
    if km%96000==0: it.append(I('spark_plugs','replace','כולל בדיקת מוליכי המצתים'))
    return {'km':km,'items':it}
trax24={
 'id':'chevrolet-trax-2023-2026-1.2-turbo','make':'Chevrolet','make_he':'שברולט','model':'Trax','model_he':'טראקס',
 'generation':'2nd gen','years':[2023,2026],'engines':['1.2 טורבו (LIH)'],'fuel':'petrol','importer':'יו.אם.איי',
 'interval':{'km':12000,'months':12,'note':'לפי ספר הנהג העברי של יו.אם.איי: סבב צמיגים ובדיקת חיי השמן כל 12,000 ק"מ; שמן ומסנן לפי מחוון חיי השמן ולפחות פעם בשנה'},
 'cycle_km':288000,
 'services':[trax_svc(k) for k in range(12000,288001,12000)],
 'long_interval':[
   L('cabin_filter','replace', every_km=36000, every_months=24),
   L('spark_plugs','replace', every_km=96000),
   L('coolant','replace','ריקון ומילוי מערכת הקירור', every_km=240000, every_months=72),
   L('timing_belt','replace','רצועת התזמון ורצועת הינע משאבת השמן', every_km=240000, every_months=180),
   L('transmission_oil','replace','שמן ומסנן גיר אוטומטי, רק בשימוש מאומץ (שטח, גרירה וכד\')', every_km=70000),
   L('brake_fluid','replace', every_months=24),
 ],
 'time_based':[
   T('engine_oil','replace',12,'לפחות פעם בשנה, גם אם המחוון לא הורה'),
   T('brake_fluid','replace',24,'כל שנתיים'),
   T('ac_system','replace',84,'החלפת שקית חומר הייבוש של המזגן כל 7 שנים'),
 ],
 'specs':{'engine_oil':'שמן במפרט dexos1 (מומלץ סינתטי מלא), בצמיגות לפי הספר',
          'coolant':'DEX-COOL מהול 50/50 במים נקיים','brake_fluid':'DOT 4',
          '_note':'נבדק מול ספר הנהג העברי של היבואן (2024)'},
 'sources':[
   {'url':CHEV+'p20bi13a/24_chev_trax_om_he_il_i_il_2023mar06_hi_rvsd_2023apr05_compressed.pdf','kind':'importer','note':'ספר נהג שברולט טראקס 2024, יו.אם.איי (GMK-Localizing-Israel), "תכנית תחזוקה" עמ\' 273-276, נוזלים עמ\' 279'},
   LIST_PAGE],
 'status':'reviewed',
 'notes':'הלוח לקוח מספר הנהג העברי של יו.אם.איי לטראקס 2024 (מנוע 1.2 טורבו). בספר אין טבלה אלא רשימת מרווחים: כל 12,000 ק"מ סבב צמיגים, בדיקת מפלס השמן ואחוז חיי השמן וסיכת המרכב; שמן ומסנן לפי המחוון ולפחות פעם בשנה; מסנן אוויר לפי מחוון חיי המסנן; מסנן מזגן כל 36,000 או שנתיים; מצתים כל 96,000; בוכנות הגז של הדלת האחורית כל 161,000 או 10 שנים (אין לזה מפתח פריט במאגר); נוזל קירור וגם רצועת התזמון ורצועת משאבת השמן כל 240,000 (6 או 15 שנים בהתאמה); נוזל בלמים כל שנתיים; מייבש המזגן כל 7 שנים. שמן גיר מוחלף רק בשימוש מאומץ (כל 70,000). המחזור כאן הוא 288,000 כדי שמסנן המזגן והמצתים ייפלו על אותם טיפולים.'
}
write(trax24)

# ---------- Trailblazer 2021-2026 (L3T), Israeli book 2021 chart ----------
def tb_svc(km):
    it=[I('tire_rotation','rotate'),
        I('engine_oil','replace','לפי מחוון חיי השמן, ולפחות פעם בשנה'), I('oil_filter','replace'),
        I('air_filter','inspect','לפי מחוון חיי מסנן האוויר, אם קיים'),
        I('coolant','inspect','מפלס'), I('washer_fluid','inspect','מפלס'),
        I('tires','inspect','לחץ ושחיקה'),
        I('body_underside','inspect','בדיקה חזותית לאיתור נזילות'),
        I('brake_pads','inspect'), I('brake_discs','inspect'), I('brake_lines','inspect'),
        I('steering','inspect','כולל הגה כוח; לפחות פעם בשנה'), I('suspension','inspect','לפחות פעם בשנה'),
        I('cv_boots','inspect','חצאי סרנים וגלי הינע'),
        I('seat_belts','inspect','רכיבי מערכת הריסון'),
        I('fuel_lines','inspect'), I('exhaust','inspect','כולל מגני חום'),
        I('door_hinges','clean','סיכת רכיבי המרכב'),
        I('parking_brake','inspect','כולל מנגנון מצב P'),
        I('pedals','inspect','דוושת ההאצה'),
    ]
    if km%24000==0: it.append(I('wipers','replace','או כל 12 חודשים'))
    if km%36000==0: it.append(I('cabin_filter','replace','או כל שנתיים'))
    if km%72000==0: it += [I('evap_system','inspect','צנרת הדלק והאדים'), I('air_filter','replace','רק ברכב ללא מחוון חיי מסנן האוויר; או כל 4 שנים')]
    if km%96000==0: it.append(I('spark_plugs','replace','כולל בדיקת חוטי המצתים'))
    if km==240000: it += [I('differential_oil','replace','סרן אחורי, ב-AWD בלבד'), I('coolant','replace','או כל 5 שנים'), I('drive_belt','inspect','או כל 10 שנים')]
    return {'km':km,'items':it}
tb={
 'id':'chevrolet-trailblazer-2021-2026-1.3-turbo','make':'Chevrolet','make_he':'שברולט','model':'Trailblazer','model_he':'טרייל בלייזר',
'years':[2021,2026],'engines':['1.3 טורבו (L3T)'],'fuel':'petrol','importer':'יו.אם.איי',
 'interval':{'km':12000,'months':12,'note':'לפי ספר הנהג העברי של יו.אם.איי: סבב צמיגים ובדיקות כל 12,000 ק"מ; שמן ומסנן לפי מחוון חיי השמן ולפחות פעם בשנה'},
 'cycle_km':240000,
 'services':[tb_svc(k) for k in range(12000,240001,12000)],
 'long_interval':[
   L('brake_fluid','replace', every_months=24),
   L('coolant','replace', every_km=240000, every_months=60),
   L('drive_belt','inspect','בדיקה חזותית; החלפה לפי הצורך', every_km=240000, every_months=120),
   L('transmission_oil','replace','תנאים קשים בלבד (פקקים בחום, הרים, גרירה, מונית): גיר 9 הילוכים, או שמן ומסנן בגיר CVT', every_km=72000),
   L('differential_oil','replace','סרן אחורי ב-AWD, תנאים קשים', every_km=120000),
 ],
 'time_based':[
   T('engine_oil','replace',12,'לפחות פעם בשנה, גם אם המחוון לא הורה'),
   T('brake_fluid','replace',24,'כל שנתיים'),
   T('ac_system','replace',84,'החלפת שקית חומר הייבוש של המזגן כל 7 שנים'),
 ],
 'specs':{'_note':'נבדק מול ספר הנהג העברי של היבואן (2021)'},
 'sources':[
   {'url':CHEV+'rpsdjbkl/טרייל-בלייזר-2021.pdf','kind':'importer','note':'ספר נהג שברולט טרייל בלייזר 2021, יו.אם.איי (GMK-Localizing-NonEU/Israel), "תכנית תחזוקה" עמ\' 306-312: טבלאות שימוש רגיל (עמ\' 309-310) ותנאים קשים (עמ\' 311-312)'},
   {'url':CHEV+'djtfp4dj/24_chev_trailblazer_om_he_il_i_il_308bh24_2023jun02_hi_compressed.pdf','kind':'importer','note':'ספר נהג טרייל בלייזר 2024, עמ\' 265-268 (רשימת מרווחים בלי טבלה)'},
   LIST_PAGE],
 'status':'reviewed',
 'notes':'הלוח לקוח מטבלת "שימוש רגיל" בספר הנהג העברי של יו.אם.איי לטרייל בלייזר 2021 (עמודות של 12,000 ק"מ עד 240,000). בכל עמודה: סבב צמיגים, בדיקת השמן ואחוז חיי השמן והחלפה לפי הצורך, ובדיקות כלליות (נוזלים, צמיגים, בלמים, היגוי ומתלים, הינע, ריסון, דלק ופליטה, בלם חניה, דוושה) וסיכת המרכב. מגבים כל 24,000 או שנה, מסנן מזגן כל 36,000 או שנתיים, מצתים כל 96,000, נוזל קירור כל 240,000 או 5 שנים, נוזל בלמים כל שנתיים, מייבש המזגן כל 7 שנים. בוכנות הגז של מכסה המנוע/הדלת האחורית מסומנות להחלפה ב-120,000 וב-240,000 (או 10 שנים) ואין להן מפתח פריט במאגר. ספר 2024 (בלי טבלה) מציין: נוזל קירור כל 240,000 או 6 שנים, בוכנות הגז כל 161,000, ושמן גיר רק בשימוש מאומץ כל 70,000.'
}
write(tb)
