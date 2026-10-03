import json, sys
sys.path.insert(0,'.')
from gen import rule, save_rules, OUT
from gen_sister import sister
SCH='/home/user/cv/data/schedules/'
# Qashqai J10 HR16DE: same ESM, HR16 tables (MA-7/MA-8) match the MR20 rows except no CVT/4WD rows
d=json.load(open(SCH+'nissan-qashqai-2007-2014-2.0.json'))
d['id']='nissan-qashqai-2007-2014-1.6'; d['engines']=['1.6 (HR16DE)']
drop={'cvt_oil','differential_oil'}
for s in d['services']: s['items']=[i for i in s['items'] if i['item'] not in drop]
d['long_interval']=[x for x in d['long_interval'] if x['item'] not in ('transfer_case_oil','propshaft')]
d['interval']['note']=d['interval']['note'].replace('MR20DE','HR16DE')
d['sources'][0]['note']='Nissan Qashqai J10 ESM (אירופה), פרק MA: טבלאות "Engine and emission control maintenance (HR16DE petrol engine)" ו-"Chassis and body maintenance (HR16DE)" לנסועה שנתית מתחת ל-30,000 ק"מ, MA-7 עד MA-8 (עמודי PDF 6173-6174)'
d['notes']='טיוטה מספר השירות האירופי של ניסאן לקשקאי J10, טבלאות מנוע 1.6 HR16DE (תיבה ידנית, הנעה קדמית). הלוח זהה בתוכנו ללוח מנוע 2.0 באותו ספר: טיפול כל 30,000 ק"מ או 24 חודשים; שמן ומסנן, מסנן מזגן ונוזל בלמים בכל טיפול; מסנן אוויר ב-60,000 וב-120,000; מצתים ב-90,000; נוזל קירור לראשונה ב-90,000 ואחר כך כל 60,000. בתנאים מחמירים (חום, אבק, נסיעות קצרות) שמן ומסנן, מסנן מזגן ונוזל בלמים כל 15,000 ק"מ או 12 חודשים - ובישראל מומלץ לשקול זאת.'
json.dump(d,open(f'{OUT}/{d["id"]}.json','w'),ensure_ascii=False,indent=2)
rule('Nissan',['QASHQAI'],(2007,2014),'nissan-qashqai-2007-2014-1.6',engine_codes=['HR16','HR16DE'])

sister('nissan-tiida-2007-2011-1.6','nissan-note-2006-2013-1.6','E11',(2006,2014),['1.6 (HR16DE)'],
  'טיוטה (דגם אחות): לא נמצא לוח לנוט E11. הלוח הועתק מלוח הטיידה C11 מספר השירות האירופי של ניסאן; שני הדגמים בנויים על אותה פלטפורמה (B) עם אותו מנוע 1.6 HR16DE.')
rule('Nissan',['NOTE'],(2006,2014),'nissan-note-2006-2013-1.6',engine_codes=['HR16','HR16DE'])

sister('nissan-qashqai-2019-2026-1.3-turbo','nissan-x-trail-2019-2022-1.3-turbo','T32',(2019,2022),['1.3 DIG-T (HR13DDT)'],
  'טיוטה (דגם אחות): לא נמצא לוח לאקס-טרייל T32 עם מנוע 1.3 טורבו. הלוח הועתק מלוח הקשקאי 1.3 (מנוע HR13DDT, אותה פלטפורמה CMF-C/D ותיבת DCT/CVT דומה); בדגמי 4X4 יש לבדוק גם שמן דיפרנציאל ותיבת העברה מול המוסך.')
rule('Nissan',['X-TRAIL','X TRAIL','XTRAIL'],(2019,2022),'nissan-x-trail-2019-2022-1.3-turbo',engine_codes=['HR13','HR13DDT'])
save_rules('rules_nissan.json')
