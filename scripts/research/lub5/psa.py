# Citroen (Lubinski) schedules from the Israeli Hebrew Citroen service & warranty booklet
# ("חוברת השירות והאחריות", edition KGCIT0920 08/2009), published as
# citroen.co.il/_Uploads/dbsAttachedFiles/CitroenWarrantyBook.pdf (archived 2012-05-09).
# Severe-conditions column used (hot >30C / dusty countries are in the booklet's severe list).
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/dl/lub5/gen')
from common import ab_services, write

U_CWB = 'http://citroen.co.il/_Uploads/dbsAttachedFiles/CitroenWarrantyBook.pdf'
U_CWB_WB = 'https://web.archive.org/web/20120509205507/http://citroen.co.il/_Uploads/dbsAttachedFiles/CitroenWarrantyBook.pdf'
IMP_C = 'דוד לובינסקי (סיטרואן)'
IMP_P = 'דוד לובינסקי (פיג\'ו)'

SRC_CWB = {'url': U_CWB_WB, 'kind': 'importer',
           'note': 'חוברת השירות והאחריות העברית של סיטרואן (לובינסקי, מהדורה 08/2009, KGCIT0920) מאתר citroen.co.il, עותק web.archive.org מ-9.5.2012. '
                   'מרווחים לפי סוג מנוע עמ\' 11 (PDF 13), פעולות קבועות בכל טיפול עמ\' 12 (PDF 14), פעולות נוספות לתנאים קשים עמ\' 17-18 (PDF 19-20), רצועת תזמון ומסנן חלקיקים עמ\' 19 (PDF 21)'}

SEVERE_DEF = ('החוברת נותנת שתי תוכניות: רגילה ותנאים קשים. רשימת התנאים הקשים כוללת שימוש מתמשך בארצות חמות (מעל 30 מעלות לעיתים קרובות) ובאזורים מאובקים, '
              'וכן נסיעות קצרות ושימוש עירוני, ולכן נבחרה עמודת התנאים הקשים.')

def routine(diesel):
    rows = [
        ('parking_brake', 'inspect', 'בדיקות בתוך הרכב (בלם חניה, צופר)', 'X'),
        ('lights', 'inspect', 'פנסים ואורות', 'X'),
        ('tires', 'inspect', 'מצב הצמיגים; תוקף ערכת תיקון התקר וחיישני לחץ האוויר אם קיימים', 'X'),
        ('brake_pads', 'inspect', 'בדיקת בטיחות של הבלמים מתחת לרכב', 'X'),
        ('steering', 'inspect', 'בדיקת בטיחות של ההיגוי', 'X'),
        ('body_underside', 'inspect', 'דליפות ממעגלי הנוזלים ומתיבת ההילוכים', 'X'),
        ('washer_fluid', 'inspect', 'השלמה לפי הצורך', 'X'),
        ('brake_fluid', 'inspect', 'מפלס והשלמה לפי הצורך', 'X'),
        ('diagnostics', 'inspect', 'בדיקת מחשבי הרכב, בדיקות הנדרשות לפי החוק, איפוס מחוון השירות ונסיעת מבחן', 'X'),
        ('engine_oil', 'replace', None, 'X'),
        ('oil_filter', 'replace', None, 'X'),
    ]
    if diesel:
        rows.insert(9, ('fuel_filter', 'clean', 'ניקוז מים ומשקעים ממסנן הסולר', 'X'))
    return rows

def svc(interval, n, rows_by_service):
    """rows_by_service: function k -> list of rows (marks 'X')."""
    out = []
    from common import merge_rows
    for k in range(1, n + 1):
        out.append({'km': interval * k, 'items': merge_rows(rows_by_service(k), 'X')})
    return out

def coolant_check(interval):
    return {'item': 'coolant', 'action': 'inspect', 'first_km': 120000, 'first_months': 48,
            'then_every_km': interval, 'then_every_months': 12, 'note': 'בדיקת נוזל הקירור: לראשונה ב-120,000 ק"מ או 4 שנים, ואחר כך בכל טיפול'}

