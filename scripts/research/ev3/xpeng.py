import json
from lib import write
g6 = json.load(open('/home/user/cv/data/schedules/xpeng-g6-2024-2026-ev.json'))
DE = {"url": "https://edge.sitecorecloud.io/hedinitaban27a1-hedin8837-prod5c4b-4604/media/Project/Hedin/Distribution-Cars/shared/user-manual/XPENG-Benutzer--und-Wartungshandbuch.pdf",
      "kind": "manufacturer",
      "note": "XPENG Benutzer- und Wartungshandbuch (für Deutschland), חל על כל דגמי XPENG הנמכרים באיחוד האירופי; טבלת התחזוקה עמ' 15-21 (כל 12 חודשים/20,000 ק\"מ וכל 24 חודשים/40,000 ק\"מ; שמן תיבה 48 חודשים/80,000; נוזל קירור 72 חודשים/120,000)"}
G6SRC = dict(g6['sources'][0]); G6SRC['note'] = "ספר האחריות והתחזוקה האירופי של G6 - אותה טבלה כמו במסמך הגרמני הכללי, עמ' 11-18"
for mid, model, years, eng in [("xpeng-g9-2024-2026-ev", "G9", [2024, 2026], ["EV (TZ220XSEDM / TZ230XY01E)"]),
                               ("xpeng-p7i-2024-2025-ev", "P7i", [2024, 2025], ["EV (TZ220XSFDM)"])]:
    d = json.loads(json.dumps(g6))
    d.update(id=mid, model=model, model_he=model, generation=model, years=years, engines=eng)
    d['interval']['note'] = "לפי ספר התחזוקה האירופי הכללי של XPENG: טיפול כל 12 חודשים או 20,000 ק\"מ; הטור השני (טיפול מורחב) כל 24 חודשים או 40,000 ק\"מ"
    d['sources'] = [DE, G6SRC]
    d['specs'] = {"battery": "סוללת הנעה + מצבר 12V", "_note": "טיוטה - לפי מסמך אירופי כללי לכל דגמי XPENG, לא נבדק מול ספר היבואן"}
    d['notes'] = ("אתר היבואן (פריסבי) לא זמין מכאן ולא נמצא ספר עברי ל-" + model + ". ספר האחריות והתחזוקה הגרמני של XPENG חל על כל דגמי המותג באיחוד האירופי, ותוכנו זהה לספר של G6, "
                  "ולכן זו טיוטה לפי אותה טבלה: טיפול A כל 20,000 ק\"מ/שנה וטיפול B כל 40,000 ק\"מ/שנתיים (בטיפול B מוחלפים נוזל הבלמים ומסנן המזגן). "
                  "שמן תיבת ההפחתה כל 80,000 ק\"מ/4 שנים ונוזל קירור כל 120,000 ק\"מ/6 שנים. בתנאי שימוש קשים (אבק, חום מעל 40 מעלות, הרים, שימוש מסחרי) יש לטפל לעתים קרובות יותר.")
    write(d)
