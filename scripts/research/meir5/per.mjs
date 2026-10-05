import { readFileSync, readdirSync } from "node:fs";
import { normalizeMake } from "/home/user/cv/scripts/lookup_plate.mjs";
import { matchSchedule } from "/home/user/cv/scripts/match_schedule.mjs";
const S="/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/meir5/";
const ids=new Set(readdirSync(S).filter(f=>f.endsWith('.json')).map(f=>f.slice(0,-5)));
const agg = JSON.parse(readFileSync("/home/user/cv/data/sources/registry-counts.json", "utf8"));
const per={};
for (const v of agg.model_year_fuel_engine) {
  const s = matchSchedule({ make: normalizeMake(v.make), model_name: v.model, year: v.year, fuel: v.fuel, engine_code: v.engine });
  const id = s && (s.id || s.schedule || s);
  if (id && ids.has(id)) per[id]=(per[id]||0)+v.n;
}
for (const id of ids) console.log(per[id]||0, id);
