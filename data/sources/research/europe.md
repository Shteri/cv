# Group "europe": report

87 schedule files plus `registry_rules.json` (89 rules). 7 files are `reviewed` (taken straight from an Israeli importer book) and 80 are `draft`.
Generator scripts (they hold every transcribed number) are in `scratchpad/dl/europe/{gen,psa,fca,gm,renault,main}.py`; downloads are in `scratchpad/dl/europe/`.
Validation: `node scripts/validate.mjs staging/europe` fails only because `registry_rules.json` sits in the same folder (the validator reads every *.json file as a schedule). Without that file (`dl/europe/val.sh` copies the schedules to a temp folder) the output is: "all schedules valid (80 draft, 7 reviewed)".

## Sources found (by importer)

### Samelet (Fiat / Jeep / Chrysler): Israeli Hebrew books are open through the WordPress media API
`https://samelet.com/wp-json/wp/v2/media?mime_type=application/pdf&per_page=100&page=N` lists 219 PDFs.
- Fiat 500 1.2 8V: `wp-content/uploads/2023/11/Fiat_500_500C_carbook_042021-1.pdf`, printed pp. 118-120 → fiat-500-2008-2021-1.2 (**reviewed**). Fiat Panda 1.2 uses the same plan (sister model, **draft**; only a new-Panda quick guide exists).
- Fiat Tipo 1.6 E.torQ (engine code 55268036, p. 155): `2023/11/Tipo-hebrew-4P-low.pdf`, pp. 129-131 → **reviewed**.
- Fiat 500X 1.4 MultiAir (55263624): `2023/11/Fiat-500X.pdf`, pp. 158-160 → **reviewed**. The Jeep Renegade 1.4 MultiAir file and the Compass 2017-2020 1.4 MultiAir file (55263623) use the same plan (**draft**).
- Fiat Doblo K9 1.5 diesel (YH01): `2024/02/Fiat_Doblo_carbook_062026.pdf`, pp. 252-254 → **reviewed**. This book is also the Israeli sister source for every PSA car with the DV5 1.5 BlueHDi engine (see below).
- Jeep Compass 1.3 T4 (55282328): `2023/11/Jeep_Compass_carbook_042021.pdf`, pp. 211-213 → **reviewed**.
- Jeep Compass 2026 with the EB2T 1.2 MHEV engine: `2023/11/260345-Jeep-Compass-OM-2026-8-6-26-S2.pdf`, pp. 198-200 → **reviewed**. The same plan is used as a sister source (**draft**) for the new-generation Stellantis 1.2 engine (registry code HN09): Peugeot 3008 from 2024, 5008 from 2025, 208 and 2008 from 2025, C3 and C3 Aircross from 2025, Opel Frontera, Opel Corsa from 2025.
- Jeep Wrangler JL 2.0 turbo: `2023/11/Jeep_Wrangler_2022_-carbook_072022.pdf`, pp. 391-394, grid of 12,000 km → **reviewed**.
- Not done: Grand Cherokee. The 2023 Hebrew book (pp. 290-291) has two conflicting grids, 16,000 km and 12,000 km, and it covers the WL generation, while most registered cars are the 3.6 WK2. Also not done: Cherokee (pp. 219-223 exist but were not transcribed), Grand Voyager, Pacifica, Qubo, Punto, the old Doblo, and 500e/EV.
- The Samelet warranty booklets (Fiat, Jeep, Avenger) have no km table.

