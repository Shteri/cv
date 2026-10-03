# Group "eu3": report (round 3)

31 schedule files (20 draft, 11 reviewed) plus `registry/registry_rules.json` (42 rules: 38 for the new files, 4 registry-only rules that point at files already in the repo).
Validation: `node scripts/validate.mjs staging/eu3` prints "all schedules valid (20 draft, 11 reviewed, 0 verified)".
Generator scripts (they hold every transcribed number): `scratchpad/dl/eu3/gen/{gen,psa,chevy,fca,ford,fiat,copies,main}.py` (run `python3 main.py`). Downloads: `scratchpad/dl/eu3/`.
Coverage check: `scratchpad/dl/eu3/gain.mjs` replays the registry counts against `registry_map.json` + all staging rules. The new rules match **about 68,600 registered vehicles that no rule matched before**. None of them changes a match that an existing rule already makes.

## Main new sources

### PSA (Peugeot / Citroen): official Peugeot France "PLAN D'ENTRETIEN" sheets
- Peugeot's dealer system prints a one-page plan for each engine, with a "normal" column and a "severe conditions" column. Owners uploaded these sheets to forum-peugeot.com. The thread pages are behind Cloudflare, but the `wp-content/uploads` PDFs open with curl. These are manufacturer documents, so status is **draft** with the market (France) named in the notes.
  - DV6 1.6 HDi / BlueHDi: `2016/08/planentretien3081.6hdi92.pdf`, `2016/08/planentretien3081.6hdi115.pdf`, `2016/09/planentretien3008hdi100.pdf`, `2016/09/planentretien3008bluehdi120eat.pdf`, `2016/08/planentretien308bluehdi100.pdf`.
  - EP6 1.6 THP: `2016/09/planentretien3008thp165.pdf`, `2016/07/planentretien5008thp165.pdf`, `2016/08/planentretien1.6thp165.pdf`, `2016/10/planentretien508thp165bvm6.pdf`, `2017/03/planentretien5008thp165eat6.pdf`, `2016/08/planentretien3081.6thp155.pdf`.
  - EB2F 1.2 VTi/PureTech 82 without turbo: `2019/05/planentretien208puretech82.pdf` (newest), `2016/06/planentretien1.2PureTech82BVM5.pdf`.
