# hyundai-kia group report
Validation: the 9 schedule JSONs pass validate.mjs (5 draft, 4 reviewed). validate.mjs on the whole dir also parses registry_rules.json as a schedule and reports errors for it; the rules file is valid JSON.
Builder scripts: scratchpad/dl/hyundai-kia/gen.py + specs/*.py

## Done
- hyundai-tucson-2015-2020-1.6-2.0 (TL) - reviewed - Colmobil Hebrew Tucson 2016 book via mirror https://www.manualpdf.co.il/hyundai/tucson-2016/מדריך?p=544 (p544-549 = book 7-11..7-16). Columns rebuilt from text coordinates + background grid. Fuel-tank air filter / fuel lines rows: only the mark count (4/8) is known, so I assumed 30/60/90/120. The book marks brake fluid R in every column. Diesel rows omitted.
- hyundai-tucson-2021-2026-1.6t-2.0 (NX4) - reviewed - https://prodmedia.colmobil.co.il/media/sites/2/2023/06/יודאי-טוסון-ספר-רכב.pdf PDF p475-478 (2021 edition; no facelift book found).
- hyundai-kona-2020-2022-1.6-hybrid - reviewed - Colmobil Kona Hybrid 2022 book (cloudinary v1716384065), scanned p477-480.
- hyundai-kona-2023-2026-1.6-hybrid - reviewed - Colmobil Kona Hybrid 2023 book p544-545; the 2026 book p553-554 has the same table.
- hyundai-i30-2008-2011-1.6 (FD) - draft - manualslib 1231781 p326-330, "except Europe" column (cross-checked with manualslib 623622 p282-286).
- hyundai-i30-2012-2016-1.6 (GD) - draft - manualpdf.co.il/hyundai/i30-2014 p398-406, list schedule "except Europe". This book gives GDI / Middle East oil every 10,000 km; stated in the note.
- hyundai-i20-2009-2014-1.25-1.4 (PB) - draft - manualpdf.co.il/hyundai/i20-2011 p319-322, except Europe. Vapour hose placed at 60/120 (count only). Local hy-i20-x.pdf is actually the i20 GB 2015+ book.
- kia-forte-2014-2018-1.6 (YD/Cerato) - draft - manualslib 1996633 p532-538, except-Europe values.
- kia-ceed-2012-2018-1.6 (JD) - draft - kceed.com normal_maintenance_schedule_except_europe-640.html (3 page images).

## Blocked / not done
- No Israeli PDF for Tucson TL / i30 / ix35 / Accent / Getz: about 160 guessed prodmedia.colmobil names (only i10/i20 exist); hyundaimotors.co.il WP API 308 then 500; api.colmobil.co.il 502 from the proxy; xn----2hc3awpyb.com Cloudflare 403 (Playwright too); esfarim.co.il no connection.
- Forte TD 2009-2013: only US 12,000 km and Latin-American 8,000 km schedules found, so no file.
- Not started (time): Accent MC (carmanualsonline accent-2009 rhd-uk-australia), Accent India 2019-23 (manualslib 1958374 p358), ix35 (manualslib 623630 p340), Rio JB/UB, Niro HEV SG2, Niro PHEV 2020-22, Getz (manualslib 752940), i10 PA (manualslib 623636), Santa Fe 2007-18 (local hy-santafe-2013-2018.pdf p408-418), Sorento XM, Ioniq5/6, Kona EV, Carnival YP (local p492-495), Soul, XCeed, Carens, H1 (manualslib 739089 p263), Veloster, Staria, Tucson JM, Ceed ED/CD, i30 PD.
- Tools: manualslib renders cleanly with Playwright element screenshots (dl/hyundai-kia/mlshot.mjs). carmanualsonline page PNGs are at /img/2/<docid>/w960_<docid>-<page>.png (send a Referer). manualpdf.co.il gives the text layer, but runs of marks packed together lose their column positions.
