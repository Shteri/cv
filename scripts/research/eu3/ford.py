# Ford (Delek Motors) one-page Hebrew service plans for Edge / Explorer / Ranger / Bronco.
# Page https://www.ford.co.il/תוכנית-טיפול/שירות embeds var data with SharePoint links (two-step cookie download).
from gen import *

FORD = dict(make='Ford', make_he='פורד', importer='דלק מוטורס')
PAGE = {'url': 'https://www.ford.co.il/תוכנית-טיפול/שירות', 'kind': 'importer',
        'note': 'דף תוכניות הטיפול של דלק מוטורס; קישורי ה-PDF לכל דגם נמצאים במשתנה data בדף'}
SP = 'https://delekmotorscoil.sharepoint.com/:b:/s/Techtrain/'
URLS = {
    'Edge_2008_2010': SP + 'EQ7bSpD0v15KpT0-zZbF0uIBU5OFf_cgHCOUh0z6RWFx5g?download=1',
    'Edge_2011_2014': SP + 'EaEwy2zeqdNLsHhm6nXqdWABWi-_D3RtxR0zUOIE7VLvLA?download=1',
    'Edge_2015_2018': SP + 'Ef4jn7gRNOZKhVxJhdOs0XEBD03uaHWVTosGiz0hR9bwJw?download=1',
    'Edge_2019_And_Up': SP + 'EVZn_ej1o-ZPm05rSHjOtjcBZWM09-vkPEAg7VKe4aXiJA?download=1',
    'Explorer_2011_2014': SP + 'ETT2AdzowURFjGqdDS3TBh4BxPzPrFc_CaL1nWoqENRztA?download=1',
    'Explorer_2015_2018': SP + 'EbZsbgRC-zRLvxAFs9LNYwAB33wp0lNs3rpwLSIIXW0glQ?download=1',
    'Explorer_2020_And_Up': SP + 'EX-NvTIFF9RNpKXz0fce6qwBCpdaYi9tstN50ORIIbimOQ?download=1',
    'Ranger_Diesel_2023_And_Up': SP + 'EYv1xArxEvROph7WazGGsN8BKDOm4Mi06hUva00DQHoZZA?download=1',
    'Bronco_2021_And_Up': SP + 'EeeszIXEYoBJri8cGbLAAa4B_AOr9gymv6RSWw6lQU-5NA?download=1',
}

def src(key, header):
    return [{'url': URLS[key], 'kind': 'importer', 'note': f'PDF תוכנית טיפול Ford_{key}.pdf של דלק מוטורס (עמוד אחד: פריט ומרווח). {header}'}, PAGE]

def fplan(key, header, step, n, every, rows, long, notes, specs, oil_note):
    g = []
    for k in range(1, n + 1):
        km = step * k
        its = [R('engine_oil', oil_note), R('oil_filter')] + list(every)
        for mult, lst in rows:
            if km % mult == 0: its += lst
        g.append((km, its))
    return {'interval': {'km': step, 'months': 24 if key.startswith('Ranger') else (6 if key == 'Edge_2008_2010' else 12),
                         'note': header},
            'cycle_km': step * n, 'grid': g, 'long': long, 'specs': specs,
            'sources': src(key, header), 'status': 'reviewed',
            'notes': 'הלוח מתוכנית הטיפול הרשמית של היבואן דלק מוטורס (עמוד אחד: פריט ומרווח). התוכנית לא מפרטת בדיקות שגרה, ולכן מופיעים רק הפריטים שבה. ' + notes}

def coolant_long(first_km, first_m, then_km, then_m):
    return LI('coolant', 'replace', first_km=first_km, first_months=first_m, then_every_km=then_km, then_every_months=then_m)

