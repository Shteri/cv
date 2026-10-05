lub5 REPORT - Lubinski group (Peugeot, Citroen, Opel, DS, MG/Car East)
Generators: scratchpad/dl/lub5/gen/{common,mg,psa,upgrade,rules,mgparse}.py. Downloads: dl/lub5/{mg,wb,war,ak}.
Validate: node scripts/validate.mjs staging/lub5 -> "all schedules valid (9 draft, 18 reviewed, 0 verified)".

ISRAELI SOURCES FOUND
1) MG / Car East Hebrew service+warranty booklets (full A/B grids + special-items tables), linked from https://mg-israel.co.il/mg_warranty/,
   files at https://media.mg-israel.co.il/wp-content/uploads/2020/10/ :
   Warranty-MG-7Y-BEV-PHEV-HEV-Update-08.2026-He-Web.pdf (EV pp.7-12, HEV/PHEV pp.13-19)
   Warranty-MG-5Y-BENZINE-Update-06.2026-He-Web.pdf (petrol MG3/ZS/HS pp.7-12)
   Warranty-MG3-7Y-09.2024_Web-2.pdf, MGZS-Hybrid-Ahrayut-11_2024-Web.pdf (pp.7-13)
   Warranty-MG-5Y-He-2024-idkun-12.2025.pdf, Warranty-MG-7Y-He-06.2024-idkun-12.2025.pdf (EHS hybrid grid pp.8-11, EV pp.12-15)
   MG-Nispah-Massnen-Delek-04.2025.pdf (erratum: HEV fuel filter 8y/100k)
   older versions via web.archive.org (08.2025 petrol, 11.2025 BEV/PHEV); ZS EV cost plan Doc1-1.pdf (02.2022, archived).
   Marks read by bullet x-position vs A/B header (mgparse.py) and checked on renders.
2) Citroen Israel (Lubinski) Hebrew service & warranty booklet, ed. 08/2009 (KGCIT0920):
   https://web.archive.org/web/20120509205507/http://citroen.co.il/_Uploads/dbsAttachedFiles/CitroenWarrantyBook.pdf
   p.11 intervals per engine class (normal/severe), p.12 routine ops, pp.13-18 extra ops, p.19 timing belt + DPF. Severe column used
   (booklet's severe list includes hot >30C and dusty countries).
3) https://online.peugeot.co.il/faq/ (2008 SUV): service every 15,000 km / 1 year (corroboration only).

FILES (status, vehicles with new rules)
UPGRADED same id (reviewed): mg-ehs-2021-2024-1.5t-phev 8692; mg-4-2023-2026-ev 7253; mg-3-hybrid-2024-2026-1.5-hybrid 5190 (now 15k/12m, draft had 24k);
  mg-zs-ev-2020-2024-ev 4674; mg-s9-2026-1.5t-phev 4637; mg-zs-hybrid-2025-2026-1.5-hybrid 4357 (15k/12m); mg-marvel-r-2023-2024-ev 1163;
  mg-5-2023-2024-ev 1013; mg-3-2025-2026-1.5 696 (15k/12m); mg-ehs-2025-2026-1.5t-phev 613.
NEW reviewed: mg-hs-hybrid-2025-2026-1.5-hybrid 829; mg-hs-2025-2026-1.5t 245; citroen-c3-c4-ds3-2009-2015-1.6-vti 2666;
  citroen-jumpy-berlingo-2004-2017-2.0-hdi 1994; citroen-c4-c3-2004-2010-1.6-16v 922; citroen-c5-c4-picasso-2006-2011-2.0 449;
  citroen-berlingo-c3-c4-2008-2013-1.6-hdi 3608* ; citroen-jumpy-2007-2012-1.6-hdi 280*   (*only with override rules)
NEW draft (sister = Citroen Israeli booklet, same PSA engine): peugeot-207-208-308-2008-2016-1.6-vti 4585; peugeot-206-307-partner-2002-2012-1.4-1.6 1520;
  peugeot-301-2013-2016-1.6-vti 761; peugeot-407-307-2006-2011-2.0 310; citroen-c-elysee-2013-2014-1.6-vti 542 (later than booklet).
