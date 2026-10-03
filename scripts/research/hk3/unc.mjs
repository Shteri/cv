import { readFileSync } from "node:fs";
import { normalizeMake } from "/home/user/cv/scripts/lookup_plate.mjs";
const agg = JSON.parse(readFileSync("/home/user/cv/data/sources/registry-counts.json", "utf8"));
const extra = process.argv[2] ? JSON.parse(readFileSync(process.argv[2],"utf8")) : [];
const MAP = JSON.parse(readFileSync("/home/user/cv/data/registry_map.json","utf8")).rules.concat(extra);
function match(v){ const name=v.model_name.toUpperCase().trim(), year=Number(v.year);
  const c=MAP.filter(r=>r.make===v.make&&r.names.some(n=>n===name)&&year>=r.years[0]&&year<=r.years[1]&&(!r.fuel||r.fuel.includes(v.fuel))&&(!r.engine_codes||r.engine_codes.includes(v.engine_code)));
  c.sort((a,b)=>(b.engine_codes?2:0)+(b.fuel?1:0)-((a.engine_codes?2:0)+(a.fuel?1:0))); return c[0]?.schedule??null; }
const out = {}; const gained={}; let g=0;
const extraIds=new Set(extra.map(r=>r.schedule+'|'+JSON.stringify(r)));
for (const r of agg.model_year_fuel_engine) {
  const mk = normalizeMake(r.make);
  if (mk !== "Hyundai" && mk !== "Kia") continue;
  const v={ make: mk, model_name: r.model, year: r.year, fuel: r.fuel, engine_code: r.engine };
  const s = match(v);
  // gained = matched only thanks to an extra rule
  const base = (()=>{ const save=MAP.length; return null; })();
  if (s) { const isExtra = extra.some(e=>e.make===mk&&e.names.includes(r.model.toUpperCase().trim())&&+r.year>=e.years[0]&&+r.year<=e.years[1]&&(!e.fuel||e.fuel.includes(r.fuel))&&(!e.engine_codes||e.engine_codes.includes(r.engine))&&e.schedule===s);
    if (isExtra){ gained[s]=(gained[s]||0)+r.n; g+=r.n;} continue; }
  const k = `${mk}|${r.model}|${r.fuel}|${r.engine}`;
  (out[k] ??= { n: 0, y: {} }); out[k].n += r.n; out[k].y[r.year] = r.n;
}
console.log('gained total',g); for (const [k,n] of Object.entries(gained).sort((a,b)=>b[1]-a[1])) console.log('  ',n,k);
for (const [k, e] of Object.entries(out).sort((a, b) => b[1].n - a[1].n).slice(0, Number(process.argv[3]||70)))
  console.log(e.n, k, Object.entries(e.y).sort().map(([y, n]) => y + ":" + n).join(" "));
