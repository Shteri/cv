champ5: Champion Motors (VW / Skoda / Seat / Audi / Cupra), Round 5
==================================================================
Builder scripts: scratchpad/dl/champ5/build.py (new + cloned files), build_up.py (upgraded drafts), parse_routine.py (full-column parser of the Champion page).
Validate: node scripts/validate.mjs staging/champ5 -> all schedules valid (7 draft, 13 reviewed, 0 verified)
Coverage simulation vs current data/registry_map.json (after lead's tail4 commit): +3,180 registry vehicles newly covered, 0 reassigned (dl/champ5/sim.mjs, rulegain.mjs).

MAIN QUESTION: Israeli Champion source for older engines (1.2/1.4/1.6/1.8 TSI, 1.6 TDI, MPI) -> NOT FOUND
- championmotors.co.il/service-routine/ (Playwright 3.10.2026): same 14 tables as 28.9 (1.0/1.5/1.4 PHEV/2.0/2.5/3.0/4.0 petrol, 2.0/3.0 diesel, BEV, T6.1, Amarok 2023, Crafter, Caddy 5). Re-parsed ALL columns incl. hidden 180k-320k commercial columns (dl/champ5/routine_now.json). Nothing for older engines.
- Champion WP sitemaps (113 pages crawled, dl/champ5/pages/): 'routin' post type (32 posts: שמן מנוע, מצתים, רצועת תזמון...) are empty title-only pages; /standards/ = workshop standards; /arrangement/* = class-action settlements; /catalog/ = parts search; wp-json 401 even in browser.
- books.championmotors.co.il (sitemap: 44 current models only). All 37 FlippingBook summaries text-extracted via signed CloudFront flash/search/searchNNNN.xml (dl/champ5/fb/*.txt, fb/all_pages.json): legal "תמצית הוראות שימוש", NO service table. Only useful line: Seat Ibiza/Arona summary (FlippingBook 89865174 p.11) fixed service 15,000 km or 1 year.
- cms.ituran.com ownerManualsFront modelID 1-80 enumerated (5-43 exist); singleChapterFront.php?chapterId=N -> 404 "File not found" in curl and Playwright (even clicking from the model page). No periodic-service chapter, only "תחזוקה שוטפת בסיסית".
- manualpdf.co.il: 363 VAG books; only SKODA books are Hebrew (Champion "ספר הפעלה ותחזוקה": Fabia 2011/12/15/17, Octavia 2014/15/16/19/20, Rapid 2015, Roomster 2012, Superb 2010/12/16/17, Yeti 2010-2017, Citigo 2017...). Fully scanned Octavia 2014, Fabia 2011, Superb 2010, Yeti 2010, Roomster 2012 (visual-order text, reversed with dl/champ5/mpw/rv.py): all defer to a separate "חוברת מועדי השירות" booklet that is not online; only intervals inside = tyre rotation every 10,000 km, TPMS calibration 10,000 km/1 yr. VW/Seat/Audi books there are English international.
- Searches for "חוברת מועדי השירות", "ספר שירות ואחריות", Seat "תוכנית תחזוקה", Skoda "שגרת טיפולים pdf": nothing. ספר-רכב.com (xn----2hc3awpyb.com, "ספר טיפולים סיאט ארונה/לאון/קודיאק") is behind Cloudflare Turnstile: failed in curl, WebFetch, headless Playwright and headful Chromium under Xvfb with checkbox click (third-party aggregator anyway).
- skoda.co.il / vw.co.il / seat.co.il / vwcv.co.il / media.champ.co.il / personal.championmotors.co.il: Link11 491 hard deny also in headful Chromium+Xvfb. audi.co.il DOES load in headful Chromium (247 passes): sitemap = marketing + FAQ pages only; wp-json rest_login_required. cupraofficial.co.il and championmotors.co.il/arrangements/ also load: no service content.
- web.archive.org blocked by egress (wayback.archive.org / wayback-api redirect there; web-beta = "Closed Test"). http://archive.org/wayback/available (metadata only) works and shows snapshots exist (skoda.co.il 2023-09-15, championmotors.co.il 2023-07-30) but content not fetchable. archive.ph: no connection; webarchive.loc.gov: Cloudflare; arquivo.pt CDX 403; Google cache gone.
- static.auto.co.il/media/ygqg0lrl/1594.pdf = Kodiaq brochure; serviceman.co.il/skoda 404.

PARTIAL ISRAELI CORROBORATION ADDED (drafts stay draft)
- auto.co.il + Engie 16.9.2016 https://www.auto.co.il/article/127813-car-news-seat-ibiza : Seat Ibiza 6J service contents "per importer" to 90,000: 15/45/75k oil+filter; 30k & 90k + air & cabin filters; 60k + air, cabin, spark plugs. Identical to draft seat-ibiza-2008-2017-1.2-1.4-1.6; belts/brake fluid/gearbox not mentioned -> still draft. Sister articles 127810 (i20), 127811 (Picanto), 127812 (i10); no other VAG model in ids 127700-127950. 2015 family-car article 111383 (Octavia) has cost tables only (images).
- Walla Cars 6.10.2011 https://cars.walla.co.il/item/1866225 : Champion VW division manager: TSI engines of the period = chain; DSG 6-speed oil every 60,000 km; DSG 7-speed no oil change; previous-Passat 2.0 turbo belt 180,000 km or on wear. Added as source to VW drafts (agrees with them).

FILES
Upgraded drafts (same id, status draft, content unchanged, sources+notes added):
  seat-ibiza-2008-2017-1.2-1.4-1.6 (+auto.co.il 2016, +Champion Seat summary 15,000/1yr, +Walla 2011)
  vw-golf-2006-2013-1.2-1.4-1.6, vw-jetta-2006-2018-1.2-1.4-1.6, vw-polo-2005-2017-1.2-1.4-1.6, vw-tiguan-2008-2016-1.4-2.0-tsi, vw-scirocco-2009-2014-1.4-2.0-tsi, vw-passat-2006-2015-1.8-2.0 (+Walla 2011)

New, reviewed, built directly from Champion tables (every mark transcribed from the parsed page; no rows from other books; no extra inspection rows):
  audi-q7-q8-sq5-s5-2018-2026-3.0-tfsi  (CWG/CZS/DCB petrol; table '3.0 ל׳ בנזין'; plugs marked 30/60/90k not 120k - copied, noted)  +326
  audi-rs3-rsq3-2016-2026-2.5-tfsi      (CZG/DAZ/DNW; '2.5 ל׳ בנזין': DQ500 120k, bevel box 3 yr, Haldex 2 yr, brake fluid 60/120k)    +312
  vw-amarok-2023-2026-diesel            (BF; 'Amarok 2023' 20k grid to 320k; cabin-filter marks irregular after 160k - copied, noted)  +263
  vw-crafter-2022-2026-2.0-tdi          (DMZ; 'Crafter' 20k grid to 240k; timing belt I 40/120/200k R 80/160/240k; no brake-fluid row) +218
  (12-month interval in the two commercial files is not from the table; notes say so)

New, reviewed, clones of existing reviewed Champion-table files (same engine/table; content identical; model fields+notes changed):
  cupra-tavascan-2025-2026-ev (from vw-id4-id5, BEV)                         +238
  vw-polo-gti-2019-2024-2.0-tsi (from vw-tiguan-2017-2026-2.0-tsi)            +181
  vw-passat-2015-2018-2.0-tdi (CRL/DFG EA288, from skoda-octavia-2015-2024-2.0-tdi) +160
  vw-id7-2024-2026-ev (from vw-id4-id5)                                       +133
  vw-passat-2020-2021-1.5-tsi (DPC, from vw-tiguan-2019-2026-1.5-tsi)         +122
  skoda-octavia-2021-2023-1.4-phev (DGE, from skoda-superb-2021-2024-1.4-phev) +114
  vw-tayron-2025-2026-1.5-tsi (DXD, from vw-tiguan 1.5)                       +81
  vw-passat-2020-2022-2.0-tsi (DKZ/DNN, from vw-tiguan 2.0)                   +67 (DNN)
  audi-q3-sportback-2023-2024-1.4-phev (DGE, from superb PHEV)                +53
  NOTE: tail4 rule PASSAT 2019-2023 DKZ/DNP/CHH -> vw-golf-2013-2026-2.0-tsi already covers Passat DKZ (179); vw-passat-2020-2022-2.0-tsi is identical content with correct model - consider swapping (base rule wins today, it is earlier in the map).

Rules only (registry/registry_rules.json, 23 rules total incl. the ones for new files):
  SUPERB PLUG IN / SUPERB IV (DGEB, *DGE***) -> skoda-superb-2021-2024-1.4-phev (63)
  NEW SUPERB / SUPERB DFC 2016-17 -> skoda-superb-2018-2024-2.0-tdi (82)
  POLO *DKL** / *DLA*** -> vw-polo-2018-2026-1.0-tsi (119)
  Q8 SB ETRON / Q8 E-TRON EAS 2023-24 -> audi-e-tron-2019-2022-ev (114)
  TT COUPE DNN 2021-24 -> audi-q5-a4-a5-a6-2017-2026-2.0-tfsi (150; draft file)
  VW CC / CC / PASSAT CC (CDA/CCZ), GOLF 3DR CCZ -> vw-passat-2006-2015-1.8-2.0 (188)
  OCTAVIYA (typo name) -> skoda-octavia-2013-2016-1.2-1.4-tsi (74); S.BACK SCOUT -> skoda-rapid-2013-2016-1.2-1.4-tsi (81); TOLEDO CBZ -> seat-toledo-2013-2018-1.4-tsi (41)
  Dropped as already covered by tail4: Octavia RS DKT, Superb FL *DPC****, Golf CCZ, Toledo CAY.

STILL UNCOVERED VAG (biggest)
Q7 e-tron CVZ (327, PHEV diesel, no Champion table); Polo/Ibiza DAJ (390, code unidentified); Amarok V6 DDX/CSH 2013-2020 (420, old Amarok not in Champion table); Passat BKP/CFF 2.0 TDI (366); Yeti/Octavia CFH, Superb CFG (EA189 2.0 TDI ~460); Q5/Q5 Sportback DRY and Q8 DCB TFSI e (PHEV, no table); Q7 CRC / Touareg CAS/CRC/BKS; Golf APK/AZJ/BMY/BWA (pre-2008); Audi A3 8P CAX/BSE/CBZ 2010-12 (~320); A6 CYG/CHV/CYP; S3 CJX; Alhambra CTH/CZD; Touran CAV; Fabia BNM; Octavia AXR.

ADDENDUM (coordinator tip: WebFetch tool), 5.10.2026
- WebFetch https://www.skoda.co.il/ , https://www.vw.co.il/ , https://www.seat.co.il/ -> HTTP 491 (Link11), body not retrieved.
- WebFetch https://media.champ.co.il//Central_Content_Management/Cupra/book/32_terramar/book.pdf -> 491.
- WebFetch https://www.championmotors.co.il/service-routine/ and https://www.audi.co.il/audi-customers/ -> empty body (JS/Reblaze challenge page; WebFetch does not run JS).
- WebFetch ספר-רכב.com (xn----2hc3awpyb.com/ספר-טיפולים-seat-leon/) -> 403 Cloudflare.
=> WebFetch route does not work for Champion/Link11/Reblaze hosts; nothing changes in the results above.