BRAKE = {'item': 'brake_fluid', 'action': 'replace', 'every_months': 24, 'note': 'כל שנתיים'}

# ---------- petrol "other engines" (1.4/1.6 16V TU, 1.6 VTi EP6, THP): severe 20,000 km / 1 year
def petrol_other(belt):
    def rows(k):
        r = routine(False) + [('cabin_filter', 'replace', 'כל 20,000 ק"מ או שנה', 'X')]
        if k % 2 == 0:
            r += [('air_filter', 'replace', 'כל 40,000 ק"מ', 'X'), ('spark_plugs', 'replace', 'כל 40,000 ק"מ', 'X')]
        return r
    li = [BRAKE, coolant_check(20000)]
    if belt:
        li.append({'item': 'timing_belt', 'action': 'replace', 'every_km': 120000, 'every_months': 120,
                   'note': 'מנועי בנזין 1.1-2.2 ל\' בתנאים קשים (בתנאים רגילים 150,000 ק"מ או 10 שנים)'})
    return svc(20000, 2, rows), li

# ---------- 2.0 petrol (EW10): severe 15,000 km / 1 year
def petrol_20():
    def rows(k):
        r = routine(False) + [('cabin_filter', 'replace', 'כל 15,000 ק"מ או שנה', 'X')]
        if k % 3 == 0:
            r += [('air_filter', 'replace', 'כל 45,000 ק"מ', 'X'), ('spark_plugs', 'replace', 'כל 45,000 ק"מ', 'X')]
        return r
    li = [BRAKE, coolant_check(15000),
          {'item': 'timing_belt', 'action': 'replace', 'every_km': 120000, 'every_months': 120,
           'note': 'מנוע בנזין 2.0 ל\' בתנאים קשים (בתנאים רגילים 140,000 ק"מ או 10 שנים)'}]
    return svc(15000, 3, rows), li

# ---------- 2.0 HDi (DW10, not 136 hp): interval 15,000 km / 1 year; extra ops from the "other engines" severe page
def hdi_20():
    def rows(k):
        return routine(True)
    li = [
        {'item': 'fuel_filter', 'action': 'replace', 'every_km': 20000, 'note': 'מסנן סולר - חריג ל-2.0 HDi בתנאים קשים (בשאר המנועים 40,000)'},
        {'item': 'air_filter', 'action': 'replace', 'every_km': 40000},
        {'item': 'cabin_filter', 'action': 'replace', 'every_km': 20000, 'every_months': 12},
        BRAKE, coolant_check(15000),
        {'item': 'timing_belt', 'action': 'replace', 'every_km': 120000, 'every_months': 120,
         'note': '2.0 HDi (לא 136 כ"ס) בתנאים קשים; בתנאים רגילים 150,000 ק"מ או 10 שנים'},
    ]
    return svc(15000, 1, rows), li

def citroen_file(**kw):
    d = {'make': 'Citroen', 'make_he': 'סיטרואן', 'importer': IMP_C, 'time_based': [], 'status': 'reviewed'}
    d.update(kw)
    return d

def peugeot_file(**kw):
    d = {'make': 'Peugeot', 'make_he': "פיג'ו", 'importer': IMP_P, 'time_based': [], 'status': 'draft'}
    d.update(kw)
    return d

SISTER = ('מקור: חוברת השירות והאחריות העברית של סיטרואן מאותו יבואן (לובינסקי), שנותנת תוכנית לפי סוג המנוע; '
          'לא נמצאה חוברת פיג\'ו מקבילה, ולכן זו טיוטה לפי הדגם האחות עם אותו מנוע PSA. ')

