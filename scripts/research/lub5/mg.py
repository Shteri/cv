# MG (Car East / Lubinski) schedules from the Israeli Hebrew service & warranty booklets.
# Marks (A/B) were read with mgparse.py (bullet x-position vs the A/B header) and checked on page renders.
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/dl/lub5/gen')
from common import ab_services, write

M = 'https://media.mg-israel.co.il/wp-content/uploads/2020/10/'
U_BEV26 = M + 'Warranty-MG-7Y-BEV-PHEV-HEV-Update-08.2026-He-Web.pdf'
U_BEV25 = 'https://mg-israel.co.il/wp-content/uploads/2020/10/Warranty-MG-7Y-BEV-PHEV-HEV-He-11.2025.3.2-idkun-12.2025.pdf'
U_MG3H24 = M + 'Warranty-MG3-7Y-09.2024_Web-2.pdf'
U_ZSH24 = M + 'MGZS-Hybrid-Ahrayut-11_2024-Web.pdf'
U_FUEL = M + 'MG-Nispah-Massnen-Delek-04.2025.pdf'
U_BENZ26 = M + 'Warranty-MG-5Y-BENZINE-Update-06.2026-He-Web.pdf'
U_BENZ25 = 'https://mg-israel.co.il/wp-content/uploads/2020/10/MG-Warranty-5Y-MG3-MG-ZS-MG-HS-He-Web-14.08.2025.pdf'
U_5Y24 = M + 'Warranty-MG-5Y-He-2024-idkun-12.2025.pdf'
U_7Y24 = M + 'Warranty-MG-7Y-He-06.2024-idkun-12.2025.pdf'
U_ZSEV_COST = 'https://mg-israel.co.il/wp-content/uploads/2020/10/Doc1-1.pdf'
U_WARR_PAGE = 'https://mg-israel.co.il/mg_warranty/'
IMP = 'קאר איסט (קבוצת לובינסקי)'

# ---------------- hybrid / PHEV table (2026 booklet pp.14-17 printed; MG3/ZS Hybrid 2024 booklets pp.8-11 printed)
HEV_ROWS = [
    ('parking_brake', 'inspect', 'בדיקת פעולה וכיוון לפי הצורך', 'AB'),
    ('lights', 'inspect', 'תאורה פנימית וחיצונית, צופר ונוריות חיווי', 'AB'),
    ('wipers', 'inspect', 'מגבים, מתזים ושמשה קדמית', 'AB'),
    ('seat_belts', 'inspect', 'חגורות בטיחות', 'AB'),
    ('ac_system', 'inspect', 'פעולת המיזוג', 'AB'),
    ('cabin_filter', 'replace', None, 'B'),
    ('seat_belts', 'inspect', 'מצב ותפקוד המושבים', 'AB'),
    ('door_hinges', 'inspect', 'תפס מכסה מנוע, מנעולי דלתות ותא מטען, צירים ומעצורים - ניקוי ושימון לפי הצורך', 'AB'),
    ('hybrid_battery_filter', 'replace', 'אלמנט מסנן האוויר של מארז סוללת המתח הגבוה', 'B'),
    ('battery_12v', 'inspect', 'מחברים, עיגון ומצב', 'AB'),
    ('washer_fluid', 'inspect', 'מפלס', 'AB'),
    ('brake_fluid', 'inspect', 'מפלס', 'AB'),
    ('transmission_oil', 'inspect', 'מפלס נוזל תמסורת ההנעה החשמלית', 'AB'),
    ('cooling_system', 'inspect', 'צנרת, מצנן ומאוורר; ניקוי לפי הצורך', 'AB'),
    ('coolant', 'inspect', 'מפלס וריכוז', 'AB'),
    ('exhaust', 'inspect', 'סעפת יניקה וסעפת פליטה', 'B'),
    ('ac_system', 'inspect', 'מדחס, צנרת ומעבה - ניקוי לפי הצורך', 'AB'),
    ('brake_lines', 'inspect', 'מגבר בלמים וצינורו', 'AB'),
    ('air_filter', 'replace', None, 'B'),
    ('body_underside', 'inspect', 'תושבות המנוע', 'B'),
    ('hybrid_system', 'inspect', 'רתמות ומחברי מתח גבוה/נמוך', 'AB'),
    ('engine_oil', 'replace', None, 'AB'),
    ('oil_filter', 'replace', None, 'AB'),
    ('transmission_oil', 'inspect', 'דליפות שמן מהמנוע ומתמסורת ההנעה החשמלית', 'AB'),
    ('exhaust', 'inspect', 'מערכת הפליטה, תושבות ומגני חום', 'B'),
    ('fuel_lines', 'inspect', 'מעיכות ודליפות', 'AB'),
    ('evap_system', 'inspect', 'צינורות ומכל הפחם הפעיל', 'B'),
    ('brake_pads', 'inspect', 'קדמיות ואחוריות, כולל קליפרים', 'AB'),
    ('brake_discs', 'inspect', None, 'AB'),
    ('brake_lines', 'inspect', 'צינורות קשיחים וגמישים ועיגונם', 'AB'),
    ('cv_boots', 'inspect', 'מסבי גלגלים ושרוולי גלי הינע', 'AB'),
    ('suspension', 'inspect', 'חיבורים, חופשים, דליפות ובלאי', 'AB'),
    ('steering', 'inspect', None, 'AB'),
    ('tires', 'inspect', 'עומק חריץ ובלאי חריג; לחץ אוויר כולל רזרבי', 'AB'),
    ('wheel_alignment', 'inspect', 'בדיקת זוויות; החלפה בין גלגלים קדמיים ואחוריים לפי הצורך', 'AB'),
    ('body_underside', 'inspect', 'ברגים ואומים בשלדה ובתחתית', 'AB'),
    ('cooling_system', 'inspect', 'מיקום תפסי צינורות הקירור ואטימה', 'AB'),
    ('hybrid_system', 'inspect', 'סוללת מתח גבוה: סימון ברגי עיגון, מארז ותושבת, שסתום פריקה; מתג שירות ידני', 'AB'),
    ('diagnostics', 'inspect', 'קריאה ומחיקה של קודי תקלה, עדכון תוכנה לפי הודעת יצרן ונסיעת מבחן', 'AB'),
]
PHEV_ROWS = [r for r in HEV_ROWS if r[0] != 'hybrid_battery_filter']