### Lubinski (Peugeot / Citroen / Opel / DS)
- The sites peugeot.co.il, citroen.co.il and opel.co.il return 403 (Akamai) to both curl and Playwright. The `online.<brand>.co.il` subdomains are open.
- Lubinski warranty booklets (`media-peugeot.lubit.co.il/.../Warranty-Peugeot-3Y-01.2024_Web-מונגש.pdf` and the 2026 editions) have no km table. They say the personal maintenance plan is handed over with the car.
- The "car books" (appendix and short guides) are listed through admin-ajax `get_clearmash_doc_url`, but every file on `lubinski.clearmash.com` is blocked by Cloudflare 403 (curl, Playwright and WebFetch all failed).
- Israeli interval: the Hebrew Opel Corsa F manual (`public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf`, p. 205) puts Israel in country group 4: 15,000 km or 1 year for the EB2 1.2 and DV5 1.5 engines. Hebrew Opel manuals for all models are open at `public-servicebox.opel.com/OVddb/OV/he_IL/index.html`. They give intervals only, not item grids.
- **DV5 1.5 BlueHDi (YH01)**: the grid comes from the Doblo Hebrew book, cross-checked with Union Motors' Toyota Proace City sheet (`books.union-motors.co.il/app/api/files/1190/download`, 15,000 km grid). The two sources disagree on the timing belt: Samelet says 120,000 km / 5 years, Toyota says 180,000 km / 10 years. The files use 120,000 km / 5 years and the note mentions the Toyota figure. Files: Berlingo K9, Partner/Rifter, Combo, 3008, 5008, 2008, C5 Aircross, C4 SpaceTourer, C4/C4X, Grandland (all **draft**).
- **1.2 PureTech turbo, older generation (HN01/HN02/HN05)**: the grid comes from the English Jeep Avenger handbook on eLUM (`aftersales.fiat.com/.../57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf`, pp. 213-217). It is laid on the Israeli 15,000 km interval. For the long items the files use the handbook's "outside Europe" values, as Samelet does in its Israeli Compass 2026 plan: plugs and air filter 20,000 km / 4 years, wet timing belt 90,000 km / 6 years then 180,000, coolant 160,000 km / 10 years. The European values are in the notes. Files: 3008, 5008, 2008, 208, 308, 408, C3, C3 Aircross, C4 Cactus, C4 Picasso/SpaceTourer, C4, C5 Aircross, Corsa F, Mokka B, Combo, Grandland, Crossland, Frontera, Avenger, DS3/DS4/DS7 (all **draft**).
- **2.0 BlueHDi (AH01)**: Citroen Jumpy 2016+ and Fiat Scudo use the Union Motors Toyota Proace 2017 sheet (`.../files/603/download`, 20,000 km grid, timing belt at 140,000 km / 10 years) (**draft**).
- Not done:
  - Berlingo/Partner B9 with the 1.6 HDi/BlueHDi (BH02, 9H06, 9HP, 9HW...), about 14k cars. No DV6 source was found. The Hebrew appendix books for C4 2013-2015, Jumpy 2012-2013 and C3 2018 exist only on the blocked clearmash host.
  - EP6 1.6 VTi/THP (5F01, 5FS, 5FW, 5G01, 5G06): C4 Picasso, 207, 308 I, 508, 3008 GT, C5 Aircross 1.6.
  - TU5/EC5 1.6 (NFP/NFU): 301, C-Elysee, 206/307.
  - Peugeot 107/108 and Citroen C1 (1KR). These can reuse the repo's `toyota-aygo-*` files as sisters, but no file was written.
  - GM-era Opel models (Corsa D/E, Astra J/K, Mokka X, Adam, Insignia, Meriva, Zafira). The Hebrew Opel manuals give only the interval: Corsa E is in the "international" group, 15,000 km / 1 year, while the Corsa D 2012 Hebrew manual lists Israel in the European group, 30,000 km / 1 year. An international item grid exists on manualslib (Corsa 2011, manual 504809, pp. 231-237) but was not transcribed.