# ---------------------------------------------------------------- Edge
p = fplan('Edge_2008_2010', 'טיפול כל 10,000 ק"מ או 6 חודשים (מנוע 3.5 בנזין, שנות ייצור 2008-2011)', 10000, 12,
          [R('cabin_filter', 'כל 10,000 ק"מ או 6 חודשים')], [(40000, [R('air_filter')])],
          [coolant_long(160000, 72, 80000, 36), LI('fuel_filter', 'replace', every_km=150000, every_months=96),
           LI('spark_plugs', 'replace', every_km=120000, every_months=48), LI('transfer_case_oil', 'replace', every_km=45000, every_months=36),
           LI('differential_oil', 'replace', every_km=240000, note='סרן אחורי'), LI('pcv_valve', 'replace', every_km=160000)],
          'שמן ומסנן ומסנן מזגן כל 10,000 ק"מ או 6 חודשים; מסנן אוויר כל 40,000; מצתים 120,000 או 4 שנים; מסנן דלק 150,000 או 8 שנים; שמן תיבת העברה 45,000 או 3 שנים; שמן סרן אחורי 240,000; שסתום PCV ב-160,000; נוזל קירור לראשונה ב-160,000 או 6 שנים ואחר כך כל 80,000 או 3 שנים.',
          {'engine_oil': '5W-30 במפרט Ford WSS-M2C971-A1', 'coolant': 'צהוב, מפרט WSS-M97B57-A2', 'brake_fluid': 'DOT 4 Low Viscosity',
           '_note': 'גיר אוטומטי Mercon LV; תיבת העברה 75W-140; סרן אחורי 80W-90 (לפי התוכנית)'}, 'כל 10,000 ק"מ או 6 חודשים')
write({**FORD, 'id': 'ford-edge-2008-2010-3.5', 'model': 'Edge', 'model_he': "אדג'", 'generation': '1st gen', 'years': [2008, 2010],
       'engines': ['3.5 V6 בנזין'], 'fuel': 'petrol'}, p, [{'names': ['EDGE'], 'years': [2007, 2010]}])

p = fplan('Edge_2011_2014', 'טיפול כל 15,000 ק"מ או 12 חודשים (מנועי בנזין 2.0/3.5, שנות ייצור 2011-2014)', 15000, 8,
          [], [(30000, [R('cabin_filter')]), (45000, [R('air_filter')])],
          [coolant_long(160000, 72, 80000, 36), LI('spark_plugs', 'replace', every_km=160000),
           LI('differential_oil', 'replace', every_km=240000, note='סרן אחורי')],
          'שמן ומסנן כל 15,000 ק"מ או שנה; מסנן מזגן כל 30,000; מסנן אוויר כל 45,000; מצתים 160,000; שמן סרן אחורי 240,000; נוזל קירור לראשונה ב-160,000 או 6 שנים ואחר כך כל 80,000 או 3 שנים.',
          {'engine_oil': '3.5: 5W-20 (WSS-M2C970-A1); 2.0: 5W-30 (WSS-M2C971-A1)', 'coolant': 'צהוב, מפרט WSS-M97B57-A2', 'brake_fluid': 'DOT 4 Low Viscosity'},
          'כל 15,000 ק"מ או 12 חודשים')
write({**FORD, 'id': 'ford-edge-2011-2014-2.0-3.5', 'model': 'Edge', 'model_he': "אדג'", 'generation': '1st gen facelift', 'years': [2011, 2014],
       'engines': ['2.0 בנזין', '3.5 V6'], 'fuel': 'petrol'}, p, [{'names': ['EDGE'], 'years': [2011, 2014]}])

p = fplan('Edge_2015_2018', 'טיפול כשמופיעה הודעה בלוח השעונים, או 15,000 ק"מ או 12 חודשים (מנועי בנזין 2.0/3.5, שנות ייצור 2015-2018)', 15000, 6,
          [], [(30000, [R('cabin_filter')]), (45000, [R('air_filter', 'אם לא הוחלף קודם'), R('transfer_case_oil')])],
          [coolant_long(160000, 72, 80000, 36), LI('spark_plugs', 'replace', every_km=150000),
           LI('transmission_oil', 'replace', every_km=240000)],
          'שמן ומסנן לפי הודעה בלוח השעונים או כל 15,000 ק"מ או שנה; מסנן מזגן כל 30,000; מסנן אוויר ושמן תיבת העברה כל 45,000; מצתים 150,000; שמן גיר 240,000; נוזל קירור לראשונה ב-160,000 או 6 שנים ואחר כך כל 80,000 או 3 שנים.',
          {'engine_oil': '3.5: 5W-20 (WSS-M2C970-A1); 2.0: 5W-30 (WSS-M2C971-A1)', 'coolant': 'צהוב, מפרט WSS-M97B57-A2', 'brake_fluid': 'DOT 4 Low Viscosity'},
          'לפי הודעה בלוח השעונים, או 15,000 ק"מ או 12 חודשים')
