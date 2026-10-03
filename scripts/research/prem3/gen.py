# Generator for prem3 schedules (Mercedes-Benz, BMW/MINI, Volvo, Audi, Lexus).
import json, os, re, collections

OUT = '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/prem3'
os.makedirs(OUT + '/registry', exist_ok=True)
REG = json.load(open('/home/user/cv/data/sources/registry-counts.json'))
MAK = [("ב.מ.וו", "BMW"), ("ב מ וו", "BMW"), ("מרצדס", "Mercedes-Benz"), ("דיימלר", "Mercedes-Benz"),
       ("אאודי", "Audi"), ("אודי", "Audi"), ("וולוו", "Volvo"), ("וולבו", "Volvo"), ("לקסוס", "Lexus"),
       ("רובר", "Land Rover"), ("לנדרובר", "Land Rover")]


def norm(m):
    for he, en in MAK:
        if m.startswith(he):
            return en
    return None


ROWS = [dict(r, mk=norm(r['make']), y=int(r['year'])) for r in REG['model_year_fuel_engine'] if norm(r['make'])]

schedules, rules, stats = [], [], []


def I(item, action, note=None):
    d = {"item": item, "action": action}
    if note:
        d["note"] = note
    return d


def rule(make, sched, years, pred, use_fuel=True):
    rows = [r for r in ROWS if r['mk'] == make and years[0] <= r['y'] <= years[1] and pred(r)]
    names = sorted({r['model'] for r in rows})
    codes = sorted({r['engine'] for r in rows})
    fuels = sorted({r['fuel'] for r in rows})
    r = {"make": make, "names": names, "years": list(years), "engine_codes": codes}
    if use_fuel:
        r["fuel"] = fuels
    r["schedule"] = sched
    rules.append(r)
    stats.append((sched, sum(x['n'] for x in rows), len(names)))
    return r


