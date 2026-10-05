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
if (fail) { console.error(`${fail} failed`); process.exit(1); }
console.log("engine ok");
