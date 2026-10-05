import json
ST="/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/tail4/"
for fid, oil, cap in [("toyota-c-hr-2024-2026-1.8-hybrid", "API SM/SN/SN Plus, 0W-16, 0W-20 או 5W-30 (לפי טבלת הנוזלים בגיליון)", "4.2 ליטר (לפי הגיליון)"),
                      ("toyota-aygo-x-2026-1.5-hybrid", "API SM/SN/SN Plus, 0W-16, 0W-20 או 5W-20 (לפי טבלת הנוזלים בגיליון)", None)]:
    p = ST + fid + ".json"; d = json.load(open(p))
    d["specs"]["engine_oil"] = oil
    if cap: d["specs"]["oil_capacity"] = cap
    d["long_interval"] = [
        {"item": "coolant", "action": "replace", "first_km": 150000, "then_every_km": 75000, "note": "נוזל קירור מנוע: החלפה ראשונה ב-150,000 (בטבלה) ואחריה כל 75,000 לפי הערת הגיליון"},
        {"item": "coolant", "action": "replace", "first_km": 240000, "then_every_km": 75000, "note": "נוזל קירור של המערכת ההיברידית (ממיר): החלפה ראשונה ב-240,000 ואחריה כל 75,000; בטבלה רק בדיקה"},
    ]
    d["notes"] = d["notes"].replace("הועתק מלוח", "לפי לוח") + " נוזל הקירור ההיברידי נבדק בטבלה ומוחלף לפי ההערה בגיליון (ראו long_interval). בטבלת 'תחזוקה מחמירה' של הגיליון: שמן ומסנן כל 7,500 ק\"מ או חצי שנה."
    json.dump(d, open(p, "w"), ensure_ascii=False, indent=2)
