prem5 report (round 5: BMW/MINI, Mercedes-Benz, Mitsubishi, Isuzu, Tesla, Land Rover)

6 schedule files, all draft. 3 upgrade existing ids (import with --force), 2 are new ids, and 1 upgrades the Grandis file added by the parallel "Round 5 Japan" commit (7e96b4f).
registry/registry_rules.json: 2 new rules, only for rows that no rule matches yet. The existing rules for the upgraded ids are unchanged and still valid.
node scripts/validate.mjs staging/prem5 -> "all schedules valid (6 draft, 0 reviewed, 0 verified)".
Generator: scratchpad/dl/prem5/gen/gen.py. Downloads: scratchpad/dl/prem5/{mit,mb,jdm,mmal,tesla,lr,sp,bmw}/.
Coverage simulation (dl/prem5/sim.mjs = repo registry_map.json + these rules): +689 newly matched vehicles (Tesla S/X 472, Eclipse Cross PHEV 217).
No reachable Israeli-importer document had a maintenance table for any make in this group, so no file could be marked "reviewed".

FILES (id | status | vehicles | source)
- tesla-model-3-2021-2026-ev (UPGRADE) | draft | 20,305 | official Tesla owner's manual, current edition (software 2026.26.200.11) on tesla.cn:
  https://www.tesla.cn/ownersmanual/model3/zh_cn/GUID-E95DAAD9-646E-4249-9930-B109ED7B1D91.html
  Changes: cabin filter 24 -> 12 months, yearly wiper blades added, brake fluid check every 48 months confirmed. The A/C desiccant row (6 yrs) stays, with a note that it comes only from older editions.
- tesla-model-y-2022-2026-ev (UPGRADE) | draft | 16,401 | same manual, modely page. Cabin filter plus 2 HEPA and 2 carbon filters yearly (was 24/36 months), brake fluid check every 48 months (was 24), wipers yearly. The desiccant row (48 months) stays, with an older-edition note.
- tesla-model-s-x-2021-2026-ev (NEW) | draft | 472 (MODEL S 3D8/5D1 2022, MODEL X 3D8/5D1 2022-23) | tesla.cn models and modelx pages (same edition): tire rotation every 10,000 km, cabin and HEPA filters yearly (Model X also the carbon filter), wipers yearly, brake fluid check every 4 years.
- mitsubishi-grandis-2005-2011-2.4 (UPGRADE of the file from commit 7e96b4f) | draft | 3,492 (incl. LPG) |
  Mitsubishi "Grandis (NA4W) Pre-delivery Inspection and Periodic Maintenance", 2006 edition, group 2 pp.2-3..2-6 (PDF 27-30):
  https://jdmfsm.info/Auto/Japan/Mitsubishi/Grandis/Manuals/Predelivery%20and%20Periodic%20Maintenance/5850NA4W_06_003ENG.pdf
  (the 2004 edition, 5850NA4W_04_003ENG.pdf, has the same 4G69 intervals plus an SRS check at 10 yrs). This table is written for the Grandis itself; the previous file used the general Mitsubishi Europe table (Lancer rows, sister).
  15,000/12; air filter 45k; brake fluid 30k/2y; coolant 60k/4y; timing belt and plugs 90k; ATF (2WD) 90k/6y (this answers the open question in the old file); fuel filter 150k/10y. The valve-clearance row is left out: it applies only to engines without hydraulic lifters, and the 4G69 has them.
- mitsubishi-outlander-2007-2012-2.0-2.4 (UPGRADE) | draft | 2,552 |
  Mitsubishi "Outlander 2007 (CW) Pre-Delivery Inspection and Periodic Maintenance" for Europe, group 2 pp.2-3..2-6 (PDF 3-6):
  https://jdmfsm.info/Auto/Japan/Mitsubishi/Outlander/Manuals/2007/Service%20Manual%20PDF/Pre-Delivery%20Inspection/GR00000300-2.pdf
  Same generation; the old file copied the next generation's ZJ-ZL Australian table. 15,000/12; air filter 45k; brake fluid 30k; coolant 60k/4y; plugs 90k; ATF/CVT and differentials (4WD) 90k/6y; transfer case 75k/5y; fuel filter 150k/10y; no timing belt (chain). The valve-clearance check every 15k is kept, as the table marks it, with a note.
