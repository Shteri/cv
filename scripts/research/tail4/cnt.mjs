import { readFileSync } from "node:fs";
import { normalizeMake } from "/home/user/cv/scripts/lookup_plate.mjs";
const agg = JSON.parse(readFileSync("/home/user/cv/data/sources/registry-counts.json", "utf8"));
const BASE = JSON.parse(readFileSync("/home/user/cv/data/registry_map.json", "utf8")).rules;
const EX = JSON.parse(readFileSync("/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/tail4/registry/registry_rules.json", "utf8"));
function m(MAP, v) {
  const name = v.model_name.toUpperCase().trim(), year = Number(v.year);
  const c = MAP.filter(r => r.make === v.make && r.names.some(n => n === name) && year >= r.years[0] && year <= r.years[1] && (!r.fuel || r.fuel.includes(v.fuel)) && (!r.engine_codes || r.engine_codes.includes(v.engine_code)));
  c.sort((a, b) => (b.engine_codes ? 2 : 0) + (b.fuel ? 1 : 0) - ((a.engine_codes ? 2 : 0) + (a.fuel ? 1 : 0)));
  return c[0]?.schedule ?? null;
}
const ALL = BASE.concat(EX); const ids = new Set(process.argv.slice(2)); const per = {};
for (const r of agg.model_year_fuel_engine) {
  const s = m(ALL, { make: normalizeMake(r.make), model_name: r.model, year: r.year, fuel: r.fuel, engine_code: r.engine });
  if (s && ids.has(s)) per[s] = (per[s] || 0) + r.n;
}
for (const [k, n] of Object.entries(per).sort((a, b) => b[1] - a[1])) console.log(n, k);