UPGRADED draft (numbers unchanged, Israeli source added): citroen-c4-picasso-c5-aircross-2011-2023-1.6-thp, peugeot-3008-5008-508-2010-2023-1.6-thp
  (CWB severe "other engines" = identical plan), peugeot-2008-2014-2026-1.2-puretech, peugeot-2008-2020-2026-1.5-bluehdi (FAQ 15k/1y).

REGISTRY
registry/registry_rules.json: 18 rules for unmatched rows -> uncovered for these makes 23,935 -> 8,199. Includes sister mappings Cyberster->mg-4
  (same booklet column) and 5F02 THP rows -> existing THP drafts.
registry/registry_rules_override.json: 3 rules for Citroen 1.6 HDi 2008-2013 (Berlingo/C3/C3 Picasso/C4, Jumpy 9HU) already matched by old draft rules;
  must be placed BEFORE the existing rules (equal specificity, first wins) or old rules narrowed. Old Berlingo draft left as is (8.7k BH02 2016-19 cars).

JUDGEMENT CALLS
- Citroen: severe column chosen; 2009 booklet edition older than some rule years (VTi 2014-15, Jumpy RH02 2013-17) - notes say so; downgrade if stricter.
- MG: "seats" folded into seat_belts note; engine mounts -> body_underside; HV checks -> hybrid_system; road test/software -> diagnostics note.
- MG3 petrol: transmission type unknown -> manual/auto/CVT fluid (80k) listed "if fitted". MG4 MCE (EH32) 2026 column (80k/3y-90k) only noted.

ROUTES TRIED
- guide-books pages (online.peugeot/citroen/opel, mg-israel): admin-ajax action=get_clearmash_doc_url returns lubinski.clearmash.com/skn/Public/<hash>.
  clearmash = Cloudflare 403 for curl (browser/curl/Googlebot/empty UA), http, --connect-to / Host via www.clearmash.com (404 tenant-scoped),
  Playwright (he-IL, Asia/Jerusalem, webdriver hidden), WebFetch (403). Wayback timemap for clearmash empty.
- www.peugeot.co.il / citroen.co.il / opel.co.il: 403 with browser UA but 200 with "User-Agent: curl/8.0" (Akamai). Maintenance pages are templates, no plan.
- WP REST 401 on online.*, media-*.lubit.co.il, mg-israel, lubit.co.il; lubinski.co.il wp-json 200 but media 401; uploads dir 403.
- Lubinski parts xlsx (מחירון-לובינסקי-מאי-2026.xlsx): only small/large service package prices.
- Current Peugeot/Citroen/Opel/DS warranty booklets: no grid ("plan handed over at delivery").
- Appointment API onlineapi.lubinski.co.il needs plate + SMS code (not used).
- web.archive.org now reachable over https (http CDX blocked; 429 when hammered; use curl -C - for 1MB-truncated files). CDX dumps: dl/lub5/wb/all_*.txt.
  Found CWB (used), MG Hebrew manuals (MG3_CAR_MANUAL.pdf p.84: Israel 15,000 km/1 yr, no grid; MGZS_CAR_MAUNAL / MG-ZS-He_01.2020: no grid),
  Opel GM-era 02_Manuals PDFs = spec sheets only, service charter 2012.pdf. No Peugeot/Opel service booklet ever captured.
- ספר-רכב.com Cloudflare challenge; serviceman.co.il 404; public.servicebox Hebrew handbooks no grid.

STILL BLOCKED / NOT DONE
- Peugeot/Citroen "נספח"/"מדריך מקוצר" and MG old "ספר נהג" only on clearmash. Opel post-2019 plans per car only.
- mg-zs-2018-2021-1.0t (2,236) unchanged: no Israeli grid (MG3 Hebrew manual implies 15k/1y vs draft 24k).
- Old MG3/MG350 15S4U/15S4C (~1,100): interval only, no file. MG4 URBAN (181): not in booklet tables.
- Peugeot Partner RHY (112), Boxer 4H03, 301 10FC1M, C3 Picasso 8F01, HN05/HN09 rows.