# ---------------- EV table (2026 booklet pp.8-10 printed)
EV26_ROWS = [
    ('parking_brake', 'inspect', 'בדיקת פעולה וכיוון לפי הצורך', 'AB'),
    ('lights', 'inspect', 'תאורה פנימית וחיצונית, צופר ונוריות חיווי', 'AB'),
    ('wipers', 'inspect', 'מגבים, מתזים ושמשה קדמית', 'AB'),
    ('seat_belts', 'inspect', 'חגורות בטיחות', 'AB'),
    ('ac_system', 'inspect', 'פעולת המיזוג', 'AB'),
    ('cabin_filter', 'replace', None, 'B'),
    ('seat_belts', 'inspect', 'מצב ותפקוד המושבים', 'AB'),
    ('door_hinges', 'inspect', 'מנעולי מכסה מנוע, דלתות ותא מטען, צירים - ניקוי ושימון לפי הצורך', 'AB'),
    ('battery_12v', 'inspect', 'מצב והידוק מחברים', 'AB'),
    ('hybrid_system', 'inspect', 'מחבר שירות ידני; רתמות, מחברים וחיבורי מתח גבוה/נמוך', 'AB'),
    ('washer_fluid', 'inspect', 'מפלס', 'AB'),
    ('brake_fluid', 'inspect', 'מפלס', 'AB'),
    ('cooling_system', 'inspect', 'צנרת, מצנן ומאוורר; ניקוי לפי הצורך', 'AB'),
    ('coolant', 'inspect', 'מפלס וריכוז', 'B'),
    ('ac_system', 'inspect', 'מדחס, צנרת ומעבה - ניקוי לפי הצורך', 'AB'),
    ('brake_lines', 'inspect', 'מגבר הבלמים', 'AB'),
    ('hybrid_system', 'inspect', 'סוללת מתח גבוה: שסתום אוורור, סימון ברגי עיגון, מארז ותושבות, כבל הארקה', 'AB'),
    ('transmission_oil', 'inspect', 'תושבות ממסרת ההינע החשמלי', 'AB'),
    ('cooling_system', 'inspect', 'מהדקי ומחברי צינורות הקירור', 'AB'),
    ('brake_pads', 'inspect', 'קדמיות ואחוריות, כולל קליפרים', 'AB'),
    ('brake_discs', 'inspect', None, 'AB'),
    ('brake_lines', 'inspect', 'צינורות קשיחים וגמישים ועיגונם', 'AB'),
    ('cv_boots', 'inspect', 'מסבי גלגלים וגומיות גלי הינע', 'AB'),
    ('suspension', 'inspect', 'דליפות ובלאי', 'AB'),
    ('steering', 'inspect', None, 'AB'),
    ('tires', 'inspect', 'עומק חריץ, נזק ובלאי לא אחיד; לחץ אוויר; כולל רזרבי אם יש', 'AB'),
    ('wheel_alignment', 'inspect', 'בדיקת זוויות; החלפה בין גלגלים קדמיים ואחוריים לפי הצורך', 'AB'),
    ('body_underside', 'inspect', 'ברגים ואומים בשלדה ובתחתית', 'AB'),
    ('transmission_oil', 'inspect', 'מפלס נוזל תמסורת ההנעה החשמלית', 'AB'),
    ('diagnostics', 'inspect', 'איפוס מונה טיפולים, קודי תקלה, עדכון תוכנה לפי הודעת יצרן, בדיקת איזון תאי הסוללה ונסיעת מבחן', 'AB'),
]

# ---------------- 2024 booklets (5Y and 7Y, identical maintenance chapter) - EV table pp.12-14 printed
EV24_ROWS = [
    ('parking_brake', 'inspect', 'בדיקת פעולה וכיוון לפי הצורך', 'AB'),
    ('lights', 'inspect', 'תאורה פנימית וחיצונית, צופר ונוריות חיווי', 'AB'),
    ('wipers', 'inspect', 'מגבים, מתזים ושמשה קדמית', 'AB'),
    ('seat_belts', 'inspect', 'חגורות בטיחות', 'AB'),
    ('ac_system', 'inspect', 'פעולת המיזוג', 'AB'),
    ('cabin_filter', 'replace', None, 'B'),
    ('seat_belts', 'inspect', 'מצב ותפקוד המושבים', 'AB'),
    ('door_hinges', 'inspect', 'מנעולי מכסה מנוע, דלתות ותא מטען, צירים - ניקוי ושימון לפי הצורך', 'AB'),
    ('battery_12v', 'inspect', 'תקינות', 'AB'),
    ('hybrid_system', 'inspect', 'רתמות, חיבורים ומחברי מתח גבוה/נמוך; מחבר שירות ידני', 'AB'),
    ('washer_fluid', 'inspect', 'מפלס', 'AB'),
    ('brake_fluid', 'inspect', 'מפלס', 'AB'),
    ('cooling_system', 'inspect', 'צנרת, מצנן ומאוורר; ניקוי לפי הצורך', 'AB'),
    ('coolant', 'inspect', 'מפלס וריכוז', 'B'),
    ('ac_system', 'inspect', 'מדחס, צנרת ומעבה - ניקוי לפי הצורך', 'AB'),
    ('brake_lines', 'inspect', 'מגבר הבלמים', 'AB'),
    ('transmission_oil', 'inspect', 'תושבות ממסרת ההינע החשמלי', 'AB'),
    ('hybrid_system', 'inspect', 'סוללת מתח גבוה: שסתום אוורור, סימון ברגי עיגון, מארז ותושבות, כבל הארקה', 'AB'),
    ('cooling_system', 'inspect', 'מהדקי ומחברי צינורות הקירור', 'AB'),
    ('brake_pads', 'inspect', 'קדמיות ואחוריות, כולל קליפרים', 'AB'),
    ('brake_discs', 'inspect', None, 'AB'),
    ('brake_lines', 'inspect', 'צינורות קשיחים וגמישים ועיגונם', 'AB'),
    ('cv_boots', 'inspect', 'מסבי גלגלים וגומיות גלי הינע', 'AB'),
    ('suspension', 'inspect', 'דליפות ובלאי', 'AB'),
    ('steering', 'inspect', None, 'AB'),
    ('tires', 'inspect', 'עומק חריץ, נזק ובלאי לא אחיד; לחץ אוויר', 'AB'),
    ('wheel_alignment', 'inspect', 'בדיקת זוויות; החלפה בין גלגלים קדמיים ואחוריים לפי הצורך', 'AB'),
    ('body_underside', 'inspect', 'ברגים ואומים בשלדה ובתחתית', 'AB'),
    ('transmission_oil', 'inspect', 'מפלס נוזל התמסורת', 'AB'),
    ('diagnostics', 'inspect', 'איפוס מונה טיפולים, קודי תקלה, עדכון תוכנה, בדיקת איזון תאי הסוללה ונסיעת מבחן', 'AB'),
]

