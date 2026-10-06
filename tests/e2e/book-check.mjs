import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync, writeFileSync } from "node:fs";
const ct = f => f.endsWith(".css") ? "text/css" : f.endsWith(".js") ? "text/javascript" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8";
const srv = createServer((q, r) => { let u = q.url.split("?")[0]; if (u.endsWith("/")) u += "index.html"; const f = SITE + u; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", ct(f)); r.end(readFileSync(f)); }).listen(8143);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium", args: ["--ignore-certificate-errors"] });
const errs = [];
// ---------- A. demo mode ----------
let p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.5 }); p.on("pageerror", e => errs.push("demo: " + e.message));
await p.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort());
await p.goto("http://localhost:8143/garage/?demo"); await p.waitForTimeout(2000);
console.log("A rows:", await p.$$eval("#rows tr", l => l.length));
// customer with shared history (index 0: linked + share_history)
await p.click('#rows [data-cust="dcus-0"]'); await p.waitForTimeout(500);
const tl = await p.$$eval("#cc-timeline .tl-row", l => l.map(e => e.className.replace("tl-row ", "") + ":" + e.textContent.replace(/\s+/g, " ").trim().slice(0, 60)));
console.log("A card timeline:", tl, "| note:", await p.textContent("#cc-hist-note"));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/book-card.png" });
// work order from the card
await p.click("#cc-cars [data-wo]"); await p.waitForTimeout(400);
console.log("A wo lines prefilled:", await p.$$eval("#wo-lines tr", l => l.length), "items:", await p.$$eval("#wo-items .chip.on", l => l.map(e => e.textContent)));
const prices = await p.$$("#wo-lines input.price"); for (const [i, x] of prices.entries()) await x.fill(String(50 + i * 40));
console.log("A total:", await p.textContent("#wo-total"), "send row shown (linked):", !(await p.$eval("#wo-send-row", e => e.hidden)));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/book-wo.png" });
await p.click("#wo-save"); await p.waitForTimeout(400); console.log("A wo saved:", await p.textContent("#toast"));
await p.click('#rows [data-cust="dcus-0"]'); await p.waitForTimeout(500); console.log("A card now has", await p.$$eval("#cc-timeline .tl-row.own", l => l.length), "own visits"); await p.click('#dlg-cust button[value="close"]');
// add customer
await p.click("#btn-add"); await p.fill("#ad-plate", "1234567"); await p.fill("#ad-name", "לקוח חדש"); await p.fill("#ad-phone", "050-1111111"); await p.fill("#ad-km", "42000"); await p.click("#ad-save"); await p.waitForTimeout(400);
console.log("A added:", await p.textContent("#toast"), "rows:", await p.$$eval("#rows tr", l => l.length));
// import CSV
writeFileSync("import.csv", "﻿שם לקוח,טלפון נייד,מספר רישוי,קילומטראז'\nאבי טל,052-1234567,11-222-33,55000\nבת שבע,,22-333-44,\n,,33-444-55,1\n");
await p.click("#btn-import"); await p.setInputFiles("#im-file", "import.csv"); await p.waitForTimeout(500);
console.log("A import mapping:", await p.$$eval("#im-map select", l => l.map(s => s.dataset.map + "=" + s.selectedOptions[0].textContent)));
await p.click("#im-go"); await p.waitForTimeout(800); console.log("A import:", await p.textContent("#im-status"), "rows:", await p.$$eval("#rows tr", l => l.length));
await p.click('#dlg-import button[value="close"]');
// forecast
await p.click('.tab[data-tab="order"]'); await p.waitForTimeout(300);
console.log("A forecast:", await p.textContent("#fc-sub"), "| items:", await p.$$eval("#fc-rows tr", l => l.slice(0, 4).map(e => e.textContent.replace(/\s+/g, " ").trim().slice(0, 70))));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/book-order.png" });
await p.click('#fc-window .chip[data-d="60"]'); await p.waitForTimeout(200); console.log("A 60 days:", await p.textContent("#fc-sub"));
const [dl] = await Promise.all([p.waitForEvent("download"), p.click("#fc-csv")]); await dl.saveAs("order.csv"); console.log("A order csv:", readFileSync("order.csv", "utf8").split("\n").slice(0, 3).join(" | ").slice(0, 160));
// ---------- B. connected mode with a simulated server ----------
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
const calls = [];
await ctx.exposeFunction("__api", (op, a) => { calls.push(op); return ({
  garageBook: [{ car_id: "g1", customer_id: "u1", name: "דנה", phone: "050-2222222", can_contact: true, source: "app", plate: "7778889", schedule_id: "hyundai-i10-2014-2019", year: 2016, km: 90000, km_month: 1200, km_at: new Date().toISOString(), last_service: "2025-12", test_expiry: "2026-12-01", linked: true, share_history: true, last_visit: null, visits: 0, pending: 0, created_at: new Date().toISOString() }],
  workOrders: [], garageCarHistory: [{ date: "2025-06", km: 74800, kind: "service", svc_km: 75000, items: ["engine_oil"], garage: "מוסך אחר", verified: true, own: false }],
  saveWorkOrder: { ...a, id: "wo1" }, sendWorkOrder: "entry1", updateGarageCar: [], addCustomer: { id: "u2" }, addGarageCar: { id: "g2" }, updateCustomer: [] })[op]; });
await ctx.addInitScript(() => { const u = { id: "o1", email: "owner@x" }; const call = op => (...a) => window.__api(op, a[0] && typeof a[0] === "object" ? a[0] : a);
  const stub = { enabled: true, hasAuthParams: false, currentUser: async () => u, signOut: async () => {}, myGarageProfiles: async () => [{ id: "G", name: "מוסך ב", city: "בת ים", status: "verified" }],
    garageBook: call("garageBook"), workOrders: call("workOrders"), garageCarHistory: call("garageCarHistory"), saveWorkOrder: call("saveWorkOrder"), sendWorkOrder: call("sendWorkOrder"), updateGarageCar: call("updateGarageCar"), addCustomer: call("addCustomer"), addGarageCar: call("addGarageCar"), updateCustomer: call("updateCustomer") };
  Object.defineProperty(window, "TipulitCloud", { configurable: true, set() {}, get() { return stub; } }); });
p = await ctx.newPage(); p.on("pageerror", e => errs.push("live: " + e.message));
await p.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort()); await p.route("https://data.gov.il/**", r => r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ result: { records: [] } }) }));
await p.goto("http://localhost:8143/garage/"); await p.waitForTimeout(1500);
console.log("B name:", await p.textContent("#g-name"), "rows:", await p.$$eval("#rows tr", l => l.length));
await p.click('#rows [data-cust="u1"]'); await p.waitForTimeout(500);
console.log("B shared history rows:", await p.$$eval("#cc-timeline .tl-row.other", l => l.length), "| phone field locked (app customer):", await p.$eval("#cc-in-phone", e => e.disabled));
await p.click("#cc-cars [data-wo]"); await p.waitForTimeout(300); const pr = await p.$$("#wo-lines input.price"); for (const x of pr) await x.fill("100");
await p.click("#wo-save"); await p.waitForTimeout(500);
console.log("B calls:", calls.join(","), "| toast:", await p.textContent("#toast"));
await p.click("#btn-add"); await p.fill("#ad-plate", "7778889"); await p.fill("#ad-name", "כפול"); await p.click("#ad-save"); await p.waitForTimeout(400); console.log("B duplicate plate:", await p.textContent("#ad-err"));
console.log("errors:", errs); await b.close(); srv.close();
