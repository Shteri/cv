import json, sys
sys.path.insert(0,'.')
from gen import rule, save_rules, OUT
SCH='/home/user/cv/data/schedules/'
def sister(src, new_id, generation, years, engines, prefix, specs_note=None, keep_specs=('engine_oil','coolant','brake_fluid','fuel','tire_pressure')):
    d=json.load(open(SCH+src+'.json'))
    d['id']=new_id; d['generation']=generation; d['years']=list(years); d['engines']=engines
    d['status']='draft'
    d['notes']=prefix+' '+d['notes']
    sp=d.get('specs',{}); d['specs']={k:v for k,v in sp.items() if k in keep_specs}
    if d['specs']: d['specs']['_note']=specs_note or 'נתונים מהדור הבא עם אותו מנוע; לאמת מול ספר הרכב'
    d['sources']=d['sources']+[{'url':'https://github.com/','kind':'other','note':'placeholder'}][:0]
    for s in d['sources']: s['note']='(לוח של הדור הבא, שימש כאחות) '+s['note']
    json.dump(d,open(f'{OUT}/{new_id}.json','w'),ensure_ascii=False,indent=2)
    return d

if __name__=='__main__':
    sister('toyota-yaris-2006-2011-1.0-1.3','toyota-yaris-2003-2005-1.3','XP10',(2003,2005),['1.3 VVT-i (2SZ-FE)'],
      'טיוטה (דגם אחות): לא נמצא לוח ישראלי או לוח יצרן לדור XP10. הלוח הועתק מגיליון יוניון מוטורס ליאריס XP90, שבה אותו מנוע 2SZ-FE, ולכן ההתאמה לדור הקודם היא הערכה שיש לאמת מול המוסך.')
    rule('Toyota',['YARIS'],(2003,2005),'toyota-yaris-2003-2005-1.3',engine_codes=['2SZ','2SZ-FE'])

    sister('mitsubishi-pajero-2007-2020-3.2-diesel','mitsubishi-pajero-2000-2006-3.2-diesel','NM/NP',(2000,2006),['3.2 DI-D (4M41)'],
      'טיוטה לדור NM/NP (2000-2006): לא נמצא לוח לדור זה; הלוח זהה לזה של הדור הבא (אותו מנוע 4M41), מטבלת מיצובישי אוסטרליה.')
    rule('Mitsubishi',['PAJERO'],(2000,2006),'mitsubishi-pajero-2000-2006-3.2-diesel',engine_codes=['4M41'])

    sister('toyota-rav4-2013-2019-2.0','toyota-rav4-2009-2012-2.0','XA30',(2009,2012),['2.0 Valvematic (3ZR-FAE)'],
      'טיוטה (דור קודם): לא נמצא לוח ישראלי לדור XA30. הלוח הועתק מגיליון יוניון מוטורס ל-RAV4 4X4 דור XA40, שבו אותו מנוע 2.0 (3ZR-FAE), ויש לאמת מול המוסך.')
    rule('Toyota',['RAV-4','RAV 4','RAV4'],(2009,2012),'toyota-rav4-2009-2012-2.0',engine_codes=['3ZR','3ZR-FAE'])

    # rule-only extensions to existing schedules
    rule('Mitsubishi',['OUTLANDER'],(2021,2021),'mitsubishi-outlander-2013-2020-2.0-2.4',engine_codes=['4J11','4J12'])
    rule('Toyota',['HILUX'],(2002,2004),'toyota-hilux-2005-2015-2.5-3.0-diesel',engine_codes=['2KD','2KD-FTV'])
    rule('Suzuki',['VITARA'],(2021,2021),'suzuki-vitara-2016-2020-1.0-1.4-turbo',engine_codes=['K14C','K10C'])
    rule('Subaru',['FORESTER'],(2011,2012),'subaru-forester-2013-2018-2.0-2.5',engine_codes=['FB 20','FB20','FB 25','FB25'])
    rule('Suzuki',['SWIFT'],(2021,2021),'suzuki-swift-2017-2020-1.2',engine_codes=['K12C'])
    rule('Suzuki',['IGNIS'],(2021,2021),'suzuki-ignis-2017-2020-1.2',engine_codes=['K12C'])
    rule('Suzuki',['SWIFT'],(2011,2011),'suzuki-swift-2005-2010-1.5',engine_codes=['M15A'])
    rule('Suzuki',['S CROSS'],(2022,2026),'suzuki-s-cross-2022-2026-1.4-mild-hybrid')
    sister('mitsubishi-outlander-2013-2020-2.0-2.4','mitsubishi-outlander-2007-2012-2.0-2.4','CW (דור 2)',(2007,2012),['2.0 MIVEC (4B11)','2.4 MIVEC (4B12)'],
      'טיוטה (דור קודם): לא נמצא לוח לאאוטלנדר CW. הלוח הועתק מלוח הדור הבא (ZJ-ZL, מיצובישי אוסטרליה), שבנוי על אותה פלטפורמה עם תיבת CVT והנעה 4X4 דומות; המנועים 4B11/4B12 של הדור הזה הם הבסיס של מנועי 4J11/4J12. יש לאמת את מרווחי המצתים ונוזל הקירור מול המוסך.')
    rule('Mitsubishi',['OUTLANDER'],(2007,2012),'mitsubishi-outlander-2007-2012-2.0-2.4',engine_codes=['4B11','4B12'])
    sister('nissan-x-trail-2014-2021-1.6-diesel','nissan-x-trail-2019-2021-1.7-diesel','T32 (מתיחת פנים)',(2019,2021),['1.7 dCi (R9N)'],
      'טיוטה (מנוע אחות): לא נמצא לוח לאקס-טרייל עם מנוע 1.7 דיזל R9N. הלוח הועתק מלוח האקס-טרייל T32 עם מנוע 1.6 דיזל R9M (ניסאן דרום אפריקה); ה-R9N הוא גרסה מוגדלת של אותו מנוע ובאותו דגם, אך יש לאמת מול המוסך.')
    rule('Nissan',['X-TRAIL','X TRAIL','XTRAIL'],(2019,2021),'nissan-x-trail-2019-2021-1.7-diesel',engine_codes=['R9N'])
    save_rules('rules_sister.json')
