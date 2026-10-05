#!/usr/bin/env python3
"""Generate data/schedules/*.json from compact per-column rules.

Why: the importer books present each plan as a grid (columns = service km,
rows = items, cells = I inspect / R replace / -). Transcribing the grid as an
8-character string per item ("IRIRIRIR") is far easier to check against the
book than hundreds of lines of JSON. Run:

    python3 scripts/build_schedules.py        # writes the files
    node scripts/validate.mjs                 # then validate

Only schedules defined here are (re)written. Draft files that were written by
hand (Toyota, Mazda, Skoda, i25) are left alone.

Facts (which item, which km) come from the Israeli importer's Hebrew book.
Text is ours. Never paste book sentences.
"""
import json
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(ROOT, "schedules")
ITEMS = json.load(open(os.path.join(ROOT, "items.json"), encoding="utf-8"))

ACT = {"I": "inspect", "R": "replace", "C": "clean", "A": "adjust", "-": None}


def grid(cols, rows, notes=None):
    """cols: list of km. rows: list of (item, pattern[, note]).
    pattern is a string with one char per column: I / R / -."""
    notes = notes or {}
    services = []
    for ci, km in enumerate(cols):
        items = []
        for row in rows:
            item, pat = row[0], row[1]
            note = row[2] if len(row) > 2 else None
            if len(pat) != len(cols):
                raise ValueError(f"{item}: pattern {pat!r} has {len(pat)} chars, grid has {len(cols)} columns")
            act = ACT[pat[ci]]
            if act is None:
                continue
            if item not in ITEMS:
                raise KeyError(f"unknown item key {item!r}")
            entry = {"item": item, "action": act}
            if note:
                entry["note"] = note
            items.append(entry)
        services.append({"km": km, "items": items})
    return services


def long_(item, action, **kw):
    """Item whose interval is longer than the grid or not aligned to it.
    kw: every_km, every_months, first_km, first_months, then_every_km,
    then_every_months, note."""
    if item not in ITEMS:
        raise KeyError(f"unknown item key {item!r}")
    d = {"item": item, "action": action}
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


# ---------------------------------------------------------------------------
# specs: one-line facts from the book's "מפרטים" chapter (oil grade and
# capacity, coolant, brake fluid, tires, battery, timing, warranty). Values
# marked in _note as checked were read in the Israeli book; the rest are
# general knowledge carried over from the product session's draft.
# ---------------------------------------------------------------------------
CHECKED = "שמן, נוזל קירור, נוזל בלמים, דלק וצמיגים אומתו מול ספר היבואן; מצבר, תזמון ואחריות: ידע כללי, לאימות"
CHECKED_NO_TIRES = "שמן, נוזל קירור, נוזל בלמים ודלק אומתו מול ספר היבואן; צמיגים, מצבר, תזמון ואחריות: ידע כללי, לאימות"
HY_WARRANTY = "כלמוביל: 3 שנים או 100,000 ק\"מ (המוקדם), מצבר 24 חודשים, צבע 12 חודשים או 20,000 ק\"מ"
KIA_WARRANTY = "טלקאר: 3 שנים או 100,000 ק\"מ (המוקדם), הרחבה בתשלום"
MZ_WARRANTY = "דלק מוטורס: 3 שנים או 100,000 ק\"מ (ידע כללי, לאימות)"
SPECS = {
 "hyundai-i10-2014-2019": {"_note": CHECKED,
   "engine_oil": "API SM / ACEA A5 ומעלה, 5W-30 (מותר 5W-20)", "oil_capacity": "1.0: 3.0 ליטר; 1.25: 3.6 ליטר (ריקון ומילוי כולל מסנן)",
   "coolant": "אתילן גליקול למקרן אלומיניום; 1.0: 4.8-4.9 ליטר, 1.25: 5.2-5.3 ליטר", "brake_fluid": "DOT 4 (FMVSS116), 0.7-0.8 ליטר",
   "fuel": "בנזין 95 אוקטן, מיכל 40 ליטר", "tires": "155/70 R13, 175/65 R14 או 185/55 R15; חלופי T115/70 D15", "tire_pressure": "14-15 אינץ': 32 psi (2.2 בר) קדמי ואחורי, בעומס מלא 33/34; 13 אינץ': 36 psi; חלופי 60 psi",
   "battery": "מצבר רגיל 12V, לוודא מידה מול הקיים", "timing": "שרשרת, ללא החלפה מתוכננת", "spare": "גלגל חלופי צר או ערכת תיקון, לפי רמת גימור", "warranty": HY_WARRANTY},
 "hyundai-i10-2020-2025": {"_note": "טיוטה, לאימות מול ספר הרכב (פרק 9)",
   "engine_oil": "5W-30 לפי תקן API עדכני / ACEA A5", "oil_capacity": "כ-3.6 ליטר", "coolant": "אתילן גליקול למקרן אלומיניום, לא לערבב",
   "brake_fluid": "DOT 4", "fuel": "בנזין 95 אוקטן", "tires": "175/65 R14 או 185/55 R15 (טיוטה)", "tire_pressure": "לפי המדבקה בעמוד הדלת",
   "battery": "מצבר רגיל 12V; ברכב עם Start-Stop (ISG) מצבר AGM/EFB בלבד", "timing": "שרשרת, ללא החלפה מתוכננת", "spare": "ערכת תיקון או גלגל חלופי צר", "warranty": HY_WARRANTY},
 "hyundai-i20-2015-2017": {"_note": CHECKED_NO_TIRES,
   "engine_oil": "API SM + ILSAC GF-4 או ACEA A5 ומעלה, 5W-30", "oil_capacity": "3.5 ליטר (ריקון ומילוי כולל מסנן)",
   "coolant": "אתילן גליקול למקרן אלומיניום, 4.3 ליטר", "brake_fluid": "DOT 4 (FMVSS116), 0.7-0.8 ליטר",
   "fuel": "בנזין 95 אוקטן, מיכל 50 ליטר", "tires": "185/65 R15 או 195/55 R16 (טיוטה)", "tire_pressure": "לפי המדבקה בעמוד הדלת",
   "battery": "מצבר רגיל 12V, לוודא מידה מול הקיים", "timing": "שרשרת, ללא החלפה מתוכננת", "spare": "גלגל חלופי צר", "warranty": HY_WARRANTY},
 "hyundai-i20-2018-2021": {"_note": CHECKED,
   "engine_oil": "MPI: 5W-30 ACEA A5/B5 (Shell Helix Ultra A5/B5); 1.0 T-GDI: 5W-40 ACEA A3/B4", "oil_capacity": "1.0 T-GDI: 3.6 ליטר; 1.25 ו-1.4: 3.5 ליטר",
   "coolant": "אתילן גליקול למקרן אלומיניום; 1.0: 6.4 ליטר, 1.25/1.4: 4.3 ליטר", "brake_fluid": "DOT 4 (FMVSS116), 0.7-0.8 ליטר",
   "fuel": "בנזין 95 אוקטן, מיכל 50 ליטר", "tires": "185/65 R15, 195/55 R16 או 205/45 R17; חלופי T125/80 D15",
   "tire_pressure": "185/65 R15: 34 psi קדמי, 31 אחורי (עומס רגיל); 16-17 אינץ' זהה; חלופי 60 psi. לפי המדבקה בעמוד הדלת",
   "battery": "מצבר רגיל 12V; עם Start-Stop (ISG): AGM/EFB בלבד", "timing": "שרשרת, ללא החלפה מתוכננת", "spare": "גלגל חלופי צר T125/80 D15 או ערכת תיקון", "warranty": HY_WARRANTY},
 "hyundai-elantra-2011-2015-1.6": {"_note": CHECKED,
   "engine_oil": "API SL/SM, ILSAC GF-3 או ACEA A3 ומעלה, 5W-30 (מותר 5W-20)", "oil_capacity": "3.3 ליטר (ריקון ומילוי)",
   "coolant": "אתילן גליקול למקרן אלומיניום, 6.4 ליטר", "brake_fluid": "DOT 3 או DOT 4 (FMVSS116), 0.7-0.8 ליטר",
   "fuel": "בנזין 95 אוקטן, מיכל 48 ליטר", "tires": "195/65 R15 או 205/55 R16; חלופי T125/80 D15",
   "tire_pressure": "2.2 בר (32 psi) קדמי ואחורי; חלופי 4.2 בר (60 psi)", "battery": "מצבר רגיל 12V, לוודא מידה מול הקיים",
   "timing": "שרשרת, ללא החלפה מתוכננת", "spare": "גלגל חלופי צר T125/80 D15", "warranty": HY_WARRANTY},
 "hyundai-elantra-2016-2018-1.6": {"_note": CHECKED,
   "engine_oil": "ACEA A5 ומעלה (בישראל מותר גם ACEA A3 או ILSAC GF-3), 5W-30", "oil_capacity": "3.6 ליטר (Gamma 1.6 MPI)",
   "coolant": "אתילן גליקול פוספטי למקרן אלומיניום, 5.6 ליטר", "brake_fluid": "DOT 3 או DOT 4 (FMVSS116), 0.7-0.8 ליטר",
   "fuel": "בנזין 95 אוקטן, מיכל 50 ליטר", "tires": "195/65 R15, 205/55 R16 או 225/45 R17; חלופי T125/80 D15/D16",
   "tire_pressure": "2.3 בר (33 psi) קדמי ואחורי; חלופי 4.2 בר", "battery": "מצבר רגיל 12V, לוודא מידה מול הקיים",
   "timing": "שרשרת, ללא החלפה מתוכננת", "spare": "גלגל חלופי צר", "warranty": HY_WARRANTY},
 "hyundai-ioniq-2016-2022-1.6-hybrid": {"_note": CHECKED,
   "engine_oil": "ACEA A5/B5 (בישראל מותר גם A3/B3), 0W-20 או 5W-30", "oil_capacity": "3.8 ליטר",
   "coolant": "שני מעגלים: נוזל קירור מנוע 6.7 ליטר ונוזל קירור ממיר 3.2 ליטר, אתילן גליקול פוספטי", "brake_fluid": "DOT 3 או DOT 4, 0.7-0.8 ליטר; נוזל מפעיל מצמד DOT 3",
   "fuel": "בנזין 95 אוקטן, מיכל 45 ליטר", "tires": "195/65 R15 או 225/45 R17; חלופי T125/80 D15",
   "tire_pressure": "2.5 בר (36 psi) קדמי ואחורי; חלופי 4.2 בר", "battery": "מצבר עזר 12V (AGM) בתא המטען, לא מצבר רגיל; סוללה היברידית ליתיום-יון",
   "timing": "שרשרת, ללא החלפה מתוכננת; רצועת HSG נבדקת בכל טיפול", "spare": "גלגל חלופי צר או ערכת תיקון", "warranty": HY_WARRANTY + "; סוללה היברידית 8 שנים או 160,000 ק\"מ (לאימות)"},
 "kia-picanto-2017-2025": {"_note": CHECKED,
   "engine_oil": "API SN / ACEA C2; לחיסכון בדלק מומלץ 0W-20, מותר גם 5W-30 ו-5W-40 (T-GDI: 5W-30/5W-40)", "oil_capacity": "1.0 MPI: 3.0 ליטר; 1.2 MPI: 3.5 ליטר; 1.0 T-GDI: 3.6 ליטר",
   "coolant": "אתילן גליקול למקרן אלומיניום, לא לערבב", "brake_fluid": "DOT 3 או DOT 4",
   "fuel": "בנזין 95 אוקטן", "tires": "155/80 R13, 175/65 R14, 185/55 R15 או 195/45 R16; חלופי T115/70 D15", "tire_pressure": "2.3 בר (33 psi) קדמי, 2.1 בר (30 psi) אחורי; בעומס מלא 2.3/2.5; Eco Pack 2.5 בכל הגלגלים; חלופי 4.2 בר",
   "battery": "מצבר רגיל 12V; עם Start-Stop (ISG): AGM/EFB בלבד", "timing": "שרשרת, ללא החלפה מתוכננת", "spare": "גלגל חלופי צר T115/70 D15 או ערכת תיקון, לפי רמת גימור", "warranty": KIA_WARRANTY},
 "kia-sportage-2016-2018": {"_note": CHECKED,
   "engine_oil": "1.6 GDI / 1.6 T-GDI / 2.4 GDI: 5W-30 ACEA A5 ומעלה; 2.0 MPI: 5W-20 API SM/ILSAC GF-4 או 5W-30 ACEA A5",
   "oil_capacity": "1.6 GDI: 3.6; 1.6 T-GDI: 4.5; 2.0 MPI: 4.0; 2.4 GDI: 4.8 ליטר", "coolant": "אתילן גליקול למקרן אלומיניום; 1.6 GDI: 7.3 (אוט') / 7.5 (ידני); 1.6 T-GDI: 7.3; 2.0: 6.9-7.1; 2.4: 7.1 ליטר",
   "brake_fluid": "DOT 3 או DOT 4 (FMVSS116)", "fuel": "בנזין 95 אוקטן, מיכל 62 ליטר", "tires": "215/70 R16, 225/60 R17 או 245/45 R19", "tire_pressure": "2.4 בר (35 psi) בכל הגלגלים, גם בעומס מלא",
   "battery": "מצבר רגיל 12V; עם Start-Stop (ISG): AGM/EFB בלבד", "timing": "שרשרת, ללא החלפה מתוכננת", "spare": "גלגל חלופי צר או ערכת תיקון", "warranty": KIA_WARRANTY},
 "kia-sportage-2019-2021": {"_note": CHECKED,
   "engine_oil": "1.6 GDI / 1.6 T-GDI: 5W-30 ACEA A5/B5/C2/C3; 2.0 MPI: 5W-20 API/ILSAC עדכני או 5W-30 ACEA A5/B5; 2.4 GDI: 5W-30",
   "oil_capacity": "1.6 GDI: 3.6; 1.6 T-GDI: 4.5; 2.0 MPI: 4.0; 2.4 GDI: 4.8 ליטר", "coolant": "אתילן גליקול למקרן אלומיניום (כמויות כמו 2016-2018)",
   "brake_fluid": "DOT 3 או DOT 4 (FMVSS116)", "fuel": "בנזין 95 אוקטן, מיכל 62 ליטר", "tires": "215/70 R16, 225/60 R17 או 245/45 R19; חלופי T135/90 R17", "tire_pressure": "2.4 בר (35 psi) בכל הגלגלים; בעומס מלא אחורי 2.75 בר (40 psi); חלופי 4.2 בר",
   "battery": "מצבר רגיל 12V; עם Start-Stop (ISG): AGM/EFB בלבד", "timing": "שרשרת, ללא החלפה מתוכננת", "spare": "גלגל חלופי רגיל, צר T135/90 R17 או ערכת תיקון לפי רמת גימור (נפח תא מטען 466/491/503 ליטר)", "warranty": KIA_WARRANTY},
 "kia-niro-2016-2022-1.6-hybrid": {"_note": CHECKED,
   "engine_oil": "API עדכני או ACEA A5/B5, 0W-20 או 5W-30", "oil_capacity": "3.8 ליטר",
   "coolant": "שני מעגלים: נוזל קירור מנוע 5.98 ליטר ונוזל קירור מערכת היברידית 2.43 ליטר, אתילן גליקול", "brake_fluid": "DOT 3 או DOT 4, כ-400 סמ\"ק; נוזל מפעיל מצמד DOT 3/4, 100 סמ\"ק",
   "fuel": "בנזין 95 אוקטן, מיכל 45 ליטר", "tires": "205/60 R16 או 225/45 R18; חלופי T125/80 D16", "tire_pressure": "2.5 בר (36 psi) קדמי ואחורי; חלופי 4.2 בר",
   "battery": "מצבר עזר 12V (AGM), לא מצבר רגיל; סוללה היברידית ליתיום-יון", "timing": "שרשרת; רצועת HSG נבדקת בכל טיפול", "spare": "גלגל חלופי צר T125/80 D16 או ערכת תיקון, לפי רמת גימור", "warranty": KIA_WARRANTY + "; סוללה היברידית 7 שנים או 150,000 ק\"מ (לאימות)"},
}
SPECS['hyundai-elantra-2019-2020-1.6'] = SPECS['hyundai-elantra-2016-2018-1.6']
MZ_SPECS_BASE = {"engine_oil": "5W-30 לפי ACEA A3/A5 או API SL/SM", "coolant": "Mazda FL22 מקורי (ירוק) בלבד", "brake_fluid": "DOT 4",
   "fuel": "בנזין 95 אוקטן", "tire_pressure": "לפי המדבקה בעמוד הדלת", "timing": "שרשרת, ללא החלפה מתוכננת",
   "_note": "שמן, נוזל קירור ונוזל בלמים מתוך תוכנית הטיפול של היבואן; נפח שמן, צמיגים, מצבר ואחריות: ידע כללי, לאימות"}
def mz_specs(**kw):
    d=dict(MZ_SPECS_BASE); d.update(kw); return d
SPECS.update({
 "mazda-3-2006-2012": mz_specs(oil_capacity="כ-4.3 ליטר (1.6) / 4.3 ליטר (2.0)", tires="195/65 R15 או 205/55 R16", battery="מצבר רגיל 12V", spare="גלגל חלופי צר", warranty=MZ_WARRANTY,
     brake_fluid="DOT 4 Super", engine_oil="5W-30 לפי ACEA A3/A5 או API SL/SM; שמן גיר Mazda V (אדום), שמן הגה Dexron III"),
 "mazda-3-2013-2019": mz_specs(oil_capacity="כ-4.2 ליטר (2.0) / 4.0 ליטר (1.5)", tires="205/60 R16 או 215/45 R18", battery="מצבר רגיל 12V; בדגמי i-Stop: EFB/AGM בלבד (Q-85)", spare="ערכת תיקון או גלגל חלופי צר, לפי רמת גימור", warranty=MZ_WARRANTY,
     engine_oil="5W-30 לפי ACEA A3/A5 או API SL/SM; שמן גיר אוטומטי Mazda FZ (כחול)"),
 "mazda-3-2020-2025": mz_specs(oil_capacity="כ-4.2 ליטר", tires="205/60 R16 או 215/45 R18", battery="i-Stop: EFB/AGM בלבד", spare="ערכת תיקון", warranty=MZ_WARRANTY,
     engine_oil="5W-30 API SN Plus; שמן גיר אוטומטי Mazda FZ (כחול)"),
 "mazda-2-2007-2014": mz_specs(oil_capacity="כ-3.9 ליטר", tires="185/55 R15", battery="מצבר רגיל 12V", spare="גלגל חלופי צר", warranty=MZ_WARRANTY,
     engine_oil="5W-30 לפי ACEA A3/A5 או API SL/SM; שמן גיר Mazda V (אדום)"),
 "mazda-2-2015-2025": mz_specs(oil_capacity="כ-4.0 ליטר (1.5)", tires="185/65 R15 או 185/60 R16", battery="בדגמי i-Stop: EFB/AGM בלבד", spare="ערכת תיקון או גלגל חלופי צר", warranty=MZ_WARRANTY,
     engine_oil="5W-30 לפי ACEA A3/A5 או API SL/SM; שמן גיר אוטומטי Mazda FZ (כחול)"),
 "mazda-cx-5-2012-2025": mz_specs(oil_capacity="כ-4.2 ליטר (2.0) / 4.5 ליטר (2.5)", tires="225/65 R17 או 225/55 R19", battery="בדגמי i-Stop: EFB/AGM בלבד", spare="גלגל חלופי צר או ערכת תיקון", warranty=MZ_WARRANTY,
     engine_oil="5W-30 לפי ACEA A3/A5 או API SL/SM; גיר אוטומטי Mazda FZ; ב-AWD תיבת העברה וסרן אחורי 80W-90 GL-5"),
 "mazda-cx-3-2017-2025": mz_specs(oil_capacity="כ-4.2 ליטר (2.0)", tires="215/60 R16 או 215/50 R18", battery="בדגמי i-Stop: EFB/AGM בלבד", spare="ערכת תיקון", warranty=MZ_WARRANTY,
     engine_oil="5W-30 לפי ACEA A3/A5 או API SL/SM; שמן גיר אוטומטי Mazda FZ (כחול)"),
 "mazda-cx-30-2020-2025": mz_specs(oil_capacity="כ-4.2 ליטר", tires="215/55 R18", battery="i-Stop: EFB/AGM בלבד", spare="ערכת תיקון", warranty=MZ_WARRANTY,
     engine_oil="5W-30 API SN Plus; שמן גיר אוטומטי Mazda FZ (כחול)"),
})


