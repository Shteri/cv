// Plate -> registry record -> schedule id. Usage:
//   node scripts/match_schedule.mjs 6895239
// Prints the registry fields and the matched schedule (or null).
import { readFileSync } from "node:fs";
import { lookupPlate } from "./lookup_plate.mjs";

const root = new URL("../data/", import.meta.url).pathname;
const MAP = JSON.parse(readFileSync(root + "registry_map.json", "utf8")).rules;

export function matchSchedule(v) {
  if (!v) return null;
  const name = (v.model_name || "").toUpperCase().trim();
  const year = Number(v.year);
  const candidates = MAP.filter(r =>
    r.make === v.make &&
    r.names.some(n => n === name) &&
    year >= r.years[0] && year <= r.years[1] &&
    (!r.fuel || r.fuel.includes(v.fuel)) &&
    (!r.engine_codes || r.engine_codes.includes(v.engine_code))
  );
  // prefer the most specific rule
  candidates.sort((a, b) => (b.engine_codes ? 2 : 0) + (b.fuel ? 1 : 0) - ((a.engine_codes ? 2 : 0) + (a.fuel ? 1 : 0)));
  return candidates[0]?.schedule ?? null;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const v = await lookupPlate(process.argv[2]);
  const schedule = matchSchedule(v);
  console.log(JSON.stringify({ vehicle: v, schedule }, null, 2));
  if (!schedule) process.exit(1);
}