### Chevrolet (UMI)
- chevrolet.co.il and umigroup.co.il return Cloudflare 403.
- Sources are the GM US/Canada owner's manuals from the `cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/<year>-<model>.pdf` mirror; chevrolet.com gave 403 for most years. Their "Additional Required Services - Normal" tables (12,000 km grid, km shown first) were parsed by word coordinates (`dl/europe/gm/gmparse.py`). Oil is changed by the oil-life monitor, at least once a year.
- Files (all **draft**): Spark M400 1.4 LV7 (2019 manual pp. 290-294), Trax 1.4T (2017 manual), Trax 1.8 (Cruze 2014 1.8 as sister), Trax 2023+ 1.2T LIH (2024 manual), Trailblazer 1.3T (2022 manual), Equinox 1.5T (2020 manual), Traverse 2018+ (2019 manual) and 2009-2017 (2016 manual), Malibu 1.5T/2.0T (2018 manual), Cruze J300 1.4T/1.6/1.8 (2014 manual; the 1.6 F16D4 follows the 1.8 rows), Cruze 2017-2019 (2018 manual), Impala (2016 manual), Blazer (2021 manual).
- Not done: Spark M300 (B10D1/B12D1, about 5k cars; manualslib only has an India Spark booklet), Aveo, Sonic, Orlando, Captiva, Optra, Camaro.

### Renault / Dacia (Carasso)
- renault.co.il and dacia.co.il are blocked by Incapsula 403, including in Playwright. No Israeli document was found.
- Renault owner manuals (user-manual.renault.com, which has Hebrew) have no maintenance table.
- Source used: Renault Australia's official page, https://www.renault.com.au/capped-price-servicing/ (open with curl):
  - Kangoo 1.5 diesel table (K9K), service every 15,000 km: filters every 30,000 km / 2 years; timing belt and accessory belt kits, coolant and brake fluid every 120,000 km / 4 years.
  - Kangoo 1.2 petrol table (H5F): plugs every 60,000 km / 4 years; accessory belt every 90,000 km / 4 years.
  - Kadjar/Arkana/Captur MY21+ table (H5H): 30,000 km / 12 months.
  - Trafic MY23 table: 2.0 diesel.
- These are applied by engine code (all **draft**):
  - K9K: Megane, Grand Coupe, Fluence, Duster, Kangoo, Kadjar, Clio, Captur, Grand Scenic, Sandero/Logan, Lodgy/Dokker.
  - H5F: Clio, Captur, Duster, Kangoo, Kadjar, Megane, Lodgy.
  - H5H: Arkana, Captur 2020+, Megane, Duster, Austral.
  - M9R: Trafic.
- The routine checks at each service (tires, lights, brakes, fluid levels, diagnostics) are not itemised on the Australian page. They are added as routine checks, and the notes say so.
- Not done: Sandero/Logan/Twingo/Clio with H4B/H4D/D4F, Clio III and Megane II K4M, Fluence H4M/M4R/K4M, Arkana/Duster/Jogger hybrids (H4M E-Tech), Koleos, Jogger, Bigster.

### Mercedes-Benz, BMW, Volvo: not done (session ended)
No files were written. Planned route: the global digital owner's manual portals, which describe condition-based service (ASSYST, CBS, Volvo service program) with fixed fallback intervals.

## Registry notes (please check lookup_plate.mjs MAKES)
- The registry spells these makes differently from MAKES:
  - "ב מ וו" (not "ב.מ.וו")
  - "וולבו" (MAKES has "וולוו")
  - "דאצ'יה" / "דאציה מרוקו" (MAKES has only "דאציה", which does not match "דאצ'יה")
  - "פיגו מרוקו" (no geresh)
- These makes are missing from MAKES: "ג'יפ" (Jeep), "קרייזלר" (Chrysler; it carries many Jeep Wrangler and Grand Cherokee cars), "די אס" (DS), "דיימלר קרייזלר".
- registry_rules.json uses the English makes Jeep, Chrysler, DS and Dacia; MAKES needs matching entries for those rules to work.
- Rules use engine codes wherever the registry has them: YH01, HN01/HN02/HN05 (older PureTech) vs HN09 (new 1.2), AH01, K9K, H5F, H5H, M9R, LV7, and others.
- Compass engine 46351268 (547 cars, 2021-2026) was not identified and is left unmatched. The PureTech HN09 code covers both the belt 100 hp engine and the mild-hybrid engine. The Avenger stays on its own handbook plan; the other HN09 cars use the MHEV plan.