# ---------------- 2024 booklets - hybrid (EHS PHEV) table pp.8-11 printed
EHS24_ROWS = [
    ('parking_brake', 'inspect', 'בדיקת פעולה וכיוון לפי הצורך', 'AB'),
    ('lights', 'inspect', 'תאורה פנימית וחיצונית, צופר ונוריות חיווי', 'AB'),
    ('wipers', 'inspect', 'מגבים, מתזים ושמשה קדמית', 'AB'),
    ('seat_belts', 'inspect', 'חגורות בטיחות', 'AB'),
    ('ac_system', 'inspect', 'פעולת המיזוג', 'AB'),
    ('cabin_filter', 'replace', None, 'B'),
    ('seat_belts', 'inspect', 'מצב ותפקוד המושבים', 'AB'),
    ('door_hinges', 'inspect', 'מנעולי מכסה מנוע, דלתות ותא מטען, צירים - ניקוי ושימון לפי הצורך', 'AB'),
    ('battery_12v', 'inspect', 'מצב והידוק מחברים', 'AB'),
    ('washer_fluid', 'inspect', 'מפלס', 'AB'),
    ('brake_fluid', 'inspect', 'מפלס', 'AB'),
    ('transmission_oil', 'inspect', 'מפלס נוזל התמסורת', 'AB'),
    ('cooling_system', 'inspect', 'צנרת, מצנן ומאוורר; ניקוי לפי הצורך', 'AB'),
    ('coolant', 'inspect', 'מפלס וריכוז', 'AB'),
    ('intercooler_pipes', 'inspect', 'סעפת היניקה של המנוע', 'B'),
    ('drive_belt', 'inspect', 'רצועת האביזרים', 'AB'),
    ('ac_system', 'inspect', 'מדחס, צנרת ומעבה - ניקוי לפי הצורך', 'AB'),
    ('brake_lines', 'inspect', 'מגבר הבלמים', 'AB'),
    ('air_filter', 'replace', None, 'B'),
    ('body_underside', 'inspect', 'תושבות המנוע', 'B'),
    ('hybrid_system', 'inspect', 'רתמת מתח גבוה ושקע הטעינה', 'AB'),
    ('engine_oil', 'replace', None, 'AB'),
    ('oil_filter', 'replace', None, 'AB'),
    ('transmission_oil', 'inspect', 'דליפות שמן מהמנוע ומתיבת ההילוכים החשמלית', 'AB'),
    ('exhaust', 'inspect', 'מערכת הפליטה, תושבות ומגני חום', 'B'),
    ('fuel_lines', 'inspect', 'כיפופים ודליפות', 'AB'),
    ('evap_system', 'inspect', 'צנרת ומסנן הקניסטר', 'B'),
    ('brake_pads', 'inspect', 'קדמיות ואחוריות, כולל קליפרים', 'AB'),
    ('brake_discs', 'inspect', None, 'AB'),
    ('brake_lines', 'inspect', 'צינורות קשיחים וגמישים ועיגונם', 'AB'),
    ('cv_boots', 'inspect', 'מסבי גלגלים וגומיות גלי הינע', 'AB'),
    ('suspension', 'inspect', 'דליפות ובלאי', 'AB'),
    ('steering', 'inspect', None, 'AB'),
    ('tires', 'inspect', 'עומק חריץ, נזק ובלאי לא אחיד; לחץ אוויר', 'AB'),
    ('wheel_alignment', 'inspect', 'בדיקת זוויות; החלפה בין גלגלים קדמיים ואחוריים לפי הצורך', 'AB'),
    ('body_underside', 'inspect', 'ברגים ואומים בשלדה ובתחתית', 'AB'),
    ('cooling_system', 'inspect', 'מהדקי ומחברי צינורות הקירור', 'AB'),
    ('hybrid_system', 'inspect', 'סוללת מתח גבוה: סימון ברגי עיגון, מארז ותושבות, כבלים ומחברים, שסתום אוורור, מחבר שירות ידני', 'AB'),
    ('diagnostics', 'inspect', 'איפוס מונה טיפולים, קודי תקלה, עדכון תוכנה, בדיקת איזון תאי הסוללה ונסיעת מבחן', 'AB'),
]

# ---------------- petrol table (petrol booklet 06.2026 pp.8-10 printed)
ICE_ROWS = [
    ('parking_brake', 'inspect', 'בדיקת פעולה וכיוון לפי הצורך', 'AB'),
    ('lights', 'inspect', 'תאורה פנימית וחיצונית, צופר ונוריות חיווי', 'AB'),
    ('wipers', 'inspect', 'מגבים, מתזים ושמשה קדמית', 'AB'),
    ('seat_belts', 'inspect', 'חגורות בטיחות', 'AB'),
    ('ac_system', 'inspect', 'פעולת המיזוג', 'AB'),
    ('cabin_filter', 'replace', None, 'B'),
    ('seat_belts', 'inspect', 'מצב ותפקוד המושבים', 'AB'),
    ('door_hinges', 'inspect', 'מנעולי מכסה מנוע, דלתות ותא מטען, צירים - ניקוי ושימון לפי הצורך', 'AB'),
    ('battery_12v', 'inspect', 'מצב והידוק מחברים', 'AB'),
    ('washer_fluid', 'inspect', 'מפלס', 'AB'),
    ('brake_fluid', 'inspect', 'מפלס', 'AB'),
    ('transmission_oil', 'inspect', 'מפלס נוזל התמסורת', 'AB'),
    ('cooling_system', 'inspect', 'צנרת, מצנן ומאוורר; ניקוי לפי הצורך', 'AB'),
    ('coolant', 'inspect', 'מפלס וריכוז', 'AB'),
    ('exhaust', 'inspect', 'סעפות היניקה והפליטה', 'B'),
    ('drive_belt', 'inspect', 'רצועת האביזרים', 'AB'),
    ('ac_system', 'inspect', 'מדחס, צנרת ומעבה - ניקוי לפי הצורך', 'AB'),
    ('brake_lines', 'inspect', 'מגבר הבלמים', 'AB'),
    ('air_filter', 'replace', None, 'B'),
    ('body_underside', 'inspect', 'תושבות המנוע', 'B'),
    ('electrical_system', 'inspect', 'רתמות החשמל של המנוע', 'AB'),
    ('engine_oil', 'replace', None, 'AB'),
    ('oil_filter', 'replace', None, 'AB'),
    ('transmission_oil', 'inspect', 'דליפות שמן מהמנוע ומתיבת ההילוכים', 'AB'),
    ('exhaust', 'inspect', 'מערכת הפליטה, תושבות ומגני חום', 'B'),
    ('fuel_lines', 'inspect', 'כיפופים ודליפות', 'AB'),
    ('evap_system', 'inspect', 'צנרת ומסנן הקניסטר', 'AB'),
    ('brake_pads', 'inspect', 'קדמיות ואחוריות, כולל קליפרים', 'AB'),
    ('brake_discs', 'inspect', None, 'AB'),
    ('brake_lines', 'inspect', 'צינורות קשיחים וגמישים ועיגונם', 'AB'),
    ('cv_boots', 'inspect', 'מסבי גלגלים וגומיות גלי הינע', 'AB'),
    ('suspension', 'inspect', 'דליפות ובלאי', 'AB'),
    ('steering', 'inspect', None, 'AB'),
    ('tires', 'inspect', 'עומק חריץ, נזק ובלאי לא אחיד; לחץ אוויר; כולל רזרבי אם יש', 'AB'),
    ('wheel_alignment', 'inspect', 'בדיקת זוויות; החלפה בין גלגלים קדמיים ואחוריים לפי הצורך', 'AB'),
    ('body_underside', 'inspect', 'ברגים ואומים בשלדה ובתחתית', 'AB'),
    ('diagnostics', 'inspect', 'איפוס מונה טיפולים, קודי תקלה, עדכון תוכנה לפי הודעת יצרן ונסיעת מבחן', 'AB'),
]