def main():
    out = []
    # A. Citroen C4/C3 1.6 16V (TU5, NFU)
    s, li = petrol_other(belt=True)
    out.append(write(citroen_file(
        id='citroen-c4-c3-2004-2010-1.6-16v', model='C4 / C3', model_he='C4 / C3', generation='C4 (B5x) / C3 (FC)',
        years=[2004, 2010], engines=['1.6 16V TU5JP4 (NFU)'], fuel='petrol',
        interval={'km': 20000, 'months': 12, 'note': 'עמודת התנאים הקשים בחוברת היבואן ל"דגמים אחרים ומנועים אחרים": 20,000 ק"מ או שנה (בתנאים רגילים 30,000 ק"מ או שנתיים)'},
        cycle_km=40000, services=s, long_interval=li,
        specs={'timing': 'רצועת תזמון', '_note': 'נבדק מול חוברת השירות והאחריות העברית של סיטרואן (לובינסקי, 2009)'},
        sources=[SRC_CWB],
        notes=('התוכנית לפי חוברת השירות והאחריות העברית של לובינסקי לסיטרואן. ' + SEVERE_DEF +
               ' בכל טיפול: שמן ומסנן שמן, מסנן אוויר לתא הנוסעים ובדיקות הבטיחות והנוזלים. כל 40,000 ק"מ גם מסנן אוויר ומצתים. '
               'נוזל בלמים כל שנתיים; נוזל הקירור נבדק מ-120,000 ק"מ או 4 שנים ואילך בכל טיפול (אין החלפה מתוכננת). רצועת התזמון כל 120,000 ק"מ או 10 שנים. '
               'ברישוי: C4 ו-C3 עם מנוע NFU.'))))
    # B. Citroen 1.6 VTi (EP6, chain)
    s, li = petrol_other(belt=False)
    out.append(write(citroen_file(
        id='citroen-c3-c4-ds3-2009-2015-1.6-vti', model='C3 / C4 / DS3 / C3 Picasso', model_he='C3 / C4 / DS3 / C3 פיקאסו',
        generation='C3 (SC), C4 (B7), DS3, C3 Picasso', years=[2009, 2015], engines=['1.6 VTi 120 EP6 (5FS / 5F01 / 5FW)'], fuel='petrol',
        interval={'km': 20000, 'months': 12, 'note': 'עמודת התנאים הקשים בחוברת היבואן ל"דגמים אחרים ומנועים אחרים": 20,000 ק"מ או שנה (בתנאים רגילים 30,000 ק"מ או שנתיים)'},
        cycle_km=40000, services=s, long_interval=li,
        specs={'timing': 'שרשרת תזמון (החוברת: הנחיית רצועת התזמון אינה חלה על מנועים עם שרשרת)', '_note': 'נבדק מול חוברת השירות והאחריות העברית של סיטרואן (לובינסקי, 2009)'},
        sources=[SRC_CWB],
        notes=('התוכנית לפי חוברת השירות והאחריות העברית של לובינסקי לסיטרואן (מהדורת 2009, שפורסמה באתר סיטרואן ישראל לפחות עד 2012); לדגמי 2013-2015 לא נמצאה מהדורה מאוחרת יותר. ' + SEVERE_DEF +
               ' בכל טיפול: שמן ומסנן שמן, מסנן אוויר לתא הנוסעים ובדיקות הבטיחות והנוזלים. כל 40,000 ק"מ גם מסנן אוויר ומצתים. '
               'נוזל בלמים כל שנתיים; נוזל הקירור נבדק מ-120,000 ק"מ או 4 שנים ואילך בכל טיפול. למנוע VTi שרשרת תזמון. ברישוי: מנועים 5FS, 5F01, 5FW.'))))
    # C. Citroen 2.0 petrol (EW10, RFJ)
    s, li = petrol_20()
    out.append(write(citroen_file(
        id='citroen-c5-c4-picasso-2006-2011-2.0', model='C5 / C4 Picasso / C4', model_he='C5 / C4 פיקאסו / C4',
        generation='C5 (X7), C4 Picasso, C4', years=[2006, 2011], engines=['2.0 16V EW10A (RFJ)'], fuel='petrol',
        interval={'km': 15000, 'months': 12, 'note': 'עמודת התנאים הקשים בחוברת היבואן ל"כל דגמי בנזין 2.0 ל\'": 15,000 ק"מ או שנה (בתנאים רגילים 20,000 ק"מ או שנתיים)'},
        cycle_km=45000, services=s, long_interval=li,
        specs={'timing': 'רצועת תזמון', '_note': 'נבדק מול חוברת השירות והאחריות העברית של סיטרואן (לובינסקי, 2009)'},
        sources=[SRC_CWB],
        notes=('התוכנית לפי חוברת השירות והאחריות העברית של לובינסקי לסיטרואן. ' + SEVERE_DEF +
               ' בכל טיפול: שמן ומסנן שמן, מסנן אוויר לתא הנוסעים ובדיקות הבטיחות והנוזלים. כל 45,000 ק"מ גם מסנן אוויר ומצתים. '
               'נוזל בלמים כל שנתיים; נוזל הקירור נבדק מ-120,000 ק"מ או 4 שנים ואילך בכל טיפול. רצועת התזמון של מנוע 2.0 כל 120,000 ק"מ או 10 שנים. ברישוי: מנוע RFJ.'))))
    # D. Citroen 2.0 HDi (DW10)
    s, li = hdi_20()
    out.append(write(citroen_file(
        id='citroen-jumpy-berlingo-2004-2017-2.0-hdi', model='Jumpy / Berlingo', model_he="ג'אמפי / ברלינגו",
        generation='Jumpy I-II, Berlingo I', years=[2004, 2017], engines=['2.0 HDi DW10 (RH02 / RHK / RHZ / RHY)'], fuel='diesel',
        interval={'km': 15000, 'months': 12, 'note': 'עמודת התנאים הקשים בחוברת היבואן ל"כל דגמי HDi (למעט ג\'אמפי 1.6 HDi)": 15,000 ק"מ או שנה (בתנאים רגילים 20,000 ק"מ או שנתיים)'},
        cycle_km=15000, services=s, long_interval=li,
        specs={'timing': 'רצועת תזמון', '_note': 'נבדק מול חוברת השירות והאחריות העברית של סיטרואן (לובינסקי, 2009)'},
        sources=[SRC_CWB],
        notes=('התוכנית לפי חוברת השירות והאחריות העברית של לובינסקי לסיטרואן (מהדורת 2009); לדגמי ג\'אמפי 2013-2017 (RH02) לא נמצאה מהדורה מאוחרת יותר. ' + SEVERE_DEF +
               ' בכל טיפול (15,000 ק"מ או שנה): שמן ומסנן שמן, ניקוז מים ממסנן הסולר ובדיקות הבטיחות והנוזלים. '
               'לפי דף הפעולות הנוספות לתנאים קשים: מסנן סולר כל 20,000 ק"מ (חריג למנוע 2.0 HDi), מסנן אוויר כל 40,000 ק"מ, מסנן תא נוסעים כל 20,000 ק"מ או שנה, נוזל בלמים כל שנתיים, '
               'ובדיקת נוזל קירור מ-120,000 ק"מ או 4 שנים בכל טיפול. רצועת התזמון של 2.0 HDi (לא 136 כ"ס) כל 120,000 ק"מ או 10 שנים. '
               'מסנן חלקיקים (לפי האבזור): בדיקת מפלס התוסף החל מ-90,000-100,000 ק"מ ובדיקת המסנן החל מ-180,000 ק"מ.'))))
    # ---- Peugeot sisters (draft)
    s, li = petrol_other(belt=False)
    out.append(write(peugeot_file(
        id='peugeot-207-208-308-2008-2016-1.6-vti', model='207 / 208 / 2008 / 308', model_he='207 / 208 / 2008 / 308',
        generation='207, 308 (T7), 208, 2008', years=[2008, 2016], engines=['1.6 VTi 120 EP6 (5FW / 5FS / 5F01)'], fuel='petrol',
        interval={'km': 20000, 'months': 12, 'note': 'לפי חוברת היבואן של סיטרואן לאותו מנוע, עמודת תנאים קשים: 20,000 ק"מ או שנה'},
        cycle_km=40000, services=s, long_interval=li,
        specs={'timing': 'שרשרת תזמון', '_note': 'טיוטה - לפי חוברת סיטרואן של היבואן (דגם אחות, אותו מנוע)'},
        sources=[SRC_CWB],
        notes=(SISTER + SEVERE_DEF + ' כל 20,000 ק"מ או שנה: שמן, מסנן שמן ומסנן תא נוסעים; כל 40,000 ק"מ גם מסנן אוויר ומצתים. נוזל בלמים כל שנתיים. '
               'לדגמי 208/2008 משנת 2013 ואילך החוברת (2009) מוקדמת מהם. ברישוי: 207/308 עם 5FW או 5FS, 208/2008 עם 5F01.'))))
    s, li = petrol_other(belt=True)
    out.append(write(peugeot_file(
        id='peugeot-206-307-partner-2002-2012-1.4-1.6', model='206 / 307 / Partner', model_he='206 / 307 / פרטנר',
        generation='206, 206+, 307, Partner (M59)', years=[2002, 2012], engines=['1.6 16V TU5JP4 (NFU)', '1.4 TU3 (KFW / KFT)'], fuel='petrol',
        interval={'km': 20000, 'months': 12, 'note': 'לפי חוברת היבואן של סיטרואן למנועי TU, עמודת תנאים קשים: 20,000 ק"מ או שנה'},
        cycle_km=40000, services=s, long_interval=li,
        specs={'timing': 'רצועת תזמון', '_note': 'טיוטה - לפי חוברת סיטרואן של היבואן (דגם אחות, אותה משפחת מנועים)'},
        sources=[SRC_CWB],
        notes=(SISTER + SEVERE_DEF + ' כל 20,000 ק"מ או שנה: שמן, מסנן שמן ומסנן תא נוסעים; כל 40,000 ק"מ גם מסנן אוויר ומצתים. נוזל בלמים כל שנתיים. '
               'רצועת תזמון כל 120,000 ק"מ או 10 שנים. ברישוי: 206/307 עם NFU, 206/206+/פרטנר עם KFW או KFT.'))))
    s, li = petrol_20()
    out.append(write(peugeot_file(
        id='peugeot-407-307-2006-2011-2.0', model='407 / 307', model_he='407 / 307', generation='407, 307',
        years=[2006, 2011], engines=['2.0 16V EW10A (RFJ)'], fuel='petrol',
        interval={'km': 15000, 'months': 12, 'note': 'לפי חוברת היבואן של סיטרואן לבנזין 2.0, עמודת תנאים קשים: 15,000 ק"מ או שנה'},
        cycle_km=45000, services=s, long_interval=li,
        specs={'timing': 'רצועת תזמון', '_note': 'טיוטה - לפי חוברת סיטרואן של היבואן (דגם אחות, אותו מנוע)'},
        sources=[SRC_CWB],
        notes=(SISTER + SEVERE_DEF + ' כל 15,000 ק"מ או שנה: שמן, מסנן שמן ומסנן תא נוסעים; כל 45,000 ק"מ גם מסנן אוויר ומצתים. נוזל בלמים כל שנתיים; רצועת תזמון כל 120,000 ק"מ או 10 שנים. ברישוי: מנוע RFJ.'))))
    s, li = petrol_other(belt=True)
    out.append(write(peugeot_file(
        id='peugeot-301-2013-2016-1.6-vti', model='301', model_he='301', generation='301',
        years=[2013, 2016], engines=['1.6 VTi 115 EC5 (NFP)'], fuel='petrol',
        interval={'km': 20000, 'months': 12, 'note': 'לפי חוברת היבואן של סיטרואן (2009) למנועי בנזין "אחרים", עמודת תנאים קשים: 20,000 ק"מ או שנה'},
        cycle_km=40000, services=s, long_interval=li,
        specs={'timing': 'רצועת תזמון', '_note': 'טיוטה - לפי חוברת סיטרואן של היבואן מ-2009; הדגם והמנוע מאוחרים לחוברת'},
        sources=[SRC_CWB],
        notes=(SISTER + 'מנוע EC5 (NFP) הוא גלגול של מנוע TU5 עם רצועת תזמון, אבל החוברת (2009) קודמת לו, ולכן הערכים כאן הם של קטגוריית "מנועי בנזין אחרים". ' + SEVERE_DEF +
               ' כל 20,000 ק"מ או שנה: שמן, מסנן שמן ומסנן תא נוסעים; כל 40,000 ק"מ גם מסנן אוויר ומצתים; רצועת תזמון כל 120,000 ק"מ או 10 שנים.'))))
    s, li = petrol_other(belt=True)
    d = citroen_file(
        id='citroen-c-elysee-2013-2014-1.6-vti', model='C-Elysee', model_he='C-אליזה', generation='C-Elysee',
        years=[2013, 2014], engines=['1.6 VTi 115 EC5 (NFP)'], fuel='petrol',
        interval={'km': 20000, 'months': 12, 'note': 'לפי חוברת היבואן של סיטרואן (2009) למנועי בנזין "אחרים", עמודת תנאים קשים: 20,000 ק"מ או שנה'},
        cycle_km=40000, services=s, long_interval=li,
        specs={'timing': 'רצועת תזמון', '_note': 'טיוטה - חוברת סיטרואן של היבואן מ-2009 קודמת לדגם'},
        sources=[SRC_CWB],
        notes=('התוכנית לפי חוברת השירות והאחריות העברית של לובינסקי לסיטרואן (2009). הדגם והמנוע EC5 (NFP) מאוחרים לחוברת, ולכן זו טיוטה לפי קטגוריית "מנועי בנזין אחרים". ' + SEVERE_DEF +
               ' כל 20,000 ק"מ או שנה: שמן, מסנן שמן ומסנן תא נוסעים; כל 40,000 ק"מ גם מסנן אוויר ומצתים; רצועת תזמון כל 120,000 ק"מ או 10 שנים.'))
    d['status'] = 'draft'
    out.append(write(d))
    for p in out: print(p)

