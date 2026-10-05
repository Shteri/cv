from lib import *
def sister(src, new_id, note_prefix, src_note, **over):
    d = json.load(open(f"/home/user/cv/data/schedules/{src}.json"))
    d.update(over); d["id"] = new_id; d["status"] = "draft"
    sp = {k: v for k, v in d.get("specs", {}).items() if k not in ("tires", "spare", "oil_capacity", "wipers", "warranty", "tire_pressure")}
    if sp: d["specs"] = sp
    else: d.pop("specs", None)
    d["sources"] = [dict(s, note=s["note"] + f" — {src_note}") for s in d["sources"]]
    d["notes"] = note_prefix + " הערות הקובץ המקורי: " + d["notes"]
    write(d)
sister("hyundai-ioniq-5-2024-2026-ev", "genesis-gv60-2022-2026-ev",
       "טיוטה ממקור אח: ל-GV60 לא נמצא ספר ישראלי או ספר עם לוח בק\"מ (הספר האמריקאי במייל). הלוח הועתק מספר העברי של איוניק 5 (2024-2026) של כלמוביל - אותה פלטפורמה E-GMP ואותו מנוע חשמלי EM17. ספר איוניק 5 של 2021 קבע טיפול כל 15,000 ק\"מ/שנה.",
       "מקור אח ל-Genesis GV60 (אותה פלטפורמה E-GMP ומנוע EM17)",
       make="Genesis", make_he="ג'נסיס", model="GV60", model_he="GV60", generation="JW1", years=[2022, 2026], engines=["EV (EM17 / EM18, E-GMP)"])

OPT = {"url": "https://www.manualpdf.co.il/kia/optima-2018/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=721", "kind": "manufacturer", "note": "ספר הנהג הבינלאומי של קיה אופטימה JF 2018, טבלאות הדיזל (U-II 1.7) לאירופה בעמ' 719-722 ומחוץ לאירופה בעמ' 725-728: מבנה זהה (רשימות לכל 30,000 באירופה; מחוץ לאירופה שמן כל 10,000)"}
def sister2(src, new_id, prefix, src_note, extra_src=None, **over):
    sister(src, new_id, prefix, src_note, **over)
    if extra_src:
        p = os.path.join(ST, new_id + ".json"); d = json.load(open(p)); d["sources"].append(extra_src); json.dump(d, open(p, "w"), ensure_ascii=False, indent=2)
sister2("kia-carens-2013-2019-1.7-diesel", "kia-optima-2012-2018-1.7-diesel",
   "טיוטה ממקור אח: ספר ישראלי של אופטימה דיזל לא נמצא. הלוח הועתק מספר היבואן העברי (קיה ישראל) של קרנס RP עם אותו מנוע 1.7 CRDi (D4FD); הטבלה האירופית של אופטימה JF לאותו מנוע זהה במבנה ובמרווחים.",
   "מקור אח לקיה אופטימה 1.7 דיזל (אותו מנוע D4FD ואותו יבואן)", OPT,
   model="Optima", model_he="אופטימה", generation="TF / JF", years=[2012, 2018], engines=["1.7 CRDi (U2, D4FD)"])
sister("hyundai-sonata-2015-2019-2.0-hybrid", "kia-optima-2016-2020-2.0-hybrid",
   "טיוטה ממקור אח: ספר ישראלי של אופטימה היברידית לא נמצא. הלוח הועתק מספר כלמוביל העברי של יונדאי סונטה LF היברידית - אותה פלטפורמה ואותו מנוע 2.0 GDI היברידי (G4NG).",
   "מקור אח לקיה אופטימה JF היברידית (אותה פלטפורמה ומנוע G4NG)",
   make="Kia", make_he="קיה", importer="טלקאר", model="Optima Hybrid", model_he="אופטימה היברידית", generation="JF hybrid", years=[2016, 2021])
sister("hyundai-santa-fe-2010-2012-2.4", "kia-sorento-2010-2012-2.4",
   "טיוטה ממקור אח: ספר של סורנטו XM עם לוח בק\"מ לא נמצא (רק ספרים אמריקאיים במייל). הלוח הועתק מקובץ סנטה פה CM 2.4 - אותה פלטפורמה ואותו מנוע G4KE.",
   "מקור אח לקיה סורנטו XM 2.4 (אותה פלטפורמה ומנוע G4KE)",
   make="Kia", make_he="קיה", importer="טלקאר", model="Sorento", model_he="סורנטו", generation="XM", years=[2010, 2012])
for mdl, mhe, gen, yrs, nid in [("Forte (Cerato)", "פורטה", "YD", [2016, 2018], "kia-forte-2016-2018-1.6-diesel"), ("Soul", "סול", "AM / PS", [2011, 2017], "kia-soul-2011-2017-1.6-diesel")]:
    sister("kia-ceed-2012-2018-1.6-diesel", nid,
       f"טיוטה ממקור אח: ספר של {mhe} דיזל לא נמצא. הלוח הועתק מקובץ סיד JD 1.6 דיזל - אותו מנוע 1.6 CRDi (D4FB) ואותה משפחת פלטפורמה; הקובץ המקורי עצמו טיוטה מהטבלה האירופית.",
       f"מקור אח לקיה {mdl} 1.6 דיזל (אותו מנוע D4FB)", model=mdl, model_he=mhe, generation=gen, years=yrs)
sister("kia-sorento-2021-2026-1.6-hybrid", "hyundai-staria-hybrid-2025-2026-1.6",
   "טיוטה ממקור אח: לא נמצא ספר של סטאריה היברידית (כלמוביל לא מפרסמת ספר סטאריה). הלוח הועתק מספר היבואן העברי של קיה סורנטו MQ4 היברידית - אותה פלטפורמה N3 ואותו מנוע 1.6 T-GDI היברידי (G4FT).",
   "מקור אח ליונדאי סטאריה היברידית (אותה פלטפורמה N3 ומנוע G4FT)",
   make="Hyundai", make_he="יונדאי", importer="כלמוביל", model="Staria Hybrid", model_he="סטאריה היברידית", generation="US4 hybrid", years=[2025, 2026])
sister("hyundai-tucson-2021-2026-1.6t-2.0", "hyundai-sonata-2020-2024-1.6-turbo",
   "טיוטה ממקור אח: ספר כלמוביל של סונטה DN8 קיים רק לגרסה ההיברידית. הלוח הועתק מספר כלמוביל העברי של טוסון NX4 - אותה פלטפורמה N3 ואותו מנוע 1.6 T-GDI (G4FP). שורות מנוע 2.0 בקובץ המקור לא רלוונטיות.",
   "מקור אח ליונדאי סונטה DN8 1.6 טורבו (אותה פלטפורמה ומנוע G4FP)",
   model="Sonata", model_he="סונטה", generation="DN8", years=[2020, 2024], engines=["1.6 T-GDI (Smartstream G1.6T, G4FP)"])
sister("kia-sportage-2011-2015", "hyundai-ix35-2010-2015-2.4",
   "טיוטה ממקור אח: מנוע 2.4 של ix35 אינו מופיע בספר הבינלאומי של ix35 שנמצא. הלוח הועתק מספר קיה ישראל העברי לספורטאז' SL - התאומה של ix35 עם מנועי Theta II (2.0/2.4).",
   "מקור אח ליונדאי ix35 2.4 (אותה פלטפורמה ומשפחת מנוע Theta II)",
   make="Hyundai", make_he="יונדאי", importer="כלמוביל", model="ix35", model_he="ix35", generation="LM", years=[2010, 2015], engines=["2.4 (Theta II, G4KE)"])
