ev2 report - 18 schedules (9 reviewed from Israeli books, 9 draft). validate.mjs staging/ev2 -> all schedules valid.
Registry rules: registry/registry_rules.json (18 rules). Build scripts + downloads: scratchpad/dl/ev2 (_build/*.py).

REVIEWED (Israeli Hebrew books; PDF page numbers 1-based)
- hyundai-ioniq-5-2021-2023-ev: Colmobil cloudinary "הוראות-הפעלה-לנהג-יונדאי-איוניק-5-שנת-2021" (hyundaimotors.co.il/maintenance) pp.604-606. 15k/12. No 2022/23 book -> assigned to 2021 book. Coolant: regular (first 200k/10y then 40k/24) in long_interval; low-conductivity 60k/36 in note.
- hyundai-ioniq-5-2024-2026-ev: Hyundai_Ioniq5_OM_2024_web.pdf pp.639-642 + Hyundai_Ioniq5_OM_2026-web pp.649-650 (identical). 30k/24, cycle 240k. Coolant R at 150k then every 30k (long_interval).
- hyundai-kona-electric-2021-2024-ev: KONA-EV-hebrew-22.08.2021-4web-L.pdf pp.463-464. Registry KONA + חשמל + EM16. 15k/12.
- hyundai-kona-electric-2023-2026-ev: KONA-EV2026-all-web-low.pdf pp.497-498 (scanned, transcribed from images). Registry KONA EV. 30k/24; extra EV table every 12 mo/13,000 km (long_interval hybrid_system). No reduction-gear row. 2023-25 assigned to 2026 book (only 2nd-gen book).
- kia-ev6-2022-2024-ev: cdnmedia.kia-israel.co.il/www/cars-book/KIA_EV6_OM_2022.pdf pp.430-431. 30k/24; coolant first 210k/120mo then 30k/24.
- kia-niro-ev-2021-2022-ev: KIA-Niro-EV-OM-2021.pdf pp.470-471. 15k/12. 2021-22 vs 2023-24 split by model year (assumed).
- kia-niro-ev-2023-2024-ev: NIRO_Hebrew_01_חשמלי_2023.pdf pp.432-433 (found on kia-israel.co.il book-by-mail page). Europe (30k/24) and non-Europe (15k/12) tables; used non-Europe per Kia Israel 15k/1yr statement and "not AU/NZ" rows (brake fluid R at 45k/90k).
- kia-niro-plus-ev-2022-2024-ev: Niro-Plus-DE-PV-EV-2023.pdf p.318 (first curl SSL exit 35, retry OK). 15k/12; coolant 60k/36.
- kia-ev3-2025-2026-ev (extra, 1,098 veh.): EV3_Book.pdf pp.644-645, same table choice as Niro EV 2023.

DRAFT
- tesla-model-3-2021-2026-ev: hamphi.com/en-eu/pages/tesla-original-guides/model-3-serviceintervall-for-fordon (translated EU manual text) + manualslib 1765784 p.162-163 via Playwright (older NA edition). No periodic service; grid = tire rotation every 10,000 km (interval.months=12 is display only, said in note). time_based: cabin filter 24mo, brake fluid check 48mo (older edition 24mo), A/C desiccant 72mo. tesla.com: 403 (curl, WebFetch).
- tesla-model-y-2022-2026-ev: mycarusermanual.com/tesla/model-y/suv/2023/maintenance--maintenance-service-intervals (copy of owner's manual). Rotation 10,000 km; brake fluid check 24mo; desiccant 48mo; cabin 24mo; HEPA 36mo. No Juniper copy found. tesla.com en_gb Owners_Manual.pdf 403.
- xpeng-g6-2024-2026-ev: Warranty and Maintenance Manual G6 (EU) s3.eu-central-1.amazonaws.com/datamotive-sulu-assets/xpeng-rotterdam/03/warranty-and-maintenance-manual-g6-for-eu.pdf pp.11-18. A 20k/12, B 40k/24; reducer oil 80k/48; coolant 120k/72. xpeng.co.il 502.
- chery-fx-ev-2024-2026-ev: Chery Malaysia OMODA E5 schedule (chery.my 2026/05 PDF). FX EV = Omoda E5: UK Omoda E5 owner's manual (omodaauto.co.uk/downloads, cdn.cworigin.com 46593bd...pdf) lists motors TZ210XS129/TZ180SMZB0 = Israeli registry, but has no schedule. 15k/12; coolant/brake fluid/reducer 45k/36; cabin filter every service.
- chery-tiggo-4-hybrid-2025-2026-1.5-hev: Chery Malaysia TIGGO CROSS 2026-09 PDF pp.1-2 (1.5L+DHT HEV). 10k/6. "Element air filter" read as engine air filter.
- mg-zs-hybrid-2025-2026-1.5-hybrid / mg-3-hybrid-2024-2026-1.5-hybrid / mg-3-2025-2026-1.5 (15FCD, extra) / mg-zs-2018-2021-1.0t (10E4E, extra): mg.co.uk/servicing HTML tables (ZS Hybrid+ 2024+, MG3 Hybrid+ 2024+, MG3 2024+, ZS 2017-2020). 15,000 mi converted to 24,000 km. 15FHC = hybrid code, so ZS 15FHC 2025-26 = ZS Hybrid+.

NOT DONE / BLOCKED
- Chery TIGGO 4 PRO (2,369, SQRG4G15): same engine code as Hybrid but Israeli powertrain unconfirmed; Malaysia 1.5T+6DCT page does not match. cheryisrael.co.il Imperva.
- Hebrew books for Tesla/Xpeng/Chery/MG: blocked or absent (tesla.com 403, xpeng.co.il 502, cheryisrael Imperva, lubinski.clearmash.com 403 per round 1, not retried).
- Not attempted: MG S9/HS Hybrid/EHS 2026, Xpeng G9/P7i, IONIQ6 (Ioniq6-2026-OM-web.pdf exists in Hyundai library; mg.co.uk has HS PHEV 2024+/HS 2024+ tables).
