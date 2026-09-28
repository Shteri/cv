from gen import *

IMP = 'פריסבי (קרסו)'
REN = dict(make='Renault', make_he='רנו', importer=IMP)
DAC = dict(make='Dacia', make_he="דאצ'יה", importer=IMP)
AU = 'https://www.renault.com.au/capped-price-servicing/'
BLOCK = {'url': 'https://www.renault.co.il/', 'kind': 'importer', 'note': 'אתרי renault.co.il ו-dacia.co.il חסומים מסביבת הענן (Incapsula 403, גם בדפדפן Playwright); ספר עברי או לוח טיפולים של היבואן לא נמצאו'}

BASIC = [R('engine_oil'), R('oil_filter'), I('tires'), I('lights'), I('brake_pads'), I('brake_discs'), I('coolant', 'מפלס'),
         I('brake_fluid', 'מפלס'), I('diagnostics')]
NOTE_BASIC = 'רשימת הבדיקות הכלליות בכל טיפול (צמיגים, תאורה, בלמים, מפלסים, קריאת מחשב) איננה מפורטת בעמוד המקור ונוספה כבדיקות שגרה; ההחלפות והמרווחים לקוחים מהמקור. '

# K9K 1.5 dCi -> Renault Australia Kangoo 1.5 diesel table
PLAN_K9K = {
    'interval': {'km': 15000, 'months': 12, 'note': 'לפי טבלת רנו אוסטרליה לקנגו 1.5 דיזל: טיפולים ב-15,000, 30,000, 45,000... ק"מ; מסננים כל 30,000 או שנתיים. משך הזמן בין טיפולים (שנה) לפי מדיניות השירות הכללית בעמוד'},
    'cycle_km': 120000,
    'grid': grid(15000, 8, BASIC, {30000: [R('air_filter', 'או כל שנתיים'), R('cabin_filter', 'או כל שנתיים'), R('fuel_filter', 'או כל שנתיים')]}),
    'long': [LI('timing_belt', 'replace', every_km=120000, every_months=48, note='ערכת רצועת תזמון וערכת רצועת אביזרים'),
             LI('drive_belt', 'replace', every_km=120000, every_months=48),
             LI('coolant', 'replace', every_km=120000, every_months=48),
             LI('brake_fluid', 'replace', every_km=120000, every_months=48)],
    'specs': {'timing': 'רצועת תזמון: 120,000 ק"מ או 4 שנים (טבלת רנו אוסטרליה, קנגו 1.5 דיזל)'},
    'sources': [{'url': AU, 'kind': 'manufacturer', 'note': 'Renault Australia, Capped Price Servicing: טבלת "Renault Kangoo 1.5 Diesel" (מנוע K9K) - מרווחי מסננים, רצועות, נוזל קירור ונוזל בלמים'}, BLOCK],
    'status': 'draft',
    'notes': 'לוח היבואן בישראל לא נמצא. המרווחים לקוחים מטבלת השירות הרשמית של רנו אוסטרליה לקנגו עם מנוע 1.5 dCi (K9K), אותו מנוע שבדגם זה. טיפול כל 15,000 ק"מ: שמן ומסנן. כל 30,000 ק"מ או שנתיים: מסנני אוויר, מזגן וסולר. ערכת רצועת תזמון ורצועת אביזרים, נוזל קירור ונוזל בלמים: כל 120,000 ק"מ או 4 שנים. ' + NOTE_BASIC + 'בדגמים החדשים יותר (מגאן IV, קדג\'אר) יש חיישן מצב שמן שעשוי להקדים טיפול.'
}