write({**FORD, 'id': 'ford-edge-2015-2018-2.0-3.5', 'model': 'Edge', 'model_he': "אדג'", 'generation': '2nd gen', 'years': [2015, 2018],
       'engines': ['2.0 בנזין', '3.5 V6'], 'fuel': 'petrol'}, p,
      [{'names': ['EDGE', 'EDGE TITANIUM', 'EDGE-TITANIUM', 'EDGE-SEL', 'EDGE SEL'], 'years': [2015, 2018]}])

p = fplan('Edge_2019_And_Up', 'טיפול כשמופיעה הודעה בלוח השעונים, או 16,000 ק"מ או 12 חודשים (מנועי בנזין 2.0/2.7, משנת ייצור 2019)', 16000, 6,
          [], [(32000, [R('cabin_filter')]), (48000, [R('air_filter')])],
          [coolant_long(320000, 120, 160000, 60), LI('spark_plugs', 'replace', every_km=160000),
           LI('transmission_oil', 'replace', every_km=240000),
           LI('drive_belt', 'inspect', first_km=160000, then_every_km=16000, note='בדיקה לראשונה ב-160,000 ובכל טיפול אחר כך; החלפה לפי הצורך'),
           LI('drive_belt', 'replace', every_km=240000, note='אם לא הוחלפה קודם')],
          'שמן ומסנן לפי הודעה בלוח השעונים או כל 16,000 ק"מ או שנה; מסנן מזגן כל 32,000; מסנן אוויר כל 48,000; מצתים 160,000; שמן גיר 240,000; רצועת אביזרים: בדיקה מ-160,000 והחלפה עד 240,000; נוזל קירור לראשונה ב-320,000 או 10 שנים ואחר כך כל 160,000 או 5 שנים.',
          {'engine_oil': '5W-30 (WSS-M2C971-A1)', 'coolant': 'צהוב, מפרט WSS-M97B57-A2', 'brake_fluid': 'DOT 4 Low Viscosity'},
          'לפי הודעה בלוח השעונים, או 16,000 ק"מ או 12 חודשים')
write({**FORD, 'id': 'ford-edge-2019-2026-2.0-2.7', 'model': 'Edge', 'model_he': "אדג'", 'generation': '2nd gen facelift', 'years': [2019, 2026],
       'engines': ['2.0 בנזין', '2.7 V6 בנזין'], 'fuel': 'petrol'}, p,
      [{'names': ['EDGE', 'EDGE TITANIUM', 'EDGE-TITANIUM', 'EDGE-SEL', 'EDGE SEL', 'EDGE ST'], 'years': [2019, 2026]}])

# ---------------------------------------------------------------- Explorer
p = fplan('Explorer_2011_2014', 'טיפול כשמופיעה הודעת OIL CHANGE REQUIRED, או 15,000 ק"מ או 12 חודשים (מנוע בנזין 3.5, שנות ייצור 2011-2014)', 15000, 6,
          [], [(30000, [R('cabin_filter', 'או שנתיים')]), (45000, [R('air_filter', 'אם לא הוחלף קודם'), R('transfer_case_oil')])],
          [coolant_long(165000, 72, 75000, 36), LI('spark_plugs', 'replace', every_km=150000),
           LI('transmission_oil', 'replace', every_km=240000), LI('differential_oil', 'replace', every_km=240000, note='סרן אחורי')],
          'שמן ומסנן לפי הודעה בלוח השעונים או כל 15,000 ק"מ או שנה; מסנן מזגן כל 30,000 או שנתיים; מסנן אוויר, מסנן אוויר של המושב המקורר ושמן תיבת העברה כל 45,000; מצתים 150,000; שמן גיר ושמן סרן אחורי 240,000; נוזל קירור לראשונה ב-165,000 או 6 שנים ואחר כך כל 75,000 או 3 שנים.',
          {'engine_oil': '5W-20 (WSS-M2C970-A1)', 'coolant': 'צהוב, מפרט WSS-M97B57-A2', 'brake_fluid': 'DOT 4 Low Viscosity',
           '_note': 'בתוכנית גם מסנן אוויר למושב מקורר כל 45,000 ק"מ (אין לו פריט ברשימה)'},
          'לפי הודעה בלוח השעונים, או 15,000 ק"מ או 12 חודשים')
