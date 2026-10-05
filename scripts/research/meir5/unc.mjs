import { readFileSync } from "node:fs";
import { normalizeMake } from "/home/user/cv/scripts/lookup_plate.mjs";
import { matchSchedule } from "/home/user/cv/scripts/match_schedule.mjs";
const agg = JSON.parse(readFileSync("/home/user/cv/data/sources/registry-counts.json", "utf8"));
const want = new Set(process.argv.slice(2));
const per = {};
for (const v of agg.model_year_fuel_engine) {
  const mk = normalizeMake(v.make); if (!want.has(mk)) continue;
  if (matchSchedule({ make: mk, model_name: v.model, year: v.year, fuel: v.fuel, engine_code: v.engine })) continue;
  const k = `${mk} | ${v.model} | ${v.fuel} | ${v.engine}`; (per[k] ??= {n:0,y:{}}); per[k].n += v.n; per[k].y[v.year]=(per[k].y[v.year]||0)+v.n;
}
for (const [k,e] of Object.entries(per).sort((a,b)=>b[1].n-a[1].n)) if (e.n>=60) console.log(e.n, k, JSON.stringify(e.y));
