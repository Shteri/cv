prem3 report (Mercedes-Benz, BMW/MINI, Volvo, Audi, Lexus, Land Rover)

18 schedule files (16 draft, 2 reviewed) + registry/registry_rules.json (18 rules, one per schedule, exact names + engine_codes + fuel).
node scripts/validate.mjs staging/prem3 -> "all schedules valid (16 draft, 2 reviewed, 0 verified)".
Simulated coverage (current repo registry_map.json + these rules, registry_coverage.mjs on a copy): 3,499,840 -> 3,591,711 covered (+91,871; 85.5% -> 87.8%).
Generator: scratchpad/dl/prem3/gen.py (downloads and page renders in scratchpad/dl/prem3/).
All condition-based brands: Hebrew note says the car's indicator (ASSYST PLUS / CBS / Volvo SRI / JLR) decides. Miles converted to km (1 mi = 1.609 km, rounded), noted in each file.

PER SCHEDULE (vehicles | id | status | interval | sources)
15778 | bmw-b38-b48-b58-2015-2026-petrol | draft | 16,000 km/12 m | BMW USA Maintenance booklet MY2025 pp.10-16 (bmwusa.com PDF via Playwright request); MY2021 booklet pp.9-14 (dealer-hosted copy di-uploads-pod15.../bmwofescondido). Cabin filter every 2nd oil service, air filter every 4th, plugs every 6th (~60k mi), X1/X2 ATF ~60-72k mi; coolant/ATF otherwise long-term.
10999 | mercedes-benz-c-e-glc-gle-2011-2026-petrol | draft | 20,000 km/12 m | mercedes-benz.ca/en/owners/service-maintenance (Playwright): Service A first ~20,000 km or 1 yr, B 1 yr later, alternating, with content lists. mbusa.com/en/owners/service-maintenance: Service B includes brake fluid exchange + cabin/combination filter.
9425 | mercedes-benz-c-e-glc-gle-2010-2026-diesel | draft | 20,000 km/12 m | same + AdBlue (Canada page). Van names excluded.
9049 | mercedes-benz-a-b-cla-gla-2013-2026-petrol | draft | 20,000 km/12 m | same (M270/M282/M260/M252).
7596 | mercedes-benz-plug-in-hybrid-2016-2026 | draft | 20,000 km/12 m | same (E300e/C300e/C350e/GLC300e/350e/A250e/CLA250e/GLA250e/GLE350de/S560e...).
7131 | bmw-plug-in-hybrid-2016-2026 | draft | 16,000 km/12 m | BMW USA booklets 2021 (330e/530e/X3 30e/X5 45e) and 2025; adds 2nd coolant reservoir + charging cable/port checks.
6221 | volvo-s60-v40-xc40-xc60-xc90-2014-2022-drive-e-petrol | draft | 16,000 km/12 m | Volvo Car USA "Schedule of Factory Maintenance Service Operations 2020/2021 ICE and PHEV" (2 pp, azure-eu-assets.contentstack.com): 10k mi/12 m; cabin filter 20k; air filter + chassis 40k; plugs 60k; ATF 50k only if towing; timing + accessory belt 150k mi/10 yrs; brake fluid 3 yrs. Volvo Laval (Canadian dealer) page agrees in km.
4964 | mini-cooper-countryman-2014-2026-1.2-1.5-2.0 | draft | 16,000 km/12 m | MINI USA Maintenance booklets 2021 pp.9-12, 2025 pp.12/14 (2018/2019/2024 checked too), minipub-prod.bmwgroup.com. Registry make "BMW" (COOPER, COOPER S, ONE, MINI ONE, COUNTRYMAN..., JOHN COOPER WOR).
4807 | volvo-xc40-xc60-xc90-s60-2016-2026-plug-in-hybrid | draft | 16,000 km/12 m | Volvo USA 2020/21 ICE+PHEV sheet + 2025 PHEV/MHEV sheet (accessory belt at 80k mi).
4419 | audi-q5-a4-a5-a6-2017-2026-2.0-tfsi | draft | 15,000 km/12 m | Champion Motors service routine, table "2.0 ל׳ בנזין" (importer), read from saved real-browser copy dl/vag/champion_routine.html (28.9.2026; live page is Reblaze 247 today even in Playwright). Draft only because code->2.0 TFSI mapping (DAX/DNT/DPU/DXA/DMS/DMT/DWZ/DKN/DLZ/DKZ/CZP) is unverified. Q3/S/RS names excluded.
4369 | volvo-s60-xc40-xc60-xc90-2020-2026-mild-hybrid | draft | 16,000 km/12 m | Volvo USA 2025 PHEV/MHEV sheet (+2020/21). B420T2/T4/T5/T11.
2320 | lexus-ux250h-ux300h-2019-2026-2.0-hybrid | draft | 15,000 km/12 m | Hebrew UX200 book (books.union-motors.co.il/LexusApp/api/files/74/download) pp.395-396 (PDF 396-397), table header says engine M20A-FXS. UX250h (conn 77, p.302) and UX300h (conn 71) books have no table.
2092 | volvo-ex30-xc40-c40-ex40-2021-2026-ev | draft | 32,000 km/24 m | Volvo USA "2026 FSM Maintenance Sheets Fully Electric": 20k mi or 2 yrs; EX30 one-time axle oil at 40k mi. ES90 excluded.
1125 | mercedes-benz-sprinter-2018-2026-diesel | draft | 32,000 km/24 m | mbvans.com "2025 MB Vans Fleet and RV Brochure" pp.3-4: A/B every 20k mi or 2 yrs to 160k; brake fluid 2 yrs, air filter 60k mi/4 yrs, Poly-V 80k mi/4 yrs, coolant 220k mi/15 yrs then every 3 yrs, fuel filter every service.
670 | lexus-rx300-2016-2022-2.0-turbo | REVIEWED | 15,000 km/12 m | Hebrew RX300/RX350/RX350L book (LexusApp files/148) p.730 "לוח אחזקה RX300 8AR-FTS" 26.4.18 (image-transcribed).
460 | land-rover-discovery-4-range-rover-sport-2014-2019-3.0-diesel | draft | 26,000 km/12 m | JLR owner handbook chapter on TOPIx (topix.landrover.jlrext.com procedure 565244 = MY16 plan 1; procedure 418654 = MY14 plan + fluid table). Israel is in the country list. Brake fluid 3 yrs, coolant 10 yrs. A/B content is only on the dealer check sheet -> only oil/filter per service.
341 | lexus-ux200-2019-2021-2.0 | REVIEWED | 15,000 km/12 m | Hebrew UX200 book (files/74) pp.395-396.
105 | land-rover-evoque-discovery-sport-2014-2018-2.0-petrol | draft | 16,000 km/12 m | same JLR handbook pages.

