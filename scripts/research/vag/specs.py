def load_specs(S, ns):
    SK, SE, VW, AU, CU = ns['SK'], ns['SE'], ns['VW'], ns['AU'], ns['CU']
    TSI10, TSI15 = ns['TSI10'], ns['TSI15']
    CH_ALL = TSI10 + TSI15
    GEN_NOTE = ("קבוצת פולקסווגן משתמשת באותן טבלאות שירות לכל הדגמים על אותה פלטפורמה ומשפחת מנוע, ולכן הקובץ נבנה מתבנית משותפת "
                "ומשויך לרכב לפי קוד המנוע ברישיון. ")

    # ------------------------------------------------------------------ SKODA
    S(id='skoda-octavia-2017-2026-1.0-1.5-tsi', make='Skoda', make_he='סקודה', model='Octavia', model_he='אוקטביה',
      generation='III פייסליפט (2017-2020), IV (2020 ואילך)', engines=['1.0 TSI (CHZ/DKR/DLA)', '1.5 TSI (DAD/DPC/DXD)', '1.5 eTSI (DFY)'],
      template='CH_SMALL', reg=[(SK, ['OCTAVIA', 'NEW OCTAVIA', 'OCTAVIA FL', 'OCTAVIA SPACE', 'OCTAVIA S'])], codes=CH_ALL,
      notes_pre=GEN_NOTE + "מחליף את הטיוטה skoda-octavia-2013-2025 עבור מנועי 1.0/1.5. ",
      specs={'engine_oil': 'לפי תקן VW 508 00 (0W-20) או 504 00 לפי הספר; לאמת', 'fuel': 'בנזין 95 אוקטן (טבלת המנועים במדריך היצרן)', 'battery': 'ברכב עם Start-Stop מצבר EFB או AGM', 'timing': 'רצועת תזמון (EA211), החלפה ב-120,000 לפי היבואן'})
    S(id='skoda-octavia-2013-2016-1.2-1.4-tsi', make='Skoda', make_he='סקודה', model='Octavia', model_he='אוקטביה',
      generation='III (5E), עד שנת דגם 2016', engines=['1.2 TSI (CJZ/CYV)', '1.4 TSI (CZD/CHP/CXS)'],
      template='FAC', opts={'brand': 'skoda', 'belt': 'yes', 'old_skoda': True, 'cabin60': True, 'srcs': ('OCT3', 'RAPID')},
      reg=[(SK, ['OCTAVIA', 'OCTAVIA S', 'OCTAVIA SPACE'])], codes=['CJZ', 'CYV', 'CZD', 'CHP', 'CXS'], reg_years=[2013, 2016],
      notes_pre=GEN_NOTE + "מנועי EA211 עם רצועת תזמון (טבלת המנועים במדריך). ")
    S(id='skoda-octavia-2017-2018-1.2-1.4-tsi', make='Skoda', make_he='סקודה', model='Octavia', model_he='אוקטביה',
      generation='III פייסליפט (5E), שנות דגם 2017-2018', engines=['1.2 TSI (CYV)', '1.4 TSI (CZD)'],
      template='FAC', opts={'brand': 'skoda', 'belt': 'yes', 'srcs': ('OCT3', 'RAPID')},
      reg=[(SK, ['OCTAVIA', 'NEW OCTAVIA', 'OCTAVIA S', 'OCTAVIA SPACE'])], codes=['CJZ', 'CYV', 'CZD', 'CHP', 'CXS'], reg_years=[2017, 2020],
      notes_pre=GEN_NOTE + "מנועי EA211 עם רצועת תזמון. ")
    S(id='skoda-octavia-2008-2013-1.2-1.4-1.6-1.8', make='Skoda', make_he='סקודה', model='Octavia', model_he='אוקטביה',
      generation='II (1Z) ופייסליפט', engines=['1.2 TSI (CBZ)', '1.4 TSI (CAX)', '1.6 MPI (BSE)', '1.8 TSI (CDA)'],
      template='FAC', opts={'brand': 'skoda', 'belt': 'cond', 'belt_engines': '1.6 BSE; 1.2/1.4/1.8 TSI עם שרשרת', 'old_skoda': True,
                            'plugs90': ['1.8 TSI (CDA)'], 'coolant_pump_belt_ea888': False, 'srcs': ('RAPID', 'OCT3', 'GOLF5')},
      reg=[(SK, ['OCTAVIA'])], codes=['CBZ', 'CAX', 'BSE', 'CDA'], reg_years=[2007, 2013],
      notes_pre=GEN_NOTE + "לא נמצא מדריך שירות באנגלית לאוקטביה II; הערכים לקוחים מפרק 'עד שנת דגם 2016' במדריכי סקודה לראפיד/אוקטביה III (אותם מנועים), וסוג הנעת התזמון לפי מדריך פולקסווגן גולף 5 (BSE עם רצועה) וטבלת המנועים של טיגואן (CTH/CAX עם שרשרת). ")
    S(id='skoda-octavia-2014-2018-1.8-tsi', make='Skoda', make_he='סקודה', model='Octavia', model_he='אוקטביה',
      generation='III (5E)', engines=['1.8 TSI (CJS)'],
      template='FAC', opts={'brand': 'skoda', 'belt': 'no', 'plugs90_only': True, 'coolant_pump_belt_ea888': True, 'srcs': ('OCT3',)},
      reg=[(SK, ['OCTAVIA', 'NEW OCTAVIA'])], codes=['CJS'],
      notes_pre=GEN_NOTE + "מנוע EA888 עם שרשרת תזמון; לפי מדריך סקודה המצתים ב-1.8 TSI מוחלפים כל 90,000 או 6 שנים. הקובץ משתמש בעמודת המדינות המאובקות משנת דגם 2017; עד 2016 היצרן קבע מסנן אוויר כל 90,000/6 שנים ומסנן מזגן כל שנתיים. ")
    S(id='skoda-octavia-2014-2026-2.0-tsi', make='Skoda', make_he='סקודה', model='Octavia', model_he='אוקטביה',
      generation='III RS, IV RS', engines=['2.0 TSI (CHH/DKZ/DLB/DNP)'],
      template='CH_20', opts={'brand': 'vw'}, reg=[(SK, ['OCTAVIA', 'NEW OCTAVIA', 'OCTAVIA FL'])], codes=['CHH', 'DKZ', 'DLB', 'DNP'],
      notes_pre=GEN_NOTE)
    S(id='skoda-octavia-2015-2024-2.0-tdi', make='Skoda', make_he='סקודה', model='Octavia', model_he='אוקטביה',
      generation='III, IV', engines=['2.0 TDI (CKF/CRM/DFF/DST/DTT)'], fuel='diesel',
      template='CH_D20', reg=[(SK, ['OCTAVIA', 'OCTAVIA SPACE', 'NEW OCTAVIA'])], codes=['CKF', 'CRM', 'DFF', 'DST', 'DTT'],
      notes_pre=GEN_NOTE + "נפח המנועים לפי טבלאות המנועים במדריכי אוקטביה III/IV (CKF/CRM/DFF = 2.0, DST/DTT = 2.0 EA288 evo). ")

    S(id='skoda-fabia-2017-2026-1.0-1.5-tsi', make='Skoda', make_he='סקודה', model='Fabia', model_he='פאביה',
      generation='III פייסליפט (2017-2021), IV (2021 ואילך)', engines=['1.0 TSI (CHZ/DKR/DKL/DLA/DUS)', '1.5 TSI (DPC/DXD)'],
      template='CH_SMALL', reg=[(SK, ['FABIA', 'FABIA FL', 'FABIA SPACE', 'FABIA HATCH'])], codes=CH_ALL, notes_pre=GEN_NOTE)
    S(id='skoda-fabia-2015-2016-1.2-tsi', make='Skoda', make_he='סקודה', model='Fabia', model_he='פאביה',
      generation='III (NJ), עד שנת דגם 2016', engines=['1.2 TSI (CJZ)'],
      template='FAC', opts={'drums': True, 'brand': 'skoda', 'belt': 'yes', 'old_skoda': True, 'srcs': ('FAB3', 'RAPID')},
      reg=[(SK, ['FABIA', 'FABIA SPACE'])], codes=['CJZ'], reg_years=[2014, 2016], notes_pre=GEN_NOTE)
    S(id='skoda-fabia-2017-2018-1.2-tsi', make='Skoda', make_he='סקודה', model='Fabia', model_he='פאביה',
      generation='III (NJ), שנות דגם 2017-2018', engines=['1.2 TSI (CJZ)'],
      template='FAC', opts={'drums': True, 'brand': 'skoda', 'belt': 'yes', 'srcs': ('FAB3', 'RAPID')},
      reg=[(SK, ['FABIA', 'FABIA SPACE'])], codes=['CJZ'], reg_years=[2017, 2019], notes_pre=GEN_NOTE)
    S(id='skoda-fabia-2008-2015-1.2-1.4-1.6', make='Skoda', make_he='סקודה', model='Fabia', model_he='פאביה',
      generation='II (5J) ופייסליפט', engines=['1.2 TSI (CBZ)', '1.4 MPI (CGG/BXW)', '1.6 MPI (BTS)'],
      template='FAC', opts={'drums': True, 'brand': 'skoda', 'belt': 'cond', 'belt_engines': '1.4 MPI CGG', 'old_skoda': True, 'awd': False, 'srcs': ('RAPID', 'FAB3')},
      reg=[(SK, ['FABIA', 'FABIA HATCH', 'FABIA SPACE'])], codes=['CBZ', 'CGG', 'BTS', 'BXW'], reg_years=[2007, 2015],
      notes_pre=GEN_NOTE + "לא נמצא מדריך שירות לפאביה II; הערכים לקוחים מפרק 'עד שנת דגם 2016' במדריכי סקודה לראפיד ולפאביה III (פלטפורמה ומנועים קרובים). ")

    S(id='skoda-kodiaq-2019-2026-1.5-tsi', make='Skoda', make_he='סקודה', model='Kodiaq', model_he='קודיאק',
      generation='I (NS) ופייסליפט, II (2024 ואילך)', engines=['1.5 TSI (DAD/DPC)', '1.5 TSI evo2 (DXD)'],
      template='CH_SMALL', opts={'has10': False}, reg=[(SK, ['KODIAQ', 'KODIAQ FL'])], codes=TSI15, notes_pre=GEN_NOTE)
    S(id='skoda-kodiaq-2017-2018-1.4-tsi', make='Skoda', make_he='סקודה', model='Kodiaq', model_he='קודיאק',
      generation='I (NS)', engines=['1.4 TSI (CZE/CZD/CZC)'],
      template='FAC', opts={'brand': 'skoda', 'belt': 'yes', 'srcs': ('KOD', 'OCT3')},
      reg=[(SK, ['KODIAQ'])], codes=['CZE', 'CZD', 'CZC'], notes_pre=GEN_NOTE + "קודי המנוע והנפח לפי טבלת המנועים במדריך קודיאק. ")
    S(id='skoda-kodiaq-2017-2026-2.0-tsi', make='Skoda', make_he='סקודה', model='Kodiaq', model_he='קודיאק',
      generation='I (NS), II', engines=['2.0 TSI (CZP/DKZ/DNN)'],
      template='CH_20', opts={'brand': 'vw'}, reg=[(SK, ['KODIAQ', 'KODIAQ FL'])], codes=['CZP', 'DKZ', 'DNN'], notes_pre=GEN_NOTE)
    S(id='skoda-kodiaq-2017-2026-2.0-tdi', make='Skoda', make_he='סקודה', model='Kodiaq', model_he='קודיאק',
      generation='I (NS), II', engines=['2.0 TDI (DFG/DFH/DTS/DTU/DXN/DXP)'], fuel='diesel',
      template='CH_D20', reg=[(SK, ['KODIAQ', 'KODIAQ FL'])], codes=['DFG', 'DFH', 'DTS', 'DTU', 'DXN', 'DXP'], notes_pre=GEN_NOTE)

    S(id='skoda-rapid-2013-2016-1.2-1.4-tsi', make='Skoda', make_he='סקודה', model='Rapid', model_he='ראפיד',
      generation='NH, עד שנת דגם 2016', engines=['1.2 TSI (CBZ/CJZ)', '1.4 TSI (CAX/CZC)'],
      template='FAC', opts={'drums': True, 'brand': 'skoda', 'belt': 'cond', 'belt_engines': 'CJZ/CZC עם רצועה (EA211); ב-CAX מדבקת קוד המנוע על בית שרשרת התזמון', 'old_skoda': True, 'awd': False, 'srcs': ('RAPID',)},
      reg=[(SK, ['RAPID', 'SPACEBACK'])], codes=['CBZ', 'CAX', 'CJZ', 'CZC'], reg_years=[2012, 2016], notes_pre=GEN_NOTE)
    S(id='skoda-rapid-2017-2019-1.2-1.4-tsi', make='Skoda', make_he='סקודה', model='Rapid', model_he='ראפיד',
      generation='NH פייסליפט, משנת דגם 2017', engines=['1.2 TSI (CJZ)', '1.4 TSI (CZC)'],
      template='FAC', opts={'drums': True, 'brand': 'skoda', 'belt': 'yes', 'awd': False, 'srcs': ('RAPID',)},
      reg=[(SK, ['RAPID', 'SPACEBACK'])], codes=['CJZ', 'CZC'], reg_years=[2017, 2019], notes_pre=GEN_NOTE)
    S(id='skoda-rapid-2017-2019-1.0-tsi', make='Skoda', make_he='סקודה', model='Rapid', model_he='ראפיד',
      generation='NH פייסליפט', engines=['1.0 TSI (CHZ/DKR)'],
      template='CH_SMALL', opts={'has15': False}, reg=[(SK, ['RAPID', 'SPACEBACK'])], codes=TSI10, notes_pre=GEN_NOTE)

    S(id='skoda-karoq-2018-2026-1.0-1.5-tsi', make='Skoda', make_he='סקודה', model='Karoq', model_he='קארוק',
      generation='NU ופייסליפט', engines=['1.0 TSI (CHZ/DKR)', '1.5 TSI (DAD/DPC/DXD)'],
      template='CH_SMALL', reg=[(SK, ['KAROQ', 'KAROQ FL'])], codes=CH_ALL, notes_pre=GEN_NOTE)
    S(id='skoda-kamiq-2020-2026-1.0-1.5-tsi', make='Skoda', make_he='סקודה', model='Kamiq', model_he='קאמיק',
      generation='NW ופייסליפט', engines=['1.0 TSI (DKR/DLA/DUS)', '1.5 TSI (DPC/DXD)'],
      template='CH_SMALL', reg=[(SK, ['KAMIQ', 'KAMIQ FL'])], codes=CH_ALL, notes_pre=GEN_NOTE)
    S(id='skoda-scala-2020-2026-1.0-1.5-tsi', make='Skoda', make_he='סקודה', model='Scala', model_he='סקאלה',
      generation='NW ופייסליפט', engines=['1.0 TSI (DKR/DLA/DUS)', '1.5 TSI (DPC)'],
      template='CH_SMALL', reg=[(SK, ['SCALA', 'SCALA FL'])], codes=CH_ALL, notes_pre=GEN_NOTE)

    S(id='skoda-superb-2009-2015-1.8-2.0-tsi', make='Skoda', make_he='סקודה', model='Superb', model_he='סופרב',
      generation='II (3T)', engines=['1.8 TSI (CDA)', '2.0 TSI (CCZ)'],
      template='FAC', opts={'brand': 'skoda', 'belt': 'no', 'old_skoda': True, 'plugs90_only': True, 'coolant_pump_belt_ea888': False, 'srcs': ('OCT3', 'TIG1')},
      reg=[(SK, ['SUPERB'])], codes=['CDA', 'CCZ'], reg_years=[2008, 2015],
      notes_pre=GEN_NOTE + "מנועי EA888 דור 2 עם שרשרת תזמון (טבלת המנועים של טיגואן 2008). מצתים כל 90,000 או 6 שנים לפי מדריכי פולקסווגן לקודי CDAA/CCZB. ")
    S(id='skoda-superb-2015-2019-1.8-tsi', make='Skoda', make_he='סקודה', model='Superb', model_he='סופרב',
      generation='III (3V)', engines=['1.8 TSI (CJS)'],
      template='FAC', opts={'brand': 'skoda', 'belt': 'no', 'plugs90_only': True, 'coolant_pump_belt_ea888': True, 'srcs': ('OCT3',)},
      reg=[(SK, ['SUPERB', 'NEW SUPERB'])], codes=['CJS'],
      notes_pre=GEN_NOTE + "לפי מדריך סקודה המצתים ב-1.8 TSI מוחלפים כל 90,000 או 6 שנים. ")
    S(id='skoda-superb-2015-2026-2.0-tsi', make='Skoda', make_he='סקודה', model='Superb', model_he='סופרב',
      generation='III (3V) ופייסליפט, IV', engines=['2.0 TSI (CHH/CJX/DKZ/DNU/DNF/DNN/DNP)'],
      template='CH_20', opts={'brand': 'vw'}, reg=[(SK, ['SUPERB', 'NEW SUPERB', 'SUPERB FL'])], codes=['CHH', 'CJX', 'DKZ', 'DNU', 'DNF', 'DNN', 'DNP'], notes_pre=GEN_NOTE)
    S(id='skoda-superb-2015-2019-1.4-tsi', make='Skoda', make_he='סקודה', model='Superb', model_he='סופרב',
      generation='III (3V)', engines=['1.4 TSI (CZE)'],
      template='FAC', opts={'brand': 'skoda', 'belt': 'yes', 'srcs': ('OCT3', 'KOD')},
      reg=[(SK, ['SUPERB', 'NEW SUPERB'])], codes=['CZE'],
      notes_pre=GEN_NOTE + "הקובץ משתמש בעמודת המדינות המאובקות משנת דגם 2017; עד 2016 היצרן קבע מסנן אוויר כל 90,000/6 שנים, מסנן מזגן כל שנתיים ונוזל בלמים ראשון אחרי 3 שנים. ")
    S(id='skoda-superb-2019-2026-1.5-tsi', make='Skoda', make_he='סקודה', model='Superb', model_he='סופרב',
      generation='III פייסליפט, IV', engines=['1.5 TSI (DAD/DPC/DXD)'],
      template='CH_SMALL', opts={'has10': False}, reg=[(SK, ['SUPERB', 'SUPERB FL'])], codes=TSI15, notes_pre=GEN_NOTE)
    S(id='skoda-superb-2018-2024-2.0-tdi', make='Skoda', make_he='סקודה', model='Superb', model_he='סופרב',
      generation='III (3V) ופייסליפט', engines=['2.0 TDI (DFH/DTU)'], fuel='diesel',
      template='CH_D20', reg=[(SK, ['SUPERB', 'SUPERB FL'])], codes=['DFH', 'DTU'], notes_pre=GEN_NOTE)
    S(id='skoda-superb-2021-2024-1.4-phev', make='Skoda', make_he='סקודה', model='Superb iV', model_he='סופרב iV',
      generation='III פייסליפט, היברידי נטען', engines=['1.4 TSI PHEV (DGE)'], fuel='plug-in-hybrid',
      template='CH_PHEV', reg=[(SK, ['SUPERB', 'SUPERB FL IV'])], codes=['DGE'], notes_pre=GEN_NOTE)

    S(id='skoda-yeti-2010-2016-1.2-1.4-tsi', make='Skoda', make_he='סקודה', model='Yeti', model_he='ייטי',
      generation='5L', engines=['1.2 TSI (CBZ)', '1.4 TSI (CAX)'],
      template='FAC', opts={'brand': 'skoda', 'belt': 'no', 'old_skoda': True, 'srcs': ('RAPID', 'OCT3')},
      reg=[(SK, ['YETI'])], codes=['CBZ', 'CAX'], reg_years=[2009, 2016],
      notes_pre=GEN_NOTE + "מנועי EA111 (CBZ/CAX); בטבלאות היצרן אין להם החלפת רצועת תזמון. לא נמצא מדריך שירות לייטי; הערכים לפי פרק 'עד שנת דגם 2016' במדריכי ראפיד ואוקטביה III. ")
    S(id='skoda-yeti-2015-2018-1.2-tsi', make='Skoda', make_he='סקודה', model='Yeti', model_he='ייטי',
      generation='5L פייסליפט', engines=['1.2 TSI (CYV)', '1.4 TSI (CZC)'],
      template='FAC', opts={'brand': 'skoda', 'belt': 'yes', 'srcs': ('OCT3', 'RAPID')},
      reg=[(SK, ['YETI', 'NEW YETI'])], codes=['CYV', 'CZC'],
      notes_pre=GEN_NOTE + "מנועי EA211 עם רצועת תזמון. הקובץ משתמש בעמודת המדינות המאובקות משנת דגם 2017; עד 2016 היצרן קבע מסנן אוויר כל 90,000/6 שנים, מסנן מזגן כל שנתיים ונוזל בלמים ראשון אחרי 3 שנים. ")
    S(id='skoda-roomster-2008-2015-1.2-1.4-1.6', make='Skoda', make_he='סקודה', model='Roomster', model_he='רומסטר',
      generation='5J', engines=['1.2 TSI (CBZ)', '1.4 MPI (CGG)', '1.6 MPI (BTS)'],
      template='FAC', opts={'drums': True, 'brand': 'skoda', 'belt': 'cond', 'belt_engines': '1.4 MPI CGG', 'old_skoda': True, 'awd': False, 'srcs': ('RAPID', 'FAB3')},
      reg=[(SK, ['ROOMSTER'])], codes=['CBZ', 'CGG', 'BTS'], notes_pre=GEN_NOTE + "לא נמצא מדריך שירות לרומסטר; הערכים לפי פרק 'עד שנת דגם 2016' במדריכי ראפיד ופאביה III. ")
    S(id='skoda-citigo-2013-2018-1.0', make='Skoda', make_he='סקודה', model='Citigo', model_he='סיטיגו',
      generation='NF', engines=['1.0 MPI (CHY)'],
      template='FAC', opts={'drums': True, 'brand': 'skoda', 'belt': 'cond', 'belt_engines': 'משפחת EA211', 'old_skoda': True, 'awd': False, 'srcs': ('FAB3', 'RAPID')},
      reg=[(SK, ['CITIGO'])], codes=['CHY'],
      notes_pre=GEN_NOTE + "מדריך פאביה III: במנועי 1.0 MPI מסנן האוויר מוחלף כל 60,000 או 4 שנים בתנאים רגילים וכל 30,000 או שנתיים במדינות מאובקות. ",
      notes_post="לרוב הרכבים משנים 2013-2016 חלות טבלאות 'עד 2016'; לשנים 2017-2018 טבלאות סקודה החדשות קובעות מסנן מזגן כל 30,000 או שנה, רצועת אביזרים כל 60,000 ונוזל בלמים כל שנתיים.")
    S(id='skoda-enyaq-2022-2026-ev', make='Skoda', make_he='סקודה', model='Enyaq', model_he='אניאק',
      generation='iV / Coupe iV', engines=['חשמלי (EBJ)'], fuel='electric',
      template='CH_BEV', reg=[(SK, ['ENYAQ IV', 'ENYAQ COUPE IV', 'ENYAQ IV 80', 'ENYAQ 80', 'ENYAQ'])], codes=['EBJ'], notes_pre=GEN_NOTE)

    # ------------------------------------------------------------------ SEAT / CUPRA
    S(id='seat-ibiza-2015-2026-1.0-1.5-tsi', make='Seat', make_he='סיאט', model='Ibiza', model_he='איביזה',
      generation='6J פייסליפט (1.0 TSI), 6F (2017 ואילך)', engines=['1.0 TSI (CHZ/DKR/DKJ/DKL/DLA/DUS)', '1.5 TSI (DPC/DXD)'],
      template='CH_SMALL', reg=[(SE, ['IBIZA'])], codes=CH_ALL, notes_pre=GEN_NOTE)
    S(id='seat-ibiza-2008-2017-1.2-1.4-1.6', make='Seat', make_he='סיאט', model='Ibiza', model_he='איביזה',
      generation='6J ופייסליפט', engines=['1.2 TSI (CBZ/CJZ)', '1.4 MPI (CGG/BXW)', '1.6 MPI (BTS)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'cond', 'belt_engines': 'CJZ (EA211) ו-1.4 MPI CGG/BXW; CBZ עם שרשרת', 'awd': False, 'srcs': ('LEON3', 'GOLF7', 'POLO')},
      reg=[(SE, ['IBIZA', 'IBIZA FLOW', 'IBIZA ST'])], codes=['CBZ', 'CJZ', 'CGG', 'BXW', 'BTS'],
      notes_pre=GEN_NOTE + "לא נמצא מדריך שירות לאיביזה 6J; הערכים לפי טבלאות סיאט לאון 3 ופולקסווגן (אותם מנועים ואותה שיטת שירות). ")
    S(id='seat-arona-2018-2026-1.0-1.5-tsi', make='Seat', make_he='סיאט', model='Arona', model_he='ארונה',
      generation='KJ ופייסליפט', engines=['1.0 TSI (DKR/DKJ/DLA/DUS)', '1.5 TSI (DPC/DXD)'],
      template='CH_SMALL', reg=[(SE, ['ARONA'])], codes=CH_ALL, notes_pre=GEN_NOTE)
    S(id='seat-leon-2013-2018-1.2-1.4-tsi', make='Seat', make_he='סיאט', model='Leon', model_he='לאון',
      generation='III (5F)', engines=['1.2 TSI (CJZ/CYV)', '1.4 TSI (CZE/CXS/CZC)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'yes', 'srcs': ('LEON3', 'GOLF7')},
      reg=[(SE, ['LEON'])], codes=['CJZ', 'CYV', 'CZE', 'CXS', 'CZC', 'CZD', 'CHP', 'CMB'], notes_pre=GEN_NOTE)
    S(id='seat-leon-2013-2018-1.8-tsi', make='Seat', make_he='סיאט', model='Leon', model_he='לאון',
      generation='III (5F)', engines=['1.8 TSI (CJS)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'no', 'srcs': ('LEON3', 'GOLF7')},
      reg=[(SE, ['LEON'])], codes=['CJS'], notes_pre=GEN_NOTE + "מנוע EA888 דור 3 עם שרשרת תזמון. ")
    S(id='seat-leon-2010-2013-1.2-1.4-1.8-tsi', make='Seat', make_he='סיאט', model='Leon', model_he='לאון',
      generation='II (1P) פייסליפט', engines=['1.2 TSI (CBZ)', '1.4 TSI (CAX)', '1.8 TSI (CDA)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'no', 'plugs90': ['1.8 TSI (CDA)'], 'srcs': ('PASSAT7', 'TIG1', 'LEON3')},
      reg=[(SE, ['LEON'])], codes=['CBZ', 'CAX', 'CDA'], reg_years=[2009, 2013],
      notes_pre=GEN_NOTE + "לא נמצא מדריך שירות ללאון II; הערכים לפי מדריכי פולקסווגן במהדורות מאוחרות לדגמים עם אותם מנועים (פאסאט B7, טיגואן 2008). ")
    S(id='seat-leon-2017-2025-1.0-1.5-tsi', make='Seat', make_he='סיאט', model='Leon', model_he='לאון',
      generation='III פייסליפט, IV (KL)', engines=['1.0 TSI (CHZ/DLA)', '1.5 TSI (DAD/DPC)', '1.5 eTSI (DFY)'],
      template='CH_SMALL', reg=[(SE, ['LEON'])], codes=CH_ALL, notes_pre=GEN_NOTE)
    S(id='seat-leon-2015-2022-2.0-tsi', make='Seat', make_he='סיאט', model='Leon Cupra', model_he='לאון קופרה',
      generation='III, IV', engines=['2.0 TSI (CJX/DKZ/DNU/DNN)'],
      template='CH_20', opts={'brand': 'seat'}, reg=[(SE, ['LEON', 'LEON CUPRA FL'])], codes=['CJX', 'DKZ', 'DNU', 'DNN'], notes_pre=GEN_NOTE)
    S(id='seat-ateca-2017-2019-1.4-tsi', make='Seat', make_he='סיאט', model='Ateca', model_he='אטקה',
      generation='KH7', engines=['1.4 TSI (CZE)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'yes', 'srcs': ('LEON3', 'GOLF7')},
      reg=[(SE, ['ATECA'])], codes=['CZE'], notes_pre=GEN_NOTE)
    S(id='seat-ateca-2019-2026-1.5-tsi', make='Seat', make_he='סיאט', model='Ateca', model_he='אטקה',
      generation='KH7 ופייסליפט', engines=['1.5 TSI (DAD/DPC/DXD)'],
      template='CH_SMALL', opts={'has10': False}, reg=[(SE, ['ATECA', 'ATECA STYLE', 'ATECA FR', 'ATECA XPERIENCE'])], codes=TSI15, notes_pre=GEN_NOTE)
    S(id='seat-cupra-2020-2024-2.0-tsi', make='Seat', make_he='סיאט', model='Cupra (Formentor / Ateca)', model_he='קופרה (פורמנטור / אטקה)',
      generation='רשום כסיאט', engines=['2.0 TSI (DNF/DNU/DNN)'],
      template='CH_20', opts={'brand': 'cupra'}, reg=[(SE, ['CUPRA', 'CUPRA ATECA'])], codes=['DNF', 'DNU', 'DNN'],
      notes_pre=GEN_NOTE + "ברישיון הרכב הדגם רשום כ'סיאט CUPRA'. ")
    S(id='seat-cupra-2021-2024-1.5-tsi', make='Seat', make_he='סיאט', model='Cupra Formentor', model_he='קופרה פורמנטור',
      generation='רשום כסיאט', engines=['1.5 TSI (DPC)', '1.5 eTSI (DFY)'],
      template='CH_SMALL', opts={'has10': False}, reg=[(SE, ['CUPRA'])], codes=TSI15,
      notes_pre=GEN_NOTE + "ברישיון הרכב הדגם רשום כ'סיאט CUPRA'. ")
    S(id='seat-cupra-2023-2024-1.4-phev', make='Seat', make_he='סיאט', model='Cupra e-Hybrid', model_he='קופרה e-Hybrid',
      generation='רשום כסיאט', engines=['1.4 TSI PHEV (DGE)'], fuel='plug-in-hybrid',
      template='CH_PHEV', reg=[(SE, ['CUPRA'])], codes=['DGE'], notes_pre=GEN_NOTE)
    S(id='cupra-formentor-leon-2024-2026-1.5-tsi', make='Cupra', make_he='קופרה', model='Formentor / Leon', model_he='פורמנטור / לאון',
      generation='רשום כקופרה (2024 ואילך)', engines=['1.5 TSI (DPC/DXD)'],
      template='CH_SMALL', opts={'has10': False}, reg=[(CU, ['FORMENTOR', 'CUPRA LEON', 'CUPRA'])], codes=TSI15,
      notes_pre=GEN_NOTE + "היצרן 'קופרה' אינו ברשימת היצרנים של lookup_plate, ולכן כלל השיוך משתמש בשם העברי. ")
    S(id='seat-toledo-2013-2018-1.4-tsi', make='Seat', make_he='סיאט', model='Toledo', model_he='טולדו',
      generation='KG (NH)', engines=['1.4 TSI (CAX/CZC)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'cond', 'belt_engines': 'CZC (EA211); CAX עם שרשרת', 'awd': False, 'srcs': ('LEON3', 'RAPID')},
      reg=[(SE, ['TOLEDO'])], codes=['CAX', 'CZC'], notes_pre=GEN_NOTE + "טולדו חולקת פלטפורמה ומנועים עם סקודה ראפיד. ")
    S(id='seat-mii-2013-2017-1.0', make='Seat', make_he='סיאט', model='Mii', model_he='מי',
      generation='KF', engines=['1.0 MPI (CHY)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'cond', 'belt_engines': 'משפחת EA211', 'awd': False, 'srcs': ('GOLF7', 'LEON3')},
      reg=[(SE, ['MII'])], codes=['CHY'],
      notes_pre=GEN_NOTE + "טבלת גולף 7 כוללת הערה נפרדת לפולקסווגן up! (אחות של Mii): מסנן אוויר כל 60,000 או 4 שנים בתנאים רגילים וכל 30,000 או שנתיים במדינות מאובקות. ")

    # ------------------------------------------------------------------ VOLKSWAGEN
    S(id='vw-golf-2019-2026-1.0-1.5-tsi', make='Volkswagen', make_he='פולקסווגן', model='Golf', model_he='גולף',
      generation='7 פייסליפט (1.5), 8', engines=['1.0 TSI (DKR/DLA)', '1.5 TSI (DAD/DPC/DXD)', '1.5 eTSI (DFY)'],
      template='CH_SMALL', reg=[(VW, ['GOLF'])], codes=CH_ALL, notes_pre=GEN_NOTE)
    S(id='vw-golf-2013-2020-1.2-1.4-tsi', make='Volkswagen', make_he='פולקסווגן', model='Golf', model_he='גולף',
      generation='7 (5G)', engines=['1.2 TSI (CJZ/CYV)', '1.4 TSI (CZC/CZD/CXS/CMB)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'yes', 'srcs': ('GOLF7',)},
      reg=[(VW, ['GOLF'])], codes=['CJZ', 'CYV', 'CZC', 'CZD', 'CXS', 'CMB', 'CHP', 'CPT'], reg_years=[2013, 2020],
      notes_pre=GEN_NOTE + "בטבלת המנועים של מדריך גולף 7 כל מנועי ה-1.2/1.4 TSI האלה מסומנים עם רצועת תזמון. ")
    S(id='vw-golf-2006-2013-1.2-1.4-1.6', make='Volkswagen', make_he='פולקסווגן', model='Golf', model_he='גולף',
      generation='5 (1K), 6 (5K), Golf Plus', engines=['1.6 MPI (BSE/BGU)', '1.6 FSI (BLF)', '1.2 TSI (CBZ)', '1.4 TSI (CAX/CAV)', '2.0 FSI (BVY)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'cond', 'belt_engines': '1.6 BSE/BGU ו-2.0 BVY לפי מדריך גולף 5; ב-TSI שרשרת', 'srcs': ('TIG1', 'PASSAT7', 'GOLF5')},
      reg=[(VW, ['GOLF', 'GOLF PLUS'])], codes=['BSE', 'BGU', 'BLF', 'CBZ', 'CAX', 'CAV', 'BVY'], reg_years=[2004, 2014],
      notes_pre=GEN_NOTE + "לא נמצאה מהדורה עדכנית של מדריך השירות לגולף 5/6; הערכים לפי טבלאות פולקסווגן במהדורות 2019-2021 לדגמים ישנים עם אותם מנועים (טיגואן 2008, פאסאט 2011). "
                "במהדורת 2009 של מדריך גולף 5 (לפני טבלאות 'אבק רב'): מסנן אוויר כל 90,000/6 שנים, מסנן מזגן כל 60,000/שנתיים, רצועת התזמון ב-BSE/BUD ללא החלפה קבועה אלא בדיקה מ-90,000 ואז כל 30,000, ורצועת 2.0 FSI כל 180,000. ")
    S(id='vw-golf-2013-2026-2.0-tsi', make='Volkswagen', make_he='פולקסווגן', model='Golf GTI', model_he='גולף GTI',
      generation='7, 8', engines=['2.0 TSI (CHH/DKT/DNP)'],
      template='CH_20', opts={'brand': 'vw'}, reg=[(VW, ['GOLF', 'GOLF GTI'])], codes=['CHH', 'DKT', 'DNP', 'CJX'], notes_pre=GEN_NOTE)
    S(id='vw-polo-2018-2026-1.0-tsi', make='Volkswagen', make_he='פולקסווגן', model='Polo', model_he='פולו',
      generation='6 (AW)', engines=['1.0 TSI (CHZ/DKR/DKL/DKJ/DLA)'],
      template='CH_SMALL', opts={'has15': False}, reg=[(VW, ['POLO'])], codes=TSI10, notes_pre=GEN_NOTE)
    S(id='vw-polo-2005-2017-1.2-1.4-1.6', make='Volkswagen', make_he='פולקסווגן', model='Polo', model_he='פולו',
      generation='4 (9N) ו-5 (6R)', engines=['1.2 TSI (CBZ/CJZ)', '1.4 MPI (BUD/BKY/BBY/CGG)', '1.6 MPI (BTS)', '1.4 TSI (CTH/CAV)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'cond', 'belt_engines': 'CJZ (EA211) ו-1.4 MPI BUD/BKY/BBY/CGG; ב-CBZ/CTH/CAV יש שרשרת', 'awd': False, 'srcs': ('POLO', 'GOLF7', 'TIG1')},
      reg=[(VW, ['POLO'])], codes=['CBZ', 'CJZ', 'CGG', 'BUD', 'BKY', 'BBY', 'BTS', 'CTH', 'CAV'], reg_years=[2003, 2017],
      notes_pre=GEN_NOTE + "טבלאות פולקסווגן כוללות הערה נפרדת לפולו 6R: מסנן מזגן בתנאים רגילים כל 30,000 או שנתיים (במדינות מאובקות כמו בשאר הדגמים, שנה או 30,000). ")
    S(id='vw-jetta-2006-2018-1.2-1.4-1.6', make='Volkswagen', make_he='פולקסווגן', model='Jetta', model_he="ג'טה",
      generation='5 (1K), 6 (1B)', engines=['1.6 MPI (BSE)', '1.2 TSI (CBZ/CYV)', '1.4 TSI (CAX/CAV/CZC)', '2.0 FSI (BVY)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'cond', 'belt_engines': '1.6 BSE, 2.0 BVY, 1.2 CYV ו-1.4 CZC (EA211); CBZ/CAX/CAV עם שרשרת', 'srcs': ('TIG1', 'PASSAT7', 'GOLF7', 'GOLF5')},
      reg=[(VW, ['JETTA'])], codes=['BSE', 'CBZ', 'CAX', 'CYV', 'CZC', 'BVY', 'CAV'],
      notes_pre=GEN_NOTE + "לא נמצא מדריך שירות לג'טה 6; הערכים לפי טבלאות פולקסווגן במהדורות מאוחרות לדגמים עם אותם מנועים (גולף 7, טיגואן 2008, פאסאט 2011). ")
    S(id='vw-tiguan-2008-2016-1.4-2.0-tsi', make='Volkswagen', make_he='פולקסווגן', model='Tiguan', model_he='טיגואן',
      generation='1 (5N)', engines=['1.4 TSI (CTH/CZD)', '2.0 TSI (CAW/CCZ)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'cond', 'belt_engines': 'CZD בלבד; CTH/CAW/CCZ עם שרשרת לפי טבלת המנועים', 'plugs90': ['2.0 TSI (CAW/CCZ)'], 'srcs': ('TIG1',)},
      reg=[(VW, ['TIGUAN'])], codes=['CTH', 'CZD', 'CAW', 'CCZ'], reg_years=[2007, 2016],
      notes_pre=GEN_NOTE + "מבוסס על מדריך השירות של טיגואן 2008 עצמו (מהדורה 03.2021). ")
    S(id='vw-tiguan-2017-2018-1.4-tsi', make='Volkswagen', make_he='פולקסווגן', model='Tiguan', model_he='טיגואן',
      generation='2 (AD)', engines=['1.4 TSI (CZE)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'yes', 'srcs': ('GOLF7', 'TIG1')},
      reg=[(VW, ['TIGUAN'])], codes=['CZE'], reg_years=[2016, 2019], notes_pre=GEN_NOTE)
    S(id='vw-tiguan-2019-2026-1.5-tsi', make='Volkswagen', make_he='פולקסווגן', model='Tiguan', model_he='טיגואן',
      generation='2 (AD) ופייסליפט, Allspace, 3', engines=['1.5 TSI (DAD/DPC)', '1.5 eTSI (DXD)'],
      template='CH_SMALL', opts={'has10': False}, reg=[(VW, ['TIGUAN', 'TIGUAN ALLSPACE', 'TIGUAN AS', 'TIGUAN AS 1.5 E', 'TIGUAN FL 1.5', 'TIGUAN FL 1.5L', 'TIGUAN FL'])], codes=TSI15, notes_pre=GEN_NOTE)
    S(id='vw-tiguan-2017-2026-2.0-tsi', make='Volkswagen', make_he='פולקסווגן', model='Tiguan', model_he='טיגואן',
      generation='2 (AD), Allspace', engines=['2.0 TSI (CZP/DKZ/DNN)'],
      template='CH_20', opts={'brand': 'vw'}, reg=[(VW, ['TIGUAN', 'TIGUAN ALLSPACE', 'TIGUAN ALL-SPAC'])], codes=['CZP', 'DKZ', 'DNN'], notes_pre=GEN_NOTE)
    S(id='vw-passat-2006-2015-1.8-2.0', make='Volkswagen', make_he='פולקסווגן', model='Passat', model_he='פאסאט',
      generation='B6, B7', engines=['1.8 TSI (CDA)', '1.8 TFSI (BZB)', '2.0 FSI (BVY/BLR)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'cond', 'belt_engines': '2.0 FSI BVY/BLR לפי מדריך גולף 5; CDA עם שרשרת', 'plugs90': ['1.8 TSI (CDA)'], 'srcs': ('PASSAT7', 'TIG1', 'GOLF5')},
      reg=[(VW, ['PASSAT', 'PASSAT CC'])], codes=['CDA', 'BZB', 'BVY', 'BLR'], reg_years=[2005, 2015],
      notes_pre=GEN_NOTE + "מבוסס בעיקר על מדריך השירות של פאסאט B7 (מהדורה 01.2019). ")
    S(id='vw-passat-2015-2019-1.4-1.8-tsi', make='Volkswagen', make_he='פולקסווגן', model='Passat', model_he='פאסאט',
      generation='B8', engines=['1.4 TSI (CZD)', '1.8 TSI (CJS)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'cond', 'belt_engines': 'CZD (EA211); CJS עם שרשרת', 'srcs': ('GOLF7', 'TIG1')},
      reg=[(VW, ['PASSAT'])], codes=['CZD', 'CJS'], notes_pre=GEN_NOTE)
    S(id='vw-t-cross-2020-2026-1.0-tsi', make='Volkswagen', make_he='פולקסווגן', model='T-Cross', model_he='טי-קרוס',
      generation='C1', engines=['1.0 TSI (DKR/DLA/DUS)'],
      template='CH_SMALL', opts={'has15': False}, reg=[(VW, ['T-CROSS', 'T-CROSS LIFE'])], codes=TSI10, notes_pre=GEN_NOTE)
    S(id='vw-t-roc-2024-2026-1.5-tsi', make='Volkswagen', make_he='פולקסווגן', model='T-Roc', model_he='טי-רוק',
      generation='A1 פייסליפט', engines=['1.5 TSI evo2 (DXD)'],
      template='CH_SMALL', opts={'has10': False}, reg=[(VW, ['T-ROC', 'T-ROC STYLE'])], codes=TSI15, notes_pre=GEN_NOTE)
    S(id='vw-id4-id5-2022-2026-ev', make='Volkswagen', make_he='פולקסווגן', model='ID.4 / ID.5', model_he='ID.4 / ID.5',
      generation='E21', engines=['חשמלי (EBJ/EDF)'], fuel='electric',
      template='CH_BEV', reg=[(VW, ['ID4', 'ID.5'])], codes=['EBJ', 'EDF'], notes_pre=GEN_NOTE)

    # ------------------------------------------------------------------ AUDI
    S(id='audi-a1-2015-2026-1.0-1.5-tfsi', make='Audi', make_he='אאודי', model='A1', model_he='A1',
      generation='8X פייסליפט (1.0), GB', engines=['1.0 TFSI (CHZ/DKR/DLA/DUS)', '1.5 TFSI (DAD/DPC)'],
      template='CH_SMALL', reg=[(AU, ['A1', 'A1 SPORTBACK'])], codes=CH_ALL, notes_pre=GEN_NOTE)
    S(id='audi-a1-2010-2017-1.4-tfsi', make='Audi', make_he='אאודי', model='A1', model_he='A1',
      generation='8X', engines=['1.4 TFSI (CAX/CZC)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'cond', 'belt_engines': 'CZC (EA211); CAX עם שרשרת', 'awd': False, 'srcs': ('GOLF7', 'PASSAT7')},
      reg=[(AU, ['A1', 'A1 SPORTBACK'])], codes=['CAX', 'CZC'],
      notes_pre=GEN_NOTE + "מדריכי השירות של אאודי שנמצאו (Q3 2012) אינם כוללים טבלת מרווחים; הערכים לפי טבלאות פולקסווגן לאותם מנועים. ")
    S(id='audi-q2-2017-2026-1.0-1.5-tfsi', make='Audi', make_he='אאודי', model='Q2', model_he='Q2',
      generation='GA ופייסליפט', engines=['1.0 TFSI (CHZ/DKR)', '1.5 TFSI (DAD/DPC/DXD)'],
      template='CH_SMALL', reg=[(AU, ['Q2'])], codes=CH_ALL, notes_pre=GEN_NOTE)
    S(id='audi-q2-2017-2018-1.4-tfsi', make='Audi', make_he='אאודי', model='Q2', model_he='Q2',
      generation='GA', engines=['1.4 TFSI (CZE)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'yes', 'srcs': ('GOLF7',)},
      reg=[(AU, ['Q2', 'Q2 DESIGN'])], codes=['CZE'], notes_pre=GEN_NOTE + "הערכים לפי טבלאות פולקסווגן לאותו מנוע (אין טבלת מרווחים במדריכי אאודי שנמצאו). ")
    S(id='audi-q3-2012-2019-1.4-tfsi', make='Audi', make_he='אאודי', model='Q3', model_he='Q3',
      generation='8U', engines=['1.4 TFSI (CZD/CHP)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'yes', 'srcs': ('GOLF7', 'TIG1')},
      reg=[(AU, ['Q3'])], codes=['CZD', 'CHP'], notes_pre=GEN_NOTE + "הערכים לפי טבלאות פולקסווגן לאותם מנועים (במדריך השירות של Q3 2012 אין טבלת מרווחים). ")
    S(id='audi-q3-2012-2018-2.0-tfsi', make='Audi', make_he='אאודי', model='Q3', model_he='Q3',
      generation='8U', engines=['2.0 TFSI (CCZ/CPS/CUL)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'no', 'plugs90': ['2.0 TFSI דור 2 (CCZ/CPS)'], 'srcs': ('TIG1', 'GOLF7')},
      reg=[(AU, ['Q3'])], codes=['CCZ', 'CPS', 'CUL'], reg_years=[2011, 2018],
      notes_pre=GEN_NOTE + "מנועי EA888 עם שרשרת; הערכים לפי טבלאות פולקסווגן (טיגואן 2008 עם CCZ). ")
    S(id='audi-q3-2019-2026-1.5-tfsi', make='Audi', make_he='אאודי', model='Q3', model_he='Q3',
      generation='F3, Sportback', engines=['1.5 TFSI (DAD/DFY/DXD)'],
      template='CH_SMALL', opts={'has10': False}, reg=[(AU, ['Q3', 'Q3 SPORTBACK', 'Q3 SB 35', 'Q3 35 TFSI'])], codes=TSI15, notes_pre=GEN_NOTE)
    S(id='audi-q3-2019-2026-2.0-tfsi', make='Audi', make_he='אאודי', model='Q3', model_he='Q3',
      generation='F3, Sportback', engines=['2.0 TFSI (DKT/DNN/DNP)'],
      template='CH_20', opts={'brand': 'audi'}, reg=[(AU, ['Q3', 'Q3 SPORTBACK', 'Q3 SB 40', 'Q3 SB 45', 'Q3 40 TFSI', 'Q3 SB S LINE 40'])], codes=['DKT', 'DNN', 'DNP'], reg_years=[2019, 2026], notes_pre=GEN_NOTE)
    S(id='audi-a3-2013-2020-1.4-tfsi', make='Audi', make_he='אאודי', model='A3', model_he='A3',
      generation='8V', engines=['1.4 TFSI (CZC/CXS/CZE/CMB)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'yes', 'srcs': ('GOLF7',)},
      reg=[(AU, ['A3', 'A3 SPORTBACK'])], codes=['CZC', 'CXS', 'CZE', 'CMB', 'CZD'], notes_pre=GEN_NOTE + "הערכים לפי טבלאות פולקסווגן לאותם מנועים (גולף 7, אותה פלטפורמה MQB). ")
    S(id='audi-a3-2013-2016-1.8-tfsi', make='Audi', make_he='אאודי', model='A3', model_he='A3',
      generation='8V', engines=['1.8 TFSI (CJS)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'no', 'srcs': ('GOLF7',)},
      reg=[(AU, ['A3', 'A3 SPORTBACK'])], codes=['CJS'], notes_pre=GEN_NOTE + "מנוע EA888 דור 3 עם שרשרת; הערכים לפי טבלאות פולקסווגן (גולף 7). ")
    S(id='audi-a3-2017-2026-1.5-tfsi', make='Audi', make_he='אאודי', model='A3', model_he='A3',
      generation='8V פייסליפט, 8Y', engines=['1.5 TFSI (DAD/DPC/DXD)', '1.5 eTFSI (DFY)'],
      template='CH_SMALL', opts={'has10': False}, reg=[(AU, ['A3', 'A3 SPORTBACK', 'A3 SEDAN', 'A3 DESIGN'])], codes=TSI15, notes_pre=GEN_NOTE)
    S(id='audi-a3-2018-2019-1.4-phev', make='Audi', make_he='אאודי', model='A3 Sportback e-tron', model_he='A3 ספורטבק e-tron',
      generation='8V', engines=['1.4 TFSI PHEV (CUK)'], fuel='plug-in-hybrid',
      template='CH_PHEV', reg=[(AU, ['A3 SB E-TRON'])], codes=['CUK'], notes_pre=GEN_NOTE)
    S(id='audi-q4-2022-2025-ev', make='Audi', make_he='אאודי', model='Q4 e-tron', model_he='Q4 e-tron',
      generation='F4', engines=['חשמלי (EBJ/EDF)'], fuel='electric',
      template='CH_BEV', reg=[(AU, ['Q4 E-TRON', 'Q4 SPORTBACK', 'Q4 SB E-TRON'])], codes=['EBJ', 'EDF'], notes_pre=GEN_NOTE)
    S(id='audi-e-tron-2019-2022-ev', make='Audi', make_he='אאודי', model='e-tron', model_he='e-tron',
      generation='GE', engines=['חשמלי (EAS)'], fuel='electric',
      template='CH_BEV', opts={'etron': True}, reg=[(AU, ['ETRON', 'ETRON SPORTBACK'])], codes=['EAS'], notes_pre=GEN_NOTE)
    S(id='audi-q5-2009-2017-2.0-tfsi', make='Audi', make_he='אאודי', model='Q5', model_he='Q5',
      generation='8R', engines=['2.0 TFSI (CDN/CNC)'],
      template='CH_20', opts={'brand': 'audi', 'status': 'draft'}, reg=[(AU, ['Q5'])], codes=['CDN', 'CNC'],
      notes_pre=GEN_NOTE + "טיוטה: טבלת ה-2.0 של צ'מפיון מוגדרת לדגמים מהשנים האחרונות, והתאמתה ל-Q5 מדור 8R לא אומתה; מדריך השירות של Q5 2008 אינו כולל טבלת מרווחים. ")

def load_specs_commercial(S, ns):
    VW = ns['VW']
    GEN_NOTE = ("קבוצת פולקסווגן משתמשת באותן טבלאות שירות לכל הדגמים על אותה פלטפורמה ומשפחת מנוע, ולכן הקובץ נבנה מתבנית משותפת "
                "ומשויך לרכב לפי קוד המנוע ברישיון. ")
    S(id='vw-transporter-t61-2021-2025-2.0-tdi', make='Volkswagen', make_he='פולקסווגן', model='Transporter / Caravelle T6.1', model_he='טרנספורטר / קרוואל T6.1',
      generation='T6.1', engines=['2.0 TDI (DNA)'], fuel='diesel',
      template='CH_T61', reg=[(VW, ['CARAVELLE', 'TRANSPORTER', 'T6 TRANSPORTER'])], codes=['DNA'], notes_pre=GEN_NOTE)
    S(id='vw-caddy-2022-2026-2.0-tdi', make='Volkswagen', make_he='פולקסווגן', model='Caddy', model_he='קאדי',
      generation='5 (SB)', engines=['2.0 TDI (DTR/DXR)'], fuel='diesel',
      template='CH_CADDY5', reg=[(VW, ['CADDY', 'CADDY MAXI', 'CADDY KOMBI', 'CADDY LIFE2.0TD'])], codes=['DTR', 'DXR'], notes_pre=GEN_NOTE)
    S(id='vw-transporter-2010-2015-2.0-tdi', make='Volkswagen', make_he='פולקסווגן', model='Transporter / Caravelle T5', model_he='טרנספורטר / קרוואל T5',
      generation='T5 פייסליפט (7E)', engines=['2.0 TDI (CAA/CCH/CFC)'], fuel='diesel',
      template='T5_2010', reg=[(VW, ['T5', 'NEW TRANSPORTER', 'TRANSPORTER', 'CARAVELLE', 'T5 PICK UP', 'TRANSPORTER D.V'])], codes=['CAA', 'CCH', 'CFC'], notes_pre=GEN_NOTE)
    S(id='vw-transporter-t6-2016-2021-2.0-tdi', make='Volkswagen', make_he='פולקסווגן', model='Transporter / Caravelle T6', model_he='טרנספורטר / קרוואל T6',
      generation='T6 (SG)', engines=['2.0 TDI (CXE/CXF/CXG/CXH)'], fuel='diesel',
      template='T6', reg=[(VW, ['T6', 'T6 TRANSPORTER', 'TRANSPORTER', 'CARAVELLE', 'TRANSPORTER T6'])], codes=['CXE', 'CXF', 'CXG', 'CXH'], notes_pre=GEN_NOTE)
    S(id='vw-transporter-2004-2010-1.9-2.5-tdi', make='Volkswagen', make_he='פולקסווגן', model='Transporter T5', model_he='טרנספורטר T5',
      generation='T5 (7H)', engines=['1.9 TDI (AXB/BRR/BRS)', '2.5 TDI (AXD/BNZ/BPC)'], fuel='diesel',
      template='T5_OLD', reg=[(VW, ['TRANSPORTER', 'CARAVEL', 'CARAVELLE'])], codes=['AXB', 'BRR', 'BRS', 'AXD', 'BNZ', 'BPC'], notes_pre=GEN_NOTE)
    S(id='vw-caddy-2008-2015-1.6-1.9-tdi-1.2-tsi', make='Volkswagen', make_he='פולקסווגן', model='Caddy', model_he='קאדי',
      generation='3 (2K/2C)', engines=['1.9 TDI (BLS)', '1.6 TDI (CAY)', '1.2 TSI (CBZ)'], fuel='petrol-or-diesel',
      template='CADDY3', reg=[(VW, ['CADDY', 'CADDY GP', 'CADDY GT', 'CADDY KOMBI', 'CADDY MAXI'])], codes=['BLS', 'CAY', 'CBZ'], notes_pre=GEN_NOTE)
    S(id='vw-caddy-2016-2021-2.0-tdi-1.4-tsi', make='Volkswagen', make_he='פולקסווגן', model='Caddy', model_he='קאדי',
      generation='4 (SA)', engines=['2.0 TDI (DFS)', '1.4 TSI (CZC/DJK)'], fuel='petrol-or-diesel',
      template='CADDY4', reg=[(VW, ['CADDY', 'CADDY COMBI', 'CADDY KOMBI', 'CADDY KOMBI MAX', 'CADDY MAXI', 'CADDY MAXI KOMB', 'CADDYMAXI KOMBI', 'CADDY MAXI D.V'])], codes=['DFS', 'CZC', 'DJK'], notes_pre=GEN_NOTE)

def load_specs_extra(S, ns):
    SK, SE, VW, AU, CU = ns['SK'], ns['SE'], ns['VW'], ns['AU'], ns['CU']
    TSI10, TSI15 = ns['TSI10'], ns['TSI15']
    GEN_NOTE = ("קבוצת פולקסווגן משתמשת באותן טבלאות שירות לכל הדגמים על אותה פלטפורמה ומשפחת מנוע, ולכן הקובץ נבנה מתבנית משותפת "
                "ומשויך לרכב לפי קוד המנוע ברישיון. ")
    S(id='skoda-karoq-2018-2019-2.0-tdi', make='Skoda', make_he='סקודה', model='Karoq', model_he='קארוק',
      generation='NU', engines=['2.0 TDI (DFF)'], fuel='diesel',
      template='CH_D20', reg=[(SK, ['KAROQ'])], codes=['DFF'], notes_pre=GEN_NOTE)
    S(id='skoda-karoq-2018-2021-1.6-tdi', make='Skoda', make_he='סקודה', model='Karoq / Scala', model_he='קארוק / סקאלה',
      generation='NU / NW', engines=['1.6 TDI (DGT)'], fuel='diesel',
      template='FAC_D', opts={'brand': 'skoda', 'fuel_km': 90000}, reg=[(SK, ['KAROQ', 'SCALA'])], codes=['DGT'],
      notes_pre=GEN_NOTE + "נפח המנוע לפי ספר התיקון של מנועי DGTA/DGTD (1.6 TDI). ")
    S(id='skoda-octavia-2011-2017-1.6-tdi', make='Skoda', make_he='סקודה', model='Octavia / Rapid', model_he='אוקטביה / ראפיד',
      generation='Octavia II/III, Rapid NH', engines=['1.6 TDI (CAY/CLH/CXX)'], fuel='diesel',
      template='FAC_D', opts={'brand': 'skoda', 'old_skoda': True, 'fuel_km': 90000,
                              'note_extra': 'במדריך ראפיד (פלטפורמה קטנה יותר) מסנן הסולר כל 60,000.'},
      reg=[(SK, ['OCTAVIA', 'RAPID'])], codes=['CAY', 'CLH', 'CXX'], notes_pre=GEN_NOTE)
    S(id='vw-jetta-2010-2015-1.6-tdi', make='Volkswagen', make_he='פולקסווגן', model='Jetta', model_he="ג'טה",
      generation='6 (1B)', engines=['1.6 TDI (CAY)'], fuel='diesel',
      template='FAC_D', opts={'brand': 'vw', 'fuel_km': 90000}, reg=[(VW, ['JETTA'])], codes=['CAY'], notes_pre=GEN_NOTE)
    S(id='vw-taigo-2024-2026-1.0-tsi', make='Volkswagen', make_he='פולקסווגן', model='Taigo', model_he='טייגו',
      generation='CS', engines=['1.0 TSI evo2 (DUS)'],
      template='CH_SMALL', opts={'has15': False}, reg=[(VW, ['TAIGO'])], codes=TSI10, notes_pre=GEN_NOTE)
    S(id='vw-beetle-2012-2018-1.2-tsi', make='Volkswagen', make_he='פולקסווגן', model='Beetle', model_he='ביטל',
      generation='5C', engines=['1.2 TSI (CBZ/CYV)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'cond', 'belt_engines': 'CYV (EA211); CBZ עם שרשרת', 'awd': False, 'srcs': ('GOLF7', 'TIG1')},
      reg=[(VW, ['BEETLE'])], codes=['CBZ', 'CYV'], notes_pre=GEN_NOTE)
    S(id='vw-scirocco-2009-2014-1.4-2.0-tsi', make='Volkswagen', make_he='פולקסווגן', model='Scirocco', model_he='שירוקו',
      generation='3 (13)', engines=['1.4 TSI (CAV/CAX/CTH)', '2.0 TSI (CCZ)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'no', 'plugs90': ['2.0 TSI (CCZ)'], 'awd': False, 'srcs': ('TIG1', 'PASSAT7')},
      reg=[(VW, ['SCIROCCO'])], codes=['CAV', 'CAX', 'CTH', 'CCZ'], notes_pre=GEN_NOTE + "מנועי EA111 ו-EA888 עם שרשרת תזמון. ")
    S(id='vw-up-2014-2015-1.0', make='Volkswagen', make_he='פולקסווגן', model='up!', model_he='אפ',
      generation='AA', engines=['1.0 MPI (CHY)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'cond', 'belt_engines': 'משפחת EA211', 'awd': False, 'srcs': ('GOLF7', 'TIG1')},
      reg=[(VW, ['UP'])], codes=['CHY'],
      notes_pre=GEN_NOTE + "טבלת גולף 7 כוללת הערה נפרדת ל-up!: מסנן אוויר כל 60,000 או 4 שנים בתנאים רגילים וכל 30,000 או שנתיים במדינות מאובקות; מסנן מזגן כל 30,000 או שנתיים (במדינות מאובקות שנה או 30,000). ")
    S(id='cupra-formentor-2021-2026-2.0-tsi', make='Cupra', make_he='קופרה', model='Formentor', model_he='פורמנטור',
      generation='KM', engines=['2.0 TSI (DNF/DNN)'],
      template='CH_20', opts={'brand': 'cupra'}, reg=[(CU, ['FORMENTOR 4X4', 'FORMENTOR VZ', 'CUPRA', 'FORMENTOR', 'CUPRA LEON VZ', 'CUPRA ATECA'])], codes=['DNF', 'DNN', 'DNU'],
      notes_pre=GEN_NOTE + "היצרן 'קופרה' אינו ברשימת היצרנים של lookup_plate, ולכן כלל השיוך משתמש בשם העברי. ")
    S(id='audi-a4-a5-2016-2021-2.0-tfsi', make='Audi', make_he='אאודי', model='A4 / A5', model_he='A4 / A5',
      generation='B9 (8W) / F5', engines=['2.0 TFSI (CVK/DLV/DEM/DDW)'],
      template='CH_20', opts={'brand': 'audi'}, reg=[(AU, ['A4', 'A5', 'A5 SPORTBACK'])], codes=['CVK', 'DLV', 'DEM', 'DDW'],
      notes_pre=GEN_NOTE + "קודי המנוע לפי ספרי התיקון של מנועי 2.0 TFSI (EA888 דור 3 ו-B-cycle). ")
    S(id='audi-a4-2016-2019-1.4-tfsi', make='Audi', make_he='אאודי', model='A4', model_he='A4',
      generation='B9 (8W)', engines=['1.4 TFSI (CVN)'],
      template='FAC', opts={'brand': 'vw', 'belt': 'yes', 'awd': False, 'srcs': ('GOLF7',)},
      reg=[(AU, ['A4', 'A5 SPORTBACK'])], codes=['CVN'],
      notes_pre=GEN_NOTE + "מנוע 1.4 TFSI ממשפחת EA211 (ספר התיקון של CVNA). במדריך השירות של A4 2015 אין טבלת מרווחים; הערכים לפי טבלאות פולקסווגן לאותה משפחת מנוע. ")
    S(id='audi-q7-q8-2015-2026-3.0-tdi', make='Audi', make_he='אאודי', model='Q7 / Q8', model_he='Q7 / Q8',
      generation='4M', engines=['3.0 TDI V6 (CRT/DHX/DPX)'], fuel='diesel',
      template='CH_D30', reg=[(AU, ['Q7', 'Q8'])], codes=['CRT', 'DHX', 'DPX'], notes_pre=GEN_NOTE)
