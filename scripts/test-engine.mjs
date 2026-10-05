// Tests for app/engine.js: next service from the grid, and from the last service actually done (window, missed services).
import { readFileSync } from "node:fs";
const root = new URL("../", import.meta.url).pathname;
await import(root + "app/engine.js");
const E = globalThis.TipulitEngine;
const sched = id => JSON.parse(readFileSync(root + `data/schedules/${id}.json`, "utf8"));
const ev = sched("byd-atto-2-2025-2026-ev"), i10 = sched("hyundai-i10-2014-2019");
let fail = 0;
const check = (label, got, want) => {
  const ok = Object.entries(want).every(([k, v]) => got[k] === v);
  console.log(`${ok ? "OK  " : "FAIL"} ${label}${ok ? "" : ` got ${JSON.stringify(Object.fromEntries(Object.keys(want).map(k => [k, got[k]])))} want ${JSON.stringify(want)}`}`);
  if (!ok) fail++;
};
const car = (km, lastSvc) => ({ km, kmMonth: 1500, lastService: null, lastSvc });

check("no history: grid only", E.next(ev, car(64000)), { nextKm: 90000, windowFrom: 90000, windowTo: 90000, remainKm: 26000 });
check("60k done late at 63k: window 90k-93k", E.next(ev, car(64000, { svcKm: 60000, km: 63000 })), { nextKm: 90000, windowFrom: 90000, windowTo: 93000, remainKm: 29000, level: "good" });
check("60k done early at 57k: window 87k-90k", E.next(ev, car(58000, { svcKm: 60000, km: 57000 })), { nextKm: 90000, windowFrom: 87000, windowTo: 90000 });
check("no service label: snaps to the nearest", E.next(ev, car(64000, { svcKm: null, km: 63000 })), { nextKm: 90000, windowTo: 93000 });
check("inside the window: warn, not overdue", E.next(ev, car(91000, { svcKm: 60000, km: 63000 })), { nextKm: 90000, level: "warn", remainKm: 2000 });
check("past the window: overdue", E.next(ev, car(93500, { svcKm: 60000, km: 63000 })), { nextKm: 90000, level: "crit", remainKm: -500 });
check("60k skipped (30k at 31k, now 65k): 60k overdue", E.next(ev, car(65000, { svcKm: 30000, km: 31000 })), { nextKm: 60000, windowTo: 61000, level: "crit" });
check("several skipped: the latest passed", E.next(ev, car(95000, { svcKm: 30000, km: 31000 })), { nextKm: 90000, level: "crit" });
check("odometer not updated since the service", E.next(ev, car(60000, { svcKm: 60000, km: 63000 })), { nextKm: 90000, windowTo: 93000 });
check("i10 grid 15k+20k: 35k done at 37k", E.next(i10, car(38000, { svcKm: 35000, km: 37000 })), { nextKm: 55000, windowFrom: 55000, windowTo: 57000 });
check("i10 first service done at 14k", E.next(i10, car(16000, { svcKm: 15000, km: 14000 })), { nextKm: 35000, windowFrom: 34000, windowTo: 35000 });
check("i10 across the cycle", E.next(i10, car(160500, { svcKm: 155000, km: 156000 })), { nextKm: 175000, windowTo: 176000 });
check("i10 no history", E.next(i10, car(36000)), { nextKm: 55000, windowTo: 55000 });
// parts replaced off the schedule move their own next replacement
const plan = (sch, km, records) => E.next(sch, { km, kmMonth: 1500, lastService: null, records, lastSvc: null }).plan;
const has = (p, k) => p.replace.includes(k);
const regular = [{ km: 35000, kind: "service", items: ["engine_oil", "oil_filter", "air_filter", "brake_fluid", "cabin_filter"] }];
check("regular history changes nothing", { at55: plan(i10, 40000, regular).replace.join(), at75: plan(i10, 60000, [...regular, { km: 55000, kind: "service", items: ["engine_oil", "oil_filter", "cabin_filter"] }]).replace.join() },
  { at55: "engine_oil,oil_filter,cabin_filter", at75: "engine_oil,oil_filter,air_filter,brake_fluid,cabin_filter" });
const airRepair = [...regular, { km: 50000, kind: "repair", items: ["air_filter"] }];
const p75 = plan(i10, 60000, airRepair);
check("air filter replaced at 50k: skipped at 75k", { replace: has(p75, "air_filter"), skip: p75.skip.map(x => `${x.item}:${x.dueKm}:${x.repair}`).join() }, { replace: false, skip: "air_filter:90000:true" });
const p95 = plan(i10, 80000, [...airRepair, { km: 75000, kind: "service", items: ["engine_oil", "oil_filter", "brake_fluid", "cabin_filter"] }]);
check("...and added to 95k (due 90k, before 115k)", { replace: has(p95, "air_filter"), add: p95.add.map(x => x.item).join() }, { replace: true, add: "air_filter" });
check("replaced a little early: no change", { ok: has(plan(i10, 60000, [...regular, { km: 40000, kind: "repair", items: ["air_filter"] }]), "air_filter") }, { ok: true });
check("long-interval part replaced in a repair: added to the visit before it runs out", { ok: has(plan(ev, 80000, [{ km: 50000, kind: "repair", items: ["transmission_oil"] }]), "transmission_oil") && !has(plan(ev, 40000, [{ km: 50000, kind: "repair", items: ["transmission_oil"] }]), "transmission_oil") }, { ok: true });
check("no records: the importer's list", { n: plan(i10, 60000).replace.length, skip: plan(i10, 60000).skip.length }, { n: 5, skip: 0 });
check("this service's own record (done early) is not an earlier replacement", { n: E.planAt(i10, [{ km: 72000, kind: "service", items: ["air_filter", "brake_fluid"] }], i10.services[3], 75000).replace.length }, { n: 5 });
check("repair inside the window counts", { skip: E.planAt(i10, [...regular, { km: 76000, kind: "repair", items: ["brake_fluid"] }], i10.services[3], 75000).skip.map(x => x.item).join() }, { skip: "brake_fluid" });
if (fail) { console.error(`${fail} failed`); process.exit(1); }
console.log("engine ok");
