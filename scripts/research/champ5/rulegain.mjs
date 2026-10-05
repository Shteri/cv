import { readFileSync } from "node:fs";
import { normalizeMake } from "/home/user/cv/scripts/lookup_plate.mjs";
const agg = JSON.parse(readFileSync("/home/user/cv/data/sources/registry-counts.json", "utf8"));
const base = JSON.parse(readFileSync("/home/user/cv/data/registry_map.json", "utf8")).rules;
const extra = JSON.parse(readFileSync(process.argv[2], "utf8"));
const hit=(r,v)=>r.make===v.make&&r.names.includes(v.model_name)&&+v.year>=r.years[0]&&+v.year<=r.years[1]&&(!r.fuel||r.fuel.includes(v.fuel))&&(!r.engine_codes||r.engine_codes.includes(v.engine_code));
extra.forEach((r,i)=>{ let newn=0, shadow=0, sh=new Set();
  for (const x of agg.model_year_fuel_engine){ const v={make:normalizeMake(x.make),model_name:x.model.toUpperCase().trim(),year:x.year,fuel:x.fuel,engine_code:x.engine};
    if(!hit(r,v)) continue; const b=base.filter(q=>hit(q,v)); if(b.length){shadow+=x.n; b.forEach(q=>sh.add(q.schedule));} else newn+=x.n; }
  console.log(i, r.schedule, r.names.join('/'), r.engine_codes.join('/'), 'new', newn, 'already', shadow, [...sh].join(','));
});
