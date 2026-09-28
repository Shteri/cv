# hk2 group report (Hyundai/Kia round 2)
Validation: `node /home/user/cv/scripts/validate.mjs staging/hk2` -> all schedules valid (4 draft, 3 reviewed).
Registry rules: registry/registry_rules.json (7 rules, all with engine_codes).
Builder scripts: scratchpad/dl/hk2/*.py (build.py = grid-to-JSON helper). Page images: scratchpad/dl/hk2/*.png

## Done
- kia-niro-2024-2026-1.6-hybrid (SG2 HEV, G4LL/G4LM, ~11k vehicles) - reviewed. Kia Israel Hebrew book NIRO_PHEV_General_Heb_01 (cdnmedia.kia-israel.co.il/www/cars-book/...), which is a shared HEV+PHEV book. Used the "except Europe" table on PDF p456-458 (15k columns, non-Middle-East rows; Middle East variants in notes: oil 10k, air filter every service, HSG belt inspect 10k/replace 100k). HEV inverter coolant = first 180k/120mo then 30k/24mo.
- kia-niro-2019-2022-1.6-plug-in-hybrid (DE PHEV, G4LE, ~9.3k) - reviewed. Niro-2019.pdf (Israeli book covers HEV+PHEV, one petrol table) PDF p549-550. Grid identical to the existing kia-niro-2016-2022-1.6-hybrid (copied from it after checking against the text layer).
- kia-carnival-2015-2020-3.3 (YP, G6DH, ~3.4k) - reviewed. Local kia-Carnival-YP-2016-2020.pdf, PDF p493-495 (read visually), 12,000 km grid to 180,000. URL https://cdnmedia.kia-israel.co.il/www/cars-book/Carnival-YP-2016-2020.pdf answered 206.
- hyundai-accent-2019-2023-1.4-1.6 (G4LC/G4FG, ~10k) - draft. manualslib 1958374 (Accent HCi 2019 export book) p358-361, 15k grid; Middle East variants in notes.
- hyundai-accent-2006-2011-1.4-1.6 (MC, G4EE/G4ED, ~9.3k) - draft. carmanualsonline "hyundai-accent-2009-owner-s-manual-rhd-uk-australia" page images 175-176 (/img/35/14392/w960_14392-N.png, Referer needed) = book 5-4/5-5.
- hyundai-getz-2003-2010-1.3-1.6 (G4EA/G4EE/G4ED, ~10.9k) - draft. manualslib 752940 p179 + p181 (general international table with EC-only rows).
- kia-rio-2011-2017-1.25-1.4 (UB, G4FA/G4LA, ~12k) - draft. manualslib 740114 p382-391 "Normal maintenance schedule - except Europe" (cumulative lists per 15k).

## Findings for the owner
- Existing data/schedules/kia-niro-2023-2024-1.6-plug-in-hybrid.json was built from PDF p460, which is the Australia/New Zealand table (heading on p459), not "except Europe". It also gives the PHEV inverter coolant as first 180k then 30k; the book says PHEV inverter coolant every 60,000 km or 36 months (p457/p460). Worth a fix.

## Not done / blocked
- ix35 (G4KD/G4NA, 12k): manualslib 623630 and 3293715 (ix35 2015) are European books; the schedule is only in the Service Passport (p340/p471 say so). No non-EU ix35 book found in the time.
- i10 PA (G4HG/G4LA, 8.6k): manualslib 623636 is the UK book (15k then every 20k km, 1.1L timing belt) - not used; a non-UK book is still needed.
- Kia Rio JB 2008-2011 (G4EE, ~4.3k), Kia Forte TD 2009-2013, Sportage 2009/diesel, Ceed ED/CD and 2019-24, Tucson JM, Santa Fe CM/DM: not reached. Santa Fe DM local scanned book (hy-santafe-2013-2018.pdf) has the schedule on PDF p408-419 as cumulative lists (15k/30k/.../240k km), not a grid - readable at dpi 150, not transcribed yet.
- Accent LC (manualslib 724162 p121) is a 10,000 km Indian-type table - not used.