BRAKE2Y = {'item': 'brake_fluid', 'action': 'replace', 'every_months': 24, 'note': 'כל שנתיים בלי קשר לק"מ'}
SEVERE_HEV = ('בתנאי שימוש קשים (טמפרטורות מתחת ל-0 או מעל 40 מעלות, אבק וחול, הרים, לחות ושלוליות, מונית/משטרה/גרירה) '
              'הספר מוסיף: נוזל בלמים כל 40,000 ק"מ או שנה, בדיקת מסנן המזגן כל 5,000 ק"מ באזורים מאובקים, ובדיקת רפידות ודיסקים לעיתים קרובות יותר; '
              'ובכל ביקור יש לבצע את בדיקות טיפול B.')

def mg_base(**kw):
    d = {'make': 'MG', 'make_he': "אם.ג'י", 'importer': IMP, 'time_based': [], 'status': 'reviewed'}
    d.update(kw)
    return d

def hev_li(model_note, trans_filter):
    li = [
        {'item': 'transmission_oil', 'action': 'replace', 'every_km': 80000,
         'note': 'נוזל תיבת ההנעה החשמלית' + ('; לפי חוברת 2026 מחליפים באותו מועד גם את מסנן היניקה ומסנן הלחץ של התיבה' if trans_filter else '')},
        BRAKE2Y,
        {'item': 'coolant', 'action': 'replace', 'every_km': 100000, 'every_months': 48, 'note': 'המוקדם מביניהם'},
        {'item': 'fuel_filter', 'action': 'replace', 'every_km': 100000, 'every_months': 96,
         'note': 'המסנן משולב במשאבת הדלק; 8 שנים לפי נספח התיקון של קאר איסט (04.2025) וחוברת 2026'},
        {'item': 'spark_plugs', 'action': 'replace', 'every_km': 40000},
    ]
    return li

# ======================= MG3 Hybrid+ =======================
def mg3_hybrid():
    d = mg_base(
        id='mg-3-hybrid-2024-2026-1.5-hybrid', model='MG3 Hybrid+', model_he='MG3 היברידי', generation='MG3 (2024+) Hybrid+',
        years=[2024, 2026], engines=['1.5 hybrid (15FHC)'], fuel='hybrid',
        interval={'km': 15000, 'months': 12, 'note': 'לפי חוברת השירות והאחריות של קאר איסט: טיפול A ב-15,000 ק"מ/12 חודשים, טיפול B ב-30,000 ק"מ/24 חודשים, וחוזר חלילה; המוקדם מביניהם. מותרת חריגה של עד 1,500 ק"מ או 28 ימים'},
        cycle_km=120000,
        services=ab_services(15000, 8, HEV_ROWS),
        long_interval=hev_li('MG3', True),
        specs={'warranty': '7 שנים או 150,000 ק"מ לרכב; סוללת מתח גבוה 8 שנים או 150,000 ק"מ (חוברת 09.2024)',
               '_note': 'נבדק מול חוברת השירות והאחריות העברית של קאר איסט ל-MG3 Hybrid ומול חוברת 2026 לדגמים היברידיים'},
        sources=[
            {'url': U_MG3H24, 'kind': 'importer', 'note': 'חוברת שירות ואחריות MG3 Hybrid (09.2024): מרווחים עמ\' 7 (PDF 9), מפרט A/B עמ\' 8-11 (PDF 10-13), פריטים מיוחדים עמ\' 12 (PDF 14), תנאים קשים עמ\' 13'},
            {'url': U_FUEL, 'kind': 'importer', 'note': 'נספח 04.2025: מסנן הדלק ב-MG3 Hybrid וב-ZS Hybrid מוחלף כל 8 שנים או 100,000 ק"מ (ולא 4 שנים כפי שנדפס)'},
            {'url': U_BEV26, 'kind': 'importer', 'note': 'חוברת 7 שנים לחשמליים/היברידיים/פלאג-אין (עדכון 08.2026): טבלת היברידיים עמ\' 13-19 (PDF 15-21) - אותו מפרט; מוסיפה מסנני יניקה ולחץ של התיבה כל 80,000 ק"מ ל-ZS HEV ול-MG3 HEV'},
            {'url': U_WARR_PAGE, 'kind': 'importer', 'note': 'עמוד האחריות של MG ישראל שממנו מקושרות החוברות'},
        ],
        notes=('התוכנית הועתקה מחוברת השירות והאחריות העברית של קאר איסט. טיפול A וטיפול B מתחלפים כל 15,000 ק"מ או שנה. '
               'בטיפול B בלבד מוחלפים מסנן המזגן, מסנן האוויר של המנוע ומסנן האוויר של מארז סוללת המתח הגבוה, ונבדקות גם מערכת הפליטה, הסעפות, מערכת אדי הדלק ותושבות המנוע. '
               'שמן ומסנן שמן מוחלפים בכל טיפול. פריטים מיוחדים: נוזל תיבת ההנעה החשמלית כל 80,000 ק"מ, נוזל בלמים כל שנתיים, נוזל קירור כל 4 שנים או 100,000 ק"מ, מצתים כל 40,000 ק"מ, '
               'ומסנן דלק (בתוך משאבת הדלק) כל 8 שנים או 100,000 ק"מ - בחוברת 09.2024 נדפס 4 שנים, והיבואן תיקן זאת בנספח. ' + SEVERE_HEV),
    )
    return write(d)