def write(s):
    if s["id"] in SPECS and "specs" not in s:
        # keep key order: specs before sources
        items = list(s.items()); idx = [k for k, _ in items].index("sources")
        items.insert(idx, ("specs", SPECS[s["id"]])); s = dict(items)
    path = os.path.join(OUT, s["id"] + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(s, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("wrote", os.path.relpath(path, os.path.join(ROOT, "..")))


ALL = "IIIIIIII"
EVEN = "-I-I-I-I"          # 2nd, 4th, 6th, 8th column
Q = "---I---I"             # 4th and 8th column
R_ALL = "RRRRRRRR"

# ---------------------------------------------------------------------------
# Hyundai (כלמוביל). Books: https://www.hyundaimotors.co.il/maintenance/
# ---------------------------------------------------------------------------
HY = {"make": "Hyundai", "make_he": "יונדאי", "importer": "כלמוביל"}

COLMOBIL_HUB = {"url": "https://www.hyundaimotors.co.il/maintenance/", "kind": "importer",
                "note": "מרכז ספרי הרכב של כלמוביל, קישורי PDF לפי דגם ושנה"}

# --- i10 IA (2014-2019) and i20 GB (2015-2017): first service 15,000 then every 20,000
GRID_15_35 = [15000, 35000, 55000, 75000, 95000, 115000, 135000, 155000]
AT_55_115 = "--I--I--"  # the 55 and 115 columns (36 and 72 months), as printed in both books (i10 p. 7-10, i20 p. 7-13)
ROWS_IA_GB = [
    ("drive_belt", ALL),
    ("engine_oil", R_ALL), ("oil_filter", R_ALL),
    ("air_filter", "IRIRIRIR"),
    ("evap_system", AT_55_115), ("vacuum_hose", EVEN), ("fuel_filter", AT_55_115, "פריט ללא תחזוקה לפי הספר; בדיקה בלבד"),
    ("fuel_lines", AT_55_115),
    ("battery_12v", ALL), ("electrical_system", EVEN),
    ("brake_lines", ALL), ("pedals", EVEN), ("parking_brake", ALL),
    ("brake_fluid", "IRIRIRIR"), ("brake_pads", ALL), ("brake_discs", ALL), ("brake_drums", EVEN),
    ("steering", ALL), ("cv_boots", ALL), ("tires", ALL), ("suspension", ALL), ("body_underside", ALL),
    ("ac_refrigerant", ALL), ("ac_system", ALL),
    ("cabin_filter", R_ALL),
]
# No cooling_system interval here: these books only say to check the coolant level and leaks daily and the
# water pump when the drive or timing belt is replaced (the 60,000/30,000 rule belongs to later Hyundai books).
LONG_IA_GB = [
    long_("spark_plugs", "replace", every_km=160000),
    long_("coolant", "replace", first_km=210000, first_months=120, then_every_km=40000, then_every_months=24),
    long_("manual_gearbox_oil", "inspect", every_km=60000, every_months=48, note="להחליף אחרי כל נסיעה במים עמוקים"),
    long_("transmission_oil", "inspect", every_km=60000, every_months=48),
]

write({
    **HY, "id": "hyundai-i10-2014-2019", "model": "i10", "model_he": "i10", "generation": "IA",
    "years": [2014, 2019], "engines": ["1.0 petrol (Kappa)", "1.25 petrol (Kappa)"], "fuel": "petrol",
    "interval": {"km": 20000, "months": 12,
                 "note": "טיפול ראשון ב-15,000 ק\"מ או 12 חודשים, אחר כך כל 20,000 ק\"מ או 12 חודשים (15, 35, 55, 75...)."},
    "first_service_km": 15000, "cycle_km": 160000,
    "services": grid(GRID_15_35, ROWS_IA_GB),
    "long_interval": LONG_IA_GB + [
        long_("valve_clearance", "inspect", every_km=95000, every_months=48, note="מנוע 1.0 בלבד"),
    ],
    "time_based": [],
    "sources": [
        {"url": "https://res.cloudinary.com/colmobil/images/v1716388497/ספר-רכב-יונדאי-i10-2014-2019_53335bdc4/ספר-רכב-יונדאי-i10-2014-2019_53335bdc4.pdf",
         "kind": "importer", "note": "ספר רכב i10 2014-2019 של כלמוביל, פרק 7 עמ' 9-13: לוח תחזוקה רגילה"},
        COLMOBIL_HUB,
    ],
    "status": "reviewed",
    "notes": "הועתק מלוח התחזוקה בספר הרכב הישראלי (ספטמבר 2026). הטבלה בספר בנויה בעמודות של 15/35/55... אלף ק\"מ. "
             "מסנן תא נוסעים מוחלף בכל טיפול לפי הספר. נוזל בלמים כל טיפול שני (35, 75, 115, 155). "
             "מסנן אוויר: בדיקה בטיפול אחד והחלפה בטיפול הבא. צינור אדים, מסנן דלק וקווי דלק נבדקים ב-55,000 וב-115,000. "
             "מערכת קירור: בדיקת מפלס ודליפות, בלי מרווח קבוע בספר. תוסף דלק מומלץ כל 15,000 ק\"מ אם הבנזין לא כולל תוספים.",
})

write({
    **HY, "id": "hyundai-i20-2015-2017", "model": "i20", "model_he": "i20", "generation": "GB",
    "years": [2015, 2017], "engines": ["1.25 petrol (Kappa)", "1.4 petrol (Kappa)"], "fuel": "petrol",
    "interval": {"km": 20000, "months": 12,
                 "note": "טיפול ראשון ב-15,000 ק\"מ או 12 חודשים, אחר כך כל 20,000 ק\"מ או 12 חודשים (15, 35, 55, 75...)."},
    "first_service_km": 15000, "cycle_km": 160000,
    "services": grid(GRID_15_35, ROWS_IA_GB),
    "long_interval": LONG_IA_GB,
    "time_based": [],
    "sources": [
        {"url": "https://prodmedia.colmobil.co.il/media/sites/2/2023/06/ספר-רכב-יונדאי-i20-2015-2017.pdf",
         "kind": "importer", "note": "ספר רכב i20 2015-2017 של כלמוביל, פרק 7 עמ' 12-16"},
        COLMOBIL_HUB,
    ],
    "status": "reviewed",
    "notes": "זהה במבנה ללוח של i10 2014-2019: עמודות 15/35/55... אלף ק\"מ, מסנן תא נוסעים בכל טיפול, נוזל בלמים כל טיפול שני, "
             "מסנן אוויר לסירוגין בדיקה/החלפה, מצתים כל 160,000 ק\"מ. צינור אדים, מסנן דלק וקווי דלק נבדקים ב-55,000 וב-115,000; "
             "למערכת הקירור אין מרווח קבוע בספר (בדיקת מפלס ודליפות).",
})

# --- i20 GB facelift (2018-2021): back to 15,000 grid
GRID_15 = [15000, 30000, 45000, 60000, 75000, 90000, 105000, 120000]
write({
    **HY, "id": "hyundai-i20-2018-2021", "model": "i20", "model_he": "i20", "generation": "GB facelift",
    "years": [2018, 2021], "engines": ["1.25 petrol (Kappa)", "1.0 T-GDI petrol", "1.4 petrol (Kappa)"], "fuel": "petrol",
    "interval": {"km": 15000, "months": 12}, "cycle_km": 120000,
    "services": grid(GRID_15, [
        ("engine_oil", R_ALL), ("oil_filter", R_ALL),
        ("air_filter", "IRIRIRIR"),
        ("evap_system", Q), ("vacuum_hose", EVEN),
        ("fuel_filter", "-I-R-I-R", "פריט ללא תחזוקה לפי הספר, אך מופיע בטבלה: בדיקה ב-30 והחלפה ב-60"),
        ("fuel_lines", Q),
        ("battery_12v", ALL), ("electrical_system", EVEN),
        ("brake_lines", ALL), ("pedals", EVEN), ("parking_brake", EVEN),
        ("brake_fluid", ALL, "בספר: בדיקה בכל טיפול, ללא מרווח החלפה קבוע"),
        ("brake_pads", ALL), ("brake_discs", ALL), ("brake_drums", EVEN),
        ("steering", ALL), ("cv_boots", ALL), ("tires", ALL), ("suspension", ALL), ("body_underside", ALL),
        ("ac_refrigerant", ALL), ("ac_system", ALL),
        ("cabin_filter", R_ALL),
    ]),
    "long_interval": [
        long_("drive_belt", "inspect", first_km=90000, first_months=72, then_every_km=30000, then_every_months=24,
              note="בתרגום העברי כתוב 'החלפה ראשונה'; בפועל מדובר בבדיקה והחלפה לפי מצב"),
        long_("spark_plugs", "replace", every_km=160000),
        long_("coolant", "replace", first_km=200000, first_months=120, then_every_km=40000, then_every_months=24),
        long_("dct_oil", "inspect", every_km=60000, every_months=48, note="להחליף אחרי כל נסיעה במים עמוקים"),
        long_("transmission_oil", "inspect", every_km=60000, every_months=48),
        long_("valve_clearance", "inspect", every_km=90000, every_months=72),
    ],
    "time_based": [],
    "sources": [
        {"url": "https://res.cloudinary.com/colmobil/images/v1716388440/ספר-רכב-יונדאי-i20-2018-2021_5400bf557/ספר-רכב-יונדאי-i20-2018-2021_5400bf557.pdf",
         "kind": "importer", "note": "ספר רכב i20 2018-2021 של כלמוביל, פרק 6 עמ' 12-16"},
        COLMOBIL_HUB,
    ],
    "status": "reviewed",
    "notes": "מהפייסליפט (2018) הלוח חזר למרווח קבוע של 15,000 ק\"מ. מסנן תא נוסעים בכל טיפול. מסנן אוויר לסירוגין. "
             "נוזל בלמים מופיע כבדיקה בלבד. מערכת קירור: בדיקת מפלס ודליפות, ללא מרווח קבוע.",
})

# --- i10 AC3 (2020-2021+)
write({
    **HY, "id": "hyundai-i10-2020-2025", "model": "i10", "model_he": "i10", "generation": "AC3",
    "years": [2020, 2025], "engines": ["1.0 petrol (Kappa)", "1.2 petrol (Kappa MPI)"], "fuel": "petrol",
    "interval": {"km": 15000, "months": 12}, "cycle_km": 120000,
    "services": grid(GRID_15, [
        ("engine_oil", R_ALL), ("oil_filter", R_ALL),
        ("air_filter", "IIRIIRII"),
        ("evap_system", Q), ("vacuum_hose", ALL), ("fuel_tank_air_filter", Q), ("fuel_filter", Q, "פריט ללא תחזוקה לפי הספר; בדיקה בלבד"),
        ("fuel_lines", Q),
        ("battery_12v", ALL), ("electrical_system", EVEN),
        ("brake_lines", ALL), ("pedals", EVEN), ("parking_brake", EVEN),
        ("brake_fluid", "IRIRIRIR"), ("brake_pads", ALL), ("brake_discs", ALL), ("brake_drums", EVEN),
        ("steering", ALL), ("cv_boots", EVEN), ("tires", ALL), ("suspension", ALL), ("body_underside", ALL),
        ("ac_refrigerant", ALL), ("ac_system", ALL),
        ("cabin_filter", R_ALL),
        ("manual_gearbox_oil", Q, "גם לגיר AMT; להחליף אחרי נסיעה במים עמוקים"),
        ("exhaust", EVEN),
    ]),
    "long_interval": [
        long_("drive_belt", "inspect", first_km=90000, first_months=72, then_every_km=30000, then_every_months=24),
        long_("spark_plugs", "replace", every_km=150000, every_months=120, note="מנוע 1.2 MPI"),
        long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24),
        long_("coolant", "replace", first_km=210000, first_months=120, then_every_km=30000, then_every_months=24),
    ],
    "time_based": [
        {"item": "ecall_battery", "action": "replace", "months": 36, "note": "סוללת מערכת eCall, אם מותקנת"},
    ],
    "sources": [
        {"url": "https://res.cloudinary.com/colmobil/images/v1716388493/ספר-רכב-יונדאי-i10-2020-2021_533471256/ספר-רכב-יונדאי-i10-2020-2021_533471256.pdf",
         "kind": "importer", "note": "ספר רכב i10 2020-2021 של כלמוביל, פרק 8 עמ' 9-13"},
        COLMOBIL_HUB,
    ],
    "status": "reviewed",
    "notes": "דור AC3. מרווח 15,000 ק\"מ או שנה. מסנן אוויר מוחלף כל 45,000 (בדיקה בשאר). נוזל בלמים כל 30,000. מסנן תא נוסעים בכל טיפול.",
})

# --- Elantra MD (i35) 2011-2015
write({
    **HY, "id": "hyundai-elantra-2011-2015-1.6", "model": "Elantra / i35", "model_he": "אלנטרה / i35", "generation": "MD",
    "years": [2011, 2015], "engines": ["1.6 petrol (Gamma MPI)"], "fuel": "petrol",
    "interval": {"km": 15000, "months": 12}, "cycle_km": 120000,
    "services": grid(GRID_15, [
        ("engine_oil", R_ALL), ("oil_filter", R_ALL),
        ("air_filter", "IIRIIRII"),
        ("spark_plugs", "---R---R"),
        ("drive_belt", "-----I-I"),
        ("evap_system", Q), ("vacuum_hose", ALL), ("fuel_tank_air_filter", Q), ("fuel_filter", Q, "פריט ללא תחזוקה לפי הספר; בדיקה בלבד"),
        ("fuel_lines", Q),
        ("battery_12v", ALL), ("electrical_system", EVEN),
        ("brake_lines", ALL), ("pedals", EVEN), ("parking_brake", EVEN),
        ("brake_fluid", "IRIRIRIR"), ("brake_pads", ALL), ("brake_discs", ALL),
        ("steering", ALL), ("cv_boots", EVEN), ("tires", ALL), ("suspension", ALL),
        ("ac_refrigerant", ALL), ("ac_system", ALL),
        ("cabin_filter", "-R-R-R-R"),
        ("exhaust", EVEN),
    ]),
    "long_interval": [
        long_("valve_clearance", "inspect", every_km=90000, every_months=48),
        long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24),
        long_("coolant", "replace", first_km=210000, first_months=120, then_every_km=30000, then_every_months=24),
    ],
    "time_based": [],
    "sources": [
        {"url": "https://res.cloudinary.com/colmobil/images/v1716388110/ספר-רכב-יונדאי-אלנטרה-היברידית-2011-2015_5602d83f9/ספר-רכב-יונדאי-אלנטרה-היברידית-2011-2015_5602d83f9.pdf",
         "kind": "importer", "note": "ספר רכב אלנטרה MD 2011-2015 של כלמוביל (בשם הקובץ כתוב 'היברידית' בטעות), פרק 7 עמ' 8-13. הלוח מוצג לפי טיפול"},
        COLMOBIL_HUB,
    ],
    "status": "reviewed",
    "notes": "בישראל נמכר כ-i35. מצתים כל 60,000. מסנן תא נוסעים ונוזל בלמים כל 30,000. מסנן אוויר כל 45,000. שמן גיר אוטומטי: ללא טיפול לפי הספר.",
})

# --- Elantra AD 2016-2018 and AD facelift 2019-2020
ROWS_AD = [
    ("engine_oil", R_ALL), ("oil_filter", R_ALL),
    ("air_filter", "IIRIIRII"),
    ("evap_system", Q), ("vacuum_hose", ALL), ("fuel_tank_air_filter", Q),
    ("fuel_lines", Q),
    ("battery_12v", ALL),
    ("brake_lines", ALL), ("pedals", EVEN), ("parking_brake", EVEN),
    ("brake_fluid", ALL, "בספר: בדיקה בכל טיפול, ללא מרווח החלפה קבוע"),
    ("brake_pads", ALL), ("brake_discs", ALL),
    ("steering", ALL), ("cv_boots", EVEN), ("tires", ALL), ("suspension", ALL), ("body_underside", ALL),
    ("ac_refrigerant", ALL), ("ac_system", ALL),
    ("cabin_filter", "-R-R-R-R"),
    ("exhaust", EVEN),
]
LONG_AD = [
    long_("drive_belt", "inspect", first_km=90000, first_months=72, then_every_km=30000, then_every_months=24),
    long_("valve_clearance", "inspect", every_km=90000, note="מנוע Gamma 1.6; בטבלה מסומנת בדיקה אחת בלבד"),
    long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24),
    long_("coolant", "replace", first_km=210000, first_months=120, then_every_km=30000, then_every_months=24),
]
write({
    **HY, "id": "hyundai-elantra-2016-2018-1.6", "model": "Elantra", "model_he": "אלנטרה", "generation": "AD",
    "years": [2016, 2018], "engines": ["1.6 petrol (Gamma MPI)"], "fuel": "petrol",
    "interval": {"km": 15000, "months": 12}, "cycle_km": 120000,
    "services": grid(GRID_15, ROWS_AD),
    "long_interval": LONG_AD + [long_("spark_plugs", "replace", every_km=165000)],
    "time_based": [],
    "sources": [
        {"url": "https://res.cloudinary.com/colmobil/images/v1716388126/ספר-רכב-יונדאי-אלנטרה-היברידית-2016-2018_55994207d/ספר-רכב-יונדאי-אלנטרה-היברידית-2016-2018_55994207d.pdf",
         "kind": "importer", "note": "ספר רכב אלנטרה AD 2016-2018 של כלמוביל, פרק 6 עמ' 8-11 (טבלת 'לאירופה')"},
        COLMOBIL_HUB,
    ],
    "status": "reviewed",
    "notes": "מצתים כל 165,000. מסנן אוויר כל 45,000. מסנן תא נוסעים כל 30,000. שמן גיר אוטומטי: ללא טיפול לפי הספר. נוזל בלמים: בדיקה בלבד בטבלה.",
})
write({
    **HY, "id": "hyundai-elantra-2019-2020-1.6", "model": "Elantra", "model_he": "אלנטרה", "generation": "AD facelift",
    "years": [2019, 2020], "engines": ["1.6 petrol (Gamma MPI)"], "fuel": "petrol",
    "interval": {"km": 15000, "months": 12}, "cycle_km": 120000,
    "services": grid(GRID_15, ROWS_AD),
    "long_interval": LONG_AD + [long_("spark_plugs", "replace", every_km=60000, note="לפי ספר 2019-2021: כל 60,000 ק\"מ (בדור הקודם 165,000)")],
    "time_based": [],
    "sources": [
        {"url": "https://res.cloudinary.com/colmobil/images/v1716388120/ספר-רכב-יונדאי-אלנטרה-היברידית-2019-2021_56006ad7c/ספר-רכב-יונדאי-אלנטרה-היברידית-2019-2021_56006ad7c.pdf",
         "kind": "importer", "note": "ספר רכב אלנטרה 2019-2021 של כלמוביל (בשם הקובץ 'היברידית' בטעות; הטבלה למנוע בנזין), פרק 6 עמ' 8-11"},
        COLMOBIL_HUB,
    ],
    "status": "reviewed",
    "notes": "כמו AD 2016-2018 חוץ ממצתים (60,000). דור CN7 ההיברידי מ-2021 דורש קובץ נפרד.",
})

# --- Ioniq AE hybrid 2016-2022
write({
    **HY, "id": "hyundai-ioniq-2016-2022-1.6-hybrid", "model": "Ioniq", "model_he": "איוניק", "generation": "AE",
    "years": [2016, 2022], "engines": ["1.6 GDI hybrid (Kappa)"], "fuel": "hybrid",
    "interval": {"km": 15000, "months": 12}, "cycle_km": 120000,
    "services": grid(GRID_15, [
        ("engine_oil", R_ALL), ("oil_filter", R_ALL),
        ("air_filter", "IIRIIRII"),
        ("hsg_belt", "IIIIIIRI", "בדיקה בכל טיפול, החלפה כל 105,000 ק\"מ או 48 חודשים"),
        ("evap_system", Q), ("vacuum_hose", ALL), ("fuel_tank_air_filter", Q), ("fuel_filter", Q, "פריט ללא תחזוקה לפי הספר; בדיקה בלבד"),
        ("fuel_lines", Q),
        ("dct_oil", Q),
        ("clutch_actuator_fluid", "IRIRIRIR"),
        ("battery_12v", ALL),
        ("brake_lines", ALL), ("pedals", EVEN), ("parking_brake", EVEN),
        ("brake_fluid", "IRIRIRIR"), ("brake_pads", ALL), ("brake_discs", ALL),
        ("steering", ALL), ("cv_boots", EVEN), ("tires", ALL), ("suspension", ALL), ("body_underside", ALL),
        ("ac_refrigerant", ALL), ("ac_system", ALL),
        ("cabin_filter", "-R-R-R-R"),
        ("exhaust", EVEN),
    ]),
    "long_interval": [
        long_("spark_plugs", "replace", every_km=165000),
        long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24),
        long_("coolant", "replace", first_km=210000, first_months=120, then_every_km=30000, then_every_months=24,
              note="נוזל קירור מנוע ונוזל קירור ממיר (אינוורטר)"),
    ],
    "time_based": [],
    "sources": [
        {"url": "https://res.cloudinary.com/colmobil/images/v1738680462/IONIQ_2016-2018_heb/IONIQ_2016-2018_heb.pdf",
         "kind": "importer", "note": "ספר רכב איוניק 2016-2018 של כלמוביל, פרק 6 עמ' 8-12"},
        {"url": "https://res.cloudinary.com/colmobil/images/v1738680477/IONIQ_2019-heb/IONIQ_2019-heb.pdf",
         "kind": "importer", "note": "ספר רכב איוניק 2019: אותה טבלה"},
        COLMOBIL_HUB,
    ],
    "status": "reviewed",
    "notes": "היברידי בלבד (לא פלאג-אין ולא חשמלי). רצועת HSG (מתנע-גנרטור) היא הפריט הייחודי. נוזל בלמים ונוזל מפעיל מצמד כל 30,000. "
             "מסנן אוויר כל 45,000. מסנן תא נוסעים כל 30,000.",
})

# ---------------------------------------------------------------------------
# Kia (טלקאר). Books: https://kia-israel.co.il/קבל-ספר-רכב-למייל
# ---------------------------------------------------------------------------
KIA = {"make": "Kia", "make_he": "קיה", "importer": "טלקאר"}
KIA_HUB = {"url": "https://kia-israel.co.il/קבל-ספר-רכב-למייל", "kind": "importer",
           "note": "ספריית ספרי הרכב של קיה ישראל (cdnmedia.kia-israel.co.il/www/cars-book/)"}

# Picanto JA: the 2017 book and the 2021 book (Smartstream engines) print the same table except the
# drive belt: replace first at 90,000 in the 2017 book, inspect first at 90,000 in the 2021 book.
def picanto_ja(id_, gen, years, engines, belt, sources, notes_extra):
  write({
    **KIA, "id": id_, "model": "Picanto", "model_he": "פיקנטו", "generation": gen,
    "years": years, "engines": engines, "fuel": "petrol",
    "interval": {"km": 15000, "months": 12}, "cycle_km": 120000,
    "services": grid(GRID_15, [
        ("engine_oil", R_ALL), ("oil_filter", R_ALL),
        ("air_filter", "-I-R-I-R"),
        ("vacuum_hose", EVEN),
        ("valve_clearance", "-----I--", "מנועי 1.0 בלבד"),
        ("transmission_oil", Q), ("manual_gearbox_oil", Q, "להחליף אחרי נסיעה במים עמוקים"),
        ("cv_boots", EVEN),
        ("evap_system", Q), ("fuel_tank_air_filter", Q), ("fuel_lines", Q),
        ("intercooler_pipes", ALL, "מנוע 1.0 T-GDI בלבד"),
        ("exhaust", ALL),
        ("ac_refrigerant", ALL), ("ac_system", ALL),
        ("cabin_filter", "-R-R-R-R"),
        ("brake_pads", ALL), ("brake_discs", ALL), ("brake_drums", EVEN), ("brake_lines", ALL),
        ("brake_fluid", "IRIRIRIR"), ("parking_brake", EVEN),
        ("steering", ALL), ("suspension", ALL), ("tires", ALL), ("battery_12v", ALL),
    ]),
    "long_interval": [
        long_("coolant", "replace", first_km=210000, first_months=120, then_every_km=30000, then_every_months=24),
        belt,
        long_("spark_plugs", "replace", every_km=150000, note="מנועי 1.0 MPI ו-1.2 MPI. מנוע 1.0 T-GDI: כל 75,000 ק\"מ"),
        long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24),
    ],
    "time_based": [],
    "sources": sources + [KIA_HUB],
    "status": "reviewed",
    "notes": "מסנן תא נוסעים ונוזל בלמים כל 30,000 לפי הספר (מוסכים בישראל נוהגים להחליף מסנן מזגן בכל טיפול בגלל אבק). "
             "מסנן אוויר: בדיקה ב-30, החלפה ב-60. תוסף דלק כל 15,000 אם הבנזין בלי תוספים. " + notes_extra,
  })
SPECS["kia-picanto-2021-2025"] = SPECS["kia-picanto-2017-2025"]
picanto_ja("kia-picanto-2017-2025", "JA", [2017, 2021], ["1.0 MPI (Kappa)", "1.25 MPI (Kappa, G4LA)", "1.0 T-GDI (Kappa)"],
           long_("drive_belt", "replace", first_km=90000, first_months=72, then_every_km=30000, then_every_months=24,
                 note="לפי הספר: החלפה ראשונה ב-90,000, אחר כך כל 30,000; בפועל בדיקה והחלפה לפי מצב"),
           [{"url": "https://kia-israel.co.il/wp-content/uploads/2020/11/ספר-רכב-Picanto_OM_2017-.pdf",
             "kind": "importer", "note": "ספר רכב פיקנטו 2017+ של קיה ישראל, פרק 8 עמ' 11-17"},
            {"url": "https://cdnmedia.kia-israel.co.il/www/cars-book/Picanto-JA-2017-2020.pdf", "kind": "importer", "note": "אותו ספר בספריית cars-book"}],
           "מנועי Kappa (G4LA/G3LA), כולל רכבי 2021 עם מנוע G4LA. מנועי Smartstream (מ-2021) בלוח kia-picanto-2021-2025, "
           "כי בספר 2021 רצועת ההנעה נבדקת (לא מוחלפת) ב-90,000. שם הקובץ נשאר עם 2025 כדי לא לשבור קישורים קיימים.")
picanto_ja("kia-picanto-2021-2025", "JA facelift", [2021, 2025], ["1.0 MPI (Smartstream G1.0)", "1.2 MPI (Smartstream G1.2, G4LF)", "1.0 T-GDi (Smartstream G1.0)"],
           long_("drive_belt", "inspect", first_km=90000, first_months=72, then_every_km=30000, then_every_months=24),
           [{"url": "https://cdnmedia.kia-israel.co.il/www/cars-book/Picanto-AMT-2021.pdf", "kind": "importer",
             "note": "ספר רכב פיקנטו 2021+ של קיה ישראל, פרק 8 עמ' 15-17: תכנית תחזוקה רגילה, מנוע בנזין (רצועת ההנעה בעמ' 8-16)"}],
           "מנועי Smartstream מהפייסליפט של 2021. הטבלה זהה לספר 2017, חוץ מרצועת ההנעה: בדיקה ראשונה ב-90,000 ק\"מ או 72 חודשים, ואחר כך בדיקה כל 30,000 או 24 חודשים.")

# Sportage QL: the book grid is 30,000 km / 24 months (European). For the
# common 1.6 GDI the book itself says 15,000/12 months under severe use, and
# the T-GDI/2.0/2.4 engines are 15,000/12 months in the normal table. The
# Israeli importer services every 15,000/12 months. So: 15k grid, and the
# 30k-column items land on the even services.
GRID_15_240 = [15000 * i for i in range(1, 17)]
def ql_rows(cabin, brake_fluid, drive_belt_pattern):
    # patterns are 16 chars: odd services (15k) only oil; book columns map to even services
    e = lambda p8: "".join("-" + c for c in p8)      # spread an 8-column pattern onto 16 services
    return [
        ("engine_oil", "R" * 16), ("oil_filter", "R" * 16),
        ("air_filter", e("IRIRIRIR")),
        ("ac_refrigerant", e(ALL)), ("ac_system", e(ALL)),
        ("battery_12v", e(ALL)),
        ("brake_pads", e(ALL)), ("brake_discs", e(ALL)), ("brake_lines", e(ALL)),
        ("brake_fluid", e(brake_fluid)),
        ("cabin_filter", e(cabin)),
        ("differential_oil", e(EVEN), "AWD בלבד"), ("transfer_case_oil", e(EVEN), "AWD בלבד"),
        ("propshaft", e(ALL), "גל ההינע האחורי, AWD בלבד"),
        ("drive_belt", e(drive_belt_pattern)),
        ("cv_boots", e(ALL)),
        ("dct_oil", e(EVEN)), ("manual_gearbox_oil", e(EVEN)),
        ("exhaust", e(ALL)),
        ("fuel_lines", e(EVEN)), ("fuel_tank_air_filter", e(EVEN)), ("evap_system", e(EVEN)),
        ("parking_brake", e(ALL)),
        ("steering", e(ALL)), ("suspension", e(ALL)), ("tires", e(ALL)),
        ("vacuum_hose", e(ALL)),
        ("valve_clearance", e("--I--I--"), "מנועי 1.6 GDI, 1.6 T-GDI ו-2.4 GDI בלבד (לא 2.0 MPI)"),
    ]
LONG_QL = [
    long_("coolant", "replace", first_km=210000, first_months=120, then_every_km=30000, then_every_months=24),
    long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24),
    long_("spark_plugs", "replace", every_km=150000, every_months=120,
          note="מנועי 1.6 GDI, 2.0 MPI, 2.4 GDI. מנוע 1.6 T-GDI: כל 75,000 ק\"מ או 60 חודשים"),
    # automatic gearbox fluid: the book says no inspection or service; replace every 90,000 only under severe
    # use. Severe-use items are not schedule entries, so it is in QL_NOTE only.
]
QL_NOTE = ("הטבלה בספר בנויה בעמודות של 30,000 ק\"מ / 24 חודשים (תוכנית אירופית). למנוע 1.6 GDI הספר עצמו קובע 15,000 ק\"מ או 12 חודשים "
           "בתנאי הפעלה קשים (אבק, חום, עצור-וסע), ולמנועי T-GDI/2.0/2.4 15,000 גם בטבלה הרגילה. היבואן מטפל כל 15,000 או שנה. "
           "לכן הקובץ בנוי על רשת 15,000: בטיפולי הביניים שמן ומסנן בלבד, והפריטים מהטבלה נופלים על הטיפולים הזוגיים. "
           "נוזל גיר אוטומטי: לפי הספר אין צורך בבדיקה או בטיפול; רק בתנאי הפעלה קשים החלפה כל 90,000 ק\"מ. "
           "מרווח שסתומים (90,000 ו-180,000) למנועי 1.6 GDI, 1.6 T-GDI ו-2.4 GDI בלבד. גל ההינע האחורי (AWD) נבדק בכל עמודה.")
write({
    **KIA, "id": "kia-sportage-2016-2018", "model": "Sportage", "model_he": "ספורטאז'", "generation": "QL",
    "years": [2016, 2018], "engines": ["1.6 GDI (Gamma)", "1.6 T-GDI (Gamma)", "2.0 MPI (Nu)", "2.4 GDI (Theta II)"], "fuel": "petrol",
    "interval": {"km": 15000, "months": 12, "note": "רשת 15,000 של היבואן; בספר עמודות של 30,000, ראה notes"},
    "cycle_km": 240000,
    "services": grid(GRID_15_240, ql_rows(cabin="IRIRIRIR", brake_fluid="IRIRIRIR", drive_belt_pattern="--I-I-I-")),
    "long_interval": LONG_QL,
    "time_based": [],
    "sources": [
        {"url": "https://cdnmedia.kia-israel.co.il/www/cars-book/Sportage-QLe-2016-2018.pdf",
         "kind": "importer", "note": "ספר רכב ספורטאז' 2016-2018 של קיה ישראל, פרק 8 עמ' 11-18"},
        KIA_HUB,
    ],
    "status": "reviewed",
    "notes": QL_NOTE + " בספר 2016-2018: מסנן תא נוסעים ונוזל בלמים בדיקה ב-30 והחלפה ב-60 (כל 60,000). רצועת הינע: בדיקה ראשונה ב-90,000, אחר כך כל 60,000.",
})
write({
    **KIA, "id": "kia-sportage-2019-2021", "model": "Sportage", "model_he": "ספורטאז'", "generation": "QL facelift",
    "years": [2019, 2021], "engines": ["1.6 GDI (Gamma)", "1.6 T-GDI (Gamma)", "2.0 MPI (Nu)", "2.4 GDI (Theta II)"], "fuel": "petrol",
    "interval": {"km": 15000, "months": 12, "note": "רשת 15,000 של היבואן; בספר עמודות של 30,000, ראה notes"},
    "cycle_km": 240000,
    "services": grid(GRID_15_240, ql_rows(cabin=R_ALL, brake_fluid=R_ALL, drive_belt_pattern=ALL)),
    "long_interval": LONG_QL,
    "time_based": [],
    "sources": [
        {"url": "https://kia-israel.co.il/wp-content/uploads/2020/11/ספר-רכב-Sportage_PE_OM_4-3-2019_OPT.pdf",
         "kind": "importer", "note": "ספר רכב ספורטאז' 2019-2021 של קיה ישראל, פרק 8 עמ' 13-21"},
        {"url": "https://cdnmedia.kia-israel.co.il/www/cars-book/Sportage-QLe-2019-2021.pdf", "kind": "importer", "note": "אותו ספר בספריית cars-book"},
        KIA_HUB,
    ],
    "status": "reviewed",
    "notes": QL_NOTE + " בספר 2019-2021: מסנן תא נוסעים ונוזל בלמים מוחלפים בכל עמודה (כל 30,000). רצועת הינע נבדקת בכל עמודה.",
})