write({**FORD, 'id': 'ford-explorer-2011-2014-3.5', 'model': 'Explorer', 'model_he': 'אקספלורר', 'generation': 'U502', 'years': [2011, 2014],
       'engines': ['3.5 V6'], 'fuel': 'petrol'}, p, [{'names': ['EXPLORER'], 'years': [2011, 2014]}])

p = fplan('Explorer_2015_2018', 'טיפול כשמופיעה הודעת OIL CHANGE REQUIRED, או 15,000 ק"מ או 12 חודשים (מנוע 3.5, שנות ייצור 2015-2018)', 15000, 6,
          [], [(30000, [R('cabin_filter', 'או שנתיים')]), (45000, [R('air_filter', 'אם לא הוחלף קודם')])],
          [coolant_long(165000, 72, 75000, 36), LI('spark_plugs', 'replace', every_km=150000),
           LI('transmission_oil', 'replace', every_km=240000), LI('differential_oil', 'replace', every_km=240000, note='סרן אחורי'),
           LI('drive_belt', 'replace', every_km=165000)],
          'שמן ומסנן לפי הודעה בלוח השעונים או כל 15,000 ק"מ או שנה; מסנן מזגן כל 30,000 או שנתיים; מסנן אוויר ומסנן אוויר של המושב המקורר כל 45,000; מצתים 150,000; רצועת אביזרים 165,000; שמן גיר ושמן סרן אחורי 240,000; נוזל קירור לראשונה ב-165,000 או 6 שנים ואחר כך כל 75,000 או 3 שנים.',
          {'engine_oil': '5W-20 (WSS-M2C970-A1)', 'coolant': 'צהוב, מפרט WSS-M97B57-A2', 'brake_fluid': 'DOT 4 Low Viscosity',
           '_note': 'בתוכנית גם מסנן אוויר למושב מקורר כל 45,000 ק"מ (אין לו פריט ברשימה). באתר היבואן התוכנית מוצגת לשנים 2012-2019'},
          'לפי הודעה בלוח השעונים, או 15,000 ק"מ או 12 חודשים')
write({**FORD, 'id': 'ford-explorer-2015-2019-3.5', 'model': 'Explorer', 'model_he': 'אקספלורר', 'generation': 'U502 facelift', 'years': [2015, 2019],
       'engines': ['3.5 V6'], 'fuel': 'petrol'}, p,
      [{'names': ['EXPLORER', 'EXPLORER LIMITE', 'EXPLORER-LIMITE', 'EXPLORER LIMITED', 'EXPLORER PLATIN', 'EXPLORER SPORT'], 'years': [2015, 2019]}])

p = fplan('Explorer_2020_And_Up', 'טיפול כשמופיעה הודעת OIL CHANGE REQUIRED, או 20,000 ק"מ או 12 חודשים (מנועי בנזין 2.3/3.0, משנת ייצור 2020)', 20000, 6,
          [R('cabin_filter', 'כל 20,000 ק"מ')], [],
          [coolant_long(320000, 120, 160000, 60), LI('air_filter', 'replace', every_km=30000),
           LI('spark_plugs', 'replace', every_km=160000), LI('transmission_oil', 'replace', every_km=240000),
           LI('differential_oil', 'replace', every_km=240000, note='סרן אחורי'), LI('brake_fluid', 'replace', every_months=36),
           LI('drive_belt', 'inspect', first_km=160000, then_every_km=40000, note='בדיקה לראשונה ב-160,000 ואחר כך בכל טיפול שני; החלפה לפי הצורך'),
           LI('drive_belt', 'replace', every_km=240000, note='בכל מקרה')],
          'שמן ומסנן לפי הודעה בלוח השעונים או כל 20,000 ק"מ או שנה; מסנן מזגן כל 20,000; מסנן אוויר כל 30,000; נוזל בלמים כל 3 שנים; מצתים 160,000; שמן גיר ושמן סרן אחורי 240,000; רצועת אביזרים: בדיקה מ-160,000 והחלפה ב-240,000; נוזל קירור לראשונה ב-320,000 או 10 שנים ואחר כך כל 160,000 או 5 שנים.',
          {'engine_oil': '5W-30 (WSS-M2C971-A1)', 'coolant': 'צהוב, מפרט WSS-M97B57-A2', 'brake_fluid': 'DOT 4 Low Viscosity',
           '_note': 'גיר אוטומטי Mercon ULV; סרן אחורי 75W-80; סרן קדמי 75W-140 (לפי התוכנית)'},
          'לפי הודעה בלוח השעונים, או 20,000 ק"מ או 12 חודשים')
