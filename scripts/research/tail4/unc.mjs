// usage: node unc.mjs [makes comma] [minN]  -- uses repo map + staging tail4 rules
import { readFileSync, existsSync } from "node:fs";
import { normalizeMake } from "/home/user/cv/scripts/lookup_plate.mjs";
const root = "/home/user/cv/data/";
const agg = JSON.parse(readFileSync(root + "sources/registry-counts.json", "utf8"));
let MAP = JSON.parse(readFileSync(root + "registry_map.json", "utf8")).rules;
const extra = "/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/tail4/registry/registry_rules.json";
let EX = existsSync(extra) ? JSON.parse(readFileSync(extra, "utf8")) : [];
const useExtra = !process.argv.includes("--base");
if (useExtra) MAP = MAP.concat(EX);
function match(v) {
  const name = v.model_name.toUpperCase().trim(), year = Number(v.year);
  const c = MAP.filter(r => r.make === v.make && r.names.some(n => n === name) && year >= r.years[0] && year <= r.years[1] && (!r.fuel || r.fuel.includes(v.fuel)) && (!r.engine_codes || r.engine_codes.includes(v.engine_code)));
  c.sort((a, b) => (b.engine_codes ? 2 : 0) + (b.fuel ? 1 : 0) - ((a.engine_codes ? 2 : 0) + (a.fuel ? 1 : 0)));
  return c[0]?.schedule ?? null;
}
const makes = (process.argv[2] || "").split(",").filter(Boolean);
const minN = Number(process.argv[3] || 100);
const g = {}; let newly = 0;
for (const r of agg.model_year_fuel_engine) {
  const mk = normalizeMake(r.make);
  if (makes.length && !makes.includes(mk)) continue;
  const s = match({ make: mk, model_name: r.model, year: r.year, fuel: r.fuel, engine_code: r.engine });
  if (s) continue;
  const k = `${mk}|${r.model}|${r.fuel}|${r.engine}`;
  const e = g[k] ??= { n: 0, y: {} }; e.n += r.n; e.y[r.year] = (e.y[r.year] || 0) + r.n;
}
const rows = Object.entries(g).sort((a, b) => b[1].n - a[1].n).filter(([, e]) => e.n >= minN);
for (const [k, e] of rows) {
  const [mk, model] = k.split("|");
  const rules = MAP.filter(r => r.make === mk && r.names.includes(model.toUpperCase().trim())).map(r => `${r.schedule}[${r.years}]${r.engine_codes ? "{" + r.engine_codes.join(",") + "}" : ""}${r.fuel ? "(" + r.fuel + ")" : ""}`);
  console.log(`${e.n}\t${k}\t${Object.entries(e.y).sort().map(([y, n]) => y + ":" + n).join(" ")}\n\t\trules: ${rules.join(" ; ") || "-"}`);
}
console.log("total uncovered listed:", rows.reduce((s, [, e]) => s + e.n, 0));
