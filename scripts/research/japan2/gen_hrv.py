import json
OUT='/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/japan2/'
services=[]
for km in range(10000,200001,10000):
    it=[{"item":"engine_oil","action":"replace"}]
    if km%20000==0: it.append({"item":"oil_filter","action":"replace"})
    it+= [{"item":"brake_pads","action":"inspect"},{"item":"brake_discs","action":"inspect"},
          {"item":"steering","action":"inspect"},{"item":"suspension","action":"inspect"},{"item":"cv_boots","action":"inspect"},
          {"item":"tire_rotation","action":"rotate","note":"סבב צמיגים כל 10,000 ק\"מ; לחץ ומצב צמיגים לבדוק פעם בחודש"}]
    if km%30000==0: it.append({"item":"air_filter","action":"replace"})
    if km%20000==0:
        it+=[{"item":"cabin_filter","action":"replace"},{"item":"brake_lines","action":"inspect"},
             {"item":"exhaust","action":"inspect"},{"item":"fuel_lines","action":"inspect"},
             {"item":"cooling_system","action":"inspect","note":"בדיקת מפלס ומצב כל הנוזלים"}]
    if km%40000==0:
        it+=[{"item":"drive_belt","action":"inspect"},{"item":"cvt_oil","action":"replace","note":"בגיר CVT"}]
    if km in (80000,160000): it.append({"item":"fuel_filter","action":"replace"})
    services.append({"km":km,"items":it})
d={"id":"honda-hr-v-2016-2021-1.5","make":"Honda","make_he":"הונדה","model":"HR-V","model_he":"HR-V",
"generation":"RU (דור 2)","years":[2016,2021],"engines":["1.5 i-VTEC (L15B)"],"fuel":"petrol",
"importer":"מאיר (הונדה ישראל)",
"interval":{"km":10000,"months":12,"note":"לפי לוח ה-Maintenance Schedule הבינלאומי (לדגמים שאינם אוסטרליה, ניו זילנד ודרום אפריקה): שמן מנוע כל 10,000 ק\"מ או שנה, ובתנאים קשים כל 5,000 ק\"מ או חצי שנה"},
"cycle_km":200000,"services":services,
"long_interval":[
 {"item":"valve_clearance","action":"inspect","every_km":120000,"note":"כיוון השסתומים ב-120,000 ק\"מ רק אם הם רועשים"},
 {"item":"spark_plugs","action":"replace","every_km":100000,"note":"מצתי אירידיום; מצתי ניקל כל 40,000 ק\"מ"},
 {"item":"coolant","action":"replace","first_km":200000,"first_months":120,"then_every_km":100000,"then_every_months":60},
 {"item":"manual_gearbox_oil","action":"replace","every_km":120000,"every_months":72,"note":"רק בגיר ידני; בתנאים קשים ב-60,000, 120,000 ו-180,000"},
 {"item":"differential_oil","action":"replace","first_km":20000,"then_every_km":80000,"note":"רק בדגמים עם הנעה כפולה (דיפרנציאל אחורי); בלוח: 20,000, 100,000 ו-180,000"}],
"time_based":[{"item":"brake_fluid","action":"replace","every_months":36,"note":"כל 3 שנים בלי קשר לק\"מ"}],
"specs":{},
"sources":[
 {"url":"https://www.manualslib.com/manual/2532246/x.html?page=508","kind":"manufacturer","note":"ספר הבעלים הבינלאומי (אנגלית) של הונדה HR-V 2018, \"Maintenance Schedule\" לדגמים שאינם אוסטרליה, ניו זילנד ודרום אפריקה, עמודי ספר 507-508 (manualslib 508-509); הטבלה נקראה מצילום העמוד"},
 {"url":"https://honda.co.il/guide_books/","kind":"importer","note":"ספריית ספרי הרכב של הונדה ישראל חסומה (Cloudflare, 403 גם ב-Playwright); לא נמצא ספר עברי"}],
"status":"draft",
"notes":"טיוטה מספר הבעלים הבינלאומי באנגלית של HR-V 2018 (דור RU), לא מספר ישראלי. שמן כל 10,000 ק\"מ או שנה, מסנן שמן כל 20,000, מסנן מזגן כל 20,000, מסנן אוויר כל 30,000, נוזל CVT כל 40,000, מסנן דלק ב-80,000 וב-160,000. בדיקת בלמים, היגוי, מתלים וגומיות ציריות כל 10,000 ק\"מ או חצי שנה. מצתים כל 100,000 ק\"מ ונוזל קירור ראשון ב-200,000 ק\"מ או 10 שנים."}
json.dump(d,open(OUT+d['id']+'.json','w'),ensure_ascii=False,indent=2)
