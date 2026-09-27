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
- Warranty and maintenance booklet (the per-km table): the page
  https://www.toyota.co.il/owners/warranty links to
  https://union-motors.toyota.co.il/files/warranty, which is Incapsula
  protected. Not yet read. Toyota files stay `draft` until it is.

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
Text not extractable (custom font): Picanto-2011-2016.pdf, Sportage-SL-2011-2015.pdf.
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
  without turbo) / 2026+; CX-90; MX-5; BT-50. Index saved during the
  session; see HANDOFF for status.

## Skoda / Seat / VW (צ'מפיון מוטורס)

- Periodic service routine: https://www.championmotors.co.il/service-routine/ (Reblaze, blocked)
- Owner-manual summaries: https://books.championmotors.co.il/cars/skoda-octavia/ (reachable) links to a
  FlippingBook viewer https://online.flippingbook.com/view/693579283 (JS viewer, no PDF link found).
- skoda.co.il: Link11, blocked.

## Government vehicle registry (data.gov.il)

- Dataset "כלי רכב פרטיים ומסחריים", resource `053cea08-09bc-40ec-8f7a-156f0677aff3`,
  4.18M rows. `datastore_search` with `filters={"mispar_rechev":N}` works
  with a browser UA. Fields: tozeret_nm (maker + country), kinuy_mishari
  (commercial name, e.g. COROLLA, I10, PICANTO), degem_nm (type code),
  shnat_yitzur, degem_manoa (engine code, e.g. G4LA, 1ZR, 2ZR), sug_delek_nm,
  moed_aliya_lakvish, ramat_gimur, misgeret (VIN), tokef_dt.
- `scripts/lookup_plate.mjs <plate>` wraps it.

## Sales rankings (for models.json)

- cartube.co.il "הדגמים הנמכרים ביותר בישראל בשנת YYYY"
- bestsellingcarsblog.com "Israel Full Year YYYY"
- bizportal decade summary: https://www.bizportal.co.il/car/news/article/20019775