if __name__ == '__main__':
    main()

# ---------- 1.6 HDi (DV6), all vehicles except Jumpy: severe 15,000 km / 1 year (booklet p.17)
def hdi_16():
    def rows(k):
        r = routine(True) + [('cabin_filter', 'replace', 'כל 15,000 ק"מ או שנה', 'X')]
        if k % 2 == 0:
            r.append(('air_filter', 'replace', 'כל 30,000 ק"מ', 'X'))
        if k % 3 == 0:
            r.append(('fuel_filter', 'replace', 'מסנן סולר כל 45,000 ק"מ', 'X'))
        return r
    li = [BRAKE, coolant_check(15000),
          {'item': 'timing_belt', 'action': 'replace', 'every_km': 180000, 'every_months': 120,
           'note': '1.6 HDi בתנאים קשים (בתנאים רגילים 240,000 ק"מ או 10 שנים)'}]
    return svc(15000, 6, rows), li

# ---------- Jumpy 1.6 HDi: "other engines" severe 20,000 km / 1 year
def hdi_16_jumpy():
    def rows(k):
        r = routine(True) + [('cabin_filter', 'replace', 'כל 20,000 ק"מ או שנה', 'X')]
        if k % 2 == 0:
            r += [('fuel_filter', 'replace', 'מסנן סולר כל 40,000 ק"מ', 'X'), ('air_filter', 'replace', 'כל 40,000 ק"מ', 'X')]
        return r
    li = [BRAKE, coolant_check(20000),
          {'item': 'timing_belt', 'action': 'replace', 'every_km': 180000, 'every_months': 120,
           'note': '1.6 HDi בתנאים קשים (בתנאים רגילים 240,000 ק"מ או 10 שנים)'},
          {'item': 'exhaust', 'action': 'inspect', 'every_km': 120000,
           'note': 'מסנן חלקיקים: מילוי מיכל התוסף למפלס המרבי או החלפת שקית התוסף (ג\'אמפי 1.6)'}]
    return svc(20000, 2, rows), li

