# Audit of the 20 most-registered "reviewed" schedules

Auditor: independent pass, 2026-10-03. Nothing under /home/user/cv was edited.

Method: every schedule was checked against the original document (PDF pages rendered to PNG and read by eye, not only the parsed JSON).
- Copies in scratchpad/pdf were confirmed identical to the live sources: Mazda SharePoint PDFs by md5 after a fresh download, and Kia/Hyundai CDN PDFs by Content-Length.
- The Champion Motors page was fetched fresh with Playwright and its icon cells were decoded.
- The Tucson mirror pages (manualpdf.co.il) were fetched fresh as HTML and screenshots.
- Toyota sheets: the local copies in scratchpad/pdf/toyota-docs were used. They were not re-downloaded, because the books.union-motors.co.il app API was not used.
- Registry side: every registry row (make|model|fuel|engine|years) that matchSchedule() routes to each file was listed and compared with the book.

Verdict scale:
- OK: matches the book.
- MINOR: wording, harmless, or disclosed in notes.
- ERROR: wrong number, wrong action, invented item, missing item, or wrong car.

## Verdict table

| # | Schedule (vehicles) | Verdict | One-line reason |
|---|---|---|---|
| 1 | kia-picanto-2017-2025 (81,883) | MINOR | Drive belt is "replace 90k then every 30k". That is literal in the 2017 book, but the 2021+ book, which covers the ~42k G4LF cars, says "inspect". The note hedges this. |
| 2 | mazda-3-2006-2012 (69,719) | **ERROR** | Fuel filter: file says every 135,000 km; the plan says 75,000 or 45,000 depending on chassis. Spark plugs: file adds a 72-month limit the plan does not have. |
| 3 | toyota-corolla-2019-2025-1.8-hybrid (59,764) | **ERROR** | Spark plugs (90k) missing. The hybrid-battery filter row became "clean engine air filter". The 2023 sheet it cites as "same structure" is not the same. |
| 4 | toyota-corolla-2013-2019-1.6 (53,741) | **ERROR** | Spark plugs (90k) and fuel filter (120k) missing. Drive belt timing is wrong. |
| 5 | hyundai-ioniq-2016-2022-1.6-hybrid (51,114) | OK | All rows match pp. 6-8 to 6-11. Only nit: HSG belt "or 48 months" is not stored. |
| 6 | mazda-cx-5-2012-2025 (49,774) | OK (registry MINOR) | Matches the 2012+ plan. 2025-26 2.5L (PY) cars have their own 2025+ plan, with cabin filter every 30k. |
| 7 | kia-picanto-2011-2016 (47,760) | OK | Every service block matches pp. 7-8 to 7-15. |
| 8 | toyota-corolla-2007-2012-1.6 (45,330) | **ERROR** | Same defects as #4: spark plugs 90k and fuel filter 120k missing, drive belt wrong. |
| 9 | skoda-octavia-2017-2026-1.0-1.5-tsi (40,281) | OK | Champion 1.0 and 1.5 tables decoded fresh; they match exactly. Added inspection rows are disclosed. |
| 10 | hyundai-tucson-2015-2020-1.6-2.0 (39,643) | MINOR | Matches the mirror text layer. Two rows are inferred, which is disclosed. Gearbox entry: the book says "replace every 100k in severe use"; the file stores this as a plain replace entry, with a note. |
| 11 | hyundai-i10-2014-2019 (38,042) | **ERROR** | Evap, fuel filter and fuel lines placed at 75k/155k; the book has 55k/115k. Cooling-system 60k/30k entry is not in this book. |
| 12 | mazda-2-2015-2025 (35,972) | OK (registry MINOR) | Matches the plan. 1,951 cars from 2015 with the ZY engine (previous DE generation) are routed here. |
| 13 | toyota-rav4-2020-2025-2.5-hybrid (34,945) | **ERROR** | Spark plugs (90k) missing. Brake pad/disc inspection missing at 15/45/75k. Battery-filter row became engine air filter. The 2023-25 sheet differs. |
| 14 | toyota-c-hr-2016-2023-1.8-hybrid (34,221) | **ERROR** | Spark plugs (90k) and fuel filter (120k) missing. |
| 15 | kia-sportage-2016-2018 (33,138) | MINOR | Matches the table. Gearbox-oil entry is "inspect every 90k"; the book says no service, and replace every 90k in severe use. AWD propshaft row omitted. |
| 16 | seat-ibiza-2015-2026-1.0-1.5-tsi (32,459) | OK | Same Champion tables as #9; they match. |
| 17 | toyota-yaris-cross-2021-2025-1.5-hybrid (31,797) | **ERROR** | Spark plugs (90k) missing. Everything else matches. |
| 18 | mazda-3-2013-2019 (31,754) | OK (registry MINOR) | Matches the plan. 655 cars from 2013 with LF/Z6 (MZR) engines are routed here. |
| 19 | hyundai-elantra-2022-2026-1.6-hybrid (28,704) | **ERROR** | Clutch-actuator fluid (replace every 30k or 24 months) missing. Vapour hose and fuel lines missing. Cooling-system entry invented. |
| 20 | hyundai-kona-2023-2026-1.6-hybrid (28,427) | OK | Scanned table pp. 9-9 and 9-10 matches cell for cell, including the odd intervals for air filter, brake fluid, cabin filter and HSG belt. |

