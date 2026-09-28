REPORT - group japan2 (round 2: Toyota, Daihatsu, Suzuki, Nissan, Honda, Mitsubishi, Subaru, Isuzu gaps)

10 schedule files. validate.mjs staging/japan2 prints: all schedules valid (8 draft, 2 reviewed).
Registry rules: registry/registry_rules.json (10 rules). They match about 56k registered vehicles (exact name, year and engine code, counted from registry-counts.json).
Generators: scratchpad/dl/japan2/gen_*.py. Downloads and page renders: scratchpad/dl/japan2/.

NEW ROUTE: procarmanuals.com embedded PDFs (full factory service manuals, many include the maintenance chapter)
- The page https://procarmanuals.com/pdf-online-<slug>/ has an iframe attribute data-pdf-lazy-original-src-enc. It is base64 of the URL XOR-ed with the key "pdf-lazy-loader-secure-key-2024".
- The decoded URL holds a pdfemb-data= base64 JSON. Its url field points to https://procarmanuals.com/wp-content/uploads/pdfs/manuals/<file>.pdf, which downloads with plain curl.
- Decoder: dl/japan2/pcm.py <page-url>...
- Many of the site's books are US or Haynes books, so check the market before using one.

PER MODEL
1. daihatsu-sirion-2005-2011-1.3 - draft - 15.5k vehicles (SIRION + .SIRION, K3, 2005-2011)
   Source: Daihatsu Service Manual No.9890, M300 series (from Nov 2004), chapter A2 pp. A2-2..A2-4 (PDF pp. 3-5).
   https://procarmanuals.com/wp-content/uploads/pdfs/manuals/DAIHATSU-SIRION-Model-M300-Series-Service-Manual-No.9890/daihatsu-sirion-model-m300-series-service-manual-no9890-maintenance.pdf
   15k/12m grid to 90k. Importer "טלקאר" stopped importing in 2012; no Israeli book was found.
2. nissan-qashqai-2007-2014-2.0 - draft - 9.1k (QASHQAI, QASHQAI PLUS 2, QASHQAI 2; engine MR20)
   Source: Nissan J10 ESM (Europe), MA-8..MA-10 (PDF 6175-6177, MR20DE tables) and MA-13 severe table (PDF 6180).
   https://procarmanuals.com/wp-content/uploads/pdfs/manuals/nissan-qashqai-2007-2010-factory-service-manual.pdf
   The normal EU plan is 30,000 km / 24 months. The severe-condition rules (oil, cabin filter and brake fluid every 15k) are in the interval note and notes.
3. suzuki-swift-2005-2010-1.5 - draft - 8.9k (SWIFT M15A, Japan + Hungary)
   Source: Suzuki Swift RS service manual 2005 (S4RS), 0B-1..0B-2 (PDF 32-33).
   https://procarmanuals.com/wp-content/uploads/pdfs/manuals/suzuki-swift-2005-rs-series-service-manual.pdf
   15k/12m grid to 90k.
4. honda-hr-v-2016-2021-1.5 - draft - 6.1k (L15B4, L15BY)
   Source: international HR-V 2018 owner's manual, "Except Australian, NZ and South African models", book pp. 507-508 (Playwright capture).
   https://www.manualslib.com/manual/2532246/x.html?page=508
   honda.co.il still returns 403 (Cloudflare).
5. nissan-tiida-2007-2011-1.6 - draft - 5.3k (TIIDA HR16)
   Source: Nissan Tiida C11 ESM 2008 (Europe), MA-8..MA-10 HR ENGINE tables (PDF 5833-5835) and severe table (PDF 5842).
   https://procarmanuals.com/wp-content/uploads/pdfs/manuals/nissan-tiida-c11-2008-service-repair-manual.pdf
6. isuzu-d-max-2007-2011-3.0-diesel - draft - 3.2k (PICK-UP / PICK - UP / PICK -UP / D-MAX, engine 4JJ1)
   Source: Isuzu KB P190 2007 (TF series) workshop manual, 0B-2..0B-4 "Maintenance Schedule (For GENERAL EXPORT)" (PDF 20-22).
   https://procarmanuals.com/wp-content/uploads/pdfs/manuals/isuzu-kb-p190-2007-iworkshop-repair-manual.pdf
   The book uses a 5,000 km grid to 100k. I used the 10k columns and noted the extra 5k checks.