def save(s):
    s.setdefault("time_based", [])
    path = f"{OUT}/{s['id']}.json"
    json.dump(s, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    schedules.append(s['id'])

# ---------------------------------------------------------------- Mercedes-Benz
MB_CA = {"url": "https://www.mercedes-benz.ca/en/owners/service-maintenance", "kind": "manufacturer",
         "note": "מרצדס-בנץ קנדה (רשמי, ק\"מ), פרק Maintenance Schedule: טיפול A ראשון בכ-20,000 ק\"מ או שנה, טיפול B שנה/20,000 ק\"מ אחריו, לסירוגין; רשימת העבודות בכל טיפול. נקרא בדפדפן (Playwright) ב-3.10.2026"}
MB_US = {"url": "https://www.mbusa.com/en/owners/service-maintenance", "kind": "manufacturer",
         "note": "מרצדס-בנץ ארה\"ב (רשמי), Service Intervals: טיפול B כולל החלפת מסנן אבק/מסנן משולב והחלפת נוזל בלמים; מרווחים במיילים (10,000/20,000)"}
MB_CA_SB = {"url": "https://www.mercedes-benz.ca/content/dam/mb-nafta/ca/owners/operators-manual/2023/SB_MY21-23_PC%20except%20463_ENG_2135842421_ALL.pdf", "kind": "manufacturer",
            "note": "חוברת שירות קנדית 2021-2023: מפרטת סוגי עבודות אך מפנה לתצוגת ASSYST PLUS ולספר השירות הדיגיטלי לגבי המרווחים (אין בה מספרים)"}
MB_IL = {"url": "https://www.mercedes-benz.co.il/site/car-books/", "kind": "importer",
         "note": "דף ספרי הרכב של כלמוביל/מרצדס ישראל: הספרים נשלחים רק בטופס עם קפצ'ה ודוא\"ל, לא הושגו"}


def mb_services(diesel=False, phev=False):
    def A():
        it = [I("engine_oil", "replace"), I("oil_filter", "replace")]
        if diesel:
            it.append(I("adblue", "inspect", "השלמת AdBlue (דיזל בלבד)"))
        it += [I("cabin_filter", "replace", "מסנן אבק לתא הנוסעים, בדגמים שבהם קיים"),
               I("lights", "inspect", "כולל צופר"), I("door_hinges", "inspect"),
               I("coolant", "inspect", "בדיקת מפלסי נוזלים והשלמה"), I("brake_fluid", "inspect", "מפלס"),
               I("wipers", "inspect", "מגבים ומערכת שטיפה"), I("brake_pads", "inspect"), I("brake_discs", "inspect"),
               I("tires", "inspect", "כולל גלגל חלופי"), I("battery_12v", "replace", "סוללת השלט (מפתח)")]
        if phev:
            it.append(I("hybrid_system", "inspect", "לפי מחוון השירות; המקור הקנדי לא מפרט בדיקות נפרדות למערכת הנטענת"))
        return it

    def B():
        it = [I("engine_oil", "replace"), I("oil_filter", "replace")]
        if diesel:
            it.append(I("adblue", "inspect", "השלמת AdBlue (דיזל בלבד)"))
        it += [I("cabin_filter", "replace", "מסנן משולב (פחם פעיל)"), I("brake_fluid", "replace", "לפי דף השירות האמריקאי של מרצדס (טיפול B)"),
               I("tire_rotation", "rotate", "כשמתאים לרכב"), I("suspension", "inspect"), I("steering", "inspect"),
               I("propshaft", "inspect", "מערכת ההינע - בלאי ונזק"), I("body_underside", "inspect", "דליפות במכלולים העיקריים"),
               I("seat_belts", "inspect"), I("drive_belt", "inspect", "רצועת Poly-V"), I("lights", "adjust", "כיוון פנסים ראשיים"),
               I("coolant", "inspect", "בדיקת מפלסי נוזלים והשלמה"), I("brake_pads", "inspect"), I("brake_discs", "inspect"),
               I("tires", "inspect")]
        if phev:
            it.append(I("hybrid_system", "inspect", "לפי מחוון השירות"))
        return it
    return [{"km": 20000, "items": A()}, {"km": 40000, "items": B()}, {"km": 60000, "items": A()}, {"km": 80000, "items": B()}]


MB_INTERVAL = {"km": 20000, "months": 12, "note": "לפי מרצדס קנדה: טיפול A ראשון בכ-20,000 ק\"מ או שנה, ואחריו טיפול B ושוב A לסירוגין, כל 20,000 ק\"מ או שנה (המוקדם). מחוון ASSYST PLUS ברכב קובע בפועל"}
MB_NOTE_COMMON = ("טיוטה. ספרי הרכב והשירות של כלמוביל לא נמצאו ברשת (נשלחים רק בטופס), ואתרי מרצדס באירופה חסומים מכאן. "
                  "המרווחים כאן מתוך דף השירות הרשמי של מרצדס-בנץ קנדה (שוק בק\"מ): טיפולי A ו-B לסירוגין, כל 20,000 ק\"מ או שנה. "
                  "ברכבי מרצדס מחוון השירות (ASSYST PLUS) מחשב את מועד הטיפול לפי נסועה, זמן ואופן נהיגה, והוא שקובע; בשווקים אחרים המרווח המרבי עשוי להיות שונה. "
                  "החלפת נוזל בלמים בטיפול B לקוחה מדף השירות האמריקאי של מרצדס. מצתים, מסנן אוויר, נוזל קירור ושמן גיר לא מפורטים במקורות שנפתחו ולכן לא נכללו - יש לבצע לפי מחוון השירות והמוסך המורשה.")

mb_common = dict(make="Mercedes-Benz", make_he="מרצדס-בנץ", importer="כלמוביל", interval=MB_INTERVAL, cycle_km=80000,
                 long_interval=[], sources=[MB_CA, MB_US, MB_CA_SB, MB_IL], status="draft",
                 specs={"_note": "לא נמצאו נתוני שמנים ונוזלים במקורות שנפתחו; יש לבדוק בספר הרכב"})

s = dict(mb_common, id="mercedes-benz-a-b-cla-gla-2013-2026-petrol", model="A-Class / B-Class / CLA / GLA / GLB", model_he="A / B / CLA / GLA / GLB",
         generation="W176/W246/C117/X156, W177/W247/C118/H247/X247", years=[2013, 2026],
         engines=["1.33 טורבו (M282)", "1.6/2.0 טורבו (M270)", "2.0 טורבו (M260)", "1.5 (M252)"], fuel="petrol",
         services=mb_services(), notes=MB_NOTE_COMMON)
save(s)
rule("Mercedes-Benz", s['id'], (2013, 2026), lambda r: r['engine'] in {"M270", "M282", "M260", "M252"} and r['fuel'] == "בנזין")

s = dict(mb_common, id="mercedes-benz-c-e-glc-gle-2011-2026-petrol", model="C-Class / E-Class / GLC / GLE / S-Class / CLE", model_he="C / E / GLC / GLE / S / CLE",
         generation="W204/W205/W206, W212/W213/W214, X253/X254, W166/V167, W222/W223", years=[2011, 2026],
         engines=["1.6/2.0 טורבו (M274)", "1.5/2.0 טורבו מיילד-היברידי (M264, M254)", "1.8 (M271)", "3.0/3.5 V6 (M276)", "3.0 שישה בטור (M256)"], fuel="petrol",
         services=mb_services(), notes=MB_NOTE_COMMON + " בדגמי AMG המרווח עשוי להיות קצר יותר.")
save(s)
rule("Mercedes-Benz", s['id'], (2011, 2026), lambda r: r['engine'] in {"M274", "M264", "M254", "M271", "M276", "M256", "254920", "264920", "256830", "256930"} and r['fuel'] == "בנזין")

VANS = re.compile(r'VITO|VIANO|SPRINTER|CITAN|^V CLASS|^V2[25]0|^[13]\d\d ?(CDI|BLUETEC)')
s = dict(mb_common, id="mercedes-benz-c-e-glc-gle-2010-2026-diesel", model="C / E / GLC / GLE / ML / GLS / B / S (דיזל)", model_he="C / E / GLC / GLE / ML / GLS / B / S דיזל",
         generation="W204/W205/W206, W212/W213, X253, W166/V167, X167, W246/W247", years=[2010, 2026],
         engines=["2.1/2.2 טורבו דיזל (OM651)", "2.0 טורבו דיזל (OM654)", "3.0 V6 טורבו דיזל (OM642)", "2.9 שישה בטור טורבו דיזל (OM656)"], fuel="diesel",
         services=mb_services(diesel=True), notes=MB_NOTE_COMMON + " מסנן דלק אינו מפורט במקור הקנדי לרכבים פרטיים; יש לבדוק במוסך.")
save(s)
rule("Mercedes-Benz", s['id'], (2010, 2026), lambda r: r['engine'] in {"OM651", "OM 651", "OM-651", "OM654", "654920", "OM656", "656830", "OM642"} and r['fuel'] == "דיזל" and not VANS.search(r['model']))

s = dict(mb_common, id="mercedes-benz-plug-in-hybrid-2016-2026", model="C / E / GLC / GLE / A / CLA / GLA / S (פלאג-אין)", model_he="C350e / C300e / E300e / E350e / GLC300e / GLC350e / A250e / CLA250e / GLA250e / GLE350de / S560e / S580e",
         generation="W205/W206, W213/W214, X253/X254, W177/C118/H247, V167, W222/W223", years=[2016, 2026],
         engines=["2.0 טורבו + מנוע חשמלי (M274, M254)", "1.33 טורבו + מנוע חשמלי (M282)", "2.0 טורבו דיזל + מנוע חשמלי (OM654)", "V6 / שישה בטור + מנוע חשמלי (M276, M256)"], fuel="plug-in-hybrid",
         services=mb_services(phev=True),
         notes=MB_NOTE_COMMON + " בפלאג-אין דיזל (GLE 350 de, E 300 de) יש להוסיף השלמת AdBlue כמו בדיזל. דף קנדה אינו מפריד בין רכב רגיל לפלאג-אין.")
save(s)
rule("Mercedes-Benz", s['id'], (2016, 2026), lambda r: r['fuel'] in {"חשמל/בנזין", "חשמל/דיזל"} and r['engine'] in {"M274", "274920", "274.920", "M282", "282914", "282814", "282.914", "M254", "254920", "M276", "276824", "M256", "256930", "OM654", "654920", "M264"})

# Sprinter (US fleet brochure, miles)
SPR = {"url": "https://www.mbvans.com/content/dam/mb-vans/us/brochures/2025%20MB%20Vans%20Fleet%20and%20RV%20Brochure.pdf", "kind": "manufacturer",
       "note": "מרצדס-בנץ ואנס ארה\"ב, חוברת צי ו-RV 2025, עמ' 3-4 'Detailed Maintenance Sheets' (ספרינטר דיזל): טיפולי A/B כל 20,000 מייל או שנתיים, עד 160,000 מייל; פריטים לפי זמן/נסועה. המיילים הומרו לק\"מ (1 מייל = 1.609 ק\"מ, מעוגל)"}
SPR_CA = {"url": "https://www.mercedes-benz-vans.ca/content/dam/mb-vans/ca/brochures/en/Sprinter%20Warranty%20Book_MY2024_Ed%20A_EN.pdf", "kind": "manufacturer",
          "note": "ספר אחריות ספרינטר קנדה 2024: מפנה לחוברת השירות לגבי המרווחים (אין בו טבלה)"}


def spr_svc(n):
    b = n % 2 == 0
    it = [I("engine_oil", "replace"), I("oil_filter", "replace"), I("fuel_filter", "replace"), I("brake_fluid", "inspect", "מפלס"),
          I("washer_fluid", "inspect", "השלמה"), I("adblue", "inspect", "מילוי מיכל AdBlue"), I("parking_brake", "inspect", "בדיקת תפקוד בלם שירות ובלם חניה"),
          I("tires", "inspect", "כולל גלגל חלופי"), I("brake_fluid", "replace", "כל שנתיים לפי החוברת (כל טיפול כזה הוא בערך שנתיים)")]
    if n <= 6:
        it.append(I("seat_belts", "inspect"))
    if b:
        it += [I("power_steering_fluid", "inspect", "בגרסת 4x4 בלבד"), I("drive_belt", "inspect", "כל רצועות Poly-V"),
               I("fuel_lines", "inspect", "כל הרכיבים הגלויים בתא המנוע - נזק ודליפות"), I("lights", "inspect", "תאורה חיצונית"),
               I("lights", "adjust", "כיוון גובה פנסים"), I("door_hinges", "inspect", "גירוז צירי דלתות אחוריות (בקוד W54)")]
        if n <= 6:
            it += [I("wipers", "inspect", "מגבים קדמיים ואחוריים ומערכות שטיפה"), I("cabin_filter", "replace", "מסנן אבק/פחם למיזוג; גם מסנן מזגן הגג האחורי אם קיים"),
                   I("body_underside", "inspect", "פתחי ניקוז ברצפה באזור הדלת ההזזה")]
    if n >= 4:
        it.append(I("diagnostics", "inspect", "בדיקת יעילות מסנן חלקיקים (DPF) במחשב, בכל טיפול אחרי 100,000 מייל"))
    return {"km": 32000 * n, "items": it}


s = dict(make="Mercedes-Benz", make_he="מרצדס-בנץ", importer="כלמוביל", id="mercedes-benz-sprinter-2018-2026-diesel", model="Sprinter", model_he="ספרינטר",
         generation="VS30 (907/910)", years=[2018, 2026], engines=["2.0 טורבו דיזל (OM654)", "2.1 טורבו דיזל (OM651)", "3.0 V6 טורבו דיזל (OM642)"], fuel="diesel",
         interval={"km": 32000, "months": 24, "note": "לפי החוברת האמריקאית: טיפולי A ו-B לסירוגין כל 20,000 מייל (כ-32,000 ק\"מ) או שנתיים, המוקדם. מחוון השירות ברכב קובע"},
         cycle_km=256000, services=[spr_svc(n) for n in range(1, 9)],
         long_interval=[I("air_filter", "replace") | {"every_km": 96000, "every_months": 48, "note": "60,000 מייל או 4 שנים"},
                        I("drive_belt", "replace") | {"every_km": 128000, "every_months": 48, "note": "רצועת Poly-V: 80,000 מייל או 4 שנים"},
                        I("coolant", "replace") | {"first_km": 354000, "first_months": 180, "then_every_months": 36, "note": "220,000 מייל או 15 שנים, ואחר כך כל 3 שנים"},
                        I("parking_brake", "inspect") | {"every_km": 257000, "every_months": 60, "note": "קריאת מונה הפעלות בלם חניה חשמלי (קוד B25): 160,000 מייל או 5 שנים"}],
         time_based=[I("brake_fluid", "replace") | {"months": 24}],
         sources=[SPR, SPR_CA, MB_IL], status="draft",
         specs={"_note": "לא נמצאו נתוני שמנים ונוזלים במקורות שנפתחו"},
         notes=("טיוטה. ספר השירות הישראלי של ספרינטר לא נמצא. הלוח מתוך גיליונות התחזוקה המפורטים של מרצדס-בנץ ואנס בארה\"ב (ספרינטר דיזל, חוברת 2025), "
                "שבהם טיפולי A ו-B לסירוגין כל 20,000 מייל או שנתיים; המיילים הומרו לק\"מ ועוגלו. בשוק האירופי או הישראלי המרווח עשוי להיות שונה, ומחוון השירות ברכב קובע. "
                "מסנן דלק מוחלף בכל טיפול לפי הגיליון. במסלולי עבודה קשים (סרק ממושך, ביודיזל) המרווחים קצרים יותר."))
save(s)
rule("Mercedes-Benz", s['id'], (2018, 2026), lambda r: r['model'] == 'SPRINTER' and r['fuel'] == 'דיזל')

# ---------------------------------------------------------------- BMW / MINI
BMW25 = {"url": "https://www.bmwusa.com/content/dam/bmw/marketUS/common/warranty-books/2025/BMW_MY25_Maintenance_with_BEVs.pdf", "kind": "manufacturer",
         "note": "חוברת אחזקה של ב.מ.וו ארה\"ב 2025, עמ' 10-16 (Maintenance Service Summary): מסנן מיזוג בכל טיפול שמן שני (כ-20,000 מייל), מסנן אוויר ברביעי (כ-40,000 מייל), מצתים בשישי (כ-60,000 מייל), שמן גיר X1/X2 כ-60,000-72,000 מייל; עמ' 7 דוגמת תצוגה: שמן בעוד 10,000 מייל ושנה, נוזל בלמים 3 שנים"}
BMW21 = {"url": "https://di-uploads-pod15.s3.us-east-1.amazonaws.com/bmwofescondido/uploads/2021/05/5A1BC92_21MY_BMW_Maintenance_FINAL_Print_withCover_111220.pdf", "kind": "manufacturer",
         "note": "עותק של חוברת האחזקה של ב.מ.וו ארה\"ב לשנת 2021 (מאתר סוכנות), עמ' 9-14: אותו סדר פעולות, כולל דגמי 330e/530e/X3 30e/X5 45e; נוזלי קירור ותיבות הילוכים מוגדרים 'לטווח ארוך'"}
MINI21 = {"url": "https://minipub-prod.bmwgroup.com/content/dam/mini/PDF/warranties/2021_MINI_Maintenance.pdf", "kind": "manufacturer",
          "note": "חוברת אחזקה של מיני ארה\"ב 2021, עמ' 9-12: מסנן מיזוג בכל טיפול שמן שני, מסנן אוויר ברביעי (כ-40,000 מייל), מצתים בשישי (כ-60,000 מייל); כולל קאנטרימן פלאג-אין"}
MINI25 = {"url": "https://minipub-prod.bmwgroup.com/content/dam/mini/PDF/warranties/MINI_MY2025_All_Models_Maintenance_2025-03-07_1K.pdf", "kind": "manufacturer",
          "note": "חוברת אחזקה של מיני 2025, עמ' 12 ו-14: אותו סדר פעולות (גם בחוברות 2018, 2019, 2024)"}
KAMOR = {"url": "https://www.bmw.co.il/", "kind": "importer", "note": "אתרי כמור (bmw.co.il, kamor.co.il, mini.co.il) חסומים מכאן (502 בפרוקסי); לא נמצא מסמך של היבואן"}

BMW_INT = {"km": 16000, "months": 12, "note": "ב.מ.וו עובדת לפי מחוון CBS שמחשב את מועד החלפת השמן. בחוברת האמריקאית כל טיפול שמן הוא בערך 10,000 מייל (כ-16,000 ק\"מ), ובדוגמת התצוגה שבה הטיפול הבא מופיע שנה אחרי המסירה. המחוון ברכב קובע"}


def bmw_services(phev=False, mini=False):
    out = []
    for n in range(1, 13):
        it = [I("engine_oil", "replace"), I("oil_filter", "replace"), I("tires", "inspect", "לחץ ניפוח ואיפוס חיישני לחץ"),
              I("diagnostics", "inspect", "הודעות Check Control ונורות אזהרה; איפוס CBS"), I("parking_brake", "inspect")]
        if n % 2 == 0:
            it += [I("cabin_filter", "replace", "מסנן מיקרו לתא הנוסעים, בכל טיפול שמן שני"), I("battery_12v", "replace", "סוללות השלט")]
        if n % 4 == 0:
            it += [I("air_filter", "replace", "בכל טיפול שמן רביעי; לעתים קרובות יותר בתנאי אבק"),
                   I("lights", "inspect"), I("wipers", "inspect"), I("seat_belts", "inspect"), I("battery_12v", "inspect", "מצב טעינה"),
                   I("coolant", "inspect", "מפלס וריכוז" + ("; בפלאג-אין בשני המכלים (מנוע ואלקטרוניקת ההנעה)" if phev else "")),
                   I("washer_fluid", "inspect"), I("brake_lines", "inspect"), I("body_underside", "inspect", "תיבת הילוכים, סרן, צנרת דלק ופליטה"),
                   I("steering", "inspect"), I("suspension", "inspect", "בולמים (ויזואלי) ונסיעת מבחן")]
            if phev:
                it.append(I("hybrid_system", "inspect", "כבל הטעינה ושקע הטעינה: נזק, קורוזיה ובלאי"))
        if n % 6 == 0:
            it.append(I("spark_plugs", "replace", "בכל טיפול שמן שישי (כ-60,000 מייל)"))
        out.append({"km": 16000 * n, "items": it})
    return out


BMW_LONG = []
BMW_TIME = [I("brake_fluid", "replace", "לפי מחוון CBS (מבוסס זמן); בדוגמת התצוגה בחוברת ההחלפה הראשונה כשלוש שנים מהמסירה") | {"months": 36}]
BMW_NOTE = ("טיוטה. אתרי כמור חסומים מכאן ולא נמצא ספר שירות ישראלי. הלוח בנוי מחוברות האחזקה הרשמיות של ב.מ.וו בארה\"ב (2021, 2025): "
            "השמן מוחלף לפי מחוון CBS, ופריטים נלווים מוחלפים בטיפול שמן מסוים - מסנן מיזוג בכל שני, מסנן אוויר בכל רביעי, מצתים בכל שישי. "
            "הק\"מ כאן הם המרת ה'בערך 10,000 מייל' של החוברת; ברכב ישראלי/אירופי מחוון CBS עשוי לתת מרווח ארוך או קצר יותר, והוא שקובע. "
            "נוזל קירור ושמן תיבת הילוכים מוגדרים בחוברת כ'לטווח ארוך' (מוחלפים רק בתיקון), למעט האמור בהערות. נוזל בלמים לפי המחוון.")

s = dict(make="BMW", make_he="ב.מ.וו", importer="כמור", id="bmw-b38-b48-b58-2015-2026-petrol",
         model="סדרות 1/2/3/4/5/7, X1/X2/X3/X4/X5/X6, Z4", model_he="118i / 318i / 320i / 330i / 520i / 530i / X1 / X2 / X3 / X4 / X5 / X6 / Z4",
         generation="F/G/U (2015 ואילך)", years=[2015, 2026],
         engines=["1.5 טורבו 3 צילינדרים (B38)", "2.0 טורבו (B48)", "3.0 טורבו שישה בטור (B58)"], fuel="petrol",
         interval=BMW_INT, cycle_km=192000, services=bmw_services(),
         long_interval=BMW_LONG + [I("transmission_oil", "replace") | {"every_km": 96000, "note": "בחוברת 2025: X1/X2 בלבד, בערך 60,000-72,000 מייל (כ-96,000-115,000 ק\"מ). בשאר הדגמים שמן לטווח ארוך"}],
         time_based=BMW_TIME, sources=[BMW25, BMW21, KAMOR], status="draft",
         specs={"_note": "שמן לפי ספר הרכב (שמן סינתטי מאושר ב.מ.וו); נוזל קירור ושמן גיר לטווח ארוך לפי החוברת"},
         notes=BMW_NOTE)
save(s)
MINI_RE = re.compile(r'COOPER|^ONE$|MINI|COUNTRYMAN|CLUBMAN|ACEMAN|PACEMAN|JOHN COOPER')
rule("BMW", s['id'], (2015, 2026), lambda r: re.match(r'B(38|48|58)', r['engine']) and r['fuel'] == 'בנזין' and not MINI_RE.search(r['model']))

s = dict(make="BMW", make_he="ב.מ.וו", importer="כמור", id="bmw-plug-in-hybrid-2016-2026",
         model="330e / 530e / X1 25e / X2 25e / X3 30e / X5 45e / X5 50e / 745e / 750e / 320e", model_he="330e / 530e / X1 xDrive25e / X3 xDrive30e / X5 xDrive45e / X5 xDrive50e / 745Le",
         generation="F/G/U (2016 ואילך)", years=[2016, 2026],
         engines=["1.5 טורבו + מנוע חשמלי (B38)", "2.0 טורבו + מנוע חשמלי (B48)", "3.0 טורבו + מנוע חשמלי (B58)"], fuel="plug-in-hybrid",
         interval=BMW_INT, cycle_km=192000, services=bmw_services(phev=True), long_interval=BMW_LONG, time_based=BMW_TIME,
         sources=[BMW21, BMW25, KAMOR], status="draft",
         specs={"_note": "שמן לפי ספר הרכב; נוזל קירור ושמן גיר לטווח ארוך לפי החוברת"},
         notes=BMW_NOTE + " בפלאג-אין החוברת מוסיפה בבדיקת הרכב את מכל נוזל הקירור של אלקטרוניקת ההנעה ואת כבל ושקע הטעינה.")
save(s)
rule("BMW", s['id'], (2016, 2026), lambda r: re.match(r'B(38|48|58)', r['engine']) and r['fuel'] == 'חשמל/בנזין' and not MINI_RE.search(r['model']))

s = dict(make="BMW", make_he="מיני (ב.מ.וו)", importer="כמור", id="mini-cooper-countryman-2014-2026-1.2-1.5-2.0",
         model="MINI One / Cooper / Cooper S / JCW / Countryman / Clubman", model_he="מיני וואן / קופר / קופר S / קאנטרימן / קלאבמן",
         generation="F54/F55/F56/F57/F60, J01/U25 (2014 ואילך)", years=[2014, 2026],
         engines=["1.2/1.5 טורבו 3 צילינדרים (B38)", "2.0 טורבו (B48)"], fuel="petrol",
         interval=BMW_INT | {"note": "מיני עובדת לפי מחוון CBS. בחוברות מיני ארה\"ב מסנן אוויר בטיפול הרביעי (כ-40,000 מייל) ומצתים בשישי (כ-60,000 מייל), כלומר כ-10,000 מייל (16,000 ק\"מ) לטיפול; זמן שנה לפי דוגמת התצוגה בחוברת ב.מ.וו. המחוון ברכב קובע"},
         cycle_km=192000, services=bmw_services(), long_interval=BMW_LONG, time_based=BMW_TIME,
         sources=[MINI21, MINI25, BMW25, KAMOR], status="draft",
         specs={"_note": "שמן לפי ספר הרכב; נוזל קירור לטווח ארוך לפי החוברת"},
         notes=BMW_NOTE.replace("ב.מ.וו בארה\"ב (2021, 2025)", "מיני בארה\"ב (2018-2025)") + " גם קאנטרימן פלאג-אין (Cooper SE ALL4) משויך לכאן; לפי החוברת יש בו בנוסף בדיקת שני מכלי נוזל הקירור ובדיקת כבל ושקע הטעינה.")
save(s)
rule("BMW", s['id'], (2014, 2026), lambda r: re.match(r'B(38|48)', r['engine']) and r['fuel'] in ('בנזין', 'חשמל/בנזין') and MINI_RE.search(r['model']))

# ---------------------------------------------------------------- Volvo
V20 = {"url": "https://azure-eu-assets.contentstack.com/v3/assets/bltccbab8edae0354cd/blt69f9c7b68d8fc5da/6846f0068fb0326a6e553940/2020-2021_FSM_Maintenance_Form_ICE-updated.pdf", "kind": "manufacturer",
       "note": "וולוו ארה\"ב, Schedule of Factory Maintenance Service Operations 2020/2021 ICE and PHEV (S60/S90/V60/V90/XC40/XC60/XC90), 2 עמודים: כל 10,000 מייל או 12 חודשים; פריטים כל 20/40/50/60/150 אלף מייל. המיילים הומרו לק\"מ"}
V25 = {"url": "https://azure-eu-assets.contentstack.com/v3/assets/bltccbab8edae0354cd/blt1f1676a16c88494e/6a29cb4fc1351a105b5ed89d/2025_FSM_Maintenance_Sheets_PHEV_MHEV_6.8.26.pdf", "kind": "manufacturer",
       "note": "וולוו ארה\"ב, גיליון 2025 PHEV/MHEV: כל 10,000 מייל או שנה; מצתים כל 60,000 מייל, רצועת אביזרים ב-80,000 מייל, רצועות תזמון/אביזרים/משאבת מים ב-150,000 מייל או 10 שנים; נוזל בלמים כל 3 שנים"}
V26EV = {"url": "https://azure-eu-assets.contentstack.com/v3/assets/bltccbab8edae0354cd/blt22bd517b635ffca9/6a29cb4cdae7b4bc40b05b92/2026_FSM_Maintenance_Sheets_Fully_Electric_6.8.26.pdf", "kind": "manufacturer",
         "note": "וולוו ארה\"ב, גיליון 2026 לרכבים חשמליים (EX30/EX40/EX90): כל 20,000 מייל או שנתיים; ב-EX30 החלפת שמן סרן חשמלי קדמי ואחורי חד-פעמית ב-40,000 מייל"}
VIL = {"url": "https://www.volvocars.com/il/", "kind": "importer", "note": "אתר וולוו ישראל וכל volvocars.com חסומים מכאן (Akamai 403); לא נמצא ספר שירות ישראלי"}
VDEAL = {"url": "https://www.volvolaval.com/en/scheduled-maintenance", "kind": "other",
         "note": "סוכנות וולוו בקנדה: טיפולים כל 16,000 ק\"מ, מסנן תא נוסעים ב-32,000, מסנן אוויר ונוזל בלמים ב-64,000, מצתים ב-96,000 - תואם להמרת הגיליון האמריקאי"}

V_INT = {"km": 16000, "months": 12, "note": "לפי גיליון וולוו ארה\"ב: כל 10,000 מייל (כ-16,000 ק\"מ) או 12 חודשים, המוקדם. מחוון השירות ברכב קובע"}


def volvo_services(mhev=False, phev=False):
    out = []
    for n in range(1, 13):
        it = [I("engine_oil", "replace"), I("oil_filter", "replace"), I("coolant", "inspect", "ריכוז נוזל נגד קיפאון ונגד קורוזיה"),
              I("transmission_oil", "inspect", "בדיקת מתג P/N של התיבה"), I("washer_fluid", "inspect"), I("wipers", "inspect"),
              I("electrical_system", "inspect", "צופר"), I("seat_belts", "inspect"), I("brake_fluid", "inspect", "מפלס"),
              I("parking_brake", "inspect"), I("brake_pads", "inspect"), I("brake_discs", "inspect"), I("tires", "inspect")]
        if mhev or phev:
            it.append(I("lights", "inspect", "תאורה חיצונית"))
        if n % 2 == 0:
            it += [I("body_underside", "inspect", "דליפות ממנוע, תיבה ותזמון"), I("lights", "adjust", "כיוון פנסים ופנסי ערפל"),
                   I("cabin_filter", "replace", "וולוו ממליצה לפחות פעם בשנה"), I("tires", "adjust", "לחץ ניפוח וכיול חיישני לחץ; גלגל חלופי")]
            if n == 2:
                it.append(I("diagnostics", "clean", "ניקוי השמשה מול מצלמת הבטיחות (פעם ראשונה בלבד)"))
        if n % 4 == 0:
            it += [I("fuel_lines", "inspect", "צנרת ומסנן דלק"), I("air_filter", "replace", "לעתים קרובות יותר בתנאי אבק"),
                   I("steering", "inspect"), I("suspension", "inspect", "קדמי ואחורי"), I("differential_oil", "inspect", "הנעה כפולה בלבד; בדיקת מפלס רק בדליפה"),
                   I("cv_boots", "inspect", "מפרקים ומגיני גומי"), I("propshaft", "inspect", "הנעה כפולה בלבד"), I("brake_lines", "inspect")]
        if n % 6 == 0:
            it.append(I("spark_plugs", "replace", "כל 60,000 מייל"))
        if (mhev or phev) and n == 8:
            it.append(I("drive_belt", "replace", "רצועת אביזרים ב-80,000 מייל (כ-128,000 ק\"מ), לפי גיליון 2025"))
        out.append({"km": 16000 * n, "items": it})
    return out


V_LONG = [I("timing_belt", "replace") | {"every_km": 240000, "every_months": 120, "note": "רצועת תזמון, מותחן וגלגלת: 150,000 מייל או 10 שנים"},
          I("drive_belt", "replace") | {"every_km": 240000, "every_months": 120, "note": "רצועת אביזרים, מותחן וגלגלת (ובגיליון 2025 גם רצועת משאבת המים): 150,000 מייל או 10 שנים"},
          I("transmission_oil", "replace") | {"every_km": 80000, "note": "וולוו ממליצה להחליף כל 50,000 מייל רק ברכב שגורר, או כשמופיעה הודעה בלוח המחוונים"}]
V_TIME = [I("brake_fluid", "replace", "וולוו: כל 3 שנים (בגיליון 2020/21: או 40,000 מייל); באזור הררי או לח - כל שנה") | {"months": 36}]
V_NOTE = ("טיוטה. אתר וולוו ישראל חסום ולא נמצא ספר שירות של היבואן. הלוח מתוך גיליונות הטיפולים הרשמיים של וולוו ארה\"ב "
          "(טיפול כל 10,000 מייל או 12 חודשים), אחרי המרה לק\"מ (16,000 ק\"מ לטיפול). בשוק הישראלי המרווח עשוי להיות שונה, ומחוון השירות ברכב קובע. "
          "במנועי Drive-E יש רצועת תזמון, שמוחלפת לפי הגיליון ב-150,000 מייל (כ-240,000 ק\"מ) או 10 שנים.")

s = dict(make="Volvo", make_he="וולוו", importer="וולוו כארס ישראל (מאיר)", id="volvo-s60-v40-xc40-xc60-xc90-2014-2022-drive-e-petrol",
         model="S60 / V40 / V60 / XC40 / XC60 / XC90 / S90 (T2/T3/T4/T5/T6)", model_he="S60 / V40 / XC40 / XC60 / XC90 בנזין",
         generation="Drive-E (VEA), 2014-2022", years=[2014, 2022],
         engines=["1.5 טורבו 3 צילינדרים (B3154T)", "1.5 טורבו (B4154T)", "2.0 טורבו (B4204T)"], fuel="petrol",
         interval=V_INT, cycle_km=192000, services=volvo_services(), long_interval=V_LONG, time_based=V_TIME,
         sources=[V20, VDEAL, VIL], status="draft", specs={"timing": "רצועת תזמון: 150,000 מייל (כ-240,000 ק\"מ) או 10 שנים לפי הגיליון", "engine_oil": "שמן סינתטי מלא בתקן ACEA A5/B5 (לפי הגיליון)"},
         notes=V_NOTE)
save(s)
VEA = {"B3154T2", "B3154T9", "B4154T2", "B4154T4", "B4204T9", "B4204T11", "B4204T14", "B4204T19", "B4204T23", "B4204T26", "B4204T27", "B4204T31", "B4204T47"}
rule("Volvo", s['id'], (2014, 2022), lambda r: r['engine'] in VEA and r['fuel'] == 'בנזין')

s = dict(make="Volvo", make_he="וולוו", importer="וולוו כארס ישראל (מאיר)", id="volvo-s60-xc40-xc60-xc90-2020-2026-mild-hybrid",
         model="S60 / V60 / XC40 / XC60 / XC90 (B3/B4/B5)", model_he="XC40 B4 / XC60 B5 / S60 B5 / XC90 B5",
         generation="Drive-E מיילד-היברידי 48V", years=[2020, 2026], engines=["2.0 טורבו מיילד-היברידי (B420T)"], fuel="petrol",
         interval=V_INT, cycle_km=192000, services=volvo_services(mhev=True), long_interval=V_LONG, time_based=V_TIME,
         sources=[V25, V20, VDEAL, VIL], status="draft", specs={"timing": "רצועת תזמון: 150,000 מייל (כ-240,000 ק\"מ) או 10 שנים לפי הגיליון", "engine_oil": "שמן סינתטי מלא בתקן ACEA A5/B5 (לפי הגיליון)"},
         notes=V_NOTE + " בגיליון 2025 של דגמי המיילד-היברידי נוספה החלפת רצועת אביזרים ב-80,000 מייל (כ-128,000 ק\"מ).")
save(s)
rule("Volvo", s['id'], (2020, 2026), lambda r: r['engine'] in {"B420T2", "B420T4", "B420T5", "B420T11"} and r['fuel'] == 'בנזין')

s = dict(make="Volvo", make_he="וולוו", importer="וולוו כארס ישראל (מאיר)", id="volvo-xc40-xc60-xc90-s60-2016-2026-plug-in-hybrid",
         model="XC40 / XC60 / XC90 / S60 / S90 / V60 (T5/T8 Recharge)", model_he="XC40 Recharge T5 / XC60 T8 / XC90 T8 / S60 T8 / S90 T8",
         generation="Twin Engine / Recharge", years=[2016, 2026], engines=["1.5 טורבו 3 צילינדרים + מנוע חשמלי (B3154T5)", "2.0 טורבו + מנוע חשמלי (B4204T34/35/46/56)"], fuel="plug-in-hybrid",
         interval=V_INT, cycle_km=192000, services=volvo_services(phev=True), long_interval=V_LONG, time_based=V_TIME,
         sources=[V20, V25, VDEAL, VIL], status="draft", specs={"timing": "רצועת תזמון: 150,000 מייל (כ-240,000 ק\"מ) או 10 שנים לפי הגיליון", "engine_oil": "שמן סינתטי מלא בתקן ACEA A5/B5 (לפי הגיליון)"},
         notes=V_NOTE + " גיליון 2020/21 חל גם על הפלאג-אין; בגיליון 2025 נוספה רצועת אביזרים ב-80,000 מייל (כ-128,000 ק\"מ).")
save(s)
rule("Volvo", s['id'], (2016, 2026), lambda r: r['engine'] in {"B4204T34", "B4204T35", "B4204T46", "B4204T56", "B3154T5"} and r['fuel'] == 'חשמל/בנזין')


def volvo_ev(n):
    it = [I("diagnostics", "inspect", "איפוס מחוון השירות"), I("cabin_filter", "replace", "וולוו ממליצה בכל טיפול"),
          I("tires", "inspect", "בלאי, עומק חריץ, לחץ וכיול חיישנים"), I("suspension", "inspect"), I("steering", "inspect"), I("cv_boots", "inspect"),
          I("wipers", "inspect"), I("electrical_system", "inspect", "צופר"), I("seat_belts", "inspect"), I("brake_pads", "inspect"), I("brake_discs", "inspect"),
          I("brake_lines", "inspect"), I("washer_fluid", "inspect"), I("brake_fluid", "inspect", "בדיקת ספיגת לחות בנוזל הבלמים")]
    if n == 2:
        it.append(I("differential_oil", "replace", "EX30 בלבד: שמן סרן חשמלי אחורי וקדמי, פעם אחת ב-40,000 מייל"))
    return {"km": 32000 * n, "items": it}


s = dict(make="Volvo", make_he="וולוו", importer="וולוו כארס ישראל (מאיר)", id="volvo-ex30-xc40-c40-ex40-2021-2026-ev",
         model="EX30 / XC40 Recharge / C40 Recharge / EX40", model_he="EX30 / XC40 חשמלי / C40 / EX40",
         generation="חשמלי", years=[2021, 2026], engines=["חשמלי"], fuel="electric",
         interval={"km": 32000, "months": 24, "note": "לפי גיליון וולוו ארה\"ב לרכב חשמלי: כל 20,000 מייל (כ-32,000 ק\"מ) או שנתיים, המוקדם"},
         cycle_km=224000, services=[volvo_ev(n) for n in range(1, 8)], long_interval=[], time_based=[],
         sources=[V26EV, VIL], status="draft", specs={},
         notes=("טיוטה. הלוח מתוך גיליון הטיפולים של וולוו ארה\"ב לדגמים החשמליים 2026 (EX30, EX40, EX90): טיפול כל 20,000 מייל או שנתיים, "
                "אחרי המרה לק\"מ. XC40/C40 Recharge מדגמי 2021-2023 הם אותו רכב כמו EX40, אבל הגיליון שנפתח הוא של 2026 - כדאי לאמת. "
                "בגיליון אין החלפה תקופתית של נוזל בלמים אלא בדיקת ספיגת לחות."))
save(s)
rule("Volvo", s['id'], (2021, 2026), lambda r: r['fuel'] == 'חשמל' and not r['model'].startswith('ES90'))

# ---------------------------------------------------------------- Audi 2.0 TFSI (Champion table)
CH = json.load(open('/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/dl/vag/champion_routine.json'))['2.0 ל׳ בנזין']
assert CH['hdr'][0] == '15,000' and len(CH['hdr']) == 8


def audi_svc(n):
    it = [I("engine_oil", "replace"), I("oil_filter", "replace"), I("brake_pads", "inspect", "קדמיות ואחוריות"), I("brake_discs", "inspect", "קדמיות ואחוריות")]
    if n % 2 == 0:
        it += [I("air_filter", "replace", "כל 30,000 ק\"מ או שנתיים"), I("cabin_filter", "replace", "כל 30,000 ק\"מ או שנה")]
    if n % 4 == 0:
        it += [I("spark_plugs", "replace", "או 4 שנים, המוקדם"), I("brake_fluid", "replace")]
    if n == 8:
        it.append(I("transmission_oil", "replace", "שמן תיבת הילוכים"))
    return {"km": 15000 * n, "items": it}


CHS = {"url": "https://www.championmotors.co.il/service-routine/", "kind": "importer",
       "note": "שגרת הטיפולים של צ'מפיון מוטורס, טבלת '2.0 ל׳ בנזין' (15,000 עד 120,000 ק\"מ). האתר חוסם בוטים; נקראה מהעתק הדף שנשמר בדפדפן אמיתי ב-28.9.2026 (dl/vag/champion_routine.html)"}
s = dict(make="Audi", make_he="אאודי", importer="צ'מפיון מוטורס", id="audi-q5-a4-a5-a6-2017-2026-2.0-tfsi",
         model="Q5 / Q5 Sportback / A4 / A5 / A6 / A3 / TT (2.0 TFSI)", model_he="Q5 / A4 / A5 / A6 2.0 TFSI",
         generation="FY / B9 / C8 / 8V", years=[2017, 2026], engines=["2.0 TFSI (DAX/DNT/DPU/DXA/DMS/DMT/DWZ/DKN/DLZ/DKZ/CZP)"], fuel="petrol",
         interval={"km": 15000, "months": 12, "note": "לפי טבלת צ'מפיון: טיפול כל 15,000 ק\"מ; מסנן מיזוג מוחלף לפחות פעם בשנה"},
         cycle_km=120000, services=[audi_svc(n) for n in range(1, 9)],
         long_interval=[I("differential_oil", "replace") | {"every_months": 36, "note": "שמן מצמד הנעה כפולה (הלדקס), אם קיים: באאודי כל שלוש שנים"},
                        I("differential_oil", "replace") | {"every_months": 24, "note": "שמן מצמד נעילת דיפרנציאל קדמי, אם קיים: כל שנתיים"}],
         time_based=[], sources=[CHS], status="draft", specs={},
         notes=("הלוח הועתק מטבלת '2.0 ל׳ בנזין' בשגרת הטיפולים של צ'מפיון מוטורס, יבואנית אאודי. הטבלה כללית לנפח המנוע ולא לדגם מסוים, "
                "ולכן נשמר כטיוטה: השיוך של קודי המנוע לנפח 2.0 נעשה לפי ידע כללי ולא אומת מול מסמך. נוזל בלמים מסומן בטבלה ב-60,000 וב-120,000 ק\"מ."))
save(s)
AUDI_CODES = {"DAX", "DNT", "DPU", "DXA", "DMS", "DMT", "DWZ", "DKN", "DLZ", "DKZ", "CZP"}
rule("Audi", s['id'], (2017, 2026), lambda r: r['engine'] in AUDI_CODES and r['fuel'] == 'בנזין' and not r['model'].startswith(('Q3', 'S', 'RS')))

# ---------------------------------------------------------------- Lexus (Israeli books)
LX_UX = {"url": "https://books.union-motors.co.il/LexusApp/api/files/74/download", "kind": "importer",
         "note": "ספר הרכב העברי של לקסוס UX200 (482 עמ'), פרק 6-3 'לוחות אחזקה', עמ' 395-396 (PDF 396-397): לוח UX200 MZA-A10, מנוע M20A (כתוב בלוח M20A-FXS), 15,000 עד 150,000 ק\"מ"}
LX_UXH = {"url": "https://books.union-motors.co.il/LexusApp/api/files/77/download", "kind": "importer",
          "note": "ספר הרכב העברי של UX250h (442 עמ'), עמ' 302: לפרטי האחזקה מפנה לחוברת השירות; אין בו לוח (גם בספר UX300h, conn 71)"}


def ux_svc(n, hybrid=False):
    km = 15 * n
    it = [I("engine_oil", "replace"), I("oil_filter", "replace"), I("battery_12v", "inspect"), I("exhaust", "inspect"),
          I("pedals", "inspect", "דוושת בלם"), I("brake_pads", "inspect"), I("brake_discs", "inspect"), I("brake_lines", "inspect"),
          I("tires", "inspect", "כולל אורות, צופר, מגבים ומתיזים"), I("lights", "inspect"), I("wipers", "inspect"), I("cabin_filter", "replace"),
          I("body_underside", "inspect", "בדיקת חלודה")]
    if km >= 105 and not hybrid:
        it.append(I("drive_belt", "inspect", "בדיקה ראשונה אחרי 105,000 ק\"מ ומאז בכל טיפול"))
    if km in (60, 120):
        it.append(I("air_filter", "replace"))
    else:
        it.append(I("air_filter", "inspect"))
    if km in (75, 150):
        it += [I("fuel_filter", "replace"), I("evap_system", "clean", "מכלול מסנן פחם")]
    if km in (45, 90, 135):
        it.append(I("evap_system", "inspect", "מכלול מסנן פחם"))
    if km % 30 == 0:
        it += [I("cooling_system", "inspect"), I("coolant", "inspect"), I("fuel_lines", "inspect", "כולל מכסה מיכל הדלק"),
               I("brake_fluid", "replace"), I("steering", "inspect"), I("cv_boots", "inspect"), I("suspension", "inspect", "מחברים כדוריים ומגיני אבק; מתלים קדמיים ואחוריים"),
               I("cvt_oil", "inspect", "נוזל תיבת הילוכים" + (" (בהיברידי: תיבה היברידית)" if hybrid else "")),
               I("differential_oil", "inspect", "שמן דיפרנציאל קדמי")]
    else:
        it.append(I("brake_fluid", "inspect"))
    if km == 90:
        it.append(I("spark_plugs", "replace", "כל 90,000 ק\"מ"))
    return {"km": km * 1000, "items": it}


UX_LONG = [I("coolant", "replace") | {"first_km": 160000, "then_every_km": 80000, "note": "נוזל קירור מנוע כולל אינטרקולר"},
           I("spark_plugs", "replace") | {"every_km": 90000},
           I("vacuum_hose", "inspect") | {"every_km": 200000, "note": "משאבת ואקום בלמים"}]
s = dict(make="Lexus", make_he="לקסוס", importer="יוניון מוטורס", id="lexus-ux200-2019-2021-2.0", model="UX 200", model_he="UX 200",
         generation="MZA-A10", years=[2019, 2021], engines=["2.0 (M20A)"], fuel="petrol",
         interval={"km": 15000, "months": 12, "note": "לפי לוח האחזקה בספר הרכב העברי: תנאי פעולה רגילים, טיפול כל 15,000 ק\"מ או 12 חודשים; בתנאים מחמירים שמן ומסנן כל 7,500 ק\"מ"},
         cycle_km=150000, services=[ux_svc(n) for n in range(1, 11)], long_interval=UX_LONG, time_based=[],
         sources=[LX_UX], status="reviewed",
         specs={"engine_oil": "0W-16 או 5W-30, 4.6 ליטר עם מסנן (לפי טבלת הנוזלים)", "coolant": "Toyota Super Long Life Coolant, 6.5 ליטר", "brake_fluid": "DOT 4 (SAE J1704 / FMVSS 116)"},
         notes=("הועתק מלוח האחזקה בספר הרכב העברי של לקסוס UX200 (תנאי פעולה רגילים). בלוח רשום 'מנוע M20A-FXS' למרות שזה ה-UX200 בנזין. "
                "בתנאים מחמירים: שמן ומסנן כל 7,500 ק\"מ, החלפת שמן התיבה כל 60,000 ק\"מ, ובדיקות בלמים והגה כל 7,500 ק\"מ."))
save(s)
rule("Lexus", s['id'], (2019, 2021), lambda r: r['model'] == 'LEXUS UX200')

s = dict(make="Lexus", make_he="לקסוס", importer="יוניון מוטורס", id="lexus-ux250h-ux300h-2019-2026-2.0-hybrid", model="UX 250h / UX 300h", model_he="UX 250h / UX 300h",
         generation="MZAH10/15", years=[2019, 2026], engines=["2.0 hybrid (M20A-FXS)"], fuel="hybrid",
         interval={"km": 15000, "months": 12, "note": "לפי לוח האחזקה של UX200 בספר העברי (אותה משפחת מנוע, ובלוח רשום M20A-FXS): כל 15,000 ק\"מ או 12 חודשים"},
         cycle_km=150000, services=[ux_svc(n, hybrid=True) for n in range(1, 11)], long_interval=UX_LONG, time_based=[],
         sources=[LX_UX, LX_UXH], status="draft",
         specs={"coolant": "Toyota Super Long Life Coolant (לפי לוח UX200)", "brake_fluid": "DOT 4 (SAE J1704 / FMVSS 116)"},
         notes=("טיוטה. ספרי הרכב העבריים של UX250h ו-UX300h מפנים לחוברת השירות ואין בהם לוח. הלוח הועתק מלוח האחזקה העברי של UX200 "
                "(אותו רכב ואותה משפחת מנוע M20A; הלוח עצמו מציין M20A-FXS, המנוע ההיברידי). שורת רצועת ההינע ושורת שמן התיבה של UX200 "
                "אינן חלות בהכרח על ההיברידי - כדאי לאמת במרכז השירות. אין כאן בדיקות ייחודיות למערכת ההיברידית (מסנן קירור סוללה וכו')."))
save(s)
rule("Lexus", s['id'], (2019, 2026), lambda r: r['model'] in ('LEXUS UX250H', 'LEXUS UX300H'))

LX_RX = {"url": "https://books.union-motors.co.il/LexusApp/api/files/148/download", "kind": "importer",
         "note": "ספר הרכב העברי של לקסוס RX300/RX350/RX350L (864 עמ'), עמ' 730: 'לוח אחזקה RX300 8AR-FTS' מיום 26.4.18, 15,000 עד 150,000 ק\"מ"}


def rx_svc(n):
    km = 15 * n
    it = [I("engine_oil", "replace"), I("oil_filter", "replace"), I("brake_pads", "inspect"), I("brake_discs", "inspect"), I("cabin_filter", "replace")]
    if km in (45, 90, 135):
        it += [I("air_filter", "replace"), I("evap_system", "inspect", "מכלול מסנן פחם")]
    else:
        it.append(I("air_filter", "inspect"))
    if km % 30 == 0:
        it += [I("cooling_system", "inspect"), I("coolant", "inspect"), I("exhaust", "inspect"), I("fuel_lines", "inspect", "כולל מכסה מיכל הדלק"),
               I("pedals", "inspect", "דוושת בלם"), I("brake_fluid", "replace"), I("brake_lines", "inspect"), I("steering", "inspect"),
               I("cv_boots", "inspect"), I("suspension", "inspect", "מחברים כדוריים; מתלים קדמיים ואחוריים"), I("tires", "inspect", "כולל אורות, צופר, מגבים"),
               I("lights", "inspect"), I("wipers", "inspect"), I("body_underside", "inspect", "בדיקת חלודה"),
               I("differential_oil", "replace", "שמן דיפרנציאל אחורי (הנעה כפולה)")]
    if km in (60, 120):
        it += [I("spark_plugs", "replace"), I("transmission_oil", "inspect"), I("differential_oil", "inspect", "שמן דיפרנציאל קדמי")]
    return {"km": km * 1000, "items": it}


s = dict(make="Lexus", make_he="לקסוס", importer="יוניון מוטורס", id="lexus-rx300-2016-2022-2.0-turbo", model="RX 300", model_he="RX 300",
         generation="AGL20/25", years=[2016, 2022], engines=["2.0 turbo (8AR-FTS)"], fuel="petrol",
         interval={"km": 15000, "months": 12, "note": "לפי לוח האחזקה בספר הרכב העברי: שמן ומסנן כל 15,000 ק\"מ או 12 חודשים גם בלי נורית; 7,500 ק\"מ או 6 חודשים בדרך לא סלולה"},
         cycle_km=150000, services=[rx_svc(n) for n in range(1, 11)],
         long_interval=[I("coolant", "replace") | {"first_km": 150000, "then_every_km": 90000},
                        I("vacuum_hose", "inspect") | {"every_km": 195000, "every_months": 120, "note": "משאבת ואקום ומגביר בלם"}],
         time_based=[], sources=[LX_RX], status="reviewed",
         specs={"engine_oil": "0W-20 או 5W-30, 4.9 ליטר עם מסנן (לפי טבלת הנוזלים)", "coolant": "Toyota Super Long Life Coolant", "brake_fluid": "DOT 3 או DOT 4",
                "_note": "שמן תיבה Toyota ATF WS, 6.7 ליטר; שמן דיפרנציאל אחורי LT 75W-85 GL-5, 0.5 ליטר (לפי הטבלה)"},
         notes=("הועתק מלוח האחזקה 'RX300 8AR-FTS' בספר הרכב העברי (תנאי פעולה רגילים). בתנאים מחמירים: מסנן אוויר נבדק כל 7,500 ק\"מ ומוחלף כל 60,000, "
                "שמן תיבה ודיפרנציאל קדמי מוחלפים ב-72 חודשים, ובדיקות בלמים, הגה ומתלים כל 7,500 ק\"מ. שמן הדיפרנציאל האחורי חל על גרסת הנעה כפולה."))
save(s)
rule("Lexus", s['id'], (2016, 2022), lambda r: r['model'] == 'LEXUS RX300')


# ---------------------------------------------------------------- Land Rover (JLR owner handbook extracts on TOPIx)
LR16 = {"url": "https://topix.landrover.jlrext.com/topix/service/procedure/565244/PDF/a806dc91-9031-45a6-a5ea-74c66d780252/en_GB", "kind": "manufacturer",
        "note": "ספר בעלים של לנד רובר (TOPIx), 'Online service history and service intervals', Service Interval Plan 1 משנת דגם 16 - ישראל ברשימת המדינות: RR/RR Sport/Discovery כל המנועים 26,000 ק\"מ או 12 חודשים; Evoque/Discovery Sport 2.0 בנזין 16,000 ק\"מ או 12 חודשים; טיפולי A/B לסירוגין"}
LR14 = {"url": "https://topix.landrover.jlrext.com/topix/service/procedure/418654/PDF/3b36d456-d7da-48a9-adc6-4ac77e49b363/en_GB", "kind": "manufacturer",
        "note": "ספר בעלים של לנד רובר (TOPIx), אותו פרק לשנת דגם 14 - ישראל ברשימה; טבלת נוזלים: נוזל בלמים כל 3 שנים ונוזל קירור כל 10 שנים ללא תלות בנסועה (Freelander 2, Discovery, Evoque, RR Sport, RR)"}
LRIL = {"url": "https://www.landrover.co.il/ownership/servicing/overview", "kind": "importer",
        "note": "דף השירות של לנד רובר ישראל: מחוון מרווחי שירות גמיש, ללא מספרים"}
LR_TIME = [I("brake_fluid", "replace", "כל 3 שנים ללא תלות בנסועה") | {"months": 36}, I("coolant", "replace", "כל 10 שנים ללא תלות בנסועה") | {"months": 120}]
LR_NOTE = ("טיוטה. המרווחים מתוך פרק השירות של ספר הבעלים של לנד רובר (מערכת TOPIx של JLR), שבו ישראל מופיעה ברשימת המדינות של תוכנית המרווחים. "
           "מחוון השירות ברכב עשוי להקדים את הטיפול לפי סגנון הנהיגה, והוא קובע. תוכן טיפולי A ו-B מפורט ב'גיליון הבדיקה' של המוסך ולא בספר, "
           "ולכן כאן מופיעים רק החלפת שמן ומסנן (שבוצעו בכל טיפול) ונוזלי הבלמים והקירור לפי הזמן. בתנאי שימוש קשים (אבק, שטח, גרירה, חום) נדרש שירות תכוף יותר.")


def lr_svcs(step):
    out = []
    for n in range(1, 5):
        kind = "A" if n % 2 else "B"
        out.append({"km": step * n, "items": [I("engine_oil", "replace", f"טיפול {kind}"), I("oil_filter", "replace"),
                                              I("diagnostics", "inspect", "תוכן מלא לפי גיליון הבדיקה של המוסך המורשה")]})
    return out


s = dict(make="Land Rover", make_he="לנד רובר", importer="לנד רובר ישראל", id="land-rover-discovery-4-range-rover-sport-2014-2019-3.0-diesel",
         model="Discovery 4 / Range Rover Sport (3.0 דיזל)", model_he="דיסקברי 4 / ריינג' רובר ספורט דיזל", generation="L319 / L494", years=[2014, 2019],
         engines=["3.0 V6 טורבו דיזל (306DT)"], fuel="diesel",
         interval={"km": 26000, "months": 12, "note": "לפי ספר הבעלים (תוכנית 1, כולל ישראל): Range Rover, Range Rover Sport ו-Discovery בכל המנועים - כל 26,000 ק\"מ או 12 חודשים, טיפולי A ו-B לסירוגין"},
         cycle_km=104000, services=lr_svcs(26000), long_interval=[], time_based=LR_TIME,
         sources=[LR16, LR14, LRIL], status="draft", specs={}, notes=LR_NOTE)
save(s)
rule("Land Rover", s['id'], (2014, 2019), lambda r: r['engine'] == '306DT' and r['fuel'] == 'דיזל' and re.search(r'DISCOVERY 4|DISCOVRY$|R\.?SPORT|R SPORT', r['model']))

s = dict(make="Land Rover", make_he="לנד רובר", importer="לנד רובר ישראל", id="land-rover-evoque-discovery-sport-2014-2018-2.0-petrol",
         model="Range Rover Evoque / Discovery Sport (2.0 בנזין)", model_he="ריינג' רובר איווק / דיסקברי ספורט בנזין", generation="L538 / L550", years=[2014, 2018],
         engines=["2.0 טורבו בנזין (204PT / PT204)"], fuel="petrol",
         interval={"km": 16000, "months": 12, "note": "לפי ספר הבעלים (תוכנית 1, כולל ישראל): Evoque ו-Discovery Sport עם מנוע בנזין 2.0 - כל 16,000 ק\"מ או 12 חודשים, טיפולי A ו-B לסירוגין"},
         cycle_km=64000, services=lr_svcs(16000), long_interval=[], time_based=LR_TIME,
         sources=[LR16, LR14, LRIL], status="draft", specs={}, notes=LR_NOTE)
save(s)
rule("Land Rover", s['id'], (2014, 2018), lambda r: r['engine'] in ('204PT', 'PT204') and r['fuel'] == 'בנזין' and re.search(r'EVOQUE|DISCOVERY SPORT|DISCOVRY SPORT', r['model']))

json.dump(rules, open(OUT + '/registry/registry_rules.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for x in stats:
    print(x)
print('total', sum(x[1] for x in stats))
