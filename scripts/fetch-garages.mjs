// Downloads the Ministry of Transport licensed-garage registry from data.gov.il and writes a compact
// directory to data/garages.json (bundled into the site as garages.json, loaded on demand by the app).
// Source: dataset "musachim" (CC-BY), one row per garage x licensed profession. We keep passenger-car
// garages and test institutes, drop tractor/forklift/truck/motorcycle-only shops, and group per garage.
// Usage: node scripts/fetch-garages.mjs [--from <raw.json>]   (the flag reuses a saved datastore_search dump)
import { readFileSync, writeFileSync } from "node:fs";
const RESOURCE = "bb68386a-a331-4bbc-b668-bba2766d517d";
const root = new URL("../", import.meta.url).pathname;
const args = process.argv.slice(2);
let raw;
if (args[0] === "--from") raw = JSON.parse(readFileSync(args[1], "utf8"));
else {
  const url = `https://data.gov.il/api/3/action/datastore_search?resource_id=${RESOURCE}&limit=32000`;
  const res = await fetch(url, { headers: { accept: "application/json" } });
  if (!res.ok) throw new Error("data.gov.il " + res.status);
  raw = await res.json();
}
const rows = raw.result.records;
if (rows.length < 5000) throw new Error("suspiciously few rows: " + rows.length);
// Profession codes that mean "cars". Anything else (tractors, forklifts, trucks, bikes, tachographs...) is ignored.
const CAR = new Set([10, 15, 20, 22, 23, 30, 33, 60, 70, 80, 81, 90, 91, 100, 130, 135, 140, 142, 143, 144, 145, 175, 177, 180, 181, 195, 202, 205, 206, 300]);
const clean = s => String(s || "").replace(/\s+/g, " ").replace(/\)([^()]*)\)/g, "($1)").trim();
const cleanName = s => clean(s).replace(/(^|\s)בע ?["']? ?מ(?=\s|$)/g, '$1בע"מ');
const cleanCity = s => clean(s).replace(/\s*-\s*/g, "-");
const by = new Map();
for (const r of rows) {
  if (!CAR.has(+r.cod_miktzoa)) continue;
  const id = +r.mispar_mosah;
  const g = by.get(id) || { i: id, n: cleanName(r.shem_mosah), c: cleanCity(r.yishuv), a: clean(r.ktovet), p: clean(r.telephone), t: +r.cod_sug_mosah, k: [] };
  if (!g.k.includes(+r.cod_miktzoa)) g.k.push(+r.cod_miktzoa);
  by.set(id, g);
}
const garages = [...by.values()].filter(g => g.n && g.c).sort((a, b) => a.c.localeCompare(b.c, "he") || a.n.localeCompare(b.n, "he"));
const cityCount = {};
for (const g of garages) cityCount[g.c] = (cityCount[g.c] || 0) + 1;
const cities = Object.entries(cityCount).sort((a, b) => b[1] - a[1]).map(([c, n]) => [c, n]);
const out = { updated: new Date().toISOString().slice(0, 10), source: "data.gov.il/dataset/musachim", cities, garages: garages.map(g => [g.i, g.n, g.c, g.a, g.p, g.t, g.k]) };
writeFileSync(root + "data/garages.json", JSON.stringify(out));
console.log(`garages: ${garages.length} in ${cities.length} cities (from ${rows.length} rows) -> data/garages.json ${Math.round(JSON.stringify(out).length / 1024)} KB`);