# --- Niro DE hybrid (2016-2022)
ROWS_NIRO = [
    ("engine_oil", R_ALL), ("oil_filter", R_ALL),
    ("vacuum_hose", ALL),
    ("dct_oil", Q),
    ("clutch_actuator_fluid", "IRIRIRIR"),
    ("cv_boots", EVEN),
    ("fuel_lines", Q), ("fuel_tank_air_filter", Q), ("evap_system", Q),
    ("air_filter", "IIRIIRII"),
    ("exhaust", EVEN),
    ("ac_refrigerant", ALL), ("ac_system", ALL),
    ("cabin_filter", "-R-R-R-R"),
    ("brake_lines", ALL), ("brake_fluid", "IRIRIRIR"), ("parking_brake", EVEN),
    ("steering", ALL), ("tires", ALL), ("suspension", ALL), ("battery_12v", ALL),
    ("brake_pads", ALL), ("brake_discs", ALL),
]
LONG_NIRO = [
    long_("coolant", "replace", first_km=210000, first_months=120, then_every_km=30000, then_every_months=24,
          note="נוזל קירור מנוע ומערכת היברידית"),
    long_("spark_plugs", "replace", every_km=150000, every_months=120),
    long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24),
]
write({
    **KIA, "id": "kia-niro-2016-2022-1.6-hybrid", "model": "Niro", "model_he": "נירו", "generation": "DE",
    "years": [2016, 2022], "engines": ["1.6 GDI hybrid (Kappa)"], "fuel": "hybrid",
    "interval": {"km": 15000, "months": 12}, "cycle_km": 120000,
    "services": grid(GRID_15, ROWS_NIRO + [
        ("hsg_belt", "IIIIIIRI", "בדיקה בכל טיפול; בספר 2019+ החלפה ב-105,000. בספר 2016-2018 בדיקה בלבד (החלפה כל 45,000 בתנאים קשים)"),
    ]),
    "long_interval": LONG_NIRO,
    "time_based": [],
    "sources": [
        {"url": "https://cdnmedia.kia-israel.co.il/www/cars-book/Niro-2016-2018.pdf", "kind": "importer", "note": "ספר רכב נירו 2016-2018 של קיה ישראל, פרק 8 עמ' 10-15"},
        {"url": "https://cdnmedia.kia-israel.co.il/www/cars-book/Niro-2019.pdf", "kind": "importer", "note": "ספר רכב נירו 2019+ (פייסליפט), פרק 7 עמ' 12-16"},
        {"url": "https://kia-israel.co.il/wp-content/uploads/2020/11/ספר-רכב-Kia_Niro_Facelift.pdf", "kind": "importer", "note": "אותו ספר פייסליפט"},
        KIA_HUB,
    ],
    "status": "reviewed",
    "notes": "היברידי בלבד (לא פלאג-אין/חשמלי). נוזל בלמים ונוזל מפעיל מצמד כל 30,000. מסנן אוויר כל 45,000. מסנן תא נוסעים כל 30,000. "
             "רצועת HSG (מתנע-גנרטור) נבדקת בכל טיפול. תוסף דלק כל 15,000 אם הבנזין בלי תוספים.",
})

# ---------------------------------------------------------------------------
# Mazda (דלק מוטורס). Plans: https://www.mazda.co.il/service-plans
# Each plan is a one-page PDF (SharePoint) listing the parts replaced and
# their interval. It lists parts only, no inspection rows, so these files
# carry replacements only.
# ---------------------------------------------------------------------------
MZ = {"make": "Mazda", "make_he": "מאזדה", "importer": "דלק מוטורס"}
MZ_PAGE = {"url": "https://www.mazda.co.il/service-plans", "kind": "importer",
           "note": "טופס 'תוכנית טיפול' של דלק מוטורס; הקישורים ל-PDF לפי דגם ושנה מוטמעים בדף (modelList). טיפול כשמופיעה התראה בלוח, אחרי 15,000 ק\"מ או אחרי שנה, המוקדם"}
MZ_NOTE = ("תוכנית היבואן מפרטת רק חלקים להחלפה ומרווחיהם (אין שורות בדיקה), ולכן הקובץ מכיל החלפות בלבד. "
           "בכל טיפול המוסך בודק בלמים, צמיגים, נוזלים ותאורה כמקובל. שמן מנוע 5W-30; נוזל קירור Mazda FL22; נוזל בלמים DOT4.")
LONG_MZ = [
    long_("coolant", "replace", first_km=195000, first_months=120, then_every_km=90000, then_every_months=60),
    long_("spark_plugs", "replace", every_km=120000, every_months=72),
    long_("fuel_filter", "replace", every_km=135000),
]
def mazda(id_, model, model_he, gen, years, engines, cabin, brake, air, url, fname, extra_note="", plan_years="", long=None):
    write({
        **MZ, "id": id_, "model": model, "model_he": model_he, "generation": gen, "years": years,
        "engines": engines, "fuel": "petrol",
        "interval": {"km": 15000, "months": 12, "note": "התראה בלוח המחוונים, 15,000 ק\"מ או 12 חודשים, המוקדם"},
        "cycle_km": 120000,
        "services": grid(GRID_15, [
            ("engine_oil", R_ALL), ("oil_filter", R_ALL),
            ("cabin_filter", cabin),
            ("brake_fluid", brake),
            ("air_filter", air),
        ]),
        "long_interval": LONG_MZ if long is None else long,
        "time_based": [],
        "sources": [
            {"url": url, "kind": "importer", "note": f"PDF תוכנית טיפול '{fname}' ({plan_years}) של דלק מוטורס, קישור SharePoint מתוך הדף"},
            MZ_PAGE,
        ],
        "status": "reviewed",
        "notes": MZ_NOTE + extra_note,
    })

SP = "https://delekmotorscoil.sharepoint.com/:b:/s/Techtrain/"
mazda("mazda-3-2013-2019", "3", "3", "BM/BN", [2013, 2019], ["1.5 Skyactiv-G", "2.0 Skyactiv-G"],
      cabin=R_ALL, brake="-R-R-R-R", air="---R---R",
      url=SP + "EaVNAnCBgNRHlc6acl9we6UBhHGiBOrgZKCJuGT5jIYjrA?download=1", fname="38646 _Mazda3_2013_2019.pdf", plan_years="שנות ייצור 2013-2019",
      extra_note=" מסנן מזגן בכל טיפול; נוזל בלמים כל שנתיים; מסנן אוויר כל 60,000; מצתים 120,000 או 6 שנים; מסנן דלק 135,000; נוזל קירור ראשון 195,000/10 שנים ואז כל 90,000/5 שנים.")
mazda("mazda-3-2020-2025", "3", "3", "BP", [2020, 2025], ["2.0 Skyactiv-G"],
      cabin="-R-R-R-R", brake="-R-R-R-R", air="---R---R",
      url=SP + "ESEJodI9CZ5IkBMfgv7OUsIB7ne1Z6AmFG4vtGtILgSoSQ?download=1", fname="38646 _Mazda3_2020_And_Above.pdf", plan_years="שנת ייצור 2020 ומעלה",
      extra_note=" בתוכנית 2020+: מסנן מזגן ונוזל בלמים כל טיפול שני, מסנן אוויר כל טיפול רביעי, מצתים 120,000, מסנן דלק 135,000. שמן API-SN Plus.")
mazda("mazda-2-2015-2025", "2", "2", "DJ", [2015, 2025], ["1.5 Skyactiv-G"],
      cabin=R_ALL, brake="-R-R-R-R", air="---R---R",
      url=SP + "EcGRp40i_QdGg50djwMw1zQBj5GjoZJHYnwUncbxuAJGHg?download=1", fname="38646 _Mazda2_2015_And_Up.pdf", plan_years="שנת ייצור 2015 ומעלה",
      extra_note=" זהה לתוכנית מאזדה 3 2013-2019: מסנן מזגן בכל טיפול, נוזל בלמים כל שנתיים, מסנן אוויר 60,000, מצתים 120,000/6 שנים, מסנן דלק 135,000.")
mazda("mazda-cx-5-2012-2025", "CX-5", "CX-5", "KE/KF", [2012, 2025], ["2.0 Skyactiv-G", "2.5 Skyactiv-G"],
      cabin=R_ALL, brake="-R-R-R-R", air="---R---R",
      url=SP + "EZE5m_k2Q69HldzGWxQc_DkBm9IFQTI7GQXksJJcxKBIFw?download=1", fname="38646 _Mazda_CX-5_2012_And_Above.pdf", plan_years="שנות ייצור 2012-2025",
      extra_note=" מסנן מזגן בכל טיפול, נוזל בלמים כל שנתיים, מסנן אוויר 60,000 או 4 שנים, מצתים 120,000/6 שנים, מסנן דלק 135,000. ב-AWD: שמן תיבת העברה וסרן אחורי 80W-90 GL-5 (ללא מרווח בתוכנית).")

mazda("mazda-3-2006-2012", "3", "3", "BK/BL", [2006, 2012], ["1.6 MZR", "2.0 MZR"],
      cabin="-R-R-R-R", brake="-R-R-R-R", air="---R---R",
      url=SP + "EUWjI7QSL4VFvtiiMXDoVX8B12h7-TbHYd1PAXx2mEhOwA?download=1", fname="38646 _Mazda3_2003_2012.pdf", plan_years="שנות ייצור 2003-2012",
      extra_note=" תוכנית 2003-2012: מסנן מזגן ונוזל בלמים כל 30,000 או שנתיים, מסנן אוויר 60,000. מצתים רגילים 45,000, מצתי אירידיום 120,000, בלי מגבלת זמן. "
                 "מסנן דלק: 75,000 עד שלדה 133398, 45,000 משלדה 1333399 (כך בתוכנית). הלוח מציג 45,000 לשני הפריטים כי לפיהם אין סיכון: "
                 "ברכב עם מצתי אירידיום, או עם שלדה עד 133398 למסנן הדלק, אפשר לדחות ל-120,000 ול-75,000 (הערה בפריט). שמן גיר Mazda V, שמן הגה Dexron III. "
                 "רכבי 2013 עם מנוע LF/Z6 (MZR) שייכים לתוכנית הזאת.",
      long=[LONG_MZ[0],
            long_("spark_plugs", "replace", every_km=45000, note="מצתים רגילים כל 45,000 ק\"מ; מצתי אירידיום כל 120,000 ק\"מ"),
            long_("fuel_filter", "replace", every_km=45000, note="לפי מספר השלדה: עד שלדה 133398 כל 75,000 ק\"מ, ובשלדות מאוחרות יותר כל 45,000 ק\"מ")])
mazda("mazda-2-2007-2014", "2", "2", "DE", [2007, 2015], ["1.3 MZR", "1.5 MZR"],
      cabin="-R-R-R-R", brake="-R-R-R-R", air="---R---R",
      url=SP + "EUleFfkd1mlPn3fX15es5HcBszPOYXuLiARcad4pgYFKjA?download=1", fname="38646 _Mazda2_2007_2014.pdf", plan_years="שנות ייצור 2007-2015",
      extra_note=" תוכנית 2007-2015 (שם הקובץ 2007_2014, הכותרת בתוכנית עד שנת ייצור 2015): מסנן מזגן ונוזל בלמים כל 30,000 או שנתיים, מסנן אוויר 60,000, "
                 "מצתי אירידיום 120,000 או 3 שנים, מסנן דלק 135,000. רכבי 2015 עם מנוע ZY (הדור הקודם) שייכים לתוכנית הזאת.",
      long=[LONG_MZ[0], long_("spark_plugs", "replace", every_km=120000, every_months=36), LONG_MZ[2]])
mazda("mazda-cx-3-2017-2025", "CX-3", "CX-3", "DK", [2017, 2025], ["2.0 Skyactiv-G"],
      cabin=R_ALL, brake="-R-R-R-R", air="---R---R",
      url=SP + "ESf1wJ_qhjZJt0RLzivAgHYBkr5k4bDwTvwspkHFBK515w?download=1", fname="38646 _Mazda_CX-3_2017_And_Above.pdf", plan_years="שנת ייצור 2017 ומעלה",
      extra_note=" זהה לתוכנית CX-5: מסנן מזגן בכל טיפול, נוזל בלמים כל שנתיים, מסנן אוויר 60,000 או 4 שנים, מצתים 120,000/6 שנים, מסנן דלק 135,000.")
mazda("mazda-cx-30-2020-2025", "CX-30", "CX-30", "DM", [2020, 2025], ["2.0 Skyactiv-G"],
      cabin="-R-R-R-R", brake="-R-R-R-R", air="---R---R",
      url=SP + "Eb5FcNyL7vlApQPossE106MBq2aV1oBzzVXKBrqC9_tuSA?download=1", fname="38646 _Mazda_CX-30_2020_And_Above.pdf", plan_years="שנת ייצור 2020 ומעלה",
      extra_note=" זהה לתוכנית מאזדה 3 2020+: מסנן מזגן ונוזל בלמים כל טיפול שני, מסנן אוויר כל טיפול רביעי, מצתים 120,000, מסנן דלק 135,000. שמן API-SN Plus.")

# --- Kia Picanto TA (2011-2016) and Sportage SL (2011-2015): older books use a
# custom font; decoded with a fixed byte offset (see SOURCES.md).
SPECS["kia-picanto-2011-2016"] = {"_note": CHECKED,
   "engine_oil": "API SM / ILSAC GF-4 ומעלה; היבואן ממליץ PAZ Power K 5W-40", "oil_capacity": "1.0: 2.9 ליטר; 1.25: 3.6 ליטר (ריקון ומילוי)",
   "coolant": "אתילן גליקול למקרן אלומיניום, 5.1 ליטר", "brake_fluid": "DOT 3 או DOT 4 (FMVSS116), 0.7-0.8 ליטר",
   "fuel": "בנזין 95 אוקטן, מיכל 35 ליטר", "tires": "155/70 R13, 165/60 R14 או 175/50 R15; חלופי T105/70 D14",
   "tire_pressure": "2.3 בר (33 psi) קדמי, 2.1 בר (31 psi) אחורי; בעומס מלא 2.5/2.5; חלופי 4.2 בר",
   "battery": "מצבר רגיל 12V, לוודא מידה מול הקיים", "timing": "שרשרת, ללא החלפה מתוכננת", "spare": "גלגל חלופי צר T105/70 D14", "warranty": KIA_WARRANTY}
SPECS["kia-sportage-2011-2015"] = {"_note": CHECKED,
   "engine_oil": "API SM (או SL) / ILSAC GF-4 ומעלה, 5W-30", "oil_capacity": "2.0: 4.1 ליטר; 2.4: 4.6 ליטר (ריקון ומילוי)",
   "coolant": "אתילן גליקול למקרן אלומיניום; ידני 6.8 ליטר, אוטומטי 6.7 ליטר", "brake_fluid": "DOT 3 או DOT 4 (FMVSS116), 0.7-0.8 ליטר; נוזל הגה כוח PSF-3, 1.0 ליטר",
   "fuel": "בנזין 95 אוקטן, מיכל 55 ליטר", "tires": "215/70 R16, 225/60 R17 או 235/55 R18; חלופי T155/90 R16",
   "tire_pressure": "2.3 בר (33 psi) קדמי ואחורי; בעומס מלא 2.6/2.9 בר; חלופי 4.2 בר",
   "battery": "מצבר רגיל 12V, לוודא מידה מול הקיים", "timing": "שרשרת, ללא החלפה מתוכננת", "spare": "גלגל חלופי צר T155/90 R16 (אם קיים)", "warranty": KIA_WARRANTY}
write({
    **KIA, "id": "kia-picanto-2011-2016", "model": "Picanto", "model_he": "פיקנטו", "generation": "TA",
    "years": [2011, 2016], "engines": ["1.0 MPI (Kappa)", "1.25 MPI (Kappa)"], "fuel": "petrol",
    "interval": {"km": 15000, "months": 12}, "cycle_km": 120000,
    "services": grid(GRID_15, [
        ("engine_oil", R_ALL), ("oil_filter", R_ALL),
        ("air_filter", "IIRIIRII"),
        ("cabin_filter", ALL, "בספר: בדיקה בכל טיפול, החלפה לפי מצב (בתנאי אבק: להחליף)"),
        ("spark_plugs", "---R---R"),
        ("drive_belt", EVEN), ("cv_boots", EVEN),
        ("fuel_filter", "-I-R-I-R"), ("fuel_lines", Q), ("evap_system", Q),
        ("transmission_oil", Q), ("manual_gearbox_oil", Q),
        ("battery_12v", ALL), ("ac_refrigerant", ALL), ("ac_system", ALL),
        ("brake_fluid", ALL, "בספר: בדיקת מפלס בכל טיפול; בתנאים קשים החלפה"), ("brake_pads", ALL), ("brake_discs", ALL), ("brake_lines", ALL),
        ("parking_brake", ALL), ("exhaust", ALL), ("suspension", ALL), ("steering", ALL), ("tires", ALL),
    ]),
    "long_interval": [
        long_("valve_clearance", "inspect", every_km=95000, every_months=48),
        long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24),
        long_("coolant", "replace", first_km=210000, first_months=120, then_every_km=30000, then_every_months=24),
    ],
    "time_based": [],
    "sources": [
        {"url": "https://cdnmedia.kia-israel.co.il/www/cars-book/Picanto-2011-2016.pdf", "kind": "importer",
         "note": "ספר רכב פיקנטו 2011-2016 של קיה ישראל, פרק 7 עמ' 8-19. הטבלה מוצגת לפי טיפול. הפונט מקודד, פוענח (היסט 0x9c)"},
        KIA_HUB,
    ],
    "status": "reviewed",
    "notes": "דור TA. מצתים כל 60,000. מסנן אוויר כל 45,000. מסנן דלק: בדיקה ב-30, החלפה ב-60. מסנן מזגן ונוזל בלמים מופיעים כבדיקה בלבד. "
             "תוסף דלק כל 15,000. יש גם טבלה נפרדת לגרסת גפ\"מ (Bi-Fuel) שלא הועתקה.",
})
write({
    **KIA, "id": "kia-sportage-2011-2015", "model": "Sportage", "model_he": "ספורטאז'", "generation": "SL",
    "years": [2010, 2015], "engines": ["2.0 MPI (Theta II)", "2.4 GDI (Theta II)"], "fuel": "petrol",
    "interval": {"km": 15000, "months": 12}, "cycle_km": 120000,
    "services": grid(GRID_15, [
        ("drive_belt", EVEN),
        ("engine_oil", R_ALL), ("oil_filter", R_ALL),
        ("air_filter", "IIRIIRII", "בספר: למזרח התיכון החלפה בכל טיפול; לשאר השווקים החלפה כל 45,000"),
        ("evap_system", Q), ("fuel_tank_air_filter", "-I-R-I-R"), ("vacuum_hose", ALL), ("fuel_filter", "-I-R-I-R"), ("fuel_lines", Q),
        ("battery_12v", ALL), ("electrical_system", EVEN),
        ("brake_lines", ALL), ("pedals", EVEN), ("parking_brake", EVEN),
        ("brake_fluid", ALL, "בספר: בדיקה בכל טיפול, ללא מרווח החלפה קבוע"), ("brake_pads", ALL), ("brake_discs", ALL),
        ("power_steering_fluid", ALL), ("steering", ALL),
        ("cv_boots", EVEN), ("tires", ALL), ("suspension", ALL), ("body_underside", ALL),
        ("ac_refrigerant", ALL), ("ac_system", ALL),
        ("cabin_filter", R_ALL),
        ("manual_gearbox_oil", Q), ("transfer_case_oil", Q, "4x4 בלבד"), ("differential_oil", Q, "4x4 בלבד"),
        ("exhaust", EVEN),
    ]),
    "long_interval": [
        long_("spark_plugs", "replace", every_km=40000, note="כך בספר הישראלי (מצתים רגילים); לפי הנוחות אפשר להחליף מוקדם יותר בטיפול אחר"),
        long_("valve_clearance", "inspect", every_km=60000, note="בטבלה שתי בדיקות במחזור של 120,000"),
        long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24),
        long_("coolant", "replace", first_km=200000, first_months=120, then_every_km=40000, then_every_months=24),
    ],
    "time_based": [],
    "sources": [
        {"url": "https://cdnmedia.kia-israel.co.il/www/cars-book/Sportage-SL-2011-2015.pdf", "kind": "importer",
         "note": "ספר רכב ספורטאז' 2011-2015 של קיה ישראל, פרק 7 עמ' 8-14 (טבלת בנזין). הפונט מקודד, פוענח"},
        KIA_HUB,
    ],
    "status": "reviewed",
    "notes": "דור SL. הטבלה בספר על רשת 15,000 עם הערות לשווקים: לסין 5,000, למזרח התיכון 10,000 ק\"מ או 12 חודשים לשמן (הערה *3, בתנאי חום מעל 40°C). "
             "היבואן בישראל מטפל כל 15,000. שמן גיר אוטומטי: ללא טיפול לפי הספר. נוזל בלמים: בדיקה בלבד בטבלה.",
})

# ---------------------------------------------------------------------------
# Alfa Romeo (סמלת). The Israeli Hebrew books sit on alfaromeo.co.il which is
# geo/bot blocked; the plans below come from the manufacturer's English
# handbooks on FCA's eLUM server (same content Samelet translates). The
# importer services every 15,000 km or 12 months; the petrol plans are on a
# 15,000 km grid anyway. Status stays draft until the Hebrew book is read.
# ---------------------------------------------------------------------------
AR = {"make": "Alfa Romeo", "make_he": "אלפא רומיאו", "importer": "סמלת"}
AR_WARR = {"url": "https://samelet.com/ebooks/AlfaRomeo_warranty_092022.pdf", "kind": "importer",
           "note": "חוברת אחריות ושירות של סמלת: אחריות 24 חודשים ללא הגבלת ק\"מ, חלודה 8 שנים, צבע 3 שנים; שגרת הטיפולים לפי ספר הרכב; איחור בטיפול מבטל אחריות"}
AR_BOOKS = {"url": "https://samelet.com/ספרות-רכב-אלפא-רומיאו/", "kind": "importer",
            "note": "עמוד ספרות הרכב של סמלת (הקישורים ל-carbook_* באתר alfaromeo.co.il חסומים מסביבת הענן)"}
AR_NOTE = ("הלוח הועתק מספר הנהג של היצרן באנגלית (eLUM). הספר העברי של סמלת הוא תרגום שלו אך לא נקרא. היבואן: טיפול כל 15,000 ק\"מ או שנה, "
           "והלוח של היצרן לבנזין בנוי על עמודות 15,000. ")
GRID_15_150 = [15000 * i for i in range(1, 11)]
A10 = "●" * 10
def ar(pat10):  # 10-column pattern -> keep as is
    return pat10
write({
    **AR, "id": "alfa-romeo-giulietta-2010-2020-1.4", "model": "Giulietta", "model_he": "ג'ולייטה", "generation": "940",
    "years": [2010, 2020], "engines": ["1.4 TB 120", "1.4 TB MultiAir 170"], "fuel": "petrol",
    "interval": {"km": 15000, "months": 12, "note": "היבואן: 15,000 או שנה. בספר היצרן: שמן כל 30,000 אך לפחות פעם בשנה (ובנסיעה עירונית או פחות מ-10,000 ק\"מ בשנה: כל שנה)"},
    "cycle_km": 120000,
    "services": grid(GRID_15_150[:8], [
        ("engine_oil", "-R-R-R-R", "לפי ספר היצרן כל 30,000 או שנה; בישראל נהוג בכל טיפול שנתי"), ("oil_filter", "-R-R-R-R"),
        ("tires", ALL), ("lights", ALL), ("coolant", ALL, "בדיקת מפלס והשלמה"), ("brake_fluid", "-R-R-R-R"),
        ("exhaust", ALL, "בדיקת פליטה"), ("diagnostics", ALL),
        ("body_underside", "I-I-I-I-"), ("wipers", "I-I-I-I-"), ("washer_fluid", "I-I-I-I-"),
        ("door_hinges", "-I-I-I-I"), ("parking_brake", "-I-I-I-I"),
        ("brake_pads", ALL), ("brake_discs", ALL),
        ("drive_belt", "---I----", "בדיקה ב-60,000 (גרסאות ללא מותחן אוטומטי)"), ("timing_belt", "---I---R", "בדיקה ב-60,000; החלפה ב-120,000 או 6 שנים, באבק/עיר 60,000 או 4 שנים"),
        ("dct_oil", "-I-I-I-I", "גיר TCT: בדיקת מפלס"),
        ("spark_plugs", "-R-R-R-R", "מנועי 1.4 TB ו-1.4 MultiAir: כל 30,000"),
        ("air_filter", "-R-R-R-R", "באזורי אבק כל 15,000"),
        ("cabin_filter", R_ALL, "בספר: חובה כל 30,000, מומלץ כל 15,000; באבק כל 15,000"),
    ]),
    "long_interval": [long_("drive_belt", "replace", every_km=120000, every_months=72, note="באזורי אבק/שימוש עירוני: 60,000 או 4 שנים")],
    "time_based": [],
    "specs": {"_note": "מתוך ספר היצרן באנגלית", "engine_oil": "Selenia StAR Pure Energy 5W-40 (ACEA C3) למנועי 1.4 TB", "oil_capacity": "1.4 TB: 3.1 ליטר כולל מסנן; 1.4 MultiAir: 3.5 ליטר", "coolant": "Paraflu UP 50% עם מים מזוקקים, 5.7 ליטר", "brake_fluid": "Tutela Top 4 (DOT 4), 0.83 ליטר",
              "fuel": "בנזין 95 אוקטן, מיכל 60 ליטר", "tires": "205/55 R16, 225/45 R17 או 225/40 R18", "tire_pressure": "לפי המדבקה בעמוד הדלת", "battery": "מצבר רגיל 12V; עם Start&Stop: EFB/AGM",
              "timing": "רצועת תזמון: החלפה ב-120,000 ק\"מ או 6 שנים (60,000/4 שנים בשימוש קשה)", "spare": "ערכת Fix&Go או גלגל חלופי צר", "warranty": "סמלת: 24 חודשים ללא הגבלת ק\"מ"},
    "sources": [
        {"url": "https://aftersales.fiat.com/eLumData/EN/83/191_GIULIETTA/83_191_GIULIETTA_604.38.735_EN_04_09.15_L_LG/83_191_GIULIETTA_604.38.735_EN_04_09.15_L_LG.pdf",
         "kind": "manufacturer", "note": "Owner handbook 2015 (EN), Scheduled Servicing Plan, petrol versions, pp. 197-200"},
        AR_BOOKS, AR_WARR,
    ],
    "status": "draft",
    "notes": AR_NOTE + "פעולות הבדיקה בספר (צמיגים, תאורה, נוזלים, פליטה, אבחון מחשב) בכל טיפול. מצתים כל 30,000 (1.4 טורבו). רצועת תזמון: החלפה ב-120,000/6 שנים.",
})
write({
    **AR, "id": "alfa-romeo-mito-2009-2018-1.4", "model": "MiTo", "model_he": "מיטו", "generation": "955",
    "years": [2009, 2018], "engines": ["1.4 78/105", "1.4 TB 120/155", "1.4 TB MultiAir 135/170"], "fuel": "petrol",
    "interval": {"km": 15000, "months": 12, "note": "היבואן: 15,000 או שנה. בספר היצרן: טיפול כל 30,000 ק\"מ או 24 חודשים"},
    "cycle_km": 120000,
    "services": grid(GRID_15_150[:8], [
        ("engine_oil", "-R-R-R-R", "לפי ספר היצרן כל 30,000 או 24 חודשים; בעיר או פחות מ-10,000 בשנה כל שנה"), ("oil_filter", "-R-R-R-R"),
        ("tires", "-I-I-I-I"), ("lights", "-I-I-I-I"), ("wipers", "-I-I-I-I"), ("washer_fluid", "-I-I-I-I"),
        ("brake_pads", "-I-I-I-I"), ("brake_discs", "-I-I-I-I"), ("body_underside", "-I-I-I-I"), ("door_hinges", "-I-I-I-I"),
        ("coolant", "-I-I-I-I", "בדיקת מפלס"), ("parking_brake", "-I-I-I-I"),
        ("timing_belt", "---I---R", "בדיקה ב-60,000; החלפה ב-120,000, ולפחות כל 4-5 שנים"), ("drive_belt", "---I---R"),
        ("exhaust", "-I-I-I-I", "בדיקת פליטה"), ("diagnostics", "-I-I-I-I"),
        ("spark_plugs", "-R-R-R-R", "כל 30,000"), ("air_filter", "---R---R"), ("brake_fluid", "---R---R", "או כל 24 חודשים"),
        ("cabin_filter", "-R-R-R-R", "או כל 24 חודשים"),
    ]),
    "long_interval": [],
    "time_based": [],
    "specs": {"_note": "מתוך ספר היצרן באנגלית", "engine_oil": "Selenia 5W-40 (ACEA C3) לטורבו; Selenia K P.E. 5W-40 לאטמוספרי", "coolant": "Paraflu UP, אדום", "brake_fluid": "Tutela Top 4 (DOT 4)",
              "fuel": "בנזין 95 אוקטן", "tires": "195/55 R16 או 215/45 R17", "tire_pressure": "לפי המדבקה", "battery": "מצבר רגיל 12V", "timing": "רצועת תזמון: 120,000 ק\"מ או 4-5 שנים", "spare": "גלגל חלופי צר או Fix&Go", "warranty": "סמלת: 24 חודשים ללא הגבלת ק\"מ"},
    "sources": [
        {"url": "https://aftersales.fiat.com/eLumData/EN/83/145_MiTo/83_145_MiTo_604.38.043_EN_01_10.08_L_LG/83_145_MiTo_604.38.043_EN_01_10.08_L_LG.pdf",
         "kind": "manufacturer", "note": "Owner handbook 2008 (EN), Scheduled Servicing Plan, petrol versions, pp. 199-200 (grid 30,000 km)"},
        AR_BOOKS, AR_WARR,
    ],
    "status": "draft",
    "notes": AR_NOTE + "הטבלה בספר היצרן בעמודות של 30,000 ק\"מ (30..180), לכן ברשת 15,000 של היבואן הפריטים נופלים על הטיפולים הזוגיים ובטיפולי הביניים שמן ובדיקות בלבד.",
})
GIULIA_ROWS = [
    ("battery_12v", "IIIIIIIIII"), ("tires", "IIIIIIIIII"), ("lights", "IIIIIIIIII"), ("coolant", "IIIIIIIIII", "בדיקת מפלס והשלמה"),
    ("exhaust", "IIIIIIIIII", "בדיקת פליטה"), ("diagnostics", "IIIIIIIIII", "כולל בדיקת מצב השמן במחשב"),
    ("body_underside", "-I-I-I-I-I"), ("wipers", "I-I-I-I-I-"), ("washer_fluid", "I-I-I-I-I-"), ("door_hinges", "-I-I-I-I-I"),
    ("brake_pads", "IIIIIIIIII"), ("brake_discs", "IIIIIIIIII"),
    ("drive_belt", "III-III-II", "בדיקה; החלפה ב-60,000 או 4 שנים (באבק/עיר 30,000 או 2 שנים)"),
    ("engine_oil", "RRRRRRRRRR", "לפי ספר היצרן לפי חיווי המחשב ולא יותר משנה; היבואן: כל 15,000 או שנה"), ("oil_filter", "RRRRRRRRRR"),
    ("spark_plugs", "---R---R--"), ("air_filter", "--R--R--R-", "באבק כל 15,000"),
    ("fuel_filter", "RRRRRRRRRR", "מסנן דלק משלים, אם קיים"),
    ("cabin_filter", "RRRRRRRRRR", "בספר: חובה כל 30,000, מומלץ כל 15,000"),
    ("brake_fluid", "-R-R-R-R-R", "כל שנתיים ללא קשר לק\"מ"),
]
GIULIA_LONG = [long_("drive_belt", "replace", every_km=60000, every_months=48, note="באבק/עיר: 30,000 או 2 שנים"),
               long_("transfer_case_oil", "replace", every_km=120000, note="גרסאות Q4 (4x4) בלבד")]
