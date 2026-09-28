import json, os
OUT='/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/europe2'
ML='https://www.manualslib.com/manual/504809/Opel-Corsa.html'
# Opel Corsa D owner's manual (EN, manualslib 504809), "Service schedule Europe" printed pp. 232-234 and
# "International service schedule" printed pp. 235-237 (site pages 238-243). Five columns (years 1-5).
# Same X pattern in both schedules. col -> set of rows.
ALL=[1,2,3,4,5]; EVEN=[2,4]; ODD=[1,3,5]
rows=[
 ('lights','inspect',ALL,'נוריות אזהרה, תאורה ואיתות; גם מנעולי הגה והתנעה'),
 ('wipers','inspect',ALL,'מגבים, מתזי שמשה ופנסים; כיוון לפי הצורך'),
 ('washer_fluid','inspect',ALL,None),
 ('coolant','inspect',ALL,'מפלס והגנת קיפאון; השלמה לפי הצורך'),
 ('coolant_hoses','inspect',ALL,'דליפות והידוק'),
 ('brake_fluid','inspect',ODD,'מפלס (בשנים שבהן לא מוחלף)'),
 ('battery_12v','inspect',ALL,'הידוק הדקים'),
 ('diagnostics','inspect',ALL,'בדיקת מערכות במחשב ואיפוס תצוגת הטיפול'),
 ('cabin_filter','replace',EVEN,'מסנן אבקנים או פחם פעיל'),
 ('drive_belt','inspect',EVEN,'בדיקה חזותית'),
 ('engine_oil','replace',ALL,None),
 ('oil_filter','replace',ALL,None),
 ('parking_brake','adjust',EVEN,'בדיקה וכיוון לפי הצורך'),
 ('suspension','inspect',EVEN,'מתלים קדמיים ואחוריים'),
 ('brake_lines','inspect',EVEN,None),
 ('fuel_lines','inspect',EVEN,None),
 ('exhaust','inspect',EVEN,None),
 ('body_underside','inspect',ALL,'מרכב וציפוי תחתון; נזקים נרשמים בפנקס השירות'),
 ('brake_pads','inspect',EVEN,'בדיקה חזותית של בלמים קדמיים ואחוריים'),
 ('brake_discs','inspect',EVEN,None),
 ('ac_system','inspect',ALL,'דליפות במדחס המזגן, יחד עם בדיקה חזותית של מנוע ותיבה'),
 ('steering','inspect',ALL,'גומיות ההגה, מוטות ההגה, קצוות מוט ומפרקים כדוריים'),
 ('cv_boots','inspect',ALL,None),
 ('tires','inspect',EVEN,'מצב ולחץ כולל גלגל חלופי; שחרור והידוק ברגי גלגל ל-110 ניוטון-מטר'),
 ('lights','adjust',EVEN,'כיוון פנסים ראשיים'),
 ('door_hinges','inspect',ALL,'בדיקת נעילה מרכזית; בשירות השני והרביעי גם שימון צירים, מנעולים ותפסים'),
]
long=[
 {'item':'air_filter','action':'replace','every_km':60000,'every_months':48},
 {'item':'spark_plugs','action':'replace','every_km':60000,'every_months':48},
 {'item':'brake_fluid','action':'replace','every_months':24,'note':'יחד עם נוזל המצמד בתיבה ידנית רובוטית; ללא קשר לק"מ'},
 {'item':'brake_drums','action':'inspect','every_km':60000,'every_months':48,'note':'פירוק תופים, ניקוי ובדיקה חזותית'},
]
src_ml={'url':ML+'?page=238','kind':'manufacturer','note':'Opel Corsa D owner\'s manual (EN, manualslib 504809): "Service schedule Europe" printed pp. 232-234 (30,000 km columns) and "International service schedule" pp. 235-237 (15,000 km columns), site pages 238-243. This edition lists Z-series engines (Z12XEP/Z14XEP family), not the later A14XER/B14XER.'}
src_d={'url':'https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_D/2010_2016/2013/manual_user/om_corsa_kta-2656_11-heb_eu_my13_ed0612_16_he_il_online%5Bcorsa%5D.pdf','kind':'importer','note':'ספר הנהג העברי של קורסה D (שנתון 2013), עמ\' 176 (דף 178 בקובץ): ישראל מופיעה ברשימת מדינות תכנית הטיפולים האירופית, טיפול כל 30,000 ק"מ או שנה. אין בספר טבלת פריטים'}
src_e={'url':'https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_E/2011_2016/2016/manual_user/om_corsa_kta-2764_3-heb_eu_my16_ed0815_14_he_il_online%5B_corsa%5D.pdf','kind':'importer','note':'ספר הנהג העברי של קורסה E (שנתון 2016), עמ\' 224 (דף 226 בקובץ): ישראל אינה ברשימת המדינות האירופיות ולכן חל המרווח הבינלאומי, 15,000 ק"מ או שנה. אין בספר טבלת פריטים'}
def build(step):
    svcs=[]
    for c in range(1,6):
        its=[]
        for item,act,cols,note in rows:
            if c in cols:
                d={'item':item,'action':act}
                if note: d['note']=note
                its.append(d)
        svcs.append({'km':step*c,'items':its})
    return svcs