write({**FORD, 'id': 'ford-explorer-2020-2026-2.3-3.0', 'model': 'Explorer', 'model_he': 'אקספלורר', 'generation': 'U625', 'years': [2020, 2026],
       'engines': ['2.3 בנזין', '3.0 V6 בנזין'], 'fuel': 'petrol'}, p,
      [{'names': ['EXPLORER', 'EXPLORER-ST', 'EXPLORER ST', 'EXPLORER LIMITE', 'EXPLORER-LIMITE', 'EXPLORER-LIMITD', 'EXPLORER LIMITED', 'EXPLORER PLATIN', 'EXPLORER-PLATIN'], 'years': [2020, 2026]}])

# ---------------------------------------------------------------- Ranger diesel 2023+
p = fplan('Ranger_Diesel_2023_And_Up', 'טיפול כשמופיעה הודעה בלוח השעונים, או 20,000 ק"מ או 24 חודשים (מנוע דיזל, משנת ייצור 2023)', 20000, 6,
          [I('fuel_filter', 'ניקוז מים; החלפה אם נורית המים בסולר לא כבתה אחרי הניקוז')], [(40000, [R('air_filter', 'או 4 שנים'), R('cabin_filter', 'או 4 שנים')])],
          [LI('coolant', 'replace', every_months=120), LI('timing_belt', 'replace', every_km=160000, every_months=72),
           LI('drive_belt', 'replace', every_km=240000, every_months=120), LI('transmission_oil', 'replace', every_km=240000, every_months=120, note='שמן ומסנן'),
           LI('differential_oil', 'replace', every_km=240000, every_months=120, note='סרן קדמי ואחורי'),
           LI('transfer_case_oil', 'replace', every_km=240000, every_months=120), LI('brake_fluid', 'replace', every_months=24)],
          'שמן ומסנן לפי הודעה בלוח השעונים או כל 20,000 ק"מ או שנתיים; ניקוז מים ממסנן הסולר; מסנני אוויר ומזגן כל 40,000 או 4 שנים; נוזל בלמים כל שנתיים; רצועת תזמון 160,000 או 6 שנים; נוזל קירור כל 10 שנים; רצועת אביזרים, שמן גיר, שמני סרנים ותיבת העברה 240,000 או 10 שנים.',
          {'engine_oil': '5W-30 (WSS-M2C913-D)', 'coolant': 'צהוב, מפרט WSS-M97B57-A2', 'brake_fluid': 'DOT 4 Low Viscosity',
           'timing': 'רצועת תזמון: 160,000 ק"מ או 6 שנים'},
          'לפי הודעה בלוח השעונים, או 20,000 ק"מ או 24 חודשים')
write({**FORD, 'id': 'ford-ranger-2023-2026-diesel', 'model': 'Ranger', 'model_he': "ריינג'ר", 'generation': 'P703', 'years': [2023, 2026],
       'engines': ['דיזל'], 'fuel': 'diesel'}, p, [{'names': ['RANGER'], 'years': [2023, 2026], 'fuel': ['דיזל']}])

