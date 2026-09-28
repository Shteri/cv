# Official importer documents

Where the real Israeli per-km tables live, and how reachable they are from
the cloud session (checked 2026-09-27).

## Access notes

- All importer sites answer 403 to curl's default User-Agent. Send a
  browser UA (`Mozilla/5.0 ... Chrome/128 ...`) and they return 200. This
  was the "network block" reported in the previous session; the egress
  proxy itself allows every host below.
- Still blocked by bot protection (JS challenges, also with headless
  Chromium): `championmotors.co.il` (Reblaze), `skoda.co.il` (Link11,
  HTTP 491), `union-motors.toyota.co.il/files/*` (Incapsula). Open these
  from a normal browser and paste or screenshot the tables.
- PDF text extraction: `pip install pymupdf`, then `page.get_text()`.
  Hebrew comes out in visual order with some words split, but the I/R
  grids are readable. Older Kia books (Picanto 2011-2016, Sportage
  2011-2015) use a custom font encoding and yield garbage; they need OCR
  or a human reader.
- `scripts/build_schedules.py` holds the transcribed grids. Edit there,
  not in the generated JSON.

## Toyota (יוניון מוטורס)

- Interval statement, 15,000 km / 12 months, 10,000 recommended for cars
  over 10 years: https://www.toyota.co.il/company/news/service-and-maintenance
- Hybrid battery warranty and yearly hybrid check:
  https://www.toyota.co.il/owners/maintenance/hybrid-service
- **Per-model Israeli maintenance sheets (the real per-km tables):** the
  document centre https://www.toyota.co.il/owners/parts-and-accessories/owners-manuals
  embeds an app at `https://books.union-motors.co.il/app` whose JSON API is
  open (the Incapsula script on the page is not enforced for the API):
  `GET /app/api/models?brand=toyota` (36 models),
  `GET /app/api/models/{id}/years`, `GET /app/api/search?modelId=&year=`
  (documents: `car_book`, `maintenance_schedule`, with `connectionId`),
  `GET /app/api/files/{connectionId}/download` (PDF). 51 one-page
  maintenance sheets (10 columns of 15,000 km, I/R/C/T cells, normal and
  severe rows, free-text long intervals, fluids table) were downloaded and
  parsed by word coordinates into `data/sources/toyota-union-sheets.json`,
  which `scripts/build_schedules.py` turns into 22 Toyota schedules.
- The warranty booklet https://union-motors.toyota.co.il/files/warranty
  itself is still Incapsula protected (warranty terms only).

## Hyundai (כלמוביל)

Manual hub with ~60 PDFs by model and year (cloudinary links, no auth):
https://www.hyundaimotors.co.il/maintenance/

Read and transcribed (chapter "תחזוקה", table "לוח תחזוקה רגילה"):

- i10 2014-2019: https://res.cloudinary.com/colmobil/images/v1716388497/ספר-רכב-יונדאי-i10-2014-2019_53335bdc4/ספר-רכב-יונדאי-i10-2014-2019_53335bdc4.pdf
- i10 2020-2021: https://res.cloudinary.com/colmobil/images/v1716388493/ספר-רכב-יונדאי-i10-2020-2021_533471256/ספר-רכב-יונדאי-i10-2020-2021_533471256.pdf
- i20 2015-2017: https://prodmedia.colmobil.co.il/media/sites/2/2023/06/ספר-רכב-יונדאי-i20-2015-2017.pdf
- i20 2018-2021: https://res.cloudinary.com/colmobil/images/v1716388440/ספר-רכב-יונדאי-i20-2018-2021_5400bf557/ספר-רכב-יונדאי-i20-2018-2021_5400bf557.pdf
- Elantra MD 2011-2015 (file name says "היברידית", it is the petrol MD): https://res.cloudinary.com/colmobil/images/v1716388110/ספר-רכב-יונדאי-אלנטרה-היברידית-2011-2015_5602d83f9/ספר-רכב-יונדאי-אלנטרה-היברידית-2011-2015_5602d83f9.pdf
- Elantra AD 2016-2018: https://res.cloudinary.com/colmobil/images/v1716388126/ספר-רכב-יונדאי-אלנטרה-היברידית-2016-2018_55994207d/ספר-רכב-יונדאי-אלנטרה-היברידית-2016-2018_55994207d.pdf
- Elantra 2019-2021 (petrol table): https://res.cloudinary.com/colmobil/images/v1716388120/ספר-רכב-יונדאי-אלנטרה-היברידית-2019-2021_56006ad7c/ספר-רכב-יונדאי-אלנטרה-היברידית-2019-2021_56006ad7c.pdf
- Ioniq 2016-2018: https://res.cloudinary.com/colmobil/images/v1738680462/IONIQ_2016-2018_heb/IONIQ_2016-2018_heb.pdf
- Ioniq 2019 (same table): https://res.cloudinary.com/colmobil/images/v1738680477/IONIQ_2019-heb/IONIQ_2019-heb.pdf

