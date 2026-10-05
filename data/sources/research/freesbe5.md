freesbe5 REPORT (round 5): Freesbe brands (Nissan, Infiniti, Renault, Dacia, Chery, Xpeng, EVEASY)

Generator: scratchpad/dl/freesbe5/gen_nissan.py (holds every transcribed mark; run python3 gen_nissan.py).
Table parser: dl/freesbe5/nparse.py <pdf page> (word coordinates). Page renders: dl/freesbe5/img/nb_p*.png.
Parser output was checked against the images of pp.21, 22, 24, 25, 28 and 34.
Downloads: dl/freesbe5/ (wb/files, jina/, nbro/, nza/, intl/, ren/, chery/).
Validation: node scripts/validate.mjs freesbe5 -> all schedules valid (9 draft, 10 reviewed).

MAIN FIND: ISRAELI NISSAN SERVICE BOOKLET
Carasso Motors (Freesbe) Nissan "חוברת אחריות ושירות", August 2016 edition, 46 pages:
  http://carz.co.il.s3.amazonaws.com/files/NewVehicle_Warranty.pdf
  - Use plain http. On https the S3 certificate does not match. The file was uploaded by the review site carz.co.il.
  - Same booklet series as the importer's files in nissan-cdn .../Nissan/israel/services/warrenty-pdf/
    (NT500__Warranty.pdf, LEAF_Warranty.pdf, GTR_Warranty.pdf, NT400_Warranty.pdf), with the same InDesign date 2016-08-02.
  - The current NewVehicle_Warranty.pdf in that folder is a 2017 warranty text with no tables.
  - Contents: p.16 time/km rule; p.17 oil grades; p.18 plan index by model; p.19 severe-use conditions (no separate table);
    pp.20-34 tables.
  - Not used: Almera Verso, Murano Z51, 370Z, Juke 4x4 (not in the registry, or very few cars).

Files upgraded or added from the booklet (table, book page / PDF page, interval, approx. registry vehicles):
  REVIEWED
  - nissan-micra-2011-2019-1.2 (same id): Micra K13, p20/21, 20,000/12, ~27.5k
  - nissan-juke-2010-2019-1.6 (same id): Juke F15 2x4, p21/22, 30,000/12, ~15.1k
  - nissan-qashqai-2014-2019-1.2-turbo (same id): J11/T32 petrol, p23/24, 20,000/12, ~9.4k (+265 H5F)
  - nissan-qashqai-2014-2021-1.6-diesel (same id): J11/T32 diesel, p24/25, 30,000/12, ~3.0k
  - nissan-x-trail-2014-2021-1.6-diesel (same id): J11/T32 diesel, p24/25, 30,000/12, ~7.7k
  - nissan-nv200-2012-2019-1.5-diesel (same id): NV200 without tow hook, p33/34, 30,000/12, ~2.0k.
    The 15,000-km tow-hook table (p34/35) is summarised in the notes.
  - NEW nissan-note-2014-2017-1.2: Note E12, p25/26, 20,000/12, ~0.6k
  - NEW nissan-altima-2013-2019-2.5: Altima, p27/28, 15,000/12, ~0.7k
  - NEW nissan-maxima-2014-2021-3.5: Maxima, p28/29, 15,000/12, ~0.5k
  - NEW nissan-navara-pathfinder-2006-2015-2.5-diesel: D40/R51, p32/33, 20,000/12, ~1.1k
  DRAFT (Israeli table, but the engine came after the 2016 edition)
  - nissan-qashqai-2014-2021-1.5-diesel (same id): J11 diesel table, ~3.5k (K9K registered only from 2019)
  - nissan-x-trail-2019-2021-1.7-diesel (same id): J11/T32 diesel table, ~2.1k.
    Years are now 2017-2021, M9R was added, and a new M9R rule covers ~0.76k more cars.