# ======================= ZS Hybrid+ =======================
def zs_hybrid():
    d = mg_base(
        id='mg-zs-hybrid-2025-2026-1.5-hybrid', model='ZS Hybrid+', model_he='ZS היברידי', generation='ZS (2024+) Hybrid+',
        years=[2025, 2026], engines=['1.5 hybrid (15FHC)'], fuel='hybrid',
        interval={'km': 15000, 'months': 12, 'note': 'לפי חוברת השירות והאחריות של קאר איסט: טיפול A ב-15,000 ק"מ/12 חודשים, טיפול B ב-30,000 ק"מ/24 חודשים, וחוזר חלילה; המוקדם מביניהם. מותרת חריגה של עד 1,500 ק"מ או 28 ימים'},
        cycle_km=120000,
        services=ab_services(15000, 8, HEV_ROWS),
        long_interval=hev_li('ZS', True),
        specs={'warranty': '7 שנים או 150,000 ק"מ (חוברת 11.2024)',
               '_note': 'נבדק מול חוברת השירות והאחריות העברית של קאר איסט ל-ZS Hybrid ומול חוברת 2026 לדגמים היברידיים'},
        sources=[
            {'url': U_ZSH24, 'kind': 'importer', 'note': 'חוברת שירות ואחריות MG ZS Hybrid (11.2024): מרווחים עמ\' 7 (PDF 9), מפרט A/B עמ\' 8-11 (PDF 10-13), פריטים מיוחדים עמ\' 12 (PDF 14)'},
            {'url': U_FUEL, 'kind': 'importer', 'note': 'נספח 04.2025: מסנן הדלק כל 8 שנים או 100,000 ק"מ (במקום 4 שנים)'},
            {'url': U_BEV26, 'kind': 'importer', 'note': 'חוברת 7 שנים (עדכון 08.2026): טבלת היברידיים עמ\' 13-19 (PDF 15-21); מסנני יניקה ולחץ של התיבה כל 80,000 ק"מ ל-ZS HEV ול-MG3 HEV'},
            {'url': U_WARR_PAGE, 'kind': 'importer', 'note': 'עמוד האחריות של MG ישראל'},
        ],
        notes=('התוכנית הועתקה מחוברת השירות והאחריות העברית של קאר איסט ל-ZS Hybrid. טיפולי A ו-B מתחלפים כל 15,000 ק"מ או שנה; בטיפול B מוחלפים מסנן המזגן, מסנן האוויר של המנוע ומסנן האוויר של סוללת המתח הגבוה. '
               'שמן ומסנן בכל טיפול. נוזל תיבת ההנעה החשמלית כל 80,000 ק"מ (וחוברת 2026 מוסיפה את מסנני התיבה), נוזל בלמים כל שנתיים, נוזל קירור כל 4 שנים או 100,000 ק"מ, מצתים כל 40,000 ק"מ, '
               'מסנן דלק כל 8 שנים או 100,000 ק"מ לפי נספח התיקון. קוד המנוע 15FHC ברישוי שייך לגרסה ההיברידית. ' + SEVERE_HEV),
    )
    return write(d)

# ======================= HS Hybrid+ (new) =======================
def hs_hybrid():
    d = mg_base(
        id='mg-hs-hybrid-2025-2026-1.5-hybrid', model='HS Hybrid+', model_he='HS היברידי', generation='HS (2024+) Hybrid+',
        years=[2025, 2026], engines=['1.5 hybrid (15FKE)'], fuel='hybrid',
        interval={'km': 15000, 'months': 12, 'note': 'לפי חוברת קאר איסט לדגמים היברידיים (2026): טיפול A ב-15,000 ק"מ/12 חודשים, טיפול B ב-30,000 ק"מ/24 חודשים, וחוזר חלילה; המוקדם מביניהם'},
        cycle_km=120000,
        services=ab_services(15000, 8, HEV_ROWS),
        long_interval=hev_li('HS', False),
        specs={'warranty': '7 שנים לרכבים חשמליים והיברידיים שנרכשו מ-2025 (חוברת 08.2026)',
               '_note': 'נבדק מול חוברת השירות והאחריות העברית של קאר איסט לדגמים חשמליים/היברידיים/פלאג-אין'},
        sources=[
            {'url': U_BEV26, 'kind': 'importer', 'note': 'חוברת 7 שנים (עדכון 08.2026): תדירות טיפולים לדגמים היברידיים עמ\' 13, מפרט A/B עמ\' 14-17 (PDF 16-19), פעולות מיוחדות - עמודת "דגמי רכבים היברידיים" עמ\' 18 (PDF 20)'},
            {'url': U_BEV25, 'kind': 'importer', 'note': 'גרסת 11.2025 של אותה חוברת (עותק ב-web.archive.org) - אותם ערכים לדגמים היברידיים'},
        ],
        notes=('MG HS Hybrid+ אינה מופיעה בשמה בטבלה, והחוברת המשותפת של קאר איסט לדגמים חשמליים, היברידיים ופלאג-אין חלה עליה (ברישוי: HS HYBRID, דלק בנזין, מנוע 15FKE). '
               'טיפולי A ו-B מתחלפים כל 15,000 ק"מ או שנה; בטיפול B מוחלפים מסנן המזגן, מסנן האוויר של המנוע ומסנן האוויר של סוללת המתח הגבוה. '
               'נוזל תיבת ההנעה החשמלית כל 80,000 ק"מ, נוזל בלמים כל שנתיים, נוזל קירור כל 4 שנים או 100,000 ק"מ, מסנן דלק כל 8 שנים או 100,000 ק"מ, מצתים כל 40,000 ק"מ. '
               'מסנני היניקה והלחץ של התיבה מופיעים רק ל-ZS ול-MG3 ההיברידיות ולכן לא נכללו. ' + SEVERE_HEV),
    )
    return write(d)

# ======================= PHEV (EHS 2025+, S9) =======================
def phev(id_, model, model_he, gen, years, engines, extra_notes, s9=False):
    li = [
        {'item': 'transmission_oil', 'action': 'replace', 'every_km': 80000, 'note': 'נוזל תיבת ההנעה החשמלית'},
        BRAKE2Y,
        {'item': 'coolant', 'action': 'replace', 'every_km': 100000, 'every_months': 48, 'note': 'המוקדם מביניהם'},
        {'item': 'fuel_filter', 'action': 'replace', 'every_km': 100000, 'every_months': 96, 'note': 'משולב במשאבת הדלק'},
        {'item': 'spark_plugs', 'action': 'replace', 'every_km': 40000},
    ]
    if s9:
        li.append({'item': 'body_underside', 'action': 'clean', 'every_months': 12, 'note': 'צינור הניקוז של גג השמש הפנורמי (אם מותקן): בדיקה וניקוי סתימות פעם בשנה'})
    d = mg_base(
        id=id_, model=model, model_he=model_he, generation=gen, years=years, engines=engines, fuel='plug-in-hybrid',
        interval={'km': 24000, 'months': 12, 'note': 'לפי חוברת קאר איסט לדגמי פלאג-אין (2026): טיפול A ב-24,000 ק"מ/12 חודשים, טיפול B ב-48,000 ק"מ/24 חודשים, וחוזר חלילה; המוקדם מביניהם'},
        cycle_km=192000,
        services=ab_services(24000, 8, PHEV_ROWS),
        long_interval=li,
        specs={'warranty': '7 שנים לרכבים חשמליים, היברידיים ופלאג-אין שנרכשו מ-2025 (חוברת 08.2026)',
               '_note': 'נבדק מול חוברת השירות והאחריות העברית של קאר איסט לדגמים חשמליים/היברידיים/פלאג-אין'},
        sources=[
            {'url': U_BEV26, 'kind': 'importer', 'note': 'חוברת 7 שנים (עדכון 08.2026): "תדירות טיפולים לדגמי פלאג אין הייבריד" עמ\' 13 (PDF 15), מפרט A/B עמ\' 14-17 (PDF 16-19), פעולות מיוחדות - עמודת פלאג-אין עמ\' 18 (PDF 20)'},
            {'url': U_BEV25, 'kind': 'importer', 'note': 'גרסת 11.2025 (עותק ב-web.archive.org): ל-S9 הוחלף שם מסנן האוויר בכל טיפול, ומסנני התיבה סומנו גם לפלאג-אין; בעדכון 2026 שני אלה הוסרו'},
        ],
        notes=('התוכנית הועתקה מחוברת קאר איסט לדגמים חשמליים, היברידיים ופלאג-אין (עדכון 08.2026). טיפולי A ו-B מתחלפים כל 24,000 ק"מ או שנה. '
               'בטיפול B מוחלפים מסנן המזגן ומסנן האוויר של המנוע; החלפת מסנן האוויר של סוללת המתח הגבוה אינה חלה על פלאג-אין. שמן ומסנן בכל טיפול. '
               'נוזל תיבת ההנעה החשמלית כל 80,000 ק"מ, נוזל בלמים כל שנתיים, נוזל קירור כל 4 שנים או 100,000 ק"מ, מסנן דלק כל 8 שנים או 100,000 ק"מ, מצתים כל 40,000 ק"מ. ' + extra_notes + SEVERE_HEV),
    )
    return write(d)

