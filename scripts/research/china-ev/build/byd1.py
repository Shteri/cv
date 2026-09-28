from sched import *
IMP = 'שלמה מוטורס'
BM = 'https://www.byd.com/material/'
MHE = 'בי.וויי.די'

def ev_old(id, model, model_he, gen, years, engines, srcs, extra_note=''):
    s = Sched(id=id, make='BYD', make_he=MHE, model=model, model_he=model_he, generation=gen, years=years, engines=engines, fuel='electric', importer=IMP,
        interval={'km': 20000, 'months': 12, 'note': 'לפי ספר הנהג העברי: רוב הבדיקות כל 12 חודשים או 20,000 ק"מ; חלק מהבדיקות פעם ראשונה ב-20,000 ואז כל 40,000 ק"מ (24 חודשים), ובנהיגה קשה כל 20,000'},
        cycle_km=120000, status='reviewed',
        notes=f'ספר הנהג העברי של BYD {model} (הגה שמאלי) מפרט טבלת פריטים עם מרווח לכל פריט ולא טבלת טיפולים; כאן סודר לטיפולים של 20,000 ק"מ. אין שמן מנוע ואין החלפת מסנן מזגן קבועה (בדיקה והחלפה לפי הצורך). שמן תמסורת, נוזל קירור, רוטציה וכיול קיבולת הסוללה ב-long_interval.' + extra_note)
    s.all('body_underside', 'adjust', 'בדיקה והידוק ברגי שלדה')
    s.every('pedals', 'inspect', 40000, 'דוושת בלם ומתג בלם חניה חשמלי (EPB)', start=20000)
    s.every('parking_brake', 'inspect', 40000, 'מתג EPB', start=20000)
    s.all('brake_pads'); s.all('brake_discs')
    s.every('brake_lines', 'inspect', 40000, start=20000)
    s.every('brake_pads', 'inspect', 40000, 'פין מוביל בקליפר - כל 24 חודשים או 40,000 ק"מ', start=40000)
    s.every('steering', 'inspect', 40000, 'גלגל ההגה ומוט ההגה; מפרקים כדוריים וגומיות; קורוזיה ביחידת הבקרה של ההגה החשמלי', start=20000)
    s.all('steering', 'inspect', 'נקודות הארקה ומחברי ההגה החשמלי (EPS)')
    s.every('cv_boots', 'inspect', 40000, 'גומיות גל הינע', start=20000)
    s.every('suspension', 'inspect', 40000, 'מתלים קדמיים ואחוריים ומרווח מסבי גלגלים', start=20000)
    s.every('wheel_alignment', 'inspect', 40000, 'בדיקת זוויות גלגלים קדמיים ואחוריים', start=20000)
    s.all('tires', 'inspect', 'מצב צמיגים ולחץ אוויר כולל TPMS')
    s.all('door_hinges', 'inspect', 'מעצור דלת (שימון) ומנעול מכסה מנוע')
    s.all('coolant', 'inspect', 'מפלס נוזל קירור')
    s.every('brake_fluid', 'replace', 40000, 'החלפה כל שנתיים או 40,000 ק"מ; בשאר הטיפולים בדיקה', other='inspect')
    s.all('diagnostics', 'inspect', 'קריאת תקלות במודולים ועדכון תוכנה')
    s.all('hybrid_system', 'inspect', 'סוללת מתח גבוה: ברגי עיגון וחיבורים, כבלי מתח גבוה, דליפות ביחידת ההנעה, תוויות')
    s.all('electrical_system', 'inspect', 'שקע הטעינה')
    s.all('cabin_filter', 'inspect', 'מסנן HEPA/פחם פעיל: בדיקה והחלפה לפי הצורך; בתנאים קשים כל 6 חודשים')
    s.all('lights', 'inspect', 'פנסים, תאורת LED וכיוון אלומה')
    s.all('wipers', 'inspect', 'להבים ומתזים')
    s.li('transmission_oil', 'replace', 'שמן תמסורת: פעם ראשונה אחרי 24 חודשים או 40,000 ק"מ, אחר כך כל 24 חודשים או 48,000 ק"מ', first_km=40000, first_months=24, then_every_km=48000, then_every_months=24)
    s.li('coolant', 'replace', 'נוזל קירור ארוך טווח: כל 4 שנים או 100,000 ק"מ', every_km=100000, every_months=48)
    s.li('tire_rotation', 'rotate', 'רוטציה כל 10,000 ק"מ; לחץ אוויר - פעם בחודש', every_km=10000)
    s.li('hybrid_system', 'inspect', 'בדיקה וכיול של קיבולת סוללת המתח הגבוה: כל 6 חודשים או 72,000 ק"מ (או טעינה מלאה ופריקה עצמית)', every_km=72000, every_months=6)
    s.spec(_note='ספר הנהג העברי אינו מפרט נוזלים בטבלת התחזוקה', battery='סוללת Blade LFP; כיול קיבולת כל 6 חודשים או 72,000 ק"מ')
    for u, n in srcs: s.src(u, 'manufacturer', n)
    s.write(); return s

