from lib import *
def sister(src, new_id, note_prefix, src_note, **over):
    d = json.load(open(f"/home/user/cv/data/schedules/{src}.json"))
    d.update(over); d["id"] = new_id; d["status"] = "draft"
    sp = {k: v for k, v in (d.get("specs") or {}).items() if k not in ("tires", "spare", "oil_capacity", "wipers", "warranty", "tire_pressure")}
    if sp: d["specs"] = sp
    else: d.pop("specs", None)
    d["sources"] = [dict(s, note=s["note"] + f" — {src_note}") for s in d["sources"]]
    d["notes"] = note_prefix + " הערות קובץ המקור: " + d["notes"]
    write(d)
sister("toyota-highlander-2021-2025-2.5-hybrid", "toyota-sienna-2021-2026-2.5-hybrid",
  "טיוטה ממקור אח: הסיינה (XL40) נמכרת בצפון אמריקה בלבד ומגיעה לישראל ביבוא מקביל/אישי; ליוניון מוטורס אין לה גיליון, והספר האמריקאי במייל (ולא נמצא עותק נגיש). הלוח הועתק מגיליון יוניון מוטורס להיילנדר ההיברידית (XU70) - אותה פלטפורמה TNGA-K ואותה מערכת הנעה היברידית 2.5 (A25A-FXS).",
  "מקור אח לטויוטה סיינה ההיברידית (אותה פלטפורמה TNGA-K ומנוע A25A-FXS)",
  model="Sienna", model_he="סיינה", generation="XL40 (hybrid)", years=[2021, 2026], importer="יבוא מקביל / אישי (לא יוניון מוטורס)")
sister("toyota-bz4x-2022-2025-ev", "toyota-c-hr-plus-2026-ev",
  "טיוטה ממקור אח: ל-C-HR+ החשמלית (2026) יוניון מוטורס מפרסמת ספר רכב אך לא גיליון אחזקה (נבדק ב-API: modelId 44). הלוח הועתק מגיליון יוניון מוטורס ל-bZ4X - אותה פלטפורמה חשמלית e-TNGA ואותו סוג מערכת הנעה.",
  "מקור אח לטויוטה C-HR+ החשמלית (אותה פלטפורמה e-TNGA)",
  model="C-HR+", model_he="C-HR+ חשמלית", generation="C-HR+ (e-TNGA)", years=[2026, 2026], engines=["EV (2XM / 1XM)"])
sister("kia-carens-2013-2018-2.0", "hyundai-i40-2012-2015-2.0",
  "טיוטה ממקור אח: ספר ישראלי של i40 לא נמצא (בספריית כלמוביל אין i40; הספר הבריטי של היונדאי כולל רק 1.6 GDI ודיזל, ובלי טבלת 2.0). הלוח הועתק מספר היבואן העברי של קיה קרנס RP עם אותו מנוע 2.0 GDI (Nu, G4NC) ומאותה תקופה; הפלטפורמה שונה, ולכן פריטי השלדה לאימות.",
  "מקור אח ליונדאי i40 2.0 (אותו מנוע G4NC)",
  make="Hyundai", make_he="יונדאי", importer="כלמוביל", model="i40", model_he="i40", generation="VF", years=[2012, 2015])
sister("kia-sorento-2021-2026-1.6-hybrid", "kia-carnival-2025-2026-1.6-hybrid",
  "טיוטה ממקור אח: לקרניבל ההיברידית (KA4 מתיחת פנים, 2025) לא נמצא ספר עברי באתר קיה ישראל (ספר הקרניבל הקיים הוא Carnival-KA4-2021 למנועי 3.5 ו-2.2 דיזל). הלוח הועתק מספר היבואן העברי של קיה סורנטו MQ4 היברידית - אותה פלטפורמה N3 ואותה מערכת היברידית 1.6 T-GDI (G4FT).",
  "מקור אח לקיה קרניבל ההיברידית (אותה פלטפורמה N3 ומנוע G4FT)",
  model="Carnival Hybrid", model_he="קרניבל היברידית", generation="KA4 PE hybrid", years=[2025, 2026])