# ======================= EVs =======================
EV_SRC_24 = [
    {'url': U_5Y24, 'kind': 'importer', 'note': 'חוברת 5 שנים (לחשמליים שנרכשו עד 2023 ול-EHS; עדכון 12.2025): מרווחים עמ\' 7 (PDF 9), מפרט לחשמליים עמ\' 12-14 (PDF 14-16), פעולות מיוחדות עמ\' 15 (PDF 17)'},
    {'url': U_7Y24, 'kind': 'importer', 'note': 'חוברת 7 שנים (לחשמליים שנרכשו מ-2023; 06.2024, עדכון 12.2025) - פרק התחזוקה זהה'},
]

def ev24(id_, model, model_he, gen, years, engines, trans_km, cool_km, cool_m, extra_li, extra_notes, extra_src=()):
    li = [
        {'item': 'transmission_oil', 'action': 'replace', 'every_km': trans_km, 'note': 'נוזל תיבת ההילוכים החשמלית'},
        BRAKE2Y,
        {'item': 'coolant', 'action': 'replace', 'every_km': cool_km, 'every_months': cool_m, 'note': 'המוקדם מביניהם'},
    ] + extra_li
    d = mg_base(
        id=id_, model=model, model_he=model_he, generation=gen, years=years, engines=engines, fuel='electric',
        interval={'km': 24000, 'months': 12, 'note': 'לפי חוברת השירות והאחריות של קאר איסט: טיפול A ב-24,000 ק"מ/12 חודשים, טיפול B ב-48,000 ק"מ/24 חודשים, וחוזר חלילה; המוקדם מביניהם'},
        cycle_km=192000,
        services=ab_services(24000, 8, EV24_ROWS),
        long_interval=li,
        specs={'_note': 'נבדק מול חוברות השירות והאחריות העבריות של קאר איסט (2024, עדכון 12.2025)'},
        sources=EV_SRC_24 + list(extra_src),
        notes=('התוכנית הועתקה מפרק התחזוקה לדגמים חשמליים בחוברות השירות והאחריות של קאר איסט. טיפולי A ו-B מתחלפים כל 24,000 ק"מ או שנה; בטיפול B מוחלף מסנן המזגן ונבדק מפלס נוזל הקירור, ושאר הבדיקות נעשות בכל טיפול. '
               'נוזל בלמים כל שנתיים. ' + extra_notes +
               ' יש לטעון ולאזן את תאי הסוללה לפחות פעם בחודש. בתנאים קשים: נוזל בלמים כל 40,000 ק"מ או שנה ובדיקת מסנן המזגן כל 5,000 ק"מ באבק.'),
    )
    return write(d)

def ev26(id_, model, model_he, gen, years, engines, trans_km, cool_km, cool_m, extra_notes, extra_src=()):
    li = [
        {'item': 'transmission_oil', 'action': 'replace', 'every_km': trans_km, 'note': 'נוזל תיבת ההנעה החשמלית'},
        BRAKE2Y,
        {'item': 'coolant', 'action': 'replace', 'every_km': cool_km, 'every_months': cool_m, 'note': 'המוקדם מביניהם'},
    ]
    d = mg_base(
        id=id_, model=model, model_he=model_he, generation=gen, years=years, engines=engines, fuel='electric',
        interval={'km': 24000, 'months': 12, 'note': 'לפי חוברת השירות והאחריות של קאר איסט: טיפול A ב-24,000 ק"מ/12 חודשים, טיפול B ב-48,000 ק"מ/24 חודשים, וחוזר חלילה; המוקדם מביניהם'},
        cycle_km=192000,
        services=ab_services(24000, 8, EV26_ROWS),
        long_interval=li,
        specs={'_note': 'נבדק מול חוברת השירות והאחריות העברית של קאר איסט (עדכון 08.2026) ומול חוברות 2024'},
        sources=[{'url': U_BEV26, 'kind': 'importer', 'note': 'חוברת 7 שנים (עדכון 08.2026): תדירות טיפולים לחשמליים עמ\' 7 (PDF 9), מפרט עמ\' 8-10 (PDF 10-12), פעולות מיוחדות עמ\' 11 (PDF 13)'}] + EV_SRC_24 + list(extra_src),
        notes=('התוכנית הועתקה מפרק התחזוקה לדגמים חשמליים בחוברת השירות והאחריות של קאר איסט. טיפולי A ו-B מתחלפים כל 24,000 ק"מ או שנה; בטיפול B מוחלף מסנן המזגן ונבדק מפלס נוזל הקירור, ושאר הבדיקות נעשות בכל טיפול. '
               'נוזל בלמים כל שנתיים. ' + extra_notes +
               ' יש לטעון ולאזן את תאי הסוללה לפחות פעם בחודש. בתנאים קשים: נוזל בלמים כל 40,000 ק"מ או שנה ובדיקת מסנן המזגן כל 5,000 ק"מ באבק.'),
    )
    return write(d)

