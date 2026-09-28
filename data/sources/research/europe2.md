# Group "europe2": report (round 2)

2 schedule files (both **draft**) and `registry/registry_rules.json` (6 rules, 2 of them for the new files and 4 sister rules pointing at the existing Toyota Aygo files).
Validation: `node scripts/validate.mjs staging/europe2` prints "all schedules valid (2 draft, 0 reviewed, 0 verified)".
Generator: `scratchpad/dl/europe2/gen/opel.py` (holds every transcribed mark). Downloads and screenshots: `scratchpad/dl/europe2/`.

## Files

| id | status | interval | registry target | source |
|---|---|---|---|---|
| opel-corsa-2008-2015-1.2-1.4 | draft | 30,000 km / 12 months, cycle 150,000 | CORSA / CORSA-D / CORSA D / CORSA-WR with A 1.4 XER, A14XER, A 1.2XER, Z14XEP, 2008-2015 (about 3.6k cars) | grid: manualslib 504809 (Opel Corsa D EN owner's manual), "Service schedule Europe", printed pp. 232-234 = site pages 238-240; interval: Hebrew Corsa D MY2013 manual on public-servicebox.opel.com, p. 176 (Israel is listed in the European plan, 30,000 km / 1 year) |
| opel-corsa-2015-2019-1.4 | draft | 15,000 km / 12 months, cycle 75,000 | CORSA with B14XER, 2015-2019 (about 2.5k cars) | grid: same manual, "International service schedule", printed pp. 235-237 = site pages 241-243 (same marks, 15,000 km columns); interval: Hebrew Corsa E MY2016 manual, p. 224 (Israel is no longer in the European list, so the international 15,000 km / 1 year plan applies) |

Notes on the Corsa files:
- The Hebrew Opel manuals (`public-servicebox.opel.com/OVddb/OV/he_IL/...`) give the interval only. The English manuals on the same portal (`OVddb/OV/en_AU/index.html`, Corsa D 2011/2013 and Corsa E 2017) also have no item grid. The only grid found is the older Corsa D English manual on manualslib (504809). That edition lists Z-series engines, not A14XER/B14XER, so both files are drafts. For Corsa E it is the previous generation on the same platform.
- The book lists timing belt, valve clearance and petrol fuel filter work only for Z16LEL/Z16LER/Z17DTR. No such row was added for the 1.2/1.4, and the specs `_note` says so. The files do not say "chain" because no opened document states it.
- Brake fluid level check: the manualslib watermark covers column 2. Column 4 is clearly empty and the fluid is replaced every 2 years, so the check was put in columns 1, 3 and 5 only.
- Importer: Opel was imported by the Shlomo group (קבוצת שלמה) from 2010 to 2019, then by Lubinski (source: web search result quoting he.wikipedia "אופל (יצרן רכב)").

## Sister mapping (registry only, no new file): Peugeot 107/108 and Citroen C1 → Toyota Aygo
These cars are built with the Aygo in the same Kolin plant, with the same 1KR-FE 1.0 engine. The registry uses engine code 1KR for them, plus CFB (the PSA code for the same engine) on C1 2010-2011. The rules point them at the existing Israeli Union Motors Aygo sheets. They are **draft sister mappings**: the numbers come from Toyota's Israeli book, not from a Lubinski document.
- Peugeot 107, 1KR, 2005-2014 → `toyota-aygo-2005-2013-1.0` (sheet title "Aygo 2005-2014"), about 3.3k cars
- Peugeot 108, 1KR, 2014-2022 → `toyota-aygo-2014-2022-1.0`, about 1.9k cars. 108 with HM01 (1.2 PureTech, 302 cars) is left unmatched on purpose.
- Citroen C1, 1KR/CFB, 2005-2013 → `toyota-aygo-2005-2013-1.0`; C1 1KR 2014-2022 → `toyota-aygo-2014-2022-1.0`, about 3.1k cars. Model year 2014 (179 C1s) is split the same way as the Aygo rules; the generation change was mid-2014.
- Suggestion: the app should say the plan is the Toyota Aygo plan, used because the car is its twin.

## Not done / blocked (in order of vehicle count)

### Citroen Berlingo / Peugeot Partner B9, 1.6 HDi / BlueHDi (DV6: BH02, 9H06, 9HN, 9HP, 9HW, 9HX, 9H02; about 14k cars)
No usable grid was found. Routes tried:
- Union Motors Toyota books API: `books.union-motors.co.il/app/api/search?modelId=22&year=2016..2020` (Proace). The Israeli Proace maintenance sheets (connection 432, fileId 306 and connection 751, fileId 330) are the 2.0 D-4D MDZ sheets (same as round 1's 603). There is no Israeli Proace with the 1.6 DV6, and no Proace documents exist before 2016.
- Peugeot DDB `public.servicebox.peugeot.com/APddb/`: it is open and has **Hebrew handbooks** (`interface/hard_divs/carnav_he_il.xml` lists 108, 2008, 207, 208, 3008 (2017+), 301, 308, 408, 5008, 508, Boxer, Expert, Partner K9, Partner VU 2015). The PDFs are at `modeles/<model>/<silhouette>/<edition>/he_il/<model>_<silhouette>_<edition>_he_il.pdf` (for example `modeles/3008/3008_p84/ed01-17/he_il/3008_3008_p84_ed01-17_he_il.pdf`, 348 pp.). These are owner's handbooks without a km grid; the 3008 handbook p. 222 has only filter advice. The Hebrew Partner "partnervu" 2015 handbook could still be checked for an interval statement. `service.citroen.com/ACddb/` redirects, but the index did not load in curl.
- Peugeot Australia capped-price page `service.peugeot.com.au/peugeot/cps/peugeot/20151221v1.html`: 12 months / 15,000 km for all models, prices only, no item list (Partner 1.6 HDi and 3008 1.6 THP are in the price table).
- Web search: only third-party sites (auto-abc.eu, forums). Their numbers were not used.
- Next ideas: manualslib (in Playwright) for a PSA "Maintenance and Warranty Guide" / "Guide d'entretien" of the B9 era; Ford/Mini/Volvo DV6 books are not a valid sister (different makers' plans).

### Peugeot 3008 gaps (about 7k cars): BH01 (1.6 BlueHDi, 2017-2018, 2.6k), 5G01 (1.6 THP 165, 2015-2018, 2.0k), 5G06 (1.6 THP 180 and PHEV, 2019-2024, 2.2k)
Not done. Same blocker as above: the Hebrew 3008 handbook on the Peugeot DDB has no grid. The Lubinski clearmash books are still blocked (Cloudflare), per round 1.

### Mercedes-Benz, BMW, Volvo
Not started; the time budget ran out. Planned route: Volvo/Mercedes/BMW global digital owner's manuals for the fixed fallback intervals of their flexible (condition-based) service, plus an item list.

## Registry notes
- Registry engine codes with spaces: "A 1.4 XER", "A 1.2XER" (Opel). The rules list both the spaced and unspaced spellings.
- `registry_rules.json` is in the `registry/` subfolder.
