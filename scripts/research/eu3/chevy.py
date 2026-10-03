# Chevrolet (GM Korea / US built) older models from GM US/Canada owner's manuals
# (mirror cdn.dealereprocess.org). Charts "Additional Required Services - Normal", 12,000 km grid.
from gen import *

UMI = 'יו.אם.איי'
CHV = dict(make='Chevrolet', make_he='שברולט', importer=UMI)
MIR = 'https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/'
BLOCK = {'url': 'https://www.chevrolet.co.il/', 'kind': 'importer',
         'note': 'אתר chevrolet.co.il ואתר umigroup.co.il מחזירים Cloudflare 403; ספר עברי או לוח טיפולים של היבואן לא נמצאו'}

# "Tire Rotation and Required Services every 12 000 km" list (same in the 2012-2016 manuals)
REQ = [R('engine_oil', 'לפי מחוון חיי השמן, ולפחות פעם בשנה'), R('oil_filter', 'עם החלפת השמן'),
       ('tire_rotation', 'rotate', None), I('coolant', 'מפלס'), I('washer_fluid'), I('wipers'), I('tires'),
       I('body_underside', 'בדיקה חזותית לדליפות נוזלים'), I('air_filter'), I('brake_pads', 'מערכת הבלמים'),
       I('steering'), I('suspension', 'כולל רכיבי שלדה'), I('seat_belts', 'מערכות ריסון'),
       I('fuel_lines'), I('exhaust', 'כולל מגני חום'), C('door_hinges', 'סיכה של רכיבי מרכב'), I('parking_brake')]

def plan(url, src_note, rows, long, notes, specs=None):
    g = []
    for n in range(1, 21):
        km = 12000 * n
        its = list(REQ)
        for kms, lst in rows:
            if km in kms: its += lst
        g.append((km, its))
    return {
        'interval': {'km': 12000, 'months': 12, 'note': 'לפי ספר הנהג של GM (צפון אמריקה): כל 12,000 ק"מ סבב צמיגים ובדיקות; שמן ומסנן לפי מחוון חיי השמן ולפחות פעם בשנה'},
        'cycle_km': 240000, 'grid': g, 'long': long, 'specs': specs or {},
        'sources': [{'url': url, 'kind': 'manufacturer', 'note': src_note}, BLOCK],
        'status': 'draft',
        'notes': 'הלוח לקוח מספר הנהג האמריקאי של GM, טבלת "שירותים נדרשים - רגיל" (הספר מציג ק"מ במקור). ספר עברי של היבואן לא נמצא. '
                 'מרווח השמן נקבע לפי מחוון חיי השמן של הרכב, ולפחות פעם בשנה; ייתכן שהיבואן בישראל קובע מרווח קבוע אחר. '
                 'בכל 12,000 ק"מ: סבב צמיגים ובדיקות (מפלסים, מגבים, צמיגים, דליפות, מסנן אוויר, בלמים, היגוי ומתלים, מערכות ריסון, דלק ופליטה) וסיכת מרכב. ' + notes,
    }

def every(step, start=None):
    start = start or step
    return tuple(range(start, 240001, step))

K36, K72 = every(36000), every(72000)

def mk(vid, model, mhe, gen_, yrs, engines, p, rules):
    v = dict(CHV, id=vid, model=model, model_he=mhe, generation=gen_, years=yrs, engines=engines, fuel='petrol')
    write(v, p, rules)