# ---------------------------------------------------------------- Bronco 2021+
p = fplan('Bronco_2021_And_Up', 'טיפול כשמופיעה הודעת OIL CHANGE REQUIRED, או 16,000 ק"מ או 12 חודשים (משנת ייצור 2021)', 16000, 6,
          [], [(32000, [R('cabin_filter')]), (48000, [R('air_filter', 'אם לא הוחלף קודם')])],
          [coolant_long(320000, 120, 160000, 60), LI('spark_plugs', 'replace', every_km=160000),
           LI('transmission_oil', 'replace', every_km=240000, note='שמן ומסנן'), LI('differential_oil', 'replace', every_km=240000, note='סרן קדמי ואחורי'),
           LI('transfer_case_oil', 'replace', every_km=240000), LI('brake_fluid', 'replace', every_months=36),
           LI('drive_belt', 'inspect', first_km=160000, then_every_km=32000, note='בדיקה לראשונה ב-160,000 ואחר כך בכל טיפול שני; החלפה לפי הצורך'),
           LI('drive_belt', 'replace', every_km=240000, note='בכל מקרה')],
          'שמן ומסנן לפי הודעה בלוח השעונים או כל 16,000 ק"מ או שנה; מסנן מזגן כל 32,000; מסנן אוויר כל 48,000; נוזל בלמים כל 3 שנים; מצתים 160,000; שמן גיר, סרנים ותיבת העברה 240,000; רצועת אביזרים: בדיקה מ-160,000 והחלפה ב-240,000; נוזל קירור לראשונה ב-320,000 או 10 שנים ואחר כך כל 160,000 או 5 שנים.',
          {'engine_oil': '5W-30 (WSS-M2C961-A1)', 'coolant': 'צהוב, מפרט WSS-M97B57-A2', 'brake_fluid': 'DOT 4 Low Viscosity'},
          'לפי הודעה בלוח השעונים, או 16,000 ק"מ או 12 חודשים')
write({**FORD, 'id': 'ford-bronco-2021-2026', 'model': 'Bronco', 'model_he': 'ברונקו', 'generation': 'U725', 'years': [2021, 2026],
       'engines': ['בנזין (תוכנית אחת לכל מנועי הברונקו)'], 'fuel': 'petrol'}, p,
      [{'names': ['BRONCO', 'BRONCO BADLANDS', 'BRONCO WILDTRAC', 'BRONCO WILDTRAK', 'BRONCO BIGBEND', 'BRONCO BIG BEND', 'BRONCO OUTER BANKS', 'BRONCO RAPTOR'], 'years': [2021, 2026]}])

# ---------------------------------------------------------------- Focus Mk1 1999-2003
URLS['Focus_1999_2003'] = SP + 'Ee430FBNfetOviTm_6b6ntQBZUu0KKGEJFkz79p06v_aBg?download=1'
p = fplan('Focus_1999_2003', 'טיפול כל 15,000 ק"מ או 12 חודשים (שנות ייצור 1999-2003)', 15000, 8,
          [], [(45000, [R('air_filter', 'אם לא הוחלף קודם')]), (60000, [R('spark_plugs')]), (75000, [R('fuel_filter')]),
               (120000, [A('valve_clearance'), R('timing_belt', 'או 5 שנים')])],
          [LI('timing_belt', 'replace', every_km=120000, every_months=60), LI('valve_clearance', 'adjust', every_km=120000),
           LI('fuel_filter', 'replace', every_km=75000), LI('coolant', 'replace', every_months=120), LI('brake_fluid', 'replace', every_months=24)],
          'שמן ומסנן כל 15,000 ק"מ או שנה; מסנן אוויר כל 45,000; מצתים כל 60,000; מסנן דלק כל 75,000; כיוון שסתומים ורצועת תזמון ב-120,000 (הרצועה או 5 שנים); נוזל בלמים כל שנתיים; נוזל קירור כל 10 שנים.',
          {'engine_oil': '5W-30 (WSS-M2C913-B)', 'coolant': 'צהוב, מפרט WSS-M97B57-A1', 'brake_fluid': 'DOT 4 Super (בלמים ומצמד)',
           'timing': 'רצועת תזמון: 120,000 ק"מ או 5 שנים'}, 'כל 15,000 ק"מ או שנה')
write({**FORD, 'id': 'ford-focus-1999-2003-1.6', 'model': 'Focus', 'model_he': 'פוקוס', 'generation': 'Mk1 (C170)', 'years': [1999, 2003],
       'engines': ['1.6 Zetec (FYD)'], 'fuel': 'petrol'}, p, [{'names': ['FOCUS'], 'years': [1999, 2003]}])
