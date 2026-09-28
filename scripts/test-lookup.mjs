// Tests for app/lookup.js resolver using mocked registry records and data/registry_map.json (no network).
import { readFileSync, readdirSync } from "node:fs";
const root = new URL("../", import.meta.url).pathname;
await import(root + "app/lookup.js");
const L = globalThis.TipulitLookup;
const rules = JSON.parse(readFileSync(root + "data/registry_map.json", "utf8")).rules;
const schedIds = new Set(readdirSync(root + "data/schedules").filter(f => f.endsWith(".json")).map(f => f.replace(/\.json$/, "")));

const rec = o => L.normalizeRecord({ mispar_rechev: 1234567, tozeret_nm: "", kinuy_mishari: "", degem_nm: "", degem_manoa: "", shnat_yitzur: 2020, sug_delek_nm: "בנזין", nefach_manoa: 1600, tokef_dt: "2027-03-01T00:00:00", ...o });
const cases = [
  [rec({ tozeret_nm: "טויוטה יפן", kinuy_mishari: "COROLLA HSD SDN", degem_manoa: "2ZR", shnat_yitzur: 2021 }), "toyota-corolla-2019-2025-1.8-hybrid"],
  [rec({ tozeret_nm: "טויוטה טורקיה", kinuy_mishari: "COROLLA", shnat_yitzur: 2016 }), "toyota-corolla-2013-2019-1.6"],
  [rec({ tozeret_nm: "טויוטה יפן", kinuy_mishari: "COROLLA CROSS", shnat_yitzur: 2023 }), "toyota-corolla-cross-2022-2025-1.8-hybrid"],
  [rec({ tozeret_nm: "יונדאי קוריאה", kinuy_mishari: "I10", degem_manoa: "G4LA", shnat_yitzur: 2017 }), "hyundai-i10-2014-2019"],
  [rec({ tozeret_nm: "קיה קוריאה", kinuy_mishari: "PICANTO", shnat_yitzur: 2020 }), "kia-picanto-2017-2025"],
  [rec({ tozeret_nm: "מזדה יפן", kinuy_mishari: "MAZDA 3", shnat_yitzur: 2015 }), "mazda-3-2013-2019"],
  [rec({ tozeret_nm: "סקודה צ'כיה", kinuy_mishari: "OCTAVIA", shnat_yitzur: 2019 }), "skoda-octavia-2013-2025"],
  [rec({ tozeret_nm: "ב.מ.וו גרמניה", kinuy_mishari: "320I", shnat_yitzur: 2019 }), "unsupported_make"],
  [rec({ tozeret_nm: "טויוטה יפן", kinuy_mishari: "LAND CRUISER", shnat_yitzur: 2019 }), "unsupported_model"],
  [rec({ tozeret_nm: "טסלה ארה\"ב", kinuy_mishari: "MODEL 3", shnat_yitzur: 2022, sug_delek_nm: "חשמל" }), "electric"],
  [null, "unknown"]
];
let fail = 0;
for (const [v, expected] of cases) {
  const r = L.resolveSchedule(v, rules);
  const got = r.status === "matched" ? r.schedule : r.status;
  const ok = got === expected; if (!ok) fail++;
  console.log(`${ok ? "ok " : "FAIL"} ${v ? v.make_raw + " " + v.commercial_name + " " + v.year : "null"} -> ${got}${ok ? "" : " (expected " + expected + ")"}`);
}
for (const r of rules) if (!schedIds.has(r.schedule)) { fail++; console.log("FAIL rule points to missing schedule", r.schedule); }
const unmapped = [...schedIds].filter(id => !rules.some(r => r.schedule === id));
console.log(`schedules without a registry rule: ${unmapped.length}${unmapped.length ? " (" + unmapped.join(", ") + ")" : ""}`);
console.log(fail ? `${fail} failure(s)` : "all lookup tests passed");
process.exit(fail ? 1 : 0);
