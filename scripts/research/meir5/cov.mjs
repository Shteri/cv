import { readFileSync, existsSync } from "node:fs";
import { normalizeMake } from "/home/user/cv/scripts/lookup_plate.mjs";
import { matchSchedule } from "/home/user/cv/scripts/match_schedule.mjs";
const S = "/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/meir5/";
const agg = JSON.parse(readFileSync("/home/user/cv/data/sources/registry-counts.json", "utf8"));
const rules = JSON.parse(readFileSync(S + "registry/registry_rules.json", "utf8"));
const per = {}; let tot = 0;
for (const r of rules) if (!existsSync(S + r.schedule + ".json") && !existsSync("/home/user/cv/data/schedules/" + r.schedule + ".json")) console.log("MISSING schedule", r.schedule);
for (const v of agg.model_year_fuel_engine) {
  const mk = normalizeMake(v.make);
  const q = { make: mk, model_name: v.model, year: v.year, fuel: v.fuel, engine_code: v.engine };
  if (matchSchedule(q)) continue;
  const name = v.model.toUpperCase().trim(), y = Number(v.year);
  const c = rules.filter(r => r.make === mk && r.names.includes(name) && y >= r.years[0] && y <= r.years[1] && (!r.fuel || r.fuel.includes(v.fuel)) && (!r.engine_codes || r.engine_codes.includes(v.engine)));
  c.sort((a, b) => (b.engine_codes ? 2 : 0) + (b.fuel ? 1 : 0) - ((a.engine_codes ? 2 : 0) + (a.fuel ? 1 : 0)));
  if (c[0]) { per[c[0].schedule] = (per[c[0].schedule] || 0) + v.n; tot += v.n; }
}
for (const [k, n] of Object.entries(per).sort((a, b) => b[1] - a[1])) console.log(n, k);
console.log("TOTAL newly covered", tot);
