# Group "eu4": report (round 4)

17 schedule files (all **draft**) and `registry/registry_rules.json` (29 rules: 22 for the new files, 7 registry-only rules that point at files already in the repo).
Validation: `node scripts/validate.mjs staging/eu4` prints "all schedules valid (17 draft, 0 reviewed, 0 verified)".
Generator (holds every transcribed mark): `scratchpad/dl/eu4/gen/{gen,opel,renault,fiat,copies,main}.py` (run `python3 main.py`). Downloads and screenshots: `scratchpad/dl/eu4/`.
Coverage check: `scratchpad/dl/eu4/gain.mjs` (replays registry-counts.json against registry_map.json + all other staging rules). The eu4 rules match **21,886 registered vehicles that no rule matched before**, with 0 conflicts. (Toyota Proace/Proace City files were drafted and then dropped, because tail4 and japan-b already cover them.)

## New sources found this round
1. **Opel GM era item grid**: Opel Insignia owner's manual EN, edition 2011, manualslib 936387, "International service schedule", printed pp. 193-196 (15,000 km / 1 year, 5 columns), additional operations p. 197. Read from page screenshots (`dl/eu4/ins11_193..197.png`). The Astra J (884807), Astra J 2010 (504892, 504796, 657426), Mokka (566317, 1070436, 3017112), Zafira Tourer 2011 (907422) manuals have no grid; Meriva 504807 and Astra 803144 have grids but for Z-series engines (Meriva A / Astra H). Insignia 2009 (1151968) and 504790/504797/504814 are other Insignia editions with the same grid.
2. **Israeli interval for Opel**: Hebrew manuals on public-servicebox.opel.com (he_IL). Checked the European country list in each:
   - MY2012 editions put Israel in the European list (30,000 km / 1 yr): Astra J 2012_5 p.218, Meriva B 2012 p.185, Zafira Tourer 2012_5 p.238, Zafira B 2012 p.185, Insignia 2011_5 p.192.
   - MY2013+ editions do not list Israel, so the international 15,000 km / 1 yr applies: Astra J 2013 p.261, Astra J 2014 p.273, Astra K 2017 p.258, Mokka 2014_5 p.189, Mokka X 2017 p.208, Meriva 2015 p.208, Zafira Tourer 2016 p.257, Insignia 2014 p.250 (and Insignia 2010_5 p.189).
   - All files use 15,000 km / 12 months and say that the 2012 editions had 30,000 km.