GIULIA_SPECS = {"_note": "מתוך ספר היצרן באנגלית", "engine_oil": "SAE 0W-30 ACEA C2 (FCA 9.55535-GS1), Selenia Digitek P.E., למנוע 2.0 T4 MultiAir", "coolant": "Paraflu UP, אדום",
                "brake_fluid": "Tutela Top 4/S (DOT 4)", "fuel": "בנזין 95 אוקטן", "tires": "225/45 R18 (ג'וליה) / 235/55 R18 (סטלביו) ומידות גדולות יותר לפי גימור", "tire_pressure": "לפי המדבקה בעמוד הדלת",
                "battery": "עם Start&Stop: מצבר AGM/EFB בלבד", "timing": "שרשרת, ללא החלפה מתוכננת", "spare": "ערכת תיקון (Fix&Go) או גלגל חלופי צר", "warranty": "סמלת: 24 חודשים ללא הגבלת ק\"מ"}
for id_, model, model_he, gen, years, src, note in [
    ("alfa-romeo-giulia-2016-2025-2.0", "Giulia", "ג'וליה", "952", [2016, 2025],
     "https://aftersales.fiat.com/eLumData/EN/83/620_GIULIA/83_620_GIULIA_603.93.005_EN_04_01.17_L_LG/83_620_GIULIA_603.93.005_EN_04_01.17_L_LG.pdf", "Owner handbook 2017 (EN), Service Schedule 2.0 T4 MAir petrol, pp. 158-160"),
    ("alfa-romeo-stelvio-2017-2025-2.0", "Stelvio", "סטלביו", "949", [2017, 2025],
     "https://aftersales.fiat.com/eLumData/EN/83/630_STELVIO/83_630_STELVIO_603.93.152_EN_02_02.18_L_LG/83_630_STELVIO_603.93.152_EN_02_02.18_L_LG.pdf", "Owner handbook 2018 (EN), Service Schedule 2.0 T4 MAir petrol, pp. 161-163 (same rows as Giulia)"),
]:
    write({
        **AR, "id": id_, "model": model, "model_he": model_he, "generation": gen, "years": years,
        "engines": ["2.0 T4 MultiAir 200/280"], "fuel": "petrol",
        "interval": {"km": 15000, "months": 12, "note": "היבואן: 15,000 או שנה; ספר היצרן: שמן לפי חיווי המחשב ולא יותר משנה"},
        "cycle_km": 150000,
        "services": grid(GRID_15_150, GIULIA_ROWS),
        "long_interval": GIULIA_LONG,
        "time_based": [],
        "specs": GIULIA_SPECS,
        "sources": [{"url": src, "kind": "manufacturer", "note": note}, AR_BOOKS, AR_WARR],
        "status": "draft",
        "notes": AR_NOTE + "מצתים ב-60 ו-120 אלף. מסנן אוויר כל 45,000. נוזל בלמים כל שנתיים. מסנן תא נוסעים חובה כל 30,000. שמן תיבת העברה ב-120,000 בגרסאות Q4. הלוח חוזר על עצמו אחרי 150,000/10 שנים.",
    })
write({
    **AR, "id": "alfa-romeo-tonale-2022-2025-1.5-hybrid", "model": "Tonale", "model_he": "טונאלה", "generation": "965",
    "years": [2022, 2025], "engines": ["1.5 T4 160 mild hybrid 48V"], "fuel": "hybrid",
    "interval": {"km": 15000, "months": 12}, "cycle_km": 150000,
    "services": grid(GRID_15_150, [
        ("tires", "IIIIIIIIII"), ("lights", "IIIIIIIIII"), ("coolant", "IIIIIIIIII", "בדיקת מפלס: קירור מנוע וקירור מערכת 48V"), ("diagnostics", "IIIIIIIIII"),
        ("body_underside", "I-I-I-I-I-"), ("wipers", "I-I-I-I-I-"), ("washer_fluid", "I-I-I-I-I-"), ("door_hinges", "-I-I-I-I-I"),
        ("brake_pads", "IIIIIIIIII"), ("brake_discs", "IIIIIIIIII"),
        ("drive_belt", "---I------", "בדיקה ב-60,000; החלפה ב-120,000 או 6 שנים (בשימוש קשה 60,000 או 4 שנים)"),
        ("engine_oil", "RRRRRRRRRR"), ("oil_filter", "RRRRRRRRRR"),
        ("spark_plugs", "---R---R--"), ("air_filter", "-R-R-R-R-R", "באבק כל 15,000"),
        ("cabin_filter", "RRRRRRRRRR", "מומלץ אף כל 6 חודשים"), ("brake_fluid", "-R-R-R-R-R", "כל שנתיים"),
        ("dct_oil", "---R---R--", "שמן תיבת הילוכים (DCT 7): כל 60,000 או 6 שנים"),
    ]),
    "long_interval": [long_("drive_belt", "replace", every_km=120000, every_months=72, note="בשימוש קשה 60,000 או 4 שנים; מותחן ב-120,000/6 שנים")],
    "time_based": [{"item": "ecall_battery", "action": "replace", "months": 60, "note": "סוללת Alfa Connect Box כל 5 שנים"}],
    "specs": {"_note": "מתוך ספר היצרן באנגלית", "engine_oil": "SAE 0W-20 ACEA C5 (FCA 9.55535-DM1), Selenia Eco2, למנוע 1.5 T4 48V; גיר DCT: Tutela DCT 700 H", "coolant": "Paraflu UP; מעגל נפרד למערכת 48V", "brake_fluid": "DOT 4",
              "fuel": "בנזין 95 אוקטן", "tires": "215/60 R17, 225/55 R18, 235/45 R19 או 235/40 R20", "tire_pressure": "לפי המדבקה בעמוד הדלת", "battery": "מצבר 12V AGM + סוללת 48V; לא מצבר רגיל",
              "timing": "שרשרת, ללא החלפה מתוכננת", "spare": "ערכת TireKit", "warranty": "סמלת: 24 חודשים ללא הגבלת ק\"מ"},
    "sources": [
        {"url": "https://aftersales.fiat.com/eLumData/EN/83/965_TONALE/83_965_TONALE_603.93.733_EN_01_03.22_L_LG/83_965_TONALE_603.93.733_EN_01_03.22_L_LG.pdf",
         "kind": "manufacturer", "note": "Owner handbook 2022 (EN), Service Schedule, pp. 224-226 (dots read from the vector drawing)"},
        AR_BOOKS, AR_WARR,
    ],
    "status": "draft",
    "notes": AR_NOTE + "היברידי מתון 48V. מצתים ב-60 ו-120 אלף, מסנן אוויר כל 30,000, נוזל בלמים כל שנתיים, שמן גיר כל 60,000/6 שנים, סוללת Alfa Connect כל 5 שנים.",
})

# ---------------------------------------------------------------------------
# Toyota (יוניון מוטורס). The importer publishes a one-page Israeli
# maintenance sheet per model/generation at books.union-motors.co.il
# (API: /app/api/models, /app/api/search?modelId&year, /app/api/files/{conn}/download).
# The sheets were parsed by word coordinates into data/sources/toyota-union-sheets.json:
# 10 columns (15..150 thousand km), letters I/R/C/T per cell, "רגילה" (normal)
# and "מחמירה" (severe) rows, plus free-text long intervals.
# ---------------------------------------------------------------------------
TY = {"make": "Toyota", "make_he": "טויוטה", "importer": "יוניון מוטורס"}
TY_SHEETS = json.load(open(os.path.join(ROOT, "sources", "toyota-union-sheets.json"), encoding="utf-8"))
TY_HUB = {"url": "https://www.toyota.co.il/owners/parts-and-accessories/owners-manuals", "kind": "importer",
          "note": "מרכז ספרות הרכב של טויוטה ישראל (בחירת דגם ושנה); המסמכים נשלפים מ-books.union-motors.co.il"}
GRID_TY = [15000 * i for i in range(1, 11)]
TY_ACT = {"I": "inspect", "R": "replace", "C": "clean", "T": "adjust", "L": "inspect", "G": "inspect"}  # L/G = גירוז (אין פעולה כזו בסכמה)
# label regex -> list of item keys (a row may feed two items)
TY_MAP = [
    (r"^שמן מנוע ומסנן", ["engine_oil", "oil_filter"]), (r"^שמן מנוע", ["engine_oil"]), (r"^מסנן שמן", ["oil_filter"]),
    (r"^מערכת קירור וחימום", ["cooling_system"]),
    (r"נוזל קירור (מערכת )?היבריד|נוזל קירור ממיר", ["coolant"]), (r"^נוזל קירור מנוע", ["coolant"]),
    (r"^צינורות פליטה", ["exhaust"]), (r"^מצבר", ["battery_12v"]), (r"^מסנן דלק", ["fuel_filter"]),
    (r"^מסנן אוויר מזגן", ["cabin_filter"]),
    # before "^מסנן אוויר": the hybrid (or 48V) battery cooling-air filter is its own item, not the engine air filter
    (r"מסנן (אוויר )?סוללה (היברידית|48V)", ["hybrid_battery_filter"]), (r"^מסנן אוויר", ["air_filter"]),
    (r"^צינורות דלק", ["fuel_lines"]), (r"מסנן פחם|מכלול פחמי", ["evap_system"]),
    (r"^מכסה מיכל דלק , קווי דלק", ["fuel_lines", "evap_system"]),  # sheet 336: cap, fuel lines and vapour valve in one row
    (r"^דוושת בלם.*חניה|^דוושת בלם", ["pedals", "parking_brake"]), (r"^דוושת מצמד", ["pedals"]),
    (r"תופי בלם|^צינורות ותופי", ["brake_drums"]),
    (r"^צלחות|^ודיסקיות", ["brake_pads", "brake_discs"]),
    (r"^נוזל (מכלול )?בלמים", ["brake_fluid"]), (r"^נוזל (מכלול )?מצמד", ["clutch"]),
    (r"^צינורות בלמים", ["brake_lines"]),
    (r"^(מסרק|תיבת) הגה|^הגה", ["steering"]), (r"^שרוולי גומי לציריות", ["cv_boots"]),
    (r"מחברים כדוריים|מפרקים כדוריים|מפרקים וגומיות|^ומגיני אבק|^אבק", ["suspension"]),
    (r"נוזל תיבת הילוכים (רציפה|CVT|E-CVT)|\(\s*ו?דיפרנציאל קדמי\s*\)|^\( משולב דיפרנציאל \)", ["cvt_oil"]),
    (r"נוזל תיבת הילוכים היברידית|נוזל \( תיבת משולב", ["transmission_oil"]),
    (r"נוזל תיבת הילוכים (אוט|רובוטית)|^רובוטית", ["transmission_oil"]),
    (r"תיבה \" ל ידנית|שמן גיר ידני|נוזל תיבת הילוכים ידנית", ["manual_gearbox_oil"]),
    (r"^מתלים", ["suspension"]), (r"^ברגי", ["body_underside"]),
    (r"^צמיגים", ["tires"]), (r"^אורות|^מגבים", ["lights", "wipers"]),
    (r"בדיקת חלודה|בדיקת קורוזיה|בדיקת גוף הרכב", ["body_underside"]),
    (r"^מרווח שסתומים|^כיוון שסתומים", ["valve_clearance"]), (r"^מצתים", ["spark_plugs"]), (r"^רצועת הינע", ["drive_belt"]),
    (r"שמן דיפרנציאל|שמן דיפרונציאל", ["differential_oil"]), (r"שמן תיבת העברה", ["transfer_case_oil"]),
    (r"^מצנן צינורות|^מחברי , צינורות ומצנן", ["coolant_hoses"]),
    # diesel / 4x4 / older sheets (Hilux, Land Cruiser, Prius, Verso, Avensis, City, bZ4X)
    (r"^עשן סמיך|^בדיקת עשן|בדיקת סתימות (PDF|DPF)|^בדיקת סתימות \(", ["exhaust"]),
    (r"^החלפה$", ["coolant"]),  # second line of 'נוזל קירור מנוע - בדיקה / החלפה'
    (r"^בדיקה$", ["coolant"]),  # first line of that block when the item name sits on its own line below it
    (r"^נוזל מערכת היגוי", ["power_steering_fluid"]),
    (r"^וקשיחים", ["brake_lines"]),
    (r"^כמות קרר|^בדיקת קרר|^קרר", ["ac_refrigerant"]),
    (r"^מפריד מים|^משקעי מים|^בית מסנן סולר|^מסנן סולר", ["fuel_filter"]),
    (r"^תופי בילום|^\) כולל בלם החניה", ["brake_drums"]),
    (r"^גירוז|^גלי הינע|^הידוק|^ואחורי הידוק|^חיזוק ברגים|^גומיות גלי הינע", ["propshaft"]),
    (r"^תיבת העברה", ["transfer_case_oil"]),
    (r"^פחמי$", ["cabin_filter"]),
    (r"^תאורה|^צופר|^חלונות , פנסים", ["lights", "wipers"]),
    (r"דיפרנציאל קדמי ואחורי|^שמן דיפ", ["differential_oil"]),
    (r"נוזל קירור מער ' הברידית|נוזל קירור ליחידת חימום|נוזל קירור סוללה|מערכת קירור סוללה|^בדיקת pH", ["coolant"]),
    (r"^אוטומטית \( משולב|^אוטומטית$", ["transmission_oil"]), (r"^ידנית$", ["manual_gearbox_oil"]),
    (r"^רצועת תזמון|^גלגלת תזמון|^מכסה( מכלול)? תזמון", ["timing_belt"]),
    (r"^שמן ומסנן שמן מנוע", ["engine_oil", "oil_filter"]),
    (r"^בדיקת מערכות קירור", ["cooling_system"]),
    (r"^צינורות , אטמי HOUSING|^צינורות ומחברי מצנן שמן", ["coolant_hoses"]),
    (r"^איטום בולמי זעזועים", ["suspension"]), (r"^מסנן מזגן", ["cabin_filter"]),
    (r"^כוונון שסתומים", ["valve_clearance"]), (r"^מכלול בלם חניה|^חניה$", ["parking_brake"]),
    (r"מצנן צינורות וחיבורים לשמן גיר|מסנן צינורות וחיבורים לנוזל גיר|^צינורות תיבת הילוכים|^צינורות ומצנן תיבת", ["transmission_oil"]),
    (r"^משאבת וו?אקום", ["vacuum_hose"]), (r"^מסנן מערכת קירור מצבר", ["hybrid_battery_filter"]),
    (r"^תמיסת אוריאה|AdBlue", ["adblue"]),
    (r"^נוזל תיבת הינע חשמלי|^נוזל תיבת הילוכים|^צינורות בתיבת הילוכים", ["transmission_oil"]),
    (r"מחזור אדי דלק|^בקרת אדי דלק|^מסנן פחמי", ["evap_system"]), (r"^קדמיים", ["body_underside"]), (r"^רצועת מנוע", ["drive_belt"]),
    (r"^בדיקת מרווח שסתומים", ["valve_clearance"]), (r"^דיפרנציאל אחורי", ["differential_oil"]),
]
TY_SKIP = re.compile(r"עיגון שטיח|^מקרא|^רגילה$|^מחמירה$|^$|ידית הילוכים|ברגי גל הינע|מסנן מצבר|^סוג הנוזל|^החלפה לפי הצורך|^(מחמירה|רגילה)( (מחמירה|רגילה))+$|^רגיל$")
def ty_rows(fid):
    """Return list of (items, pattern, severe, months_text, label) for one sheet."""
    out = []
    for r in TY_SHEETS[str(fid)]["rows"]:
        lab = r["label"]
        if TY_SKIP.search(lab):
            continue
        severe = "מחמירה" in lab and "רגילה" not in lab
        lab_clean = lab.replace("רגילה", "").replace("מחמירה", "").strip(" -")
        items = None
        for rx, it in TY_MAP:
            if re.search(rx, lab_clean):
                items = it; break
        if not items:
            raise KeyError(f"sheet {fid}: unmapped label {lab!r}")
        out.append((items, r["pattern"], severe, r["months"], lab_clean))
    return out
KM = r"(\d{2,3})[.,]?000"
TY_LONG_LABELS = [  # label at the start of a sheet line -> item, for intervals written as text in the notes column
    (r"^מצתים", "spark_plugs"), (r"^מסנן דלק", "fuel_filter"), (r"^רצועת (?:הינע|מנוע|אביזרים)", "drive_belt"),
    (r"^מערכת קירור וחימום", "cooling_system"), (r"^צינורות דלק", "fuel_lines"), (r"^צינורות ומחברי מצנן שמן", "coolant_hoses"),
    (r"^גלי הינע", "propshaft"),
]
def ty_months(s):
    """Months next to a km figure: '( או 72 חודשים )', '( או 72 ח ')'."""
    m = re.match(r"\s*(?:ק\"מ)?\s*(?:\(?\s*או|\\)\s*(\d{1,3})\s*ח", s)
    return int(m.group(1)) if m else None
def ty_long(fid, grid_rows=()):
    """Long-interval facts written as text on the sheet. They are read from the
    sheet's `lines` (words grouped by their y position), so a label and the
    interval printed beside it stay together; in the plain page text they are
    far apart and out of order ("החלפה מדי90,000 ק"מ ... מסנן דלק מצתים").
    grid_rows: the (item, pattern) rows of the grid, used for the coolant note
    "after the first replacement, every N"."""
    sheet = TY_SHEETS[str(fid)]
    t = sheet["text"]
    lines = sheet.get("lines") or []
    cut = next((i for i, l in enumerate(lines) if "תחזוקה מחמירה" in l), len(lines))  # severe-only table at the bottom
    lines = lines[:cut]
    cols = sheet.get("columns_km") or GRID_TY
    L = []; notes = []
    def add(item, action, **kw):
        key = lambda d: (d.get("item"), d.get("action"), d.get("first_km"), d.get("every_km"), d.get("note"))
        if key(dict(kw, item=item, action=action)) not in {key(x) for x in L}:
            L.append(long_(item, action, **kw))
    iridium = any("Iridium" in l or "אירידיום" in l for l in sheet.get("lines") or [])
    for i, l in enumerate(lines):
        if "מחמירה" in l:
            continue  # severe-use row; the normal row is what the schedule shows
        s = re.sub(r"^[\s*()]+", "", l)
        # coolant: "החלפה ראשונה ב 150,000 ק"מ ומאז כל 75,000"; the label is on this line or the line above
        m = re.search(r"החלפה ראשונה\s*,?\s*(?:ב|לאחר)\s*-?\s*" + KM + r"\s*ק\"מ\s*,?\s*(?:ומאז|לאחר מכן)\s*(?:כל|מדי|מידי)\s*" + KM, s)
        if m:
            first, then = int(m.group(1)) * 1000, int(m.group(2)) * 1000
            ctx = s[:m.start()].replace("החלפה", "").strip(" -")
            if not ctx and i:
                ctx = lines[i - 1]
            if "סוללה" in ctx:
                note = "נוזל קירור סוללת מתח גבוה"
            elif "היבריד" in ctx or "הברידית" in ctx or "ממיר" in ctx or (not ctx and first >= 200000):
                note = "נוזל קירור מערכת היברידית/ממיר"
            else:
                note = "נוזל קירור מנוע (SLLC)"
            add("coolant", "replace", first_km=first, then_every_km=then, note=note)
            continue
        # coolant, newer sheets: replaced once in the grid, then "לאחר החלפה ראשונה יש להחליף מדי 75,000"
        m = re.search(r"^נוזל קירור מנוע\s*-?\s*לאחר החלפה ראשונה\s*,?\s*יש להחליף (?:מדי|מידי|כל)\s*" + KM, s)
        if m:
            first = next((cols[j] for it, pat in grid_rows if it == "coolant" for j, c in enumerate(pat) if c == "R"), None)
            if first:
                add("coolant", "replace", first_km=first, then_every_km=int(m.group(1)) * 1000,
                    note=f"נוזל קירור מנוע: החלפה ראשונה ב-{first:,} ק\"מ (בטבלה), אחר כך כל {int(m.group(1)) * 1000:,}")
            continue
        # "רגילה בדיקה מדי 10,000 ק"מ ( או 6 חודשים ) , החלפה מדי 30,000 ..." with the item's name on the next
        # line (diesel sheets: engine air filter)
        m = re.search(r"^רגילה\s*(?:בדיקה|אבחון) (?:מדי|מידי|כל)\s*" + KM + r"(.*?)החלפה (?:מדי|מידי|כל)\s*" + KM + r"(.*)$", s)
        if m and i + 1 < len(lines):
            nxt = re.sub(r"[\s*]+$", "", lines[i + 1])
            it = next((v for rx, v in TY_MAP if re.search(rx, nxt)), None)
            if it and len(it) == 1:
                add(it[0], "inspect", every_km=int(m.group(1)) * 1000, every_months=ty_months(m.group(2)))
                add(it[0], "replace", every_km=int(m.group(3)) * 1000, every_months=ty_months(m.group(4)))
            continue
        item = next((it for rx, it in TY_LONG_LABELS if re.search(rx, s)), None)
        if not item:
            continue
        # "replace every N" (spark plugs, fuel filter); months from "( או M חודשים )" or the months column "R : 144"
        m = re.search(r"(?:החלפה|החלף) (?:מדי|מידי|כל)\s*" + KM + r"\s*ק\"מ", s)
        if m and item in ("spark_plugs", "fuel_filter"):
            rest = s[m.end():]
            mo = ty_months(rest)
            mm = re.search(r"R\s*:\s*(\d{2,3})\b|\b(\d{2,3})\s*:\s*R", rest)
            if mo is None and mm:
                mo = int(mm.group(1) or mm.group(2))
            kw = {"every_km": int(m.group(1)) * 1000}
            if mo:
                kw["every_months"] = mo
            if item == "spark_plugs" and iridium:
                kw["note"] = "מצתי אירידיום"
            add(item, "replace", **kw)
            continue
        m = re.search(r"הידוק (?:הברגים )?(?:מדי|מידי|כל)\s*" + KM + r"(.*)$", s)
        if m and item == "propshaft":
            add(item, "adjust", every_km=int(m.group(1)) * 1000, every_months=ty_months(m.group(2)),
                note="הידוק ברגי גלי ההינע" + (", 4x4 בלבד" if "4X4" in s.upper() else ""))
            continue
        # "inspect first at N1 (or M1 months) [and at N2] then every N3 (or M3 months)": drive belt, and on the
        # Land Cruiser sheets the cooling system, fuel lines and oil-cooler hoses
        m = re.search(r"(?:אבחון|בדיקה|בדוק)\s*(?:ראשון|ראשונה|לראשונה)?\s*(?:ב|לאחר)\s*-?\s*" + KM + r"(.*?)(?:ומאז|לאחר מכן)\s*(?:כל|מדי|מידי)\s*" + KM + r"(.*)$", s)
        if m:
            first, mid, then, tail = int(m.group(1)) * 1000, m.group(2), int(m.group(3)) * 1000, m.group(4)
            fm, tm = ty_months(mid), ty_months(tail)
            if fm is None or tm is None:  # months only in the months column: "72(1) : I , 12 : I" / "I:12 and I:72"
                ms = sorted({int(a or b) for a, b in re.findall(r"(\d{1,3})\s*(?:\(\d\))?\s*,?\s*:|I\s*:\s*(\d{1,3})", tail)})
                if len(ms) >= 2:
                    fm, tm = fm or ms[-1], tm or ms[0]
            kw = {}
            second = re.search(r"וב\s*-?\s*" + KM, mid)
            if second:  # "at 40,000 and at 80,000, then every 20,000"
                kw["note"] = f"בדיקה ראשונה ב-{first:,} ק\"מ" + (f" ({fm} חודשים)" if fm else "") + f", שנייה ב-{int(second.group(1)) * 1000:,}, ואז כל {then:,}"
                first = int(second.group(1)) * 1000
                fm = ty_months(mid[second.end():])
            if "החלפה לפי הצורך" in tail:
                kw["note"] = (kw.get("note", "") + "; " if kw.get("note") else "") + "החלפה לפי הצורך"
            add(item, "inspect", first_km=first, first_months=fm, then_every_km=then, then_every_months=tm, **kw)
    # oil by service indicator (Hilux / Land Cruiser diesels): "שמן מנוע החלפה עפ"י נורת התראה או 30,000 ק"מ \ 24 חודשים"
    m = (re.search(r"שמן ה?מנוע.{0,60}?(?:נורת התראה|אחד מהתנאים).{0,80}?(\d{2}),000 ק\"מ.{0,30}?(\d{2})\s*חודשים", t)
         or re.search(r"שמן ה?מנוע.{0,60}?(?:נורת התראה|אחד מהתנאים).{0,40}?(\d{2}),000 ק\"מ.{0,20}?(שנתיים)", t)
         or re.search(r"שמן ה?מנוע.{0,60}?(?:נורת התראה|אחד מהתנאים).{0,60}?(שנתיים).{0,25}?(\d{2}),000 ק\"מ", t))
    if not m:  # Hilux 2026 (sheet 368): merged cell "replace every 30,000 km, two years or by the service light"
        mm = re.search(r"שנתיים או נורת התראה,?\s*מ\"\s*ק\s*(\d{2}),000\s*החלפה כל", t)
        if mm:
            m = type("M", (), {"group": (lambda self, i, a=mm.group(1): a if i == 1 else "24")})()
    if not m:
        mm = re.search(r"נורת התראה או כל\s*(\d{2}),000 ק\"מ.{0,15}?(\d{2})\s*חודשים", t)  # Hilux 2015+: oil & filter by indicator or 30,000 / 24 months
        if mm and not re.search(r"בהופעת התראת החלפת שמן|לפי מנורת התראה", t):
            m = mm
    if m and m.group(1) == "שנתיים":
        m = type("M", (), {"group": (lambda self, i, a=m.group(2), b="שנתיים": a if i == 1 else b)})()
    if m:
        mo = 24 if m.group(2) == "שנתיים" else int(m.group(2))
        add("engine_oil", "replace", every_km=int(m.group(1)) * 1000, every_months=mo, note="לפי נורת ההתראה של מערכת הטיפולים, או המרווח הזה, המוקדם מביניהם; מסנן השמן מוחלף בכל החלפת שמן")
        add("oil_filter", "replace", every_km=int(m.group(1)) * 1000, every_months=mo)
    m = re.search(r"משאבת וו?אקום (?:החלפה|החלף) (?:מדי|כל)\s*(\d{3}),000 ק\"מ( או\s*\d+ שנים)?", t)
    if m: notes.append(f"משאבת ואקום: החלפה כל {m.group(1)},000 ק\"מ{m.group(2) or ''}.")
    tb = []  # time-based items written as text (diesel sheets)
    for l in lines:
        m = re.search(r"^צינורות גמישים למכלול DPF.*?(?:R\s*:\s*(\d{2})|(\d{2})\s*:\s*R|כל\s*(\d{2})\s*חודשים)", l)
        if m:
            tb.append({"item": "exhaust", "action": "replace", "months": int(next(g for g in m.groups() if g)),
                       "note": "הצינורות הגמישים של מכלול מסנן החלקיקים (DPF)"})
            break
    m = next((re.search(r"^מד זרימת אוויר.*?מדי\s*" + KM + r"\s*ק\"מ\s*\(?\s*או\s*(\d{2})\s*חודשים", l) for l in lines if l.startswith("מד זרימת אוויר")), None)
    if m: notes.append(f"מד זרימת האוויר: ניקוי בנשיפת אוויר כל {m.group(1)},000 ק\"מ או {m.group(2)} חודשים.")
    return L, notes, tb