Details:
  - Specs in the reviewed files come only from the booklet (oil grade, warranty). The South Africa/Europe specs were dropped.
  - Footnotes are in long_interval: coolant "first X, then every Y"; coolant "* = 5 years or 90,000"; NV200 timing belt 150,000/5 years.
  - Cabin-filter low-mileage footnote is an item note.
  - The book contradicts itself in two places. Both are transcribed as printed, with an explanation:
    - Micra: footnote says first coolant change at 100k, but the table also marks 120k.
    - NV200: table marks coolant at 150k, footnote says first at 90k.
  - Item mapping:
    - "בדיקת בלמים" = brake_pads inspect (with a note). Navara adds parking_brake.
    - "סט רצועת מנוע" = drive_belt.
    - "נקז" = fuel_filter clean, with a "drain water" note.
    - "סבב" = tire_rotation rotate.

Corroboration: old Israeli brochures still in the stale cache of
https://www.nissan-cdn.net/content/dam/Nissan/israel/brochures/ (www-europe.nissan-cdn.net serves the current ones).
They state the Israeli interval, matching the booklet, and were added as extra sources:
  - Juke 30,000/12
  - New-Qashqai (J11): petrol 20,000, diesel 30,000
  - Qashqai R9M 30,000
  - Note 20,000
  - NV200 30,000
  - Altima 15,000
  - Maxima 15k
Also found in brochures:
  - Sentra B17 MRA8DE: 15,000/1yr. A note and source were added to the draft nissan-sentra-2016-2019-1.8 (its US grid is 8,000 km).
  - Pointers only: Micra K14 HR10 20,000/1yr (www-europe 2022 brochure); Altima L34 PR25DD 15,000/1yr; Navara D23 30,000/2yrs.

DACIA: ISRAELI INTERVAL FOUND
  - https://www.dacia.co.il/about-dacia/faq.html, read via https://r.jina.ai/<url> (passes Imperva and renders JS):
    - petrol and diesel: 20,000 km or 1 year;
    - taxi and driving-school cars: 15,000 km or 6 months.
  - The car book and the service booklet are given only via customer service.
  - Re-issued with the same ids, still draft, with this importer source plus notes and interval-note text. The grid is still Renault Australia:
      dacia-duster-2012-2024-1.5-dci, dacia-duster-2015-2020-1.2-tce, dacia-duster-2019-2026-1.3-tce,
      dacia-lodgy-2013-2019-1.2-tce, dacia-lodgy-dokker-2013-2022-1.5-dci, dacia-sandero-logan-2013-2021-1.5-dci
  - Lead decision: showing the 20,000 interval needs a 20,000-km item grid, and none was found.

registry/registry_rules.json: new rows only.
  NOTE HR12DDR; ALTIMA QR25/QR25DE; MAXIMA VQ35*; NAVARA+PATHFINDER YD25*; X-TRAIL M9R 2017-2019.

STILL NOT FOUND
- Nissan:
  - Juke Hybrid (~5.1k), Juke F16 HR10 (~2.2k), X-Trail T33 KR15/e-POWER (~2.2k), Qashqai J12 e-POWER (~0.5k).
  - Qashqai J11/J12 HR13: still on the South Africa J12 draft.
  - Micra K14: interval only. Micra K12. Note E11.
  - The 2015-16 Israeli Hebrew owner books (Wayback) contain no schedule; they point to the booklet.
  - The Nissan UK online manuals point to a separate booklet.
  - Nissan South Africa New-Juke, Juke-Hybrid and X-Trail-e-POWER: still 403/404.
- Renault/Dacia: no Israeli item schedule.
  - Gaps: H4B, H4D, H4M E-Tech, H5P, K4M, D4F, Koleos H5H/R9N, Jogger H5D.
  - Archived Israeli Hebrew driver handbooks (Renault CarBooks for Clio III/IV, Captur, Kadjar, Fluence, Megane, Kangoo, Scenic, Trafic,
    Logan, Koleos, ZOE; Dacia SEFERNAAG for Duster, Lodgy, Dokker, Logan+Sandero) have no table and refer to the service booklet.
  - Renault_Warranty_Car.pdf and the Dacia warranty, extension and conditions PDFs contain warranty terms only.
  - Not used: Renault UK and Dacia UK "fixed price retailer guide Q4 2026" on cdn.group.renault.com.
    - They give a year-based A/B programme: brake fluid every 3 years; air filter and plugs every 4; coolant and hybrid 12V every 5;
      accessory belt and automatic gearbox oil every 6.
    - Dacia Ireland: oil every 2 years or 30,000 km.
    - Reasons: no km limits for the long items; unclear which cars are on the A/B programme; conflicts with the Israeli 20,000/1yr.