# ---------------------------------------------------------------- Spark M300 1.0/1.2
p = plan(MIR + '2014-spark.pdf', '2014 Chevrolet Spark Owner\'s Manual (GM, US/Canada), Maintenance Schedule pp. 11-3 to 11-6 (PDF 305-308), טבלת Normal',
         [(K36, [R('cabin_filter', 'או כל שנתיים')]), (K72, [I('evap_system'), R('air_filter', 'או כל 4 שנים')]),
          ((156000,), [R('spark_plugs'), R('transmission_oil', 'גיר אוטומטי'), I('drive_belt', 'רצועת משאבת מים/אלטרנטור: מתיחה ובלאי')]),
          ((240000,), [R('coolant', 'ניקוז ומילוי, או כל 5 שנים'), I('drive_belt', 'רצועת מדחס המזגן')]),
          (every(48000), [R('brake_fluid', 'נוזל בלמים/מצמד, או כל שנתיים')])],
         [LI('coolant', 'replace', every_km=240000, every_months=60),
          LI('brake_fluid', 'replace', every_km=48000, every_months=24, note='נוזל בלמים ומצמד')],
         'מסנן מזגן כל 36,000 או שנתיים; מסנן אוויר כל 72,000 או 4 שנים; מצתים ושמן גיר אוטומטי ב-156,000; נוזל בלמים/מצמד כל 48,000 או שנתיים; נוזל קירור ב-240,000 או 5 שנים. '
         'בטבלת "שימוש קשה" (נסיעה עירונית צפופה במזג אוויר חם) שמן הגיר האוטומטי מוחלף כל 72,000 ק"מ. '
         'הספר האמריקאי מכסה את מנוע 1.2 (B12D1, בארה"ב LL0); מנוע 1.0 (B10D1) מאותה משפחה נמכר רק מחוץ לצפון אמריקה, והלוח הוחל עליו כדגם אח.')
mk('chevrolet-spark-2010-2015-1.0-1.2', 'Spark', 'ספארק', 'M300', [2010, 2015], ['1.2 (B12D1)', '1.0 (B10D1)'], p,
   [{'names': ['SPARK', 'SPARK LS', 'SPARK LT'], 'years': [2010, 2015], 'engine_codes': ['B12D1', 'B10D1']}])

# ---------------------------------------------------------------- Sonic T300 1.6 / 1.4T
p = plan(MIR + '2014-sonic.pdf', '2014 Chevrolet Sonic Owner\'s Manual (GM, US/Canada), Maintenance Schedule, טבלת Normal (PDF 345-346)',
         [(K36, [R('cabin_filter', 'או כל שנתיים')]), (K72, [I('evap_system'), R('air_filter', 'או כל 4 שנים')]),
          ((156000,), [R('spark_plugs', 'מנוע 1.6 (בספר: 1.8)'), R('transmission_oil', 'גיר אוטומטי'),
                       R('timing_belt', 'מנוע 1.6 (בספר: 1.8): רצועה, גלגל מוביל ומותחן')]),
          ((96000, 192000), [R('spark_plugs', 'מנוע 1.4 טורבו בלבד')]),
          ((240000,), [R('coolant', 'ניקוז ומילוי, או כל 5 שנים'), I('drive_belt', 'או כל 10 שנים'), R('brake_fluid', 'או כל 10 שנים')])],
         [LI('coolant', 'replace', every_km=240000, every_months=60),
          LI('brake_fluid', 'replace', every_km=240000, every_months=120),
          LI('timing_belt', 'replace', every_km=156000, note='רק במנוע 1.6 (F16D4); בספר האמריקאי למנוע 1.8 מאותה משפחה')],
         'מסנן מזגן כל 36,000 או שנתיים; מסנן אוויר כל 72,000 או 4 שנים; מצתים: 1.4 טורבו כל 96,000, 1.6 ב-156,000; רצועת תזמון (1.6) ושמן גיר אוטומטי ב-156,000; '
         'נוזל קירור ב-240,000 או 5 שנים; נוזל בלמים ב-240,000 או 10 שנים. בטבלת שימוש קשה שמן הגיר (אוטומטי וידני) מוחלף כל 72,000. '
         'בספר האמריקאי יש מנועי 1.4 טורבו ו-1.8; לישראל הגיע 1.6 (F16D4) מאותה משפחה עם רצועת תזמון, ונתוני ה-1.8 הוחלו עליו. לא כולל את מנוע 1.4 ללא טורבו (A14XER).')
mk('chevrolet-sonic-2011-2016-1.4t-1.6', 'Sonic', 'סוניק', 'T300', [2011, 2016], ['1.6 (F16D4)', '1.4 טורבו (A14NET)'], p,
   [{'names': ['SONIC', 'SONIC LT', 'SONIC LS'], 'years': [2011, 2016], 'engine_codes': ['F16D4', 'A14NET']}])

# ---------------------------------------------------------------- Malibu 8th gen 2.0T (2013-2015)
p = plan(MIR + '2013-malibu.pdf', '2013 Chevrolet Malibu Owner\'s Manual (GM, US/Canada), Maintenance Schedule, טבלת Normal (PDF 374) והערות (PDF 375)',
         [(K36, [R('cabin_filter', 'או כל שנתיים')]), (K72, [I('evap_system'), R('air_filter', 'או כל 4 שנים')]),
          ((156000,), [R('spark_plugs'), R('transmission_oil', 'גיר אוטומטי')]),
          ((240000,), [R('coolant', 'ניקוז, שטיפה ומילוי, או כל 5 שנים'), I('drive_belt', 'או כל 10 שנים')])],
         [LI('coolant', 'replace', every_km=240000, every_months=60), LI('drive_belt', 'inspect', every_km=240000, every_months=120)],
         'מסנן מזגן כל 36,000 או שנתיים; מסנן אוויר כל 72,000 או 4 שנים; מצתים ושמן גיר אוטומטי ב-156,000; נוזל קירור ב-240,000 או 5 שנים. בטבלה אין החלפה מתוזמנת של נוזל בלמים.')
mk('chevrolet-malibu-2013-2015-2.0-turbo', 'Malibu', 'מאליבו', '8th gen', [2013, 2015], ['2.0 טורבו (LTG)'], p,
   [{'names': ['MALIBU', 'MALIBU LT'], 'years': [2013, 2015], 'engine_codes': ['LTG']}])

# ---------------------------------------------------------------- Malibu 7th gen (2008-2012)
p = plan(MIR + '2012-malibu.pdf', '2012 Chevrolet Malibu Owner\'s Manual (GM, US/Canada), Maintenance Schedule, טבלת Normal (PDF 321) והערות (PDF 322)',
         [(K72, [I('evap_system'), R('air_filter', 'או כל 4 שנים')]),
          ((156000,), [R('spark_plugs'), R('transmission_oil', 'גיר אוטומטי')]),
          ((240000,), [R('coolant', 'ניקוז, שטיפה ומילוי, או כל 5 שנים'), I('drive_belt', 'או כל 10 שנים')])],
         [LI('coolant', 'replace', every_km=240000, every_months=60), LI('drive_belt', 'inspect', every_km=240000, every_months=120)],
         'מסנן אוויר כל 72,000 או 4 שנים; מצתים ושמן גיר אוטומטי ב-156,000; נוזל קירור ב-240,000 או 5 שנים. בטבלת הדגם הזה אין מסנן מזגן ואין החלפה מתוזמנת של נוזל בלמים.')
mk('chevrolet-malibu-2008-2012-2.4', 'Malibu', 'מאליבו', '7th gen', [2008, 2012], ['2.4 (LE5)'], p,
   [{'names': ['MALIBU', 'MALIBU LT'], 'years': [2007, 2012], 'engine_codes': ['11B', '1N9', '1KA', '1N7', 'LE5']}])

# ---------------------------------------------------------------- Captiva Sport 2.4 (LEA)
p = plan(MIR + '2013-captiva.pdf', '2013 Chevrolet Captiva Sport Owner\'s Manual (GM, US/Canada), Maintenance Schedule, טבלת Normal (PDF 319) והערות (PDF 320)',
         [(K36, [R('cabin_filter', 'או כל שנתיים')]), (K72, [I('evap_system'), R('air_filter', 'או כל 4 שנים')]),
          ((156000,), [R('spark_plugs'), R('transmission_oil', 'גיר אוטומטי'), R('transfer_case_oil', 'רק בהנעה כפולה AWD')]),
          ((240000,), [R('coolant', 'ניקוז, שטיפה ומילוי, או כל 5 שנים'), I('drive_belt', 'או כל 10 שנים'), R('brake_fluid', 'או כל 10 שנים')])],
         [LI('coolant', 'replace', every_km=240000, every_months=60), LI('brake_fluid', 'replace', every_km=240000, every_months=120),
          LI('drive_belt', 'inspect', every_km=240000, every_months=120)],
         'מסנן מזגן כל 36,000 או שנתיים; מסנן אוויר כל 72,000 או 4 שנים; מצתים, שמן גיר אוטומטי ושמן תיבת העברה (AWD) ב-156,000; נוזל קירור ב-240,000 או 5 שנים; נוזל בלמים ב-240,000 או 10 שנים.')
mk('chevrolet-captiva-sport-2012-2015-2.4', 'Captiva Sport', 'קפטיבה ספורט', '', [2012, 2015], ['2.4 (LEA)'], p,
   [{'names': ['CAPTIVA SPORT'], 'years': [2012, 2015], 'engine_codes': ['LEA']}])

# ---------------------------------------------------------------- Equinox 2.4 (LEA) 2016-2017
p = plan(MIR + '2016-equinox.pdf', '2016 Chevrolet Equinox Owner\'s Manual (GM, US/Canada), Maintenance Schedule, טבלת Normal (PDF 275) והערות (PDF 276)',
         [(K36, [R('cabin_filter', 'או כל שנתיים')]), (K72, [I('evap_system'), R('air_filter', 'או כל 4 שנים; בתנאי אבק לבדוק בכל החלפת שמן')]),
          ((156000,), [R('spark_plugs'), R('transfer_case_oil', 'רק בהנעה כפולה AWD')]),
          ((240000,), [R('coolant', 'ניקוז ומילוי, או כל 5 שנים'), I('drive_belt', 'או כל 10 שנים')])],
         [LI('coolant', 'replace', every_km=240000, every_months=60), LI('brake_fluid', 'replace', every_months=60),
          LI('drive_belt', 'inspect', every_km=240000, every_months=120)],
         'מסנן מזגן כל 36,000 או שנתיים; מסנן אוויר כל 72,000 או 4 שנים; מצתים ושמן תיבת העברה (AWD) ב-156,000; נוזל קירור ב-240,000 או 5 שנים; נוזל בלמים כל 5 שנים. '
         'בטבלת שימוש קשה שמן הגיר האוטומטי מוחלף כל 72,000 ק"מ.')
mk('chevrolet-equinox-2016-2017-2.4', 'Equinox', 'אקווינוקס', '2nd gen', [2016, 2017], ['2.4 (LEA)'], p,
   [{'names': ['EQUINOX'], 'years': [2016, 2017], 'engine_codes': ['LEA']}])

# ---------------------------------------------------------------- Orlando 1.4 turbo -> Cruze J300 2014 (same platform and engine)
p = plan(MIR + '2014-cruze.pdf', '2014 Chevrolet Cruze Owner\'s Manual (GM, US/Canada), Maintenance Schedule, טבלת Normal (PDF 365) והערות (PDF 366); שורות מנוע 1.4 טורבו',
         [(K36, [R('cabin_filter', 'או כל שנתיים')]), (K72, [I('evap_system'), R('air_filter', 'או כל 4 שנים')]),
          ((96000, 192000), [R('spark_plugs', 'כולל בדיקת מגפי סלילי ההצתה')]),
          ((156000,), [R('transmission_oil', 'גיר אוטומטי')]),
          ((240000,), [R('coolant', 'ניקוז ומילוי, או כל 5 שנים'), I('drive_belt', 'או כל 10 שנים'), R('brake_fluid', 'או כל 10 שנים; גם נוזל מצמד')])],
         [LI('coolant', 'replace', every_km=240000, every_months=60), LI('brake_fluid', 'replace', every_km=240000, every_months=120, note='גם נוזל המצמד'),
          LI('drive_belt', 'inspect', every_km=240000, every_months=120)],
         'אורלנדו לא נמכרה בארה"ב; הלוח לקוח מספר הנהג של שברולט קרוז 2014, שבנויה על אותה פלטפורמה (J300) עם אותו מנוע 1.4 טורבו. '
         'מסנן מזגן כל 36,000 או שנתיים; מסנן אוויר כל 72,000 או 4 שנים; מצתים כל 96,000; שמן גיר אוטומטי ב-156,000; נוזל קירור ב-240,000 או 5 שנים; נוזל בלמים ומצמד ב-240,000 או 10 שנים. '
         'בטבלת שימוש קשה שמן הגיר מוחלף כל 72,000 ק"מ. לא כולל את גרסת הדיזל 2.0.')
mk('chevrolet-orlando-2014-2018-1.4-turbo', 'Orlando', 'אורלנדו', 'J309', [2014, 2018], ['1.4 טורבו (A14NET/B14NET)'], p,
   [{'names': ['ORLANDO'], 'years': [2011, 2018], 'engine_codes': ['A14NET', 'B14NET']}])
