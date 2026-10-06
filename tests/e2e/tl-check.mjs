import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const srv = createServer((q, r) => { const f = SITE + (q.url === "/" ? "/index.html" : q.url.split("?")[0]); if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8137);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" }); const p = await b.newPage({ viewport: { width: 400, height: 860 }, deviceScaleFactor: 2 });
const errs = []; p.on("pageerror", e => errs.push(e.message + " @ " + (e.stack || "").split("\n")[1])); for (const u of ["https://data.gov.il/**", "https://cdn.jsdelivr.net/**", "https://fonts.g**"]) await p.route(u, r => r.abort());
await p.goto("http://localhost:8137/"); await p.evaluate(() => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "guest" }, cars: [{ plate: "12-345-67", schedule: "kia-picanto-2017-2025", year: 2020, km: 43800, kmMonth: 1500 }], active: 0 }))); await p.reload(); await p.waitForTimeout(500);
await p.click("#to-garage"); await p.waitForTimeout(500);
console.log("screen:", await p.$$eval(".screen", l => l.filter(e => !e.hidden).map(e => e.id)));
const next = await p.$(".tl-item.next"); console.log("next item:", !!next, next && await next.evaluate(e => e.className));
console.log("checklist visible:", await p.$$eval(".tl-item.next .chk", l => l.filter(e => e.offsetParent).length), "tips fold:", await p.$$eval(".tl-item.next details.fold", l => l.length));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/tl-now.png" });
if (await p.$(".tl-item.next details.fold summary")) { await p.click(".tl-item.next details.fold summary"); await p.waitForTimeout(200); console.log("tips open:", await p.$eval(".tl-item.next details.fold", e => e.open), "tl item still open:", await p.$eval(".tl-item.next", e => e.classList.contains("open"))); }
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/tl-now2.png", fullPage: true });
console.log("errors:", errs); await b.close(); srv.close();