def toyota(id_, fid, model, model_he, gen, years, engines, fuel, extra_sheets=(), notes_extra="", specs=None):
    sheet = TY_SHEETS[str(fid)]
    rows = ty_rows(fid)
    # normal rows only; severe-only rows become notes
    grid_rows = []; severe_notes = []
    normal_keys = {tuple(it) for it, pat, sev, mo, lab in rows if not sev}
    for it, pat, sev, mo, lab in rows:
        if sev:
            if tuple(it) not in normal_keys:
                severe_notes.append(f"{lab}: בתנאים מחמירים בלבד ({pat})")
            continue
        note = f"תדירות בחודשים לפי הגיליון: {mo}" if mo else None
        pat = pat.replace("T", "A").replace("L", "I").replace("G", "I")
        for k in it:
            grid_rows.append((k, pat, note) if note else (k, pat))
    cols = sheet.get("columns_km") or GRID_TY
    step = cols[0]
    if not any(k in ("engine_oil",) for k, *_ in grid_rows) and re.search(r"התראת החלפת שמן|נורית התראת טיפול|נורת התראת טיפול|לפי מנורת התראה", sheet["text"]) and fuel != "electric":
        n = f"לפי הגיליון: בהופעת התראת החלפת שמן, או לאחר {step:,} ק\"מ, או לאחר 12 חודשים (הקודם); בתנאים מחמירים 7,500 ק\"מ או 6 חודשים"
        grid_rows = [("engine_oil", "R" * len(cols), n), ("oil_filter", "R" * len(cols), n)] + grid_rows
    # merge duplicate (item,column) entries: grid() emits duplicates, dedupe after
    services = grid(cols, grid_rows)
    for svc in services:
        seen = {}; merged = []
        for e in svc["items"]:
            key = (e["item"], e["action"])
            if key in seen: continue
            seen[key] = 1; merged.append(e)
        svc["items"] = merged
    long_items, ln, time_items = ty_long(fid, [(r[0], r[1]) for r in grid_rows])
    engine_line = sheet.get("engine")
    # source URLs download by connection id (see scripts/toyota_sheets_export.py); the note names the document's fileId
    ref = lambda sh, fid: f"מסמך {fid}" + (f", קישור נבדק {sh['checked']}" if sh.get("checked") else "")
    srcs = [{"url": sheet["source"], "kind": "importer", "note": f"לוח אחזקה של יוניון מוטורס '{sheet['title']}' (דגמים {', '.join(sheet['models'])}, שנים {sheet['years'][0]}-{sheet['years'][1]}; {ref(sheet, fid)}); דגם מנוע בגיליון: {engine_line}"}]
    for x in extra_sheets:
        # (fileId, how it relates to the main sheet); a bare fileId is a sheet checked to carry the same plan
        x, rel = (x, "אותה תוכנית") if isinstance(x, int) else x
        sh = TY_SHEETS[str(x)]
        srcs.append({"url": sh["source"], "kind": "importer", "note": f"לוח אחזקה נוסף '{sh['title']}' ({sh['years'][0]}-{sh['years'][1]}; {ref(sh, x)}): {rel}"})
    srcs.append(TY_HUB)
    sp = {"_note": "שמן, נוזל קירור ונוזל בלמים מהגיליון של היבואן; שאר הפריטים ידע כללי, לאימות"}
    sp.update(specs or {})
    write({
        **TY, "id": id_, "model": model, "model_he": model_he, "generation": gen, "years": years, "engines": engines, "fuel": fuel,
        "interval": ({"km": 15000, "months": 12, "note": "לפי הגיליון: תנאי פעולה רגילים 15,000 ק\"מ או 12 חודשים; בתנאים מחמירים שמן ומסנן כל 7,500 ק\"מ או 6 חודשים"} if step == 15000
                     else {"km": step, "months": 6, "note": f"לפי הגיליון: {step:,} ק\"מ או 6 חודשים, המוקדם מביניהם (גיליון דיזל/4x4 של 16 עמודות)"}),
        "cycle_km": cols[-1],
        "services": services,
        "long_interval": long_items,
        "time_based": time_items,
        "specs": sp,
        "sources": srcs,
        "status": "reviewed",
        "notes": (f"הועתק מלוח האחזקה הישראלי של יוניון מוטורס ({len(cols)} עמודות של {step:,} ק\"מ). פעולות: I בדיקה, R החלפה, C ניקוי, T הידוק, L/G גירוז (נרשם כבדיקה). "
                  + ("שורות 'מחמירה' בלבד: " + "; ".join(severe_notes) + ". " if severe_notes else "")
                  + (" ".join(ln) + " " if ln else "") + notes_extra).strip(),
    })

TY_OIL_OLD = {"engine_oil": "API SL/SM/SN, 0W-20 או 5W-30 (לפי טבלת הנוזלים בגיליון)", "coolant": "Toyota SLLC (ורוד), לא לערבב", "brake_fluid": "DOT 3 או DOT 4 (FMVSS 116)", "fuel": "בנזין 95 אוקטן", "timing": "שרשרת, ללא החלפה מתוכננת", "tire_pressure": "לפי המדבקה בעמוד הדלת", "warranty": "יוניון מוטורס: 3 שנים או 100,000 ק\"מ (ידע כללי, לאימות)"}
TY_OIL_NEW = dict(TY_OIL_OLD, engine_oil="API SL/SM/SN, 0W-16, 0W-20, 5W-30 או 10W-30 (לפי הגיליון)")
HYB = {"battery": "מצבר עזר 12V קטן (לא מצבר רגיל) + סוללה היברידית; בדיקת סוללה שנתית תנאי לאחריות הסוללה"}
toyota("toyota-corolla-2007-2012-1.6", 287, "Corolla", "קורולה", "E150", [2007, 2012], ["1.6 (1ZR-FE)"], "petrol",
       specs=dict(TY_OIL_OLD, oil_capacity="כ-4.2 ליטר", tires="195/65 R15 או 205/55 R16", battery="מצבר רגיל 12V", spare="גלגל חלופי צר"))
toyota("toyota-corolla-2013-2019-1.6", 289, "Corolla", "קורולה", "E170", [2013, 2019], ["1.6 (1ZR-FAE)"], "petrol",
       specs=dict(TY_OIL_OLD, oil_capacity="4.2 ליטר (לפי הגיליון)", coolant="Toyota SLLC, 5.8 ליטר", tires="205/55 R16", battery="מצבר רגיל 12V", spare="גלגל חלופי צר",
                  brake_fluid="SAE J1704 / FMVSS 116 DOT 4"),
       notes_extra="הגיליון הוא לשנים 2013-2017; דור E170 נמכר עד 2019. מצתים DENSO Iridium SC20HR11; שמן CVT Toyota Genuine CVT Fluid FE.")
toyota("toyota-corolla-2019-2025-1.6", 327, "Corolla", "קורולה", "E210 (ZRE210)", [2019, 2025], ["1.6 (1ZR-FAE)"], "petrol",
       extra_sheets=((317, "גיליון מרץ 2019: אותה תוכנית, אבל בלי שורת מסנן הדלק"),),
       specs=dict(TY_OIL_NEW, oil_capacity="4.2 ליטר (לפי הגיליון)", coolant="Toyota SLLC, 5.8 ליטר", tires="205/55 R16 או 225/40 R18", battery="מצבר רגיל 12V", spare="ערכת תיקון או גלגל חלופי צר, לפי גימור",
                  brake_fluid="SAE J1703/J1704 / FMVSS 116 DOT 3/DOT 4"),
       notes_extra="גיר אוטומטי (ATF WS, ללא החלפה מתוכננת בתנאים רגילים; בדיקה כל 60,000).")
toyota("toyota-corolla-2019-2025-1.8-hybrid", 316, "Corolla", "קורולה", "E210 (ZWE211)", [2019, 2022], ["1.8 hybrid (2ZR-FXS)"], "hybrid",
       specs=dict(TY_OIL_NEW, oil_capacity="4.2 ליטר (לפי הגיליון)", coolant="Toyota SLLC: מנוע 5.4 ליטר, מערכת היברידית 1.4 ליטר (לפי הגיליון)", tires="205/55 R16 או 225/40 R18", spare="ערכת תיקון או גלגל חלופי צר", **HYB,
                  brake_fluid="SAE J1703/J1704 / FMVSS 116 DOT 3/DOT 4"),
       notes_extra="מסנן אוויר סוללה היברידית: ניקוי בכל טיפול. נוזל קירור מערכת היברידית: החלפה ראשונה 240,000 ואז כל 90,000. "
                   "הפייסליפט ZWE219 (2023 ואילך) בלוח נפרד toyota-corolla-2023-2025-1.8-hybrid (גיליון 345), כי התוכנית שונה. "
                   "שם הקובץ נשאר עם 2025 כדי לא לשבור קישורים קיימים.")
toyota("toyota-corolla-2023-2025-1.8-hybrid", 345, "Corolla", "קורולה", "E210 facelift (ZWE219)", [2023, 2025], ["1.8 hybrid (2ZR-FXE)"], "hybrid",
       specs=dict(TY_OIL_NEW, oil_capacity="4.2 ליטר (לפי הגיליון)", coolant="Toyota SLLC: מנוע 5.4 ליטר, מערכת היברידית 1.5 ליטר (לפי הגיליון)", tires="205/55 R16 או 225/40 R18", spare="ערכת תיקון או גלגל חלופי צר", **HYB,
                  brake_fluid="SAE J1703/J1704 / FMVSS 116 DOT 3/DOT 4"),
       notes_extra="הגיליון של הפייסליפט (ZWE219). לעומת גיליון 2019 (ZWE211): מסנן מזגן מוחלף בכל טיפול, מסנן דלק מוחלף ב-75,000 וב-150,000, "
                   "אחרי ההחלפה הראשונה נוזלי הקירור (מנוע ומערכת היברידית) מוחלפים כל 75,000 (במקום 90,000), ונוזל בלמים נבדק גם בטיפולי הביניים. "
                   "באפליקציית היבואן הגיליון רשום לשנת 2023, ולשנים 2024-2025 מופיע גם הגיליון הקודם; הלוח הזה חל על כל רכבי ZWE219.")
toyota("toyota-corolla-cross-2022-2025-1.8-hybrid", 346, "Corolla Cross", "קורולה קרוס", "XG10", [2022, 2025], ["1.8 hybrid (2ZR-FXE)"], "hybrid",
       extra_sheets=((338, "גיליון ספטמבר 2022 בפורמט הקודם: אותה תוכנית (מצתים ונוזל קירור כתובים כטקסט ולא בטבלה)"),),
       specs=dict(TY_OIL_NEW, tires="215/60 R17 או 225/50 R18", spare="ערכת תיקון", **HYB))
toyota("toyota-yaris-2011-2019-1.33-1.5", 311, "Yaris", "יאריס", "XP130", [2011, 2019], ["1.33 (1NR-FE)", "1.5 (2NR-FKE, 2017+)"], "petrol", extra_sheets=(314,),
       specs=dict(TY_OIL_OLD, oil_capacity="3.4 ליטר (1.33) / 3.1 ליטר (1.5), לפי הגיליון", coolant="Toyota SLLC, 4.8 ליטר", tires="175/65 R15 או 185/60 R15", battery="מצבר רגיל 12V", spare="גלגל חלופי צר או ערכת תיקון",
                  brake_fluid="SAE J1704 / FMVSS 116 DOT 4"),
       notes_extra="שני גיליונות (2011-2017 מנוע 1NR-FE, 2017-2019 מנוע 2NR-FKE) עם אותה טבלה. שמן CVT: Toyota Genuine CVT Fluid FE / TC.")
toyota("toyota-yaris-2012-2019-1.5-hybrid", 312, "Yaris", "יאריס", "XP130 hybrid", [2012, 2019], ["1.5 hybrid (1NZ-FXE)"], "hybrid",
       specs=dict(TY_OIL_OLD, tires="175/65 R15 או 185/60 R15", spare="ערכת תיקון או גלגל חלופי צר", **HYB),
       notes_extra="מרווח שסתומים: בדיקה ב-90,000 (72 חודשים). נוזל קירור ממיר מתח: בדיקה כל 30,000.")
# Yaris XP210: the sheets the importer's app lists for Yaris 2021 (336) and Yaris Hybrid 2021 (335) are
# headed Yaris Cross MXPB10 / MXPJ10. The Yaris's own sheets (MXPA11 / MXPH11) are 320 and 321 (2020)
# and 355 / 356 (2023 on), so those carry the plan.
toyota("toyota-yaris-2020-2025-1.5", 320, "Yaris", "יאריס", "XP210 (MXPA11)", [2020, 2022], ["1.5 (M15A-FKS)"], "petrol",
       extra_sheets=((336, "רשום באפליקציית היבואן ליאריס 2021-2023 אך כותרתו יאריס קרוס MXPB10 (יולי 2021): אותה תוכנית, בלי בדיקת תופי בלם אחוריים"),),
       specs=dict(TY_OIL_NEW, tires="185/65 R15 או 205/45 R17", battery="מצבר רגיל 12V", spare="ערכת תיקון"),
       notes_extra="מ-2023 לוח נפרד toyota-yaris-2023-2025-1.5 (גיליון 355), כי בו מסנן המזגן מוחלף בכל טיפול. שם הקובץ נשאר עם 2025 כדי לא לשבור קישורים קיימים.")
toyota("toyota-yaris-2023-2025-1.5", 355, "Yaris", "יאריס", "XP210 (MXPA11)", [2023, 2025], ["1.5 (M15A-FKS)"], "petrol",
       specs=dict(TY_OIL_NEW, tires="185/65 R15 או 205/45 R17", battery="מצבר רגיל 12V", spare="ערכת תיקון"),
       notes_extra="גיליון יולי 2023. לעומת גיליון 2020: מסנן מזגן מוחלף בכל טיפול (במקום ניקוי והחלפה לסירוגין), אין שורת תופי בלם, "
                   "ומצתים, רצועת הינע ונוזל הקירור מסומנים בטבלה (אותם מרווחים).")
toyota("toyota-yaris-2020-2025-1.5-hybrid", 321, "Yaris", "יאריס", "XP210 hybrid (MXPH11)", [2020, 2022], ["1.5 hybrid (M15A-FXE)"], "hybrid",
       extra_sheets=((335, "רשום באפליקציית היבואן ליאריס היברידית 2021 אך מסומן MXPJ10 (שלדת יאריס קרוס, יולי 2021): אותה תוכנית, בלי בדיקת תופי בלם אחוריים"),),
       specs=dict(TY_OIL_NEW, tires="185/65 R15 או 205/45 R17", spare="ערכת תיקון", **HYB),
       notes_extra="מ-2023 לוח נפרד toyota-yaris-2023-2025-1.5-hybrid (גיליון 356). שם הקובץ נשאר עם 2025 כדי לא לשבור קישורים קיימים.")
toyota("toyota-yaris-2023-2025-1.5-hybrid", 356, "Yaris", "יאריס", "XP210 hybrid (MXPH11)", [2023, 2025], ["1.5 hybrid (M15A-FXE)"], "hybrid",
       specs=dict(TY_OIL_NEW, tires="185/65 R15 או 205/45 R17", spare="ערכת תיקון", **HYB),
       notes_extra="גיליון יוני 2023. לעומת גיליון 2020: מסנן מזגן מוחלף בכל טיפול, צינורות פליטה נבדקים בכל טיפול, אין שורת תופי בלם, "
                   "ומצתים ונוזל הקירור מסומנים בטבלה (אותם מרווחים).")
toyota("toyota-yaris-cross-2021-2025-1.5-hybrid", 340, "Yaris Cross", "יאריס קרוס", "XP210", [2021, 2025], ["1.5 hybrid (M15A-FXE)"], "hybrid",
       extra_sheets=((354, "גיליון יולי 2023 בפורמט החדש: אותה תוכנית (מצתים ונוזל קירור מסומנים בטבלה)"),),
       specs=dict(TY_OIL_NEW, tires="205/65 R16 או 215/50 R18", spare="ערכת תיקון", **HYB))
toyota("toyota-yaris-cross-2021-2025-1.5", 341, "Yaris Cross", "יאריס קרוס", "XP210", [2021, 2022], ["1.5 (M15A-FKS)"], "petrol",
       extra_sheets=((336, "גיליון יולי 2021 (MXPB10): מסנן מזגן בניקוי והחלפה לסירוגין ומסנן דלק רק ב-120,000; הגיליון מספטמבר 2022 מחליף אותו"),),
       specs=dict(TY_OIL_NEW, tires="205/65 R16 או 215/50 R18", battery="מצבר רגיל 12V", spare="ערכת תיקון"),
       notes_extra="מ-2023 לוח נפרד toyota-yaris-cross-2023-2025-1.5 (גיליון 353). שם הקובץ נשאר עם 2025 כדי לא לשבור קישורים קיימים.")
toyota("toyota-yaris-cross-2023-2025-1.5", 353, "Yaris Cross", "יאריס קרוס", "XP210", [2023, 2025], ["1.5 (M15A-FKS)"], "petrol",
       specs=dict(TY_OIL_NEW, tires="205/65 R16 או 215/50 R18", battery="מצבר רגיל 12V", spare="ערכת תיקון"),
       notes_extra="גיליון יולי 2023. לעומת גיליון 2022: מסנן דלק מוחלף ב-120,000 בלבד (במקום 75,000 ו-150,000), "
                   "ומצתים, רצועת הינע ונוזל קירור מסומנים בטבלה.")
toyota("toyota-auris-2013-2019-1.6", 281, "Auris", "אוריס", "E180", [2013, 2019], ["1.6 (1ZR-FAE)"], "petrol",
       specs=dict(TY_OIL_OLD, tires="205/55 R16", battery="מצבר רגיל 12V", spare="גלגל חלופי צר"))
toyota("toyota-auris-2011-2019-1.8-hybrid", 280, "Auris", "אוריס", "E180 hybrid", [2013, 2019], ["1.8 hybrid (2ZR-FXE)"], "hybrid",
       specs=dict(TY_OIL_OLD, tires="205/55 R16 או 225/45 R17", spare="ערכת תיקון או גלגל חלופי צר", **HYB),
       notes_extra="לשנים 2011-2012 לוח נפרד toyota-auris-2011-2012-1.8-hybrid (גיליון 282). שם הקובץ נשאר כדי לא לשבור קישורים קיימים.")
toyota("toyota-auris-2011-2012-1.8-hybrid", 282, "Auris", "אוריס", "E150 hybrid", [2011, 2012], ["1.8 hybrid (2ZR-FXE)"], "hybrid",
       specs=dict(TY_OIL_OLD, tires="205/55 R16 או 225/45 R17", spare="ערכת תיקון או גלגל חלופי צר", **HYB),
       notes_extra="לעומת גיליון 2013-2019: מסנן מזגן מנוקה בטיפולי הביניים ומוחלף כל 30,000, וצינורות הפליטה ובדיקת החלודה כל 30,000 (לא בכל טיפול).")
toyota("toyota-rav4-2013-2019-2.0", 307, "RAV4", "ראב 4", "XA40", [2013, 2019], ["2.0 (3ZR-FAE / לפי הגיליון 1ZR-FAE)"], "petrol",
       specs=dict(TY_OIL_OLD, tires="225/65 R17 או 235/55 R18", battery="מצבר רגיל 12V", spare="גלגל חלופי צר"), notes_extra="גיליון 4x4: כולל שמן דיפרנציאל ותיבת העברה.")
toyota("toyota-rav4-2016-2019-2.5-hybrid", 308, "RAV4", "ראב 4", "XA40 hybrid", [2016, 2019], ["2.5 hybrid (2AR-FXE)"], "hybrid",
       specs=dict(TY_OIL_OLD, tires="225/65 R17 או 235/55 R18", spare="גלגל חלופי צר", **HYB))
toyota("toyota-rav4-2020-2025-2.0", 325, "RAV4", "ראב 4", "XA50", [2020, 2022], ["2.0 (M20A-FKS)"], "petrol",
       specs=dict(TY_OIL_NEW, tires="225/65 R17 או 235/55 R19", battery="מצבר רגיל 12V", spare="גלגל חלופי צר"),
       notes_extra="מ-2023 לוח נפרד toyota-rav4-2023-2025-2.0 (גיליון 351). שם הקובץ נשאר עם 2025 כדי לא לשבור קישורים קיימים.")
toyota("toyota-rav4-2023-2025-2.0", 351, "RAV4", "ראב 4", "XA50 (MXAA5#)", [2023, 2025], ["2.0 (M20A-FKS)"], "petrol",
       specs=dict(TY_OIL_NEW, tires="225/65 R17 או 235/55 R19", battery="מצבר רגיל 12V", spare="גלגל חלופי צר"),
       notes_extra="גיליון יולי 2023. לעומת גיליון 2018: מסנן מזגן מוחלף בכל טיפול, מסנן דלק מוחלף ב-120,000, נוזל קירור מוחלף ב-150,000 ואז כל 75,000 (במקום 90,000), "
                   "וב-4x4 שמן תיבת העברה ודיפרנציאל אחורי מוחלפים כל 30,000 ובורגי גלי ההינע מהודקים כל 15,000.")
toyota("toyota-rav4-2020-2025-2.5-hybrid", 324, "RAV4", "ראב 4", "XA50 hybrid", [2020, 2022], ["2.5 hybrid (A25A-FXS)"], "hybrid",
       specs=dict(TY_OIL_NEW, tires="225/65 R17 או 235/55 R19", spare="גלגל חלופי צר", **HYB),
       notes_extra="מ-2023 לוח נפרד toyota-rav4-2023-2025-2.5-hybrid (גיליון 350). שם הקובץ נשאר עם 2025 כדי לא לשבור קישורים קיימים.")
toyota("toyota-rav4-2023-2025-2.5-hybrid", 350, "RAV4", "ראב 4", "XA50 hybrid (AXAH/AXAL)", [2023, 2025], ["2.5 hybrid (A25A-FXS)"], "hybrid",
       specs=dict(TY_OIL_NEW, tires="225/65 R17 או 235/55 R19", spare="גלגל חלופי צר", **HYB),
       notes_extra="גיליון יולי 2023. לעומת גיליון 2018: מסנן מזגן מוחלף בכל טיפול, מסנן דלק מוחלף ב-120,000, נוזלי הקירור מוחלפים כל 75,000 אחרי ההחלפה הראשונה (במקום 90,000), "
                   "נוזל בלמים נבדק גם בטיפולי הביניים, מסנן הסוללה ההיברידית נבדק ומנוקה לסירוגין, ויש שורה לנוזל תיבת ההילוכים של המנוע החשמלי האחורי (AWD).")
toyota("toyota-c-hr-2017-2019-1.2", 285, "C-HR", "C-HR", "AX10", [2017, 2019], ["1.2 turbo (8NR-FTS)"], "petrol",
       specs=dict(TY_OIL_OLD, tires="215/60 R17 או 225/50 R18", battery="מצבר רגיל 12V", spare="ערכת תיקון"))
toyota("toyota-c-hr-2016-2023-1.8-hybrid", 326, "C-HR", "C-HR", "AX10 hybrid", [2016, 2023], ["1.8 hybrid (2ZR-FXE)"], "hybrid",
       extra_sheets=((286, "גיליון 2016-2019: אותה תוכנית, בלי שורת מסנן האוויר של הסוללה ההיברידית"),),
       specs=dict(TY_OIL_NEW, tires="215/60 R17 או 225/50 R18", spare="ערכת תיקון", **HYB),
       notes_extra="הדור השני (AX20, 2024 ואילך) בלוח נפרד toyota-c-hr-2024-2025-1.8-hybrid (גיליון 362).")
toyota("toyota-c-hr-2024-2025-1.8-hybrid", 362, "C-HR", "C-HR", "AX20 hybrid (ZYX20)", [2024, 2025], ["1.8 hybrid (2ZR-FXE)"], "hybrid",
       extra_sheets=(361,),
       specs=dict(TY_OIL_NEW, oil_capacity="4.2 ליטר (לפי הגיליון)", coolant="Toyota SLLC: מנוע 5.5 ליטר, מערכת היברידית 1.5 ליטר (לפי הגיליון)", spare="ערכת תיקון", **HYB),
       notes_extra="הדור השני של C-HR (ZYX20), גיליון דצמבר 2023. לעומת הדור הקודם: מסנן מזגן מוחלף בכל טיפול, מסנן דלק מוחלף ב-120,000, "
                   "מצתים ב-90,000, ואחרי ההחלפה הראשונה נוזלי הקירור מוחלפים כל 75,000. גרסת הפלאג-אין 2.0 (M20A) לא נכללת.")
