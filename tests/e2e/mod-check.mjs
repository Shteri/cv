import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const ct = f => f.endsWith(".css") ? "text/css" : f.endsWith(".js") ? "text/javascript" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8";
const srv = createServer((q, r) => { let u = q.url.split("?")[0]; if (u.endsWith("/")) u += "index.html"; const f = SITE + u; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", ct(f)); r.end(readFileSync(f)); }).listen(8147);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const errs = [];
const tabs = p => p.$$eval(".tab", l => l.filter(e => !e.hidden).map(e => e.textContent));
// demo: switch modules off
let p = await b.newPage({ viewport: { width: 1440, height: 900 } }); p.on("pageerror", e => errs.push(e.message));
await p.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort());
await p.goto("http://localhost:8147/garage/?demo"); await p.waitForTimeout(1500);
console.log("demo tabs:", await tabs(p));
await p.click("#btn-modules"); console.log("modules:", await p.$$eval("#md-list label", l => l.map(e => e.querySelector("b").textContent + (e.querySelector("input").checked ? "+" : "-"))));
await p.uncheck('#md-list [data-mod="stock"]'); await p.uncheck('#md-list [data-mod="billing"]'); await p.click("#md-save"); await p.waitForTimeout(300);
console.log("after off:", await tabs(p));
await p.click('#rows [data-wo]'); await p.waitForTimeout(300);
console.log("wo save-inv hidden:", await p.$eval("#wo-save-inv", e => e.hidden), "| lines from stock:", await p.$$eval("#wo-lines td:first-child", l => l.filter(e => e.textContent.includes("מהמלאי")).length));
await p.evaluate(() => document.querySelectorAll("dialog[open]").forEach(d => d.close()));
await p.click('#rows [data-cust="dcus-1"]'); await p.waitForTimeout(400); console.log("card invoice buttons:", await p.$$eval("#cc-timeline [data-inv]", l => l.length));
// real mode: body-shop garage from the registry, and a garage that saved its own choice
const stub = (gid, modules) => () => {};
for (const [gid, modules, label] of [[(process.argv[2] || "5392"), null, "body shop"], [(process.argv[3] || "40200"), null, "mechanics"], [(process.argv[3] || "40200"), ["billing"], "chose billing only"]]) {
  const c = await b.newContext({ viewport: { width: 1440, height: 900 } }); const q = await c.newPage(); q.on("pageerror", e => errs.push(label + ": " + e.message));
  await q.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort()); await q.route("https://data.gov.il/**", r => r.abort());
  await q.addInitScript(([gid, modules]) => {
    const G = "11111111-1111-1111-1111-111111111111"; window.__loads = [];
    const rec = n => async () => { window.__loads.push(n); return []; };
    const s = { enabled: true, hasAuthParams: false, currentUser: async () => ({ id: "u", email: "g@x" }),
      myGarageProfiles: async () => [{ id: G, garage_id: +gid, name: "מוסך", status: "verified", modules }],
      garageBook: async () => [], workOrders: async () => [], parts: rec("parts"), suppliers: rec("suppliers"), purchaseOrders: rec("pos"), invoices: rec("invoices"), billing: async () => null };
    Object.defineProperty(window, "TipulitCloud", { get: () => s, set: () => {} });
  }, [gid, modules]);
  await q.goto("http://localhost:8147/garage/"); await q.waitForTimeout(1500);
  await q.click("#btn-modules");
  console.log(label + ":", await tabs(q), "| loaded:", await q.evaluate(() => window.__loads.join(",")), "|", await q.textContent("#md-from"));
  await c.close();
}
console.log("errors:", errs); await b.close(); srv.close();
