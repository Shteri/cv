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
ROWS_IA_GB = [
    ("drive_belt", ALL),
    ("engine_oil", R_ALL), ("oil_filter", R_ALL),
    ("air_filter", "IRIRIRIR"),
    ("evap_system", Q), ("vacuum_hose", EVEN), ("fuel_filter", Q, "פריט ללא תחזוקה לפי הספר; בדיקה בלבד"),
    ("fuel_lines", Q),
    ("battery_12v", ALL), ("electrical_system", EVEN),
    ("brake_lines", ALL), ("pedals", EVEN), ("parking_brake", ALL),
    ("brake_fluid", "IRIRIRIR"), ("brake_pads", ALL), ("brake_discs", ALL), ("brake_drums", EVEN),
    ("steering", ALL), ("cv_boots", ALL), ("tires", ALL), ("suspension", ALL), ("body_underside", ALL),
    ("ac_refrigerant", ALL), ("ac_system", ALL),
    ("cabin_filter", R_ALL),
]
LONG_IA_GB = [
    long_("spark_plugs", "replace", every_km=160000),
    long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24),
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
             "מסנן אוויר: בדיקה בטיפול אחד והחלפה בטיפול הבא. תוסף דלק מומלץ כל 15,000 ק\"מ אם הבנזין לא כולל תוספים.",
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
             "מסנן אוויר לסירוגין בדיקה/החלפה, מצתים כל 160,000 ק\"מ.",
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

write({
    **KIA, "id": "kia-picanto-2017-2025", "model": "Picanto", "model_he": "פיקנטו", "generation": "JA",
    "years": [2017, 2025], "engines": ["1.0 MPI (Kappa)", "1.2 MPI (Kappa)", "1.0 T-GDI (Kappa)"], "fuel": "petrol",
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
        long_("drive_belt", "replace", first_km=90000, first_months=72, then_every_km=30000, then_every_months=24,
              note="לפי הספר: החלפה ראשונה ב-90,000, אחר כך כל 30,000; בפועל בדיקה והחלפה לפי מצב"),
        long_("spark_plugs", "replace", every_km=150000, note="מנועי 1.0 MPI ו-1.2 MPI. מנוע 1.0 T-GDI: כל 75,000 ק\"מ"),
        long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24),
    ],
    "time_based": [],
    "sources": [
        {"url": "https://kia-israel.co.il/wp-content/uploads/2020/11/ספר-רכב-Picanto_OM_2017-.pdf",
         "kind": "importer", "note": "ספר רכב פיקנטו 2017+ של קיה ישראל, פרק 8 עמ' 11-17"},
        {"url": "https://cdnmedia.kia-israel.co.il/www/cars-book/Picanto-JA-2017-2020.pdf", "kind": "importer", "note": "אותו ספר בספריית cars-book"},
        {"url": "https://cdnmedia.kia-israel.co.il/www/cars-book/Picanto-AMT-2021.pdf", "kind": "importer", "note": "ספר רכב פיקנטו 2021+ (גיר AMT)"},
        KIA_HUB,
    ],
    "status": "reviewed",
    "notes": "מסנן תא נוסעים ונוזל בלמים כל 30,000 לפי הספר (מוסכים בישראל נוהגים להחליף מסנן מזגן בכל טיפול בגלל אבק). "
             "מסנן אוויר: בדיקה ב-30, החלפה ב-60. תוסף דלק כל 15,000 אם הבנזין בלי תוספים.",
})

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
        ("drive_belt", e(drive_belt_pattern)),
        ("cv_boots", e(ALL)),
        ("dct_oil", e(EVEN)), ("manual_gearbox_oil", e(EVEN)),
        ("exhaust", e(ALL)),
        ("fuel_lines", e(EVEN)), ("fuel_tank_air_filter", e(EVEN)), ("evap_system", e(EVEN)),
        ("parking_brake", e(ALL)),
        ("steering", e(ALL)), ("suspension", e(ALL)), ("tires", e(ALL)),
        ("vacuum_hose", e(ALL)),
        ("valve_clearance", e("--I--I--")),
    ]
