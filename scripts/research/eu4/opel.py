# Opel GM era: item grid = Opel Insignia 2011 EN owner's manual (manualslib 936387),
# "International service schedule", printed pp. 193-196 (15,000 km / 1 year columns 1-5).
# Interval for Israel = Hebrew Opel manuals on public-servicebox.opel.com (Israel not in the European list -> international 15,000 km / 1 year).
from gen import *

ML = 'https://www.manualslib.com/manual/936387/Opel-2011-Insignia.html?page=193'
HE = 'https://public-servicebox.opel.com/OVddb/OV/he_IL/'
IMPORTER = 'קבוצת שלמה (יבואנית אופל 2010-2019; מאז 2019 דוד לובינסקי)'

ALL = 'all'; ODD = {1, 3, 5}; EVEN = {2, 4}
GRID = [
    (ALL, it('lights', 'inspect', 'בדיקה חזותית של יחידות בקרה, תאורה ואיתות וכריות אוויר; מנעול הגה ומתג התנעה')),
    (ALL, it('wipers', 'inspect', 'מגבים ומתזי שמשה ופנסים')),
    (ALL, it('washer_fluid', 'inspect')),
    (ALL, it('coolant', 'inspect', 'מפלס והגנת קיפאון; השלמה לפי הצורך')),
    (ODD, it('brake_fluid', 'inspect', 'מפלס; השלמה לפי הצורך')),
    (ALL, it('battery_12v', 'inspect', 'הידוק הדקים ועין הסוללה')),
    (EVEN, it('cabin_filter', 'replace', 'מסנן אבקנים או פחם פעיל')),
    (EVEN, it('drive_belt', 'inspect', 'בדיקה חזותית של רצועת האביזרים')),
    (ALL, it('power_steering_fluid', 'inspect', 'בהגה הידראולי: דליפות ומפלס שמן')),
    (ALL, it('engine_oil', 'replace')),
    (ALL, it('oil_filter', 'replace')),
    (EVEN, it('suspension', 'inspect', 'עיגון הגלגלים וקפיצי המתלים מלפנים ומאחור')),
    (EVEN, it('brake_lines', 'inspect', 'צנרת וצינורות לחץ של הבלמים')),
    (EVEN, it('fuel_lines', 'inspect')),
    (EVEN, it('exhaust', 'inspect')),
    (ALL, it('body_underside', 'inspect', 'מרכב והגנת קורוזיה בתחתית; נזקים נרשמים בפנקס השירות')),
    (ALL, it('brake_pads', 'inspect', 'בדיקה חזותית של בלמים קדמיים ואחוריים')),
    (ALL, it('brake_discs', 'inspect')),
    (ALL, it('ac_system', 'inspect', 'דליפות במדחס המזגן, יחד עם בדיקת דליפות במנוע ובתיבה')),
    (ALL, it('cv_boots', 'inspect', 'גומיות ההגה, מוטות ההגה וצירי ההנעה')),
    (ALL, it('steering', 'inspect', 'קצוות מוטות הגה ומפרקים כדוריים')),
    (EVEN, it('tires', 'inspect', 'מצב ולחץ (כולל גלגל חלופי או ערכת תיקון); שחרור והידוק מחדש של ברגי הגלגלים')),
    (EVEN, it('lights', 'adjust', 'כיוון פנסים ראשיים')),
    (EVEN, it('door_hinges', 'inspect', 'שימון צירי דלתות, מעצורים, צילינדר מנעול, תפסים ומנעול מכסה מנוע')),
]

def long_items(plugs_120=False, belts=False, valves=False, plugs_note=None):
    L = [
        LI('air_filter', 'replace', every_km=60000, every_months=48),
        LI('spark_plugs', 'replace', every_km=120000 if plugs_120 else 60000, every_months=96 if plugs_120 else 48, **({'note': plugs_note} if plugs_note else {})),
        LI('brake_fluid', 'replace', every_months=24, note='יחד עם נוזל המצמד; ללא קשר לק"מ'),
    ]
    if belts:
        L.append(LI('drive_belt', 'replace', every_km=150000, every_months=120))
        L.append(LI('timing_belt', 'replace', every_km=150000, every_months=120, note='כולל גלגלת מתיחה'))
        L.append(LI('drive_belt', 'replace', every_km=120000, every_months=120, note='רצועת משאבת המים ומשאבת ההגה (רצועה נפרדת)'))
    if valves:
        L.append(LI('valve_clearance', 'inspect', every_km=150000, every_months=120, note='בדיקה וכיוון לפי הצורך; רק במנוע A16XER'))
    return L

