import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const root = SITE;
const srv = createServer((q, r) => { let f = root + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8132);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 400, height: 1400 } });
const errs = []; p.on("pageerror", e => errs.push(e.message));
await p.goto("http://localhost:8132/"); await p.waitForTimeout(200);
const all = ["engine_oil", "oil_filter", "cabin_filter"];
const hist = [
  { id: "a", kind: "service", svcKm: 35000, km: 35000, date: "2024-01", items: [...all, "air_filter", "brake_fluid"], receipts: [], share: false },
  { id: "b", kind: "service", svcKm: 55000, km: 55000, date: "2025-01", items: all, receipts: [], share: false },
  { id: "c", kind: "repair", km: 68000, date: "2025-09", text: "החלפת מסנן אוויר וטיפול בבלמים", items: ["air_filter", "brake_fluid"], receipts: [], share: false }];
await p.evaluate(h => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "guest" }, cars: [{ plate: "12-345-67", schedule: "hyundai-i10-2014-2019", year: 2017, km: 70000, kmMonth: 1500, lastService: "2025-01", history: h }], active: 0 })), hist);
await p.reload(); await p.waitForTimeout(500);
console.log("hero items:", (await p.locator("#home-body .card.ink .items").innerText()).replace(/\s+/g, " "));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/part-home.png", clip: { x: 0, y: 500, width: 400, height: 700 } });
await p.click('#nav button[data-go="tl"]'); await p.waitForTimeout(200);
console.log("next row:", (await p.locator(".tl-item.next .tl-body").innerText()).replace(/\s+/g, " ").slice(0, 260));
await p.click('#nav button[data-go="home"]'); await p.waitForTimeout(150);
await p.click("#done-svc"); await p.waitForTimeout(200);
await p.selectOption("#log-svc", "75000"); await p.waitForTimeout(100);
console.log("log preselect:", await p.$$eval("#log-items .chip.on, [id^=log] .chip.on", x => [...new Set(x.map(e => e.textContent))]));
const g = await b.newPage({ viewport: { width: 1300, height: 900 } }); g.on("pageerror", e => errs.push("garage: " + e.message));
await g.goto("http://localhost:8132/garage/?demo"); await g.waitForTimeout(1200);
const r = await g.evaluate(() => { const G = window.Garage, c = G.st.rows.find(x => x.n && x.s && x.s.id === "hyundai-i10-2014-2019") || G.st.rows.find(x => x.n); const before = c.n.plan.replace.join(); const k = c.n.plan.replace[c.n.plan.replace.length - 1];
  G.st.wos.unshift({ id: "t", garage_car_id: c.car_id, kind: "repair", km: c.estKm - 500, items: [k], lines: [] }); const v = G.view(c); return { sched: c.s.id, next: c.n.nextKm, before, after: v.n.plan.replace.join(), skip: v.n.plan.skip.map(x => x.item + ":" + x.dueKm).join() }; });
console.log("garage:", r);
console.log("errors:", errs);
await b.close(); srv.close();