3. **Renault Malaysia** (official distributor TC Euro Cars), PDFs linked from https://www.renault.com.my/ownership : `Renault_Malaysia_{Fluence___ClioGTLine,Captur___Koleos,Zoe___Twizy,MeganeRS___ClioRS}_Periodic_Maintenance_Service-1603198170.pdf`. 12 columns of 10,000 km / 6 months up to 120,000 km. Parsed with word coordinates (`dl/eu4/myparse.py`) and checked on rendered images. Malaysian Fluence = 2.0 M4R CVT (paultan.org review).
4. **Fiat EN handbooks**: Punto 2012 (aftersales.fiat.com eLum, 603.47.010 ed. 07/2017, pp.111-117), Qubo Euro 6 (manualslib 1883346, site pages 132-139), Doblo 2016 (manualslib 2151994, site pages 174-181).
5. **VW Golf 5 Maintenance 11.2009** (vwts.ru, already in the repo's VAG sources), PDF pp.16-17: toothed belt table lists BXE/BLS/BKD (TDI-PD): from MY2007 belt every 150,000 km, roller every 300,000.

## Files
| vehicles (new) | id | status | interval | registry rule(s) | sources / notes |
|---|---|---|---|---|---|
| 5114 | opel-astra-j-2010-2016-1.4-turbo | draft | 15000/12m, cycle 75k | Opel ASTRA, TRA BERLINA, ASTRA BERLINA, ASTRA ST, ASTRA GTC, ASTRA SEDAN 2011-2018 [A14NET, A 1.4 NET, B14NET, B 1.4 NET] | Insignia 2011 grid (manualslib 936387 pp.193-196) + Hebrew Astra J 2013/2014 manuals. 1.4T rows: no belt/valve rows (not in the grid's engine lists) |
| 2608 | opel-mokka-2013-2018-1.4-turbo | draft | 15000/12m | MOKKA, MOKKA - X, MOKKA FIX 2013-2019 [same 1.4T codes] | same grid + Hebrew Mokka 2014_5, Mokka X 2017 |
| 1916 | opel-astra-k-2016-2018-1.4-turbo | draft | 15000/12m | ASTRA 2016-2018 [B 14 XFT, B14XFT, LE2] | same grid + Hebrew Astra K 2017 |
| 821 | opel-insignia-2009-2017-1.6-2.0-turbo | draft | 15000/12m | INSIGNIA 2009-2017 [A 2.0 NHT, A 2.0 NFT, B 2.0 NHT, A 1.6 XHT, B 16 SHL (+unspaced)] | grid is from the Insignia itself; A20NHT plugs 120k/8y and V-belt 150k/10y |
| 610 | opel-zafira-tourer-2012-2018-1.4-turbo | draft | 15000/12m | ZAFIRA TOURER/ZAFIRA 2012-2018 [1.4T codes] | + Hebrew Zafira Tourer 2016 |
| 447 | opel-meriva-b-2014-2017-1.4 | draft | 15000/12m | MERIVA 2013-2017 [B14NEL...] | + Hebrew Meriva 2015 |
| 328 | opel-astra-j-2010-2014-1.6 | draft | 15000/12m | ASTRA family 2010-2015 [A 1.6 XER, A16XER, A 1.6LET...] | grid rows for A16XER/A16LET: toothed belt + V-belt 150k/10y, water-pump/PS belt 120k/10y, A16XER valve clearance 150k/10y |
| 1811 | fiat-doblo-2010-2022-1.3-1.6-multijet | draft | 35000/24m, cycle 175k | Fiat DOBLO/FIAT DOBLO/DOBLO1.3/DOBLO 1.3 COMBI/DOBLO 1.6 COMBY/DOBLO 1.6 VAN 2010-2022 diesel [263A2000, 198A3000, 263A5000, 263A8000, 330A1000, 55280444, 55283775, 199A9000] | Doblo 2016 EN handbook, DPF diesel table. Engine codes not verified against a Fiat document (mapped by model/years) |
| 1358 | fiat-punto-2007-2014-1.2-1.4-8v | draft | 15000/12m, cycle 120k | PUNTO 1.4/PUNTO1.4/PUNTO 1.2/GRANDE PUNTO1.2/1.4/GRANDE PUNTO/PUNTO/PUNTO EVO 2006-2015 [350A1000, 199A4000, 169A4000] petrol | Punto 2012 EN handbook petrol plan; dusty-area belt 60k/4y and filters 15k noted |
| 498 | fiat-qubo-2009-2018-1.4 | draft | 30000/24m, cycle 180k | QUBO 2009-2018 [350A1000] petrol | Qubo EN Euro 6 handbook; book says oil yearly and filters every 15k in dusty areas (noted, long_interval oil 12m) |
| 462 | fiat-qubo-2013-2018-1.3-multijet | draft | 35000/24m, cycle 175k | QUBO 2012-2018 [199A9000, 225A2000] diesel | Qubo EN Euro 6 diesel table (Euro 5 199A9000 predates the edition) |
| 1573 | audi-a4-a5-a6-2008-2016-1.8-2.0-tfsi | draft | 15000/12m | Audi A4/AUDI A4/A4 AVANT and A5/A5 SPORTBACK/A5 COUPE 2008-2016 [CDH, CAB, CJE, CDN]; A6 2011-2016 [CDN, CJE] petrol | copy of repo file audi-q5-2009-2017-2.0-tfsi (same EA888 chain family, Champion 2.0 table); vwts index confirms CDHx/CABx/CDNx = EA888 gen 2, CJEx = EA888 gen 3. Multitronic CVT oil not covered (no document) |
| 1145 | renault-fluence-2010-2016-2.0 | draft | 10000/6m, cycle 120k | Renault FLUENCE 2009-2016 [M4R, M4RK7]; SCENIC/GRAND SCENIC/GEREND SCENIC/MEGANE 2009-2016 [M4R] petrol | Renault Malaysia Fluence page |
| 396 | renault-koleos-2009-2011-2.5 | draft | 10000/6m | KOLEOS 2008-2012 [2TR, 2TRA7] petrol | Renault Malaysia "KOLEOS 2.5" page (gen 1) |
| 457 | renault-zoe-2017-2021-ev | draft | 10000/6m | ZOE 2013-2022 fuel חשמל | Renault Malaysia Zoe page; battery/coolant rows have no verb → shown as inspect |
| 634 | skoda-octavia-2007-2010-1.9-tdi | draft | 15000/12m | Skoda OCTAVIA/OCTAVIA COMBI/OCTAVIA SCOUT 2006-2010 [BXE, BKD] diesel | template = repo file skoda-octavia-2011-2017-1.6-tdi, timing belt changed to Golf 5 PD rows (150k, roller 300k) |
| 355 | vw-jetta-golf-2007-2010-1.9-tdi | draft | 15000/12m | VW JETTA/GOLF PLUS/GOLF 2006-2010 [BXE, BKD]; TOURAN 2006-2010 [BXE, BLS, BKD] diesel | same |

## Registry-only rules (existing files)
- Citroen C4 PICASSO/C4 GD PICASSO/GRAND C4 PICASSO/C4 SPACETOURER 2014-2019 [AH01]; DS DS7/DS 7/DS7 CROSSBACK 2018-2022 [AH01]; Peugeot 3008/5008/508 2017-2022 [AH01] → citroen-jumpy-2016-2026-2.0-bluehdi (586 vehicles). Sister mapping: same DW10FC 2.0 BlueHDi and same EMP2 platform; that file comes from the Israeli Union Motors Toyota Proace sheet (603), which I re-checked against the PDF.
- Citroen JUMPY HDI/JUMPY 2007-2016 [9HU] (1.6 HDi DV6) → citroen-berlingo-2008-2019-1.6-hdi (280). PSA plans are per engine.
- Citroen JUMPY 2019-2022 [YH01] → citroen-berlingo-2018-2026-1.5-bluehdi (68).
- Note: the eu3 rule C4 SPACETOURER/C4 PICASSO [HNY/HN02] is still only in staging/eu3 (not in registry_map.json); it was not duplicated here.
- Renault MEGANE 2013-2015 [H5F] petrol → renault-megane-2016-2019-1.2-tce (257; same H5F engine, the file's plan is engine-based from the Renault Australia H5F table).
- Renault KANGOO 2/KANGOO 2008-2012 [K9KB8] → renault-kangoo-2008-2021-1.5-dci (113).
- VW CADDY/CADDY KOMBI/CADDY MAXI 2004-2007 [BJB] → vw-caddy-2008-2015-1.6-1.9-tdi-1.2-tsi (49; BJB is in the same TDI-PD row as BLS in the Golf 5 table).

## Not done / blocked (biggest first)
- **Renault/Dacia H4B 0.9 TCe, H4D 1.0, K4M 1.6, H4M 1.6 (Fluence and E-Tech hybrids), D4F 1.2, Koleos H5H, Kangoo K4M** (about 22k vehicles). No manufacturer document with intervals was found. Tried:
  - renault.co.il, dacia.co.il, service.carasso.co.il: 403; carasso.co.il / carassomotors.co.il: no connection.
  - Renault Australia /capped-price-servicing/ (re-read: still only Kadjar/Arkana/Captur MY21, Koleos MY20, Megane RS, Kangoo, Trafic, Master) and the new /servicing/ "assured price" selector (Arkana, Arkana Hybrid, Duster, Koleos...): prices and intervals only, no items.
  - Renault UK service-schedule page: login (My Renault) only. Renault SA service-plan guide: generic.
  - Owner's manuals without a maintenance table: Dacia UK Sandero III/Jogger (cdn.group.renault.com), manualslib Dacia Sandero 2014 (1106251, "service sheets" are stamp pages), Duster 1154069/1171600, Renault Brazil Logan 2012, Renault Colombia Fluence 2014 (cdn.group.renault.com/ren/co/manuales/...), Russian Logan/Sandero X52ph2 and Fluence 2013 manuals (cdn.group.renault.com/ren/ru/manuals/...).
  - Renault e-guide old PDFs: 404. autojm.fr has no Renault folder. Renault Turkey / Colombia quoter / Argentina / Chile: price tools only. avtogermes.ru (Russian dealer docs): connection closed by egress.
  - Only third-party schedules exist (Haynes maintenance plans, auto-abc, idgarages, c3carecarcenter); not used.
- **PSA EP6 1.6 VTi 120 (5FS, 5F01, 5FW, 5F02: 207, 208, 2008, C3, C4, 308, 508; ~7k) and TU5 NFU/NFP (~3k)**: no official sheet. Searched forum-peugeot uploads (only HDi/THP/PureTech sheets listed), eduscol bac-pro dossiers (random vehicles, no VTi plan found in the two opened), Peugeot Australia price-promise pages (prices only). idgarages has a "3008 1.6i 120 16V, valid from 01/05/2013" plan but it is third-party, not used.
- **Citroen Jumpy II 2.0 HDi RH02 (1,470)**: no DW10 2.0 HDi (non-BlueHDi) plan found.
- **Ford Tourneo Connect 1.8 TDCi R3PA/HCPB/KKDA (~2.2k)**: only Haynes. No Ford Europe service guide found.
- **Fiat Qubo KFT (336)**: KFT is a PSA engine code; could not confirm what engine these Qubo rows really have, left unmatched. Fiat Bravo 1.4 (198A4000), Doblo 940C1000/223B1000: not done.
- Opel BERLINA 1.6 CDTI B16DTH (303), Insignia B (B15XHT), Astra L/Mokka B PSA engines (HN05/HN09/ZK01): not done.

## Caveats written in the notes
- Opel: the grid is from the Insignia manual (same Opel generation); the 1.4 turbo, B14XFT and B14NEL engines are not named in it, so no belt/valve rows were added for them. Interval 15,000 km / 1 yr per Hebrew MY2013+ manuals; MY2012 Hebrew editions said 30,000 km.
- Renault Malaysia: tropical market, 10,000 km / 6 months; the Israeli importer interval is unknown.
- Fiat Qubo/Doblo: book intervals 30,000-35,000 km / 2 years; the books ask for yearly oil and 15,000 km filters in dusty areas or town use.