# ======================= EHS PHEV 2021-2024 =======================
def ehs24():
    li = [
        {'item': 'drive_belt', 'action': 'replace', 'every_km': 100000, 'every_months': 36, 'note': 'רצועת האביזרים; המוקדם מביניהם'},
        {'item': 'transmission_oil', 'action': 'replace', 'every_km': 80000, 'note': 'נוזל תיבת ההילוכים החשמלית'},
        BRAKE2Y,
        {'item': 'coolant', 'action': 'replace', 'every_km': 90000, 'every_months': 36, 'note': 'המוקדם מביניהם'},
        {'item': 'fuel_filter', 'action': 'replace', 'every_km': 100000, 'every_months': 96, 'note': 'משולב במשאבת הדלק'},
        {'item': 'fuel_tank_air_filter', 'action': 'replace', 'every_km': 80000, 'every_months': 48, 'note': 'מסנן האוויר של יחידת אבחון הדליפות ממיכל הדלק'},
        {'item': 'spark_plugs', 'action': 'replace', 'every_km': 48000},
    ]
    d = mg_base(
        id='mg-ehs-2021-2024-1.5t-phev', model='EHS PHEV', model_he='EHS פלאג-אין', generation='EHS PHEV',
        years=[2021, 2024], engines=['1.5T PHEV (15E4E) + EDU'], fuel='plug-in-hybrid',
        interval={'km': 24000, 'months': 12, 'note': 'לפי חוברת השירות והאחריות של קאר איסט: טיפול A ב-24,000 ק"מ/12 חודשים, טיפול B ב-48,000 ק"מ/24 חודשים, וחוזר חלילה; המוקדם מביניהם'},
        cycle_km=192000,
        services=ab_services(24000, 8, EHS24_ROWS),
        long_interval=li,
        specs={'_note': 'נבדק מול חוברות השירות והאחריות העבריות של קאר איסט (2024, עדכון 12.2025)'},
        sources=[
            {'url': U_5Y24, 'kind': 'importer', 'note': 'חוברת 5 שנים (לחשמליים שנרכשו עד 2023 ולרכבי MG EHS; עדכון 12.2025): מרווחים עמ\' 7 (PDF 9), "תוכנית תחזוקה רגילה לדגמים היברידיים" עמ\' 8-11 (PDF 10-13), פעולות מיוחדות עמ\' 15 (PDF 17), תנאים קשים עמ\' 16 (PDF 18)'},
            {'url': U_7Y24, 'kind': 'importer', 'note': 'חוברת 7 שנים (06.2024, עדכון 12.2025) - פרק התחזוקה זהה'},
        ],
        notes=('התוכנית הועתקה מהפרק לדגמים היברידיים בחוברת השירות והאחריות של קאר איסט (שחלה על MG EHS). טיפולי A ו-B מתחלפים כל 24,000 ק"מ או שנה. '
               'בטיפול B מוחלפים מסנן המזגן ומסנן האוויר של המנוע ונבדקות סעפת היניקה, מערכת הפליטה, מערכת אדי הדלק ותושבות המנוע. שמן ומסנן בכל טיפול. '
               'פריטים מיוחדים: רצועת אביזרים כל 3 שנים או 100,000 ק"מ, נוזל תיבת ההילוכים החשמלית כל 80,000 ק"מ, נוזל בלמים כל שנתיים, נוזל קירור כל 3 שנים או 90,000 ק"מ, '
               'מסנן דלק כל 8 שנים או 100,000 ק"מ, מסנן אוויר של יחידת אבחון הדליפות במיכל הדלק כל 4 שנים או 80,000 ק"מ, ומצתים כל 48,000 ק"מ. '
               'בתנאים קשים (נסיעות קצרות מתחת ל-8 ק"מ, פקקים, חום מעל 30 מעלות, אבק, הרים): שמן ומסנן כל 5,000 ק"מ, בדיקת מסנני האוויר והמזגן כל 5,000 ק"מ באבק, ונוזל בלמים כל 40,000 ק"מ או שנה.'),
    )
    return write(d)

# ======================= petrol (MG3 1.5, HS 1.5T) =======================
def petrol(id_, model, model_he, gen, years, engines, li, extra_notes):
    d = mg_base(
        id=id_, model=model, model_he=model_he, generation=gen, years=years, engines=engines, fuel='petrol',
        interval={'km': 15000, 'months': 12, 'note': 'לפי חוברת השירות והאחריות של קאר איסט לדגמי בנזין: טיפול A ב-15,000 ק"מ/12 חודשים, טיפול B ב-30,000 ק"מ/24 חודשים, וחוזר חלילה; המוקדם מביניהם'},
        cycle_km=120000,
        services=ab_services(15000, 8, ICE_ROWS),
        long_interval=li,
        specs={'warranty': '5 שנים לרכבי MG בנזין שנרכשו מ-2025',
               '_note': 'נבדק מול חוברת השירות והאחריות העברית של קאר איסט לדגמי בנזין (עדכון 06.2026)'},
        sources=[
            {'url': U_BENZ26, 'kind': 'importer', 'note': 'חוברת 5 שנים לדגמי בנזין MG3/ZS/HS (עדכון 06.2026): תדירות טיפולים עמ\' 7 (PDF 9), מפרט A/B עמ\' 8-10 (PDF 10-12), פריטי תחזוקה מיוחדים לפי דגם עמ\' 11 (PDF 13), תנאים קשים עמ\' 12'},
            {'url': U_BENZ25, 'kind': 'importer', 'note': 'גרסת 08.2025 של אותה חוברת (עותק ב-web.archive.org) - אותם ערכים'},
        ],
        notes=('התוכנית הועתקה מחוברת השירות והאחריות העברית של קאר איסט לדגמי בנזין. טיפולי A ו-B מתחלפים כל 15,000 ק"מ או שנה. '
               'בטיפול B מוחלפים מסנן המזגן ומסנן האוויר של המנוע ונבדקות הסעפות, מערכת הפליטה ותושבות המנוע. שמן ומסנן בכל טיפול. ' + extra_notes +
               ' בתנאים קשים (נסיעות קצרות מתחת ל-8 ק"מ, פקקים, טמפרטורות מתחת ל-0 או מעל 30 מעלות, אבק, הרים, מונית): שמן ומסנן כל 5,000 ק"מ, בדיקת מסנן האוויר ומסנן המזגן כל 5,000 ק"מ באבק, ונוזל בלמים כל 40,000 ק"מ או שנה.'),
    )
    return write(d)

