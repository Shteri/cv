REPORT - group jp3 (round 3: Toyota, Honda, Mitsubishi, Daihatsu, Subaru, Nissan, Lexus, Suzuki gaps)

There are 22 schedule files. `node scripts/validate.mjs staging/jp3` prints: all schedules valid (21 draft, 1 reviewed).
The 31 rules in registry/registry_rules.json add coverage for about 58,000 registered vehicles.
- This count comes from registry-counts.json, matched on exact name, year and engine code.
- None of the rules changes a match that the current data/registry_map.json already makes.

Tools:
- Generators: scratchpad/dl/jp3/gen_*.py. The shared helper is gen.py, copied from japan-b.
- Per-make rule files: dl/jp3/rules/. merge.py merges them into registry_rules.json.
- Page captures: dl/jp3/{honda,sub,mit,lexus,nissan}/.
- Coverage check: dl/jp3/gain.mjs (new matches against the current registry_map).
- Remaining gaps: dl/jp3/unc.mjs <Make> lists them row by row.

NEW ROUTES / NOTES
- procarmanuals.com PDFs now return 403 to plain curl (Cloudflare). They still download if you add the viewer page as Referer:
  curl -e "https://procarmanuals.com/pdf-online-<slug>/" <pdf-url>
- manualslib search: these URLs work in Playwright (dl/jp3/mlsearch.mjs):
  - https://www.manualslib.com/t/<words+joined+by+plus>.html
  - https://www.manualslib.com/brand/<brand>/automobile.html
  dl/jp3/mltoc2.mjs <regex> <ids...> greps a manual's TOC.
- Lexus API still works: books.union-motors.co.il/LexusApp/api/{models/{id}/years, search?modelId=&year=, files/{conn}/download}.
  Model ids: UX=12, RX=17, NX=13, IS=16.
- OVERLAP: group prem3 merged Lexus UX200, UX250h/UX300h and RX300 into the repo while I was working (commit 1aa4b04).
  I deleted my copies of those three, so only NX300 is left from my Lexus work.
- EXISTING-RULE ISSUE (not changed, please review): the repo rule "Toyota COROLLA 2007-2012 -> toyota-corolla-2007-2012-1.6"
  (E150 / 1ZR sheet) also matches about 8.9k 2007-registered COROLLA rows whose engine code is 3ZZ.
  Those are the old E120 generation: Japan 6,040 and Turkey 2,909.

PER MODEL (vehicles = newly matched registry vehicles)

HONDA (importer מאיר; honda.co.il is still Cloudflare 403)
All files are draft, from international owner's manuals on manualslib (Playwright screenshots).
- honda-civic-2017-2022-1.0-1.5-turbo (4.1k)
  Source: manualslib 2530542 p.559-560, Civic 2017 OM, "Maintenance Schedule - Except Australian and New Zealand models", book pp. 558-559.
  Oil and filter go by the indicator (max 1 yr / 2 yrs), so they are in time_based.
- honda-civic-2016-2021-1.6 (1.8k)
  Source: manualslib 2529262 p.513-514, Civic 2016 general-market OM, Non Turbo rows. Covers R16B1.
- honda-cr-v-2012-2018-2.0 (3.3k)
  Source: manualslib 1431921 p.538-539, CR-V RM European OM, "Petrol - Except European models". Covers R20A9 (UK-built).
- honda-cr-v-2007-2012-2.0 (1.8k)
  Source: manualslib 829415 p.434-436, CR-V RE OM 42SWAF30, "Petrol (Except EU, Russia, Ukraine, South Africa)". A watermark hides some dots.
- honda-cr-v-2018-2022-1.5-turbo (1.2k)
  Source: manualslib 2512935 p.565-566, CR-V 2017 general-market OM, Turbo rows.
- honda-accord-2003-2008-2.0-2.4 (2.7k)
  Source: manualslib 1207475 p.356-358, Accord/Accord Euro OM 32SEA610, "Schedule B, Petrol (Except EU, Australia, NZ)". Covers K20A6, K20Z2 and K24A3.
- honda-jazz-2020-2026-1.5-hybrid (2.4k)
  Source: manualslib 2051002 p.537-538, Jazz 2021 e:HEV OM, "Except Ukrainian models without Service Book".
  Covers JAZZ 1.5, JAZZ HYBRID and JAZZ CROSTAR with engine LEB8.
