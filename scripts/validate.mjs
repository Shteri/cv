// Minimal validator for data/schedules/*.json. No dependencies.
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const root = new URL("../data/", import.meta.url).pathname;
const items = JSON.parse(readFileSync(join(root, "items.json"), "utf8"));
const dir = join(root, "schedules");
const required = ["id","make","model","years","engines","importer","interval","cycle_km","services","sources","status"];
const actions = new Set(["replace","inspect","adjust","clean","rotate"]);
let errors = 0;

for (const file of readdirSync(dir).filter(f => f.endsWith(".json"))) {
  const s = JSON.parse(readFileSync(join(dir, file), "utf8"));
  const fail = msg => { errors++; console.error(`${file}: ${msg}`); };
  for (const k of required) if (!(k in s)) fail(`missing ${k}`);
  if (s.id && file !== `${s.id}.json`) fail(`filename should be ${s.id}.json`);
  if (!Array.isArray(s.years) || s.years.length !== 2) fail("years must be [first,last]");
  if (!s.interval?.km || !s.interval?.months) fail("interval needs km and months");
  if (!Array.isArray(s.sources) || s.sources.length === 0) fail("needs at least one source");
  let prevKm = 0;
  for (const svc of s.services ?? []) {
    if (svc.km <= prevKm) fail(`services must be ascending, got ${svc.km} after ${prevKm}`);
    prevKm = svc.km;
    if (s.interval?.km && svc.km % s.interval.km !== 0) fail(`${svc.km} is not a multiple of interval ${s.interval.km}`);
    for (const it of svc.items ?? []) {
      if (!items[it.item]) fail(`unknown item '${it.item}' at ${svc.km}`);
      if (!actions.has(it.action)) fail(`bad action '${it.action}' for ${it.item} at ${svc.km}`);
    }
  }
  if (prevKm && s.cycle_km && prevKm > s.cycle_km) fail(`last service ${prevKm} exceeds cycle_km ${s.cycle_km}`);
  for (const t of s.time_based ?? []) if (!items[t.item]) fail(`unknown time_based item '${t.item}'`);
}
console.log(errors ? `${errors} error(s)` : "all schedules valid");
process.exit(errors ? 1 : 0);