# H5F 1.2 TCe -> Kangoo 1.2 petrol table
PLAN_H5F = {
    'interval': {'km': 15000, 'months': 12, 'note': 'לפי טבלת רנו אוסטרליה לקנגו 1.2 בנזין: טיפולים כל 15,000 ק"מ; מסננים כל 30,000 או שנתיים'},
    'cycle_km': 120000,
    'grid': grid(15000, 8, BASIC, {30000: [R('air_filter', 'או כל שנתיים'), R('cabin_filter', 'או כל שנתיים'), R('fuel_filter', 'או כל שנתיים')],
                                  60000: [R('spark_plugs', 'או כל 4 שנים')]}),
    'long': [LI('drive_belt', 'replace', every_km=90000, every_months=48, note='ערכת רצועת אביזרים'),
             LI('coolant', 'replace', every_km=120000, every_months=48),
             LI('brake_fluid', 'replace', every_km=120000, every_months=48)],
    'specs': {'timing': 'שרשרת תזמון (מנוע H5F), אין החלפה בטבלה'},
    'sources': [{'url': AU, 'kind': 'manufacturer', 'note': 'Renault Australia, Capped Price Servicing: טבלת "Renault Kangoo 1.2 Petrol" (מנוע 1.2 TCe H5F)'}, BLOCK],
    'status': 'draft',
    'notes': 'לוח היבואן בישראל לא נמצא. המרווחים לקוחים מטבלת רנו אוסטרליה לקנגו עם מנוע 1.2 TCe (H5F), אותו מנוע שבדגם זה. טיפול כל 15,000 ק"מ: שמן ומסנן. כל 30,000 או שנתיים: מסנני אוויר, מזגן ודלק. מצתים כל 60,000 או 4 שנים. ערכת רצועת אביזרים כל 90,000 או 4 שנים. נוזל קירור ונוזל בלמים כל 120,000 או 4 שנים. ' + NOTE_BASIC
}

# H5H 1.3 TCe -> Kadjar/Arkana/Captur MY21+ table
PLAN_H5H = {
    'interval': {'km': 30000, 'months': 12, 'note': 'לפי רנו אוסטרליה (קדג\'אר, ארקנה וקפצ\'ור מ-2021): טיפול כל 12 חודשים או 30,000 ק"מ; חיישן מצב השמן עשוי להקדים טיפול'},
    'cycle_km': 120000,
    'grid': grid(30000, 4, BASIC + [R('air_filter'), R('cabin_filter')], {60000: [R('spark_plugs', 'או כל 4 שנים')]}),
    'long': [LI('drive_belt', 'replace', every_km=120000, every_months=48, note='ערכת רצועת אביזרים'),
             LI('coolant', 'replace', every_km=120000, every_months=48),
             LI('brake_fluid', 'replace', every_km=120000, every_months=48)],
    'specs': {'timing': 'שרשרת תזמון (מנוע 1.3 TCe H5H), אין החלפה בטבלה'},
    'sources': [{'url': AU, 'kind': 'manufacturer', 'note': 'Renault Australia, Capped Price Servicing: טבלת "Renault Kadjar, Arkana & Captur (MY21 onwards)" (מנוע 1.3 TCe H5H)'}, BLOCK],
    'status': 'draft',
    'notes': 'לוח היבואן בישראל לא נמצא. לפי טבלת רנו אוסטרליה למנוע 1.3 TCe: טיפול כל שנה או 30,000 ק"מ עם החלפת שמן, מסנן אוויר ומסנן מזגן. מצתים כל 60,000 או 4 שנים. ערכת רצועת אביזרים, נוזל קירור ונוזל בלמים כל 120,000 או 4 שנים. מערכת חיישן השמן ברכב עשויה לדרוש טיפול מוקדם יותר, והיבואן בישראל עשוי לקבוע מרווח קצר יותר. ' + NOTE_BASIC
}