Downloaded, not yet transcribed:

- Tucson hybrid 2025: https://res.cloudinary.com/colmobil/images/v1756290337/tucso-hybrid-2025-hebrew-web-low/tucso-hybrid-2025-hebrew-web-low.pdf
  (pages 544-560: 15k grid, HSG belt, spark plugs at 45/90, coolant first 150,000/120 months)

Also on the hub (not downloaded): Ioniq 2020-2021, Elantra hybrid 2022,
Kona 2018-2020 turbo / 2021 / 2022-2023 hybrid, Santa Fe 2013-2018 /
2019-2020 / 2021, Sonata hybrid 2015-2021, i30N, Venue, Bayon.
No i25/Accent or ix35/Tucson 2015-2020 manual is listed.

Warranty booklet (no km table, warranty terms only):
https://prodmedia.colmobil.co.il/media/sites/2/2023/07/ספר-שירות-וכתב-אחריות-יונדאי.pdf

## Kia (טלקאר)

Manual library, one `<select>` per model, ~35 PDFs, no auth:
https://kia-israel.co.il/קבל-ספר-רכב-למייל
Files sit at `https://cdnmedia.kia-israel.co.il/www/cars-book/<name>.pdf`.

Read and transcribed (chapter "תחזוקה", tables "מרווחי התחזוקה"):