common=dict(make='Opel',make_he='אופל',model='Corsa',model_he='קורסה',fuel='petrol',
  importer='קבוצת שלמה (יבואנית אופל 2010-2019; מאז 2019 דוד לובינסקי)',time_based=[],status='draft',
  specs={'_note':'הספר האנגלי (504809) מפרט החלפת רצועת תזמון ובדיקת מרווח שסתומים רק למנועים Z16LEL/Z16LER/Z17DTR, והחלפת מסנן דלק בנזין רק ל-Z16LEL/Z16LER; מנועי 1.2/1.4 אינם ברשימות אלה'})
D=dict(common,id='opel-corsa-2008-2015-1.2-1.4',generation='Corsa D',years=[2008,2015],engines=['1.2 (A12XER)','1.4 (Z14XEP/A14XER)'],
  interval={'km':30000,'months':12,'note':'ספר הנהג העברי של קורסה D (2013) משייך את ישראל לתכנית האירופית: 30,000 ק"מ או שנה. הטבלה נלקחה מהספר האנגלי'},
  cycle_km=150000,services=build(30000),long_interval=long,sources=[src_ml,src_d],
  notes='טבלת פריטים מתוך ספר הנהג האנגלי של קורסה D (טבלת אירופה, חמש עמודות של 30,000 ק"מ או שנה), עם המרווח שספר הנהג העברי קובע לישראל. בכל טיפול: שמן ומסנן, בדיקת מחשב, נוזלים, תאורה, הגה ומרכב. בכל שנייה (60,000 ק"מ): מסנן מזגן, בלמים, מתלים, צנרת, פליטה, בלם יד, צמיגים וכיוון פנסים. מסנן אוויר ומצתים כל 60,000 ק"מ או 4 שנים, נוזל בלמים כל שנתיים. במהדורת הספר שנבדקה מופיעים מנועי Z ולא A14XER, ולכן זו טיוטה. בספר העברי של קורסה E (2015 ואילך) ישראל כבר בתכנית הבינלאומית של 15,000 ק"מ.')
E=dict(common,id='opel-corsa-2015-2019-1.4',generation='Corsa E',years=[2015,2019],engines=['1.4 (B14XER)'],
  interval={'km':15000,'months':12,'note':'ספר הנהג העברי של קורסה E (2016): ישראל בתכנית הבינלאומית, 15,000 ק"מ או שנה'},
  cycle_km=75000,services=build(15000),long_interval=long,sources=[src_ml,src_e],
  notes='טבלת הפריטים הבינלאומית (חמש עמודות של 15,000 ק"מ או שנה) מתוך ספר הנהג האנגלי של קורסה D, הדור הקודם על אותה פלטפורמה; ספר קורסה E עצמו (עברי ואנגלי) נותן רק את המרווח. בכל טיפול: שמן ומסנן, בדיקת מחשב, נוזלים, תאורה, הגה ומרכב. בכל טיפול שני (30,000 ק"מ): מסנן מזגן, בלמים, מתלים, צנרת, פליטה, בלם יד, צמיגים וכיוון פנסים. מסנן אוויר ומצתים כל 60,000 ק"מ או 4 שנים, נוזל בלמים כל שנתיים. טיוטה: ספר של דגם אחר ומנועים אחרים.')
for s in (D,E):
    json.dump(s,open(os.path.join(OUT,s['id']+'.json'),'w'),ensure_ascii=False,indent=1)
print('ok')