def ev_new(id, model, model_he, gen, years, engines, srcs, extra_note=''):
    s = Sched(id=id, make='BYD', make_he=MHE, model=model, model_he=model_he, generation=gen, years=years, engines=engines, fuel='electric', importer=IMP,
        interval={'km': 30000, 'months': 24, 'note': 'לפי ספר הנהג העברי: רוב הבדיקות כל 24 חודשים או 30,000 ק"מ'},
        cycle_km=180000, status='reviewed',
        notes=f'לפי ספר הנהג העברי של BYD {model} - מרווח של 30,000 ק"מ / 24 חודשים. שמן תמסורת, נוזל קירור וכיול סוללה ב-long_interval.' + extra_note)
    for it, n in [('brake_pads', None), ('brake_discs', None), ('brake_lines', None), ('steering', 'גלגל ומוט הגה; מפרקים כדוריים; קורוזיה והארקה של EPS'), ('cv_boots', 'גומיות גל הינע'),
                  ('suspension', 'מתלים קדמיים ואחוריים'), ('tires', 'מצב צמיגים ולחץ אוויר כולל TPMS'), ('coolant', 'מפלס נוזל קירור'),
                  ('hybrid_system', 'בליטות או עיוותים בתחתית סוללת המתח הגבוה, מגן ושסתומים; דליפות ביחידת ההנעה'), ('body_underside', 'ברגי שלדה')]:
        s.all(it, 'inspect', n)
    s.every('brake_fluid', 'replace', 30000, 'החלפה כל 24 חודשים או 30,000 ק"מ')
    s.all('cabin_filter', 'inspect', 'מסנן מיזוג: בדיקה; בתנאים קשים כל 6 חודשים והחלפה לפי הצורך')
    s.all('wheel_alignment', 'inspect', 'בבלאי לא אחיד של הצמיגים; רוטציה לפי הצורך')
    s.li('transmission_oil', 'replace', 'שמן תמסורת והמסנן: פעם ראשונה אחרי 24 חודשים או 30,000 ק"מ, אחר כך כל 24 חודשים או 48,000 ק"מ', first_km=30000, first_months=24, then_every_km=48000, then_every_months=24)
    s.li('coolant', 'replace', 'נוזל קירור ארוך טווח: כל 6 שנים או 90,000 ק"מ', every_km=90000, every_months=72)
    s.li('hybrid_system', 'inspect', 'בדיקה וכיול קיבולת סוללת המתח הגבוה: כל 6 חודשים או 72,000 ק"מ', every_km=72000, every_months=6)
    for u, n in srcs: s.src(u, 'manufacturer', n)
    s.write(); return s