SRC_ML = {'url': ML, 'kind': 'manufacturer', 'note': 'Opel Insignia owner\'s manual (EN, edition 2011, manualslib 936387): "International service schedule", printed pp. 193-196 (site pages 193-196), five columns of 15,000 km / 1 year; additional operations p. 197. Insignia lists A16XER/A18XER/A16LET/A20NHT/A28NET and diesels.'}

def he_src(path, page, text):
    return {'url': HE + path, 'kind': 'importer', 'note': f'ספר הנהג העברי באתר אופל, עמוד {page} בקובץ: {text}'}

COMMON_NOTES = ('טבלת הפריטים לקוחה מטבלת השירות הבינלאומית בספר הנהג האנגלי של אופל אינסיגניה (מהדורת 2011), מאותו דור של אופל; ספרי הנהג של אסטרה, מוקה, מריבה וזאפירה מתקופה זו (בעברית ובאנגלית) מפנים למוסך ואינם כוללים טבלה. '
    'בכל טיפול (כל 15,000 ק"מ או שנה): שמן ומסנן, בדיקת נוזלים ומצבר, תאורה, הגה, גומיות, בלמים, מרכב ודליפות במנוע ובמזגן. '
    'בכל טיפול שני (30,000 ק"מ): מסנן מזגן, רצועת אביזרים (בדיקה), מתלים, צנרת בלמים ודלק, פליטה, צמיגים, כיוון פנסים ושימון צירים. '
    'מסנן אוויר ומצתים כל 60,000 ק"מ או 4 שנים, נוזל בלמים ומצמד כל שנתיים. בתנאי שימוש קשים (אבק, חום, נסיעות קצרות) היצרן מקצר מרווחים.')

def opel_file(id_, model, model_he, gen, years, engines, he_srcs, rules, extra_note='', plugs_120=False, belts=False, valves=False, plugs_note=None, longx=None):
    s = {
        'id': id_, 'make': 'Opel', 'make_he': 'אופל', 'model': model, 'model_he': model_he, 'generation': gen,
        'years': years, 'engines': engines, 'fuel': 'petrol', 'importer': IMPORTER,
        'interval': {'km': 15000, 'months': 12, 'note': 'ספרי הנהג העבריים של אופל מ-2013 ואילך: ישראל אינה ברשימת המדינות האירופיות ולכן חל המרווח הבינלאומי, 15,000 ק"מ או שנה'},
        'cycle_km': 75000,
        'services': build(15000, 5, GRID),
        'long_interval': long_items(plugs_120, belts, valves, plugs_note) + (longx or []),
        'specs': {'_note': 'הטבלה אינה מפרטת סוג שמן או החלפת נוזל קירור; ההחלפות הנוספות לפי המנוע מופיעות בלוח הארוך'},
        'sources': [SRC_ML] + he_srcs,
        'status': 'draft',
        'notes': COMMON_NOTES + ' ' + extra_note + ' טיוטה: טבלת פריטים של דגם אחר מאותו דור.'
    }
    write(s, rules)

A14 = ['A14NET', 'A 1.4 NET', 'B14NET', 'B 1.4 NET']
NOTE_14T = 'מנוע 1.4 טורבו (A14NET/B14NET) אינו מופיע ברשימות ההחלפה של רצועות התזמון והאביזרים ובכיוון השסתומים בטבלה, ולכן לא נוספו לו שורות כאלה. '
NOTE_2012 = 'בספרי הנהג העבריים של שנתון 2012 ישראל עוד נכללה ברשימה האירופית (30,000 ק"מ או שנה); הקובץ משתמש במרווח הבינלאומי שחל מהמהדורות של 2013 ואילך.'

