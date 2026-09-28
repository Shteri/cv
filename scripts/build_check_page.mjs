// Builds data/check/index.html: a self-contained page for checking the data by hand.
//   node scripts/build_check_page.mjs
// - Plate lookup against the live data.gov.il registry (the API allows browser calls),
//   run through the same matching rules as scripts/match_schedule.mjs.
// - Every schedule: status, years, engines, the service grid, long intervals, specs,
//   notes, and links to the source books, so each row can be checked against the PDF.
// - The biggest registry models that still have no schedule.
import { readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { normalizeMake } from "./lookup_plate.mjs";
import { matchSchedule } from "./match_schedule.mjs";

const root = new URL("../data/", import.meta.url).pathname;
const items = JSON.parse(readFileSync(join(root, "items.json"), "utf8"));
const rules = JSON.parse(readFileSync(join(root, "registry_map.json"), "utf8")).rules;
const schedules = readdirSync(join(root, "schedules")).filter(f => f.endsWith(".json"))
  .map(f => JSON.parse(readFileSync(join(root, "schedules", f), "utf8")))
  .sort((a, b) => (a.make + a.model + a.years[0]).localeCompare(b.make + b.model + b.years[0]));
const makes = JSON.parse(readFileSync(new URL("./lookup_plate.mjs", import.meta.url), "utf8").match(/const MAKES = (\[[\s\S]*?\]);/)[1].replace(/,\s*\]$/, "]"));

// coverage (same logic as registry_coverage.mjs)
const agg = JSON.parse(readFileSync(join(root, "sources", "registry-counts.json"), "utf8"));
const byModel = {}; let total = 0, covered = 0;
for (const r of agg.model_year_fuel_engine ?? agg.model_year) {
  const mk = normalizeMake(r.make);
  const s = matchSchedule({ make: mk, model_name: r.model, year: r.year, fuel: r.fuel, engine_code: r.engine });
  const e = byModel[mk + " | " + r.model] ??= { n: 0, unc: 0 };
  e.n += r.n; total += r.n;
  if (s) covered += r.n; else e.unc += r.n;
}
const uncovered = Object.entries(byModel).map(([k, e]) => [k, e.unc, e.n]).filter(x => x[1] > 0).sort((a, b) => b[1] - a[1]).slice(0, 60);
const perSchedule = {};
for (const r of agg.model_year_fuel_engine ?? []) {
  const s = matchSchedule({ make: normalizeMake(r.make), model_name: r.model, year: r.year, fuel: r.fuel, engine_code: r.engine });
  if (s) perSchedule[s] = (perSchedule[s] || 0) + r.n;
}

