from lib import *
FIX15 = {"toyota-auris-2013-2019-1.6": "281/conn 40", "toyota-c-hr-2017-2019-1.2": "285/conn 534", "toyota-corolla-2007-2012-1.6": "287/conn 109",
         "toyota-corolla-2013-2019-1.6": "289/conn 123", "toyota-prius-2004-2009-1.5-hybrid": "301/conn 412", "toyota-rav4-2009-2012-2.0": "307/conn 249",
         "toyota-rav4-2013-2019-2.0": "307/conn 249", "toyota-verso-2009-2018-1.6-1.8": "310", "toyota-yaris-2011-2019-1.33-1.5": "311",
         "toyota-yaris-2020-2025-1.5": "336", "toyota-verso-s-2010-2016-1.33": "309/conn 261", "toyota-yaris-cross-2021-2025-1.5": "341/conn 940",
         "toyota-rav4-2016-2019-2.5-hybrid": "308"}
NOTE15 = " תיקון (סבב 5): רצועת ההינע בגיליון היא שורת טקסט - בדיקה ראשונה ב-105,000 ק\"מ (או 72 חודשים) ואחר כך כל 15,000 (או 12 חודשים); בגרסה הקודמת היא נקראה כבדיקה בודדת בעמודה שגויה."
def fix(fid, first, step, months_first, note, extra=None):
    d = json.load(open(f"/home/user/cv/data/schedules/{fid}.json"))
    for s in d["services"]:
        s["items"] = [e for e in s["items"] if e["item"] != "drive_belt"]
        if s["km"] >= first and (s["km"] - first) % step == 0:
            s["items"].append({"item": "drive_belt", "action": "inspect"})
    d["long_interval"] = [l for l in d["long_interval"] if l["item"] != "drive_belt"] + [
        L("drive_belt", "inspect", first_km=first, first_months=months_first, then_every_km=step, then_every_months=12, note="לפי הגיליון: בדיקה ראשונה ואחר כך במרווח הקבוע; החלפה לפי הצורך")]
    if extra: extra(d)
    d["notes"] = d["notes"] + note
    write(d)
for fid in FIX15:
    fix(fid, 105000, 15000, 72, NOTE15)
# Hilux 2015-2019 (sheets 292/293/294) and 2020-2025 (329/357): belt text, coolant row and air-filter text row
AIR = "IIRIIRIIRIIRIIRI"
def hilux_extra(d):
    for i, s in enumerate(d["services"]):
        s["items"] = [e for e in s["items"] if e["item"] not in ("coolant", "air_filter")]
        a = AIR[i]
        s["items"].append({"item": "air_filter", "action": "replace" if a == "R" else "inspect"})
        if s["km"] % 40000 == 0:
            s["items"].append({"item": "coolant", "action": "replace" if s["km"] == 160000 else "inspect"})
    d["long_interval"].append(L("air_filter", "replace", every_km=30000, every_months=36, note="לפי הגיליון: בדיקה כל 10,000 ק\"מ (או 6 חודשים) והחלפה כל 30,000 (או 36 חודשים); בתנאי אבק בדיקה כל 2,500"))
NOTEHX = (" תיקון (סבב 5): בגיליון שורות טקסט שלא נקראו בגרסה הקודמת - מסנן אוויר (בדיקה כל 10,000, החלפה כל 30,000) ורצועת הינע (בדיקה ראשונה ב-100,000 ואז כל 20,000); "
          "נוזל הקירור נבדק כל 40,000 ומוחלף ב-160,000 (בגרסה הקודמת סומן בעמודה שגויה). נבדק מול גיליונות 293 (conn 170) ו-329 (conn 848).")
for fid in ["toyota-hilux-2015-2019-2.4-2.8-diesel", "toyota-hilux-2020-2025-2.4-2.8-diesel"]:
    fix(fid, 100000, 20000, 72, NOTEHX, hilux_extra)
