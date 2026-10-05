// node unc.mjs <EnglishMake> [modelRegex] [extraRulesJson]
import { readFileSync, existsSync } from "node:fs";
import { normalizeMake } from "/home/user/cv/scripts/lookup_plate.mjs";
const root="/home/user/cv/data/";
const agg=JSON.parse(readFileSync(root+"sources/registry-counts.json","utf8"));
let MAP=JSON.parse(readFileSync(root+"registry_map.json","utf8")).rules;
const extra=process.argv[4]||"/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/jp4/registry/registry_rules.json";
let mine=[]; if(existsSync(extra)) mine=JSON.parse(readFileSync(extra,"utf8"));
MAP=MAP.concat(mine);
function match(v){const name=v.model_name.toUpperCase().trim(),year=+v.year;const c=MAP.filter(r=>r.make===v.make&&r.names.some(n=>n===name)&&year>=r.years[0]&&year<=r.years[1]&&(!r.fuel||r.fuel.includes(v.fuel))&&(!r.engine_codes||r.engine_codes.includes(v.engine_code)));c.sort((a,b)=>(b.engine_codes?2:0)+(b.fuel?1:0)-((a.engine_codes?2:0)+(a.fuel?1:0)));return c[0]?.schedule??null;}
const mk=process.argv[2], re=new RegExp(process.argv[3]||".");
const g={}; let mineN=0;
for(const r of agg.model_year_fuel_engine){const m=normalizeMake(r.make); if(m!==mk||!re.test(r.model))continue;
 const v={make:m,model_name:r.model,year:r.year,fuel:r.fuel,engine_code:r.engine}; const s=match(v);
 if(s && mine.some(x=>x.schedule===s && x.make===m && x.names.includes(r.model.toUpperCase().trim()))) mineN+=r.n;
 if(!s){const k=`${r.model} | ${r.fuel} | ${r.engine}`; (g[k]??={n:0,y:{}}).n+=r.n; g[k].y[r.year]=(g[k].y[r.year]||0)+r.n;}}
for(const [k,e] of Object.entries(g).sort((a,b)=>b[1].n-a[1].n).slice(0,+process.argv[5]||40)) console.log(e.n,k,Object.entries(e.y).sort().map(([y,n])=>y+":"+n).join(" "));
console.log("matched by my rules (approx):",mineN);