toyota("toyota-camry-2013-2019-2.5-hybrid", 291, "Camry", "קאמרי", "XV50 hybrid", [2013, 2019], ["2.5 hybrid (2AR-FXE)"], "hybrid",
       specs=dict(TY_OIL_OLD, tires="215/55 R17", spare="גלגל חלופי צר", **HYB))
toyota("toyota-camry-2020-2025-2.5-hybrid", 319, "Camry", "קאמרי", "XV70 hybrid", [2020, 2023], ["2.5 hybrid (A25A-FXS)"], "hybrid",
       specs=dict(TY_OIL_NEW, tires="215/55 R17 או 235/45 R18", spare="גלגל חלופי צר", **HYB),
       notes_extra="הדור הבא (XV80, 2024 ואילך) בלוח נפרד toyota-camry-2024-2025-2.5-hybrid (גיליון 363). שם הקובץ נשאר עם 2025 כדי לא לשבור קישורים קיימים.")
toyota("toyota-camry-2024-2025-2.5-hybrid", 363, "Camry", "קאמרי", "XV80 hybrid (AXVH80)", [2024, 2025], ["2.5 hybrid (A25A-FXS)"], "hybrid",
       specs=dict(TY_OIL_NEW, spare="גלגל חלופי צר", **HYB),
       notes_extra="גיליון ספטמבר 2024. לעומת גיליון XV70: מסנן מזגן מוחלף בכל טיפול, מסנן דלק מוחלף ב-75,000 וב-150,000 (במקום 120,000), "
                   "מסנן הסוללה ההיברידית נבדק ומנוקה לסירוגין, ומצתים ונוזל קירור מסומנים בטבלה.")
toyota("toyota-aygo-x-2022-2025-1.0", 344, "Aygo X", "איגו X", "AB70", [2022, 2025], ["1.0 (1KR-FE)"], "petrol",
       extra_sheets=((339, "גיליון ספטמבר 2022: אותה תוכנית, אבל מרווח השסתומים נבדק רק ב-90,000 (72 חודשים) ולא בכל טיפול"),),
       specs=dict(TY_OIL_NEW, tires="175/65 R17 או 175/60 R18", battery="מצבר רגיל 12V", spare="ערכת תיקון"))
toyota("toyota-aygo-2014-2022-1.0", 284, "Aygo", "איגו", "AB40", [2014, 2022], ["1.0 (1KR-FE)"], "petrol", extra_sheets=(318,),
       specs=dict(TY_OIL_OLD, tires="165/65 R14 או 165/60 R15", battery="מצבר רגיל 12V", spare="ערכת תיקון"))


# --- diesel pickups / SUVs, hybrids and older models (sheets found in the second pass) ---
TY_DIESEL = dict(TY_OIL_OLD, engine_oil="שמן דיזל לפי טבלת הנוזלים בגיליון (ACEA C2/C5 0W-30 / 5W-30 בדורות החדשים)", fuel="סולר", timing="שרשרת",
                 brake_fluid="DOT 3 / DOT 4 (FMVSS 116)")
TY_4X4_NOTE = "רכב 4x4: שמן דיפרנציאלים ותיבת העברה ופעולות גירוז/הידוק גל הינע מופיעים בגיליון; בגיליון גם שורות 'מחמירה' תכופות יותר לנהיגת שטח."
toyota("toyota-avensis-2009-2018-1.6-2.0", 283, "Avensis", "אוונסיס", "T270", [2009, 2018], ["1.6 (1ZR-FAE)", "1.8 (2ZR-FAE)", "2.0 (3ZR-FAE)"], "petrol",
       specs=dict(TY_OIL_OLD, tires="215/55 R17", battery="מצבר רגיל 12V"))
toyota("toyota-hilux-2005-2015-2.5-3.0-diesel", 295, "Hilux", "היילקס", "AN10/AN20/AN30 (Vigo)", [2005, 2015], ["2.5 D-4D (2KD-FTV)", "3.0 D-4D (1KD-FTV)"], "diesel",
       extra_sheets=((296, "גיליון הגיר האוטומטי: נוזל גיר אוטומטי במקום שמן גיר ידני, ושורות רצועת התזמון והבדיקות מעט שונות"),),
       notes_extra="הלוח לפי גיליון 295 (גיר ידני). " + TY_4X4_NOTE, specs=TY_DIESEL)
toyota("toyota-hilux-2015-2019-2.4-2.8-diesel", 293, "Hilux", "היילקס", "AN120/AN130", [2015, 2019], ["2.4 D-4D (2GD-FTV)", "2.8 D-4D (1GD-FTV)"], "diesel",
       extra_sheets=((292, "4x4 Euro 5 (1GD): אותה תוכנית"), (294, "4x2: אותה תוכנית בלי תיבת העברה וגומיות ציריות קדמיות")),
       notes_extra="גיליון 293 = 4x4 Euro 6. " + TY_4X4_NOTE, specs=TY_DIESEL)
toyota("toyota-hilux-2020-2025-2.4-2.8-diesel", 329, "Hilux", "היילקס", "AN120 facelift", [2020, 2022], ["2.4 D-4D (2GD-FTV)", "2.8 D-4D (1GD-FTV)"], "diesel",
       notes_extra="מ-2023 לוח נפרד toyota-hilux-2023-2025-2.4-2.8-diesel (גיליון 357). שם הקובץ נשאר עם 2025 כדי לא לשבור קישורים קיימים. " + TY_4X4_NOTE, specs=TY_DIESEL)
toyota("toyota-hilux-2023-2025-2.4-2.8-diesel", 357, "Hilux", "היילקס", "AN120 facelift (GUN125/126/135)", [2023, 2025], ["2.4 D-4D (2GD-FTV)", "2.8 D-4D (1GD-FTV)"], "diesel",
       notes_extra="גיליון יולי 2023. לעומת הגיליון הקודם: מסנן מזגן מוחלף כל 20,000 בלי ניקוי ביניים, אין שורת תופי בלם וצינורות מצנן, "
                   "צנרת בלמים, הגה ומשאבת ואקום נבדקים בכל טיפול, ונוזל קירור מוחלף ב-160,000 ואז כל 80,000. מסנן הדלק מוחלף כשמופיעה נורת התראה. " + TY_4X4_NOTE, specs=TY_DIESEL)
toyota("toyota-hilux-2026-2.8-mhev-diesel", 368, "Hilux", "היילקס", "AN120 48V MHEV", [2026, 2026], ["2.8 D-4D 48V (1GD-FTV)"], "diesel",
       notes_extra="כולל תמיסת AdBlue ובדיקת DPF. " + TY_4X4_NOTE, specs=TY_DIESEL)
toyota("toyota-land-cruiser-2003-2009-3.0-diesel", 297, "Land Cruiser", "לנד קרוזר", "J120 (Prado)", [2003, 2009], ["3.0 D-4D (1KD-FTV)"], "diesel",
       notes_extra=TY_4X4_NOTE, specs=TY_DIESEL)
toyota("toyota-land-cruiser-2010-2015-3.0-diesel", 298, "Land Cruiser", "לנד קרוזר", "J150", [2010, 2015], ["3.0 D-4D (1KD-FTV)"], "diesel",
       notes_extra=TY_4X4_NOTE, specs=TY_DIESEL)
toyota("toyota-land-cruiser-2016-2019-2.8-diesel", 299, "Land Cruiser", "לנד קרוזר", "J150 facelift", [2016, 2019], ["2.8 D-4D (1GD-FTV)"], "diesel",
       notes_extra=TY_4X4_NOTE, specs=TY_DIESEL)
toyota("toyota-land-cruiser-2009-2019-4.0", 300, "Land Cruiser", "לנד קרוזר", "J150 petrol", [2009, 2019], ["4.0 V6 (1GR-FE)"], "petrol",
       notes_extra=TY_4X4_NOTE, specs=dict(TY_OIL_OLD, fuel="בנזין 95 אוקטן"))
toyota("toyota-land-cruiser-2020-2024-2.8-diesel", 365, "Land Cruiser", "לנד קרוזר", "J150 (GDJ150)", [2020, 2024], ["2.8 D-4D (1GD-FTV)"], "diesel",
       extra_sheets=((323, "גיליון ישן יותר לאותן שנים (GDJ150 יורו 6): מסנן מזגן מנוקה בטיפולי הביניים, מסנן אוויר בבדיקה כל 10,000 והחלפה כל 30,000 (כתוב כטקסט), ושורות הבלמים והדיפרנציאל שונות; הלוח לפי הגיליון החדש מיולי 2023"),),
       notes_extra=TY_4X4_NOTE, specs=dict(TY_DIESEL, oil_capacity="7.7 ליטר (לפי הגיליון)", coolant="Toyota SLLC, 12 ליטר (לפי הגיליון)"))
toyota("toyota-land-cruiser-2025-2026-2.8-diesel", 364, "Land Cruiser", "לנד קרוזר", "J250 (GDJ250)", [2025, 2026], ["2.8 D-4D (1GD-FTV)"], "diesel",
       notes_extra=TY_4X4_NOTE, specs=TY_DIESEL)
toyota("toyota-prius-2004-2009-1.5-hybrid", 301, "Prius", "פריוס", "XW20", [2004, 2009], ["1.5 hybrid (1NZ-FXE)"], "hybrid", specs=dict(TY_OIL_OLD, **HYB))
toyota("toyota-prius-2009-2015-1.8-hybrid", 302, "Prius", "פריוס", "XW30", [2009, 2015], ["1.8 hybrid (2ZR-FXE)"], "hybrid", specs=dict(TY_OIL_OLD, **HYB))
toyota("toyota-prius-2016-2022-1.8-hybrid", 303, "Prius", "פריוס", "XW50", [2016, 2022], ["1.8 hybrid (2ZR-FXE)"], "hybrid",
       extra_sheets=((328, "גיליון 2020-2021 (ZVW50/52): אותם מרווחי החלפה; בדיקות השלדה, הבלמים והפליטה כל 30,000 במקום בכל טיפול, ונוזל הגיר נבדק כל 60,000"),), specs=dict(TY_OIL_NEW, **HYB))
toyota("toyota-prius-2023-2025-2.0-hybrid", 348, "Prius", "פריוס", "XW60", [2023, 2025], ["2.0 hybrid (M20A-FXS)"], "hybrid", specs=dict(TY_OIL_NEW, **HYB))
toyota("toyota-prius-plug-in-2012-2017-1.8-hybrid", 304, "Prius Plug-in", "פריוס פלאג-אין", "XW35 PHV", [2012, 2017], ["1.8 plug-in hybrid (2ZR-FXE)"], "plug-in-hybrid", specs=dict(TY_OIL_OLD, **HYB))
toyota("toyota-prius-plug-in-2023-2025-2.0-hybrid", 349, "Prius Plug-in", "פריוס פלאג-אין", "XW60 PHEV", [2023, 2025], ["2.0 plug-in hybrid (M20A-FXS)"], "plug-in-hybrid", specs=dict(TY_OIL_NEW, **HYB))
toyota("toyota-prius-plus-2013-2021-1.8-hybrid", 305, "Prius+", "פריוס פלוס", "ZVW40", [2013, 2021], ["1.8 hybrid (2ZR-FXE)"], "hybrid", specs=dict(TY_OIL_OLD, **HYB))
toyota("toyota-verso-2009-2018-1.6-1.8", 310, "Verso", "ורסו", "AR20", [2009, 2018], ["1.6 (1ZR-FAE)", "1.8 (2ZR-FAE)"], "petrol", specs=TY_OIL_OLD)
toyota("toyota-verso-s-2010-2016-1.33", 309, "Verso-S (Space Verso)", "ספייס ורסו", "XP120", [2010, 2016], ["1.33 (1NR-FE)"], "petrol", specs=TY_OIL_OLD)
toyota("toyota-highlander-2021-2025-2.5-hybrid", 322, "Highlander", "היילנדר", "XU70", [2021, 2022], ["2.5 hybrid (A25A-FXS)"], "hybrid", specs=dict(TY_OIL_NEW, **HYB),
       notes_extra="מ-2023 לוח נפרד toyota-highlander-2023-2025-2.5-hybrid (גיליון 347). שם הקובץ נשאר עם 2025 כדי לא לשבור קישורים קיימים.")
toyota("toyota-highlander-2023-2025-2.5-hybrid", 347, "Highlander", "היילנדר", "XU70 (AXUH78)", [2023, 2025], ["2.5 hybrid (A25A-FXS)"], "hybrid", specs=dict(TY_OIL_NEW, **HYB),
       notes_extra="גיליון יולי 2023. לעומת גיליון 2020: מסנן מזגן מוחלף בכל טיפול, מסנן הסוללה ההיברידית נבדק ומנוקה לסירוגין, "
                   "בדיקות השלדה בכל טיפול, ואין שורה לשמן הדיפרנציאל. מצתים, מסנן דלק ונוזל קירור מסומנים בטבלה.")
toyota("toyota-camry-2011-2019-2.5", 290, "Camry", "קאמרי", "XV50", [2011, 2019], ["2.5 (2AR-FE)"], "petrol", specs=TY_OIL_OLD)
toyota("toyota-aygo-2005-2013-1.0", 288, "Aygo", "איגו", "AB10", [2005, 2013], ["1.0 (1KR-FE)"], "petrol", specs=TY_OIL_OLD)
toyota("toyota-yaris-2006-2011-1.0-1.3", 313, "Yaris", "יאריס", "XP90", [2006, 2011], ["1.0 (1KR-FE)", "1.33 (1NR-FE, 2009+)"], "petrol", specs=TY_OIL_OLD,
       notes_extra="מנוע 2SZ-FE (1.3) בלוח נפרד toyota-yaris-2006-2009-1.3-2sz (גיליון 315).")
toyota("toyota-yaris-2006-2009-1.3-2sz", 315, "Yaris", "יאריס", "XP90", [2006, 2009], ["1.3 (2SZ-FE)"], "petrol", specs=TY_OIL_OLD,
       notes_extra="גיליון מנוע 2SZ-FE. לעומת גיליון 1KR/1NR: מצתים רגילים, בדיקה כל 30,000 והחלפה כל 60,000 (במקום אירידיום כל 90,000), "
                   "ובדיקת מרווח שסתומים ב-90,000.")
toyota("toyota-bz4x-2022-2025-ev", 342, "bZ4X", "bZ4X", "XEAM10", [2022, 2025], ["EV (1XM / 1YM)"], "electric",
       extra_sheets=((359, "גיליון יולי 2023: אותם פריטים בטבלה מלאה עד 150,000 (בגיליון הראשי עמודות עד 90,000); החלפה ראשונה של נוזלי הקירור ב-200,000 במקום 195,000"),),
       specs={"_note": "רכב חשמלי: אין שמן מנוע; נוזל קירור סוללה ותיבת הינע לפי הגיליון", "brake_fluid": "DOT 3 / DOT 4", **HYB})

print("done")

# ===================== Hyundai / Kia: tables parsed from the Hebrew owner's books =====================
# data/sources/hk-tables.json is produced by scripts/hk_table_parse.py from the importer PDFs.
# Each row: one I/R/-/. per km column (ascending). The books come in two templates:
#   family 15: columns 15,30,...,120 (x1000 km)         -> 8 services of 15,000 km
#   family 30: columns 30,60,...,240 (x1000 km)         -> 16 services of 15,000 km; the book's oil note
#              ("החלף כל 15,000 ק\"מ או 12 חודשים") puts oil+filter in every 15,000 km service
HK_TABLES = json.load(open(os.path.join(ROOT, "sources", "hk-tables.json"), encoding="utf-8"))["books"]
KIA_INTERVAL = {"url": "https://kia-israel.co.il/טיפול-ותחזוקה/טיפולים-לרכב", "kind": "importer", "note": "הצהרת קיה ישראל: טיפול תקופתי כל 15,000 ק\"מ או שנה"}
HY_INTERVAL = {"url": "https://www.hyundaimotors.co.il/maintenance/", "kind": "importer", "note": "ספריית ספרי הרכב של כלמוביל (הורדת ספר לפי דגם); טיפול כל 15,000 ק\"מ או שנה"}
HK_MAP = [
    (r"שמן מנוע|ומסנן שמן|מסנן שמן\+", ["engine_oil", "oil_filter"]),
    (r"HSG|מחולל התנעה", ["hsg_belt"]),
    (r"רצועות? ה?הנעה|חגורות הינע|רצועת ההנעה|רצועת4", ["drive_belt"]),
    (r"מרווח שסתומים", ["valve_clearance"]),
    (r"ואקום|וואקום|אוורור", ["vacuum_hose"]),
    (r"נוזל מפעיל|נוזל iMT|מנגנון .*iMT|נוזל תיבת חכמה מפעיל", ["clutch_actuator_fluid"]),
    (r"צינור .{0,25}וקו|צינור גמיש וצינור קשיח של נוזל מפעיל|צינור בוכנת מצמד|מפעיל מצמד המנוע$|צינורות גמישים וקשיחים של מפעיל", ["clutch"]),
    (r"גל .{0,8}הינע.*ושרוולים|גל הינע ושרוולים", ["cv_boots"]),
    (r"ידנית", ["manual_gearbox_oil"]),
    (r"כפולת מצמדים|DCT", ["dct_oil"]),
    (r"אוטומטית", ["transmission_oil"]),
    (r"גל מדחף|גל הינע \(AWD\)|גל הינע \(4WD\)|\(4WD\) גל הינע|גל הינע \( הינע בכל הגלגלים|\(AWD\) בנזין$|\(AWD\) דיזל$", ["propshaft"]),
    (r"גל הינע|גלי הינע|ציריות", ["cv_boots"]),
    (r"דיפרנציאל", ["differential_oil"]),
    (r"תיבת העברה", ["transfer_case_oil"]),
    (r"מסנן האוויר של מי|מסנן אוויר מכל ה?דלק|אוויר למיכל דלק|מסנן מיכל אוויר|מסנן הדלק האוויר של מיכל|אוויר של מיכל הדלק", ["fuel_tank_air_filter"]),
    (r"צינורות דלק|קווי דלק|צינורות .{0,20}דלק|דלק קשיחים", ["fuel_lines"]),
    (r"צינור אדים|צינור האדים|מכסה מי|מכסה התדלוק|מילוי הדלק|מכסה פתח|צינור מיכל הדלק האדים|צינור הדלק אדים|ומ § סה מי", ["evap_system"]),
    (r"מסנן הדלק|מסנן דלק|סינון של מסנן", ["fuel_filter"]),
    (r"בקרת|האקלים|תא הנוסעים|מסנן מזגן|מסנן מער|מסנן אוויר של מער", ["cabin_filter"]),
    (r"מסנן אוויר|מסנן אויר|אטם הגומי של מסנן", ["air_filter"]),
    (r"מצנן ביניים|ליניקת|יניקת אוויר|כניסת אוויר|צינור גמיש לכניסה", ["intercooler_pipes"]),
    (r"מערכת ה?קירור|כת קירור|כת הקירור", ["cooling_system"]),
    (r"פליטה", ["exhaust"]),
    (r"קרר|מדחס|חס מ", ["ac_system"]),
    (r"דיסקים ורפידות|בלמי דיסק|צלחות ורפידות|דיסקיות ור|פידות של הבלמים|פידות בלימה|רפידות בלימה|פידותI", ["brake_pads", "brake_discs"]),
    (r"תופי בלם|בלמי תוף|תופי בלמים", ["brake_drums"]),
    (r"נוזל ה?בלמים", ["brake_fluid"]),
    (r"צינורות בלמים|קווי בלמים|הצינורות הקשיחים|הצינורות והחיבורים|צינורות .{0,15}בלמים|ת בלמים צינורות|הגמישים והחיבורים|הצינורות הצינורות", ["brake_lines"]),
    (r"דוושת בלם|דוושת בלמ", ["pedals"]),
    (r"בלם חני|בלם הפעלה חניה", ["parking_brake"]),
    (r"היגוי|מסרק|פס משונן|תיבת הגה|בת הגה|בת ההגה", ["steering"]),
    (r"מפרקים|מפרקי המתלה|מתלה קד|מתלים|כת מתלים", ["suspension"]),
    (r"צמיג", ["tires"]),
    (r"מצבר", ["battery_12v"]),
    (r"ברגים ואומים|חיזוק אומים|השלדה|בשלד", ["body_underside"]),
    (r"מערכות החשמל|כות החשמליות", ["electrical_system"]),
    (r"אוריאה", ["adblue"]),
    (r"מצתים", ["spark_plugs"]),
]
HK_SKIP = re.compile(r"תוספי דלק|^בנזין$|^דיזל$|^\s*$|למעט|עבור (סין|מקסיקו|אוסטרליה|המזרח)|ובניו|וניו עבור|פרט התיכון|מסנן דלק עבור סין|מסנן דלק \) בנזין \( עבור")
def hk_items(label):
    for rx, items in HK_MAP:
        if re.search(rx, label):
            return items
    return None
def hk(id_, brand, book, pages, model, model_he, gen, years, engines, fuel, family, url, book_note, extra_notes="",
       specs=None, long=(), overrides=None, oil_every_service=True, status="reviewed", drop=(), interval_page=None, ncols=None, brand_note=None,
       add_rows=()):
    """add_rows: (item, pattern) rows read from the book by eye where the parser lost them (same column
    layout as the parsed table, before the family-30 spread)."""
    b = HK_TABLES[book]; overrides = overrides or {}
    cols = [15000 * i for i in range(1, (ncols or (8 if family == 15 else 16)) + 1)]
    rows = []; skipped = []; seen = set()
    for pg in b["pages"]:
        if pg["page"] not in pages:
            continue
        for r in pg["rows"]:
            lab = r["label"].strip(); pat = r["pattern"].replace(".", "-")
            if not re.search(r"[IR]", pat):
                continue
            if lab in overrides:
                items = overrides[lab]
            elif HK_SKIP.search(lab):
                skipped.append((lab, pat)); continue
            else:
                items = hk_items(lab)
            if not items:
                skipped.append((lab, pat)); continue
            if items == "skip":
                continue
            if family == 30:
                pat = "".join("-" + ch for ch in pat)
            for it in items:
                if it in drop or (it, pat) in seen:
                    continue
                seen.add((it, pat)); rows.append((it, pat))
    for it, pat in add_rows:
        rows.append((it, "".join("-" + ch for ch in pat) if family == 30 else pat))
    if oil_every_service:
        rows = [(it, p) for it, p in rows if it not in ("engine_oil", "oil_filter")]
        rows = [("engine_oil", "R" * len(cols)), ("oil_filter", "R" * len(cols))] + rows
    services = grid(cols, rows)
    for svc in services:
        dd = {}
        for e in svc["items"]:
            k = (e["item"], e["action"])
            if k in dd:
                continue
            dd[k] = e
        svc["items"] = list(dd.values())
    if skipped:
        print(f"  [{id_}] rows not used: " + "; ".join(f"{l[:45]!r}={p}" for l, p in skipped))
    interval_src = interval_page or (KIA_INTERVAL if brand is KIA else HY_INTERVAL)
    if family == 30 and ncols:
        raise ValueError("ncols is only for 15,000-km tables")
    tmpl = ("טבלת הספר בנויה בעמודות של 15,000 ק\"מ." if family == 15 else
            "טבלת הספר בנויה בעמודות של 30,000 ק\"מ; הספר מציין החלפת שמן ומסנן כל 15,000 ק\"מ או 12 חודשים, ולכן הלוח מוצג בצעדי 15,000 ופריטי הטבלה נופלים על הטיפולים הזוגיים.")
    write({
        **brand, "id": id_, "model": model, "model_he": model_he, "generation": gen, "years": years, "engines": engines, "fuel": fuel,
        "interval": {"km": 15000, "months": 12, "note": "לפי ספר הרכב של היבואן: 15,000 ק\"מ או 12 חודשים, המוקדם מביניהם; בתנאי הפעלה קשים שמן ומסנן כל 7,500 ק\"מ או 6 חודשים"},
        "cycle_km": cols[-1], "services": services, "long_interval": list(long), "time_based": [],
        "specs": specs or {"_note": "לאימות מול הספר"},
        "sources": [{"url": url, "kind": "importer", "note": f"{book_note} (טבלת התחזוקה בעמודי PDF {min(pages) + 1}-{max(pages) + 1})"}, interval_src],
        "status": status,
        "notes": (f"הועתק מטבלת 'תכנית תחזוקה רגילה' בספר הרכב בעברית של היבואן. {tmpl} I בדיקה, R החלפה. " + extra_notes).strip(),
    })

KB = "https://cdnmedia.kia-israel.co.il/www/cars-book/"
COOL_KIA = long_("coolant", "replace", first_km=210000, first_months=120, then_every_km=30000, then_every_months=24, note="נוזל קירור מנוע: החלפה ראשונה 210,000 ק\"מ או 120 חודשים, אחר כך כל 30,000 או 24 חודשים")
COOL_KIA_180 = long_("coolant", "replace", first_km=180000, first_months=120, then_every_km=30000, then_every_months=24)
BELT_KIA = long_("drive_belt", "inspect", first_km=90000, first_months=72, then_every_km=30000, then_every_months=24, note="רצועת הנעה: בדיקה ראשונה 90,000/72 חודשים ואחר כך כל 30,000/24")
COOLSYS_KIA = long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24)
KIA_SPECS = {"_note": "לפי ספר הרכב; לאימות נפחים", "engine_oil": "לפי הספר: שמן מנוע העונה למפרט ACEA A5/B5 או API SN לפי המנוע (בנזין); 0W-20/5W-30", "coolant": "נוזל קירור מבוסס אתילן-גליקול לפי קיה (פוספט), מדולל 50%", "brake_fluid": "DOT 4", "fuel": "בנזין 95 אוקטן", "tire_pressure": "לפי המדבקה בעמוד דלת הנהג"}

hk("kia-stonic-2018-2025-1.0-1.4", KIA, "kia-Stonic_Facelift_2021.pdf", [484, 485], "Stonic", "סטוניק", "YB (facelift 2021)", [2018, 2025],
   ["1.0 T-GDi (Smartstream G1.0, 48V MHEV 2021+)", "1.2 MPI (G1.2)", "1.4 MPI"], "petrol", 15, KB + "Stonic_Facelift_2021.pdf",
   "ספר רכב סטוניק פייסליפט 2021-2025 (קיה ישראל)",
   overrides={"48V HEV T-GDi G1.0 Smartstream": ["drive_belt"]},
   long=[COOL_KIA, BELT_KIA, COOLSYS_KIA, long_("spark_plugs", "replace", every_km=75000, note="1.0 T-GDi; מנועי 1.2/1.4 MPI: כל 150,000"),
         long_("manual_gearbox_oil", "replace", every_km=120000, note="בתנאי הפעלה קשים בלבד"), long_("dct_oil", "replace", every_km=120000, note="בתנאי הפעלה קשים בלבד"),
         long_("transmission_oil", "replace", every_km=100000, note="גיר אוטומטי, בתנאי הפעלה קשים בלבד")],
   extra_notes="הספר הוא של הפייסליפט (2021+); דגמי 2018-2020 עם אותם מנועים משתמשים באותה תכנית. תוספי דלק: כל 15,000 ק\"מ לפי הספר.", specs=KIA_SPECS)
hk("kia-stonic-2026-1.0-mhev", KIA, "kia-Stonic_PE_2026.pdf", [408, 409], "Stonic", "סטוניק", "YB PE (2026)", [2026, 2026],
   ["1.0 T-GDi 48V MHEV (Smartstream G1.0, Euro 7)"], "petrol", 15, KB + "Stonic_PE_2026.pdf", "ספר רכב סטוניק 2026 (קיה ישראל)",
   long=[COOL_KIA_180, BELT_KIA, long_("spark_plugs", "replace", every_km=75000), long_("hsg_belt", "replace", every_km=105000, first_months=None) if False else long_("drive_belt", "replace", every_km=105000, note="לפי הספר: החלפה כל 105,000")],
   extra_notes="הטבלה בספר מודפסת עם עמודת מיילים (10-80) ועמודת ק\"מ (15-120); נעשה שימוש בעמודת הק\"מ.", specs=KIA_SPECS)
