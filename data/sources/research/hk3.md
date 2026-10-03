# hk3 group report (Hyundai/Kia round 3)

Validation: node /home/user/cv/scripts/validate.mjs staging/hk3 -> all schedules valid (29 files: 9 reviewed, 20 draft).
Registry rules: registry/registry_rules.json (35 rules, almost all with engine_codes; 6 only point existing schedules at more years/engines).
Coverage check (exact year/fuel/engine rows; dl/hk3/unc.mjs = matchSchedule logic + these rules): about +78,400 vehicles newly matched.
Builder scripts: scratchpad/dl/hk3/s1.py..s16.py (+ build.py). Page images: dl/hk3/*.png. manualpdf text cache: dl/hk3/mpt/.

## New sources found this round
- Kia Israel CDN has more old Hebrew books than its web page lists: cdnmedia.kia-israel.co.il/www/cars-book/Soul-AM-2012-2013.pdf,
  Soul-PS-2014.pdf, Carens-RP-2013.pdf (found by trying ~6,000 guessed names; no Ceed/XCeed/Forte/Sorento-XM/Optima/Venga/Rio-JB under the patterns tried).
  Sorento-MQ4-HEV-PHEV-2021.pdf is listed but had not been used yet. Soul PS and Carens PDFs have an encoded font -> read from page images.
- manualpdf.co.il (Hebrew version of manua.ls) serves many older international books as HTML pages. Playwright screenshot of
  ".viewer-page .pf" from https://www.manualpdf.co.il/<make>/<model-year>/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=N (dl/hk3/mpshot.mjs);
  page text is in the HTML (dl/hk3/mpscan.py). Some sparse rows render with shifted marks; I checked those against another edition (noted in the file).
- Local Colmobil Hebrew Kona 2024 book (pdf/hy-kona-2024.pdf, scanned) has a simple 15k table on PDF p510-512.

## Files (vehicles newly matched; source; pages; status)
- hyundai-ix35-2010-2015-2.0 (G4KD/G4NA) 10,878 - manualpdf hyundai/ix35-2014 (EL FL English book) p894-903 "except Europe" cumulative 15k lists - draft
- hyundai-i10-2008-2013-1.1-1.2 (G4HG/G4LA) 8,631 - manualpdf hyundai/i10-2010 p278-282 "except Europe" grid; valve-clearance (1.1) row renders badly -> every 30k as in the EU table of the same book - draft
- kia-forte-2009-2013-1.6 (TD, G4FC) 7,955 - SISTER-ENGINE source: Kia Soul AM 2009 international book (manualpdf kia/soul-2009 p269-272, except-Europe columns), same Gamma 1.6 MPI G4FC/era. The only Forte TD books found: 8,000 km/4-month market book (forte-2010 p258) and an Arabic Gulf book - draft
- kia-sportage-2019-2022-1.6-diesel (QL, D4FE) 7,321 - Kia Israel Hebrew book Sportage-QLe-2019-2021 (local pdf/kia-sportage-2019.pdf) PDF p547-554 diesel "Smartstream D1.6" rows (the existing rule was petrol-only) - reviewed
- kia-rio-2007-2012-1.4-1.6 (JB, G4EE) 5,093 - manualpdf kia/rio-2010 p264-267 (except AU/NZ, except-Europe columns); checked against kia/rio-2009 p251-254 (clean render), vapor/vacuum hose rows from 2009 - draft
- hyundai-tucson-2005-2010-2.0-2.7 (JM, G6BA; incl. TOCSON + LPG) 4,388 - manualpdf hyundai/tucson-2007 (GAT general book) p251-254, except-ME / except-EC - draft
- hyundai-tucson-2005-2009-2.0-diesel (D4EA) 509 - same book p252-254 - draft
- kia-ceed-xceed-2019-2021-1.4-turbo (CD, G4LD) 3,249 - manualslib 1799825 (Kia XCeed 2020, EU) p566-569 - draft
- kia-ceed-2012-2018-1.6-diesel (JD, D4FB) 2,701 - manualslib 2438705 (Ceed JD PE 2017) p530-534 EU table; except-Europe (p536-540) diesel oil 10k noted - draft
- kia-ceed-2019-2023-1.6-diesel (CD, D4FE) 685 - manualslib 1799825 p566-570 EU diesel rows - draft
- kia-ceed-2007-2011-1.4-1.6 (ED, G4FC) 2,055 - manualpdf kia/ceed-2008 (EU book) p286-289 - draft
- hyundai-h1-2008-2021-2.5-diesel (TQ, D4CB) 2,112 - manualslib 739089 (H-1) p268-271 "for Europe A2.5 diesel" 20k grid; except-Europe oil 10k noted - draft
- hyundai-veloster-2011-2017-1.6 (G4FD) 2,068 - manualpdf hyundai/veloster-2012 p303-313 except-Europe lists - draft
- hyundai-santa-fe-2012-2018-2.4 (DM, G4KJ) 2,006 - COLMOBIL HEBREW BOOK local pdf/hy-santafe-2013-2018.pdf PDF p409-420 (30k cumulative lists; 15k oil grid per severe/oil notes) - reviewed
- hyundai-santa-fe-2013-2018-2.2-diesel (DM, D4HB) 1,460 - same - reviewed
- hyundai-santa-fe-2010-2012-2.4 (CM FL, G4KE) 1,096 - manualslib 3393691 (Santa Fe CM) p306-311 except-Europe - draft
- hyundai-santa-fe-2010-2012-2.2-diesel (CM, D4HB) 910 - same p312-317, "For Europe" diesel columns (except-Europe = 10k oil, noted) - draft
- kia-sorento-2012-2014-2.4 (XM, G4KJ) 1,113 - SISTER source: Colmobil Santa Fe DM Hebrew book, same engine/years (only US-mile Sorento XM books found) - draft
- kia-sorento-2010-2014-2.2-diesel (XM, D4HB) 546 - SISTER source, same DM book diesel rows - draft
- kia-sorento-2021-2026-1.6-hybrid (MQ4 HEV/PHEV, G4FT) 932 - Kia Israel Sorento-MQ4-HEV-PHEV-2021.pdf PDF p611-613 - reviewed
- kia-sportage-2005-2010-2.0-2.7 (KM, G6BA) 957 - SISTER source: Tucson JM GAT book (same platform/engines) - draft
- kia-carens-2013-2018-2.0 (RP, G4NC) 952 - Kia Israel Carens-RP-2013.pdf PDF p563-572 (30k lists) - reviewed
- kia-carens-2013-2019-1.7-diesel (D4FD) 724 - same - reviewed
- kia-soul-2014-2018-1.6 (PS, G4FD/G4FG) 892 - Kia Israel Soul-PS-2014.pdf PDF p517-526 - reviewed
- kia-soul-2012-2013-1.6-gdi (AM FL, G4FD) 693 - Kia Israel Soul-AM-2012-2013.pdf PDF p328-336 (text layer) - reviewed
- kia-soul-2009-2011-1.6 (AM, G4FC) 452 - manualpdf kia/soul-2009 p269-272 - draft
- hyundai-staria-2022-2024-2.2-diesel (D4HB) 948 - manualslib 2356247 (Staria US4 2021) p678-682 EU tables - draft
- hyundai-i30-2017-2020-1.4-turbo (PD, G4LD) 909 - manualslib 1363798 (i30 2018) p402-404 EU table (oil 10k) - draft
- hyundai-kona-2024-2026-1.6t-1.0t (SX2, G4FP/G3LE) 755 - Colmobil Hebrew Kona 2024 book (local pdf/hy-kona-2024.pdf, scanned) PDF p510-512 - reviewed

Rules that only point existing schedules at more cars (no new file):
- FORTE 2013 G4FG -> kia-forte-2014-2018-1.6 (2,062): the YD launched in 2013 with G4FG; TD cars use G4FC.
- I35 2016 G4FG -> hyundai-elantra-2011-2015-1.6 (1,673; MD still sold as I35 in 2016).
- ELANTRA 2021 G4FG -> hyundai-elantra-2019-2020-1.6 (708; AD engine, CN7 uses G4FM).
- TUCSON 2021 G4NA -> hyundai-tucson-2015-2020-1.6-2.0 (373; TL Nu 2.0 stock).
- I30 2017 G4FD -> hyundai-i30-2012-2016-1.6 (273).
- SORENTO 2021-2026 D4HE -> kia-sorento-2021-2026-2.5-2.2 (307; Smartstream D2.2 = D4HE, the existing rule listed only D4HB).

## Method notes
- Books with 30k columns (Israeli DM/Carens/Sportage, EU tables): I built a 15k grid with oil and filter at every 15k (from the book's
  severe/importer note) and the table items at the even services, the same approach as the existing kia-sportage-2019-2021.
- "Except Europe" tables: I used the non-Middle-East column. The book's "Middle East" means Gulf/Iran/Yemen; their 10k variant is in interval.note.
- No invented intervals. Where a mark position was ambiguous, the file note says how I resolved it (Rio vapor/vacuum hose, i10 valve clearance,
  Soul AM 2009 vapor hose/fuel lines).

## Not done / blocked
- Santa Fe CM 2.7 V6 G6EA 2007-2009 (1,357) + D4EB (353): manualpdf santa-fe-2008 = US book; santa-fe-2010/2011 "-EU" = US-style 7,500-mile tables;
  the manualslib CM book covers only 2.4/3.5/R2.2.
- Ceed/XCeed 1.5 T-GDI G4LK 2021-2025 (~1,600): no MY2022+ full book (manualpdf ceed-2021/22/23 are 12-page quick guides; manualslib 4592112 Finnish quick guide).
- Staria Hybrid G4FT 2025-26 (1,265): no Colmobil Staria book listed; no 2025 manual found.
- ix35 diesel D4HA (821): same 2014 book but diesel oil every 10,000 km inside 15k lists -> not written. ix35 2.4 G4KE (381): not in the 2014 book.
- Accent LC G4EB 2000-2006 (1,059): only the Indian 10,000 km book (hk2 finding). Genesis GV70/GV60/GV80, Terracan J3, Optima diesel/HEV,
  Carnival J3/G6EA, Elantra XD/Matrix G4ED, Forte YD diesel D4FB, Sonata DN8 1.6T (the Colmobil Sonata 2024 book is hybrid-only), i40, K2500: not done.
- Sorento XM: only US-mile books (manualpdf sorento-2012/2013/2014, manualslib 630609/3264055) -> used Santa Fe DM sister source (draft).
- Forte TD: forte-2010 (8,000 km/4-month table), forte-2011 (Arabic), forte-2012/2013 (brochure/audio); manualslib 2017768/1996633 are later generations.
- Dead routes: Kia CDN name guessing for Ceed/XCeed/Forte/Optima/Sorento/Venga/Rio-JB (~6,000 HEAD requests, all 404);
  manualslib /brand/kia/car.html 404 (use /brand/kia/automobile.html); carmanualsonline /kia/* redirects to home.