LONG_QL = [
    long_("coolant", "replace", first_km=210000, first_months=120, then_every_km=30000, then_every_months=24),
    long_("cooling_system", "inspect", first_km=60000, first_months=48, then_every_km=30000, then_every_months=24),
    long_("spark_plugs", "replace", every_km=150000, every_months=120,
          note="מנועי 1.6 GDI, 2.0 MPI, 2.4 GDI. מנוע 1.6 T-GDI: כל 75,000 ק\"מ או 60 חודשים"),
    long_("transmission_oil", "inspect", every_km=90000, note="לפי הספר אין צורך בטיפול בתנאים רגילים; בתנאי הפעלה קשים החלפה כל 90,000"),
]
QL_NOTE = ("הטבלה בספר בנויה בעמודות של 30,000 ק\"מ / 24 חודשים (תוכנית אירופית). למנוע 1.6 GDI הספר עצמו קובע 15,000 ק\"מ או 12 חודשים "
           "בתנאי הפעלה קשים (אבק, חום, עצור-וסע), ולמנועי T-GDI/2.0/2.4 15,000 גם בטבלה הרגילה. היבואן מטפל כל 15,000 או שנה. "
           "לכן הקובץ בנוי על רשת 15,000: בטיפולי הביניים שמן ומסנן בלבד, והפריטים מהטבלה נופלים על הטיפולים הזוגיים.")
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
def mazda(id_, model, model_he, gen, years, engines, cabin, brake, air, url, fname, extra_note="", plan_years=""):
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
        "long_interval": LONG_MZ,
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
      extra_note=" תוכנית 2003-2012: מסנן מזגן ונוזל בלמים כל 30,000 או שנתיים, מסנן אוויר 60,000. מצתים רגילים 45,000, מצתי אירידיום 120,000. "
                 "מסנן דלק: 75,000 עד שלדה 133398, 45,000 משלדה 1333399 (כך בתוכנית). שמן גיר Mazda V, שמן הגה Dexron III.")