if __name__ == '__main__':
    out = []
    out.append(mg3_hybrid())
    out.append(zs_hybrid())
    out.append(hs_hybrid())
    out.append(phev('mg-ehs-2025-2026-1.5t-phev', 'EHS / HS PHEV', 'EHS פלאג-אין', 'HS PHEV (2024+)', [2025, 2026], ['1.5T PHEV (15FKE)'],
                    'רישוי: EHS עם מנוע 15FKE ודלק חשמל/בנזין. '))
    out.append(phev('mg-s9-2026-1.5t-phev', 'S9 PHEV', 'S9 פלאג-אין', 'S9 (RX9)', [2026, 2026], ['1.5T PHEV (15FKE)'],
                    'ל-S9 מומלץ לבדוק ולנקות את צינור הניקוז של גג השמש פעם בשנה. ', s9=True))
    # EVs, 2024 booklets (models bought until 2024)
    out.append(ev24('mg-zs-ev-2020-2024-ev', 'ZS EV', 'ZS חשמלי', 'ZS EV', [2020, 2024], ['EV (TZ204XS1152 / TZ204XS1481)'],
                    80000, 96000, 60, [],
                    'ל-ZS EV: נוזל תיבת ההילוכים החשמלית כל 80,000 ק"מ ונוזל קירור כל 5 שנים או 96,000 ק"מ (בשאר החשמליים 4 שנים). במסמך עלויות הטיפול של היבואן ל-ZS EV 2020-2021 (02.2022) נוזל הקירור מופיע בטיפול 48 חודשים/96,000 ק"מ.',
                    extra_src=[{'url': U_ZSEV_COST, 'kind': 'importer', 'note': 'מפרט ועלויות טיפולים ל-MG ZS EV 2020-2021 (20.2.2022), עותק ב-web.archive.org (2022-06-22): טיפול כל 24,000 ק"מ/12 חודשים; נוזל בלמים ומסנן מזגן בטיפולי 24 ו-48 חודשים, שמן תיבה ב-80,000 ק"מ, נוזל קירור בטיפול 48 חודשים'}]))
    out.append(ev24('mg-marvel-r-2023-2024-ev', 'Marvel R', 'מרוול R', 'Marvel R Electric', [2022, 2024], ['EV (TZ204XS1155 / TZ204XS1154)'],
                    80000, 96000, 48,
                    [{'item': 'electrical_system', 'action': 'adjust', 'every_km': 20000, 'note': 'כיול מסנכרן המיקום (חוברות 2024 וגרסת 11.2025; הוסר בעדכון 08.2026)'}],
                    'ל-Marvel R: נוזל תיבת ההילוכים החשמלית כל 80,000 ק"מ, נוזל קירור כל 4 שנים או 96,000 ק"מ, וכיול מסנכרן המיקום כל 20,000 ק"מ.',
                    extra_src=[{'url': U_BEV26, 'kind': 'importer', 'note': 'חוברת 08.2026, פעולות מיוחדות עמ\' 11: עמודת MARVEL R - אותם ערכים לנוזלים'}]))
    out.append(ev26('mg-4-2023-2026-ev', 'MG4', 'MG4', 'MG4 Electric', [2023, 2026], ['EV (TZ180XS0951 / TZ204XS1351)'],
                    96000, 96000, 48,
                    'נוזל תיבת ההנעה החשמלית כל 96,000 ק"מ ונוזל קירור כל 4 שנים או 96,000 ק"מ (עמודת MG5/MG4/S5/S6/Cyberster; כך גם בחוברות 2024). בעדכון 08.2026 מופיעה עמודה נפרדת "MG4 MCE (EH32)" עם 80,000 ק"מ לנוזל התיבה ו-3 שנים או 90,000 ק"מ לנוזל הקירור; ייתכן שהיא חלה על גרסת הפייסליפט.'))
    out.append(ev26('mg-5-2023-2024-ev', 'MG5', 'MG5', 'MG5 Electric', [2023, 2024], ['EV (TZ204XS1152)'],
                    96000, 96000, 48,
                    'ל-MG5: נוזל תיבת ההנעה החשמלית כל 96,000 ק"מ ונוזל קירור כל 4 שנים או 96,000 ק"מ (כך בחוברות 2024 ובעדכון 08.2026).'))
    # petrol
    out.append(petrol('mg-3-2025-2026-1.5', 'MG3', 'MG3', 'MG3 (2024+)', [2025, 2026], ['1.5 (15FCD)'],
                      [{'item': 'drive_belt', 'action': 'replace', 'every_km': 100000, 'every_months': 36, 'note': 'רצועת הינע עזר; המוקדם מביניהם'},
                       {'item': 'manual_gearbox_oil', 'action': 'replace', 'every_km': 80000, 'note': 'ברכב עם תיבה ידנית'},
                       {'item': 'transmission_oil', 'action': 'replace', 'every_km': 80000, 'note': 'ברכב עם תיבה אוטומטית'},
                       {'item': 'cvt_oil', 'action': 'replace', 'every_km': 80000, 'note': 'ברכב עם תיבה רציפה'},
                       BRAKE2Y,
                       {'item': 'coolant', 'action': 'replace', 'every_km': 100000, 'every_months': 48, 'note': 'המוקדם מביניהם'},
                       {'item': 'fuel_filter', 'action': 'replace', 'every_km': 100000, 'every_months': 96, 'note': 'משולב במשאבת הדלק'},
                       {'item': 'spark_plugs', 'action': 'replace', 'every_km': 40000}],
                      'פריטים מיוחדים בעמודת MG3: רצועת הינע עזר כל 3 שנים או 100,000 ק"מ, נוזל תיבת הילוכים (ידנית, אוטומטית או רציפה - לפי התיבה המותקנת) כל 80,000 ק"מ, נוזל בלמים כל שנתיים, נוזל קירור כל 4 שנים או 100,000 ק"מ, מסנן דלק כל 8 שנים או 100,000 ק"מ ומצתים כל 40,000 ק"מ. מסנני התיבה אינם חלים על MG3.'))
    out.append(petrol('mg-hs-2025-2026-1.5t', 'HS', 'HS', 'HS (2024+)', [2025, 2026], ['1.5T (15FDE)'],
                      [{'item': 'drive_belt', 'action': 'replace', 'every_km': 100000, 'every_months': 36, 'note': 'רצועת הינע עזר; המוקדם מביניהם'},
                       {'item': 'manual_gearbox_oil', 'action': 'replace', 'every_km': 80000, 'note': 'ברכב עם תיבה ידנית'},
                       {'item': 'transmission_oil', 'action': 'replace', 'every_km': 80000, 'note': 'תיבה אוטומטית בעלת 7 הילוכים; מסנן היניקה של התיבה מוחלף באותו מועד'},
                       BRAKE2Y,
                       {'item': 'coolant', 'action': 'replace', 'every_km': 100000, 'every_months': 48, 'note': 'המוקדם מביניהם'},
                       {'item': 'fuel_filter', 'action': 'replace', 'every_km': 100000, 'every_months': 96, 'note': 'משולב במשאבת הדלק'},
                       {'item': 'spark_plugs', 'action': 'replace', 'every_km': 40000, 'note': 'בגרסאות מנוע 1.5T ו-1.5L'}],
                      'פריטים מיוחדים בעמודת MG HS: רצועת הינע עזר כל 3 שנים או 100,000 ק"מ, נוזל תיבה ידנית כל 80,000 ק"מ, נוזל התיבה האוטומטית בת 7 ההילוכים ומסנן היניקה שלה כל 80,000 ק"מ, נוזל בלמים כל שנתיים, נוזל קירור כל 4 שנים או 100,000 ק"מ, מסנן דלק כל 8 שנים או 100,000 ק"מ ומצתים כל 40,000 ק"מ. ברישוי: HS, בנזין, מנוע 15FDE.'))
    out.append(ehs24())
    for p in out: print(p)
