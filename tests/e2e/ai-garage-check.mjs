import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const ct = f => f.endsWith(".css") ? "text/css" : f.endsWith(".js") ? "text/javascript" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8";
const srv = createServer((q, r) => { let u = q.url.split("?")[0]; if (u.endsWith("/")) u += "index.html"; const f = SITE + u; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", ct(f)); r.end(readFileSync(f)); }).listen(8150);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const errs = [];
// demo
const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.5 }); p.on("pageerror", e => errs.push(e.message));
await p.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort());
await p.goto("http://localhost:8150/garage/?demo"); await p.waitForTimeout(1500);
await p.click('#rows [data-wo]'); await p.waitForTimeout(300);
await p.fill("#wo-ai", "טיפול 60, החלפתי רפידות בלם ומסנן שמן, שעה וחצי עבודה"); await p.click("#wo-ai-go"); await p.waitForTimeout(300);
console.log("demo wo:", await p.textContent("#wo-ai-msg"), "|", await p.$$eval("#wo-lines tr", l => l.map(e => e.children[0].textContent.trim() + ":" + e.querySelector("input").value + " x" + e.querySelectorAll("input")[1].value + " ₪" + e.querySelectorAll("input")[2].value)));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/ai-wo.png" });
await p.evaluate(() => document.querySelectorAll("dialog[open]").forEach(d => d.close()));
await p.click('#rows [data-cust="dcus-1"]'); await p.waitForTimeout(300); await p.click("#cc-cars [data-act-car]"); await p.waitForTimeout(300);
await p.fill("#in-ai", "רפידות קדמיות 2 מ\"מ, מגבים משאירים פסים, מצבר חלש, השאר תקין"); await p.click("#in-ai-go"); await p.waitForTimeout(300);
console.log("demo insp:", await p.textContent("#in-sum"), "|", await p.$$eval('#in-rows .insp-row:not([data-st="ok"])', l => l.map(e => e.querySelector("b").textContent + "=" + e.dataset.st)));
// real mode with a stubbed AI
const q = await b.newPage({ viewport: { width: 1440, height: 900 } }); q.on("pageerror", e => errs.push("real: " + e.message));
await q.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort()); await q.route("https://data.gov.il/**", r => r.abort());
await q.addInitScript(() => {
  const G = "11111111-1111-1111-1111-111111111111";
  const s = { enabled: true, hasAuthParams: false, currentUser: async () => ({ id: "u", email: "g@x" }),
    myGarageProfiles: async () => [{ id: G, name: "מוסך", status: "verified", labor_rate: 300, modules: null }],
    garageBook: async () => [{ car_id: "c1", customer_id: "k1", name: "שרה", phone: "050", plate: "1234567", schedule_id: "toyota-corolla-2007-2012-1.6", year: 2011, km: 150000, km_month: 1500, km_at: new Date().toISOString(), linked: false, created_at: new Date().toISOString() }],
    workOrders: async () => [], parts: async () => [{ id: "p1", name: "רפידות קורולה", item_key: "brake_pads", price: 320, stock: 4, unit: "unit", active: true }], suppliers: async () => [], purchaseOrders: async () => [], invoices: async () => [], billing: async () => null, jobTemplates: async () => [{ id: "j1", name: "רפידות בלם קדמיות", hours: 1, parts: [], active: true }], approvalsFor: async () => [],
    aiAssist: async (task, note, ctx) => { window.__ai = { task, note, ctx }; if (note.includes("נכשל")) throw new Error("ai not configured");
      return { kind: "repair", svc_km: null, km: 151000, notes: "לקוח ביקש לבדוק רעש", lines: [{ type: "part", desc: "רפידות", qty: 1, price: null, hours: null, part_id: "p1", item: "brake_pads", job_id: null }, { type: "labor", desc: "עבודה", qty: 1, price: null, hours: 1.5, part_id: null, item: null, job_id: null }] }; } };
  Object.defineProperty(window, "TipulitCloud", { get: () => s, set: () => {} });
});
await q.goto("http://localhost:8150/garage/"); await q.waitForTimeout(1500);
await q.click('#rows [data-wo]'); await q.waitForTimeout(300);
await q.fill("#wo-ai", "רפידות קדמיות, שעה וחצי"); await q.click("#wo-ai-go"); await q.waitForTimeout(300);
const sent = await q.evaluate(() => window.__ai);
console.log("real: task", sent.task, "| ctx stock/catalog/rate:", sent.ctx.stock.length, sent.ctx.catalog.length, sent.ctx.labor_rate, "| lines:", await q.$$eval("#wo-lines tr", l => l.map(e => e.children[0].textContent.trim() + ":" + e.querySelector("input").value + " ₪" + e.querySelectorAll("input")[2].value)), "| km", await q.inputValue("#wo-km"), "| notes", await q.inputValue("#wo-notes"));
await q.fill("#wo-ai", "נכשל"); await q.click("#wo-ai-go"); await q.waitForTimeout(200); console.log("error msg:", await q.textContent("#wo-ai-msg"));
console.log("errors:", errs); await b.close(); srv.close();