def dmi(id, model, model_he, gen, years, engines, srcs, fuel_filter='inspect', air='replace15', ehs='60k', canister=True, extra_note=''):
    s = Sched(id=id, make='BYD', make_he=MHE, model=model, model_he=model_he, generation=gen, years=years, engines=engines, fuel='plug-in-hybrid', importer=IMP,
        interval={'km': 15000, 'months': 12, 'note': 'לפי ספר הנהג: שמן ומסנן שמן כל 12 חודשים או 15,000 ק"מ; רוב הבדיקות כל 24 חודשים או 30,000 ק"מ'},
        cycle_km=180000, status='reviewed',
        notes=f'ספר הנהג של BYD {model} (DM-i) מפרט טבלת פריטים עם מרווח לכל פריט; כאן סודר לטיפולים של 15,000 ק"מ. שמן גיר EHS, נוזלי קירור וכיול סוללה ב-long_interval. לפני הטיפול הראשון מומלץ לנסוע במצב ECO עם לפחות 50% שימוש במנוע (HEV), ואחריו לפחות 10%.' + extra_note)
    s.all('engine_oil', 'replace'); s.all('oil_filter', 'replace')
    s.all('coolant_hoses', 'inspect', 'שלמות צינורות הקירור והידוק החיבורים')
    for it, n in [('brake_pads', None), ('brake_discs', None), ('brake_lines', None), ('steering', 'גלגל ההגה ומוט ההגה; קורוזיה ומחברי EPS'),
                  ('cv_boots', 'כיסוי אבק של גל ההינע'), ('suspension', 'מתלים קדמיים ואחוריים, פין כדורי וכיסוי'), ('coolant', 'מפלס נוזל קירור'),
                  ('hybrid_system', 'מגש סוללת המתח הגבוה, מגנים ושסתום אוורור; דליפות ביחידת ההנעה'), ('cabin_filter', 'בדיקה; בסביבה מאובקת להחליף לפי הצורך'),
                  ('exhaust', 'דליפה במחברי צינור הפליטה'), ('fuel_lines', 'מכסה מילוי, צינור הדלק ומחברים')]:
        s.every(it, 'inspect', 30000, n)
    s.all('tires', 'inspect', 'שחיקת צמיגים; רוטציה לפי הצורך; בבלאי לא אחיד מעל 2 מ"מ לבדוק זוויות')
    s.every('brake_fluid', 'replace', 30000, 'החלפה כל שנתיים או 30,000 ק"מ; בשאר הטיפולים בדיקה', other='inspect')
    s.every('spark_plugs', 'replace', 45000, 'החלפה כל 45,000 ק"מ')
    if fuel_filter == 'replace': s.every('fuel_filter', 'replace', 30000, 'החלפה כל 24 חודשים או 30,000 ק"מ')
    elif fuel_filter == 'inspect': s.every('fuel_filter', 'inspect', 30000, 'בדיקה כל 24 חודשים או 30,000 ק"מ')
    else: s.every('fuel_filter', 'inspect', 30000, fuel_filter)
    if air == 'replace15': s.all('air_filter', 'replace', 'החלפה כל 12 חודשים או 15,000 ק"מ; בתנאים קשים בדיקה נוספת')
    elif air == 'replace30': s.every('air_filter', 'replace', 30000, 'החלפה כל 24 חודשים או 30,000 ק"מ; בתנאים קשים לבדוק לעתים קרובות')
    if canister: s.every('evap_system', 'replace', 30000, 'מסנן האבק של מכל הפחם: כל שנתיים או 30,000 ק"מ, או מוקדם יותר אם אקדח התדלוק נעצר שוב ושוב')
    if ehs == '60k':
        s.all('transmission_oil', 'inspect', 'בדיקת כמות שמן גיר EHS')
        s.li('transmission_oil', 'replace', 'שמן גיר EHS ומכלול המסנן: כל 4 שנים או 60,000 ק"מ', every_km=60000, every_months=48)
    else:
        s.all('transmission_oil', 'inspect', 'בדיקת כמות שמן גיר EHS')
        s.li('transmission_oil', 'replace', 'שמן גיר EHS: כל 300,000 ק"מ; בתנאים קשים כל 5 שנים או 80,000 ק"מ', every_km=300000)
    s.li('coolant', 'replace', 'נוזל קירור ארוך טווח של המנוע ושל מנוע ההנעה: כל 6 שנים או 90,000 ק"מ', every_km=90000, every_months=72)
    s.li('hybrid_system', 'inspect', 'טעינה מלאה ופריקה (כיול עצמי) או בדיקת קיבולת במרכז שירות: לפחות כל 6 חודשים או 72,000 ק"מ', every_km=72000, every_months=6)
    for u, n in srcs: s.src(u[0], u[1], n)
    s.write(); return s