JUDGEMENT CALLS
- BMW/MINI time cap: US booklets give none for combustion engines ("as specified by CBS"). 12 months comes from the booklet's example CBS screen for a new car (oil "in 10000 mi" one year later, brake fluid ~3 years). Said so in the note; brake fluid = time_based 36 months "per CBS".
- Mercedes: Canada (km market) = 20,000 km/1 yr. European 25,000 km/1 yr could not be opened from any Mercedes page, so not used. Spark plugs, air filter, coolant, gearbox oil are in no opened Mercedes source -> omitted, Hebrew note says so.
- Volvo: US sheets (miles) only; 2025 sheets add accessory belt at 80k mi -> 128,000 km in MHEV/PHEV.
- Lexus UX hybrid copied from the UX200 table; drive-belt row dropped for the hybrid, CVT row kept as inspect with note.

BLOCKED / DEAD ROUTES
- mercedes-benz.co.il/site/car-books: books only via email form with captcha; /services/manuals: none. colmobil.co.il wp-json media: non-JSON.
- mercedes-benz.co.uk/.com.au/.co.nz/.de/.co.za/.co.in/la.mercedes-benz.com: proxy 502 / 503 (curl, Playwright, WebFetch). .ie/.com.cy/mena reachable, no numbers. mercedes-benz.ca service booklets and mbusa warranty booklets: no interval numbers. bevo -> operatingfluids.mercedes-benz.com (SPA, empty). forum-mercedes.com PDF: Cloudflare.
- bmw.co.il, kamor.co.il, mini.co.il: proxy 502. bmw.ca/.co.uk/.de/.ie/.co.za/.com.au: 000/502. bmwusa.com HTML: socket hang up. BMW 2017 US booklet and bmwtechinfo SIB CBS attachments: 404/hang.
- volvocars.com (incl. /il) and its /images PDFs: Akamai 403; same PDFs load from azure-eu-assets.contentstack.com.
- championmotors.co.il/service-routine: Reblaze 247 (saved copy used). audi.co.il: 247.
- landrover.co.il: no numbers; ownerinfo.landrover.com: no connection; no TOPIx handbook found for 2020+ models.

NOT COVERED (biggest first)
- Mercedes VITO / V CLASS / VITO TOURER (OM651/OM654, ~3.5k): no Vito source opened (Sprinter sheet not used as sister).
- BMW diesels X6/X5 30d (B57/N57, ~3k), X3/X4 20d; BMW N-engine petrol 2009-2016 (N20/N13/N46/N52/N55, ~5k).
- Mercedes EVs (EQA/EQB/EQC/EQE/EQS ~3.5k) and BMW EVs (iX3/iX1/iX2/i4/i5/iX ~2.7k): sources only say "2 years" / "24 months, no mileage influence" (BMW 2025 p.17); no km -> not written (Tesla-style placeholder possible).
- Mercedes pre-2011 (M272/M271/M112/OM646).
- Land Rover 2019+ (RRS PHEV PT204/PT306, Evoque L551, Defender DT306, RRS DT306, Discovery 5, Velar, ~6k).
- Volvo S60 2008-10 (B5244S), S80 2.5T, XC60 T6 3.0, S40/C30 2.0, Ford-engine T4 1.6 (B4164T), T5 2012-13 (B4204T6/T7).
- Lexus RX350h (663) / RX450h+ (459): suggest rule to existing sister lexus-nx350h-2022-2026-2.5-hybrid. RX350 2GR (577), NX300 8AR (267; table on conn 158 pp.480-481 not transcribed), IS300 (316), UX300e.
- Audi A4 B8 1.8 TFSI CDH (1.25k), A6 C7 CDN/CYG/CYP, Q7 CRT older, Q5/A7 TFSI e.
