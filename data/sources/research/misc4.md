misc4 report (round 4: KGM/SsangYong, GM (Cadillac/Buick/Chevrolet), Chrysler group, Isuzu; premium/Chinese leftovers attempted)

22 schedule files (4 reviewed, 18 draft) + registry/registry_rules.json (33 rules).
node scripts/validate.mjs staging/misc4 -> "all schedules valid (18 draft, 4 reviewed, 0 verified)".
Simulated coverage (repo registry_map.json first, then these rules; dl/misc4/cov.mjs over registry-counts.json): ~21,900 newly covered vehicles.
Build scripts: scratchpad/dl/misc4/gen/{kgm,sister_ssy,gm,chrysler,chrysler_box,rules,dump_rules}.py (run in that order).
Downloads: dl/misc4/ (KGM books), dl/misc4/gm/ (GM/Chrysler US manuals), renders in dl/misc4/img/. PDF pages are 1-based file pages.

MAKES (scripts/lookup_plate.mjs): "SsangYong", "KGM" and "EVEC" (איויאיסי) are all present. Nothing to add.

NEW ROUTES WORTH REUSING
- kgm.co.il WordPress media API: /wp-json/wp/v2/media?mime_type=application/pdf&per_page=100 lists all Hebrew books (Rexton 2018/2024,
  Torres petrol, Torres Hybrid, Musso Q300, Musso EV, Korando C300, Tivoli diesel appendix). Rexton 2024 text layer is a shifted font -> page images.
- cdn.dealereprocess.org/cdn/servicemanuals/<brand>/<year>-<model>.pdf: US owner's manuals for buick, cadillac, chevrolet, chrysler, dodge, jeep
  (minivan = chrysler/<year>-townandcountry.pdf). Parsers: dl/misc4/gm/gmparse.py (GM "@" charts by coordinates), gm/boxparse.py (Chrysler boxes).
- data.gov.il model table (resource 142afde2-6228-49f9-8a29-9b6c3a0cbe40, q=<degem_nm>) gives cc/hp/"היברידי רגיל"; with the vehicle table
  (053cea08..., filter degem_manoa) it decodes engine codes: TORRES 177910 = E0A1R hybrid; LACROSSE 4CB=2.4, 4DB=3.6, 4GA=3.0; TRAVERSE NDA/NDB=3.6.
- books.union-motors.co.il/LexusApp/api/models?brand=lexus -> /models/<id>/years -> /search?modelId=&year= -> files/<connectionId>/download.

PER SCHEDULE (vehicles newly matched | id | status | interval | source)
3019 | kgm-rexton-2021-2026-2.2-diesel | REVIEWED | 15,000 km/12 m |
  kgm.co.il/wp-content/uploads/2024/04/240370_REXTON_OM_Y461-17-04-24-AllBookForWeb.pdf pp.6-5..6-7 (PDF 464-466) "D22DTR - (GEN)"
  (EU table 6-2, 20,000 km, is EU-only). Fuel filter 30k, axles 30k (IRS 60k), transfer 60k, ATF inspect (severe replace 60k),
  coolant 5 yr/200k, brake fluid 2 yr. Applied to 2021-2023 too (same code 672980) - noted.
453 | ssangyong-rexton-2018-2021-2.2-diesel | REVIEWED | 15,000/12 | kgm.co.il/wp-content/uploads/2020/10/new_Rexton_OM_2018-.pdf
  pp.7-5..7-7 (PDF 393-395) "D22DTR (כללי)"; frequency columns mapped onto 15k services; fuel filter 45k, air filter 30k.
554 | ssangyong-rodius-rexton-w-2016-2019-2.2-diesel | draft | sister copy of the Rexton 2018 table (same D22DTR, code 672.960).
341 | kgm-musso-2024-2026-2.2-diesel | draft | 15,000/12 | .../2026/08/260841-MUSSO-Q300-OM-S1-SH-20-08-26.pdf pp.6-5..6-7 (PDF 453-455);
  draft because the book is the 2026 Q300.
1281 | kgm-torres-2024-2026-1.5t | REVIEWED | 15,000/12 | .../2025/02/241583-Torres-gasoline-OM-AllBookOptRF-03-02-25.pdf pp.6-2..6-4
  (PDF 420-422). Korando C300 Hebrew book petrol table (Ssangyong_Korando.pdf PDF 439) is identical -> TIVOLI/KORANDO 175950 rules point here.
1077 | kgm-torres-hybrid-2025-2026-1.5t-hev | REVIEWED | 10,000 km/12 m | .../2026/03/251095-TORRES-HYBRID-2025-OM-Print.pdf pp.6-8..6-10
  (PDF 490-492) "HEV". Coolant row printed "20,000 km or 5 years" (petrol table: 200,000) -> recorded as 5 years only, flagged.
242 | ssangyong-korando-tivoli-2018-2023-1.6-diesel | draft | 15,000/12 | .../2020/10/Ssangyong_Korando.pdf pp.6-5..6-7 (PDF 433-435);
  also used for TIVOLI XLV diesel (same 673910; Tivoli diesel appendix has no table).