# Trafic 2.0 dCi -> Trafic MY23 2.0 diesel table
PLAN_TRAFIC = {
    'interval': {'km': 30000, 'months': 12, 'note': 'לפי רנו אוסטרליה לטראפיק 2.0 דיזל: טיפולים כל 30,000 ק"מ, מסננים כל שנה או 30,000'},
    'cycle_km': 120000,
    'grid': grid(30000, 4, BASIC + [R('air_filter'), R('cabin_filter'), R('fuel_filter')], {90000: [R('dct_oil', 'רק בגיר EDC: שמן ומסנן, או כל 6 שנים')]}),
    'long': [LI('drive_belt', 'replace', every_km=120000, every_months=48, note='ערכת רצועת אביזרים'),
             LI('coolant', 'replace', every_km=120000, every_months=48),
             LI('brake_fluid', 'replace', every_km=120000, every_months=48),
             LI('dct_oil', 'replace', every_km=90000, every_months=72, note='רק בגיר כפול מצמד EDC')],
    'specs': {},
    'sources': [{'url': AU, 'kind': 'manufacturer', 'note': 'Renault Australia, Capped Price Servicing: טבלת "Renault Trafic (MY23 onwards)", Trafic 2.0L Diesel 125kW'}, BLOCK],
    'status': 'draft',
    'notes': 'לוח היבואן בישראל לא נמצא. לפי טבלת רנו אוסטרליה לטראפיק 2.0 דיזל: טיפול כל שנה או 30,000 ק"מ עם שמן ומסנני אוויר, מזגן וסולר. ערכת רצועת אביזרים, נוזל קירור ונוזל בלמים כל 120,000 או 4 שנים. בגיר EDC: שמן ומסנן כל 90,000 או 6 שנים. ' + NOTE_BASIC
}

def mk(base, vid, model, mhe, gen_, yrs, engines, fuel, plan, names, codes, note_pre=''):
    v = dict(base, id=vid, model=model, model_he=mhe, generation=gen_, years=yrs, engines=engines, fuel=fuel)
    p = plan
    if note_pre:
        p = copy.deepcopy(plan); p['notes'] = note_pre + plan['notes']
    write(v, p, [{'names': names, 'years': yrs, 'engine_codes': codes}])

K9 = ['1.5 dCi (K9K)']
for base, vid, model, mhe, gen_, yrs, names in [
    (REN, 'renault-megane-2010-2024-1.5-dci', 'Megane', 'מגאן', 'III / IV', [2010, 2024], ['MEGANE']),
    (REN, 'renault-megane-grand-coupe-2017-2019-1.5-dci', 'Megane Grand Coupe', 'מגאן גראנד קופה', 'IV', [2017, 2019], ['GRAND COUPE']),
    (REN, 'renault-fluence-2010-2017-1.5-dci', 'Fluence', 'פלואנס', 'L38', [2010, 2017], ['FLUENCE']),
    (DAC, 'dacia-duster-2012-2024-1.5-dci', 'Duster', 'דאסטר', 'HS / HM', [2012, 2024], ['DUSTER']),
    (REN, 'renault-kangoo-2008-2021-1.5-dci', 'Kangoo', 'קנגו', 'II (KW)', [2008, 2021], ['KANGOO', 'KANGOO 2']),
    (REN, 'renault-kadjar-2016-2021-1.5-dci', 'Kadjar', "קדג'אר", 'HA', [2016, 2021], ['KADJAR']),
    (REN, 'renault-clio-2013-2019-1.5-dci', 'Clio', 'קליאו', 'IV', [2013, 2019], ['CLIO']),
    (REN, 'renault-captur-2014-2019-1.5-dci', 'Captur', "קפצ'ור", 'J87', [2014, 2019], ['CAPTUR']),
    (REN, 'renault-grand-scenic-2013-2021-1.5-dci', 'Grand Scenic', 'גראנד סניק', 'III / IV', [2013, 2021], ['GRAND SCENIC']),
    (DAC, 'dacia-sandero-logan-2013-2021-1.5-dci', 'Sandero / Logan', 'סנדרו / לוגאן', 'II', [2013, 2021], ['SANDERO', 'LOGAN', 'SANDERO STEPWAY']),
    (DAC, 'dacia-lodgy-dokker-2013-2022-1.5-dci', 'Lodgy / Dokker', "לודג'י / דוקר", '', [2013, 2022], ['LODGY', 'DOKKER']),
]:
    mk(base, vid, model, mhe, gen_, yrs, K9, 'diesel', PLAN_K9K, names, ['K9K'])

