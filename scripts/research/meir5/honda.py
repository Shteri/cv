from common import *
SRC='https://www.manualpdf.co.il/honda/jazz-2010/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=324'
def svc(km):
    it=[I('engine_oil','replace','או פעם בשנה'),
        I('brake_pads','inspect','בלמים קדמיים ואחוריים (או כל 6 חודשים)'), I('brake_discs','inspect'),
        I('tire_rotation','rotate','ובדיקת לחץ ומצב הצמיגים לפחות פעם בחודש'),
        I('steering','inspect','מוטות היגוי, תיבת הגה ומגפונים'), I('suspension','inspect'), I('cv_boots','inspect')]
    if km%20000==0:
        it+=[I('oil_filter','replace'), I('cabin_filter','replace','מסנן אבק ואבקנים'),
             I('brake_lines','inspect','כולל ABS'), I('coolant','inspect','מפלסי כל הנוזלים ומצבם'), I('brake_fluid','inspect','מפלס ומצב'),
             I('exhaust','inspect'), I('fuel_lines','inspect')]
    if km in (20000,40000,80000,120000,160000,200000): it.append(I('parking_brake','adjust','בדיקת כיוון בלם היד'))
    if km%30000==0: it.append(I('air_filter','replace'))
    if km%40000==0: it+=[I('valve_clearance','inspect'), I('drive_belt','inspect'), I('cvt_oil','replace','גיר CVT')]
    if km%80000==0: it.append(I('fuel_filter','replace'))
    if km%100000==0: it.append(I('spark_plugs','replace','מצתי אירידיום'))
    if km==120000: it.append(I('diagnostics','inspect','בדיקת סיבובי סרק'))
    return {'km':km,'items':it}
jz={
 'id':'honda-jazz-2009-2014-1.2-1.4','make':'Honda','make_he':'הונדה','model':'Jazz','model_he':"ג'אז",
 'generation':'GE','years':[2009,2014],'engines':['1.2 i-VTEC (L12B1)','1.3/1.4 i-VTEC (L13Z1)'],'fuel':'petrol','importer':'מאיר',
 'interval':{'km':10000,'months':12,'note':'לפי ספר הנהג הבינלאומי של הונדה (טבלה לרכב ללא חוברת שירות): שמן כל 10,000 ק"מ או שנה; בדיקות בלמים, היגוי ומתלים כל 10,000 ק"מ או חצי שנה'},
 'cycle_km':200000,
 'services':[svc(k) for k in range(10000,200001,10000)],
 'long_interval':[
   L('air_filter','replace','החלפה כל 30,000 ק"מ', every_km=30000),
   L('valve_clearance','inspect', every_km=40000),
   L('spark_plugs','replace', every_km=100000),
   L('coolant','replace','ראשונה ב-200,000 ק"מ או 10 שנים, ואחר כך כל 100,000 ק"מ או 5 שנים', first_km=200000, first_months=120, then_every_km=100000, then_every_months=60),
   L('manual_gearbox_oil','replace','גיר ידני, תנאים רגילים (בתנאים קשים: כל 60,000)', every_km=120000, every_months=72),
   L('cvt_oil','replace','גיר CVT', every_km=40000),
   L('brake_fluid','replace', every_months=36),
 ],
 'time_based':[T('brake_fluid','replace',36,'כל 3 שנים, בלי קשר לק"מ'), T('engine_oil','replace',12,'פעם בשנה אם לא הגיעו ל-10,000 ק"מ')],
 'specs':{'_note':'טיוטה: מספר הנהג הבינלאומי, לא מספר היבואן'},
 'sources':[{'url':SRC,'kind':'manufacturer','note':"Honda Jazz (GE) owner's manual 32TF0630 (general markets), 'Maintenance Schedule (On vehicles without Service Book)' pp. 319-320 (manualpdf.co.il pages 324-325); severe conditions p. 322"}],
 'status':'draft',
 'notes':'טיוטה: הלוח לקוח מספר הנהג הבינלאומי (באנגלית) של הונדה ג\'אז דור GE, מהטבלה לרכבים ללא חוברת שירות; ספר עברי של מאיר לא נמצא (honda.co.il חסום). עמודות הטבלה הן כל 20,000 ק"מ עד 200,000, ופריטים מסוימים כתובים כמרווח קבוע: שמן כל 10,000 או שנה, בדיקת בלמים והיגוי ומתלים כל 10,000 או חצי שנה, מסנן אוויר כל 30,000, מרווח שסתומים כל 40,000, מצתים כל 100,000. מסנן שמן, מסנן מזגן ובדיקות נוזלים, צנרת ופליטה כל 20,000; מסנן דלק ב-80,000 וב-160,000; רצועת עזר ושמן CVT כל 40,000; בלם יד ב-20/40/80/120/160/200 אלף; סיבובי סרק ב-120,000. הספר מגדיר נהיגה בחום של מעל 35 מעלות, פקקים ונסיעות קצרות כתנאים קשים: אז שמן כל 5,000 ק"מ או חצי שנה ומסנן שמן כל 10,000.'
}
write(jz)