def main():
    opel_file('opel-astra-j-2010-2016-1.4-turbo', 'Astra', 'אסטרה', 'J (הצ\'בק, סדאן, סטיישן ST, GTC)', [2011, 2018], ['1.4 Turbo (A14NET/B14NET)'],
        [he_src('Astra_J/2010_2016/2013/manual_user/om_astra_kta-2685_6-heb_eu_my13_ed0812_18_he_il_online%5Bastra%5D.pdf', 261, 'ישראל אינה ברשימה האירופית; מרווח בינלאומי 15,000 ק"מ או שנה. אין טבלת פריטים'),
         he_src('Astra_J/2010_2016/2014/manual_user/om_astra_kta-2685_8-heb_eu_my14_ed0813_23_he_il_online%5Bastra%5D.pdf', 273, 'אותו מרווח בינלאומי (שנתון 2014)'),
         he_src('Astra_J/2010_2016/2012_5/manual_user/om_astra_KTA-2685_5-heb_eu_my12_ed0112_16_he_IL_online.pdf', 218, 'במהדורת 2012 ישראל עוד ברשימה האירופית (30,000 ק"מ או שנה)')],
        [{'make': 'Opel', 'names': ['ASTRA', 'TRA BERLINA', 'ASTRA BERLINA', 'ASTRA ST', 'ASTRA GTC', 'ASTRA SEDAN'], 'years': [2011, 2018], 'engine_codes': A14}],
        NOTE_14T + NOTE_2012)
    opel_file('opel-astra-k-2016-2018-1.4-turbo', 'Astra', 'אסטרה', 'K', [2016, 2018], ['1.4 Turbo (B14XFT)'],
        [he_src('Astra_K/2016_2021/2017/manual_user/ID-OASKOLSE1608-he_7_online.pdf', 258, 'ישראל אינה ברשימה האירופית; מרווח בינלאומי 15,000 ק"מ או שנה. אין טבלת פריטים')],
        [{'make': 'Opel', 'names': ['ASTRA'], 'years': [2016, 2018], 'engine_codes': ['B 14 XFT', 'B14XFT', 'LE2']}],
        'מנוע B14XFT (קוד GM: LE2) אינו מופיע בטבלה, ולכן אין לו שורות של רצועת תזמון או כיוון שסתומים. אסטרה K היא דור חדש יותר מהאינסיגניה שבספר.')
    opel_file('opel-mokka-2013-2018-1.4-turbo', 'Mokka / Mokka X', 'מוקה / מוקה X', 'J13', [2013, 2018], ['1.4 Turbo (A14NET/B14NET)'],
        [he_src('Mokka_X/2011_2016/2014_5/manual_user/om_mokka_kta-2749_2-heb_eu_my14_ed0114_5_he_il_online%5BMokka%5D.pdf', 189, 'ישראל אינה ברשימה האירופית; מרווח בינלאומי 15,000 ק"מ או שנה. אין טבלת פריטים'),
         he_src('Mokka_X/2017_2022/2017/manual_user/ID-OMKAOLSE1608-he_16_online.pdf', 208, 'מוקה X: אותו מרווח בינלאומי')],
        [{'make': 'Opel', 'names': ['MOKKA', 'MOKKA - X', 'MOKKA X', 'MOKKA FIX'], 'years': [2013, 2019], 'engine_codes': A14}],
        NOTE_14T)
    opel_file('opel-meriva-b-2014-2017-1.4', 'Meriva', 'מריבה', 'B', [2014, 2017], ['1.4 (B14NEL)'],
        [he_src('Meriva_B/2010_2015/2015/manual_user/om_meriva_kta-2690_8-heb_eu_my15_ed0514_22_he_il_online%5BMeriva%5D.pdf', 208, 'ישראל אינה ברשימה האירופית; מרווח בינלאומי 15,000 ק"מ או שנה. אין טבלת פריטים'),
         he_src('Meriva_B/2010_2015/2012/manual_user/om_Meriva_2690_3-en_eu_my12_ed0611_11_he_IL_online.pdf', 185, 'במהדורת 2012 ישראל עוד ברשימה האירופית (30,000 ק"מ או שנה)')],
        [{'make': 'Opel', 'names': ['MERIVA', 'MERIVA B'], 'years': [2013, 2017], 'engine_codes': ['B14NEL', 'B 14 NEL', 'A14NEL', 'A 1.4 NEL']}],
        'מנוע B14NEL (1.4 טורבו בהספק נמוך) אינו מופיע ברשימות ההחלפה של רצועות ושסתומים בטבלה.')
    opel_file('opel-zafira-tourer-2012-2018-1.4-turbo', 'Zafira Tourer', 'זאפירה טורר', 'C', [2012, 2018], ['1.4 Turbo (A14NET/B14NET)'],
        [he_src('Zafira_C/2012_2017/2016/manual_user/om_zafira_tourer_kta-2722_9-heb_eu_my16_ed0815_26_he_il_online%5B_zafira_tourer%5D.pdf', 257, 'ישראל אינה ברשימה האירופית; מרווח בינלאומי 15,000 ק"מ או שנה. אין טבלת פריטים'),
         he_src('Zafira_C/2012_2017/2012_5/manual_user/om_zafira_tourer_kta-2722_1-he_eu_my12_ed0112_6_he_il_online.pdf', 238, 'במהדורת 2012 ישראל עוד ברשימה האירופית (30,000 ק"מ או שנה)')],
        [{'make': 'Opel', 'names': ['ZAFIRA TOURER', 'ZAFIRA'], 'years': [2012, 2018], 'engine_codes': A14}],
        NOTE_14T + NOTE_2012)
    opel_file('opel-insignia-2009-2017-1.6-2.0-turbo', 'Insignia', 'אינסיגניה', 'A', [2011, 2017], ['2.0 Turbo (A20NHT/A20NFT/B20NHT)', '1.6 Turbo (A16XHT/B16SHL)'],
        [he_src('Insignia/2010_2016/2014/manual_user/om_insignia_kta-2675_11-heb_eu_my14_ed0813_36_he_il_online%5Binsignia%5D.pdf', 250, 'ישראל אינה ברשימה האירופית; מרווח בינלאומי 15,000 ק"מ או שנה. אין טבלת פריטים'),
         he_src('Insignia/2010_2016/2011_5/manual_user/Insignia_24_he.pdf', 192, 'במהדורת 2011 ישראל ברשימה האירופית (30,000 ק"מ או שנה)'),
         he_src('Insignia/2010_2016/2010_5/manual_user/Insignia_18_he.pdf', 189, 'במהדורת 2010 ישראל אינה ברשימה האירופית (15,000 ק"מ או שנה)')],
        [{'make': 'Opel', 'names': ['INSIGNIA'], 'years': [2009, 2017], 'engine_codes': ['A 2.0 NHT', 'A20NHT', 'A 2.0 NFT', 'A20NFT', 'B 2.0 NHT', 'B20NHT', 'A 1.6 XHT', 'A16XHT', 'B 16 SHL', 'B16SHL']}],
        'זה הדגם שבספר. במנוע 2.0 טורבו A20NHT המצתים מוחלפים כל 120,000 ק"מ או 8 שנים ורצועת האביזרים כל 150,000 ק"מ או 10 שנים; מנועי A20NFT, A16XHT ו-B16SHL מאוחרים מהספר ואינם ברשימותיו, ולכן חל עליהם מרווח המצתים הכללי (60,000 ק"מ או 4 שנים). ספרי אינסיגניה העבריים שינו את שיוך ישראל בין המהדורות (2010: בינלאומי, 2011: אירופי, 2014: בינלאומי); הקובץ משתמש במרווח הבינלאומי.',
        plugs_note='מרווח כללי; במנוע A20NHT לפי הטבלה 120,000 ק"מ או 8 שנים',
        longx=[LI('drive_belt', 'replace', every_km=150000, every_months=120, note='רק במנוע A20NHT לפי רשימת הטבלה')])
    opel_file('opel-astra-j-2010-2014-1.6', 'Astra', 'אסטרה', 'J', [2010, 2014], ['1.6 (A16XER)', '1.6 Turbo (A16LET)'],
        [he_src('Astra_J/2010_2016/2013/manual_user/om_astra_kta-2685_6-heb_eu_my13_ed0812_18_he_il_online%5Bastra%5D.pdf', 261, 'ישראל אינה ברשימה האירופית; מרווח בינלאומי 15,000 ק"מ או שנה. אין טבלת פריטים'),
         he_src('Astra_J/2010_2016/2012_5/manual_user/om_astra_KTA-2685_5-heb_eu_my12_ed0112_16_he_IL_online.pdf', 218, 'במהדורת 2012 ישראל עוד ברשימה האירופית (30,000 ק"מ או שנה)')],
        [{'make': 'Opel', 'names': ['ASTRA', 'ASTRA SEDAN', 'ASTRA ST', 'TRA BERLINA', 'ASTRA BERLINA'], 'years': [2010, 2015], 'engine_codes': ['A 1.6 XER', 'A16XER', 'A 1.6LET', 'A16LET', 'A 1.6 LET']}],
        'מנועי A16XER ו-A16LET מופיעים בטבלה עצמה: רצועת תזמון וגלגלת מתיחה ורצועת אביזרים כל 150,000 ק"מ או 10 שנים, רצועת משאבת המים וההגה כל 120,000 ק"מ או 10 שנים, ובמנוע A16XER גם בדיקת מרווח שסתומים כל 150,000 ק"מ או 10 שנים. ' + NOTE_2012,
        belts=True, valves=True)