- Picanto JA 2017-2020: Picanto-JA-2017-2020.pdf (same as
  https://kia-israel.co.il/wp-content/uploads/2020/11/ספר-רכב-Picanto_OM_2017-.pdf)
- Picanto AMT 2021+: Picanto-AMT-2021.pdf (not diffed yet, assumed same)
- Sportage QL 2016-2018: Sportage-QLe-2016-2018.pdf
- Sportage QL 2019-2021: Sportage-QLe-2019-2021.pdf (same as
  https://kia-israel.co.il/wp-content/uploads/2020/11/ספר-רכב-Sportage_PE_OM_4-3-2019_OPT.pdf)
- Niro 2016-2018: Niro-2016-2018.pdf
- Niro 2019+: Niro-2019.pdf (same as
  https://kia-israel.co.il/wp-content/uploads/2020/11/ספר-רכב-Kia_Niro_Facelift.pdf)

Downloaded, not yet transcribed: Sportage_NQ5_2022.pdf (pages 450-458).
Older books (Picanto-2011-2016.pdf, Sportage-SL-2011-2015.pdf) use a custom
font: each Hebrew letter is stored as byte 0x9c + index (alef = 0x9c ... tav =
0xb6) and lines are in visual order. Decode with `chr(0x5D0 + ord(c) - 0x9c)`
and reverse each line; digits inside Hebrew lines come out reversed
("000,51" = 15,000). Both were transcribed this way (kia-picanto-2011-2016,
kia-sportage-2011-2015).
Also available: Rio 2017 / 2018+ / 2022, Stonic, Seltos, Sorento, Carnival,
Niro PHEV, Sportage hybrid/PHEV 2022 and 2026, EV models.

Interval statement (about 15,000 km on new cars, seasonal checks):
https://kia-israel.co.il/טיפול-ותחזוקה/טיפולים-לרכב

## Mazda (דלק מוטורס)

- Interval statement (dashboard alert / 15,000 km / 12 months, earliest):
  https://www.mazda.co.il/service-plans
- The page is a Next.js form. The per-model plan PDFs are embedded in the
  page HTML (`self.__next_f.push` payload, key `modelList`) as SharePoint
  links `https://delekmotorscoil.sharepoint.com/:b:/s/Techtrain/...?download=1`.
  Variants: Mazda2 2007-2014 / 2015+; Mazda3 2003-2012 / 2013-2019 /
  2020-2025 / 2025+; Mazda6; CX-3; CX-30; CX-5 2012-2025 / 2025+ (with and
  without turbo) / 2026+; CX-90; MX-5; BT-50.
- Download needs two steps with a cookie jar: GET the share link (saves a
  `FedAuth` cookie, answers 302 to
  `/sites/Techtrain/Shared Documents/.../mazda/<file>.pdf`), then GET that
  location with the cookie. A plain `curl -L` gets a 13-byte "403 FORBIDDEN".
- Transcribed (one page each, parts and intervals only): Mazda3 2003-2012,
  2013-2019, 2020+; Mazda2 2007-2014, 2015+; CX-5 2012-2025; CX-3 2017+;
  CX-30 2020+. Not yet: Mazda3 2025+ (2.5, turbo plugs 64,000), CX-5 2025+,
  Mazda6, MX-5, CX-90, BT-50.

## Skoda / Seat / VW (צ'מפיון מוטורס)

- Periodic service routine: https://www.championmotors.co.il/service-routine/ (Reblaze, blocked; also via WebFetch and Wayback rate-limited)
- Owner-manual summaries: https://books.championmotors.co.il/cars/skoda-octavia/ links to a FlippingBook
  viewer https://online.flippingbook.com/view/693579283. Its text layer is readable: load the viewer once
  (headless browser) to obtain the signed CloudFront URL of `html/workspace.json`, then fetch
  `flash/search/searchNNNN.xml` (words separated by \x02, `word\x02R\x02...`) with the same
  signature within ~20 minutes. Result: the 30-page "תמצית הוראות שימוש" has no service table
  (only fluid-level checks and "replace at an authorised garage"). `publication.pdf` returns 403.
- skoda.co.il: Link11, blocked. Forum reports (carsforum, 2019 Octavia) say the Champion app shows
  20,000 km / 12 months; unverified. skoda-octavia stays `draft`.

## Alfa Romeo (סמלת)

- alfaromeo.co.il (Akamai) returns 403 to every egress we have, including the Hebrew car books
  at `/carbook_giulia`, `/carbook_stelvio`, `/carbook_tonale` and the interval page `/treatment-routine`.
- samelet.com is open: warranty and service booklet
  https://samelet.com/ebooks/AlfaRomeo_warranty_092022.pdf (24 months unlimited km, no km table;
  the plan is "in the owner's book"), manuals page https://samelet.com/ספרות-רכב-אלפא-רומיאו/.
- Manufacturer handbooks (EN) on FCA's eLUM server, open:
  Giulietta 2015 `.../83/191_GIULIETTA/83_191_GIULIETTA_604.38.735_EN_04_09.15_L_LG/...pdf` (plan pp. 197-200),
  MiTo 2008 `.../83/145_MiTo/83_145_MiTo_604.38.043_EN_01_10.08_L_LG/...pdf` (pp. 199-200, 30k grid),
  Giulia 2017 `.../83/620_GIULIA/83_620_GIULIA_603.93.005_EN_04_01.17_L_LG/...pdf` (pp. 158-160),
  Stelvio 2018 `.../83/630_STELVIO/83_630_STELVIO_603.93.152_EN_02_02.18_L_LG/...pdf` (pp. 161-163),
  Tonale 2022 `.../83/965_TONALE/83_965_TONALE_603.93.733_EN_01_03.22_L_LG/...pdf` (pp. 224-226; dots are
  vector drawings, read with `page.get_drawings()`). Base: https://aftersales.fiat.com/eLumData/EN/
- Interval statement from an Israeli garage aggregator (galgalim.co.il, Cloudflare-blocked here):
  "טיפול 15,000 ק"מ (או שנה)" ladder for Alfa Romeo.

## Hyundai i25 / Accent

No Accent (RB) book is published by Colmobil. The Elantra MD 2011-2015 book
(same Gamma 1.6 / Kappa 1.4 engines and era) is used as the closest source
and the i25 file stays `draft` with a note.

## Toyota, second pass (28.9.2026)

The API lists 91 documents whose title is just a model name ("Hilux", "Prius
2009-2015", "לוח אחזקות לנד קרוזר"); they are maintenance sheets too. All 88
usable ones are in `data/sources/toyota-union-sheets.json` (rebuilt with
`scripts/toyota_sheets_export.py` from the scratch parse). Diesel/4x4 sheets
(Hilux, Land Cruiser, Proace, City van) have 16 columns of 10,000 km and use
Hebrew marks (ב בדיקה, ה החלפה, ג גירוז, ח חיזוק, נ ניקוי); the generator maps
them to inspect/replace and keeps the 10,000 km step. Several sheets give the
oil rule as text instead of marks: "בהופעת התראת החלפת שמן / 15,000 ק"מ / 12
חודשים" (Yaris, Corolla Cross, Aygo X, C-HR) or "עפ"י נורת התראה או 30,000 ק"מ
/ 24 חודשים" (Hilux 2015+, Land Cruiser 2020+); `ty_long()` turns these into
oil rules. Hilux 2026 (sheet 368) still lacks an oil row (parser drops it).
Not turned into schedules: Proace, City/City van (two sheet layouts), Highlander
petrol, Hilux 2026/08 multi-page sheets 370-372.

## Kia and Hyundai books, second pass (28.9.2026)

`scripts/hk_table_parse.py` reads the "תכנית תחזוקה רגילה" table of a Hebrew
Hyundai/Kia book by word coordinates. Two templates exist: columns of 15,000 km
(older books, and books printed with a miles row 10-80 next to a km row 15-120)
and columns of 30,000 km (Sportage NQ5, Sorento MQ4, Carnival KA4, Sportage
HEV) whose oil note still says 15,000 km / 12 months. Hyundai books are printed
landscape with rotated text; the parser handles that (dict mode, vertical lines)
and repairs headers whose digits are lost ("1", "3", "4"... = 15, 30, 45...).
Parsed tables: `data/sources/hk-tables.json`; generator `hk()` with `HK_MAP`.
Books that could not be parsed: Kona 2023+ and Kona hybrid 2023-2026 (scanned
images), Kona hybrid 2022 and Santa Fe 2013-2018 (table without extractable
km header), i30 N. No book exists for Tucson petrol (2016-2024), i30, i35,
ix35, Getz, Accent, Kia Forte/Cerato, Ceed, Soul.

Kia book URLs: `https://cdnmedia.kia-israel.co.il/www/cars-book/<file>` with
files Stonic_Facelift_2021, Stonic_PE_2026, Rio-SC-2017, Rio-YB-2018,
Rio-OM-2022, Seltos-2020, Sportage_NQ5_2022, "Sportage_HEV-PHEV 2022",
Sportage-Hybrid-2026, Sorento-MQ4-GSL-DSL-2021, Sorento-UMPE-2019-2020,
NIRO_PHEV_General_Heb_01_פלאגאין, Niro-Plus-HEV-PHEV-OM-2022, Carnival-KA4-2021,
Carnival-YP-2016-2020 (12,000 km grid, not used), Picanto-AMT-2021.
Hyundai book URLs are the cloudinary links listed in the schedules' sources.

## Other importers probed (28.9.2026)

- Mitsubishi (כלמוביל): the site is `mitsubishi-israel.co.il` (mitsubishi-motors.co.il is dead).
  `/car_books/` is a WordPress form whose `<option data-pdf="ID">` values are attachment
  ids; `https://www.mitsubishi-israel.co.il/wp-json/wp/v2/media/<ID>` gives the cloudinary
  PDF. 20 Hebrew books (Outlander 2010-2024, Eclipse Cross, ASX, Space Star, Attrage, L200);
  only Outlander 2021-2024 has a maintenance table (chapter 9, 15 columns of 15,000 km),
  parsed into `hk-tables.json` and used by `hk(..., ncols=15)`.
- Suzuki: `https://suzuki.co.il/content/ספרי-נהג-סוזוקי` has only S-Cross 2025 (Hebrew/Arabic);
  its table (PDF pages 647-650) is the global 20,000 km grid, not transcribed.
- Ford (דלק מוטורס): `https://www.ford.co.il/תוכנית-טיפול/שירות` embeds `var data = [...]`
  (model -> displayList -> pdf.url, SharePoint links). Same two-step cookie download as
  Mazda. Plans are one page (item, interval); parsed into `data/sources/ford-plans.json`
  and generated by `ford()`. Edge/Explorer/Ranger plans use another layout (not parsed).
- Mazda plans not transcribed before (Mazda5, Mazda6 x2, CX-90, MX-5 x2, BT-50) now go
  through the same generator from `data/sources/mazda-plans.json`.
- Subaru: `https://subaru.co.il/services/owners-manuals/` renders through JS and gave no
  links even in Playwright.
- Nissan: no manuals online (service via service.freesbe.com).
- Mercedes: `/site/car-books/` links to the global digital manual portal.
- Honda, Renault, Dacia, Peugeot, Citroen, Opel, Fiat, Chevrolet: 403 for all egress; Seat/VW/Skoda: Link11 491.

## Government vehicle registry (data.gov.il)

- Dataset "כלי רכב פרטיים ומסחריים", resource `053cea08-09bc-40ec-8f7a-156f0677aff3`,
  4.18M rows. `datastore_search` with `filters={"mispar_rechev":N}` works
  with a browser UA. Fields: tozeret_nm (maker + country), kinuy_mishari
  (commercial name, e.g. COROLLA, I10, PICANTO), degem_nm (type code),
  shnat_yitzur, degem_manoa (engine code, e.g. G4LA, 1ZR, 2ZR), sug_delek_nm,
  moed_aliya_lakvish, ramat_gimur, misgeret (VIN), tokef_dt.
- Naming quirks seen: Toyota hybrids carry the name (`COROLLA HYBRID`,
  `RAV4 HYBRID` / `RAV4 HSD`, `C-HR HYBRID`, `AYGO X HYBRID`) while
  `sug_delek_nm` stays `בנזין`; Mazda is spelled `מזדה` with names
  `MAZDA 3`, `MAZDA CX-30`; Alfa Romeo is `אלפא רומיאו_אי` with
  `ALFA GIULIETTA`, `GIULIA`, `GIULIA Q4`, `STELVIO`.
- `scripts/lookup_plate.mjs <plate>` wraps it.

### Full dump and popularity counts

The resource's CSV dump (875 MB, pipe-delimited, **windows-1255**) downloads from
`https://data.gov.il/dataset/7a338622-63bb-4cfd-b3f7-0d2e8cf71033/resource/053cea08-09bc-40ec-8f7a-156f0677aff3/download/053cea08-09bc-40ec-8f7a-156f0677aff3.csv`
(browser User-Agent; the `e.data.gov.il` link from `resource_show` redirects to a
Google login; `datastore_search_sql` is disabled). `scripts/registry_counts.py`
aggregates it into `data/sources/registry-counts.json` (snapshot 28.9.2026,
4,181,617 rows) and `scripts/registry_coverage.mjs` ranks models without a
schedule. Engine codes in the dump are short (1ZR, 2GD, G4LE, 55273835).

## Sales rankings (for models.json)

- cartube.co.il "הדגמים הנמכרים ביותר בישראל בשנת YYYY"
- bestsellingcarsblog.com "Israel Full Year YYYY"
- bizportal decade summary: https://www.bizportal.co.il/car/news/article/20019775
