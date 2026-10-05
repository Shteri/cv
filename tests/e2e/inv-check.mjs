import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const ct = f => f.endsWith(".css") ? "text/css" : f.endsWith(".js") ? "text/javascript" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8";
const srv = createServer((q, r) => { let u = q.url.split("?")[0]; if (u.endsWith("/")) u += "index.html"; const f = SITE + u; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", ct(f)); r.end(readFileSync(f)); }).listen(8145);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const errs = [];
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.5, timezoneId: "Asia/Jerusalem" });
const p = await ctx.newPage(); p.on("pageerror", e => errs.push(e.message));
await p.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort());
await p.goto("http://localhost:8145/garage/?demo"); await p.waitForTimeout(1500);
const close = () => p.evaluate(() => document.querySelectorAll("dialog[open]").forEach(d => d.close()));
// forecast with stock
await p.click('.tab[data-tab="order"]'); await p.waitForTimeout(300);
console.log("fc rows:", await p.$$eval("#fc-rows tr", l => l.slice(0, 6).map(e => [...e.children].slice(0, 4).map(td => td.textContent.replace(/\s+/g, " ").trim()).join(" | "))));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/inv-forecast.png" });
await p.click("#fc-po"); await p.waitForTimeout(400);
console.log("fc-po toast:", await p.textContent("#toast"), "| tab:", await p.$eval(".tab.on", e => e.dataset.tab));
console.log("pos:", await p.$$eval("#st-rows tr", l => l.map(e => e.textContent.replace(/\s+/g, " ").trim().slice(0, 110))));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/inv-pos.png" });
// parts list
await p.click('#st-seg button[data-v="parts"]'); await p.waitForTimeout(200);
console.log("kpis:", (await p.textContent("#st-kpis")).replace(/\s+/g, " "));
console.log("parts rows:", await p.$$eval("#st-rows tr", l => l.length), "first:", await p.$eval("#st-rows tr", e => e.textContent.replace(/\s+/g, " ").trim().slice(0, 120)));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/inv-parts.png" });
// new part with opening stock
await p.click("#st-new"); await p.fill("#pt-sku", "TEST-1"); await p.selectOption("#pt-item", "wipers"); await p.fill("#pt-min", "4"); await p.fill("#pt-stock", "10"); await p.fill("#pt-cost", "20"); await p.fill("#pt-price", "45");
console.log("auto name:", await p.inputValue("#pt-name"));
await p.click("#pt-save"); await p.waitForTimeout(300); console.log("part add:", await p.textContent("#toast"));
await p.click("#st-new"); await p.fill("#pt-sku", "test-1"); await p.fill("#pt-name", "כפול"); await p.click("#pt-save"); console.log("dup sku err:", await p.textContent("#pt-err")); await close();
// count
const cnt = await p.$('#st-rows [data-count="dpt-4"]'); await cnt.click(); await p.fill("#ct-qty", "5"); await p.click("#ct-save"); await p.waitForTimeout(200);
await p.click('#st-rows [data-part="dpt-4"]'); await p.waitForTimeout(300); console.log("moves:", (await p.textContent("#pt-moves")).replace(/\s+/g, " ")); await close();
// receive the sent PO
await p.click('#st-seg button[data-v="pos"]'); await p.click('#st-rows [data-po="dpo-2"]'); await p.waitForTimeout(200);
console.log("po actions:", await p.$$eval("#po-actions .btn", l => l.map(e => e.textContent)));
await p.click("#po-recv"); await p.fill('#po-lines input[data-k="recv"][data-i="0"]', "8"); await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/inv-receive.png" });
await p.click("#po-confirm"); await p.waitForTimeout(300); console.log("received:", await p.textContent("#toast"), await p.textContent("#po-status")); await close();
await p.click('#st-seg button[data-v="parts"]'); console.log("toyota filter stock after:", await p.$eval('#st-rows [data-part="dpt-4"]', e => e.closest("tr").children[3].textContent.trim()));
// draft: send to supplier
await p.click('#st-seg button[data-v="pos"]'); const draft = await p.$$eval("#st-rows tr", l => l.filter(e => e.textContent.includes("טיוטה")).map(e => e.querySelector("[data-po]").dataset.po));
await p.click(`#st-rows [data-po="${draft[0]}"]`); await p.click("#po-send"); await p.waitForTimeout(300);
console.log("send msg:", (await p.inputValue("#msg-text")).slice(0, 160).replace(/\n/g, " / ")); await close();
// suppliers
await p.click('#st-seg button[data-v="sups"]'); console.log("sups:", await p.$$eval("#st-rows tr", l => l.map(e => e.textContent.replace(/\s+/g, " ").trim().slice(0, 60))));
// work order from a customer: parts from stock, save and invoice
await p.click('.tab[data-tab="customers"]'); await p.waitForTimeout(200);
const before = await p.evaluate(() => 0);
await p.click('#rows [data-wo]'); await p.waitForTimeout(300);
console.log("wo lines:", await p.$$eval("#wo-lines tr", l => l.map(e => e.children[0].textContent.trim() + ":" + e.querySelector("input").value + " x" + e.querySelectorAll("input")[1].value + " ₪" + e.querySelectorAll("input")[2].value)));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/inv-wo.png" });
for (const x of await p.$$('#wo-lines input[data-k="price"]')) if (!(await x.inputValue())) await x.fill("300");
await p.click("#wo-save-inv"); await p.waitForTimeout(400);
console.log("inv dialog open:", await p.$eval("#dlg-inv", e => e.open), "| who:", await p.textContent("#iv-who"), "| total:", await p.textContent("#iv-total"));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/inv-dialog.png" });
await p.click('#iv-pay .chip[data-v="cash"]'); await p.click("#iv-issue"); await p.waitForTimeout(300);
console.log("issued:", await p.textContent("#toast"), "|", (await p.textContent("#iv-morning-note")).trim()); await close();
// billing tab
await p.click('.tab[data-tab="billing"]'); await p.waitForTimeout(200);
console.log("billing kpis:", (await p.textContent("#bi-kpis")).replace(/\s+/g, " "), "| rows:", await p.$$eval("#bi-rows tr", l => l.length), "| open:", await p.$$eval("#bi-open [data-inv]", l => l.length));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/inv-billing.png" });
await p.click("#bi-open [data-inv]"); await p.fill("#iv-number", "777"); await p.click("#iv-record"); await p.waitForTimeout(200); console.log("manual:", await p.textContent("#toast")); await close();
await p.click("#bi-settings"); console.log("billing state:", await p.textContent("#bl-state")); await close();
// stock after work order consumption
await p.click('.tab[data-tab="stock"]'); await p.click('#st-seg button[data-v="parts"]');
console.log("oil stock now:", await p.$eval('#st-rows [data-part="dpt-1"]', e => e.closest("tr").children[3].textContent.trim()), await p.$eval('#st-rows [data-part="dpt-2"]', e => e.closest("tr").children[3].textContent.trim()));
console.log("errors:", errs); await b.close(); srv.close();
