// Pull real plates from the live data.gov.il registry and show which schedule each one gets.
//   node scripts/sample_plates.mjs [models=40] [perModel=2]
// Picks the biggest registry models (data/sources/registry-counts.json), asks the API for
// real plates of each (make, name, year, engine), runs matchSchedule, and writes
// data/check/sample-plates.md: a table to spot-check by hand, with a link per plate to the
// check page (data/check/index.html?plate=NNN) and to the schedule's source book.
import { readFileSync, writeFileSync } from "node:fs";
import { normalizeMake } from "./lookup_plate.mjs";
import { matchSchedule } from "./match_schedule.mjs";

const root = new URL("../data/", import.meta.url).pathname;
const RESOURCE = "053cea08-09bc-40ec-8f7a-156f0677aff3";
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36";
const nModels = Number(process.argv[2] || 40), perModel = Number(process.argv[3] || 2);
const agg = JSON.parse(readFileSync(root + "sources/registry-counts.json", "utf8"));
const byModel = {};
for (const r of agg.model_year_fuel_engine) (byModel[r.make + "|" + r.model] ??= []).push(r);
const top = Object.values(byModel).map(rows => ({ rows, n: rows.reduce((a, r) => a + r.n, 0) })).sort((a, b) => b.n - a.n).slice(0, nModels);

async function api(filters, offset) {
  const u = new URL("https://data.gov.il/api/3/action/datastore_search");
  u.searchParams.set("resource_id", RESOURCE); u.searchParams.set("filters", JSON.stringify(filters));
  u.searchParams.set("limit", "1"); u.searchParams.set("offset", String(offset));
  const res = await fetch(u, { headers: { "User-Agent": UA } });
  if (!res.ok) throw new Error("HTTP " + res.status);
  return (await res.json()).result?.records?.[0];
}
const pick = rows => { let x = Math.random() * rows.reduce((a, r) => a + r.n, 0); for (const r of rows) { x -= r.n; if (x <= 0) return r; } return rows[0]; };
const out = [];
for (const { rows } of top) {
  for (let i = 0; i < perModel; i++) {
    const r = pick(rows);
    try {
      const rec = await api({ tozeret_nm: r.make, kinuy_mishari: r.model, shnat_yitzur: Number(r.year), degem_manoa: r.engine }, Math.floor(Math.random() * Math.min(r.n, 200)));
      if (!rec) continue;
      const v = { make: normalizeMake(rec.tozeret_nm), model_name: rec.kinuy_mishari, year: rec.shnat_yitzur, fuel: rec.sug_delek_nm, engine_code: rec.degem_manoa };
      const id = matchSchedule(v);
      let s = null; try { s = id && JSON.parse(readFileSync(root + "schedules/" + id + ".json", "utf8")); } catch {}
      out.push({ plate: rec.mispar_rechev, make: v.make, name: rec.kinuy_mishari, year: rec.shnat_yitzur, fuel: rec.sug_delek_nm, engine: rec.degem_manoa, id, status: s?.status ?? "", src: s?.sources?.[0]?.url ?? "" });
      process.stdout.write(`${rec.mispar_rechev}\t${v.make} ${rec.kinuy_mishari} ${rec.shnat_yitzur} ${rec.degem_manoa}\t-> ${id ?? "NO SCHEDULE"} ${s?.status ?? ""}\n`);
    } catch (e) { console.error("skip", r.model, r.year, e.message); }
  }
}
const md = ["# Real plates from the registry, and the schedule each one gets", "",
  `Generated ${new Date().toISOString().slice(0, 10)} by scripts/sample_plates.mjs from the live data.gov.il registry.`,
  "Open data/check/index.html?plate=NNN to see the schedule next to the registry record, then compare with the source book.", "",
  "| plate | make | name | year | fuel | engine | schedule | status | source |", "|---|---|---|---|---|---|---|---|---|",
  ...out.map(o => `| ${o.plate} | ${o.make} | ${o.name} | ${o.year} | ${o.fuel} | ${o.engine} | ${o.id ?? "**none**"} | ${o.status} | ${o.src ? `[book](${o.src})` : ""} |`)];
writeFileSync(root + "check/sample-plates.md", md.join("\n") + "\n");
const hit = out.filter(o => o.id).length;
console.log(`\n${hit}/${out.length} sampled plates matched a schedule; wrote data/check/sample-plates.md`);