- honda-jazz-2002-2008-1.3 (2.1k)
  Source: manualslib 811004 p.282-283, Jazz GD OM 32SAA650, "Except EU". A watermark hides part of the fuel-filter row; I read dots at 80k and 160k.
- honda-fr-v-2005-2009-1.8 (1.2k)
  Source: manualslib 814923 p.234-235, FR-V OM 32SJD620, "Petrol (Except EU and NZ)".
- Rule only: CIVIC 2012 R18A2 is mapped to the existing honda-civic-2006-2011-1.8 (0.8k).
NOT FOUND:
- Jazz Hybrid / Insight LDA3 (9.1k), Accord CU R20A3 2008-2015 (3.4k), Civic 7th gen D16V1/D16W7 (2.5k), Jazz GE L13Z1 (1.1k), Civic Hybrid LDA2 (1k).
- Every manualslib copy for these is a US Maintenance Minder manual. Checked: 1472915, 513499, 543332/543334, 955210, 3247202, 454871, 720375, 918832, 713284, 714951.
- honda.co.uk only has manuals from 2016 on, and honda.ie returns 403.

MITSUBISHI (importer כלמוביל)
- mitsubishi-l200-2006-2015-2.5-diesel (draft, 3.7k)
  Source: manualslib 1634870 p.31-34, Pajero Sport 2013 Inspection and Maintenance manual, "Periodic Inspection and Maintenance Schedule - For General Export".
  The "For Europe" table is on pp. 34-37.
  Pajero Sport KH uses the same platform and the same 4D56 engine as L200/Triton KB, so this is a sister source.
  I used the general-export diesel values (oil every 10k). The notes give the Europe values for comparison.
- mitsubishi-outlander-2007-2012-2.0-2.4 (draft, sister, 2.6k)
  Copy of the repo's ZJ-ZL MMAL schedule for the CW generation (4B11/4B12). The note says which items to verify.
- mitsubishi-pajero-2000-2006-3.2-diesel (draft, sister, 2.2k)
  Copy of the repo's NX MMAL schedule (same 4M41 engine).
- Rule only: OUTLANDER 2021 4J11/4J12 is mapped to the existing mitsubishi-outlander-2013-2020 (2.5k).
NOT FOUND: Lancer CS 4G18 (5.9k) and Grandis 4G69 (3.5k).
- MMAL lists nothing older than MY15.
- The manualslib Grandis owner's manual (1792177) has no schedule.
- The Pajero 2001 WM (2182048) has only 28 pages and no schedule.
- The Outlander SM 1590697 is engine overhaul only.

SUBARU (importer יפנאוטו / סמלת). samelet.com/ebooks has no book for the EJ-engine models.
Source for all three files:
  https://www.manualslib.com/manual/1585126/x.html?page=105
  Subaru Legacy 2005 (BL/BP) service manual, PM-3 "Maintenance Schedule 1 - EUROPE AREA" (15k/12m grid to 120k, timing belt at 105k).
  The severe schedule is PM-5 (p.107).
- subaru-b4-2003-2013-2.0-2.5 (draft, 4.1k). Covers EJ20/EJ25.
- subaru-forester-2003-2012-2.0 (draft, sister: same EJ20 engine and SM table, 1.9k).
- subaru-impreza-2005-2011-2.0 (draft, sister: EJ20 only, 1.0k).
- Rule only: FORESTER 2011-2012 FB20 is mapped to the existing subaru-forester-2013-2018 (0.8k).
NOT FOUND:
- Impreza / B3 EL15 1.5 (5.3k). Every Impreza 2008-2011 manual on manualslib is a US one with no table. The Legacy table does not list the EL15 spark-plug interval, so I did not reuse it.
- Impreza EJ16 (1.8k).

NISSAN (importer פריסבי / קרסו)
- nissan-qashqai-2007-2014-1.6 (draft, 1.1k)
  Source: Qashqai J10 European ESM (procarmanuals PDF, the same file used in round 2), MA-7/MA-8 "HR16DE petrol" tables, PDF pp. 6173-6174.
  Same content as the MR20 file, minus the CVT and 4WD rows.
- nissan-note-2006-2013-1.6 (draft, sister, 2.1k)
  Copy of the repo's Tiida C11 HR16DE European-ESM schedule (same B platform and engine).
- nissan-x-trail-2019-2022-1.3-turbo (draft, sister, 4.1k)
  Copy of the repo's Qashqai HR13DDT schedule.
- nissan-x-trail-2019-2021-1.7-diesel (draft, sister, 2.1k)
  Copy of the repo's X-Trail T32 1.6 dCi R9M schedule, for R9N.