mazda("mazda-2-2007-2014", "2", "2", "DE", [2007, 2014], ["1.3 MZR", "1.5 MZR"],
      cabin="-R-R-R-R", brake="-R-R-R-R", air="---R---R",
      url=SP + "EUleFfkd1mlPn3fX15es5HcBszPOYXuLiARcad4pgYFKjA?download=1", fname="38646 _Mazda2_2007_2014.pdf", plan_years="שנות ייצור 2007-2014",
      extra_note=" תוכנית 2007-2014: מסנן מזגן ונוזל בלמים כל 30,000 או שנתיים, מסנן אוויר 60,000, מצתי אירידיום 120,000 או 3 שנים, מסנן דלק 135,000.")
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
TY_ACT = {"I": "inspect", "R": "replace", "C": "clean", "T": "adjust"}
# label regex -> list of item keys (a row may feed two items)
TY_MAP = [
    (r"^שמן מנוע ומסנן", ["engine_oil", "oil_filter"]), (r"^שמן מנוע", ["engine_oil"]), (r"^מסנן שמן", ["oil_filter"]),
    (r"^מערכת קירור וחימום", ["cooling_system"]),
    (r"נוזל קירור (מערכת )?היבריד|נוזל קירור ממיר", ["coolant"]), (r"^נוזל קירור מנוע", ["coolant"]),
    (r"^צינורות פליטה", ["exhaust"]), (r"^מצבר", ["battery_12v"]), (r"^מסנן דלק", ["fuel_filter"]),
    (r"^מסנן אוויר מזגן", ["cabin_filter"]), (r"^מסנן אוויר", ["air_filter"]),
    (r"^צינורות דלק", ["fuel_lines"]), (r"מסנן פחם|מכלול פחמי", ["evap_system"]),
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
    (r"מסנן (אוויר )?סוללה היברידית", ["hybrid_battery_filter"]),
    (r"^מרווח שסתומים|^כיוון שסתומים", ["valve_clearance"]), (r"^מצתים", ["spark_plugs"]), (r"^רצועת הינע", ["drive_belt"]),
    (r"שמן דיפרנציאל|שמן דיפרונציאל", ["differential_oil"]), (r"שמן תיבת העברה", ["transfer_case_oil"]),
    (r"^מצנן צינורות|^מחברי , צינורות ומצנן", ["coolant_hoses"]),
]
TY_SKIP = re.compile(r"עיגון שטיח|^מקרא|^רגילה$|^מחמירה$|^בדיקה$|^$|ידית הילוכים|ברגי גל הינע|מסנן מצבר")
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
def ty_long(fid):
    """Long-interval facts from the sheet's free text (layout order is messy,
    so we match anchored phrases in the whole normalized text)."""
    t = TY_SHEETS[str(fid)]["text"]
    L = []; notes = []
    def add(item, action, **kw):
        k = (item, action, kw.get("first_km"), kw.get("every_km"))
        if k not in {(x["item"], x["action"], x.get("first_km"), x.get("every_km")) for x in L}:
            L.append(long_(item, action, **kw))
    for m in re.finditer(r"(.{0,40})החלפה ראשונה (?:ב|לאחר)\s*(\d{3}),000 ק\"מ ומאז (?:כל|מידי|מדי)\s*(\d{2,3}),000", t):
        ctx = m.group(1); first, then = int(m.group(2)) * 1000, int(m.group(3)) * 1000
        hyb = ("היבריד" in ctx or "ממיר" in ctx or first >= 200000)
        add("coolant", "replace", first_km=first, then_every_km=then, note="נוזל קירור מערכת היברידית/ממיר" if hyb else "נוזל קירור מנוע (SLLC)")
    m = (re.search(r"מצתים\s*(?:החלפה|החלף) (?:מדי|מידי|כל)\s*(\d{2,3})[.,]000", t)
         or re.search(r"מסנן שמן מנוע (?:החלף|החלפה) כל\s*(\d{2,3})[.,]000", t))
    if m: add("spark_plugs", "replace", every_km=int(m.group(1)) * 1000, note="מצתי אירידיום")
    m = re.search(r"מסנן דלק\s*(?:החלפה|החלף) (?:מדי|מידי|כל)\s*(\d{2,3}),000", t)
    if m: add("fuel_filter", "replace", every_km=int(m.group(1)) * 1000)
    m = re.search(r"(?:אבחון|בדיקה) ראשונ?ה? (?:ב|לאחר)\s*(\d{3}),000 ק\"מ \(?או\s*(\d{2}) ח[ודשים']*\)? ומאז (?:כל|מידי|מדי)\s*(\d{2}),000", t)
    if m: add("drive_belt", "inspect", first_km=int(m.group(1)) * 1000, first_months=int(m.group(2)), then_every_km=int(m.group(3)) * 1000, then_every_months=12)
    m = re.search(r"(?:רציפה|E-CVT|CVT)[^.]{0,60}?בדיקה כל\s*(\d{2}),000 ק\"מ ?[.,]? ?החלפה כל\s*(\d{2}),000", t)
    if m: add("cvt_oil", "replace", every_km=int(m.group(2)) * 1000, note=f"בדיקה כל {m.group(1)},000")
    m = re.search(r"משאבת וו?אקום (?:החלפה|החלף) (?:מדי|כל)\s*(\d{3}),000 ק\"מ( או\s*\d+ שנים)?", t)
    if m: notes.append(f"משאבת ואקום: החלפה כל {m.group(1)},000 ק\"מ{m.group(2) or ''}.")
    return L, notes
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
        for k in it:
            grid_rows.append((k, pat.replace("T", "A"), note) if note else (k, pat.replace("T", "A")))
    # merge duplicate (item,column) entries: grid() emits duplicates, dedupe after
    services = grid(GRID_TY, grid_rows)
    for svc in services:
        seen = {}; merged = []
        for e in svc["items"]:
            key = (e["item"], e["action"])
            if key in seen: continue
            seen[key] = 1; merged.append(e)
        svc["items"] = merged
    long_items, ln = ty_long(fid)
    engine_line = sheet.get("engine")
    srcs = [{"url": sheet["source"], "kind": "importer", "note": f"לוח אחזקה של יוניון מוטורס '{sheet['title']}' (דגמים {', '.join(sheet['models'])}, שנים {sheet['years'][0]}-{sheet['years'][1]}); דגם מנוע בגיליון: {engine_line}"}]
    for x in extra_sheets:
        sh = TY_SHEETS[str(x)]
        srcs.append({"url": sh["source"], "kind": "importer", "note": f"לוח אחזקה נוסף '{sh['title']}' ({sh['years'][0]}-{sh['years'][1]}), אותו מבנה"})
    srcs.append(TY_HUB)
    sp = {"_note": "שמן, נוזל קירור ונוזל בלמים מהגיליון של היבואן; שאר הפריטים ידע כללי, לאימות"}
    sp.update(specs or {})
    write({
        **TY, "id": id_, "model": model, "model_he": model_he, "generation": gen, "years": years, "engines": engines, "fuel": fuel,
        "interval": {"km": 15000, "months": 12, "note": "לפי הגיליון: תנאי פעולה רגילים 15,000 ק\"מ או 12 חודשים; בתנאים מחמירים שמן ומסנן כל 7,500 ק\"מ או 6 חודשים"},
        "cycle_km": 150000,
        "services": services,
        "long_interval": long_items,
        "time_based": [],
        "specs": sp,
        "sources": srcs,
        "status": "reviewed",
        "notes": ("הועתק מלוח האחזקה הישראלי של יוניון מוטורס (10 עמודות של 15,000 ק\"מ). פעולות: I בדיקה, R החלפה, C ניקוי, T הידוק. "
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
toyota("toyota-corolla-2019-2025-1.6", 327, "Corolla", "קורולה", "E210 (ZRE210)", [2019, 2025], ["1.6 (1ZR-FAE)"], "petrol", extra_sheets=(317,),
       specs=dict(TY_OIL_NEW, oil_capacity="4.2 ליטר (לפי הגיליון)", coolant="Toyota SLLC, 5.8 ליטר", tires="205/55 R16 או 225/40 R18", battery="מצבר רגיל 12V", spare="ערכת תיקון או גלגל חלופי צר, לפי גימור",
                  brake_fluid="SAE J1703/J1704 / FMVSS 116 DOT 3/DOT 4"),
       notes_extra="גיר אוטומטי (ATF WS, ללא החלפה מתוכננת בתנאים רגילים; בדיקה כל 60,000).")
toyota("toyota-corolla-2019-2025-1.8-hybrid", 316, "Corolla", "קורולה", "E210 (ZWE211)", [2019, 2025], ["1.8 hybrid (2ZR-FXS)"], "hybrid", extra_sheets=(345,),
       specs=dict(TY_OIL_NEW, oil_capacity="4.2 ליטר (לפי הגיליון)", coolant="Toyota SLLC: מנוע 5.4 ליטר, מערכת היברידית 1.4 ליטר (לפי הגיליון)", tires="205/55 R16 או 225/40 R18", spare="ערכת תיקון או גלגל חלופי צר", **HYB,
                  brake_fluid="SAE J1703/J1704 / FMVSS 116 DOT 3/DOT 4"),
       notes_extra="מסנן אוויר סוללה היברידית: ניקוי בכל טיפול. נוזל קירור מערכת היברידית: החלפה ראשונה 240,000 ואז כל 90,000.")
toyota("toyota-corolla-cross-2022-2025-1.8-hybrid", 346, "Corolla Cross", "קורולה קרוס", "XG10", [2022, 2025], ["1.8 hybrid (2ZR-FXE)"], "hybrid", extra_sheets=(338,),
       specs=dict(TY_OIL_NEW, tires="215/60 R17 או 225/50 R18", spare="ערכת תיקון", **HYB))
toyota("toyota-yaris-2011-2019-1.33-1.5", 311, "Yaris", "יאריס", "XP130", [2011, 2019], ["1.33 (1NR-FE)", "1.5 (2NR-FKE, 2017+)"], "petrol", extra_sheets=(314,),
       specs=dict(TY_OIL_OLD, oil_capacity="3.4 ליטר (1.33) / 3.1 ליטר (1.5), לפי הגיליון", coolant="Toyota SLLC, 4.8 ליטר", tires="175/65 R15 או 185/60 R15", battery="מצבר רגיל 12V", spare="גלגל חלופי צר או ערכת תיקון",
                  brake_fluid="SAE J1704 / FMVSS 116 DOT 4"),
       notes_extra="שני גיליונות (2011-2017 מנוע 1NR-FE, 2017-2019 מנוע 2NR-FKE) עם אותה טבלה. שמן CVT: Toyota Genuine CVT Fluid FE / TC.")
toyota("toyota-yaris-2012-2019-1.5-hybrid", 312, "Yaris", "יאריס", "XP130 hybrid", [2012, 2019], ["1.5 hybrid (1NZ-FXE)"], "hybrid",
       specs=dict(TY_OIL_OLD, tires="175/65 R15 או 185/60 R15", spare="ערכת תיקון או גלגל חלופי צר", **HYB),
       notes_extra="מרווח שסתומים: בדיקה ב-90,000 (72 חודשים). נוזל קירור ממיר מתח: בדיקה כל 30,000.")
toyota("toyota-yaris-2020-2025-1.5", 336, "Yaris", "יאריס", "XP210", [2020, 2025], ["1.5 (M15A-FKS)"], "petrol", extra_sheets=(320, 355),
       specs=dict(TY_OIL_NEW, tires="185/65 R15 או 205/45 R17", battery="מצבר רגיל 12V", spare="ערכת תיקון"))
toyota("toyota-yaris-2020-2025-1.5-hybrid", 335, "Yaris", "יאריס", "XP210 hybrid", [2020, 2025], ["1.5 hybrid (M15A-FXE)"], "hybrid", extra_sheets=(321, 356),
       specs=dict(TY_OIL_NEW, tires="185/65 R15 או 205/45 R17", spare="ערכת תיקון", **HYB))
toyota("toyota-yaris-cross-2021-2025-1.5-hybrid", 340, "Yaris Cross", "יאריס קרוס", "XP210", [2021, 2025], ["1.5 hybrid (M15A-FXE)"], "hybrid", extra_sheets=(354,),
       specs=dict(TY_OIL_NEW, tires="205/65 R16 או 215/50 R18", spare="ערכת תיקון", **HYB))
toyota("toyota-yaris-cross-2021-2025-1.5", 341, "Yaris Cross", "יאריס קרוס", "XP210", [2021, 2025], ["1.5 (M15A-FKS)"], "petrol", extra_sheets=(353,),
       specs=dict(TY_OIL_NEW, tires="205/65 R16 או 215/50 R18", battery="מצבר רגיל 12V", spare="ערכת תיקון"))
toyota("toyota-auris-2013-2019-1.6", 281, "Auris", "אוריס", "E180", [2013, 2019], ["1.6 (1ZR-FAE)"], "petrol",
       specs=dict(TY_OIL_OLD, tires="205/55 R16", battery="מצבר רגיל 12V", spare="גלגל חלופי צר"))
toyota("toyota-auris-2011-2019-1.8-hybrid", 280, "Auris", "אוריס", "E180 hybrid", [2011, 2019], ["1.8 hybrid (2ZR-FXE)"], "hybrid", extra_sheets=(282,),
       specs=dict(TY_OIL_OLD, tires="205/55 R16 או 225/45 R17", spare="ערכת תיקון או גלגל חלופי צר", **HYB))
toyota("toyota-rav4-2013-2019-2.0", 307, "RAV4", "ראב 4", "XA40", [2013, 2019], ["2.0 (3ZR-FAE / לפי הגיליון 1ZR-FAE)"], "petrol",
       specs=dict(TY_OIL_OLD, tires="225/65 R17 או 235/55 R18", battery="מצבר רגיל 12V", spare="גלגל חלופי צר"), notes_extra="גיליון 4x4: כולל שמן דיפרנציאל ותיבת העברה.")
toyota("toyota-rav4-2016-2019-2.5-hybrid", 308, "RAV4", "ראב 4", "XA40 hybrid", [2016, 2019], ["2.5 hybrid (2AR-FXE)"], "hybrid",
       specs=dict(TY_OIL_OLD, tires="225/65 R17 או 235/55 R18", spare="גלגל חלופי צר", **HYB))
toyota("toyota-rav4-2020-2025-2.0", 325, "RAV4", "ראב 4", "XA50", [2020, 2025], ["2.0 (M20A-FKS)"], "petrol", extra_sheets=(351,),
       specs=dict(TY_OIL_NEW, tires="225/65 R17 או 235/55 R19", battery="מצבר רגיל 12V", spare="גלגל חלופי צר"))
toyota("toyota-rav4-2020-2025-2.5-hybrid", 324, "RAV4", "ראב 4", "XA50 hybrid", [2020, 2025], ["2.5 hybrid (A25A-FXS)"], "hybrid", extra_sheets=(350,),
       specs=dict(TY_OIL_NEW, tires="225/65 R17 או 235/55 R19", spare="גלגל חלופי צר", **HYB))
toyota("toyota-c-hr-2017-2019-1.2", 285, "C-HR", "C-HR", "AX10", [2017, 2019], ["1.2 turbo (8NR-FTS)"], "petrol",
       specs=dict(TY_OIL_OLD, tires="215/60 R17 או 225/50 R18", battery="מצבר רגיל 12V", spare="ערכת תיקון"))
toyota("toyota-c-hr-2016-2023-1.8-hybrid", 326, "C-HR", "C-HR", "AX10 hybrid", [2016, 2023], ["1.8 hybrid (2ZR-FXE)"], "hybrid", extra_sheets=(286,),
       specs=dict(TY_OIL_NEW, tires="215/60 R17 או 225/50 R18", spare="ערכת תיקון", **HYB))
toyota("toyota-camry-2013-2019-2.5-hybrid", 291, "Camry", "קאמרי", "XV50 hybrid", [2013, 2019], ["2.5 hybrid (2AR-FXE)"], "hybrid",
       specs=dict(TY_OIL_OLD, tires="215/55 R17", spare="גלגל חלופי צר", **HYB))
toyota("toyota-camry-2020-2025-2.5-hybrid", 319, "Camry", "קאמרי", "XV70 hybrid", [2020, 2025], ["2.5 hybrid (A25A-FXS)"], "hybrid", extra_sheets=(363,),
       specs=dict(TY_OIL_NEW, tires="215/55 R17 או 235/45 R18", spare="גלגל חלופי צר", **HYB))
toyota("toyota-aygo-x-2022-2025-1.0", 344, "Aygo X", "איגו X", "AB70", [2022, 2025], ["1.0 (1KR-FE)"], "petrol", extra_sheets=(339,),
       specs=dict(TY_OIL_NEW, tires="175/65 R17 או 175/60 R18", battery="מצבר רגיל 12V", spare="ערכת תיקון"))
toyota("toyota-aygo-2014-2022-1.0", 284, "Aygo", "איגו", "AB40", [2014, 2022], ["1.0 (1KR-FE)"], "petrol", extra_sheets=(318,),
       specs=dict(TY_OIL_OLD, tires="165/65 R14 או 165/60 R15", battery="מצבר רגיל 12V", spare="ערכת תיקון"))

print("done")
