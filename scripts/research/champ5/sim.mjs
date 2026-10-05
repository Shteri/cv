import { readFileSync } from "node:fs";
import { normalizeMake } from "/home/user/cv/scripts/lookup_plate.mjs";
const agg = JSON.parse(readFileSync("/home/user/cv/data/sources/registry-counts.json", "utf8"));
const base = JSON.parse(readFileSync("/home/user/cv/data/registry_map.json", "utf8")).rules;
const extra = JSON.parse(readFileSync(process.argv[2], "utf8"));
function mk(MAP){ return v => { const name=(v.model_name||"").toUpperCase().trim(), year=Number(v.year);
  const c=MAP.filter(r=>r.make===v.make&&r.names.some(n=>n===name)&&year>=r.years[0]&&year<=r.years[1]&&(!r.fuel||r.fuel.includes(v.fuel))&&(!r.engine_codes||r.engine_codes.includes(v.engine_code)));
  c.sort((a,b)=>(b.engine_codes?2:0)+(b.fuel?1:0)-((a.engine_codes?2:0)+(a.fuel?1:0))); return c[0]?.schedule??null; }; }
const m0=mk(base), m1=mk([...base,...extra]);
const per={}; let gain=0, changed=0;
for (const r of agg.model_year_fuel_engine) {
  const v={make:normalizeMake(r.make),model_name:r.model,year:r.year,fuel:r.fuel,engine_code:r.engine};
  const a=m0(v), b=m1(v);
  if (!a && b) { gain+=r.n; per[b]=(per[b]||0)+r.n; }
  else if (a && b && a!==b) { changed+=r.n; console.log('CHANGED', a, '->', b, r.model, r.year, r.engine, r.n); }
}
console.log('newly covered', gain, 'reassigned', changed);
for (const [k,v] of Object.entries(per).sort((a,b)=>b[1]-a[1])) console.log(v,k);
