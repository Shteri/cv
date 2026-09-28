// Minimal validator for data/schedules/*.json. No dependencies.
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const root = new URL("../data/", import.meta.url).pathname;
const items = JSON.parse(readFileSync(join(root, "items.json"), "utf8"));
const dir = process.argv[2] ?? join(root, "schedules");  // optional: validate a staging dir
const required = ["id","make","model","years","engines","importer","interval","cycle_km","services","sources","status"];
const actions = new Set(["replace","inspect","adjust","clean","rotate"]);
const statuses = new Set(["draft","reviewed","verified"]);
const fuels = new Set(["petrol","diesel","hybrid","plug-in-hybrid","electric","petrol-or-diesel"]);
const specKeys = new Set(["engine_oil","oil_capacity","coolant","brake_fluid","fuel","tires","tire_pressure","battery","timing","spare","wipers","warranty","_note"]);
let errors = 0;
const counts = { draft: 0, reviewed: 0, verified: 0 };

for (const file of readdirSync(dir).filter(f => f.endsWith(".json"))) {
  const s = JSON.parse(readFileSync(join(dir, file), "utf8"));
  const fail = msg => { errors++; console.error(`${file}: ${msg}`); };
  for (const k of required) if (!(k in s)) fail(`missing ${k}`);
  if (s.id && file !== `${s.id}.json`) fail(`filename should be ${s.id}.json`);
  if (!Array.isArray(s.years) || s.years.length !== 2) fail("years must be [first,last]");
  if (!s.interval?.km || !s.interval?.months) fail("interval needs km and months");
  if (!Array.isArray(s.sources) || s.sources.length === 0) fail("needs at least one source");
  if (s.fuel !== undefined && !fuels.has(s.fuel)) fail(`bad fuel '${s.fuel}'`);
  if (!statuses.has(s.status)) fail(`bad status '${s.status}'`); else counts[s.status]++;
  const first = s.first_service_km ?? s.interval?.km;
  let prevKm = 0;
  for (const svc of s.services ?? []) {
    if (svc.km <= prevKm) fail(`services must be ascending, got ${svc.km} after ${prevKm}`);
    prevKm = svc.km;
    if (s.interval?.km && (svc.km - first) % s.interval.km !== 0) fail(`${svc.km} is not ${first} + n*${s.interval.km}`);
    for (const it of svc.items ?? []) {
      if (!items[it.item]) fail(`unknown item '${it.item}' at ${svc.km}`);
      if (!actions.has(it.action)) fail(`bad action '${it.action}' for ${it.item} at ${svc.km}`);
    }
  }
  if (prevKm && s.cycle_km && prevKm > s.cycle_km) fail(`last service ${prevKm} exceeds cycle_km ${s.cycle_km}`);
  for (const t of s.time_based ?? []) if (!items[t.item]) fail(`unknown time_based item '${t.item}'`);
  // Item notes are shown to drivers. Transcriber remarks belong in `notes` / sources[].note, which the bundler strips.
  const devWords = /לא אומת|לא נקרא|לא נמצא|חסומ|סביבת הענן|carbook|eLUM|לוודא מול|בשם הקובץ/;
  const userNotes = [...(s.services ?? []).flatMap(x => x.items ?? []), ...(s.time_based ?? []), ...(s.long_interval ?? [])];
  for (const it of userNotes) if (it.note && devWords.test(it.note)) fail(`item note for '${it.item}' reads like a transcriber remark, move it to notes: "${it.note}"`);
  if (s.interval?.note && devWords.test(s.interval.note)) fail(`interval.note reads like a transcriber remark: "${s.interval.note}"`);
  for (const [k, v] of Object.entries(s.specs ?? {})) {
    if (!specKeys.has(k)) fail(`unknown specs key '${k}'`);
    if (typeof v !== "string" || !v.trim()) fail(`specs.${k} must be a non-empty string`);
  }
  for (const l of s.long_interval ?? []) {
    if (!items[l.item]) fail(`unknown long_interval item '${l.item}'`);
    if (!actions.has(l.action)) fail(`bad action '${l.action}' in long_interval ${l.item}`);
    const simple = l.every_km || l.every_months, staged = l.first_km || l.first_months;
    if (!simple && !staged) fail(`long_interval ${l.item} needs every_* or first_*`);
    if (staged && !(l.then_every_km || l.then_every_months)) fail(`long_interval ${l.item} has first_* but no then_every_*`);
  }
}
console.log(errors ? `${errors} error(s)` : `all schedules valid (${counts.draft} draft, ${counts.reviewed} reviewed, ${counts.verified} verified)`);
process.exit(errors ? 1 : 0);
