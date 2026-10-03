ev3 report (EVs / Chinese brands / new entrants, round 3)

19 schedules (13 reviewed from Israeli importer documents, 6 draft). node scripts/validate.mjs staging/ev3 -> all schedules valid (6 draft, 13 reviewed).
Registry rules: registry/registry_rules.json (24 rules; 4 map to existing repo schedules as sister mappings, marked with _note).
Estimated vehicles matched by the rules (registry-counts.json): about 42,600.
Build scripts: scratchpad/dl/ev3/_build/*.py; downloads in scratchpad/dl/ev3/. PDF page numbers are 1-based file pages.

NEW ROUTES WORTH REUSING
- Delek Motors brand sites (dongfeng.co.il; same platform on mazda/ford/bmw/mini/nio/voyah .co.il): /service-plan/ reads a CSV from
  /wp-admin/admin-ajax.php?action=get_csv_raw (Manufacturer, Model, DisplayName, FileName, Url). Url = SharePoint link
  (delekmotorscoil.sharepoint.com/:b:/s/Techtrain/...?download=1). Plain curl gets an Azure AD login page, but curl with a cookie jar
  (-c cj -b cj -L) gets the PDF: the first 302 sets an anonymous FedAuth cookie.
- Lynk & Co car guide API: https://gw.api.lynkco.biz/mobile-app/car-guide/v1/api/v1/guide/types, /guide/type/<TYPE>?language=en-US,
  /guide/type/<TYPE>/category/<id>, /guide/type/<TYPE>/data/topic/<id>, then /data/asset/<sha256-...> (302 to context.lynkco.com).
  E335_* = 02, DX11_* = 08, CX11_* = 01 (CX11 JSON has another shape, not parsed).
- WordPress media API worked: lynkco.co.il, skywell.co.il, zeekr-israel.co.il, seres.co.il, leapmotor.co.il, samelet.com (Leapmotor books
  are on samelet.com). Failed: mg-israel.co.il (401 REST login), dongfeng.co.il (PHP out of memory), smart.co.il/api2.colmobil.co.il
  (500/403 CloudFront), ora-israel.co.il (500).
- changan.co.il (Shopify) page /pages/ספרי-רכב-וכתב-אחריות links the Deepal Hebrew books on cdn.shopify.com.
- ora-israel.co.il /service and model pages link Colmobil cloudinary PDFs (warranty + car book).
- Seres M5 Hebrew book: text layer is a shifted font (Hebrew at U+02A0.., ASCII shifted by 0x1D); read from page images.

PER MODEL
MG S9 PHEV 15FKE 2026 (4,637) - draft - mg-s9-2026-1.5t-phev
  Sister table mg.co.uk/servicing "MG HS Plug-in Hybrid (2024 onwards)" (15,000 mi/12 mo -> 24,000 km, 5-year table); same 1.5T PHEV
  powertrain, and the registry gives EHS 2025-26 the same code 15FKE. Specs from MGS9 PHEV Owner Manual EU
  (cdn.mgmotor.eu/manuals/MGS9-PHEV-Owner-Manual-EN_compressed.pdf) pp.348-356; that manual has no schedule. mg.co.uk has no S9 table.
  Blocked: mg-israel.co.il/guide-books sends books only after a phone-number form (not submitted); WP REST 401; cdn.mgmotor.eu
  service-portfolio guesses for S9/HS PHEV 404.
MG EHS 15FKE 2025-2026 (613) - draft - mg-ehs-2025-2026-1.5t-phev
  Same UK HS PHEV (2024+) table (direct model match). MG HS 2024 EU owner manual has no schedule.
Lynk & Co 02 (3,669) - draft - lynk-co-02-2025-2026-ev
  Lynk & Co Car Guide EU (E335_MORE/CORE/2027_MORE) Maintenance > Service: 40,000 km/2 yr; brake fluid + cabin filter + washer top-up each
  service; reducer oil "replace at 80,000 km/4 yr"; coolant every 80,000/4 yr. Importer Meir: lynkco.co.il media has only warranty annexes
  (no table) and the 01 PHEV 2023 Hebrew book (no schedule); Meir price list (updates.mct.co.il/services) needs plate + phone.
  Not done: Lynk 08 PHEV / 01 PHEV (BHE15-DFZ, 2.2k): car guide gives only "every service / every other service", condition-based, no km.
Deepal S05 EV (2,958) - reviewed - deepal-s05-2025-2026-ev
  cdn.shopify.com/.../S05_2026.pdf (booklet CH 28982225, 07/2026) pp.13-15; same table in S05 Hebrew driver book pp.354-355.
  20k/12, to 200k. Reducer oil 3 yr/60k, brake fluid 4 yr/40k, coolant 3 yr/80k (long_interval). Tyre "I.A.R" from 40k read as rotation.
Deepal S07 (1,871) - reviewed - deepal-s07-2025-2026-ev
  .../2026.pdf (booklet CH 28981124, 07/2026) pp.14-16. Brake fluid R every 40k in grid; coolant R at 60/100/140/180k; reducer oil 3 yr/60k.
  Importer מכשירי תנועה ומכוניות (2004). deepal.co.il unreachable (egress connect rejected). Not done: S05 PHEV (JL469Q1, 162): books exist.
Zeekr X (2,994), 7X (1,793), 001 (1,360) - reviewed
  zeekr-israel.co.il WP media Hebrew books: Zeeker-BX_HEB26022024.pdf pp.345-346, Zeeker-001-DC1E-...Hebrew_012024.pdf p.352,
  Zeeker-7x_Hebrew_31072025.pdf p.420. 40,000 km/24 mo; brake fluid 24 mo; cabin filter 24 mo/40k (7X 24 mo); coolant 48 mo; reducer oil
  every 40,000 km. Brake fluid and coolant are time_based.
Dongfeng Box (2,631) - reviewed - dongfeng-box-2025-2026-ev
  Delek Motors plan PDF "250857 39609 Dongfeng_Box_2025_and_up" via the CSV/SharePoint route: 30k/24; cabin filter each; brake fluid and
  coolant 60k/4 yr; reducer oil 90k/6 yr; cycle 180k.
Skywell ET5 (2,424) - reviewed - skywell-et5-2021-2025-ev
  skywell.co.il: warranty/service booklet 1.9.24 p.10 (free check 5,000/6 mo, then 40,000/24 mo; coolant, brake fluid, reducer oil, cabin
  filter each time; cabin filter note 12 mo/20k); ET5 driver book 2022 p.256 (fluids), p.266 (rotation 10k); short book 03.24 p.13.
  The 5,000 km check is in notes only (does not fit the grid).
ORA Funky Cat / ORA 3 (2,656) - reviewed - ora-funky-cat-2023-2026-ev
  Colmobil cloudinary ora-warranty-06.2024-1.pdf pp.8-9: 30k/24 to 210k; cabin filter each; brake fluid 2 yr/40k; coolant 4 yr/40k; gearbox
  oil only in severe use (50k). Specs from ספר-רכב-אורה-03-28.3.pdf p.221. ORA 3 (2025-26) same motor code, same plan (assumption).
Xpeng G9 (1,915), P7i (1,775) - draft
  XPENG Benutzer- und Wartungshandbuch (für Deutschland), edge.sitecorecloud.io (Hedin) pp.15-21, applies to all XPENG models sold in the EU;
  identical to the G6 EU manual already in the repo. Files are copies of xpeng-g6 with these sources.
  Blocked: G9/P7 manuals on the datamotive S3 bucket 403; xpeng.co.il not retried (502 in round 2).
Hyundai Ioniq 6 (1,354) - reviewed - hyundai-ioniq-6-2023-2026-ev
  Colmobil cloudinary ספר-רכב-איוניק-6-2023.pdf (2024 file identical) pp.533-535; Ioniq6-2026-OM-web.pdf pp.480-483 (same table).
  30k/24, cycle 240k; reducer fluid inspect every 60k (severe: replace 120k); coolant first 200k/10 yr then 40k/24 mo; eCall battery 3 yr.
Leapmotor C10 EV (1,028 in counts file), C10 REEV (880), B10 (351) - reviewed (importer סמלת, samelet.com media)
  C10 EV: LEAP-C10-RWDAWD-HEB.pdf pp.141-146 (20k/12; brake fluid 2 yr/40k; coolant 4 yr/40k; reducer oil+filter 60k; cabin 1 yr/20k;
  rotation 10k). B10: B10-גירסה-סופית-מכווצת.pdf pp.162-164 (same plan).
  C10 REEV: LEAP-C10-REEV-NOV2025-חדש-עם-שגרת-טיפולים.pdf pp.165-170: grid 15k/12; engine items from text (oil 1 yr/10k, printed "10,00";
  air filter 2 yr/20k; plugs 40k; canister filter 1 yr/20k); coolant 4 yr/45k in table vs 40k in text. Inconsistencies in notes.
  Not done: T03 (Metro Motor era, ~1k): T03 Hebrew book p.166 gives only "3,000 / 10,000 / every 10,000 km or yearly", no item list;
  Leapmotor international sites 403.
Seres 5 / M5 (3,223) - reviewed - seres-5-m5-2023-2025-ev
  seres.co.il SERES_M5_EV_OM_24-09-24 (Hebrew; cover "SERES M5", body "EV SERES 5") p.206 intervals, p.207 items: inspection 1 yr/20k,
  cabin filter 1 yr/20k, brake fluid 3 yr/60k, battery coolant 4 yr/100k, reducer oil 5 yr/100k (Castrol 805C EV).
  Assumption: registry "SERES" 2023-2025 (SEP201) = same car (renamed M5). Importer טלקאר מוטורס.
  Not done: SERES 3 (1.7k): warranty booklets are scans pointing to the driver book; no Seres 3 driver book found.
BYD Atto 3 EVO (1,318) - draft - byd-atto-3-evo-2026-ev
  BYD Europe Hebrew book .../0820atto3evo/ATTO 3 EVO Owner's Manual-Left-hand Drive-20260427-HE.pdf pp.173-174. The table mixes
  "20,000 miles" (inspections) and "20,000 km" (cabin filter, brake fluid, gear oil); EN and NL books have the same mix. Draft uses
  20,000 km/24 mo; gear oil first 20k then 30k/24 mo; coolant 6 yr/"60,000 miles" recorded as 60,000 km. Verify with Shlomo Motors.

SISTER MAPPINGS IN RULES ONLY (no new file)
- MG S5 (432), MG S6 (509) -> mg-4-2023-2026-ev (same motor codes as MG4; MG UK tables for MGS5 EV and MG4 EV 2026 are identical;
  MGS6 EU manual has no schedule).
- Omoda 9 PHEV (1,302) -> jaecoo-8-2025-2026-1.5t-phev (same SQRH4J15; repo already maps Omoda 7 PHEV the same way).
- Jaecoo 5 BEV (930) -> chery-fx-ev-2024-2026-ev (same motor TZ180SMZB0; no J5 BEV book on jaecoo.co.il/car-book).

NOT FOUND / BLOCKED
- Smart #1/#3 (~1.9k): smart.co.il (Colmobil) states 2 years or 30,000 km, but the book is emailed only after a form (not submitted);
  api2.colmobil.co.il REST/GraphQL 403; smart Australia: 12 mo/20,000 km, prices only. No item list -> not written.
- Volvo EX30 (~1k): volvocars.com 403 (curl and Playwright, Akamai). Not written (Lynk 02 sister possible but Volvo has its own programme).
- Aiways U5 (2,032): aiways.co.il 403; manuall.co.uk Cloudflare; not on manua.ls/manualslib.
- Maxus MIFA 7 (~1.5k): maxus-israel.co.il parked; three importers; not pursued.
- EVEC LIMO (1.7k): evec.co.il unreachable.
- Mercedes EQA, Volvo/BMW/Mercedes PHEVs, Genesis GV60: not attempted (premium groups).
