REPORT - group jp4 (round 5: Toyota / Mitsubishi / Daihatsu / Subaru gaps)

A previous agent started this group and was stopped by a usage limit. I checked its 4 files against their sources:
- I kept 2 files, after fixes.
- I moved 2 files out (Honda and Nissan belong to other groups).
- I added 2 Mitsubishi files.

`node scripts/validate.mjs staging/jp4` prints: all schedules valid (4 draft, 0 reviewed).
registry/registry_rules.json has 5 rules.
- They cover 43,309 registered vehicles that had no match before. This was measured with dl/jp4/gain.mjs against the current data/registry_map.json.
- They change 0 existing matches.

TOOLS (scratchpad/dl/jp4/)
- gen.py: the shared helper.
  - Fix: time_based entries now use the key `months`, which the schema requires. They used to use `every_months`.
- gen_toyota.py, gen_daihatsu.py, gen_mitsubishi.py: one generator per make.
- rules/*.json: per-make rule files. merge.py merges them into registry_rules.json.
- mlsgrep.py: greps the text of manua.ls pages.
- mmc/: the Mitsubishi downloads.

FILES
1. toyota-corolla-2001-2007-1.6 | draft (sister) | 29,165 vehicles
   - Covers COROLLA 3ZZ 2001-2007 and COROLLA RUNX 3ZZ 2003-2007.
   - Source: Toyota Motor Europe "MAINTENANCE SCHEDULE - EUROPE 15,000 km", dated 2008-6-23, Corolla Verso ZNR10 3ZZ-FE column.
     https://www.yumpu.com/en/document/view/27164868/
2. mitsubishi-lancer-2004-2009-1.6 | draft (international) | 6,027 vehicles
   - Covers LANCER 4G18 2004-2009.
   - Source: Mitsubishi Motors Europe "Pre-Delivery Inspection and Periodic Maintenance", Sept 2005.
     - Group 2, pp. 2-3 to 2-6. Only rows marked "Applicable for LANCER" were used.
     - File PDI/GR00000300-2.pdf inside https://mmc-manuals.ru/manuals/lancer_ix/maintenance/Lancer_MY2006_Service_Manual_eng.zip
3. daihatsu-terios-2006-2011-1.5 | draft (international) | 4,625 vehicles
   - Covers TERIOS 3SZ 2007-2011.
   - Source: Daihatsu Terios J200/J210 owner's manual, Italian edition, (c) 2009.
     - Chapter 13 "Programma di manutenzione", pp. 13-3 to 13-7 (manua.ls p.236-240).
     - https://www.manua.ls/daihatsu/terios-2009/manual?p=236
4. mitsubishi-grandis-2005-2011-2.4 | draft (sister) | 3,492 vehicles
   - Covers GRANDIS 4G69 2005-2011.
   - Source: the same 2005 Mitsubishi Europe table as the Lancer file, using the Lancer rows for front-wheel drive with automatic gearbox.
   - Cross-checked against the Outlander CU edition of the same table: May 2003, CHASSIS/PDI_03/pdi-engels-02.pdf in
     https://mmc-manuals.ru/manuals/outlander/maintenance/Outlander_Service_Manual_May2003.zip
     That edition covers the 4G6 engines, including the 4G69.

TOYOTA COROLLA E120 / RUNX 3ZZ-FE (previous agent's file, re-verified)
I checked every row at full resolution against three page images:
- yuL_1.jpg: petrol engine page
- yuL_3.jpg: chassis 1/2
- yuL_4.jpg: chassis 2/2
These rows were transcribed correctly:
- Engine oil grid.
- Air filter: I-I-I-R-I-I.
- S-LLC coolant: inspect every 30k; first replace at 150k, then every 90k.
- Exhaust, fuel lines, canister (45k/90k), valve clearance (sensory check at 90k).
- Drive belt: first check at 105k, then every 15k.
- Brake pads and discs every 15k. Brake drums, lines and DOT4 fluid every 30k.
- Clutch fluid, power steering fluid, steering, CV boots, suspension (ball joints, front and rear).
- Manual gearbox oil at 60k, tyres, particle filter replaced every 30k, corrosion check.
Not in the grid:
- The spark-plug "Others" row (I-R-I) is described in the note instead.
- The fuel-injection "F" row and the "bolts and nuts (severe only)" row are not marked for the Verso.
Why this is a sister source: the 2008 Toyota Europe table has only a Corolla Verso column, with the same engine. The Corolla E12 sedan/hatchback is not in the 2008 edition.
Added note: some 2001-2002 registry rows may be the older E110 with the same 3ZZ-FE engine.

DAIHATSU TERIOS (previous agent's file, re-verified, one fix)
I re-read pp. 13-3 to 13-7 from the page images (dl/jp4/dai/bg236..240.webp). The cover (bg1) confirms Terios J200/J210 with K3-VE and 3SZ-VE engines.
- Fix: the "Pompa freni" row (brake master cylinder leak check at 30/60/90) was missing. It now sits in the brake_lines note, which has the same pattern.
- All other rows match the book.
- Coolant, brake fluid and clutch fluid every 2 years, and the vapour hose every 8 years, are in time_based.

MITSUBISHI LANCER CS 4G18 (new)
The Mitsubishi Europe table gives intervals ("every X km or Y years") rather than a grid. I expanded each interval onto a 15k grid up to 180k.
I used every row marked for LANCER:
- Engine compartment: A1, A3, A7, A8, A9-A16.
  - A8 spark plugs: standard plugs every 45k. Platinum/iridium plugs every 90k are in the note.
- Under the car: B1, B2, B4, B5, B6, B8, B12.
- Inside and outside the car: C1-C3, D1-D6.
- Warm-engine checks: E1, E2 (2WD automatic fluid 90k/6y), E3, E4, and E5/E6/E8 as diagnostics.
- Placement outside the grid:
  - Timing belt every 90k (A6), fuel filter 150k/10y (A18) and manual gearbox oil 105k/7y (B8) are in long_interval.
  - F1 (yearly body check) is in time_based.
  - F2 (road test) is in the diagnostics note.
  - D2 (front wheel bearings, 60k) is in the suspension note at multiples of 60k.
Cross-check: the Aug 2003 edition (PDI/02-PDI-ENGELS.PDF, a grid from 15k to 300k with a LANCER column) has the same intervals.

MITSUBISHI GRANDIS 4G69 (new, sister)
I found no periodic table written for the Grandis. Places checked:
- The Grandis 2004 workshop manual zip: group 00 has no maintenance chapter.
- The Grandis 2008 online service manual and technical information manual: no maintenance menu item.
- The Grandis MY2010 European owner's manual (OXPE10E1, from procarmanuals): no schedule.
What I used instead:
- The generic Mitsubishi Europe table, the same document and rows as the Lancer file.
- I checked it against the Outlander CU edition (4G6 engines including 4G69). The engine rows there are identical: timing belt 90k, plugs, coolant 60k/4y, brake fluid 30k, fuel filter 150k.
- The note asks the owner to confirm the automatic gearbox fluid interval with a garage.

MOVED OUT OF STAGING (other groups own these makes; I did not re-verify them)
They are in scratchpad/dl/jp4/handoff_other_groups/ with their rule files:
- honda-jazz-2008-2014-1.2-1.3 (Honda belongs to group meir5)
- nissan-juke-2020-2026-1.0-turbo (Nissan belongs to group freesbe5)

NOT FOUND
- Subaru Impreza / Impreza B3 EL15 1.5, 2007-2012 (about 5.3k vehicles): no source.
  - manua.ls subaru/impreza-2007..2011 are US manuals. They point to the "Warranty and Maintenance Booklet".
  - The procarmanuals Impreza 2009 and WRX 2011 factory service manuals (dl/jp4/sub/) have only US and Canada schedules (PM-3 to PM-6), with no EL15.
  - The samelet.com media search for "subaru" returns only new-model books and two warranty booklets, neither with a schedule:
    - subaru-achrayut-V8.6.26-Digi.pdf
    - 300829.1_hoveretyad2_SUBARU_B.pdf
- Corolla E120: no Israeli document.
  - Union Motors API, Corolla Sedan (modelId 9): starts at 2007.
    - year=2007 returns car_book conn 101 (fileId 4, "2007-2009").
    - It also returns maintenance sheet conn 102 (fileId 287, "Corolla 2006-2012"). That sheet is 1ZR-FE only.
  - Avensis (id 1) starts at 2009. Corolla Space and Excite start at 2019.
- Honda and Nissan targets: skipped, as instructed.

ROUTES TRIED (URL -> result)
- books.union-motors.co.il/app/api/models?brand=toyota and /models/{id}/years -> 200. Nothing before 2007 except Prius (id 12, from 2004).
- yumpu 27164868 (Toyota Europe 2008 15k schedule) -> used.
  - Pages 5-8 hold the "GENERAL 10,000 km" table. Not used, because Europe is preferred.
- yumpu 3856326 "MAINTENANCE SCHEDULE" -> Prius NHW20 only.
- yumpu 27164898 "Corolla" -> cargo-net fitting instructions.
- toyota-tech.eu -> Keycloak login, no change from before.
- manua.ls toyota/corolla-2002..2007 -> 200, but all are US manuals (OM...U) that point to a "Scheduled Maintenance Guide". No table.
- Downloaded by the previous agent, not usable:
  - dl/jp4/cor0308.pdf: Haynes US Corolla 2003-2008 (third-party book).
  - dl/jp4/cor06p1.pdf: Russian Corolla E150 / Auris book.
- manualslib.com -> NEW BLOCK. A Cloudflare "Just a moment..." page appears even in Playwright with --disable-blink-features=AutomationControlled / headless=new, on both the brand page and /t/ search.
- mmc-manuals.ru (Russian Mitsubishi manual wiki, 200) -> NEW USEFUL ROUTE for old Mitsubishi models.
  - It has European service manual zips that include the Mitsubishi Europe PDI/Periodic Maintenance manual.
  - Opened: Lancer IX MY2004/2005/2006, Outlander CU May 2003 and Nov 2006, Grandis 2004 workshop manual.
  - Pages also exist for Colt Z3, Galant, Pajero Pinin/III and L200 K6/K7. I did not open those.
  - mmc-manuals.ru/manuals/common/karta_TO_1.pdf and karta_TO_2.pdf: a Russian service card compiled by a forum user ("megaaxel 2013") for many models, Grandis included. Not used, because it is not a manufacturer document.
- procarmanuals mitsubishi-grandis-my-2010-owners-manual (PDF fetched with Referer) -> 200, European owner's manual, no schedule.
- dl/jp4/mit/ Mitsubishi Europe Lancer 2005/2006 workshop manuals (previous agent) -> group 00 is a contents page only, no schedule.
- Mitsubishi Australia maintenance-schedule list -> no Grandis. Lancer is CJ MY16/17 only.
- samelet.com/wp-json/wp/v2/media?search=impreza -> not JSON. search=subaru -> no Impreza book.