GM (importer יו.אם.איי; chevrolet.co.il/cadillac.co.il 403) - all draft, US/Canada owner's manuals (km printed):
1522 | cadillac-xt4-xt5-2019-2026-2.0t (LSY) | 12,000/12 | 2021 XT4 PDF 359-365 (+2021 XT5 2.0 rows). Air filter per life monitor.
965 | cadillac-xt5-2017-2019-3.6 (LGX) | 2018 XT5 pp.330-334 (PDF 331-335).
834 | cadillac-xt5-xt6-2020-2026-3.6 (LGX) | 2021 XT5 PDF 377-383; 2022 XT6 PDF 382-388. Air filter per life monitor (no km).
584 | cadillac-srx-2013-2016-3.6 (LFX) | 2014 SRX PDF 355-360.
464 | cadillac-ats-cts-2013-2019-2.0t (LTG) | 2016 ATS PDF 379-386; CTS LTG as sister.
223 | cadillac-srx-2010-2012-3.0 (LF1) | 2011 SRX PDF 454-458 (text format "first oil change after every X km").
1331 | buick-lacrosse-2010-2012-2.4-3.0-3.6 (4CB/4DB/4GA) | 2011 LaCrosse PDF 414-418.
345 | buick-lacrosse-2012-2016-2.4-3.6 (LFX) | 2012 LaCrosse PDF 433-438 (image charts).
427 | chevrolet-traverse-2025-2026-2.5t (LK0) | 2025 Traverse pp.330-333 (PDF 331-334).
2452 | chevrolet-aveo-optra-2004-2010-1.4-1.6 (Aveo F14D3/F14D4, Optra F16D3) | 12,500/12 | 2008 US Aveo pp.6-4..6-17 (PDF 328-341),
  Long Trip/Highway schedule; US engine = 1.6 E-TEC II (= Optra F16D3, same family as 1.4). Timing belt 100k. Sister/draft.
Rules to EXISTING repo files: Traverse NDA/NDB 2009-2014 -> chevrolet-traverse-2009-2017-3.6 (473); Captiva LE5 2011-12 ->
  chevrolet-captiva-sport-2012-2015-2.4 (201, sister, verify).

Chrysler group (importer סמלת) - all draft, US owner's manuals:
816 | chrysler-grand-voyager-2011-2017-3.6 (G, petrol+LPG) | 16,000/12 | 2014 Town & Country pp.662-666 (PDF 664-668), chart from renders.
325 | chrysler-grand-voyager-2008-2010-3.8 (EGL) | 10,000/6 | 2010 Town & Country boxes (PDF 494-506).
415 | chrysler-pacifica-2017-2026-3.6 (petrol) | 16,000/12 | 2019 Pacifica pp.509-511 (PDF 511-513).
395 | dodge-journey-2008-2014-2.4-3.6 (ED3, G) | 13,000/6 | 2012 Journey boxes (PDF 554-580).
897 | jeep-patriot-dodge-caliber-2007-2012-2.0-2.4 (ED3/ECN; Compass MK ED3/ECN as sister) | 10,000/6 | 2010 Patriot (PDF 452-466) and
  2010 Caliber (PDF 442-454), identical except AWD PTU/RDA rows.

Isuzu (rules to existing repo files):
2162 | PICK-UP 4JK1 2007-2011 -> isuzu-d-max-2007-2011-3.0-diesel. SISTER, lead to decide: 4JK1 = 2.5 of the 4JJ1 family in the same TF
  D-Max; the KB P190 workshop manual covers 4JK1 vehicles but its GENERAL EXPORT schedule rows name only 4JJ1.
72 | "PICK -UP" 4JK1 2015-16 -> isuzu-d-max-2012-2020 (spelling missing from current rule). 30 | PICK-UP RZ4E 2021 -> 2021-2026 file.

NOT COVERED / BLOCKED (biggest first)
- BMW diesels (B57/N57 ~3.1k), N-engine petrol (~5k), BMW i: bmwusa.com now hangs for every path (curl, Playwright request, WebFetch 503),
  incl. the MY2025 booklet that worked in round 3; bmwtechinfo 2017 booklet 404.
- Mercedes Vito/V-Class/Vito Tourer OM654/OM651 (~3.4k): mercedes-benz.co.il/vans pages link only spec sheets (no interval); UK dealer 403;
  only press figures (25,000 km/12 m or 40,000 km/24 m) without items.
- Chery Tiggo 4 Pro SQRG4G15 (2,369; data.gov.il degem DB21B = 1.5 NA 95 hp automatic): cheryisrael.co.il 403 in Playwright, freesbe.com 403,
  chery.co.za JS app/404, only an inconsistent Russian dealer page.
- Aiways U5 (2,032): manuall.de/.co.uk Cloudflare (also Playwright); ai-ways.eu no WP API.
- Seres 3 (1,681): seres.co.il Seres3 warranty booklet (shifted font) refers to the driver book; no driver book found.
- EVEC LIMO (1,666): EVeasy (Freesbe) = JMEV Yi / Mobilize Limo; no schedule found.
- ORA 5 SUV GW4B15M (1,094): Hebrew OM res.cloudinary.com/colmobil/images/v1790231226/ORA-5-OM_web/ORA-5-OM_web.pdf has no maintenance table.
- Smart #1/#3, Lynk 08/01 PHEV, Mercedes EQA/EQC, BMW iX3: no km table (see ev3/prem3).
- Land Rover 2019+: TOPIx procedures found (162966, 491499, 565243) are pre-2019 handbooks.
- Lexus RX350/RX450h 2GR 2010-2018: "RX RANGE" book (conn 144) no table; RX300/RX350 book table is 8AR only; IS300 8AR 2021+ book (conn 119) no table.
- Volvo S60 B5244S / T4 B4164T / S40 2.0: no official km schedule reachable.
- Older SsangYong (Rexton/Rodius 665, 671.960; Tivoli 1.6 petrol): no books on kgm.co.il.
- Chevrolet Spark L5Q, Sonic A14XER, Orlando/Captiva diesel: no US equivalent engine.