- The list of operations done at every service, and the definition of severe conditions, come from the Peugeot "Carnet d'entretien et de garanties" 03-2014 (https://www.autojm.fr/pdf/notices/PEUGEOT/carnet-entretien-peugeot.pdf, printed pp. 11-12 = PDF 13-14). Severe conditions include a prolonged stay in a dusty country, so the files use the **severe column**:
  - DV6: 15,000 km / 1 year.
  - THP: 20,000 km / 1 year.
  - EB2F: 15,000 km / 1 year.

  The DV6 and EB2F values match the Israeli figure in the Hebrew Opel manual (15,000 km / 1 year for PSA engines).
- Files:
  - citroen-berlingo-2008-2019-1.6-hdi
  - peugeot-partner-2008-2018-1.6-hdi
  - peugeot-3008-5008-2016-2019-1.6-bluehdi (BH01/BH02, also 208/2008/301/308 BlueHDi)
  - citroen-c3-c4-picasso-cactus-2010-2018-1.6-hdi
  - peugeot-3008-5008-508-2010-2023-1.6-thp (5FV/5G01/5G06)
  - citroen-c4-picasso-c5-aircross-2011-2023-1.6-thp (also DS4 5G06 petrol)
  - peugeot-208-2008-301-2013-2017-1.2-vti (HM01/HMZ/HM02)
  - citroen-c4-cactus-c3-2014-2017-1.2-vti
- Caveats (also written in the notes):
  - The sheets are from 2016-2019. Older carnets (before July 2012) had longer intervals, for example a 240,000 km timing belt.
  - The 5G06 (THP 180 EAT8, 2019-2023) has no sheet of its own, so the THP 155/165 sheets are used.
  - The sheets are Peugeot ones; Citroen uses the same PSA engines and plans.

### Chevrolet: GM US/Canada owner's manuals (mirror cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/)
"Additional Required Services - Normal" charts, 12,000 km grid. Oil is changed by the oil-life monitor, at least once a year. All files are **draft**.
| Manual | Pages (PDF) | Notes | File |
|---|---|---|---|
| 2014-spark.pdf | 305-308 | B12D1; B10D1 used as sister | chevrolet-spark-2010-2015-1.0-1.2 |
| 2014-sonic.pdf | 345-346 | F16D4 follows the book's 1.8 rows (timing belt 156,000), A14NET follows the 1.4T rows | chevrolet-sonic-2011-2016-1.4t-1.6 |
| 2013-malibu.pdf | 374-375, chart is an image | LTG | chevrolet-malibu-2013-2015-2.0-turbo |
| 2012-malibu.pdf | 321-322, image | — | chevrolet-malibu-2008-2012-2.4 |
| 2013-captiva.pdf (Captiva Sport) | 319-320, image | LEA | chevrolet-captiva-sport-2012-2015-2.4 |
| 2016-equinox.pdf | 275-276 | LEA | chevrolet-equinox-2016-2017-2.4 |
| 2014-cruze.pdf | 365-366 | 1.4T rows; Orlando is on the same J300 platform with the same engine | chevrolet-orlando-2014-2018-1.4-turbo |

### Jeep / Chrysler (registry engine letter G = 3.6 Pentastar)
- jeep-grand-cherokee-2011-2021-3.6 (WK2), **draft**. Source: 2019 Grand Cherokee US owner's manual (cdn.dealereprocess.org/cdn/servicemanuals/jeep/2019-grandcherokee.pdf, pp. 437-440 = PDF 439-442). Grid of 16,000 km per year.
  - Rules: make Chrysler, names GRAND CHEROKEE / JEEP GRAND CHER, 2011-2022, engine G. Make Jeep, 2011-2021, engine G.
- jeep-grand-cherokee-2022-2026-3.6 (WL), **draft**. Source: Samelet Hebrew book https://samelet.com/wp-content/uploads/2023/11/Jeep_Grand_Cherokee-2023_carbook.pdf pp. 289-292 (PDF 290-293).
  - The book has two grids that do not agree: p. 290 assumes 16,000 km per year and p. 291 assumes 12,000 km per year. The file uses the detailed 12,000 km grid, and the notes say so. This is why it is not "reviewed".
  - Registry make Jeep 2021 is ambiguous (WK2 MY2021 and WL L overlapped). It is mapped to WK2.
- jeep-wrangler-2012-2018-3.6 (JK), **draft**. Source: 2016 Wrangler US owner's manual (…/jeep/2016-wrangler.pdf, pp. 665-670 = PDF 667-672). Rule: Chrysler/Jeep WRANGLER names, 2012-2018, engine G.

### Ford (Delek Motors): Hebrew one-page plans, **reviewed**
Source: the page https://www.ford.co.il/תוכנית-טיפול/שירות. It embeds `var data`, which holds SharePoint links; the PDFs download with the two-step cookie method. Round 2 skipped the Edge, Explorer and Ranger plans because of their different layout. Their text layer is clean, and they are now transcribed:
- ford-edge-2008-2010-3.5 (10,000 km / 6 months)
- ford-edge-2011-2014-2.0-3.5
- ford-edge-2015-2018-2.0-3.5
- ford-edge-2019-2026-2.0-2.7
- ford-explorer-2011-2014-3.5
- ford-explorer-2015-2019-3.5
- ford-explorer-2020-2026-2.3-3.0
- ford-ranger-2023-2026-diesel
- ford-bronco-2021-2026
- ford-focus-1999-2003-1.6 (the Focus 1999-2003 plan had been parsed into ford-plans.json but never generated)

These plans list only replacement items, and the files do not add any routine checks.

### Fiat 500e (electric), **reviewed**
Samelet Hebrew book https://samelet.com/wp-content/uploads/2023/11/Fiat_Fiat-E_carbook_072021.pdf, "תוכנית טיפולי שירות" pp. 218-220 (PDF 219-221): 15,000 km / 1 year, 10 columns. Rule: Fiat FIAT 500 / 500 / 500E, fuel חשמל, 2020-2026.

### Clones of plans already in the repo (same engine, new model/generation), **draft**
- renault-clio-2020-2022-1.3-tce: Clio V H5H/H5HB4B. It copies renault-captur-2020-2026-1.3-tce, which comes from the Renault Australia table for the 1.3 TCe. The table was re-read on https://www.renault.com.au/capped-price-servicing/ (Playwright) and is unchanged.
- citroen-c4-2015-2018-1.2-puretech: C4 B7 with HN02. It copies citroen-c4-2021-2026-1.2-puretech; the numbers were not re-verified by this group.

## Registry-only rules (no new file)
- Citroen C4 SPACETOURER / C4 PICASSO with engine code "HNY/HN02" (2018, 161 cars) → citroen-c4-spacetourer-2014-2022-1.2-puretech.
- Fiat (make) RENEGADE, engine 55263624, 2015-2019 (311 cars) → jeep-renegade-2015-2019-1.4-multiair.
- Opel ADAM, engine B14XER, 2013-2019 (1,364 cars) → opel-corsa-2015-2019-1.4. This is a sister mapping: same B14XER engine and the same Corsa platform. The Hebrew Adam 2017 manual (public-servicebox.opel.com he_IL Adam/2013_2019/2017, p. 199) puts Israel in the international 15,000 km / 1 year plan, like the Corsa E file.

## File list (sorted by newly covered vehicles)
| vehicles (new) | id | status | interval | registry rule(s) | main source(s) |
|---|---|---|---|---|---|
| 14754 | citroen-berlingo-2008-2019-1.6-hdi | draft | 15000/12m | Citroen BERLINGO 2008-2019 [9HX,9HW,9HP,9HN,9H06,9H02,9HF,BH02,BH01] | https://www.forum-peugeot.com/wp-content/uploads/2016/08/planentretien3081.6hdi92.pdf ; https://www.forum-peugeot.com/wp-content/uploads/2016/09/planentretien3008hdi100.pdf ; https://www.forum-peugeot.com/wp-content/uploads/2016/09/planentretien3008bluehdi120eat.pdf |
| 6539 | peugeot-3008-5008-508-2010-2023-1.6-thp | draft | 20000/12m | Peugeot 3008/5008/508/RCZ 2010-2023 [5FV,5G01,5G06] fuel בנזין | https://www.forum-peugeot.com/wp-content/uploads/2016/09/planentretien3008thp165.pdf ; https://www.forum-peugeot.com/wp-content/uploads/2016/07/planentretien5008thp165.pdf ; https://www.forum-peugeot.com/wp-content/uploads/2016/08/planentretien3081.6thp155.pdf |
| 5267 | chevrolet-spark-2010-2015-1.0-1.2 | draft | 12000/12m | Chevrolet SPARK/SPARK LS/SPARK LT 2010-2015 [B12D1,B10D1] | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2014-spark.pdf ; https://www.chevrolet.co.il/ |
| 4944 | jeep-grand-cherokee-2011-2021-3.6 | draft | 16000/12m | Chrysler GRAND CHEROKEE/JEEP GRAND CHER/JEEP GRAND CHEROKEE/GRAND CHEROKEE LAREDO 2011-2022 [G]; Jeep GRAND CHEROKEE 2011-2021 [G] | https://cdn.dealereprocess.org/cdn/servicemanuals/jeep/2019-grandcherokee.pdf ; https://samelet.com/wp-content/uploads/2023/11/Jeep_Grand_Cherokee-2023_carbook.pdf |
| 4171 | citroen-c4-picasso-c5-aircross-2011-2023-1.6-thp | draft | 20000/12m | Citroen C4 PICASSO/C4 GD PICASSO/GRAND C4 PICASSO/C4 SPACETOURER 2011-2023 [5FV,5G01,5G06] fuel בנזין; DS DS4/DS 4/DS7/DS 7 2018-2024 [5G06] fuel בנזין | https://www.forum-peugeot.com/wp-content/uploads/2016/09/planentretien3008thp165.pdf ; https://www.forum-peugeot.com/wp-content/uploads/2016/07/planentretien5008thp165.pdf ; https://www.forum-peugeot.com/wp-content/uploads/2016/08/planentretien3081.6thp155.pdf |
| 3280 | peugeot-3008-5008-2016-2019-1.6-bluehdi | draft | 15000/12m | Peugeot 3008 2016-2019 [BH01,BH02]; Peugeot 5008 2017-2019 [BH01,BH02]; Peugeot 208/2008/301/308 2015-2019 [BH01,BH02] | https://www.forum-peugeot.com/wp-content/uploads/2016/08/planentretien3081.6hdi92.pdf ; https://www.forum-peugeot.com/wp-content/uploads/2016/09/planentretien3008hdi100.pdf ; https://www.forum-peugeot.com/wp-content/uploads/2016/09/planentretien3008bluehdi120eat.pdf |
| 2608 | chevrolet-sonic-2011-2016-1.4t-1.6 | draft | 12000/12m | Chevrolet SONIC/SONIC LT/SONIC LS 2011-2016 [F16D4,A14NET] | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2014-sonic.pdf ; https://www.chevrolet.co.il/ |
| 2330 | citroen-c3-c4-picasso-cactus-2010-2018-1.6-hdi | draft | 15000/12m | Citroen C3 PICASSO 2009-2018 [9HP,9H06,9HN,BH02,BH01]; Citroen C4 PICASSO/C4 SPACETOURER/C4 GD PICASSO/GRAND C4 PICASSO 2014-2018 [BH01,BH02]; Citroen C4 CACTUS 2014-2018 [BH01,BH02,9H06]; Citroen C3/C4/C-ELYSEE/DS3 2010-2018 [9HP,9H06,9HR,9H05,BH01,BH02] | https://www.forum-peugeot.com/wp-content/uploads/2016/08/planentretien3081.6hdi92.pdf ; https://www.forum-peugeot.com/wp-content/uploads/2016/09/planentretien3008hdi100.pdf ; https://www.forum-peugeot.com/wp-content/uploads/2016/09/planentretien3008bluehdi120eat.pdf |
| 1745 | ford-explorer-2020-2026-2.3-3.0 | reviewed | 20000/12m | Ford EXPLORER/EXPLORER-ST/EXPLORER ST/EXPLORER LIMITE 2020-2026 | https://delekmotorscoil.sharepoint.com/:b:/s/Techtrain/EX-NvTIFF9RNpKXz0fce6qwBCpdaYi9tstN50ORIIbimOQ?download=1 ; https://www.ford.co.il/תוכנית-טיפול/שירות |
| 1658 | chevrolet-malibu-2008-2012-2.4 | draft | 12000/12m | Chevrolet MALIBU/MALIBU LT 2007-2012 [11B,1N9,1KA,1N7,LE5] | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2012-malibu.pdf ; https://www.chevrolet.co.il/ |
| 1621 | ford-explorer-2015-2019-3.5 | reviewed | 15000/12m | Ford EXPLORER/EXPLORER LIMITE/EXPLORER-LIMITE/EXPLORER LIMITED 2015-2019 | https://delekmotorscoil.sharepoint.com/:b:/s/Techtrain/EbZsbgRC-zRLvxAFs9LNYwAB33wp0lNs3rpwLSIIXW0glQ?download=1 ; https://www.ford.co.il/תוכנית-טיפול/שירות |
| 1585 | jeep-grand-cherokee-2022-2026-3.6 | draft | 12000/12m | Jeep GRAND CHEROKEE/GRAND CHEROKEE L 2022-2026 [G] | https://samelet.com/wp-content/uploads/2023/11/Jeep_Grand_Cherokee-2023_carbook.pdf |
| 1486 | peugeot-208-2008-301-2013-2017-1.2-vti | draft | 15000/12m | Peugeot 208/2008/301 2012-2017 [HM01,HMZ-HM01,HMZ,HM02,HM05] | https://www.forum-peugeot.com/wp-content/uploads/2019/05/planentretien208puretech82.pdf ; https://www.forum-peugeot.com/wp-content/uploads/2016/06/planentretien1.2PureTech82BVM5.pdf ; https://www.autojm.fr/pdf/notices/PEUGEOT/carnet-entretien-peugeot.pdf |
| 1256 | chevrolet-captiva-sport-2012-2015-2.4 | draft | 12000/12m | Chevrolet CAPTIVA SPORT 2012-2015 [LEA] | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2013-captiva.pdf ; https://www.chevrolet.co.il/ |
| 1197 | peugeot-partner-2008-2018-1.6-hdi | draft | 15000/12m | Peugeot PARTNER/NEW PARTNER/PARTNER TEPEE 2008-2018 [9HX,9HW,9HP,9HN,9H06,9H02,9HF,BH02,BH01] | https://www.forum-peugeot.com/wp-content/uploads/2016/08/planentretien3081.6hdi92.pdf ; https://www.forum-peugeot.com/wp-content/uploads/2016/09/planentretien3008hdi100.pdf ; https://www.forum-peugeot.com/wp-content/uploads/2016/09/planentretien3008bluehdi120eat.pdf |
| 1189 | renault-clio-2020-2022-1.3-tce | draft | 30000/12m | Renault CLIO 2020-2022 [H5H,H5HB4B] | https://www.renault.com.au/capped-price-servicing/ ; https://www.renault.co.il/ |
| 1072 | chevrolet-malibu-2013-2015-2.0-turbo | draft | 12000/12m | Chevrolet MALIBU/MALIBU LT 2013-2015 [LTG] | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2013-malibu.pdf ; https://www.chevrolet.co.il/ |
| 1053 | ford-edge-2011-2014-2.0-3.5 | reviewed | 15000/12m | Ford EDGE 2011-2014 | https://delekmotorscoil.sharepoint.com/:b:/s/Techtrain/EaEwy2zeqdNLsHhm6nXqdWABWi-_D3RtxR0zUOIE7VLvLA?download=1 ; https://www.ford.co.il/תוכנית-טיפול/שירות |
| 1045 | chevrolet-orlando-2014-2018-1.4-turbo | draft | 12000/12m | Chevrolet ORLANDO 2011-2018 [A14NET,B14NET] | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2014-cruze.pdf ; https://www.chevrolet.co.il/ |
| 1012 | fiat-500e-2021-2026-ev | reviewed | 15000/12m | Fiat FIAT 500/500/500E/FIAT 500E 2020-2026 fuel חשמל | https://samelet.com/wp-content/uploads/2023/11/Fiat_Fiat-E_carbook_072021.pdf |
| 1010 | jeep-wrangler-2012-2018-3.6 | draft | 16000/12m | Chrysler WRANGLER/WRANGLER UNLIMI/WRANGLER UNLIM/WRANGLER UNLI 2012-2018 [G]; Jeep WRANGLER/WRANGLER UNLIMI/WRANGLER UNLIM/JEEP WRANGLER 2012-2018 [G] | https://cdn.dealereprocess.org/cdn/servicemanuals/jeep/2016-wrangler.pdf |
| 983 | ford-edge-2015-2018-2.0-3.5 | reviewed | 15000/12m | Ford EDGE/EDGE TITANIUM/EDGE-TITANIUM/EDGE-SEL 2015-2018 | https://delekmotorscoil.sharepoint.com/:b:/s/Techtrain/Ef4jn7gRNOZKhVxJhdOs0XEBD03uaHWVTosGiz0hR9bwJw?download=1 ; https://www.ford.co.il/תוכנית-טיפול/שירות |
| 980 | ford-explorer-2011-2014-3.5 | reviewed | 15000/12m | Ford EXPLORER 2011-2014 | https://delekmotorscoil.sharepoint.com/:b:/s/Techtrain/ETT2AdzowURFjGqdDS3TBh4BxPzPrFc_CaL1nWoqENRztA?download=1 ; https://www.ford.co.il/תוכנית-טיפול/שירות |
| 635 | ford-bronco-2021-2026 | reviewed | 16000/12m | Ford BRONCO/BRONCO BADLANDS/BRONCO WILDTRAC/BRONCO WILDTRAK 2021-2026 | https://delekmotorscoil.sharepoint.com/:b:/s/Techtrain/EeeszIXEYoBJri8cGbLAAa4B_AOr9gymv6RSWw6lQU-5NA?download=1 ; https://www.ford.co.il/תוכנית-טיפול/שירות |
| 587 | ford-edge-2008-2010-3.5 | reviewed | 10000/6m | Ford EDGE 2007-2010 | https://delekmotorscoil.sharepoint.com/:b:/s/Techtrain/EQ7bSpD0v15KpT0-zZbF0uIBU5OFf_cgHCOUh0z6RWFx5g?download=1 ; https://www.ford.co.il/תוכנית-טיפול/שירות |
| 541 | citroen-c4-cactus-c3-2014-2017-1.2-vti | draft | 15000/12m | Citroen C4 CACTUS/C3/C-ELYSEE/C ELYSEE 2013-2017 [HM01,HMZ-HM01,HMZ,HM02,HM05] | https://www.forum-peugeot.com/wp-content/uploads/2019/05/planentretien208puretech82.pdf ; https://www.forum-peugeot.com/wp-content/uploads/2016/06/planentretien1.2PureTech82BVM5.pdf ; https://www.autojm.fr/pdf/notices/PEUGEOT/carnet-entretien-peugeot.pdf |
| 523 | ford-ranger-2023-2026-diesel | reviewed | 20000/24m | Ford RANGER 2023-2026 fuel דיזל | https://delekmotorscoil.sharepoint.com/:b:/s/Techtrain/EYv1xArxEvROph7WazGGsN8BKDOm4Mi06hUva00DQHoZZA?download=1 ; https://www.ford.co.il/תוכנית-טיפול/שירות |
| 435 | ford-focus-1999-2003-1.6 | reviewed | 15000/12m | Ford FOCUS 1999-2003 | https://delekmotorscoil.sharepoint.com/:b:/s/Techtrain/Ee430FBNfetOviTm_6b6ntQBZUu0KKGEJFkz79p06v_aBg?download=1 ; https://www.ford.co.il/תוכנית-טיפול/שירות |
| 429 | ford-edge-2019-2026-2.0-2.7 | reviewed | 16000/12m | Ford EDGE/EDGE TITANIUM/EDGE-TITANIUM/EDGE-SEL 2019-2026 | https://delekmotorscoil.sharepoint.com/:b:/s/Techtrain/EVZn_ej1o-ZPm05rSHjOtjcBZWM09-vkPEAg7VKe4aXiJA?download=1 ; https://www.ford.co.il/תוכנית-טיפול/שירות |
| 423 | chevrolet-equinox-2016-2017-2.4 | draft | 12000/12m | Chevrolet EQUINOX 2016-2017 [LEA] | https://cdn.dealereprocess.org/cdn/servicemanuals/chevrolet/2016-equinox.pdf ; https://www.chevrolet.co.il/ |
| 376 | citroen-c4-2015-2018-1.2-puretech | draft | 15000/12m | Citroen C4 2014-2018 [HN01,HN02,HN05] | https://aftersales.fiat.com/eLumData/EN/57/619_AVENGER/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG/57_619_AVENGER_603.85.823_EN_02_12.22_L_LG.pdf ; https://public-servicebox.opel.com/OVddb/OV/he_IL/Corsa_F/2017_2022/2021_05/manual_user/ID-OCRFOLSE2105-he_11_online.pdf ; https://media-peugeot.lubit.co.il/wp-content/uploads/2023/06/Warranty-Peugeot-3Y-01.2024_Web-%D7%9E%D7%95%D7%A0%D7%92%D7%A9.pdf |

## Not done / blocked (biggest first)
- **PSA EP6 1.6 VTi 120 without turbo** (5FS, 5F01, 5FW, 5F02, 5FS-5F01: 207, C3, C4, 208, 2008, 308, 508; about 5.5k cars). No official sheet was found.
  - forum-peugeot.com has no VTi sheet among the files that search engines list. Guessed upload names returned 404, and its WP media API returns 403.
  - The feline208.net forum quotes the 2012 carnet (VTi 120: 30,000 km / 1 year, filters and plugs 60,000 km). That is a third-party transcription, so it was not used.
  - The 2007 Peugeot 308 per-engine documents linked from forum-peugeot are on association-bmfia.net, which is now a parked domain.
  - planete-citroen.com and pdfcoffee.com are behind Cloudflare 403. ds-prod.citroen.in (Citroen India maintenance booklets) is refused by the egress proxy (502).
- **PSA TU5/EC5 1.6** (NFU, NFP: C4 2006-2010, 301, C-Elysee, 206/307; about 2.8k cars): no source found.
- **Citroen Jumpy II 2.0 HDi** (RH02, 9HU; about 1.7k cars): no DW10 sheet was found. One 508 2.0 HDi 163 plan exists as a forum attachment, but it needs a login.
- **Renault/Dacia H4B (0.9 TCe) and H4D (1.0 TCe)** (Sandero, Logan, Clio IV/V, Twingo; about 9k cars), K4M 1.6, H4M hybrids, Koleos:
  - The Renault Australia page (re-read in Playwright) has no table for these engines.
  - renault.co.il and dacia.co.il still return 403.
  - Only third-party schedules turned up in search (Haynes, RTA, odopass, auto-abc), and none of them was used.
- **Opel, GM era** (Astra J/K, Mokka, Meriva, Zafira Tourer, Insignia; about 8k cars):
  - The Hebrew manuals on public-servicebox.opel.com give the interval only. The 2013 Astra J and 2017 Astra K editions put Israel in the international 15,000 km / 1 year plan. The 2011 English Astra J manual (manualslib 884807) still lists Israel in the European 30,000 km plan.
  - No item grid exists in the Astra J (manualslib 884807) or Mokka (3017112) manuals; both say the schedule is held by the workshop.
  - The only Opel grid known (Corsa D, manualslib 504809) was not stretched to other models.
- **Chevrolet**:
  - Aveo T250 (F14D3) and Optra (F16D3) use the older "Maintenance I/II" format. The 2009/2010 US Aveo has a 1.6 instead of the 1.4, and these were not transcribed.
  - Spark M400 L5Q (749 cars): the engine is not covered by the US manual.
  - Sonic with A14XER: no US equivalent.
  - Orlando 2.0 diesel (Z20D1): not the US Cruze diesel engine.
  - Captiva 2.2 diesel: not done.
- **Chrysler** Grand Voyager / Pacifica / Journey / Patriot, Wrangler 3.8 (EGT), and Grand Cherokee 3.0 diesel (VM23D): not done.
- **Ford**:
  - Tourneo/Transit Connect 1.8 TDCi (R3PA, HCPB; about 2k cars): Delek has no plan for it, and none was found elsewhere.
  - S-Max/Galaxy and Mondeo 2012-2015 with 2.0 EcoBoost (TNWA/TNBA): Delek's 2007 plan names only the 2.0/2.3 petrol and 2.0 diesel engines up to 2011/2012, so it was not extended.
  - Transit 350 (JXFA): not done.
- **Fiat** Punto/Qubo 1.4 8V (350A1000), Qubo 1.3 diesel, Doblo 2015-2019 diesel, Bravo, Fullback: Samelet has no Hebrew book for them (219 PDFs were listed through the WP media API). The Fiat 500 Hebrew book covers only the 1.2.
- **Audi** Q5 DAX/DPU, A4 DMS/CDH and **Skoda** Octavia 1.9 TDI (BXE): the engine codes could not be confirmed from an opened document (the vwts.ru index does not list DAX/DPU/DMS), so they were left for a VAG pass.

## Registry notes
- Registry make "Chrysler" carries most Wrangler JK and Grand Cherokee WK2 cars; rules exist for both Chrysler and Jeep.
- PSA engine codes used:
  - DV6 1.6 HDi: 9HX, 9HW, 9HP, 9HN, 9H06, 9H02, 9HF, 9HR, 9H05.
  - DV6 1.6 BlueHDi: BH01, BH02.
  - EP6 THP: 5FV, 5G01, 5G06.
  - EB2F without turbo: HM01, HMZ-HM01, HM02.
- Rules carry fuel ["בנזין"] where a PHEV shares the engine code. 3008 HYBRID4 and DS7 E-Tense use 5G06 with fuel חשמל/בנזין and are intentionally left unmatched.
