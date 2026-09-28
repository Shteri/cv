from gen import *

UMI = 'יו.אם.איי'
CHV = dict(make='Chevrolet', make_he='שברולט', importer=UMI)
MIR = 'https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/'

REQ = [R('engine_oil', 'לפי מחוון חיי השמן, ולפחות פעם בשנה'), R('oil_filter'), ('tire_rotation', 'rotate', None),
       I('coolant', 'מפלס'), I('brake_fluid', 'מפלס'), I('washer_fluid'), I('brake_pads'), I('brake_discs'), I('brake_lines'),
       I('steering'), I('suspension'), I('cv_boots'), I('fuel_lines'), I('exhaust'), I('parking_brake'),
       I('seat_belts', 'מערכות ריסון'), C('door_hinges', 'סיכה של רכיבי מרכב')]

def gm_plan(url, note_src, cabin=36000, evap=True, air=72000, plugs=(), extra=None, coolant_months=60,
            brake_months=60, brake_km=None, wipers=True, notes='', specs=None, air_life=False, long_extra=None):
    g = []
    for n in range(1, 21):
        km = 12000 * n
        its = list(REQ)
        if cabin and km % cabin == 0: its.append(R('cabin_filter', 'או כל שנתיים'))
        if evap and km % 72000 == 0: its.append(I('evap_system'))
        if air and km % air == 0: its.append(R('air_filter', 'או כל 4 שנים; באבק לבדוק בכל החלפת שמן'))
        if air_life: its.append(I('air_filter', 'לפי מחוון חיי המסנן; החלפה לפי הצורך'))
        if km in plugs: its.append(R('spark_plugs'))
        if wipers and km % 24000 == 0: its.append(R('wipers', 'או כל 12 חודשים'))
        if km == 240000: its += [R('coolant', 'ניקוז ומילוי, או כל %d שנים' % (coolant_months // 12)), I('drive_belt', 'או כל 10 שנים')]
        for k, lst in (extra or {}).items():
            if km in (k if isinstance(k, tuple) else (k,)): its += lst
        g.append((km, its))
    long = [LI('coolant', 'replace', every_km=240000, every_months=coolant_months),
            LI('drive_belt', 'inspect', every_km=240000, every_months=120)]
    if brake_months:
        long.append(LI('brake_fluid', 'replace', every_months=brake_months, **({'every_km': brake_km} if brake_km else {})))
    long += long_extra or []
    return {
        'interval': {'km': 12000, 'months': 12, 'note': 'לפי ספר הנהג של GM (צפון אמריקה): כל 12,000 ק"מ סבב צמיגים ובדיקות; שמן ומסנן לפי מחוון חיי השמן ולפחות פעם בשנה'},
        'cycle_km': 240000, 'grid': g, 'long': long, 'specs': specs or {},
        'sources': [{'url': url, 'kind': 'other', 'note': note_src}],
        'status': 'draft',
        'notes': 'הלוח לקוח מספר הנהג האמריקאי של GM (עמודות ק"מ ומייל; הספר מציג ק"מ במקור). ספר עברי של היבואן לא נמצא: אתר chevrolet.co.il ואתר יו.אם.איי חסומים (Cloudflare 403). מרווח השמן נקבע לפי מחוון חיי השמן של הרכב, ולפחות פעם בשנה; ייתכן שהיבואן בישראל קובע מרווח קבוע אחר. ' + notes,
    }

def mk(vid, model, mhe, gen_, yrs, engines, plan, names, codes=None, fuel='petrol'):
    v = dict(CHV, id=vid, model=model, model_he=mhe, generation=gen_, years=yrs, engines=engines, fuel=fuel)
    r = {'names': names, 'years': yrs}
    if codes: r['engine_codes'] = codes
    write(v, plan, [r])

# Spark M400 1.4 (LV7)
p = gm_plan(MIR + '2019-spark.pdf', '2019 Chevrolet Spark Owner\'s Manual (GM, US/Canada), Maintenance Schedule pp. 290-294; mirror of chevrolet.com owner-center PDF',
            plugs=(156000,), brake_months=36,
            extra={156000: [R('manual_gearbox_oil', 'גיר ידני')]},
            specs={'oil_capacity': '3.5 ליטר כולל מסנן', 'coolant': '4.8 ליטר', 'fuel': 'מיכל 35 ליטר'},
            notes='מסנן מזגן כל 36,000 (או שנתיים), מסנן אוויר כל 72,000 (או 4 שנים), מצתים ב-156,000, נוזל קירור 240,000 או 5 שנים, נוזל בלמים כל 3 שנים, להבי מגבים כל 24,000 או שנה. למנוע אין רצועת תזמון להחלפה בלוח.')
p['sources'].append({'url': 'https://www.chevrolet.com/ownercenter/content/dam/gmownercenter/gmna/dynamic/manuals/2019/Chevrolet/Spark/2019-chevrolet-spark-owners-manual.pdf', 'kind': 'manufacturer', 'note': 'אותו ספר באתר GM'})
mk('chevrolet-spark-2016-2022-1.4', 'Spark', 'ספארק', 'M400', [2016, 2023], ['1.4 (LV7)'], p, ['SPARK'], ['LV7'])

# Trax 1.4 turbo 2013-2019
p = gm_plan(MIR + '2017-trax.pdf', '2017 Chevrolet Trax Owner\'s Manual (GM, US/Canada), Maintenance Schedule p. 325 (2018 edition identical)',
            plugs=(96000, 192000), extra={156000: [R('transfer_case_oil', 'רק בהנעה כפולה AWD')]},
            notes='מנוע 1.4 טורבו: מצתים כל 96,000; מסנן מזגן 36,000/שנתיים; מסנן אוויר 72,000/4 שנים; נוזל קירור 240,000 או 5 שנים; נוזל בלמים כל 5 שנים.')
mk('chevrolet-trax-2013-2020-1.4-turbo', 'Trax', 'טראקס', 'U200', [2013, 2020], ['1.4 טורבו (A14NET/B14NET)'], p, ['TRAX'], ['A14NET', 'B14NET'])

# Trax 2024 1.2 turbo LIH
p = gm_plan(MIR + '2024-trax.pdf', '2024 Chevrolet Trax Owner\'s Manual (GM, US/Canada), Maintenance Schedule pp. 287-290',
            cabin=36000, evap=False, air=None, air_life=True, plugs=(96000, 192000), coolant_months=72, wipers=False,
            extra={240000: [R('timing_belt', 'יחד עם המותחן ומשאבת השמן')]},
            notes='מנוע 1.2 טורבו (LIH): מסנן אוויר לפי מחוון חיי המסנן, מסנן מזגן 36,000/שנתיים, מצתים כל 96,000, נוזל קירור ורצועת תזמון עם משאבת שמן ב-240,000 (נוזל קירור או 6 שנים), נוזל בלמים כל 5 שנים.')
mk('chevrolet-trax-2023-2026-1.2-turbo', 'Trax', 'טראקס', '2nd gen', [2023, 2026], ['1.2 טורבו (LIH)'], p, ['TRAX'], ['LIH'])

# Trailblazer 2021+ 1.3 turbo
p = gm_plan(MIR + '2022-trailblazer.pdf', '2022 Chevrolet Trailblazer Owner\'s Manual (GM, US/Canada), Maintenance Schedule pp. 322-323',
            evap=False, air=None, air_life=True, plugs=(96000, 192000),
            extra={240000: [R('differential_oil', 'סרן אחורי, רק ב-AWD')]},
            notes='מנוע 1.3 טורבו: מסנן אוויר לפי מחוון (או 4 שנים), מסנן מזגן 36,000/שנתיים, מצתים כל 96,000, נוזל קירור 240,000 או 5 שנים, נוזל בלמים כל 5 שנים. בגרסת 1.2 (LIH) הספר מוסיף החלפת רצועת תזמון ורצועת משאבת שמן ב-240,000 ק"מ.')
mk('chevrolet-trailblazer-2021-2026-1.3-turbo', 'Trailblazer', 'טרייל בלייזר', '', [2021, 2026], ['1.3 טורבו (L3T)'], p, ['TRAIL BLAZER', 'TRAILBLAZER'], ['L3T'])

# Equinox 2018-2023 1.5T
p = gm_plan(MIR + '2020-equinox.pdf', '2020 Chevrolet Equinox Owner\'s Manual (GM, US/Canada), Maintenance Schedule pp. 362-364',
            plugs=(96000, 192000), extra={240000: [R('differential_oil', 'שמן סרן אחורי / תיבת העברה, רק ב-AWD')]},
            notes='מנוע 1.5 טורבו: מצתים כל 96,000; מסנן מזגן 36,000/שנתיים; מסנן אוויר 72,000/4 שנים; נוזל קירור 240,000 או 5 שנים; נוזל בלמים כל 5 שנים.')
mk('chevrolet-equinox-2018-2023-1.5-turbo', 'Equinox', 'אקווינוקס', '3rd gen', [2017, 2023], ['1.5 טורבו (LYX)'], p, ['EQUINOX'], ['LYX'])

# Traverse 2018+ 3.6
p = gm_plan(MIR + '2019-traverse.pdf', '2019 Chevrolet Traverse Owner\'s Manual (GM, US/Canada), Maintenance Schedule pp. 373-375',
            plugs=(156000,), notes='מנוע 3.6 V6: מצתים ב-156,000; מסנן מזגן 36,000/שנתיים; מסנן אוויר 72,000/4 שנים; נוזל קירור 240,000 או 5 שנים; נוזל בלמים כל 5 שנים.')
mk('chevrolet-traverse-2018-2026-3.6', 'Traverse', 'טראוורס', 'C1XX', [2018, 2026], ['3.6 V6 (LFY)'], p, ['TRAVERSE'], ['LFY'])

# Traverse 2009-2017 3.6 LLT
p = gm_plan(MIR + '2016-traverse.pdf', '2016 Chevrolet Traverse Owner\'s Manual (GM, US/Canada), Maintenance Schedule pp. 345-347',
            plugs=(156000,), brake_months=36, wipers=False,
            extra={156000: [R('transfer_case_oil', 'רק ב-AWD')], (72000, 144000, 216000): [R('brake_fluid', 'או כל 3 שנים')]},
            notes='מנוע 3.6 V6: מצתים ב-156,000; מסנן מזגן 36,000/שנתיים; מסנן אוויר 72,000/4 שנים; נוזל בלמים כל 72,000 או 3 שנים; נוזל קירור 240,000 או 5 שנים.')
mk('chevrolet-traverse-2009-2017-3.6', 'Traverse', 'טראוורס', 'GMT967', [2009, 2017], ['3.6 V6 (LLT)'], p, ['TRAVERSE'], ['LLT'])

# Malibu 2016-2023 1.5T / 2.0T
p = gm_plan('x', 'x', plugs=(96000, 192000), wipers=False,
            notes='מנועי 1.5 ו-2.0 טורבו: מצתים כל 96,000; מסנן מזגן 36,000/שנתיים; מסנן אוויר 72,000/4 שנים; נוזל קירור 240,000 או 5 שנים; נוזל בלמים כל 5 שנים.')
p['sources'] = [{'url': 'https://www.chevrolet.com/ownercenter/content/dam/gmownercenter/gmna/dynamic/manuals/2018/Chevrolet/Malibu/2018-chevrolet-malibu-owners-manual.pdf', 'kind': 'manufacturer', 'note': '2018 Chevrolet Malibu Owner\'s Manual (GM, US/Canada), Maintenance Schedule pp. 369-370'}]
mk('chevrolet-malibu-2016-2023-1.5-2.0-turbo', 'Malibu', 'מאליבו', '9th gen', [2016, 2023], ['1.5 טורבו (LFV)', '2.0 טורבו (LTG)'], p, ['MALIBU', 'MALIBU LT'], ['LFV', 'LTG'])

# Cruze J300 (Korea) 1.4T / 1.6 / 1.8
p = gm_plan(MIR + '2014-cruze.pdf', '2014 Chevrolet Cruze Owner\'s Manual (GM, US/Canada), Maintenance Schedule pp. 364-366',
            wipers=False, brake_months=120, brake_km=240000, plugs=(),
            extra={(96000, 192000): [R('spark_plugs', 'מנוע 1.4 טורבו')],
                   156000: [R('spark_plugs', 'מנוע 1.8 (ו-1.6)'), R('transmission_oil', 'גיר אוטומטי, מנועי 1.4 ו-1.8')]},
            long_extra=[LI('timing_belt', 'replace', every_km=156000, every_months=120, note='רק במנועי 1.6/1.8: רצועה, גלגל מוביל, מותחן ומשאבת מים')],
            notes='בספר האמריקאי מנוע 1.4 טורבו ומנוע 1.8; לישראל הגיע גם 1.6 (F16D4) מאותה משפחה עם רצועת תזמון, והנתונים של ה-1.8 הוחלו עליו. מצתים: 1.4 טורבו כל 96,000, 1.8 ב-156,000. רצועת תזמון (1.6/1.8) ב-156,000 או 10 שנים. נוזל בלמים ב-240,000 או 10 שנים. נוזל קירור 240,000 או 5 שנים.')
mk('chevrolet-cruze-2009-2016-1.4-1.6-1.8', 'Cruze', 'קרוז', 'J300', [2009, 2016], ['1.4 טורבו (A14NET/B14NET)', '1.6 (F16D4)', '1.8 (F18D4)'], p,
   ['CRUZE', 'CRUZE 1.6 LS', 'CRUZE I.6 LS', 'CRUZE 1.8 LT', 'CRUZE 1.6 LT', 'CRUZE 1.6 L.S'])
# Trax 1.8 F18D4 -> Cruze plan
p2 = copy.deepcopy(p)
p2['notes'] = 'טראקס עם מנוע 1.8 (F18D4) לא נמכר בצפון אמריקה, ולכן נלקח הלוח של שברולט קרוז 2014 שבו אותו מנוע 1.8. ' + p['notes']
mk('chevrolet-trax-2013-2016-1.8', 'Trax', 'טראקס', 'U200', [2013, 2016], ['1.8 (F18D4)'], p2, ['TRAX'], ['F18D4'])

# Cruze 2017-2019 1.4T (Mexico)
p = gm_plan(MIR + '2018-cruze.pdf', '2018 Chevrolet Cruze Owner\'s Manual (GM, US/Canada), Maintenance Schedule pp. 353-354',
            plugs=(96000, 192000), wipers=False,
            notes='מנוע 1.4 טורבו: מצתים כל 96,000; מסנן מזגן 36,000/שנתיים; מסנן אוויר 72,000/4 שנים; נוזל קירור 240,000 או 5 שנים; נוזל בלמים כל 5 שנים.')
mk('chevrolet-cruze-2017-2019-1.4-turbo', 'Cruze', 'קרוז', 'J400', [2017, 2019], ['1.4 טורבו (LE2)'], p, ['CRUZE'], ['LE2'])

# Impala 2014-2019 3.6
p = gm_plan(MIR + '2016-impala.pdf', '2016 Chevrolet Impala Owner\'s Manual (GM, US/Canada), Maintenance Schedule pp. 328-329',
            plugs=(156000,), wipers=False, brake_months=0,
            extra={(72000, 144000, 216000): [R('brake_fluid')]},
            notes='מנוע 3.6 V6: מצתים ב-156,000; מסנן מזגן 36,000/שנתיים; מסנן אוויר 72,000/4 שנים; נוזל בלמים כל 72,000; נוזל קירור 240,000 או 5 שנים.')
mk('chevrolet-impala-2014-2020-3.6', 'Impala', 'אימפלה', '10th gen', [2014, 2020], ['3.6 V6 (LFX)'], p, ['IMPALA', 'IMPALA LTZ', 'IMPALA LT'], ['LFX'])

# Blazer 2019+
p = gm_plan(MIR + '2021-blazer.pdf', '2021 Chevrolet Blazer Owner\'s Manual (GM, US/Canada), Maintenance Schedule pp. 334-335',
            evap=False, air=None, air_life=True,
            extra={(96000, 192000): [R('spark_plugs', 'מנוע 2.0 טורבו')], 156000: [R('spark_plugs', 'מנוע 3.6')],
                   240000: [R('differential_oil', 'סרן אחורי, רק ב-AWD')]},
            notes='מצתים: 2.0 טורבו כל 96,000, 3.6 ב-156,000. מסנן אוויר לפי מחוון (או 4 שנים), מסנן מזגן 36,000/שנתיים, נוזל קירור 240,000 או 5 שנים, נוזל בלמים כל 5 שנים.')
mk('chevrolet-blazer-2019-2024-2.0-3.6', 'Blazer', 'בלייזר', '3rd gen', [2019, 2024], ['2.0 טורבו (LSY)', '3.6 V6 (LGX)'], p, ['BLAZER'], ['LSY', 'LGX'])