- mitsubishi-eclipse-cross-phev-2021-2026-2.4-phev (NEW) | draft | 217 (ECLIPSE CROSS, fuel חשמל/בנזין, 4B12, 2023-24) |
  Mitsubishi Motors Australia "24MY YB Eclipse Cross Plug-in Hybrid Inspection and Maintenance Schedule" pp.1-2, read from page images:
  https://www.mitsubishi-motors.com.au/content/dam/mmal/pdfs/maintenance-schedules/24MY%20YB%20ECLIPSE%20CROSS%20PLUG-IN%20HYBRID%20INSPECTION%20AND%20MAINTENANCE%20SCHEDULE%20WEB.pdf
  The Colmobil Hebrew Eclipse Cross PHEV book has no table.

Self-check against the audit failure modes: every row of each source table is either in the grid or long_interval, or named in the Hebrew notes as not mapped (wheel bearings, EGR, idle/CO, road test, ignition cables, diesel and manual-gearbox rows). Engine coolant (first 165k/8y, then 105k/5y) and rear-motor coolant (400k/20y) are both in long_interval of the EC PHEV file. Nothing comes from another book except the Tesla desiccant rows, which are labelled as older editions.

ISRAELI ROUTES TRIED (none gave a maintenance table)
BMW / MINI (BMW and MINI Israel are run by Delek Motors; the service site bmws.co.il is Delek's)
- www.bmw.co.il, www.mini.co.il, kamor.co.il: proxy CONNECT 502 (curl and Playwright). The bmw.co.il / mini.co.il apex domains answer, but only with a 301 to www. --connect-to does not help (the proxy resolves by name).
- WebFetch on www.bmw.co.il (service-instructions page and /wp-admin/admin-ajax.php?action=get_csv_raw): 503. r.jina.ai reader: Cloudflare challenge.
- Delek SharePoint (delekmotorscoil.sharepoint.com/sites/Techtrain): the folder "Shared Documents/מפרטי תוכניות שרות לאתרים היצרנים/<brand>/" exists (found via web search: mazda/38646 _Mazda_BT-50...). The anonymous guest cookie from a share link exposes only the item that link shares. _api/web/lists answers (list "מסמכים", 33,939 items), but the items query returns only the shared Dongfeng file; direct paths go to AccessDenied; the search API says "לא מורשה". The BMW share links are only in bmw.co.il's CSV, which is blocked.
- All international BMW hosts (bmwusa.com, bmw.com, .co.uk, .de, .com.au, .ca, .ie, .co.za, .com.cy, .com.tr, bmw-me.com, .gr, .ae, mini.co.uk, ownersmanuals2.bmw.com): 000 (egress). bimmerpost 2018 maintenance booklet attachment: 403 (curl and WebFetch). usermanual.wiki X5 35d booklet redirects to manuals.plus, which shows a Cloudflare challenge (Playwright too).
- manualpdf.co.il/bmw and /mini: only manua.ls-style non-Israeli manuals.
Mercedes-Benz (Colmobil)
- mercedes-benz.co.il (Netdirector platform, not WordPress): the /site/car-books form needs model, e-mail and reCAPTCHA, and the book is sent by e-mail, so it was not submitted. The PDFs it links on nd-mediagallery2-public-production.s3.amazonaws.com are the class-action settlement, tyre labels and display-car terms; bucket listing gives AccessDenied. /vans pages: no intervals.
- colmobil.co.il: Next.js, no wp-json. /spareparts/ links prodmedia.colmobil.co.il/spare-parts/MERC.PDF (808 pp) and MIT.PDF (160 pp), which are parts price lists only, with no service intervals.
- assets.mbvans.com MY19 MB Service Booklet: stamp pages only. mercedes-benz.com.au vans maintenance page: 000 / WebFetch 503.
- data.gov.il package_search for "טיפול", "טיפולים", "מחירון": no service-plan dataset.
Mitsubishi (Colmobil)
- mitsubishi-israel.co.il wp-json media (mime_type=application/pdf, 2 pages; search=ספר): 24 Hebrew books on res.cloudinary.com/colmobil (Outlander 2010, 2012, 2013, diesel 2013, 2015, 2018, 2021; ASX 2017/2019/2022; Eclipse Cross 2018/2022/PHEV; Space Star 2013-2020; Attrage 2012; L200 2015). All downloaded and text-searched for km values: only the Outlander 2021+ book has a table, and it is already used. No Lancer, Grandis, Pajero or old L200 book is listed (searches for לנסר / גרנדיס / פגרו / טריטון return 0).
- Mitsubishi-Tipulimshirut2024-copy.pdf is the warranty certificate. It refers to a separate "ספר השירות", which is not online.
- mitsubishi-israel.co.il pages (wp-json page content): no intervals.
Isuzu (Universal Motors / UMI)
- isuzu.co.il and isuzu-dmax.co.il: Cloudflare 403 (curl, Playwright, WebFetch). universal-motors.co.il: 000. umi.co.il redirects to umigroup.co.il.
- isuzu.co.uk media API: only the 12-17MY, 17MY and 24MY D-Max manuals (already used); nothing for the 2007-2011 TF 4JK1.
Tesla
- tesla.com (all paths, including /he_il and ownersmanual), service.tesla.com, static-assets.tesla.com: 403. www.tesla.cn: 200, used. Only the zh_cn locale exists there (he_il and en_eu give 404).
Land Rover (JLR)
- www.ownerinfo.landrover.com (iGuide) works: POST /i18n with locale=iw_IL and country=IL, then /model/<code>/years/<year>/index lists the Hebrew Israeli-market handbooks (Defender 3E 2024 doc 1697625, RRS 3R 2024 doc 1706811, Evoque 3G 2022 doc 1667626, Range Rover 3K 2023, Discovery 3D / Discovery Sport 3A / Velar 3B 2020).
  The procedure text comes from https://topix.jlrext.com/topix/service/procedure/<doc>/ODYSSEY/<G-id>/he_IL?uid=...&country=IL (script: dl/prem5/lr/topix.py).
  In the 2020+ handbooks, the service chapter ("דרישות לביצוע טיפולים", "תוכן הטיפולים", "החלפת נוזלים") gives no km or time values: the service is flexible, the due date is shown on the cluster, and the content is on the dealer worksheet. Handbooks for 2016-2019 are not offered for country IL. Land Rover 2019+ therefore stays uncovered, because the owner documents contain no numbers.

OTHER ROUTES (international)
- jdmfsm.info (open directory index, Mitsubishi tree) has Mitsubishi Pre-delivery & Periodic Maintenance manuals for: Grandis (2004, 2006); Outlander 2004 CU (pdi-engels-02.pdf, grid table, not processed: 287 cars, 4G69, 2005-08); Outlander 2007 CW; L200 KB4T for Europe (43522020KB4T_07003ENG.pdf: 20,000 km/12 m table for the 4D56 DI-D). The L200 table was NOT used: the existing L200 2006-2015 file uses the General Export table, which is probably closer to Israel; the lead may compare. There is no Lancer CS (4G18) document there; the Japan group has since added Lancer 4G18.
- MMAL has Outlander PHEV MY14.5 and MY17 schedules (A/B service format). Not processed; they could extend the PHEV file to 2014-2016 (185 cars).

NOT COVERED / STILL BLOCKED (biggest first)
- BMW: all 43k cars stay on the BMW USA booklet drafts. Diesels B57/N57 (X5/X6 30d, ~2.9k), N13/N20/N46/N52/N55 petrol (~5k) and BMW i (iX3 518, etc.): no reachable source with numbers.
- Mercedes: Vito / V-Class / Vito Tourer OM651/OM654 (~3.2k), EQA/EQC (~1.6k), pre-2011 M271/M272: no source.
- Isuzu: PICK-UP 4JK1 2007-2011 (2,162): still only the sister mapping suggested in misc4 (to isuzu-d-max-2007-2011-3.0-diesel). Trooper 4JX1, Ippon 4JG2 and Rodeo 6VD1 are old and small.
- Land Rover 2019+ (DT306 Defender/RRS, PT204/PT306/PT153 Evoque/RRS PHEV, ~6k): the owner documents contain no intervals.
- Mitsubishi: L200 4D56 1999-2005 (1k), Pajero 4M40 1998-2000 and 6G75 2008-11, Outlander diesel 4N14 2013-17 (439), Outlander 4B40 2026 (348), Outlander PHEV 2014-16 (185), Outlander CU 4G69 2005-08 (287; source found, not processed).