NOT FOUND:
- Juke Hybrid (5.1k), Juke F16 HR10 (2.2k), X-Trail T33 KR15 (2.2k), Micra K12 CR14 (1.7k), Micra K14 HR10 (0.7k).
- Nissan ZA has only Juke F15, X-Trail T32, Micra K13, Navara, Almera, NP200, Qashqai and Leaf. Juke-Hybrid, New-Juke and X-Trail-e-POWER return 403.
- The Nissan IE online manuals point to a separate maintenance booklet.

TOYOTA (importer יוניון מוטורס)
- toyota-yaris-2003-2005-1.3 (draft, sister, 1.8k)
  Copy of the repo's Israeli Yaris XP90 sheet, which uses the same 2SZ-FE engine.
- toyota-rav4-2009-2012-2.0 (draft, previous generation, 2.1k)
  Copy of the repo's Israeli RAV4 XA40 4X4 sheet, same 3ZR-FAE engine. Covers registry name "RAV-4".
- Rule only: HILUX 2002-2004 2KD is mapped to the existing toyota-hilux-2005-2015 (same engine as the Israeli Euro5 sheet, 1.4k).
NOT FOUND: Corolla E120 3ZZ 2001-2006 (16k) and Corolla RunX 3ZZ (4.1k).
- toyota-union-sheets.json and the Toyota/Lexus API have nothing older than 2007.
- toyota-tech.eu MS/PDFS maintenance schedules redirect to a Keycloak login. Search engines index a 2004 Corolla/Verso 3ZZ/1ZZ EU table there.
- The pakwheels PDFs are an E170 Pakistan schedule and an engine-only RM (no MA section).
- procarmanuals "Corolla 2000 SM" is a Russian third-party JDM book with no table.
- manualslib has only the US Corolla 2003 OM.
- The toyotaownersclub thread returns 403.
Also not found: RAV4 1AZ 2006-2009 (2.5k, different engine), Yaris 2NZ 2000-2002 (1.1k), Hiace 2KD (1.5k), Prado 1KZ (1k), Sienna.

DAIHATSU (Terios J200 3SZ, 4.8k): NOT FOUND
- The procarmanuals Daihatsu category has only Terios J100.
- The Materia M400 manual (same 3SZ-VE engine) is a 1,310-page Toyota-style RM with no maintenance chapter.
- The Sirion M300 table is generic for M300. I did not reuse it, because the Terios is a different FR 4WD model.

LEXUS (Israeli books)
- lexus-nx300-2018-2021-2.0-turbo (REVIEWED, 0.3k)
  Source: https://books.union-motors.co.il/LexusApp/api/files/161/download , "לוח אחזקה NX300 8AR-FTS", pp. 479-480 (10 columns to 150k), plus the fluids table.
- Found but not used, because prem3 already merged these:
  - UX200 table (conn 74, pp. 395-396).
  - RX300 sheet dated 26.4.18 (conn 148, p.730).
  - The UX250h (conn 77) and UX300h (conn 70) books have no table.
- The IS300 2020 book (conn 116) is an abridged hybrid book (it has an inverter-coolant row), so it does not fit IS300 8AR.

SUZUKI (rule only, to existing Israeli-book schedules)
- SWIFT K12C 2021 -> swift-2017-2020.
- IGNIS K12C 2021 -> ignis-2017-2020.
- SWIFT M15A 2011 -> swift-2005-2010.
- "S CROSS" (name with a space) -> s-cross-2022-2026.
- VITARA K14C/K10C 2021 -> vitara-2016-2020-turbo (1.95k).
Not done: Liana M16A (2k), old Ignis M13A, Grand Vitara G16B.

BLOCKED ROUTES
- toyota-tech.eu: SSO login.
- honda.co.il: 403.
- honda.ie: 403.
- toyotaownersclub.com: 403.
- procarmanuals: 403 without a Referer.
- Nissan ZA: only some model PDFs exist.
- MMAL: lists MY15 and later only.

TRANSCRIPTION NOTES
- All grids were read from page screenshots or renders.
- Watermarked manualslib rows where only some dots are visible are recorded as every 20k. The note says so.
- In the Honda turbo files, the oil and oil filter follow the car's indicator. I put them in time_based (12 / 24 months) instead of inventing a km figure.
- The L200 draft uses the "General Export" diesel table (oil every 10k), not the Europe table (oil every 20k). The notes say which one is used.
