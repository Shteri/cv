// Which registered models still lack a maintenance schedule? Ranks by vehicle count.
//   node scripts/registry_coverage.mjs [limit]
// Reads data/sources/registry-counts.json and applies data/registry_map.json through
// matchSchedule(), using each model's most common fuel and engine code.
import { readFileSync } from "node:fs";
import { normalizeMake } from "./lookup_plate.mjs";
import { matchSchedule } from "./match_schedule.mjs";

const root = new URL("../data/", import.meta.url).pathname;
const agg = JSON.parse(readFileSync(root + "sources/registry-counts.json", "utf8"));
const limit = Number(process.argv[2] || 80);
const fuel = {}, eng = {};
for (const r of agg.model_fuel) { const k = r.make + "|" + r.model; fuel[k] ??= r.fuel; }
for (const r of agg.model_engine) { const k = r.make + "|" + r.model; eng[k] ??= r.engine; }
const byModel = {}; let covered = 0, total = 0;
for (const r of agg.model_year) {
  const mk = normalizeMake(r.make), k = r.make + "|" + r.model;
  const s = matchSchedule({ make: mk, model_name: r.model, year: r.year, fuel: fuel[k], engine_code: eng[k] });
  const e = byModel[mk + " | " + r.model] ??= { n: 0, covered: 0, years: {}, fuel: fuel[k], eng: eng[k] };
  e.n += r.n; total += r.n;
  if (s) { e.covered += r.n; covered += r.n; } else e.years[r.year] = (e.years[r.year] || 0) + r.n;
}
console.log(`snapshot ${agg.snapshot}: ${total} vehicles in model_year rows, ${covered} covered (${(100 * covered / total).toFixed(1)}%)`);
const rows = Object.entries(byModel).map(([k, e]) => ({ k, ...e, unc: e.n - e.covered })).sort((a, b) => b.unc - a.unc);
console.log("\nuncovered / total  model [fuel, engine]  years:count (>=300)");
for (const r of rows.slice(0, limit)) {
  const yrs = Object.entries(r.years).filter(([, n]) => n >= 300).sort().map(([y, n]) => `${y}:${n}`).join(" ");
  console.log(`${r.unc} / ${r.n}  ${r.k} [${r.fuel}, ${r.eng}]  ${yrs}`);
}
const byMake = {};
for (const r of rows) { const m = r.k.split(" | ")[0]; const e = byMake[m] ??= { n: 0, unc: 0 }; e.n += r.n; e.unc += r.unc; }
console.log("\nuncovered / total by make");
for (const [m, e] of Object.entries(byMake).sort((a, b) => b[1].unc - a[1].unc).slice(0, 25)) console.log(`${e.unc} / ${e.n}  ${m}`);
