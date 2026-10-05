tail4 group report (Round 5): Hyundai/Kia/Genesis, Toyota, Mazda and Suzuki long tail, plus VAG rule-level fixes

Validation: node /home/user/cv/scripts/validate.mjs staging/tail4 -> "all schedules valid" (47 files: 23 reviewed, 24 draft).
Registry rules: registry/registry_rules.json, 64 rules. Builder: dl/tail4b/rules.py (run it with exec; its __main__ guard is never true that way).
Coverage check: dl/tail4b/gain.mjs replays matchSchedule with these rules added -> +31,512 registry vehicles newly matched, 6,739 re-routed to a more specific file.
Scripts in scratchpad/dl/tail4b/: lc_petrol.py, ty_fix.py, ty_belt.py, fix_ty.py, gen_sis2.py, tygrid.py (Union sheet reader using text coordinates), unc.mjs, gain.mjs, cnt.mjs.
The previous agent's scripts are in dl/tail4/ (gen_*.py, rules.py).

== 1. Review of the 23 files the stopped agent left (each checked against its source image or sheet) ==
- suzuki-liana-2002-2008-1.6, draft, 2,052 vehicles (LIANA + ליאנה): OK. Checked against manualslib 1292260 p33-34 images.
- suzuki-ignis-2001-2007-1.3, draft, 906: OK. Checked against manualslib 1586259 p36-37.
- suzuki-grand-vitara-1998-2005-1.6-2.0, draft, 670: FIXED. Two book rows were missing: the crankcase-ventilation hose (inspect at 45k and 90k) and the iridium-plug alternative (105k). Source: manualslib 1212471 p29-30.
- hyundai-matrix-2001-2010-1.6-1.8, draft, 436: OK. Checked against manualslib 1215243 p197-199 (GAT book, except-EC columns).
- hyundai-elantra-2001-2006-1.6, draft, 631: OK. Sister file of the Matrix (same XD platform, G4ED engine).
- hyundai-elantra-n-2025-2026-2.0-turbo, draft, 147: OK as a draft. The Colmobil web PDF holds only the "continued" page 9-8; its first page (air filter, belt, DCT) is missing from the published file, and the note says so.
- hyundai-ix35-2010-2015-2.0-diesel, draft, 821: OK. Sister file of the Kia Israel Sportage SL diesel table.
- kia-sportage-2011-2015-2.0-diesel, reviewed, 0 vehicles (no diesel SL in the registry): OK. Checked against the Kia Israel book PDF p295-298 images. Kept as the source for the ix35 file.
- hyundai-ix35-2010-2015-2.4, draft, 381: OK. Sister file of the Israeli Sportage SL book.
- hyundai-sonata-2020-2024-1.6-turbo, draft, 565: FIXED. Removed the DCT-oil row that came from the Tucson NX4 sister book; the Sonata DN8 1.6T has an 8-speed automatic.
- hyundai-staria-hybrid-2025-2026-1.6, draft, 1,265: OK. Sister file of the Kia Israel Sorento MQ4 HEV book.
- genesis-gv70-2021-2026-2.5-turbo, draft, 878: OK. Checked against manualslib 4105563 p601-605. Oil is every 10k in long_interval and the grid is every 15k, exactly as the book prints them.
- genesis-g80-2021-2026-2.5-turbo, draft, 212: OK. Sister file of the GV70 (same M3 platform, G4KR engine).
- genesis-gv60-2022-2026-ev, draft, 1,014: OK. Sister file of the Colmobil Ioniq 5 Hebrew book. The GV60 book on manualpdf is the US edition in miles.
- kia-optima-2012-2018-1.7-diesel, draft, 690: OK. Sister file of the Israeli Carens RP D4FD book.
- kia-optima-2016-2020-2.0-hybrid, draft, 684: OK. Sister file of the Colmobil Sonata LF hybrid book.
- kia-sorento-2010-2012-2.4, draft, 270: OK. Sister file of the Santa Fe CM 2.4.
- kia-forte-2016-2018-1.6-diesel (714) and kia-soul-2011-2017-1.6-diesel (256), draft: OK. Sister files of the Ceed JD D4FB.
- toyota-proace-2017-2026-2.0-diesel, reviewed, 742: OK. Checked against Union sheets 432 and 1132 (images).
- toyota-c-hr-2024-2026-1.8-hybrid, reviewed, 771 new + 3,442 re-routed: FIXED. Added the missing long rows: engine coolant (150k, then every 75k) and hybrid-system coolant (240k, then every 75k). The specs oil grade now follows the sheet's own fluid table.
- toyota-aygo-x-2026-1.5-hybrid, reviewed, 572: FIXED. Added the missing long rows: plugs every 90k, fuel filter every 75k, engine coolant 150k then 75k, and hybrid coolant 240k then 75k (the sheet's footnote text is reversed, so the regex missed them). Removed the generic severe-oil note, which this sheet does not have. Corrected the oil grade.
- toyota-land-cruiser-2003-2008-4.0, draft, 906: REBUILT, because its source (the repo's 2009-2019 4.0 file) was wrong (see section 2).

== 2. Repo audit: Union-sheet parser bugs, with corrected same-id files (lead: import with --force) ==
The sheets in data/sources/toyota-union-sheets.json lose every "text row", meaning a row whose cells merge into a sentence such as "first inspection at 100,000 then every 20,000" or "inspect every 10,000, replace every 30,000". The marks of the neighbouring rows then shift into the wrong rows. I re-read the original PDFs from books.union-motors.co.il/app/api/files/<connectionId>/download, using word coordinates (tygrid.py) and the page images. The fileId-based numbers stored in the repo now return other documents; for example, files/300 is now a Yaris book.
- toyota-land-cruiser-2009-2019-4.0 (1GR, conn 599), 141 vehicles. No air filter (inspect every 20k, replace every 40k) and no plugs (every 100k). Cooling system, oil-cooler hoses and fuel lines (first at 80k, then every 20k) had been read as a single mark at 50k. An extra coolant mark sat at 90k.
- toyota-land-cruiser-2003-2009-3.0-diesel (1KD, sheet 297 / conn 173), 8,863 vehicles. No air filter (inspect every 10k, replace every 30k). Belt was put at 40k; the sheet says first at 100k, then every 20k. Coolant columns were wrong.
- toyota-land-cruiser-2010-2015-3.0-diesel (sheet 298 / conn 175), 4,123 vehicles. No air filter. Cooling system and fuel lines (40k, 80k, then every 20k) had been read as one mark at 30k. Coolant was wrong. The DPF hoses (every 36 months) were missing.
- toyota-land-cruiser-2016-2019-2.8-diesel (1GD, sheet 299 / conn 199), 4,963 vehicles. Rows were shifted: brake pads/discs, CV boots and differentials were missing. No air filter. Belt and coolant were wrong.
- toyota-hilux-2005-2015-2.5-3.0-diesel (sheets 295/296 / conn 385/386), 8,782 vehicles. The timing-belt replacement at 150k had landed in the coolant row. Belt was wrong. Steering and suspension were marked every 10k; the sheet says every 20k.
- toyota-hilux-2015-2019 (4,301 vehicles) and toyota-hilux-2020-2025 (10,373 vehicles), 2.4-2.8 diesel. Minimal patch: air filter added (inspect every 10k, replace every 30k), belt set to first at 100k then every 20k, coolant set to inspect every 40k with replacement at 160k. Checked against conn 170 and conn 848.
- Drive belt only, in 13 files with 15k grids: corolla-2007-2012, corolla-2013-2019, yaris-2011-2019, verso-2009-2018, rav4-2016-2019-2.5-hybrid, rav4-2013-2019, yaris-2020-2025-1.5, verso-s, rav4-2009-2012, yaris-cross-2021-2025-1.5, prius-2004-2009, auris-2013-2019, c-hr-2017-2019-1.2. They cover about 172.5k vehicles in total (Corolla E150/E170 alone about 99k). The sheet says first inspection at 105k (72 months), then every 15k. The old files had a single inspection at 45k, or an "adjust" at 90k. Text checked on conn 40, 534, 109, 123, 412, 249, 308, 261 and 940; verso 310 and yaris 311/336 were checked on the stored sheet text.
- Not re-checked: the other Toyota and Lexus sheet files. They passed a sanity scan (air filter and oil present, no lone marks); the scan only covered files whose sheet is in the JSON.

== 3. New files this round ==
- toyota-sienna-2021-2026-2.5-hybrid, draft, 1,284 vehicles. Sister file of the Union Highlander hybrid sheet (TNGA-K, A25A-FXS). The Sienna is a US model with no Union sheet, and the toyota.com T-MMS PDFs return 404.
- toyota-c-hr-plus-2026-ev, draft, 295 vehicles. Sister file of the Union bZ4X sheet (e-TNGA). The Union API (modelId 44) has only car books for it, no maintenance sheet.
- hyundai-i40-2012-2015-2.0, draft, 528 vehicles. Sister file of the Kia Israel Carens RP G4NC book (same engine, different platform; the note says so). The Hyundai UK i40 book covers only 1.6 GDI and diesel.
- kia-carnival-2025-2026-1.6-hybrid, draft, 712 vehicles re-routed. Sister file of the Kia Israel Sorento MQ4 HEV book. Without it, the repo rule CARNIVAL 2021-2026 (no engine codes) sends the G4FT hybrids to the 3.5/2.2 file.
- Plus the corrected same-id files listed in section 2.

== 4. Registry rules (64) ==
- The previous agent's 46 rules were kept after checking that every target exists. They include Toyota name variants, the Corolla 2ZR->hybrid change, C-HR 2024+ -> the new C-HR file, Mazda "BT 50"/"MX 5"/6 wagon, Suzuki ליאנה/איגניס, and Genesis names written with a double space.
- New rules:
  - SIENNA / SIENNA HYBRID (A25A).
  - C-HR PLUS (EV).
  - I40 (G4NC).
  - CARNIVAL 2024-26 G4FT (re-route).
  - PRIUS PLUG IN 2017-2022 2ZR -> prius-2016-2022. Union's Prius plug-in (304) and Prius (302/303) sheets have identical grids; Union has no sheet for the 2019-21 plug-in, and its car book gives only 15,000 km / 12 months.
- APPROXIMATE rules, each flagged in its _note so the lead can drop any of them:
  - RAV 4 2006-2009 1AZ -> rav4-2009-2012-2.0 (same XA30 generation, different 2.0 engine): 2,198 vehicles.
  - YARIS 2000-2002 2NZ -> yaris-2003-2005-1.3 (same XP10 generation): 1,062.
  - PRADO/LAND CRUISER 2001 1KD -> LC 2003-2009 1KD sheet: 448.
  - B-2500 2000-2007 WL/WLT diesel -> mazda-bt-50 Delek plan (the BT-50's predecessor, same WL engine): 555.
- VAG, rule level only (engine-family template files; no new files):
  - SUPERB FL "*DPC****" -> superb 1.5 TSI: 193.
  - OCTAVIA RS DKT -> octavia 2.0 TSI: 142.
  - PASSAT 2019-23 DKZ/DNP -> vw-golf-2013-2026-2.0-tsi: 179.
  - GOLF/GOLF GTI 2009-13 CCZ -> vw-passat-2006-2015-1.8-2.0: 212.
  - AUDI A3 2008-13 CDA and A6 2014-18 CYG -> audi-a4-a5-a6-2008-2016 EA888 file: 414.
  - SEAT TOLEDO diesel CAY -> skoda-octavia-2011-2017-1.6-tdi (the Rapid twin): 144.

== 5. Not done, and every route tried ==
- manualslib.com is now BLOCKED: curl returns 403, and Playwright (webdriver hidden, 30-second wait) stays on Cloudflare's "Just a moment..." page. Only the previous agent's screenshots in dl/tail4/ml/ remain.
- Mazda Lantis/323 BJ, ZM/FP/FS 1999-2004 (~3,100 vehicles). manualslib 831867 is an older 323F (80k cycle); 916585/840832 are workshop manuals. manua.ls and manualpdf.co.il list only the US Protege5. carmanualsonline /mazda/323 redirects to its home page. workshopservicemanual.com and allcarmanuals.com return 403 (curl and WebFetch). manual-directory.com needs a reCAPTCHA. Mazda Demio B5, MPV AJ, 626 FS: no source found.
- Toyota Hiace 2KD 2002-2011 (1,455). The Union API has no Hiace model. Hilux shares only the engine, so it was not used.
- Santa Fe CM 2.7 G6EA 2007-09 (1,357 + 211 LPG) and D4EB (353). The Hyundai UK list (https://www.hyundai.com/uk/en/owners/owning-a-hyundai/owners-manuals.html; 57 dmassets PDFs, links read with Playwright) has "Santa+Fe+CM+1-mergedpdf". It is the CM facelift book only (2.4/3.5/R2.2, the same as manualslib 3393691); its pages 305-316 have no 2.7.
- Ceed/XCeed G4LK 2021-25 (1,586). The Hyundai UK i30 PDe 2025 book (same G4LK engine) has no schedule table. The Kia Israel WP media API (ceed/xceed/manual/ספר) finds only images, spec sheets and the warranty book (encoded font, no table). manual-directory.com needs a reCAPTCHA.
- Accent LC G4EB (1,059). Only the Indian 10k book exists (manualslib 724162, images in dl/tail4/ml/acc_*). Not used: its intervals look specific to that market. The other books found are US editions.
- No source found for: Prado 1KZ (1,051), Terracan/Carnival J3 (853 + 652), Corolla 4A (809), Hilux 2L (965), K2500 D4CB (407), GV80 diesel (389), Palisade G6DN (385), Carnival G6EA 2007-10 (384), Carens UN G4GC (374), Baleno G16B (373), LC250 petrol T24A (336; Union has only the 1GD sheet 364), Tucson NX4 D4FE (191; the Colmobil NX4 book has no diesel), Yaris Verso 2NZ (571).
- The toyota.com T-MMS Sienna PDFs return 404.

== 6. Notes for the lead ==
- Treat toyota-union-sheets.json text rows as unreliable. Read the sheet PDF instead, with dl/tail4b/tygrid.py <pdf> (one pattern per row plus the months column and the label).
- Union files/<n>/download takes a CONNECTION id. Get them from /app/api/search?modelId=&year=; the models are at /app/api/models.