hk("kia-rio-2017-2020-1.0-1.4", KIA, "kia-Rio-YB-2018.pdf", [435, 436, 437], "Rio", "ריו", "YB", [2017, 2020],
   ["1.0 T-GDi (Kappa)", "1.2 MPI (Kappa)", "1.4 MPI (Kappa)"], "petrol", 15, KB + "Rio-YB-2018.pdf", "ספר רכב ריו 2018+ (קיה ישראל)",
   long=[COOL_KIA, BELT_KIA, COOLSYS_KIA, long_("spark_plugs", "replace", every_km=75000, note="1.0 T-GDi; 1.2/1.4 MPI: כל 150,000"),
         long_("transmission_oil", "replace", every_km=90000, note="בתנאי הפעלה קשים בלבד"), long_("manual_gearbox_oil", "replace", every_km=120000, note="בתנאי הפעלה קשים בלבד"), long_("dct_oil", "replace", every_km=120000, note="בתנאי הפעלה קשים בלבד")],
   extra_notes="הטבלה בספר מודפסת עם עמודת מיילים ועמודת ק\"מ (15-120); נעשה שימוש בעמודת הק\"מ. גם ספר ריו 2017 (Rio-SC-2017.PDF) באותה תכנית.", specs=KIA_SPECS)
hk("kia-rio-2021-2024-1.0-1.4", KIA, "kia-Rio-OM-2022.pdf", [518, 519, 520], "Rio", "ריו", "YB facelift", [2021, 2024],
   ["1.0 T-GDi 48V MHEV (Smartstream G1.0)", "1.2 MPI (Smartstream G1.2)", "1.4 MPI"], "petrol", 15, KB + "Rio-OM-2022.pdf", "ספר רכב ריו 2022 (קיה ישראל)",
   overrides={"HEV G1.0 48V T-GDi Smartstream": ["drive_belt"]},
   long=[COOL_KIA, BELT_KIA, COOLSYS_KIA, long_("spark_plugs", "replace", every_km=75000, note="1.0 T-GDi; 1.2/1.4 MPI: כל 150,000"),
         long_("manual_gearbox_oil", "replace", every_km=120000, note="בתנאי הפעלה קשים בלבד"), long_("transmission_oil", "replace", every_km=90000, note="בתנאי הפעלה קשים בלבד"), long_("dct_oil", "replace", every_km=120000, note="בתנאי הפעלה קשים בלבד")],
   specs=KIA_SPECS)
hk("kia-seltos-2020-2026-1.6-2.0", KIA, "kia-Seltos-2020.pdf", [498, 499], "Seltos", "סלטוס", "SP2", [2020, 2026],
   ["1.6 MPI / 1.6 T-GDI (Gamma)", "2.0 MPI (Nu / Smartstream G2.0)"], "petrol", 15, KB + "Seltos-2020.pdf", "ספר רכב סלטוס 2020+ (קיה ישראל)",
   overrides={"MPI 2.0 Nu": ["valve_clearance"]},
   long=[long_("coolant", "replace", first_km=100000, first_months=60, then_every_km=30000, then_every_months=24), long_("spark_plugs", "replace", every_km=75000, note="1.6 T-GDI; 2.0 MPI: כל 150,000"),
         long_("transmission_oil", "replace", every_km=90000, note="בתנאי הפעלה קשים בלבד"), long_("manual_gearbox_oil", "replace", every_km=120000, note="בתנאי הפעלה קשים בלבד"), long_("dct_oil", "replace", every_km=120000, note="בתנאי הפעלה קשים בלבד")],
   status="draft",
   extra_notes="הטבלה בספר בעמודות של 15,000 ק\"מ, אבל שורת שמן המנוע בספר אומרת 'החלף כל 10,000 ק\"מ או 12 חודשים' (ספר מבוסס-הודו). קיה ישראל מצהירה על 15,000; הלוח הולך לפי הטבלה. לאימות מול היבואן, לכן draft.", specs=KIA_SPECS)
hk("kia-sportage-2022-2025-1.6-2.0", KIA, "kia-Sportage_NQ5_2022.pdf", [450, 451], "Sportage", "ספורטאז'", "NQ5", [2022, 2025],
   ["1.6 T-GDi (Smartstream G1.6, 48V MHEV)", "2.0 MPI (Smartstream G2.0)"], "petrol", 30, KB + "Sportage_NQ5_2022.pdf", "ספר רכב ספורטאז' 2022+ (קיה ישראל)",
   long=[COOL_KIA, long_("drive_belt", "inspect", every_km=15000, every_months=12, note="בדיקה בכל טיפול; החלפה כל 105,000 ק\"מ או 48 חודשים"), long_("drive_belt", "replace", every_km=105000, every_months=48),
         long_("spark_plugs", "replace", every_km=75000, note="1.6 T-GDi; 2.0 MPI: כל 150,000"), long_("transmission_oil", "replace", every_km=90000, note="בתנאי הפעלה קשים בלבד"),
         long_("differential_oil", "replace", every_km=120000, note="AWD, בתנאי הפעלה קשים"), long_("transfer_case_oil", "replace", every_km=120000, note="AWD, בתנאי הפעלה קשים")],
   extra_notes="גרסת הדיזל 1.6 CRDi (עמ' 456-457 בספר) לא נכללה בלוח זה.", specs=KIA_SPECS)
hk("kia-sportage-2022-2024-1.6-hybrid", KIA, "kia-Sportage_HEV-PHEV_2022.pdf", [430], "Sportage", "ספורטאז'", "NQ5 HEV/PHEV", [2022, 2024],
   ["1.6 T-GDi hybrid (Smartstream G1.6, G4FT)", "1.6 T-GDi plug-in hybrid"], "hybrid", 30, KB + "Sportage_HEV-PHEV%202022.pdf", "ספר רכב ספורטאז' היברידי/פלאג-אין 2022 (קיה ישראל)",
   long=[COOL_KIA, long_("coolant", "replace", first_km=210000, first_months=120, then_every_km=30000, then_every_months=24, note="נוזל קירור המערכת ההיברידית (מעגל נפרד)"),
         long_("hsg_belt", "inspect", every_km=15000, every_months=12), long_("hsg_belt", "replace", every_km=105000, every_months=48), long_("spark_plugs", "replace", every_km=75000),
         long_("transmission_oil", "replace", every_km=90000, note="בתנאי הפעלה קשים בלבד"), long_("differential_oil", "replace", every_km=120000, note="AWD, בתנאי הפעלה קשים"), long_("transfer_case_oil", "replace", every_km=120000, note="AWD, בתנאי הפעלה קשים")],
   extra_notes="PHEV: פריט נוסף בספר עם החלפה כל 60,000 ק\"מ או 36 חודשים (הערה 4 בספר; לא זוהה בוודאות).", specs=dict(KIA_SPECS, battery="מצבר עזר 12V + סוללת מתח גבוה"))
hk("kia-sportage-2025-2026-1.6-hybrid", KIA, "kia-Sportage-Hybrid-2026.pdf", [480], "Sportage", "ספורטאז'", "NQ5 facelift HEV/PHEV", [2025, 2026],
   ["1.6 T-GDi hybrid (G4FT / G4FZ)", "1.6 T-GDi plug-in hybrid"], "hybrid", 30, KB + "Sportage-Hybrid-2026.pdf", "ספר רכב ספורטאז' היברידי 2026 (קיה ישראל)",
   long=[COOL_KIA_180, long_("coolant", "replace", first_km=180000, first_months=120, then_every_km=30000, then_every_months=24, note="נוזל קירור המערכת ההיברידית"),
         long_("drive_belt", "replace", every_km=75000, note="רצועת ההנעה של משאבת המים: החלפה כל 75,000 לפי הספר"), long_("spark_plugs", "replace", every_km=60000, note="לפי הספר: כל 60,000"),
         long_("transmission_oil", "replace", every_km=90000, note="בתנאי הפעלה קשים בלבד"), long_("differential_oil", "replace", every_km=120000, note="AWD, בתנאי הפעלה קשים"), long_("transfer_case_oil", "replace", every_km=120000, note="AWD, בתנאי הפעלה קשים")],
   extra_notes="ספר גלובלי עם טבלאות לכמה שווקים; נעשה שימוש בטבלה הראשית (עמ' 481 ב-PDF) בעמודות של 30,000 ק\"מ, עם הערת שמן כל 15,000.", specs=dict(KIA_SPECS, battery="מצבר עזר 12V + סוללת מתח גבוה"))
hk("kia-sorento-2021-2026-2.5-2.2", KIA, "kia-Sorento-MQ4-GSL-DSL-2021.pdf", [621, 622, 623], "Sorento", "סורנטו", "MQ4", [2021, 2026],
   ["2.5 MPI (Smartstream G2.5)", "3.5 MPI (Smartstream G3.5)", "2.2 CRDi (Smartstream D2.2)"], "petrol-or-diesel", 30, KB + "Sorento-MQ4-GSL-DSL-2021.pdf", "ספר רכב סורנטו 2021+ בנזין/דיזל (קיה ישראל)",
   long=[COOL_KIA, BELT_KIA, long_("drive_belt", "inspect", first_km=90000, first_months=48, then_every_km=30000, then_every_months=24, note="דיזל D2.2"),
         long_("spark_plugs", "replace", every_km=165000, note="מנועי בנזין"), long_("timing_belt", "inspect", every_km=120000, note="דיזל: בדיקת רצועת התזמון כל 120,000, החלפה כל 240,000 לפי הספר"),
         long_("transmission_oil", "replace", every_km=90000, note="בתנאי הפעלה קשים בלבד"), long_("dct_oil", "replace", every_km=120000, note="בתנאי הפעלה קשים בלבד"),
         long_("differential_oil", "replace", every_km=120000, note="AWD, בתנאי הפעלה קשים"), long_("transfer_case_oil", "replace", every_km=120000, note="AWD, בתנאי הפעלה קשים")],
   extra_notes="דיזל 2.2: שמן ומסנן כל 30,000 ק\"מ או 24 חודשים לפי הספר (הלוח מציג 15,000 לפי מנועי הבנזין; ברכב דיזל אפשר לדלג על הטיפולים האי-זוגיים לשמן). ההיברידי 1.6 (2022+) בספר נפרד שלא עובד.", specs=KIA_SPECS)
hk("kia-sorento-2015-2020-2.4-2.2", KIA, "kia-Sorento-UMPE-2019-2020.pdf", [151, 152, 153, 154], "Sorento", "סורנטו", "UM", [2015, 2020],
   ["2.4 GDI / MPI (Theta II)", "3.5 MPI (Lambda II)", "2.0 / 2.2 CRDi"], "petrol-or-diesel", 30, KB + "Sorento-UMPE-2019-2020.pdf", "ספר רכב סורנטו 2019-2020 (קיה ישראל)",
   overrides={"בנזין מנוע II Theta 2.4 ליטר": ["engine_oil", "oil_filter"], "דיזל מנוע 2.0 ליטר": ["engine_oil", "oil_filter"], "דיזל מנוע 2.2 ליטר": ["engine_oil", "oil_filter"],
              "בנזין MPI מנוע II Theta 2.4 ליטר": ["valve_clearance"], "בנזין MPI מנוע II Lambda 3.5 ליטר": ["valve_clearance"]},
   long=[COOL_KIA, long_("spark_plugs", "replace", every_km=40000, note="2.4 MPI לפי הספר; GDI: כל 150,000"),
         long_("transmission_oil", "replace", every_km=90000, note="בתנאי הפעלה קשים בלבד"), long_("manual_gearbox_oil", "replace", every_km=120000, note="בתנאי הפעלה קשים בלבד"),
         long_("differential_oil", "replace", every_km=120000, note="AWD, בתנאי הפעלה קשים"), long_("transfer_case_oil", "replace", every_km=120000, note="AWD, בתנאי הפעלה קשים")],
   extra_notes="הספר הוא לשנתונים 2019-2020 (פייסליפט UM); הדור UM נמכר מ-2015.", specs=KIA_SPECS)
hk("kia-niro-2023-2024-1.6-plug-in-hybrid", KIA, "kia-NIRO_PHEV_General_Heb_01_פלאגאין.pdf", [459], "Niro", "נירו", "SG2 PHEV", [2023, 2024],
   ["1.6 GDI plug-in hybrid (Smartstream G1.6, G4LL)"], "plug-in-hybrid", 15, KB + "NIRO_PHEV_General_Heb_01_%D7%A4%D7%9C%D7%90%D7%92%D7%90%D7%99%D7%9F.pdf", "ספר רכב נירו פלאג-אין 2023+ (קיה ישראל)",
   long=[COOL_KIA_180, long_("coolant", "replace", every_km=60000, every_months=36, note="נוזל קירור ממיר/מערכת היברידית (PHEV): כל 60,000 ק\"מ או 36 חודשים לפי הספר"),
         long_("clutch_actuator_fluid", "replace", every_km=40000), long_("hsg_belt", "inspect", every_km=15000, every_months=12), long_("hsg_belt", "replace", every_km=105000),
         long_("spark_plugs", "replace", every_km=150000), long_("dct_oil", "replace", every_km=120000, note="בתנאי הפעלה קשים בלבד")],
   status="draft",
   extra_notes="ספר גלובלי עם כמה טבלאות אזוריות. בדיקה חוזרת (סבב 2) מצאה שייתכן שהטבלה שנבחרה (עמ' 460 ב-PDF) היא של אוסטרליה/ניו זילנד ולא 'except Europe' (עמ' 457-458); לאמת לפני סימון reviewed.", specs=dict(KIA_SPECS, battery="מצבר עזר 12V + סוללת מתח גבוה"))
hk("kia-niro-plus-2022-2024-1.6-hybrid", KIA, "kia-Niro-Plus-HEV-PHEV-OM-2022.pdf", [342, 343], "Niro Plus", "נירו פלוס", "DE (Niro Plus) HEV/PHEV", [2022, 2024],
   ["1.6 GDI hybrid / plug-in hybrid (Kappa, G4LE)"], "hybrid", 15, KB + "Niro-Plus-HEV-PHEV-OM-2022.pdf", "ספר רכב נירו פלוס היברידי/פלאג-אין 2022 (קיה ישראל)",
   long=[COOL_KIA_180, long_("clutch_actuator_fluid", "replace", every_km=40000, every_months=24), long_("hsg_belt", "inspect", every_km=15000, every_months=12), long_("hsg_belt", "replace", every_km=105000, every_months=48),
         long_("spark_plugs", "replace", every_km=150000), long_("dct_oil", "replace", every_km=120000, note="בתנאי הפעלה קשים בלבד")],
   specs=dict(KIA_SPECS, battery="מצבר עזר 12V + סוללת מתח גבוה"))
hk("kia-carnival-2021-2026-2.2-3.5", KIA, "kia-Carnival-KA4-2021.pdf", [639, 640], "Carnival", "קרניבל", "KA4", [2021, 2026],
   ["2.2 CRDi (Smartstream D2.2)", "3.5 MPI (Smartstream G3.5)"], "petrol-or-diesel", 30, KB + "Carnival-KA4-2021.pdf", "ספר רכב קרניבל 2021+ (קיה ישראל)",
   overrides={"בנזין": "skip"},
   long=[COOL_KIA, long_("drive_belt", "inspect", first_km=80000, first_months=48, then_every_km=20000, then_every_months=12), long_("spark_plugs", "replace", every_km=165000, note="3.5 בנזין"),
         long_("timing_belt", "inspect", every_km=120000, note="דיזל: בדיקה כל 120,000, החלפה כל 240,000 לפי הספר"),
         long_("transmission_oil", "replace", every_km=90000, note="בתנאי הפעלה קשים בלבד"), long_("fuel_filter", "replace", every_km=30000, note="דיזל: לפי הספר החלפה כל 30,000 (הערה 8)")],
   extra_notes="לפי הספר שמן ומסנן כל 15,000 ק\"מ או 12 חודשים גם לדיזל.", specs=dict(KIA_SPECS, fuel="סולר / בנזין 95"))
print("done hk")

# ---- Hyundai books (rotated landscape tables; labels come out fragmented but the km grid is reliable) ----
HB = "https://res.cloudinary.com/colmobil/images/"
HY_SPECS = {"_note": "לפי ספר הרכב; נפחים לאימות", "engine_oil": "לפי הספר: ACEA A5/B5 או API SN/SP; 0W-20 / 5W-30 לפי המנוע", "coolant": "נוזל קירור מבוסס אתילן-גליקול (פוספט) לפי יונדאי, מדולל 50%", "brake_fluid": "DOT 4", "fuel": "בנזין 95 אוקטן", "tire_pressure": "לפי המדבקה בעמוד דלת הנהג"}
COOL_HY = long_("coolant", "replace", first_km=200000, first_months=120, then_every_km=30000, then_every_months=24, note="החלפה ראשונה 200,000 ק\"מ או 120 חודשים, אחר כך כל 30,000 או 24 חודשים")
COOL_HY_40 = long_("coolant", "replace", first_km=200000, first_months=120, then_every_km=40000, then_every_months=24)
COOL_HY_210 = long_("coolant", "replace", first_km=210000, first_months=120, then_every_km=30000, then_every_months=24)
COOL_HY_195 = long_("coolant", "replace", first_km=195000, first_months=120, then_every_km=30000, then_every_months=24)
COOLSYS_HY = long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24)
COOLSYS_HY_40 = long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=40000, then_every_months=24)
BELT_HY = long_("drive_belt", "inspect", first_km=90000, first_months=72, then_every_km=30000, then_every_months=24)
hk("hyundai-kona-2018-2020-1.6-turbo", HY, "hy-kona-2018-2020.pdf", [420, 422, 423], "Kona", "קונה", "OS", [2018, 2020],
   ["1.6 T-GDI (Gamma, G4FJ)", "1.0 T-GDI"], "petrol", 15, HB + "v1716384260/ספר-רכב-יונדאי-קונה-טורבו-2018-2020_7711bdb91/ספר-רכב-יונדאי-קונה-טורבו-2018-2020_7711bdb91.pdf",
   "ספר רכב יונדאי קונה טורבו 2018-2020 (כלמוביל)",
   overrides={"T-GDI שמן מנוע ומסנן שמן3 * 2": ["engine_oil", "oil_filter"], "*1 חגורות הינע": ["drive_belt"]},
   long=[COOL_HY_40, COOLSYS_HY, long_("spark_plugs", "replace", every_km=75000, every_months=60), long_("dct_oil", "replace", every_km=100000, note="בתנאי הפעלה קשים בלבד")],
   extra_notes="הטבלה בספר מודפסת לרוחב; חלק מהשורות (מסנן דלק, מצתים) מופיעות כטקסט ולכן נרשמו ב-long_interval.", specs=HY_SPECS)
hk("hyundai-kona-2021-2023-1.6-turbo", HY, "hy-kona-2021.pdf", [493, 495, 496, 497], "Kona", "קונה", "OS facelift", [2021, 2023],
   ["1.6 T-GDI (Smartstream G1.6, G4FP)", "1.0 T-GDI (G3LE)"], "petrol", 15, HB + "v1716384256/ספר-רכב-יונדאי-קונה-טורבו-2021_7712f86ce/ספר-רכב-יונדאי-קונה-טורבו-2021_7712f86ce.pdf",
   "ספר רכב יונדאי קונה טורבו 2021 (כלמוביל)",
   overrides={"3* ֳשמן מנוע ומסנן שמן2*": ["engine_oil", "oil_filter"], "חגורות הינע1*": ["drive_belt"]},
   long=[COOL_HY, COOLSYS_HY_40, long_("spark_plugs", "replace", every_km=75000), long_("dct_oil", "replace", every_km=100000, note="בתנאי הפעלה קשים בלבד")],
   extra_notes="הטבלה בספר מודפסת לרוחב; פריטים שמופיעים כטקסט נרשמו ב-long_interval.", specs=HY_SPECS)
hk("hyundai-elantra-2022-2026-1.6-hybrid", HY, "hy-elantra-hybrid-1.pdf", [490, 491, 492, 493], "Elantra", "אלנטרה", "CN7 hybrid", [2022, 2026],
   ["1.6 GDI hybrid (Smartstream G1.6, G4LE)"], "hybrid", 15, HB + "v1716189028/ספר-רכב-יונדאי-אלנטרה-היברידית-1/ספר-רכב-יונדאי-אלנטרה-היברידית-1.pdf",
   "ספר רכב יונדאי אלנטרה היברידית (כלמוביל)",
   overrides={"תוספי דלק * 4": "skip"},
   # p. 9-9: vapour hose / filler cap and fuel lines are I at 60 and 120 (rows lost by the parser)
   add_rows=[("evap_system", "---I---I"), ("fuel_lines", "---I---I")],
   long=[long_("coolant", "replace", first_km=195000, first_months=120, then_every_km=30000, then_every_months=24, note="נוזל קירור מנוע/ממיר (שורה אחת בספר)"),
         long_("clutch_actuator_fluid", "replace", every_km=30000, every_months=24),
         long_("hsg_belt", "inspect", every_km=15000, every_months=12), long_("hsg_belt", "replace", every_km=105000, every_months=48), long_("spark_plugs", "replace", every_km=150000),
         long_("dct_oil", "replace", every_km=120000, note="בתנאי הפעלה קשים בלבד")],
   extra_notes="נוזל בוכנת המצמד מוחלף כל 30,000 ק\"מ או 24 חודשים; צינור בוכנת המצמד נבדק בכל טיפול. סוללת מערכת eCall (אם קיימת): החלפה כל 3 שנים. "
               "מערכת הקירור נבדקת בכל טיפול לפי הטבלה, בלי מרווח 60,000/30,000 נפרד. שורות צינור האדים וקווי הדלק (בדיקה ב-60,000 וב-120,000) הוזנו ידנית מעמ' 9-9.",
   specs=dict(HY_SPECS, battery="מצבר עזר 12V + סוללת מתח גבוה"))
hk("hyundai-venue-2020-2026-1.6", HY, "hy-venue-2024.pdf", [397, 398, 399], "Venue", "ונו", "QX", [2020, 2026],
   ["1.6 MPI (Smartstream G1.6, G4FM)"], "petrol", 15, HB + "v1727680821/Hyundai_Venue_2024_OM_web/Hyundai_Venue_2024_OM_web.pdf", "ספר רכב יונדאי ונו 2024 (כלמוביל)",
   long=[COOL_HY_195, BELT_HY, COOLSYS_HY, long_("spark_plugs", "replace", every_km=160000), long_("transmission_oil", "replace", every_km=90000, note="בתנאי הפעלה קשים בלבד")],
   extra_notes="גם ספר ונו 2020-2021 באותה תכנית (מצתים 160,000; תוסף דלק כל 15,000).", specs=HY_SPECS)
hk("hyundai-sonata-2015-2019-2.0-hybrid", HY, "hy-sonata-hybrid-2015-2017.pdf", [338, 339, 340, 341], "Sonata", "סונטה", "LF hybrid", [2015, 2019],
   ["2.0 GDI hybrid (Nu, G4NG)"], "hybrid", 15, HB + "v1716389111/יונדאי-סונטה-היברידית-ספר-רכב-שנים-2015-2017_4614a8466/יונדאי-סונטה-היברידית-ספר-רכב-שנים-2015-2017_4614a8466.pdf",
   "ספר רכב יונדאי סונטה היברידית 2015-2017 (כלמוביל)",
   overrides={"*1 שמן מנוע ומסנן שמן": ["engine_oil", "oil_filter"], "*5 מסנן דלק": ["fuel_filter"]},
   long=[long_("coolant", "replace", first_km=105000, first_months=60, then_every_km=45000, note="לפי הספר: החלפה ראשונה 105,000/60 חודשים ואחר כך כל 45,000"), COOLSYS_HY,
         long_("spark_plugs", "replace", every_km=165000), long_("hsg_belt", "inspect", every_km=15000, every_months=12), long_("hsg_belt", "replace", every_km=105000, every_months=48),
         long_("transmission_oil", "replace", every_km=100000, note="בתנאי הפעלה קשים בלבד")],
   extra_notes="ספר 2018 זהה.", specs=dict(HY_SPECS, battery="מצבר עזר 12V + סוללת מתח גבוה"))
hk("hyundai-sonata-2020-2023-2.0-hybrid", HY, "hy-sonata-hybrid-2021.pdf", [468, 469, 470, 471], "Sonata", "סונטה", "DN8 hybrid", [2020, 2023],
   ["2.0 GDI hybrid (Smartstream G2.0, G4NR)"], "hybrid", 15, HB + "v1716389103/יודאי-סונטה-היברידית-ספר-רכב-שנה-2021_461602813/יודאי-סונטה-היברידית-ספר-רכב-שנה-2021_461602813.pdf",
   "ספר רכב יונדאי סונטה היברידית 2021 (כלמוביל)",
   overrides={"*1 שמן מנוע ומסנן שמן": ["engine_oil", "oil_filter"]},
   long=[COOL_HY_210, COOLSYS_HY, long_("spark_plugs", "replace", every_km=160000), long_("transmission_oil", "replace", every_km=100000, note="בתנאי הפעלה קשים בלבד")],
   specs=dict(HY_SPECS, battery="מצבר עזר 12V + סוללת מתח גבוה"))
hk("hyundai-sonata-2024-2026-2.0-hybrid", HY, "hy-sonata-2024.pdf", [465, 466, 467, 468], "Sonata", "סונטה", "DN8 facelift hybrid", [2024, 2026],
   ["2.0 GDI hybrid (Smartstream G2.0, G4NR)"], "hybrid", 15, HB + "v1731938134/Sonata_OM_2024_LR/Sonata_OM_2024_LR.pdf", "ספר רכב יונדאי סונטה 2024 (כלמוביל)",
   overrides={"תוספי דלק * 2": "skip"},
   long=[COOL_HY_210, long_("hsg_belt", "inspect", every_km=15000, every_months=12), long_("hsg_belt", "replace", every_km=105000), long_("spark_plugs", "replace", every_km=150000),
         long_("transmission_oil", "replace", every_km=100000, note="בתנאי הפעלה קשים בלבד")],
   specs=dict(HY_SPECS, battery="מצבר עזר 12V + סוללת מתח גבוה"))
hk("hyundai-santa-fe-2019-2020-2.4-2.2", HY, "hy-santafe-2019-2020.pdf", [589, 590, 591], "Santa Fe", "סנטה פה", "TM", [2019, 2020],
   ["2.4 GDI (Theta II, G4KJ)", "3.5 MPI", "2.2 CRDi (D4HB)"], "petrol-or-diesel", 15, HB + "v1716388807/ספר-רכב-סנטה-פה-2019-2020_5052df246/ספר-רכב-סנטה-פה-2019-2020_5052df246.pdf",
   "ספר רכב יונדאי סנטה פה 2019-2020 (כלמוביל)",
   overrides={"*מסנן דלק5": ["fuel_filter"], "*9 (4WD) שמן דיפרנציאל אחורי": ["differential_oil"]},
   long=[COOL_HY_40, COOLSYS_HY, long_("spark_plugs", "replace", every_km=160000, every_months=120, note="2.4 MPI/GDI, 3.5 MPI"),
         long_("transmission_oil", "replace", every_km=90000, note="בתנאי הפעלה קשים בלבד"), long_("differential_oil", "replace", every_km=120000, note="4WD, בתנאי הפעלה קשים")],
   extra_notes="עמודי הדיזל (594-596 ב-PDF): מסנן דלק ובדיקת רצועה בתדירות שונה; הלוח מבוסס על טבלת הבנזין.", specs=HY_SPECS)