7. isuzu-d-max-2004-2007-3.0-diesel - draft - 2.3k (engine 4JH1)
   Same pages, 4JH1-TC rows: oil filter every 10k, fuel filter every 15k (long_interval), valve adjust every 20k.
8. subaru-forester-2025-2026-2.5 - REVIEWED - 2.9k (FORESTER FB25/FB 25, 2025-2026)
   Source: Samelet Hebrew book https://samelet.com/ebooks/Subaru_Forester_25MY_carbook_082024.pdf, 11-1 "תכנית תחזוקה" pp. 431-432 (PDF 435-436).
   The plan is A/B/C/D every 10,000 km / 12 months to 100k, written as text lists. I converted it to a grid.
9. subaru-outback-2015-2020-2.5 - REVIEWED - 1.2k (OUTBACK FB 25/FB25, 2014-2020)
   Source: Samelet Hebrew book https://samelet.com/ebooks/Car_Book_outback.pdf (Legacy/Outback 2014 OM), 11-3..11-6 (PDF 453-456).
   15k/12m grid to 120k. The 3.6 engine is not included.
10. mitsubishi-outlander-phev-2017-2021-2.0-2.4-phev - draft - 1.8k (OUTLANDER PHEV 4B11/4B12)
   Source: Mitsubishi Motors Australia schedules PHEV MY18 (ZK 2.0), MY19 and 20MY.
   https://www.mitsubishi-motors.com.au/content/dam/mmal/pdfs/maintenance-schedules/OUTLANDER-PHEV-MY19_Maintenance%20Schedule.pdf
   The MY19 layout drops the "severe usage" label on the transaxle-oil rows. MY18 shows those 30k replacements are severe-only, so they are in notes, not in services.

NOT COVERED / BLOCKED
- Toyota Corolla 2000-2006 3ZZ (17k) and Corolla RunX (4.1k): not covered.
  - The books.union-motors.co.il API lists Corolla Sedan only from 2007. The 2007-2009 car_book (conn 101) and the "Corolla 2006-2012" sheet are both E150/1ZR.
  - procarmanuals has only a Haynes US 2003-2008 book and a Russian E150 book.
  - tcorolla.net has an E120 repair manual only, with no interval table.
  - The manualslib Corolla 2004 manuals (1121605, 621529) are US ones.
- Daihatsu Terios J200 3SZ (5.4k): no source found.
  - The daihatsu-club.net J2 workshop manual needs a login.
  - procarmanuals has only Terios J100.
- Mitsubishi Lancer CS 4G18 (5.6k): the procarmanuals "Lancer 2005 workshop manual" has no periodic-maintenance pages (group 00 is a stub). MMAL lists no older models.
- Mitsubishi Outlander CW 2008-2012: not done. Leads not checked: the procarmanuals Outlander 2011 service manual (9 parts; part1 has no schedule text) and the "Outlander 2006 pre-delivery inspection and periodic maintenance" page.
- Honda: not done:
  - Civic 2004-2006 D16V1.
  - Accord CL/CU.
  - CR-V RE/RM.
  - Jazz Hybrid and Insight LDA3.
  procarmanuals has only US/old Honda shop manuals.
- Nissan X-Trail: not done:
  - HR13 petrol 2019-2022. The repo's Qashqai HR13 schedule could serve as a sister-engine rule; none was written.
  - Diesel M9R/R9N.
  - KR15.
  nissan-cdn ZA has only the current files and Navara/NP300.
- Suzuki Swift: the manualslib 1594932 (2018), 804802 (old G13) and 3795340 (RS diesel) manuals are the wrong books. suzukimanuals.com.au has only current models.
- Subaru Forester SH EJ20, Impreza B3, B4 EJ20: not attempted this round.
- Blocked routes:
  - daihatsu-club.net needs a login.
  - scribd does not render.
  - manualslib fails with curl (challenge) but works in Playwright.

NOTES
- All grids were read from page images; text layers were used to cross-check where they exist.
- Isuzu front hub grease every 30k is mapped to suspension replace (long_interval), because there is no hub-bearing item key.