if __name__ == '__main__':
    A3 = BM + 'byd-site/eu/support/service/manual/atto3-ev-2022/'
    s = ev_old('byd-atto-3-2022-2024-ev', 'Atto 3', 'אטו 3', 'ATTO 3 (ספר 2023-2024)', [2022, 2024], ['EV (2G / TZ200XSQ / 2F / 2H / 2A), Blade'],
        [(A3 + '2024-08-20/BYD%20ATTO%203%20%D7%9E%D7%93%D7%A8%D7%99%D7%9A%20%D7%9C%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9-%D7%94%D7%92%D7%94%20%D7%91%D7%A6%D7%93%20%D7%A9%D7%9E%D7%90%D7%9C-HE.pdf', 'ספר נהג עברי ATTO 3 (מרץ 2024), עמ\' 135-137 - לוח זמני התחזוקה (אתר BYD אירופה, עבור ישראל)'),
         (A3 + 'BYD%20ATTO%203%20%D7%9E%D7%93%D7%A8%D7%99%D7%9A%20%D7%9C%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9-%D7%94%D7%92%D7%94%20%D7%91%D7%A6%D7%93%20%D7%A9%D7%9E%D7%90%D7%9C-HE.pdf', 'מהדורה קודמת (נובמבר 2023), עמ\' 156-158 - אותם מרווחים')],
        ' בדגמי ATTO 3 המעודכנים (ספר ATTO 3 2024) המרווח הוארך ל-30,000 ק"מ / 24 חודשים - ראו קובץ נפרד; החלוקה לפי שנת רישום היא הערכה.')
    s.rule('BYD', ['ATTO 3'], [2022, 2024])
    s = ev_new('byd-atto-3-2025-2026-ev', 'Atto 3 (2024 update)', 'אטו 3', 'SC2ES', [2025, 2026], ['EV (2G / TZ200XSQ), Blade'],
        [(BM + 'byd-site/eu/support/service/manual/20250327/BYD%20ATTO%203%20(2024)%20%D7%9E%D7%93%D7%A8%D7%99%D7%9A%20%D7%9C%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9-%D7%94%D7%92%D7%94%20%D7%91%D7%A6%D7%93%20%D7%A9%D7%9E%D7%90%D7%9C-HE.pdf', 'ספר נהג עברי ATTO 3 (2024), SC2ES, מרץ 2025, עמ\' 148-149')],
        ' שיוך לשנות רישום 2025 ואילך הוא הערכה: ייתכן שחלק מרכבי 2024 כבר מהגרסה המעודכנת.')
    s.d['model'] = 'Atto 3'; s.write(); s.rule('BYD', ['ATTO 3'], [2025, 2026])
    s = ev_old('byd-dolphin-2023-2026-ev', 'Dolphin', 'דולפין', 'DOLPHIN', [2023, 2026], ['EV (TZ200XSQ / 2F / 2G), Blade'],
        [(BM + 'byd-site/eu/support/service/manual/dolphin/20231201/%D7%9E%D7%93%D7%A8%D7%99%D7%9A%20%D7%9C%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9BYD%20DOLPHIN%20-%D7%94%D7%92%D7%94%20%D7%91%D7%A6%D7%93%20%D7%A9%D7%9E%D7%90%D7%9C-HE.pdf', 'ספר נהג עברי BYD DOLPHIN (דצמבר 2023), עמ\' 131-133 - לוח זמני התחזוקה')])
    s.rule('BYD', ['BYD DOLPHIN', 'DOLPHIN'], [2023, 2026])
    s = ev_old('byd-seal-2024-2026-ev', 'Seal', 'סיל', 'SEAL', [2024, 2026], ['EV (TZ200XYC / 3M), RWD/AWD'],
        [(BM + 'byd-site/eu/support/service/manual/byd-seal/20231201/%D7%9E%D7%93%D7%A8%D7%99%D7%9A%20%D7%9C%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9BYD%20SEAL%20-%D7%94%D7%92%D7%94%20%D7%91%D7%A6%D7%93%20%D7%A9%D7%9E%D7%90%D7%9C-HE.pdf', 'ספר נהג עברי BYD SEAL (דצמבר 2023), עמ\' 151-153 - לוח זמני התחזוקה')])
    s.rule('BYD', ['SEAL'], [2024, 2026])
    s = ev_old('byd-seal-u-2024-2026-ev', 'Seal U EV', 'סיל U חשמלית', 'SEAL U EV', [2024, 2026], ['EV (TZ200XSA / TZ200XYM / TZ200XSAC)'],
        [(BM + 'byd-site/eu/support/service/manual/new-seal-u-ev/BYD%20SEAL%20U%20EV%20%D7%9E%D7%93%D7%A8%D7%99%D7%9A%20%D7%9C%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9-%D7%94%D7%92%D7%94%20%D7%91%D7%A6%D7%93%20%D7%A9%D7%9E%D7%90%D7%9C-HE.pdf', 'ספר נהג עברי BYD SEAL U EV, עמ\' 154-156 - לוח זמני התחזוקה')])
    s.rule('BYD', ['BYD SEAL U'], [2024, 2026]); s.rule('BYD', ['SEAL U'], [2024, 2026], fuel=['חשמל'])
    s = ev_new('byd-atto-2-2025-2026-ev', 'Atto 2', 'אטו 2', 'ATTO 2 EV', [2025, 2026], ['EV (TZ200XSBH)'],
        [(BM + 'ATTO%202%20Owner\'s%20Manual-Left-hand-Drive-0251212-HE.pdf', 'ספר נהג עברי ATTO 2 (דצמבר 2025), עמ\' 147-148')])
    s.rule('BYD', ['BYD ATTO 2', 'ATTO 2'], [2025, 2026])
    s = ev_new('byd-sealion-7-2025-2026-ev', 'Sealion 7', 'סילאיון 7', 'SEALION 7', [2025, 2026], ['EV (TZ200XYT), RWD/AWD'],
        [(BM + 'onwer\'smanual0612/BYD%20SEALION%207%20%D7%9E%D7%93%D7%A8%D7%99%D7%9A%20%D7%9C%D7%91%D7%A2%D7%9C%D7%99%D7%9D-Heb-20260611.pdf', 'ספר בעלים עברי SEALION 7 (יוני 2026), עמ\' 173-174')])
    s.rule('BYD', ['BYD SEALION 7', 'SEALION 7'], [2025, 2026])
    s = ev_new('byd-dolphin-surf-2025-2026-ev', 'Dolphin Surf', 'דולפין סרף', 'DOLPHIN SURF', [2025, 2026], ['EV (TZ180XSX / TZ200XSAU)'],
        [(BM + 'byd-site/eu/support/service/manual/20250702/Dolphin%20Surf%20Owner\'s%20Manual_HE.pdf', 'ספר נהג עברי BYD DOLPHIN SURF, עמ\' 130-131')],
        ' בנוסף: נוזל הקירור של סוללת המתח הגבוה מוחלף לראשונה אחרי 24 חודשים או 30,000 ק"מ ואחר כך כל 48 חודשים או 60,000 ק"מ, ונוזל הקירור של המזגן/הסוללה (מסומן בכוכבית) כל 6 שנים או 90,000 ק"מ.')
    s.li('coolant', 'replace', 'נוזל קירור של סוללת המתח הגבוה: ראשון אחרי 24 חודשים או 30,000 ק"מ, אחר כך כל 48 חודשים או 60,000 ק"מ', first_km=30000, first_months=24, then_every_km=60000, then_every_months=48)
    s.li('door_hinges', 'inspect', 'שימון מנעולי הדלתות: ראשון אחרי 5,000 ק"מ ואחר כך כל 12 חודשים או 20,000 ק"מ', first_km=5000, then_every_km=20000, then_every_months=12)
    s.write(); s.rule('BYD', ['DOLPHIN SURF'], [2025, 2026])
    # DM-i
    SU = BM + 'byd-site/eu/support/service/manual/20250106/'
    s = dmi('byd-seal-u-dm-i-2024-2026-1.5-phev', 'Seal U DM-i', 'סיל U DM-i', 'SEAL U DM-i', [2024, 2026], ['1.5 DM-i PHEV (BYD472QA) / 1.5T (BYD476ZQC)'],
        [((SU + 'BYD%20SEAL%20U%20DM-i%20%D7%9E%D7%93%D7%A8%D7%99%D7%9A%20%D7%9C%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9-%D7%94%D7%92%D7%94%20%D7%91%D7%A6%D7%93%20%D7%A9%D7%9E%D7%90%D7%9C-HE.pdf', 'manufacturer'), 'ספר נהג עברי BYD SEAL U DM-i (ינואר 2025), עמ\' 182-184 - לוח הזמנים של התחזוקה')],
        fuel_filter='inspect', air='replace15', ehs='60k', canister=True,
        extra_note=' מסנן הדלק: הספר מורה לבדוק כל 24 חודשים או 30,000 ק"מ. נוזל הקירור של סוללת המתח הגבוה מוחלף גם הוא כל 6 שנים או 90,000 ק"מ.')
    s.rule('BYD', ['SEAL U'], [2024, 2026], fuel=['חשמל/בנזין'])
    s = dmi('byd-sealion-5-2025-2026-1.5-phev', 'Sealion 5 DM-i', 'סילאיון 5', 'SEALION 5 DM-i', [2025, 2026], ['1.5 DM-i PHEV (BYD472QA)'],
        [((BM + '%E3%80%90v1%E3%80%91byd-sealion-5-owner\'s-manual-left-hand-drive/BYD%20Sealion%205%20Owner\'s%20Manual-Left-hand%20Drive-20251202-HE.pdf', 'manufacturer'), 'ספר נהג עברי BYD SEALION 5 (דצמבר 2025), עמ\' 182-183')],
        fuel_filter='מסנן דלק: הספר מציין 24 חודשים או 30,000 ק"מ בלי לפרט בדיקה או החלפה', air='replace15', ehs='60k', canister=True,
        extra_note=' לפי הספר גם אלמנט המסנן של תיבת ההילוכים מוחלף כל 4 שנים או 60,000 ק"מ.')
    s.rule('BYD', ['SEALION 5'], [2025, 2026])
    s = dmi('byd-seal-5-2025-2026-1.5-phev', 'Seal 5 DM-i', 'סיל 5', 'SEAL 5 DM-i', [2025, 2026], ['1.5 DM-i PHEV (BYD472QA / TZ220XYE3)'],
        [((BM + 'BYD%20SEAL%205%20Owner\'s%20Manual-Left-hand%20Drive-EN-250418.pdf', 'manufacturer'), 'ספר נהג אנגלי BYD SEAL 5 (הגה שמאלי, אפריל 2025), עמ\' 160-162; אין גרסה עברית באתר BYD אירופה')],
        fuel_filter='מסנן דלק (לא משולב): הספר מציין 24 חודשים או 30,000 ק"מ בלי לפרט בדיקה או החלפה', air='replace15', ehs='60k', canister=True,
        extra_note=' מקור: ספר נהג באנגלית (הגה שמאלי, BYD אירופה), לכן טיוטה. הספר מציין גם בדיקת מכל פחם כל 12 חודשים או 10,000 ק"מ.')
    s.d['status'] = 'draft'; s.li('evap_system', 'inspect', 'בדיקת מכל הפחם: כל 12 חודשים או 10,000 ק"מ', every_km=10000, every_months=12); s.write()
    s.rule('BYD', ['BYD SEAL 5', 'SEAL 5'], [2025, 2026])
    s = dmi('byd-atto-2-dm-i-2026-1.5-phev', 'Atto 2 DM-i', 'אטו 2 DM-i', 'ATTO 2 DM-i', [2026, 2026], ['1.5 DM-i PHEV (BYD472QA)'],
        [((BM + '__EU/0910atto2dmiowner/ATTO%202%20DM-i-Owner%E2%80%99s%20manual-Left-hand%20drive-20260909-EN.pdf', 'manufacturer'), 'ספר נהג אנגלי ATTO 2 DM-i (הגה שמאלי, ספטמבר 2026), עמ\' 208-210; אין גרסה עברית באתר BYD אירופה')],
        fuel_filter='replace', air='replace30', ehs='300k', canister=False,
        extra_note=' מקור: ספר נהג באנגלית (BYD אירופה), לכן טיוטה.')
    s.d['status'] = 'draft'; s.write()
    s.rule('BYD', ['BYD ATTO 2 DM-I', 'ATTO 2 DM-I'], [2026, 2026])
    save_rules('byd')
