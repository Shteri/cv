import { readFileSync, existsSync, readdirSync } from "node:fs";
import { normalizeMake } from "/home/user/cv/scripts/lookup_plate.mjs";
const agg=JSON.parse(readFileSync("/home/user/cv/data/sources/registry-counts.json","utf8"));
const base=JSON.parse(readFileSync("/home/user/cv/data/registry_map.json","utf8")).rules;
const S="/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/";
let other=[]; for (const g of readdirSync(S)) { if (g==='eu4') continue; const f=S+g+"/registry/registry_rules.json"; if (existsSync(f)) try{other=other.concat(JSON.parse(readFileSync(f,"utf8")))}catch(e){} }
const mine=JSON.parse(readFileSync(S+"eu4/registry/registry_rules.json","utf8"));
const m=(MAP,v)=>{const name=v.model_name.toUpperCase().trim(),year=+v.year; const c=MAP.filter(r=>r.make===v.make&&r.names.some(n=>n===name)&&year>=r.years[0]&&year<=r.years[1]&&(!r.fuel||r.fuel.includes(v.fuel))&&(!r.engine_codes||r.engine_codes.includes(v.engine_code))); c.sort((a,b)=>(b.engine_codes?2:0)+(b.fuel?1:0)-((a.engine_codes?2:0)+(a.fuel?1:0))); return c[0]?.schedule??null;};
const before=base.concat(other), after=mine.concat(base).concat(other);
const per={}; let gain=0, conflict=0;
for (const r of agg.model_year_fuel_engine){ const v={make:normalizeMake(r.make),model_name:r.model,year:r.year,fuel:r.fuel,engine_code:r.engine};
  const b=m(before,v); const a=m(mine,v);
  if(!a) continue;
  if(!b){ gain+=r.n; per[a]=(per[a]||0)+r.n; } else if (b!==a) { conflict+=r.n; console.log('CONFLICT', r.make, r.model, r.year, r.engine, b, '->', a, r.n); }
}
for (const [k,v] of Object.entries(per).sort((a,b)=>b[1]-a[1])) console.log(v,k);
console.log('total new vehicles', gain, 'conflicting', conflict);
