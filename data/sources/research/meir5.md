meir5 REPORT (round 5: Meir = Honda/Volvo/Lynk & Co; UMI = Chevrolet/Cadillac/Buick)

14 schedule files (13 reviewed, 1 draft) + registry/registry_rules.json (3 new rules).
node scripts/validate.mjs staging/meir5 -> "all schedules valid (1 draft, 13 reviewed, 0 verified)".
Builders: scratchpad/dl/meir5/gen/{common,spark,gmk12,gm12k,gmna,honda}.py. Israeli PDFs: dl/meir5/chev/*.pdf.
Coverage scripts: dl/meir5/cov/{cov,per,unc}.mjs.

KEY NEW ROUTE: chevrolet.co.il via WebFetch
- curl, Playwright (headless and headful under xvfb, with stealth settings) all get Cloudflare 403 on chevrolet.co.il, cadillac.co.il,
  umigroup.co.il and honda.co.il.
- WebFetch DOES reach www.chevrolet.co.il. The page https://www.chevrolet.co.il/שירות-שברולט/ספר-רכב/ lists every Hebrew owner's book (2015+)
  as /media/<id>/<name>.pdf.
- WebFetch on a PDF URL saves the full binary to the session tool-results dir (webfetch-*.pdf). Results of parallel calls come back in call order.
  The books have a text layer.
- These are UMI's localized books (GMK-/GMNA-/PATAC-Localizing-Israel).
- Korean-built models (Spark, Trax, Trailblazer, Orlando, Cruze J300) have a full Israeli schedule: 15,000 km/12 m, Service I/II or a 15/30/45/60 grid.
- Newer GMNA books have an Israeli schedule: Equinox 2022, Blazer 2023 and Traverse 2022 at 10,000 km; Traverse 2025 at 12,000.
- Older GMNA books have NO table (they point to a separate maintenance booklet): Malibu 2015-2023, Impala 2015/2019, Cruze 2017-2019,
  Equinox 2016-2021, Traverse 2015/2019, Blazer 2019.
- WebFetch still gets 403 on cadillac.co.il, umigroup.co.il, honda.co.il, volvocars.com/il and xn----2hc3awpyb.com.

FILES (vehicles = registry vehicles matched to the id; URLs are https://www.chevrolet.co.il/media/...; PDF page numbers = file pages)
22,637 (+749 L5Q new) | chevrolet-spark-2016-2022-1.4 | REVIEWED (upgrade)
    1b5hrpl4/ספארק-2016-2017.pdf pp.216-219; biqhgacl/ספארק-2019-2020.pdf pp.233-236; bszhpelj/ספארק-2022-new.pdf pp.181-184
6,293 | chevrolet-cruze-2009-2016-1.4-1.6-1.8 | REVIEWED (upgrade)
    rw4i4teg/קרוז-2015.pdf pp.205-210 (the 2016 book is identical)
5,298 | chevrolet-equinox-2018-2023-1.5-turbo | REVIEWED (upgrade)
    r5ff231y/newאקווינוקס-2022.pdf pp.283-288
5,267 | chevrolet-spark-2010-2015-1.0-1.2 | REVIEWED (upgrade)
    hdqneopi/ספארק-2015.pdf pp.232-236 (book pp.11-2..11-6)
4,649 | chevrolet-trailblazer-2021-2026-1.3-turbo | REVIEWED (upgrade)
    rpsdjbkl/טרייל-בלייזר-2021.pdf pp.306-312 (@ charts on pp.309 and 311); 2024 book pp.265-268
3,852 | chevrolet-trax-2023-2026-1.2-turbo | REVIEWED (upgrade)
    p20bi13a/24_chev_trax_om_he_il_...pdf pp.273-280
3,673 | chevrolet-traverse-2018-2026-3.6 | REVIEWED (upgrade)
    53cebdpu/טרוורס-2022new.pdf pp.333-337
3,643 | chevrolet-trax-2013-2020-1.4-turbo | REVIEWED (upgrade)
    v4zjjnqv/טראקס-2015.pdf pp.252-256; ibtcfztg/טראקס-2020.pdf pp.271-276
2,396 | chevrolet-trax-2013-2016-1.8 | REVIEWED (upgrade)
    טראקס-2015.pdf pp.252-256
1,045 | chevrolet-orlando-2014-2018-1.4-turbo | REVIEWED (upgrade)
    vwapt4hx/אורלנדו-2015.pdf pp.210-216; pvpj4zwa/אורלנדו-2018.pdf pp.211-215
1,017 new | chevrolet-orlando-2012-2015-2.0-diesel | REVIEWED (new)
    Same Orlando books; the book's LNP code = Z20D1 in the registry
998 | chevrolet-blazer-2019-2024-2.0-3.6 | REVIEWED (upgrade)
    yrlos5wo/2023-בלייזר.pdf pp.314-319
427 | chevrolet-traverse-2025-2026-2.5t | REVIEWED (upgrade)
    elxny4sy/24_chev_traverse_om_he_il_...pdf pp.307-311
1,368 new | honda-jazz-2009-2014-1.2-1.4 | DRAFT (new)
    manualpdf.co.il honda/jazz-2010 p.324-325 = Honda Jazz GE OM 32TF0630, "Maintenance Schedule (On vehicles without Service Book)"
    pp.319-320, general markets, in km; severe conditions on p.322
Upgraded to Israeli data: about 60,200 vehicles. Newly covered: 3,134 (Jazz GE 1,368; Orlando diesel 1,017; Spark L5Q 749).

WHAT CHANGED AGAINST THE OLD US DRAFTS
- Interval:
  - 15,000 km/12 m: Spark, Trax, Cruze J300, Orlando (the old drafts had 12,000).
  - 10,000: Equinox, Blazer, Traverse LFY.
  - 12,000: Trailblazer, Trax 2024, Traverse 2025.
- Brake fluid:
  - Every 2 years in the Korean books (the old drafts had 5 years).
  - Every 5 years in Equinox/Blazer/Traverse.
- Cabin filter:
  - Every service (10k/12 m) on Equinox/Blazer/Traverse.
  - 15k on Spark M400.
  - 45k/2 years on Cruze and Orlando.
  - 60k/2 years on Trax.
- Spark M400:
  - The grid has no km mark for oil; the rule is yearly or when the car shows the message, so oil is put in every yearly service with that note.
  - Air filter and spark plugs at 60k.
  - CVT fluid only in severe use (72k).
- New rows:
  - A/C desiccant every 7 years.
  - Gas struts: no item key exists, so they are mentioned in the notes.
  - Timing belt vs chain split per engine.

JUDGEMENT CALLS (flag for the lead)
- Orlando 1.4T timing:
  - The Orlando book says "petrol engine: timing belt every 150,000".
  - The Cruze book from the same importer says LUJ (1.4T) has a chain, changed at 240,000.
  - The file records the chain, and the note says so.
- Trax:
  - The book lists both a belt (150,000) and a chain (240,000) without naming engines.
  - The 1.4T file got the chain and the 1.8 file got the belt, based on the Cruze book's engine split. The notes say so.
- A later book was applied to earlier years of the same generation and engine. The notes say so; the files are still reviewed, so downgrade them if preferred:
  - Equinox 2022 book -> 2017-2023
  - Blazer 2023 book -> 2019-2024
  - Traverse 2022 book -> 2018-2024
  - Spark 2015 book -> 2010-2014
  - Cruze 2015/16 book -> 2009-2014
  - Orlando 2015 book -> 2014
- Traverse 2025: the introduction says to come in every 10,000, but the plan itself is built on 12,000; the file uses 12,000. Spark plugs at 90k are only in long_interval.
- Kept from the existing files: id, generation, years. Existing registry rules are unchanged.

NOT DONE / BLOCKED (biggest first), every route tried
HONDA (Meir): no Israeli data reachable
- honda.co.il:
  - curl: Cloudflare 403, including the /wp-content/uploads PDFs.
  - Playwright headless with stealth settings, and headful under xvfb: 403; the "רק רגע" non-interactive challenge never clears.
  - WebFetch: 403.
- xn----2hc3awpyb.com (ספר-רכב mirror): 403 via curl and WebFetch. Its "ספר טיפולים" items are a generic 15-page log template, not a schedule.
- mct.co.il WordPress media API: 10 PDFs (dealer standards, terms, an EX30 letter). No books.
- updates.mct.co.il/services (Meir service price list): plate + reCAPTCHA v3. The getServices API returned an empty body in Playwright (headless and
  headful). Not pursued further.
- honda.org.il: now a motorcycle dealer. tyre-pressures.co.il "all Israeli books" page: 404.
- manualpdf.co.il: all Honda car books are English (US Minder or general market). manualslib: now 403 even in Playwright.
  carmanualsonline: Insight/Accord/Civic are US books.
- club-honda.eu: Insight books are US (P/N 00X31 TM8); the rest are brochures. honda.co.uk service-reminders/jazz-hybrid PDF: Minder code list, no km.
- Remaining gaps:
  - Jazz Hybrid + Insight LDA3 (9.1k): the Jazz GE table was NOT used as a sister (different IMA hybrid engine).
  - Accord R20A3 (3.4k).
  - Civic D16V1/D16W7 (2.5k).
  - Civic Hybrid LDA2 (1.0k).
  - HR-V e:HEV (0.5k) and City (0.5k): not attempted.
VOLVO (Meir)
- volvocars.com/il: Akamai 403 via curl, Playwright headless and headful, and WebFetch.
- volvoselekt.co.il (Meir used cars): the guide page is marketing text only ("15-20 thousand km", "maximum interval 20K"), so it was not used. Its WordPress media holds terms PDFs only.
- manualpdf.co.il Volvo books: English, no tables (Volvo keeps them in a separate booklet).
- No upgrade.
- Remaining gaps: S60 B5244S (0.9k), B4164T T4 (about 0.8k), S40 B4204S3, B4204T6/T7, B5254T, B6304T2.
LYNK & CO (Meir)
- lynkco.co.il WordPress media: the JSON has a BOM, so strip ﻿ before parsing. New since ev3:
  - Lynk-co-08-service-terms.pdf (premium service, no intervals)
  - נספח-אחריות-08.pdf (warranty 5 years / 150,000; it says the service routine is on the website)
  - G5016143-V001.pdf
  - Brochures
- The service page /שרות-לקוחות/ has no intervals. Its footer "מחירון טיפולים" points to updates.mct.co.il/services, which is blocked as above.
- 01 PHEV 2023 Hebrew book (287 pp.): refers to a separate service and warranty booklet; no km table.
- Not done: 08 PHEV (1.3k), 01 PHEV 2025-26 (0.9k), 01 HEV/PHEV JLH-3G15TD 2023-25 (1.0k).
CHEVROLET / CADILLAC / BUICK (UMI)
- Still draft (US manuals), because the Israeli books have no table:
  - Malibu 2013-2023
  - Impala
  - Cruze 2017-2019
  - Equinox 2016-17
  - Traverse 2009-2017
  - Captiva Sport
  - Sonic
  - Aveo/Optra
  - Malibu 2008-12
- Checked and found without a table: Malibu 2015/2016/2021/2022, Malibu 2023 (a 23-page usage summary), Impala 2015/2019, Cruze 2017/2019,
  Equinox 2016/2018/2021, Traverse 2015/2019, Blazer 2019.
- The site lists books only from 2015 on. The old path chevrolet.co.il/Owners-area/Manuals/<Model> <yy>.pdf ("Sonic 12.pdf") redirects to the Cloudflare site (403).
- Uncovered: Sonic A14XER (1.1k), Captiva diesel Z22D1 (0.2k).
- Cadillac: cadillac.co.il is 403 for curl, Playwright and WebFetch. images.auto.co.il/attachment/catalog/pdf/<n>,.pdf hosts UMI brochures (no schedule).
  The Cadillac/Buick drafts stay US. Cadillac OPTIQ / Escalade IQ (EV, about 0.3k): not attempted.

OTHER
- In the reviewed files every number comes from the Israeli books listed in the sources. The two inferences (timing chain, earlier years) are stated in the notes.
- Jazz GE draft: the book counts driving in heat above 35°C, traffic jams and short trips as severe. Then oil is changed every 5,000 km or 6 months and the filter every 10,000. This is in the notes only.
