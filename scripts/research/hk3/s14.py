import json
from build import OUT
def clone(src, upd):
    d=json.load(open(OUT+src+'.json')); d.update(upd)
    json.dump(d,open(OUT+d['id']+'.json','w'),ensure_ascii=False,indent=2); print('wrote',d['id'])
KIA={'make':'Kia','make_he':'קיה','importer':'טלקאר'}
clone('hyundai-santa-fe-2012-2018-2.4',{**KIA,'id':'kia-sorento-2012-2014-2.4','model':'Sorento','model_he':'סורנטו','generation':'XM facelift','years':[2012,2014],
 'engines':['2.4 GDI (Theta II, G4KJ)'],'status':'draft',
 'notes':'לא נמצא ספר ישראלי או ספר בינלאומי עם טבלה שאינה אמריקאית לסורנטו XM (הספרים שנמצאו הם לצפון אמריקה, במיילים). הקובץ מבוסס על ספר היבואן העברי של יונדאי סנטה פה DM (2013-2018), דגם אחות מאותה קבוצה עם אותו מנוע 2.4 GDI (G4KJ) ובאותן שנים. זה מקור חלופי; יש לאמת מול טלקאר. הספר נותן רשימות לכל 30,000 ק"מ; הקובץ בנוי על רשת 15,000 עם שמן ומסנן בכל טיפול. מסנן אוויר כל 60,000, נוזל בלמים ומסנן מזגן כל 30,000.'})
clone('hyundai-santa-fe-2013-2018-2.2-diesel',{**KIA,'id':'kia-sorento-2010-2014-2.2-diesel','model':'Sorento','model_he':'סורנטו','generation':'XM','years':[2010,2014],
 'engines':['2.2 CRDi (R, D4HB)'],'status':'draft',
 'notes':'לא נמצא ספר ישראלי או ספר בינלאומי לא-אמריקאי לסורנטו XM. הקובץ מבוסס על ספר היבואן העברי של יונדאי סנטה פה DM, שורות הדיזל של אותו מנוע R 2.2 (D4HB), דגם אחות מאותה קבוצה. זה מקור חלופי; יש לאמת מול טלקאר. רשימות לכל 30,000 ק"מ, ברשת 15,000 עם שמן ומסנן בכל טיפול. מחסנית מסנן הסולר מוחלפת כל 60,000.'})
