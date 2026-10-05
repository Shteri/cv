# Add Israeli importer corroboration to existing PSA drafts (numbers unchanged, status stays draft).
import json, sys
sys.path.insert(0, '.')
from common import write
S = '/home/user/cv/data/schedules/'
CWB = 'https://web.archive.org/web/20120509205507/http://citroen.co.il/_Uploads/dbsAttachedFiles/CitroenWarrantyBook.pdf'
FAQ = 'https://online.peugeot.co.il/faq/'
def load(i): return json.load(open(S + i + '.json'))
for i in ['citroen-c4-picasso-c5-aircross-2011-2023-1.6-thp', 'peugeot-3008-5008-508-2010-2023-1.6-thp']:
    d = load(i)
    d['sources'].append({'url': CWB, 'kind': 'importer', 'note': 'חוברת השירות והאחריות העברית של סיטרואן (לובינסקי, 08/2009), עמ\' 11 ו-18: למנועי בנזין "אחרים" (כולל 1.6 THP) בתנאים קשים 20,000 ק"מ או שנה, מסנן אוויר ומצתים כל 40,000 ק"מ, מסנן תא נוסעים כל 20,000 ק"מ או שנה, נוזל בלמים כל שנתיים, בדיקת נוזל קירור מ-120,000 ק"מ'})
    d['notes'] += ' אימות מול מקור ישראלי: חוברת השירות העברית של לובינסקי לסיטרואן (2009) נותנת לקטגוריית מנועי הבנזין "האחרים" בתנאים קשים בדיוק את אותם מרווחים (20,000 ק"מ או שנה; מסנן אוויר ומצתים כל 40,000 ק"מ). החוברת קודמת לדגמי 2017 ואילך, ולכן הקובץ נשאר טיוטה.'
    print(write(d))
for i in ['peugeot-2008-2014-2026-1.2-puretech', 'peugeot-2008-2020-2026-1.5-bluehdi']:
    d = load(i)
    d['sources'].append({'url': FAQ, 'kind': 'importer', 'note': 'עמוד השאלות והתשובות של פיג\'ו ישראל (לובינסקי) ל-2008 SUV: תדירות הטיפולים כל 15,000 ק"מ או שנה, המוקדם מביניהם (נבדק 10.2026)'})
    d['notes'] += ' היבואן מאשר בעמוד השאלות והתשובות של ה-2008 מרווח של 15,000 ק"מ או שנה; פירוט הפריטים עדיין לפי מקור בינלאומי.'
    print(write(d))
