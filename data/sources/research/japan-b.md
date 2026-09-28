# japan-b report (Nissan, Honda, Lexus, leftover Toyota)
29 schedule files (11 reviewed, 18 draft) and 33 rules in registry_rules.json.
validate.mjs also reads registry_rules.json as if it were a schedule. Run on a copy of the folder without that file, it prints "all schedules valid (18 draft, 11 reviewed)" (script: scratchpad/dl/japan-b/val.sh).
Generators: scratchpad/dl/japan-b/{gen,lexus,lexus_sister,toyota,nissan,honda}.py. Downloads: scratchpad/dl/japan-b/*.

## Lexus (יוניון מוטורס)
Lexus has its own copy of the Toyota books API at https://books.union-motors.co.il/LexusApp/api/ (models?brand=lexus, models/{id}/years, search?modelId=&year=, files/{conn}/download). /app/api/models?brand=lexus returns [] and there are no maintenance sheets.
The older, shorter Hebrew books have a table in chapter 7-2. The newer full books point to the service booklet instead.
- lexus-ct200h-2011-2020-1.8-hybrid, reviewed: conn 88, pp.87-88
- lexus-nx300h-2014-2021-2.5-hybrid, reviewed: conn 162, pp.98-99
- lexus-is300h-2013-2020-2.5-hybrid, reviewed: conn 114, pp.89-90
- lexus-gs300h-2013-2018-2.5-hybrid, reviewed: conn 107, pp.106-107
- lexus-nx200t-2014-2017-2.0-turbo, reviewed: conn 154, pp.92-93
- lexus-rx450h-2016-2022-3.5-hybrid, reviewed: conn 150, p.746 (sheet dated 26.4.18)
- NX350h, ES300h, LBX and NX450h+ are drafts copied from sister Toyota sheets: RAV4 hybrid, Camry hybrid, Yaris Cross hybrid and RAV4 PHEV. Their Hebrew books (conn 123, 42, 36, 124) have no table.
- Flag: the CT, NX300h, IS300h and GS300h books word the coolant row as "בדיקה ראשונה ב-150,000". I coded it as a replacement, as the RX and NX300 books have it, and added a note.
- Not done: UX250h (no table, no sister), UX200 (conn 72, pp.396-397), NX300 (conn 158, pp.480-481), RX300/350 (the conn 145 download failed), RX350h, UX300h, EVs.

## Toyota leftovers (יוניון מוטורס), all reviewed
The old Hebrew car_book PDFs in the /app API contain "לוח אחזקה מונעת" tables. The pages are rotated and were read as images.
- toyota-auris-2007-2009-1.6: conn 24, pp.210-211 (PDF 229-230)
- toyota-auris-2010-2012-1.6: conn 25, pp.220-221. The MMT oil row is inspect here but replace in the 2007 book.
- toyota-camry-2006-2011-2.4: conn 75, pp.265-267 (PDF 277-279)
- toyota-city-2020-2026-1.5-diesel: conn 930 sheet dated 01/07/2021, 14 columns to 210k. The repo's file-331 parse had only 10 columns.
- toyota-rav4-plug-in-2021-2023-2.5-phev: conn 857 (14.02.2021). The 2024 sheet (conn 1114) has a different layout and was not used.
- Name-only rules to existing schedules: C-HR with 2ZR, LAND CRISER / PRADO with 1KD 2002-09, YARIS CROSS HEV, COROLLA HB HSD.
- UNCOVERED false positives (already covered by engine-code rules): LAND CRUISER 2004-09, HILUX 2011-13, PRIUS 2007-08.
- No source found: COROLLA 2000-06 (3ZZ), COROLLA RUNX, YARIS 2001-05, RAV4 2006-12, HIACE, SIENNA, old PRADO 1KZ. COROLLA SEDAN with M15A is left unmapped (the Israeli sheet is 1ZR).

## Nissan (פריסבי/קרסו), all draft
Blocked routes:
- nissan.co.il has no books.
- service.freesbe.com and freesbe.com return 403.
- The Israeli mirror xn----2hc3awpyb.com is behind Cloudflare (Playwright too).
- carasso.co.il is denied by the egress policy.
Source used: Nissan South Africa official km tables, https://www.nissan-cdn.net/content/dam/Nissan/za/Maintenance/<Model>.pdf (the nissan.co.za host serves New-Qashqai-Maintenance-Schedule.pdf).
- qashqai-2014-2019-1.2-turbo: Qashqai.pdf pp.7-9
- qashqai-2014-2021-1.6-diesel: pp.1-3
- qashqai-2014-2021-1.5-diesel: pp.4-6
- qashqai-2019-2026-1.3-turbo: J12 HR13 sheet, also used for J11 with HR13
- x-trail-2014-2021-1.6-diesel: X-Trail.pdf pp.1-3. The air-filter row is misprinted; the air filter was taken from the Qashqai sheet for the same engine.
- juke-2010-2019-1.6: Juke.pdf pp.1-3
- micra-2011-2019-1.2: Micra.pdf, HR12 rows
- nv200-2012-2019-1.5-diesel: NV200.pdf pp.4-6
- almera-2012-2016-1.5-1.6: sister, SA 1.5 HR15
- sentra-2016-2019-1.8: USA 2019 manual pp.417-422 (km column, 8,000 km grid)
- sentra-2020-2026-2.0: USA 2022 manual pp.489-497
Not done: Qashqai J10 (MR20/HR16), Tiida C11, Note E11, Micra K12, X-Trail petrol and e-Power, Juke F16/Hybrid, Altima, Navara YD25.

## Honda (מאיר), all draft
Blocked routes:
- honda.co.il/guide_books and wp-json are behind Cloudflare (curl and Playwright).
- carsforum.co.il returns 403.
Source used: the "Maintenance Schedule (Except EU)" tables in the international English owner's manuals on manualslib, captured with Playwright (dl/japan-b/mlshot.mjs).
- honda-civic-2006-2011-1.8: manualslib 822871 pp.360-362 (32SMG610). The watermark hides some dots. Also used for the FD sedan.
- honda-civic-2012-2016-1.8: manualslib 2119749 pp.313-314 (32TR0600, "Except European, South African and New Zealand models")
- honda-jazz-2015-2020-1.3: manualslib 1445713 pp.485-486
Found but not written up:
- Jazz GD: 811004 pp.282-283 (watermark hides the fuel-filter column)
- Jazz 2021: 2051002 p.536
- HR-V 2018: 2532246 p.508
- CR-V 2017: 2512935 p.564
- Civic 2016: 2529262 p.512
- HR-V e:HEV: 2986036 pp.510-512
- Jazz GD European ESM on hondafitjazz.com
Not found: Accord CL/CU, CR-V RE/RM, Insight/Jazz Hybrid LDA3. The manualslib copies are US Maintenance Minder manuals.