hk("hyundai-santa-fe-2021-2023-2.5-2.2", HY, "hy-santafe-2021.pdf", [579, 580, 583, 584], "Santa Fe", "סנטה פה", "TM facelift", [2021, 2023],
   ["2.5 GDI / 2.5 T-GDI (Smartstream)", "1.6 T-GDI hybrid", "2.2 CRDi (Smartstream D2.2)"], "petrol-or-diesel", 15, HB + "v1716388803/ספר-רכב-סנטה-פה-2021_505372a45/ספר-רכב-סנטה-פה-2021_505372a45.pdf",
   "ספר רכב יונדאי סנטה פה 2021 (כלמוביל)",
   overrides={"שמן מנוע ומסנן שמן2* ,1*": ["engine_oil", "oil_filter"], "חגורות הינע3*": ["drive_belt"], "*מסנן דלק8": ["fuel_filter"]},
   long=[COOL_HY, COOLSYS_HY, long_("spark_plugs", "replace", every_km=160000), long_("transmission_oil", "replace", every_km=90000, note="בתנאי הפעלה קשים בלבד"),
         long_("dct_oil", "replace", every_km=100000, note="בתנאי הפעלה קשים בלבד"), long_("differential_oil", "replace", every_km=120000, note="4WD, בתנאי הפעלה קשים"), long_("transfer_case_oil", "replace", every_km=120000, note="4WD, בתנאי הפעלה קשים")],
   specs=HY_SPECS)
hk("hyundai-santa-fe-2024-2026-1.6-hybrid", HY, "hy-santafe-hybrid-2025.pdf", [588, 589, 590, 591], "Santa Fe", "סנטה פה", "MX5 hybrid", [2024, 2026],
   ["1.6 T-GDI hybrid (Smartstream G1.6, G4FT)"], "hybrid", 15, HB + "v1742998775/SantaFe-HEV_OM_2025_web/SantaFe-HEV_OM_2025_web.pdf", "ספר רכב יונדאי סנטה פה היברידית 2025 (כלמוביל)",
   overrides={"תיכון למעט מזרח": "skip"},
   long=[COOL_HY_195, long_("coolant", "replace", first_km=195000, first_months=120, then_every_km=30000, then_every_months=24, note="נוזל קירור המערכת ההיברידית"),
         long_("spark_plugs", "replace", every_km=70000, note="לפי הספר: כל 70,000"), long_("hsg_belt", "replace", every_km=100000), long_("transmission_oil", "replace", every_km=100000, note="בתנאי הפעלה קשים בלבד"),
         long_("differential_oil", "replace", every_km=120000, note="AWD, בתנאי הפעלה קשים"), long_("transfer_case_oil", "replace", every_km=120000, note="AWD, בתנאי הפעלה קשים")],
   status="draft", extra_notes="הספר (מהדורת 2025) נוקב בכמה מרווחים של 10,000 ק\"מ ('החלף כל 10,000') לצד טבלה של 15,000; לאימות מול היבואן.", specs=dict(HY_SPECS, battery="מצבר עזר 12V + סוללת מתח גבוה"))
hk("hyundai-bayon-2022-2025-1.0-turbo", HY, "hy-bayon-2022.pdf", [446, 447, 448, 449], "Bayon", "באיון", "BC3 CUV", [2022, 2025],
   ["1.0 T-GDI (Smartstream G1.0, G3LE/G3LF, 48V)", "1.2 MPI"], "petrol", 15, HB + "v1716388083/ספר-רכב-יונדאי-באיון-2022_56661b991/ספר-רכב-יונדאי-באיון-2022_56661b991.pdf", "ספר רכב יונדאי באיון 2022 (כלמוביל)",
   overrides={"3* ֳשמן מנוע ומסנן שמן2*": ["engine_oil", "oil_filter"], "*מסנן דלק7": ["fuel_filter"]},
   long=[COOL_HY, BELT_HY, COOLSYS_HY_40, long_("spark_plugs", "replace", every_km=75000, every_months=60), long_("dct_oil", "replace", every_km=100000, note="בתנאי הפעלה קשים בלבד")],
   specs=HY_SPECS)
hk("hyundai-i20-2022-2025-1.0-1.2", HY, "hy-i20-2024.pdf", [436, 437, 438, 439], "i20", "i20", "BC3", [2022, 2025],
   ["1.0 T-GDI (Smartstream G1.0, G3LC/G3LE, 48V)", "1.2 MPI (G4LC/G4LF)"], "petrol", 15, HB + "v1716190865/ספר-רכב-יונדאי-i20-2024/ספר-רכב-יונדאי-i20-2024.pdf", "ספר רכב יונדאי i20 2024 (כלמוביל)",
   overrides={"3* ֳשמן מנוע ומסנן שמן2*": ["engine_oil", "oil_filter"], "*מסנן דלק7": ["fuel_filter"]},
   long=[COOL_HY, BELT_HY, COOLSYS_HY_40, long_("spark_plugs", "replace", every_km=150000, every_months=120, note="1.2 MPI; 1.0 T-GDI: 75,000"), long_("dct_oil", "replace", every_km=100000, note="בתנאי הפעלה קשים בלבד")],
   specs=HY_SPECS)
hk("hyundai-tucson-2025-2026-1.6-hybrid", HY, "hyundai-tucson-hybrid-2025.pdf", [544, 545], "Tucson", "טוסון", "NX4 facelift hybrid", [2025, 2026],
   ["1.6 T-GDI hybrid (Smartstream G1.6, G4FT)"], "hybrid", 15, HB + "v1756290337/tucso-hybrid-2025-hebrew-web-low/tucso-hybrid-2025-hebrew-web-low.pdf", "ספר רכב יונדאי טוסון היברידי 2025 (כלמוביל)",
   overrides={"מסנן שמן+ שמן מנוע1,2*": ["engine_oil", "oil_filter"], "רצועת4*HSG": ["hsg_belt"], "מסנן אויר": ["air_filter"]},
   long=[long_("coolant", "replace", first_km=150000, first_months=120, then_every_km=30000, then_every_months=24), long_("hsg_belt", "replace", every_km=105000),
         long_("transmission_oil", "replace", every_km=100000, note="בתנאי הפעלה קשים בלבד")],
   extra_notes="הספר מציין מסנן אוויר: החלפה בכל טיפול (R בכל עמודה).", specs=dict(HY_SPECS, battery="מצבר עזר 12V + סוללת מתח גבוה"))
print("done hyundai")

# ---- Mitsubishi (כלמוביל): only the Outlander 2021+ Hebrew book carries a maintenance table ----
MI = {"make": "Mitsubishi", "make_he": "מיצובישי", "importer": "כלמוביל"}
MI_HUB = {"url": "https://www.mitsubishi-israel.co.il/car_books/", "kind": "importer", "note": "ספריית ספרי הרכב של מיצובישי ישראל (בחירת דגם ושנה; הקבצים ב-res.cloudinary.com/colmobil)"}
hk("mitsubishi-outlander-2021-2026-2.5", MI, "mitsu-ספר_רכב_מיצובישי_אאוטלנדר-2021-2024.pdf", [431, 432], "Outlander", "אאוטלנדר", "GN (4th gen)", [2021, 2026],
   ["2.5 MIVEC (PR25DD)"], "petrol", 15, "https://res.cloudinary.com/colmobil/images/v1722236766/ספר-רכב-מיצובישי-אאוטלנדר_1267488853/ספר-רכב-מיצובישי-אאוטלנדר_1267488853.pdf",
   "ספר רכב מיצובישי אאוטלנדר 2021-2024 (כלמוביל), פרק 9 'לוח תחזוקה'", ncols=15, interval_page=MI_HUB,
   overrides={"* 2 גומיות גלי הינע , אתר נזק": ["cv_boots"], "5 שמן דיפרנציאל ( #4 )": ["differential_oil"], "1 יישור גלגלים": ["wheel_alignment"], "2 נסיעת מבחן": "skip",
              "* 3 בלמים צינורות , אתר נזילות": ["brake_lines"], "רפידות וצלחות , בדוק שחיקה": ["brake_pads", "brake_discs"], "4 צינורות דלק , אתר נזילות": ["fuel_lines"],
              "1 חופש דוושת הבלמים ודוושת המצמד": ["pedals"], "4 צינורות מצנן , בדוק נזק וחיבור נכון": ["coolant_hoses"], "5 נוזל קירור מנוע ( #2 ,) ( #3 )": ["coolant"],
              "6 חיבורי צינורות המפלט , אתר דליפות גז ובדוק את ההתקנה": ["exhaust"], "7 נוזל בלמים ונוזל מצמד": ["brake_fluid"], "8 מצבר": ["battery_12v"],
              "* 2 מסנ ן אוויר בתא הנוסעים": ["cabin_filter"], "* 1 נוזל תיבת הילוכים אוטומטית ( כולל נוזל תיבת ההילוכים הרציפה )": ["cvt_oil"]},
   long=[long_("drive_belt", "inspect", every_km=15000, every_months=12, note="רצועות V: החלפה אם פגומות או כשהמותחן האוטומטי בקצה"),
         long_("spark_plugs", "replace", every_km=90000, every_months=72, note="מצתי אירידיום"),
         long_("coolant", "replace", first_km=150000, first_months=120, then_every_km=75000, then_every_months=60),
         long_("air_filter", "replace", every_km=30000, every_months=24, note="ניקוי כל 15,000 ק\"מ או שנה"),
         long_("fuel_filter", "replace", every_km=165000, every_months=132),
         long_("suspension", "inspect", every_km=30000, every_months=24, note="מערכת המתלה, מפרקים כדוריים וגומיות הגנה"),
         long_("steering", "inspect", every_km=15000, every_months=12, note="מוט קישור, אטמים וגומיות"),
         long_("transfer_case_oil", "replace", every_km=180000, every_months=144, note="4WD; לפי הספר אין צורך בטיפול עד 180,000 ק\"מ או 12 שנים"),
         long_("differential_oil", "replace", every_km=75000, every_months=60, note="בגרירה/גגון/כבישים משובשים: החלפה כל 30,000 ק\"מ או שנה"),
         long_("wheel_alignment", "inspect", every_km=30000, every_months=24, note="חופש מסבי גלגלים"),
         long_("cvt_oil", "replace", every_km=60000, note="לפי הטבלה: בדיקה בכל טיפול והחלפה כל טיפול רביעי (60,000 ק\"מ); בתנאים קשים החלפה כל 30,000")],
   extra_notes="הטבלה בספר מכסה 15 טיפולים של 15,000 ק\"מ (עד 225,000). שמן ומסנן: כל 15,000 ק\"מ או שנה, או כשמופיע מחוון החלפת השמן. עמוד 'שירות בתנאים קשים' (עמ' 434 ב-PDF) לא נכלל בלוח.",
   specs={"_note": "לפי ספר הרכב; נפחים לאימות", "engine_oil": "לפי הספר: שמן מנוע במפרט ILSAC GF-6 / API SP, 0W-20", "coolant": "נוזל קירור מקורי מיצובישי (Super Long Life) 50/50", "brake_fluid": "DOT 3 / DOT 4", "fuel": "בנזין 95 אוקטן", "timing": "שרשרת"})
print("done mitsubishi")

# ===================== Ford (דלק מוטורס): one-page service plans, same portal as Mazda =====================
# data/sources/ford-plans.json = items parsed from the plan PDFs (label, interval text, km, months, every_service).
FORD = {"make": "Ford", "make_he": "פורד", "importer": "דלק מוטורס"}
FORD_PAGE = {"url": "https://www.ford.co.il/תוכנית-טיפול/שירות", "kind": "importer", "note": "תוכנית טיפול לפי דגם ושנת עלייה לכביש: התראה בלוח המחוונים / 15,000 ק\"מ / שנה, המוקדם"}
FORD_PLANS = json.load(open(os.path.join(ROOT, "sources", "ford-plans.json"), encoding="utf-8"))
FORD_MAP = [
    (r"שמן ומסנן שמן מנוע ופקק", ["engine_oil", "oil_filter"]), (r"^שמן מנוע", ["engine_oil"]), (r"מסנן שמן מנוע", ["oil_filter"]), (r"^פקק אגן שמן", ["oil_filter"]),
    (r"מסנן אוויר למזגן", ["cabin_filter"]), (r"נוזל קירור", ["coolant"]), (r"נוזל בלמים", ["brake_fluid"]),
    (r"מסנן או?ויר למנוע", ["air_filter"]), (r"מצתים", ["spark_plugs"]), (r"כיוון שסתומים|מרווח שסתומים", ["valve_clearance"]),
    (r"מסנן דלק|מסנן סולר", ["fuel_filter"]), (r"רצועת תזמון ורצועת אביזרים", ["timing_belt", "drive_belt"]), (r"רצועת תזמון", ["timing_belt"]),
    (r"רצועת אביזרים", ["drive_belt"]), (r"תיבת הילוכים רובוטית", ["dct_oil"]), (r"תיבת הילוכים ידנית", ["manual_gearbox_oil"]), (r"שמן תיבת הילוכים", ["transmission_oil"]),
    (r"שמן סרן", ["differential_oil"]), (r"שמן תיבת העברה", ["transfer_case_oil"]), (r"ניקוז מים ממסנן סולר", ["fuel_filter"]), (r"גירוז", ["propshaft"]), (r"ניקוי מסנן אוויר", ["air_filter"]),
]
def ford(id_, plan_file, model, model_he, gen, years, engines, fuel, url=None, extra_notes="", specs=None, status="reviewed", skip=(), brand=None, plans=None, page=None):
    """Delek Motors one-page service plan -> schedule (Ford by default; Mazda plans share the layout)."""
    brand = brand or FORD; plans = plans or FORD_PLANS; page = page or FORD_PAGE
    plan = plans[plan_file]
    url = plan.get("url") or url
    cols = [15000 * i for i in range(1, 9)]
    rows = []; longs = []; notes = []
    for it in plan["items"]:
        lab = it["label"]
        if any(re.search(s, lab) for s in skip):
            continue
        items = next((v for rx, v in FORD_MAP if re.search(rx, lab)), None)
        if not items:
            notes.append(f"פריט לא ממופה: {lab} ({it['interval_text']})"); continue
        qual = re.search(r"ליטר\s*[\d./]+|[\d./]+\s*ליטר|בנזין|דיזל|03/12", lab)
        note = (f"{lab}: {it['interval_text']}".strip()) if qual else None
        km, mo, ev = it["km"], it["months"], it["every_service"]
        act = "adjust" if items == ["valve_clearance"] else ("inspect" if re.search(r"^ניקוז|^ניקוי|^גירוז", lab) else "replace")
        if "ואז" in it["interval_text"]:  # "195,000 ק\"מ או 10 שנים ואז כל 90,000 ק\"מ או 5 שנים"
            kms = sorted(int(x) * 1000 for x in re.findall(r"(\d{2,3}),000", it["interval_text"]))
            yrs = sorted(int(x) * 12 for x in re.findall(r"(?<![\d,])(\d{1,2})(?![\d,])", it["interval_text"]) if 1 <= int(x) <= 20)
            if len(kms) >= 2:
                for k in items:
                    longs.append(long_(k, "replace", first_km=kms[-1], first_months=(yrs[-1] if yrs else None), then_every_km=kms[0], then_every_months=(yrs[0] if yrs else None)))
                continue
        if ev == 1 or (km == 15000):
            pat = "R" * 8
        elif ev == 2 or (km is None and mo == 24) or km == 30000:
            pat = "-R" * 4
        elif km and km % 15000 == 0 and km <= 120000:
            n = km // 15000; pat = "".join("R" if (i + 1) % n == 0 else "-" for i in range(8))
        else:
            kw = {}
            if km: kw["every_km"] = km
            if mo: kw["every_months"] = mo
            if not kw:
                notes.append(f"{lab}: {it['interval_text']}"); continue
            for k in items:
                longs.append(long_(k, act, note=note, **kw) if note else long_(k, act, **kw))
            continue
        if act == "adjust":
            pat = pat.replace("R", "A")
        elif act == "inspect":
            pat = pat.replace("R", "I")
        for k in items:
            rows.append((k, pat, note) if note else (k, pat))
    services = grid(cols, rows)
    for svc in services:
        dd = {}
        for e in svc["items"]:
            dd.setdefault((e["item"], e["action"]), e)
        svc["items"] = list(dd.values())
    fl = "; ".join(plan["fluids"][:8])
    write({
        **brand, "id": id_, "model": model, "model_he": model_he, "generation": gen, "years": years, "engines": engines, "fuel": fuel,
        "interval": {"km": 15000, "months": 12, "note": "לפי תוכנית הטיפול של דלק מוטורס: התראה בלוח המחוונים, 15,000 ק\"מ או 12 חודשים, המוקדם"},
        "cycle_km": 120000, "services": services, "long_interval": longs, "time_based": [],
        "specs": dict({"_note": "מפרטי הנוזלים מתוך תוכנית הטיפול (מק\"טי Ford WSS): " + fl}, **(specs or {})),
        "sources": [{"url": url, "kind": "importer", "note": f"PDF תוכנית טיפול '{plan_file.replace('ford-plan-', '').replace('mazda-plan-', '')}' של דלק מוטורס (קישור SharePoint מתוך הדף; {plan['header'][:80]})"}, page],
        "status": status,
        "notes": ("הועתק מתוכנית הטיפול (עמוד אחד: פריט ומרווח). הלוח מציג 8 טיפולים של 15,000 ק\"מ; פריטים עם מרווח ארוך יותר ב-long_interval. "
                  + (" ".join(notes) + " " if notes else "") + extra_notes).strip(),
    })

FSP = "https://delekmotorscoil.sharepoint.com/:b:/s/Techtrain/"
ford("ford-focus-2004-2010-1.6-2.0", "ford-plan-Ford_Focus_2004_2010.pdf", "Focus", "פוקוס", "Mk2 (C307)", [2004, 2010], ["1.6 Duratec (HWDA/SHDA)", "2.0 Duratec"], "petrol",
     None, extra_notes="מסנן דלק 135,000 או 6 שנים; רצועת תזמון 120,000 או 5 שנים; כיוון שסתומים 120,000.")
ford("ford-focus-2011-2015-1.6-2.0", "ford-plan-Ford_Focus_2011_2015.pdf", "Focus", "פוקוס", "Mk3 (C346)", [2011, 2015], ["1.6 Ti-VCT (PNDA)", "1.6 EcoBoost", "2.0 GDI"], "petrol",
     None, extra_notes="מסנן דלק 45,000 רק לרכבים עד ייצור 03/2012. רצועת תזמון ורצועת אביזרים 120,000 או 5 שנים.")
ford("ford-focus-2016-2018-1.0-1.5", "ford-plan-Ford_Focus_2016_2018.pdf", "Focus", "פוקוס", "Mk3 facelift", [2016, 2018], ["1.0 EcoBoost (M1DA/M2DA)", "1.5 EcoBoost (M8DC/M9DC)"], "petrol",
     None, extra_notes="רצועת תזמון (ברטובה בשמן) 195,000 או 10 שנים; רצועת אביזרים 120,000 או 5 שנים.")
ford("ford-focus-2019-2021-1.0-1.5", "ford-plan-Ford_Focus_2019_2021.pdf", "Focus", "פוקוס", "Mk4 (C519)", [2019, 2021], ["1.0 EcoBoost (M0DC/Y1DA)", "1.5 EcoBoost", "1.5 EcoBlue diesel"], "petrol-or-diesel",
     None, extra_notes="דיזל: שמן ומסנן כל טיפול שני לפי התוכנית (בבנזין כל טיפול); מסנן סולר 60,000 או 4 שנים; רצועת תזמון דיזל 180,000 או 10 שנים.")
ford("ford-focus-2022-2026-1.0", "ford-plan-Ford_Focus_2022_And_Up.pdf", "Focus", "פוקוס", "Mk4 facelift", [2022, 2026], ["1.0 EcoBoost mHEV (Y1DA/FYD)"], "petrol",
     None)
ford("ford-fiesta-2008-2018-1.0-1.6", "ford-plan-Ford_Fiesta_2008_2018.pdf", "Fiesta", "פיאסטה", "Mk7 (B299)", [2008, 2018], ["1.0 EcoBoost (SFJA/SFJB)", "1.25 Duratec (SNJB/SNJA)", "1.4 Duratec (SPJA)", "1.6 Ti-VCT (IQJA)"], "petrol",
     None, extra_notes="מנוע 1.0 EcoBoost: נוזל קירור 150,000 או 5 שנים, מצתים 60,000, רצועות תזמון ואביזרים 195,000 או 10 שנים; שאר המנועים: רצועות 120,000 או 5 שנים.")
ford("ford-kuga-2013-2016-1.5-1.6", "ford-plan-Ford_Kuga_2013_2016.pdf", "Kuga", "קוגה", "Mk2 (C520)", [2013, 2016], ["1.6 EcoBoost", "1.5 EcoBoost"], "petrol",
     None, extra_notes="רצועת תזמון: 1.6 - 120,000 או 5 שנים; 1.5 - 195,000 או 10 שנים. שמן גיר אוטומטי 240,000 או 12 שנים.")
ford("ford-kuga-2017-2026-1.5", "ford-plan-Ford_Kuga_2017_And_Up.pdf", "Kuga", "קוגה", "Mk2 facelift / Mk3", [2017, 2026], ["1.5 EcoBoost (M9MB/M8MA)"], "petrol",
     None, extra_notes="שמן גיר אוטומטי 240,000 או 12 שנים; רצועת תזמון 195,000 או 10 שנים.")
ford("ford-mondeo-2007-2012-2.0-2.3", "ford-plan-Ford_Mondeo_2007_2012.pdf", "Mondeo", "מונדאו", "Mk4 (CD345)", [2007, 2012], ["2.0 Duratec (SEBA)", "2.3 Duratec", "2.0 TDCi"], "petrol-or-diesel",
     None, extra_notes="דיזל: מסנן דלק 45,000 או 3 שנים, רצועת תזמון 135,000 או 6 שנים; בנזין: מרווח שסתומים - בדיקת רעשים ב-135,000; גיר רובוטי (PowerShift) שמן 60,000 או 3 שנים.")
ford("ford-puma-2020-2026-1.0", "ford-plan-Ford_Puma_2020_And_Up.pdf", "Puma", "פומה", "J2K", [2020, 2026], ["1.0 EcoBoost mHEV (B7JA)"], "petrol",
     None, extra_notes="פקק אגן שמן מוחלף בכל טיפול; רצועת אביזרים 240,000.")
ford("ford-s-max-galaxy-2007-2011-2.0-2.3", "ford-plan-Ford_Smax_Galaxy_2007_2011.pdf", "S-Max / Galaxy", "אס-מקס / גלקסי", "WA6", [2007, 2011], ["2.0 Duratec", "2.3 Duratec", "2.0 TDCi"], "petrol-or-diesel",
     None, extra_notes="דיזל: מסנן דלק 45,000/3 שנים, רצועת תזמון 135,000/6 שנים; 2.3 בנזין: מסנן דלק 135,000/6 שנים.")
print("done ford")

# ---- more Mazda plans through the same generator ----
MAZDA_PLANS = json.load(open(os.path.join(ROOT, "sources", "mazda-plans.json"), encoding="utf-8"))
def mazda_plan(id_, plan_file, model, model_he, gen, years, engines, fuel="petrol", extra_notes="", skip=(), url=None):
    ford(id_, plan_file, model, model_he, gen, years, engines, fuel, url=url, brand=MZ, plans=MAZDA_PLANS, page=MZ_PAGE, extra_notes=extra_notes, skip=skip)
mazda_plan("mazda-5-2005-2015", "mazda-plan-38646_Mazda5_2005_And_Up.pdf", "5", "5", "CR/CW", [2005, 2015], ["1.8 MZR", "2.0 MZR (LF)"],
           extra_notes="מסנן מזגן בכל טיפול; מצתים 120,000 או 3 שנים; מסנן דלק 105,000.")
mazda_plan("mazda-6-2002-2012", "mazda-plan-38646_Mazda6_2002_2013.pdf", "6", "6", "GG/GH", [2002, 2012], ["1.8 / 2.0 / 2.3 MZR (L5, LF, L3)"],
           extra_notes="מסנן מזגן: כל טיפול, וממודל 2008 כל 30,000 או שנתיים; מצתים 90,000; מסנן דלק 135,000.")
mazda_plan("mazda-6-2013-2025", "mazda-plan-38646_Mazda6_2014_And_Up.pdf", "6", "6", "GJ/GL", [2013, 2025], ["2.0 Skyactiv-G (PE)", "2.5 Skyactiv-G (PY)"],
           extra_notes="מסנן מזגן בכל טיפול; מצתים 120,000 או 6 שנים; מסנן דלק 135,000.")
mazda_plan("mazda-cx-5-2025-2026-2.5", "mazda-plan-39547_Mazda_CX-5_2025_NA_And_Above.pdf", "CX-5", "CX-5", "KF (2025+)", [2025, 2026], ["2.5 Skyactiv-G (PY)"],
           skip=(r"מפרט", r"^קירור נוזל", r"^נוזל בלמיםDOT", r"^שמן תיבת העברה"),
           url=FSP + "ER5rxZVHJy9Dtk-KLdX_rCgB45a6cl67_5kzgMjw0cQc7Q?download=1",
           extra_notes="תוכנית נפרדת לשנת ייצור 2025 ואילך עם מנוע 2.5 (PY) בלי טורבו. לעומת תוכנית 2012+: מסנן מזגן כל 30,000 או שנתיים (לא בכל טיפול), "
                       "שמן 0W-20 API SN Plus, נוזל בלמים DOT3. מצתים 120,000 או 6 שנים; מסנן דלק 135,000. התוכנית של CX-5 החדשה ממודל 2026 (40609) זהה בכל הפריטים. "
                       "מנוע 2.0 (PE) נשאר בתוכנית 2012+, ולגרסת הטורבו יש תוכנית שלישית (12,000 ק\"מ) שלא הועתקה.")
mazda_plan("mazda-cx-90-2022-2026-3.3", "mazda-plan-38646_Mazda_CX-90_2022_And_Above.pdf", "CX-90", "CX-90", "KK", [2022, 2026], ["3.3 e-Skyactiv G turbo mild hybrid"],
           extra_notes="מצתים כל 64,000 (מנוע טורבו).")
mazda_plan("mazda-mx-5-2007-2014-1.8-2.0", "mazda-plan-38646_Mazda_MX-5_2007_2014.pdf", "MX-5", "MX-5", "NC", [2007, 2014], ["1.8 MZR", "2.0 MZR"],
           extra_notes="גיר ידני: שמן 90,000; סרן אחורי 75,000; מצתים 90,000 או 3 שנים; מסנן דלק 105,000.")
mazda_plan("mazda-mx-5-2015-2026-1.5-2.0", "mazda-plan-38646_Mazda_MX-5_2015_And_Up.pdf", "MX-5", "MX-5", "ND", [2015, 2026], ["1.5 Skyactiv-G", "2.0 Skyactiv-G"],
           extra_notes="גיר ידני: שמן 90,000; מצתים 120,000 או 6 שנים; מסנן דלק 105,000.")
mazda_plan("mazda-bt-50-2007-2026-diesel", "mazda-plan-38646_Mazda_BT-50_2007_And_Above.pdf", "BT-50", "BT-50", "J97M / UP / TF", [2007, 2026], ["2.5 / 3.0 / 3.2 turbo diesel"], fuel="diesel",
           extra_notes="טנדר דיזל: ניקוז מים ממסנן הסולר, גירוז מפרקים וניקוי מסנן אוויר בכל טיפול; מסנן סולר 30,000; רצועת תזמון 120,000; כיוון שסתומים 120,000 או 8 שנים; ב-4x4 שמן סרנים 30,000.")
print("done mazda plans")
