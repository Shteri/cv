// Tests for app/lookup.js resolver using mocked registry records (no network).
import { readFileSync } from "node:fs";
const root = new URL("../", import.meta.url).pathname;
await import(root + "app/lookup.js");
const L = globalThis.TipulitLookup;
const rules = JSON.parse(readFileSync(root + "data/gov-match.json", "utf8")).rules;
const schedIds = new Set(JSON.parse(readFileSync(root + "app/data.js", "utf8").replace(/^.*?= /s, "").replace(/;\s*$/, "")).schedules.map(s => s.id));

const rec = (o) => L.normalizeRecord({ mispar_rechev: 1234567, tozeret_nm: "", kinuy_mishari: "", degem_nm: "", shnat_yitzur: 2020, sug_delek_nm: "בנזין", nefach_manoa: 1600, tokef_dt: "2027-03-01T00:00:00", mivchan_acharon_dt: "2026-02-20T00:00:00", ...o });
const cases = [
  [rec({ tozeret_nm: "טויוטה יפן", kinuy_mishari: "COROLLA", degem_nm: "ZRE212L-DEXNKW", shnat_yitzur: 2021, sug_delek_nm: "חשמל/בנזין", nefach_manoa: 1798 }), "toyota-corolla-2019-2025-1.8-hybrid"],
  [rec({ tozeret_nm: "טויוטה טורקיה", kinuy_mishari: "COROLLA", shnat_yitzur: 2016, nefach_manoa: 1598 }), "toyota-corolla-2013-2019-1.6"],
  [rec({ tozeret_nm: "טויוטה יפן", kinuy_mishari: "COROLLA CROSS", shnat_yitzur: 2023, sug_delek_nm: "חשמל/בנזין", nefach_manoa: 1798 }), "unsupported_model"],
  [rec({ tozeret_nm: "טויוטה צרפת", kinuy_mishari: "YARIS", shnat_yitzur: 2018, nefach_manoa: 1329 }), "toyota-yaris-2011-2020"],
  [rec({ tozeret_nm: "יונדאי קוריאה", kinuy_mishari: "I10", shnat_yitzur: 2017, nefach_manoa: 1248 }), "hyundai-i10-2014-2019"],
  [rec({ tozeret_nm: "יונדאי קוריאה", kinuy_mishari: "I20", shnat_yitzur: 2022, nefach_manoa: 998 }), "unsupported_model"],
  [rec({ tozeret_nm: "יונדאי קוריאה", kinuy_mishari: "I25", shnat_yitzur: 2015, nefach_manoa: 1396 }), "hyundai-i25-2011-2018"],
  [rec({ tozeret_nm: "קיה קוריאה", kinuy_mishari: "PICANTO", shnat_yitzur: 2020, nefach_manoa: 998 }), "kia-picanto-2017-2025"],
  [rec({ tozeret_nm: "קיה סלובקיה", kinuy_mishari: "SPORTAGE", shnat_yitzur: 2018, nefach_manoa: 1591 }), "kia-sportage-2016-2021"],
  [rec({ tozeret_nm: "מאזדה יפן", kinuy_mishari: "3", degem_nm: "BM5", shnat_yitzur: 2015, nefach_manoa: 1496 }), "mazda-3-2013-2025"],
  [rec({ tozeret_nm: "מאזדה יפן", kinuy_mishari: "CX-5", shnat_yitzur: 2019, nefach_manoa: 1998 }), "unsupported_model"],
  [rec({ tozeret_nm: "סקודה צ'כיה", kinuy_mishari: "OCTAVIA", shnat_yitzur: 2019, nefach_manoa: 1395 }), "skoda-octavia-2013-2025"],
  [rec({ tozeret_nm: "ב.מ.וו גרמניה", kinuy_mishari: "320I", shnat_yitzur: 2019, nefach_manoa: 1998 }), "unsupported_make"],
  [rec({ tozeret_nm: "טסלה ארה\"ב", kinuy_mishari: "MODEL 3", shnat_yitzur: 2022, sug_delek_nm: "חשמל", nefach_manoa: 0 }), "electric"],
  [null, "unknown"]
];
let fail = 0;
for (const [v, expected] of cases) {
  const r = L.resolveSchedule(v, rules);
  const got = r.status === "matched" ? r.schedule : r.status;
  const ok = got === expected;
  if (!ok) fail++;
  console.log(`${ok ? "ok " : "FAIL"} ${v ? v.make_raw + " " + v.commercial_name + " " + v.year : "null"} -> ${got}${r.ambiguous ? " (ambiguous: " + r.ambiguous.join(",") + ")" : ""}`);
}
for (const r of rules) if (!schedIds.has(r.schedule)) { fail++; console.log("FAIL rule points to missing schedule", r.schedule); }
console.log(`plate normalize: ${L.normalizePlate("12-345-67")} ${L.normalizePlate("123-45-678")}`);
console.log(fail ? `${fail} failure(s)` : "all lookup tests passed");
process.exit(fail ? 1 : 0);