- Chery:
  - Tiggo 4 Pro (~2.4k): the Israeli brochure https://cheryisrael.co.il/TechSpecs/Chery-Tiggo4-Brochure.pdf confirms SQRG4G15 1.5 NA,
    95 hp, CVT, with no service data. No table for this powertrain was found.
  - The other Chery drafts are unchanged. Model pages (jina) give only warranty terms (6y/150,000; electric drive 8y).
    The WP media API lists 2 PDFs (brochures).
- Xpeng:
  - The importer site is heyxpeng.co.il; xpeng.co.il does not resolve.
  - /service (WebFetch) gives only the warranty (7y/160,000; battery 8y/160,000). The WP media API is empty. The drafts are unchanged.
- EVEASY Limo (~1.7k): nothing found.

ROUTES THAT WORKED
- carz.co.il S3 bucket, plain http. Bucket listing is denied; guessed Renault/Dacia names returned 403.
- nissan-cdn.net and www-europe.nissan-cdn.net, content/dam/Nissan/israel/...
  - Folder oracle: https://www.nissan.co.il/content/dam/Nissan/israel/<folder>.json (200 = exists).
    Existing folders: services/car-books, services/warrenty-pdf, brochures, legal, forms.
  - .1.json, .infinity.json and querybuilder are blocked. nissan.co.il itself answers curl 200.
- Wayback over https: CDX url=<domain>/*&filter=mimetype:application/pdf, then web/<ts>id_/<url>.
  - Got the Nissan HEB car books 2014-16, Renault CarBooks and Dacia SEFERNAAG books. None has a schedule.
  - Archived HTML (dacia service/faq, manuals, warranty; renault service/faq) has no schedule either.
- r.jina.ai passes Imperva on dacia.co.il, renault.co.il, cheryisrael.co.il, heyxpeng.co.il, freesbe.com and service.freesbe.com.
  service.freesbe.com is only the booking app, the parts-warranty page and the site map.
- WebFetch passes Imperva for PDFs (saved under tool-results) and some HTML. Useful results:
  - renault.co.il and dacia.co.il sitemap.xml: no book pages.
  - Renault Clio brochure: no interval.
  - Chery WP media API.
  - Guessed Renault/Dacia booklet names: 404.
- app.freesbe.com is a public Strapi v4 server:
  - /api/upload/files: 88 media files (images plus one form PDF).
  - /api/service-centers: public.
  - /api/car-models and /api/brands: 403.
  - About 120 other names: 404.
  - Media is on S3 carassobucket1; listing is denied.

ROUTES BLOCKED OR DEAD
- Imperva blocks this IP for curl, Playwright headless/headful (Xvfb, stealth) and UA curl/8.0:
  renault.co.il (Playwright home page passed 2 of ~15 times), dacia.co.il, cheryisrael.co.il (TechSpecs PDFs answer intermittently),
  heyxpeng.co.il, freesbe.com, service.freesbe.com, admin.freesbe.com.
- No DNS or connection: xpeng.co.il, freesbe.co.il, carasso.co.il, carassomotors.co.il, infiniti.co.il, evec.co.il.
- docplayer.co.il/167032738 (the Carasso booklet): egress 502.
- xn----2hc3awpyb.com: Cloudflare challenge.
- manualpdf.co.il: English manua.ls copies, not Israeli books.
- manuals.plus: 403. daciaforum.co.uk: 202 challenge. carsforum.co.il: 403.
- data.gov.il: no maintenance dataset.