Totals:
- ERROR: 9 files (#2, 3, 4, 8, 11, 13, 14, 17, 19)
- MINOR: 3 files (#1, 10, 15)
- OK: 8 files, 3 of them with minor registry notes (#6, 12, 18)
- UNVERIFIABLE: none

## ERROR details with evidence

### #2 mazda-3-2006-2012
Source: '38646 _Mazda3_2003_2012.pdf', a one-page Delek Motors plan.

- **Fuel filter**
  - Plan: "מסנן דלק עד שלדה 133398 – 75,000 ק"מ" and "מסנן דלק משלדה 1333399 – 45,000 ק"מ".
  - File: `long_interval fuel_filter every_km 135000`. 135,000 is the figure from the 2013-2019 plan.
  - The file's own `notes` quote the correct 75,000/45,000, so the data contradicts its notes.
- **Spark plugs**
  - Plan: "מצתים רגילים 45,000 ק"מ" and "מצתי אירידיום 120,000 ק"מ", with no time limit.
  - File: `every_km 120000, every_months 72`. The 72 months is invented (copied from the 2013+ plan), and the 45k interval for regular plugs appears only in notes.
- Everything else matches: coolant 195k/10y then 90k/5y, brake fluid every 2 years, air filter 60k, cabin filter 30k or 2 years.
- Registry: Z6/LF engines, 2004-2012. Plausible.

### #3 toyota-corolla-2019-2025-1.8-hybrid
Source: sheet fileId 316, "ZWE211 2ZR-FXS", dated 12.03.2019. Extra source: sheet 345.

- **Spark plugs**
  - Sheet: "מצתים – החלפה מדי 90,000 ק"מ" (Iridium).
  - File: no `spark_plugs` entry at all.
- **Wrong item**
  - Sheet: "מסנן אוויר סוללה היברידית" is C (clean) in all 10 columns.
  - File: `{"item":"air_filter","action":"clean"}` at every service, so the engine air filter is shown as "clean" every 15k.
  - Cause: in `scripts/build_schedules.py`, the `TY_MAP` pattern `^מסנן אוויר` matches before the hybrid-battery pattern.
- **Second sheet misrepresented**
  - The file calls sheet 345 "אותו מבנה", but sheet 345 (ZWE219, 2ZR-FXE, 2023) differs:
    - cabin filter: R at every service (sheet 316: every 30k);
    - fuel filter: R at 75k and 150k (absent from sheet 316);
    - engine coolant: after 150k, then every 75,000 (sheet 316: every 90,000);
    - brake fluid: I at 15k, then R every 30k.
  - Registry: about 9.5k cars from 2023-2026 are routed to this file.
- Everything else verified cell by cell: oil, coolant 150k/90k and hybrid coolant 240k/90k, air filter R at 60/120, brake fluid R every 30k, cabin filter R every 30k, evap at 45/90/135, gearbox inspection at 60/120.

### #4 toyota-corolla-2013-2019-1.6
Source: sheet 289, "2013- קורולה 1ZR-FAE", dated 20.03.2016.

- **Spark plugs**
  - Sheet: "מצתים – החלפה מדי 90,000 ק"מ" (DENSO Iridium SC20HR11).
  - File: missing.
- **Fuel filter**
  - Sheet: "מסנן דלק – החלפה מדי 120,000 ק"מ" (144 months).
  - File: missing.
- **Drive belt**
  - Sheet: "רצועת הינע – אבחון ראשון ב-105,000 ק"מ (או 72 חודשים) ומאז כל 15,000 ק"מ (או 12 חודשים)".
  - File: inspect only at 45k (and therefore 135k), from a mis-parsed merged cell (`--I-------`).
- Everything else matches: brake fluid I/R alternating, cabin filter C/R alternating, air filter R at 60/120, automatic gearbox I every 30k, manual gearbox I at 45/90/135, coolant 150k/75k.

### #8 toyota-corolla-2007-2012-1.6
Source: sheet 287, "2006-2012 קורולה/אוריס 1ZR-FE".

- The same three defects as #4:
  - spark plugs "החלפה מדי 90,000" missing;
  - fuel filter "החלפה מדי 120,000" missing;
  - drive belt "first 105,000/72 months, then every 15,000" stored as inspect at 45k only.
- The other rows match, including gearbox inspections at 60/120 and exhaust, steering and suspension every 30k.

### #11 hyundai-i10-2014-2019
Source: Colmobil i10 2014-2019 book, PDF pp. 331-335 (pp. 7-9 to 7-12). Size matches the cloudinary file.

- **Wrong timing for three rows**
  - Page 7-10: "צינור אדים ומכסה מילוי דלק", "מסנן דלק" and "קווי דלק, צינורות וחיבורים" are I in the 55 and 115 columns (36 and 72 months).
  - Confirmed from word coordinates: the I glyphs sit at the y-position of the 55 and 115 header cells.
  - File: `evap_system`, `fuel_filter` and `fuel_lines` at 75,000 and 155,000.
  - The vacuum hose on the same page (35/75/115/155) is correct.
- **Invented entry**
  - File: `long_interval cooling_system inspect first 60,000/48 months, then 30,000/24 months`.
  - Book (p. 7-10, "מערכת קירור"): only "בדוק מפלס ודליפה של נוזל קירור כל יום; בדוק את משאבת המים כשאתה מחליף חגורת הינע או תזמון". It has no 60k/30k interval; that interval comes from other Hyundai books.
- Everything else matches: first service at 15k then every 20k, air filter I/R alternating, spark plugs 160k, valve clearance 95k/48 months (1.0 only), coolant 210k then every 40k, brake fluid R at 35/75/115/155, cabin filter R every service, gearbox inspection every 60k/48 months.

### #13 toyota-rav4-2020-2025-2.5-hybrid
Source: sheet 324, "ראב 4 HV AXAH52/54 A25A-FXS", dated 29.11.2018. Extra source: sheet 350.

- **Spark plugs**
  - Sheet: "מצתים – החלף כל 90.000 ק"מ".
  - File: missing.
- **Brake pads and discs**
  - Sheet: the regular row has I in all 10 columns. The I's under 15, 45 and 75 are printed slightly lower in the cell.
  - File: inspects only at 30/60/90/105/120/135/150 (parsed as `-I-I-IIIII`), so 15k, 45k and 75k lack the brake inspection.
- **Wrong item**: the hybrid-battery filter row (C at every service) became `air_filter clean`, the same mapping bug as in #3.
- **Second sheet misrepresented**
  - The file calls sheet 350 (RAV4 HV, 2023-2025) "אותו מבנה", but it differs:
    - cabin filter: ה (replace) at every service;
    - fuel filter: replace at 120k;
    - engine coolant: "לאחר החלפה ראשונה … מדי 75,000";
    - brake fluid: inspect at 15k, then replace every 30k;
    - adds a rear e-motor transmission fluid row.
  - Registry: about 26k cars from 2023-2026 are routed to this file.
- Everything else matches: CVT oil I at 60/120, evap at 45/90/135, air filter R at 60/120, cabin filter C/R alternating, coolant 150k/90k and 240k/90k.

### #14 toyota-c-hr-2016-2023-1.8-hybrid
Source: sheet 326, "C-HR היברידית ZYX11 2ZR-FXE", dated 29.10.2020. Extra source: sheet 286, which really is the same.

- **Spark plugs**: sheet says "מצתים – החלפה מדי 90,000 ק"מ"; file has nothing.
- **Fuel filter**: sheet says "מסנן דלק – החלפה מדי 120,000 ק"מ" (144 months); file has nothing.
- Everything else matches: cabin filter I/R alternating, brake fluid I/R alternating, coolant 160k/80k and hybrid coolant 240k/80k, gearbox I every 30k, hybrid-battery filter I at every service (mapped correctly here).
- Registry: about 3.5k cars from 2024-2026 named "TOYOTA C-HR" or "C-HR" with 2ZR (likely the second-generation AX20) are routed to this AX10 file. Rule 412 runs to 2026.

### #17 toyota-yaris-cross-2021-2025-1.5-hybrid
Source: sheet 340, "יאריס קרוס הייבריד MXPJ10 M15A-FXE", dated 18/09/2022. Extra source: sheet 354, which really is the same.

- **Spark plugs**: sheet says "מצתים – החלף כל 90,000 ק"מ"; file has nothing.
- Everything else matches:
  - fuel filter R at 75k and 150k;
  - E-CVT inspection at 30/60/90/120/150 (checked on a zoomed render);
  - hybrid-battery filter I/C alternating;
  - cabin filter R at every service;
  - coolant 150k then 75k, inverter coolant 240k then 75k.

### #19 hyundai-elantra-2022-2026-1.6-hybrid
Source: Colmobil "אלנטרה היברידית" book, PDF pp. 490-493 (pp. 9-8 to 9-11). Size matches the cloudinary file.

- **Clutch-actuator fluid (p. 9-10)**
  - Book: "נוזל בוכנת מצמד – החלף כל 30,000 ק"מ או 24 חודשים".
  - File: no `clutch_actuator_fluid` entry anywhere.
  - Only "צינור בוכנת מצמד" (I at every service) was transcribed, as `clutch inspect`.
- **Vapour hose and fuel lines (p. 9-9)**
  - Book: "צינור אדים ומכסה מילוי דלק" and "צינורות דלק וחיבורים" are both I at 60 and 120.
  - File: no `evap_system` and no `fuel_lines` entries.
- **Invented cooling-system entry**
  - Book: "מערכת קירור" is I at every 15k (correctly in the grid).
  - File: adds `long_interval cooling_system first 60k/48 months, then 30k/24 months`, which is not in this book.
- **Minor issues**
  - Coolant is stored as two identical long-interval entries (book: a single row "נוזל קירור מנוע/ממיר").
  - "סוללת מערכת eCall – החלף כל 3 שנים" is omitted.
- Everything else matches: HSG belt inspect every 15k and replace at 105k/48 months, air filter R at 45/90, brake fluid R at 45/90, cabin filter R at every service, spark plugs 150k, fuel-tank air filter I/R at 30/60.

## MINOR details
- **#1 kia-picanto-2017-2025**
  - Drive belt:
    - 2017 book p. 8-13: "החלפה ראשונה לאחר 90,000 ק"מ או 72 חודשים, לאחר מכן החלף כל 30,000".
    - 2021 AMT book p. 8-16 (PDF p. 458): "בדיקה ראשונה … לאחר מכן בדוק כל 30,000".
    - The file keeps `replace`, with a hedging note. The 2021+ book applies to the majority (G4LF engine, 2021-2026, ~42k cars).
  - Everything else matches both books: air filter I30/R60, cabin filter R every 30k, brake fluid I/R, spark plugs 150k (MPI) and 75k (T-GDI), valve clearance at 90k (1.0 engines), coolant 210k then 30k.
- **#10 hyundai-tucson-2015-2020** (source is the manualpdf.co.il text-layer mirror, not an original PDF)
  - Confirmed against the mirror:
    - brake fluid is literally `RRRRRRRR` (R in all 8 columns) and cabin filter `RRRRRRRR`;
    - spark plugs "150,000 (1.6) / 165,000 (2.0)";
    - drive belt first 90k/72 months, then every 30k;
    - coolant 210k/10 years, then 30k;
    - valve clearance I at 45k and 90k, and manual/DCT/4WD rows I at 30/60/90/120 (from the screenshot positions).
  - Fuel-tank air filter and fuel lines (`IIII`) have no recoverable positions; the "every 30k" placement is an assumption, disclosed in the notes.
  - `transmission_oil` long-interval entry: `replace every 100,000`; the book says that applies only to severe use.
- **#15 kia-sportage-2016-2018** (pp. 8-14 to 8-17)
  - The file's 15k grid derived from the book's 30k columns is consistent, and disclosed.
  - `transmission_oil` long-interval entry is "inspect every 90,000". Book: "אין צורך בבדיקה או טיפול"; severe use: R every 90,000.
  - The "גל הינע (AWD)" row (I every column) is omitted.
  - Valve clearance at 90k/180k has no engine note; the book lists it for 1.6 GDI, 1.6 T-GDI and 2.4 only, not 2.0.
- **#6, #12, #18 (registry notes)**
  - #6: 2,176 CX-5 cars from 2025-2026 with the PY (2.5) engine fall under plan '39547 CX-5 2025 NA' (2.5L from 2025), which has cabin filter every 30,000 or 2 years instead of every 15,000.
  - #12: 1,951 MAZDA 2 cars from 2015 with the ZY engine are the old DE generation (plan 2007-2014, valid to 2015, cabin filter every 30k).
  - #18: 655 MAZDA 3 cars from 2013 with LF/Z6 engines are MZR cars routed to the Skyactiv file.
- **#7 kia-picanto-2011-2016**: the book's 15,000 header reads "כל 15,000 ק"מ או 6 חודשים" (p. 7-8). Every other header (30k/24 months, 45k/36 months and so on) implies 12 months, so this is a book typo; the file correctly uses 12.

## Systemic finding (outside the 20, same root cause)
`scripts/build_schedules.py` `ty_long()` only finds "מצתים … החלפה מדי N" if the phrases appear in order in the extracted text. In the extracted text of most sheets they do not (for example "החלפה מדי7,500 ק"מ  החלפה מדי90,000 ק"מ 5.6 מסנן דלק מצתים"), so the long-interval rows are silently dropped. The same applies to the fuel filter and the drive belt in its merged-cell form.

A scan of all `data/schedules/toyota-*.json` found:
- **About 40 Toyota files with no `spark_plugs` entry.** Most are reviewed. Diesels (Hilux, City, most Land Cruiser) and the bZ4X EV are expected to have none; the petrol and hybrid ones are suspect: Auris, Aygo, C-HR, Camry, Corolla, RAV4, Verso, Yaris, Yaris Cross, Highlander.
- **5 more files with the battery-filter-as-`air_filter clean` bug:** Corolla Cross, Highlander, Prius 2023, Prius PHEV 2023 and Hilux 2026.

Separately, extra sheets are labelled "אותו מבנה" without checking. Sheets 345 and 350 differ materially from their primary sheets.