H5F = ['1.2 TCe (H5F)']
for base, vid, model, mhe, gen_, yrs, names in [
    (REN, 'renault-clio-2013-2020-1.2-tce', 'Clio', 'קליאו', 'IV', [2013, 2020], ['CLIO']),
    (REN, 'renault-captur-2013-2019-1.2-tce', 'Captur', "קפצ'ור", 'J87', [2013, 2019], ['CAPTUR']),
    (DAC, 'dacia-duster-2015-2020-1.2-tce', 'Duster', 'דאסטר', 'HS / HM', [2015, 2020], ['DUSTER']),
    (REN, 'renault-kangoo-2013-2021-1.2-tce', 'Kangoo', 'קנגו', 'II (KW)', [2013, 2021], ['KANGOO']),
    (REN, 'renault-kadjar-2016-2019-1.2-tce', 'Kadjar', "קדג'אר", 'HA', [2016, 2019], ['KADJAR']),
    (REN, 'renault-megane-2016-2019-1.2-tce', 'Megane / Grand Coupe', 'מגאן / גראנד קופה', 'IV', [2016, 2019], ['MEGANE', 'GRAND COUPE']),
    (DAC, 'dacia-lodgy-2013-2019-1.2-tce', 'Lodgy', "לודג'י", '', [2013, 2019], ['LODGY']),
]:
    mk(base, vid, model, mhe, gen_, yrs, H5F, 'petrol', PLAN_H5F, names, ['H5F'])

H5H = ['1.3 TCe (H5H)']
for base, vid, model, mhe, gen_, yrs, names, pre in [
    (REN, 'renault-arkana-2022-2026-1.3-tce', 'Arkana', 'ארקנה', 'LJL', [2022, 2026], ['ARKANA'], ''),
    (REN, 'renault-captur-2020-2026-1.3-tce', 'Captur', "קפצ'ור", 'HJB', [2020, 2026], ['CAPTUR'], ''),
    (REN, 'renault-megane-2019-2024-1.3-tce', 'Megane', 'מגאן', 'IV', [2019, 2024], ['MEGANE', 'GRAND SCENIC'], 'מגאן עם מנוע 1.3 TCe לא מופיע בטבלה האוסטרלית; נלקחו נתוני המנוע מקדג\'אר/קפצ\'ור. '),
    (DAC, 'dacia-duster-2019-2026-1.3-tce', 'Duster', 'דאסטר', 'HM', [2019, 2026], ['DUSTER'], 'דאצ\'יה לא נמכרת באוסטרליה; נלקחו נתוני המנוע 1.3 TCe מטבלת קדג\'אר/קפצ\'ור של רנו. '),
    (REN, 'renault-austral-2023-2026-1.3-tce', 'Austral', 'אוסטרל', 'HCB', [2023, 2026], ['AUSTRAL'], 'אוסטרל לא מופיע בטבלה האוסטרלית; נלקחו נתוני מנוע 1.3 TCe (היברידי מתון) מטבלת קדג\'אר/ארקנה/קפצ\'ור. '),
]:
    mk(base, vid, model, mhe, gen_, yrs, H5H, 'petrol', PLAN_H5H, names, ['H5H', 'H5HB4B'], pre)

mk(REN, 'renault-trafic-2015-2026-2.0-dci', 'Trafic', 'טראפיק', 'III', [2015, 2026], ['2.0 dCi (M9R)'], 'diesel', PLAN_TRAFIC, ['TRAFIC'], ['M9R'])
