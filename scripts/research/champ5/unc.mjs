import { readFileSync } from "node:fs";
import { normalizeMake } from "/home/user/cv/scripts/lookup_plate.mjs";
import { matchSchedule } from "/home/user/cv/scripts/match_schedule.mjs";
const agg = JSON.parse(readFileSync("/home/user/cv/data/sources/registry-counts.json", "utf8"));
const makes = new Set(["Volkswagen","Audi","Skoda","Seat","Cupra"]);
const out = {};
for (const r of agg.model_year_fuel_engine) {
  const mk = normalizeMake(r.make); if (!makes.has(mk)) continue;
  const s = matchSchedule({ make: mk, model_name: r.model, year: r.year, fuel: r.fuel, engine_code: r.engine });
  if (s) continue;
  const k = `${mk} | ${r.model} | ${r.fuel} | ${r.engine}`;
  const e = out[k] ??= { n: 0, y: {} }; e.n += r.n; e.y[r.year] = (e.y[r.year]||0) + r.n;
}
for (const [k, e] of Object.entries(out).sort((a,b)=>b[1].n-a[1].n).slice(0, +process.argv[2]||60))
  console.log(e.n, k, JSON.stringify(e.y));
