import sys, json, copy; sys.path.insert(0, '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/dl/japan-b')
from gen import *
REPO = '/home/user/cv/data/schedules/'
STG = OUT + '/'
LEX_PAGE = 'https://www.lexus.co.il/owners/maintenance/owner-books'
def sister(src_path, id_, model, gen, years, engines, fuel, book_conn, book_note, sis_he, names, ryears):
    s = json.load(open(src_path))
    d = copy.deepcopy(s)
    d.update(id=id_, make='Lexus', make_he='לקסוס', model=model, model_he=model, generation=gen, years=list(years), engines=engines,
             fuel=fuel, importer='יוניון מוטורס', status='draft')
    d['sources'] = [dict(url=f'https://books.union-motors.co.il/LexusApp/api/files/{book_conn}/download', kind='importer',
                         note=f'ספר הרכב העברי של לקסוס ({book_note}) מפנה לחוברת השירות ואין בו לוח אחזקה')] + \
                   [dict(url=x['url'], kind=x['kind'], note='דגם אחות: ' + x['note']) for x in s['sources']]
    d['notes'] = (f'טיוטה: ספר הרכב העברי של לקסוס {model} לא כולל לוח אחזקה (מפנה ל"חוברת השירות של לקסוס", שלא נמצאה ברשת). '
                  f'הלוח כאן הועתק מלוח האחזקה הישראלי של {sis_he}, שחולק עם הדגם את המנוע ואת הפלטפורמה. '
                  'כדאי לאמת מול מרכז השירות של לקסוס. ' + 'הערת המקור: ' + s.get('notes', ''))
    json.dump(d, open(STG + id_ + '.json', 'w'), ensure_ascii=False, indent=2)
    rule('Lexus', names, ryears, id_)
sister(REPO + 'toyota-rav4-2020-2025-2.5-hybrid.json', 'lexus-nx350h-2022-2026-2.5-hybrid', 'NX 350h', 'AZ20', (2022, 2026),
       ['2.5 hybrid (A25A-FXS)'], 'hybrid', 123, 'NX350h 2022, 558 עמודים; עמוד 391', 'טויוטה RAV4 היברידי 2020-2025 (A25A-FXS, TNGA-K)', ['LEXUS NX350H', 'NX350H'], (2021, 2026))
sister(REPO + 'toyota-camry-2020-2025-2.5-hybrid.json', 'lexus-es300h-2019-2025-2.5-hybrid', 'ES 300h', 'XZ10', (2019, 2025),
       ['2.5 hybrid (A25A-FXS)'], 'hybrid', 42, 'ES300h 2019-2025; פרק 6-3 מפנה לחוברת השירות', 'טויוטה קאמרי היברידית 2020-2025 (A25A-FXS, TNGA-K)', ['LEXUS ES300H', 'ES300H'], (2018, 2025))
sister(REPO + 'toyota-yaris-cross-2021-2025-1.5-hybrid.json', 'lexus-lbx-2024-2026-1.5-hybrid', 'LBX', 'MAYH10', (2024, 2026),
       ['1.5 hybrid (M15A-FXE)'], 'hybrid', 36, 'LBX 2024, 524 עמודים; עמוד 378', 'טויוטה יאריס קרוס היברידית 2021-2025 (M15A-FXE, GA-B)', ['LEXUS LBX', 'LBX'], (2023, 2026))
sister(STG + 'toyota-rav4-plug-in-2021-2023-2.5-phev.json', 'lexus-nx450h-plus-2022-2026-2.5-phev', 'NX 450h+', 'AZ20', (2022, 2026),
       ['2.5 plug-in hybrid (A25A-FXS)'], 'plug-in-hybrid', 124, 'NX450h+ 2022, 595 עמודים', 'טויוטה RAV4 פלאג-אין 2021 (A25A-FXS, אותה מערכת הנעה)', ['LEXUS NX450PHEV', 'NX450PHEV', 'NX450H+'], (2021, 2026))
save_rules('rules_lexus2.json')