## File list
| id | status | interval km | main source(s) |
|---|---|---|---|
| chevrolet-blazer-2019-2024-2.0-3.6 | draft | 12000 | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2021-blazer.pdf |
| chevrolet-cruze-2009-2016-1.4-1.6-1.8 | draft | 12000 | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2014-cruze.pdf |
| chevrolet-cruze-2017-2019-1.4-turbo | draft | 12000 | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2018-cruze.pdf |
| chevrolet-equinox-2018-2023-1.5-turbo | draft | 12000 | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2020-equinox.pdf |
| chevrolet-impala-2014-2020-3.6 | draft | 12000 | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2016-impala.pdf |
| chevrolet-malibu-2016-2023-1.5-2.0-turbo | draft | 12000 | https://www.chevrolet.com/ownercenter/content/dam/gmownercenter/gmna/dynamic/manuals/2018/Chevrolet/Malibu/2018-chevrolet-malibu-owners-manual.pdf |
| chevrolet-spark-2016-2022-1.4 | draft | 12000 | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2019-spark.pdf ; https://www.chevrolet.com/ownercenter/content/dam/gmownercenter/gmna/dynamic/manuals/2019/Chevrolet/Spark/2019-chevrolet-spark-owners-manual.pdf |
| chevrolet-trailblazer-2021-2026-1.3-turbo | draft | 12000 | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2022-trailblazer.pdf |
| chevrolet-traverse-2009-2017-3.6 | draft | 12000 | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2016-traverse.pdf |
| chevrolet-traverse-2018-2026-3.6 | draft | 12000 | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2019-traverse.pdf |
| chevrolet-trax-2013-2016-1.8 | draft | 12000 | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2014-cruze.pdf |
| chevrolet-trax-2013-2020-1.4-turbo | draft | 12000 | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2017-trax.pdf |
| chevrolet-trax-2023-2026-1.2-turbo | draft | 12000 | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2024-trax.pdf |
| citroen-berlingo-2018-2026-1.5-bluehdi | draft | 15000 | https://samelet.com/wp-content/uploads/2024/02/Fiat_Doblo_carbook_062026.pdf ; https://books.union-motors.co.il/app/api/files/1190/download |
| citroen-c3-2017-2026-1.2-puretech | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| citroen-c3-2025-2026-1.2-hybrid | draft | 15000 | https://samelet.com/wp-content/uploads/2023/11/260345-Jeep-Compass-OM-2026-8-6-26-S2.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| citroen-c3-aircross-2018-2026-1.2-puretech | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| citroen-c3-aircross-2025-2026-1.2-hybrid | draft | 15000 | https://samelet.com/wp-content/uploads/2023/11/260345-Jeep-Compass-OM-2026-8-6-26-S2.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| citroen-c4-2021-2026-1.2-puretech | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| citroen-c4-2021-2026-1.5-bluehdi | draft | 15000 | https://samelet.com/wp-content/uploads/2024/02/Fiat_Doblo_carbook_062026.pdf ; https://books.union-motors.co.il/app/api/files/1190/download |
| citroen-c4-cactus-2015-2020-1.2-puretech | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| citroen-c4-spacetourer-2014-2022-1.2-puretech | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| citroen-c4-spacetourer-2018-2022-1.5-bluehdi | draft | 15000 | https://samelet.com/wp-content/uploads/2024/02/Fiat_Doblo_carbook_062026.pdf ; https://books.union-motors.co.il/app/api/files/1190/download |
| citroen-c5-aircross-2019-2026-1.2-puretech | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| citroen-c5-aircross-2019-2026-1.5-bluehdi | draft | 15000 | https://samelet.com/wp-content/uploads/2024/02/Fiat_Doblo_carbook_062026.pdf ; https://books.union-motors.co.il/app/api/files/1190/download |
| citroen-jumpy-2016-2026-2.0-bluehdi | draft | 20000 | https://books.union-motors.co.il/app/api/files/603/download ; https://media-peugeot.lubit.co.il/wp-content/uploads/2023/06/Warranty-Peugeot-3Y-01.2024_Web-%D7%9E%D7%95%D7%A0%D7%92%D7%A9.pdf |
| dacia-duster-2012-2024-1.5-dci | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| dacia-duster-2015-2020-1.2-tce | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| dacia-duster-2019-2026-1.3-tce | draft | 30000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| dacia-lodgy-2013-2019-1.2-tce | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| dacia-lodgy-dokker-2013-2022-1.5-dci | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| dacia-sandero-logan-2013-2021-1.5-dci | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| ds-ds3-ds4-ds7-2019-2026-1.2-puretech | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| fiat-500-2008-2021-1.2 | reviewed | 15000 | https://samelet.com/wp-content/uploads/2023/11/Fiat_500_500C_carbook_042021-1.pdf |
| fiat-500x-2015-2019-1.4-multiair | reviewed | 15000 | https://samelet.com/wp-content/uploads/2023/11/Fiat-500X.pdf |
| fiat-doblo-2023-2026-1.5-diesel | reviewed | 15000 | https://samelet.com/wp-content/uploads/2024/02/Fiat_Doblo_carbook_062026.pdf |
| fiat-panda-2011-2017-1.2 | draft | 15000 | https://samelet.com/wp-content/uploads/2023/11/Fiat_500_500C_carbook_042021-1.pdf ; https://samelet.com/wp-content/uploads/2023/11/260617-QuickGuide-Fiat-Panda-Heb-AR-S3-SH.pdf |
| fiat-scudo-2023-2026-2.0-diesel | draft | 20000 | https://books.union-motors.co.il/app/api/files/603/download ; https://media-peugeot.lubit.co.il/wp-content/uploads/2023/06/Warranty-Peugeot-3Y-01.2024_Web-%D7%9E%D7%95%D7%A0%D7%92%D7%A9.pdf |
| fiat-tipo-2016-2020-1.6 | reviewed | 15000 | https://samelet.com/wp-content/uploads/2023/11/Tipo-hebrew-4P-low.pdf |
| jeep-avenger-2023-2026-1.2 | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://samelet.com/wp-content/uploads/2023/11/AVENGER-HOVERET-2026-WEB.pdf |
| jeep-compass-2018-2020-1.4-multiair | draft | 15000 | https://samelet.com/wp-content/uploads/2023/11/Fiat-500X.pdf ; https://samelet.com/wp-content/uploads/2023/11/Jeep_renegede_shortguide_151020.pdf |
| jeep-compass-2021-2024-1.3-turbo | reviewed | 15000 | https://samelet.com/wp-content/uploads/2023/11/Jeep_Compass_carbook_042021.pdf |
| jeep-compass-2025-2026-1.2-mhev | reviewed | 15000 | https://samelet.com/wp-content/uploads/2023/11/260345-Jeep-Compass-OM-2026-8-6-26-S2.pdf |
| jeep-renegade-2015-2019-1.4-multiair | draft | 15000 | https://samelet.com/wp-content/uploads/2023/11/Fiat-500X.pdf ; https://samelet.com/wp-content/uploads/2023/11/Jeep_renegede_shortguide_151020.pdf |
| jeep-wrangler-2018-2026-2.0-turbo | reviewed | 12000 | https://samelet.com/wp-content/uploads/2023/11/Jeep_Wrangler_2022_-carbook_072022.pdf |
| opel-combo-2019-2026-1.2 | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| opel-combo-2019-2026-1.5-diesel | draft | 15000 | https://samelet.com/wp-content/uploads/2024/02/Fiat_Doblo_carbook_062026.pdf ; https://books.union-motors.co.il/app/api/files/1190/download |
| opel-corsa-2020-2026-1.2 | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| opel-corsa-2025-2026-1.2-hybrid | draft | 15000 | https://samelet.com/wp-content/uploads/2023/11/260345-Jeep-Compass-OM-2026-8-6-26-S2.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| opel-crossland-2018-2024-1.2 | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| opel-frontera-2025-2026-1.2-hybrid | draft | 15000 | https://samelet.com/wp-content/uploads/2023/11/260345-Jeep-Compass-OM-2026-8-6-26-S2.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| opel-frontera-2025-2026-1.2 | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| opel-grandland-2018-2025-1.5-diesel | draft | 15000 | https://samelet.com/wp-content/uploads/2024/02/Fiat_Doblo_carbook_062026.pdf ; https://books.union-motors.co.il/app/api/files/1190/download |
| opel-grandland-2018-2026-1.2 | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| opel-mokka-2021-2026-1.2 | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| peugeot-2008-2014-2026-1.2-puretech | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| peugeot-2008-2020-2026-1.5-bluehdi | draft | 15000 | https://samelet.com/wp-content/uploads/2024/02/Fiat_Doblo_carbook_062026.pdf ; https://books.union-motors.co.il/app/api/files/1190/download |
| peugeot-2008-2025-2026-1.2-hybrid | draft | 15000 | https://samelet.com/wp-content/uploads/2023/11/260345-Jeep-Compass-OM-2026-8-6-26-S2.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| peugeot-208-2013-2026-1.2-puretech | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| peugeot-208-2025-2026-1.2-hybrid | draft | 15000 | https://samelet.com/wp-content/uploads/2023/11/260345-Jeep-Compass-OM-2026-8-6-26-S2.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| peugeot-3008-2017-2025-1.2-puretech | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| peugeot-3008-2017-2025-1.5-bluehdi | draft | 15000 | https://samelet.com/wp-content/uploads/2024/02/Fiat_Doblo_carbook_062026.pdf ; https://books.union-motors.co.il/app/api/files/1190/download |
| peugeot-3008-2024-2026-1.2-hybrid | draft | 15000 | https://samelet.com/wp-content/uploads/2023/11/260345-Jeep-Compass-OM-2026-8-6-26-S2.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| peugeot-308-2014-2021-1.2-puretech | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| peugeot-408-2023-2026-1.2-puretech | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| peugeot-5008-2018-2025-1.2-puretech | draft | 15000 | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| peugeot-5008-2018-2025-1.5-bluehdi | draft | 15000 | https://samelet.com/wp-content/uploads/2024/02/Fiat_Doblo_carbook_062026.pdf ; https://books.union-motors.co.il/app/api/files/1190/download |
| peugeot-5008-2025-2026-1.2-hybrid | draft | 15000 | https://samelet.com/wp-content/uploads/2023/11/260345-Jeep-Compass-OM-2026-8-6-26-S2.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf |
| peugeot-partner-rifter-2019-2026-1.5-bluehdi | draft | 15000 | https://samelet.com/wp-content/uploads/2024/02/Fiat_Doblo_carbook_062026.pdf ; https://books.union-motors.co.il/app/api/files/1190/download |
| renault-arkana-2022-2026-1.3-tce | draft | 30000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-austral-2023-2026-1.3-tce | draft | 30000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-captur-2013-2019-1.2-tce | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-captur-2014-2019-1.5-dci | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-captur-2020-2026-1.3-tce | draft | 30000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-clio-2013-2019-1.5-dci | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-clio-2013-2020-1.2-tce | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-fluence-2010-2017-1.5-dci | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-grand-scenic-2013-2021-1.5-dci | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-kadjar-2016-2019-1.2-tce | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-kadjar-2016-2021-1.5-dci | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-kangoo-2008-2021-1.5-dci | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-kangoo-2013-2021-1.2-tce | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-megane-2010-2024-1.5-dci | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-megane-2016-2019-1.2-tce | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-megane-2019-2024-1.3-tce | draft | 30000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-megane-grand-coupe-2017-2019-1.5-dci | draft | 15000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| renault-trafic-2015-2026-2.0-dci | draft | 30000 | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |