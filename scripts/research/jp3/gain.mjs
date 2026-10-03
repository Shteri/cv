import { readFileSync } from "node:fs";
import { normalizeMake } from "/home/user/cv/scripts/lookup_plate.mjs";
const agg=JSON.parse(readFileSync("/home/user/cv/data/sources/registry-counts.json","utf8"));
const base=JSON.parse(readFileSync("/home/user/cv/data/registry_map.json","utf8")).rules;
const mine=JSON.parse(readFileSync("/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/jp3/registry/registry_rules.json","utf8"));
function m(MAP,v){const name=v.model_name.toUpperCase().trim(),year=+v.year;const c=MAP.filter(r=>r.make===v.make&&r.names.some(n=>n===name)&&year>=r.years[0]&&year<=r.years[1]&&(!r.fuel||r.fuel.includes(v.fuel))&&(!r.engine_codes||r.engine_codes.includes(v.engine_code)));c.sort((a,b)=>(b.engine_codes?2:0)+(b.fuel?1:0)-((a.engine_codes?2:0)+(a.fuel?1:0)));return c[0]?.schedule??null;}
const all=base.concat(mine); const per={}; let gain=0, changed=0;
for(const r of agg.model_year_fuel_engine){const v={make:normalizeMake(r.make),model_name:r.model,year:r.year,fuel:r.fuel,engine_code:r.engine};
 const a=m(base,v), b=m(all,v);
 if(!a&&b){gain+=r.n; per[b]=(per[b]||0)+r.n;} else if(a&&b&&a!==b){changed+=r.n; per['CHANGED '+a+' -> '+b]=(per['CHANGED '+a+' -> '+b]||0)+r.n;}}
for(const [k,n] of Object.entries(per).sort((x,y)=>y[1]-x[1])) console.log(n,k);
console.log('TOTAL newly covered',gain,'changed',changed);