const DATA = { items, rules, schedules, makes, uncovered, perSchedule, total, covered, snapshot: agg.snapshot, built: new Date().toISOString().slice(0, 10) };
const html = `<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>בדיקת נתוני טיפולית</title>
<style>
:root{--bg:#f7f7f5;--fg:#1d1d1b;--mut:#6b6b66;--card:#fff;--line:#e2e2dc;--acc:#1f5fbf;--ok:#1d7a46;--warn:#a15c00;--r:#b3261e;--rb:#e8f0fb;--ib:#f1f1ee}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#161615;--fg:#ececea;--mut:#a3a39d;--card:#20201f;--line:#34342f;--acc:#7fb0ff;--ok:#5fd38f;--warn:#f0b35a;--r:#ff8a80;--rb:#1f2c42;--ib:#2a2a27}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Arial,sans-serif}
main{max-width:1100px;margin:0 auto;padding:16px}h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:24px 0 8px}
.mut{color:var(--mut)}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:10px 0}
input,select,button{font:inherit;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg)}
button{background:var(--acc);color:#fff;border:0;cursor:pointer}.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.pill{display:inline-block;padding:1px 8px;border-radius:99px;font-size:12px;border:1px solid var(--line)}
.reviewed{color:var(--ok);border-color:var(--ok)}.draft{color:var(--warn);border-color:var(--warn)}.verified{color:var(--acc);border-color:var(--acc)}
.list .it{border-top:1px solid var(--line);padding:8px 0;cursor:pointer}.list .it:first-child{border-top:0}
.tbl{overflow-x:auto}table{border-collapse:collapse;font-size:13px;min-width:100%}th,td{border:1px solid var(--line);padding:3px 6px;text-align:center;white-space:nowrap}
th:first-child,td:first-child{text-align:right;position:sticky;right:0;background:var(--card)}td.R{background:var(--rb);font-weight:600}td.I{background:var(--ib)}
a{color:var(--acc)}dl{display:grid;grid-template-columns:max-content 1fr;gap:2px 12px;margin:0}dt{color:var(--mut)}dd{margin:0}
.kv{font-size:13px}.stat{font-size:28px;font-weight:700}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}
details summary{cursor:pointer;color:var(--acc)}
</style></head><body><main>
<h1>בדיקת נתוני טיפולית</h1>
<div class="mut" id="meta"></div>
<div class="grid" id="stats"></div>

<h2>בדיקת מספר רכב (מאגר משרד התחבורה, חי)</h2>
<div class="card"><div class="row"><input id="plate" inputmode="numeric" placeholder="מספר רכב, למשל 5714838" style="flex:1;min-width:180px"><button id="go">בדוק</button></div>
<div id="plateOut" style="margin-top:10px"></div></div>

<h2>כל הלוחות</h2>
<div class="row"><input id="q" placeholder="חיפוש: יצרן, דגם, מנוע, מזהה" style="flex:1;min-width:180px">
<select id="st"><option value="">כל הסטטוסים</option><option>reviewed</option><option>draft</option><option>verified</option></select>
<select id="mk"><option value="">כל היצרנים</option></select></div>
<div class="card list" id="list"></div>

<h2>דגמים גדולים שעדיין בלי לוח</h2>
<div class="card tbl"><table id="unc"><thead><tr><th>דגם</th><th>בלי לוח</th><th>סה"כ במאגר</th></tr></thead><tbody></tbody></table></div>
<p class="mut kv">נבנה מ-data/ ע"י scripts/build_check_page.mjs. R = החלפה, I = בדיקה, A = כוונון, C = ניקוי.</p>
</main>
<script>
const D=${JSON.stringify(DATA)};
const $=s=>document.querySelector(s), esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const fmt=n=>Number(n).toLocaleString("he-IL");
const act={replace:"R",inspect:"I",adjust:"A",clean:"C",rotate:"S"};
$("#meta").textContent=\`נבנה \${D.built} · מאגר רישוי \${D.snapshot} · \${D.schedules.length} לוחות\`;
const cnt=s=>D.schedules.filter(x=>x.status===s).length;
$("#stats").innerHTML=[["כיסוי כלי רכב במאגר",(100*D.covered/D.total).toFixed(1)+"%"],["רכבים עם לוח",fmt(D.covered)],["reviewed (ספר ישראלי)",cnt("reviewed")],["draft (לאימות)",cnt("draft")]]
 .map(([k,v])=>\`<div class="card"><div class="mut kv">\${k}</div><div class="stat">\${v}</div></div>\`).join("");
function normalizeMake(raw){if(!raw)return null;for(const [he,en] of D.makes) if(raw.startsWith(he)) return en;return raw.split(" ")[0]}
function match(v){const name=(v.model_name||"").toUpperCase().trim(),y=Number(v.year);
 const c=D.rules.filter(r=>r.make===v.make&&r.names.some(n=>n===name)&&y>=r.years[0]&&y<=r.years[1]&&(!r.fuel||r.fuel.includes(v.fuel))&&(!r.engine_codes||r.engine_codes.includes(v.engine_code)));
 c.sort((a,b)=>(b.engine_codes?2:0)+(b.fuel?1:0)-((a.engine_codes?2:0)+(a.fuel?1:0)));return c[0]?.schedule??null}
function grid(s){const kms=s.services.map(x=>x.km),keys=[];for(const sv of s.services)for(const it of sv.items)if(!keys.includes(it.item))keys.push(it.item);
 const cell=(sv,k)=>{const a=sv.items.filter(i=>i.item===k).map(i=>act[i.action]);return a.includes("R")?"R":(a[0]||"")};
 return \`<div class="tbl"><table><thead><tr><th>פריט \\\\ ק"מ</th>\${kms.map(k=>\`<th>\${fmt(k/1000)}K</th>\`).join("")}</tr></thead><tbody>\${keys.map(k=>\`<tr><td>\${esc(D.items[k]?.he||k)}</td>\${s.services.map(sv=>{const c=cell(sv,k);return \`<td class="\${c}">\${c}</td>\`}).join("")}</tr>\`).join("")}</tbody></table></div>\`}
function detail(s){const li=(s.long_interval||[]).map(l=>{const p=[];if(l.every_km)p.push("כל "+fmt(l.every_km)+' ק"מ');if(l.every_months)p.push("כל "+l.every_months+" חודשים");if(l.first_km)p.push("ראשונה "+fmt(l.first_km)+' ק"מ'+(l.first_months?" / "+l.first_months+" ח׳":""));if(l.then_every_km)p.push("ואז כל "+fmt(l.then_every_km)+(l.then_every_months?" / "+l.then_every_months+" ח׳":""));
  return \`<li>\${esc(D.items[l.item]?.he||l.item)} (\${act[l.action]}): \${p.join(", ")}\${l.note?" – "+esc(l.note):""}</li>\`}).join("");
 const sp=Object.entries(s.specs||{}).map(([k,v])=>\`<dt>\${esc(k)}</dt><dd>\${esc(v)}</dd>\`).join("");
 return \`<div class="kv"><dl><dt>מזהה</dt><dd>\${esc(s.id)}</dd><dt>מרווח</dt><dd>\${fmt(s.interval.km)} ק"מ / \${s.interval.months} חודשים\${s.interval.note?" – "+esc(s.interval.note):""}</dd><dt>מחזור</dt><dd>\${fmt(s.cycle_km)} ק"מ</dd><dt>מנועים</dt><dd>\${esc((s.engines||[]).join(", "))}</dd><dt>רכבים במאגר</dt><dd>\${fmt(D.perSchedule[s.id]||0)}</dd></dl>
 <h4>מקורות (לבדיקה מול הספר)</h4><ul>\${s.sources.map(x=>\`<li><a href="\${esc(x.url)}" target="_blank" rel="noopener">\${esc(x.url.length>90?x.url.slice(0,90)+"…":x.url)}</a> <span class="pill">\${esc(x.kind)}</span><br><span class="mut">\${esc(x.note||"")}</span></li>\`).join("")}</ul>
 \${grid(s)}\${li?\`<h4>מרווחים ארוכים</h4><ul>\${li}</ul>\`:""}\${sp?\`<details><summary>מפרט</summary><dl>\${sp}</dl></details>\`:""}<p>\${esc(s.notes||"")}</p></div>\`}
function renderList(){const q=$("#q").value.trim().toLowerCase(),st=$("#st").value,mk=$("#mk").value;
 const L=D.schedules.filter(s=>(!st||s.status===st)&&(!mk||s.make===mk)&&(!q||JSON.stringify([s.id,s.make,s.make_he,s.model,s.model_he,s.engines,s.generation]).toLowerCase().includes(q)));
 $("#list").innerHTML=L.map(s=>\`<div class="it" data-id="\${esc(s.id)}"><b>\${esc(s.make_he||s.make)} \${esc(s.model_he||s.model)}</b> \${s.years[0]}-\${s.years[1]} <span class="mut">\${esc(s.generation||"")} · \${esc((s.engines||[]).join(", "))}</span> <span class="pill \${s.status}">\${s.status}</span> <span class="mut kv">\${fmt(D.perSchedule[s.id]||0)} רכבים</span><div class="det"></div></div>\`).join("")||"<div class=mut>אין תוצאות</div>"}
[...new Set(D.schedules.map(s=>s.make))].sort().forEach(m=>$("#mk").insertAdjacentHTML("beforeend",\`<option>\${esc(m)}</option>\`));
["#q","#st","#mk"].forEach(s=>$(s).addEventListener("input",renderList));
$("#list").addEventListener("click",e=>{const it=e.target.closest(".it");if(!it||e.target.closest("a,details,table"))return;const d=it.querySelector(".det");d.innerHTML=d.innerHTML?"":detail(D.schedules.find(s=>s.id===it.dataset.id))});
renderList();
$("#unc tbody").innerHTML=D.uncovered.map(([k,u,n])=>\`<tr><td>\${esc(k)}</td><td>\${fmt(u)}</td><td>\${fmt(n)}</td></tr>\`).join("");
async function lookup(){const p=$("#plate").value.replace(/\\D/g,""),out=$("#plateOut");if(p.length<5){out.textContent="צריך 5-8 ספרות";return}
 out.textContent="בודק…";try{const u=new URL("https://data.gov.il/api/3/action/datastore_search");u.searchParams.set("resource_id","053cea08-09bc-40ec-8f7a-156f0677aff3");u.searchParams.set("filters",JSON.stringify({mispar_rechev:Number(p)}));u.searchParams.set("limit","1");
 const r=(await (await fetch(u)).json())?.result?.records?.[0];if(!r){out.textContent="לא נמצא במאגר";return}
 const v={make:normalizeMake(r.tozeret_nm),model_name:r.kinuy_mishari,year:r.shnat_yitzur,fuel:r.sug_delek_nm,engine_code:r.degem_manoa};const id=match(v),s=D.schedules.find(x=>x.id===id);
 out.innerHTML=\`<dl class="kv"><dt>יצרן</dt><dd>\${esc(r.tozeret_nm)} → \${esc(v.make)}</dd><dt>כינוי מסחרי</dt><dd>\${esc(r.kinuy_mishari)}</dd><dt>דגם</dt><dd>\${esc(r.degem_nm)}</dd><dt>שנה</dt><dd>\${esc(r.shnat_yitzur)}</dd><dt>דלק</dt><dd>\${esc(r.sug_delek_nm)}</dd><dt>קוד מנוע</dt><dd>\${esc(r.degem_manoa)}</dd><dt>עלייה לכביש</dt><dd>\${esc(r.moed_aliya_lakvish)}</dd></dl>\`+
 (s?\`<h3>\${esc(s.make_he||s.make)} \${esc(s.model_he||s.model)} <span class="pill \${s.status}">\${s.status}</span></h3>\${detail(s)}\`:\`<p><b>אין לוח מתאים.</b> <span class="mut">אין כלל ב-registry_map שמתאים לשם/שנה/מנוע האלה.</span></p>\`)}catch(e){out.textContent="שגיאה: "+e.message}}
$("#go").addEventListener("click",lookup);$("#plate").addEventListener("keydown",e=>{if(e.key==="Enter")lookup()});
const qp=new URLSearchParams(location.search).get("plate");if(qp){$("#plate").value=qp;lookup()}
</script></body></html>`;
writeFileSync(join(root, "check", "index.html"), html);
console.log(`wrote data/check/index.html (${(html.length / 1024).toFixed(0)} KB, ${schedules.length} schedules, coverage ${(100 * covered / total).toFixed(1)}%)`);