def main2():
    out = []
    s, li = hdi_16()
    out.append(write(citroen_file(
        id='citroen-berlingo-c3-c4-2008-2013-1.6-hdi', model='Berlingo / C3 Picasso / C3 / C4', model_he='ברלינגו / C3 פיקאסו / C3 / C4',
        generation='Berlingo II (B9), C3 Picasso, C3, C4', years=[2008, 2013], engines=['1.6 HDi DV6 (9HX / 9HW / 9H02 / 9HP / 9HN / 9H06 / 9HF / 9HR / 9H05)'], fuel='diesel',
        interval={'km': 15000, 'months': 12, 'note': 'עמודת התנאים הקשים בחוברת היבואן ל"כל דגמי HDi (למעט ג\'אמפי 1.6 HDi)": 15,000 ק"מ או שנה (בתנאים רגילים 20,000 ק"מ או שנתיים)'},
        cycle_km=90000, services=s, long_interval=li,
        specs={'timing': 'רצועת תזמון', '_note': 'נבדק מול חוברת השירות והאחריות העברית של סיטרואן (לובינסקי, 2009)'},
        sources=[SRC_CWB],
        notes=('התוכנית לפי חוברת השירות והאחריות העברית של לובינסקי לסיטרואן (מהדורת 2009). ' + SEVERE_DEF +
               ' בכל טיפול (15,000 ק"מ או שנה): שמן ומסנן שמן, מסנן תא נוסעים, ניקוז מים ממסנן הסולר ובדיקות הבטיחות והנוזלים. מסנן אוויר כל 30,000 ק"מ ומסנן סולר כל 45,000 ק"מ. '
               'נוזל בלמים כל שנתיים; נוזל הקירור נבדק מ-120,000 ק"מ או 4 שנים בכל טיפול. רצועת התזמון של 1.6 HDi כל 180,000 ק"מ או 10 שנים. '
               'מסנן חלקיקים (לפי האבזור): בדיקת מפלס התוסף החל מ-90,000-100,000 ק"מ; בדיקת המסנן החל מ-160,000 ק"מ בברלינגו ומ-180,000 ק"מ בשאר הדגמים. '
               'לרכבים עם מצלמת סטייה מנתיב: בדיקה חזותית של החיישנים כל 20,000 ק"מ.'))))
    s, li = hdi_16_jumpy()
    out.append(write(citroen_file(
        id='citroen-jumpy-2007-2012-1.6-hdi', model='Jumpy', model_he="ג'אמפי", generation='Jumpy II',
        years=[2007, 2012], engines=['1.6 HDi 90 DV6 (9HU)'], fuel='diesel',
        interval={'km': 20000, 'months': 12, 'note': 'לג\'אמפי 1.6 HDi החוברת קובעת את מרווחי "דגמים אחרים": בתנאים קשים 20,000 ק"מ או שנה (בתנאים רגילים 30,000 ק"מ או שנתיים)'},
        cycle_km=40000, services=s, long_interval=li,
        specs={'timing': 'רצועת תזמון', '_note': 'נבדק מול חוברת השירות והאחריות העברית של סיטרואן (לובינסקי, 2009)'},
        sources=[SRC_CWB],
        notes=('התוכנית לפי חוברת השירות והאחריות העברית של לובינסקי לסיטרואן (מהדורת 2009). החוברת מוציאה את ג\'אמפי 1.6 HDi מקבוצת ה-HDi ושמה אותו במרווחי "דגמים אחרים". ' + SEVERE_DEF +
               ' בכל טיפול (20,000 ק"מ או שנה): שמן ומסנן שמן, מסנן תא נוסעים, ניקוז מים ממסנן הסולר ובדיקות הבטיחות והנוזלים; כל 40,000 ק"מ גם מסנן סולר ומסנן אוויר. '
               'נוזל בלמים כל שנתיים; נוזל הקירור נבדק מ-120,000 ק"מ או 4 שנים בכל טיפול. רצועת תזמון כל 180,000 ק"מ או 10 שנים. '
               'מסנן חלקיקים: מילוי התוסף או החלפת שקית התוסף כל 120,000 ק"מ ובדיקת המסנן החל מ-180,000 ק"מ (לפי האבזור). ברישוי: JUMPY HDI עם מנוע 9HU.'))))
    for p in out: print(p)

if __name__ == '__main__':
    main2()
