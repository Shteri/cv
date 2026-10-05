import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const root = SITE;
const srv = createServer((q, r) => { let f = root + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8136);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 400, height: 900 } });
const errs = []; p.on("pageerror", e => errs.push(e.message)); p.on("dialog", d => d.accept());
await p.goto("http://localhost:8136/"); await p.waitForTimeout(200);
const all = ["engine_oil", "oil_filter", "cabin_filter"];
const hist = [{ id: "a", kind: "service", svcKm: 35000, km: 35000, date: "2024-01", items: [...all, "air_filter", "brake_fluid"], receipts: [], share: false },
  { id: "b", kind: "service", svcKm: 55000, km: 55000, date: "2025-01", items: all, receipts: [], share: false }];
await p.evaluate(h => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "guest" }, cars: [{ plate: "12-345-67", schedule: "hyundai-i10-2014-2019", year: 2017, km: 70000, kmMonth: 1500, lastService: "2025-01", history: h }], active: 0 })), hist);
await p.reload(); await p.waitForTimeout(400);
await p.click('#nav button[data-go="car"]').catch(async () => { await p.evaluate(() => document.querySelector("#to-car").click()); }); await p.waitForTimeout(300);
const row = k => p.evaluate(k => { const e = document.querySelector(`#car-state [data-item="${k}"]`); return e ? e.innerText.replace(/\s+/g, " ") : null; }, k);
console.log("before air:", await row("air_filter"));
await p.evaluate(() => document.querySelector('#car-state [data-item="air_filter"]').click()); await p.waitForTimeout(200);
console.log("sheet:", await p.locator("#it-title").innerText(), "|", await p.locator("#it-now").innerText());
await p.fill("#it-km", "90000"); await p.click("#it-save"); console.log("err:", await p.locator("#it-err").innerText());
await p.fill("#it-km", "68000"); await p.fill("#it-date", "2025-09"); await p.click("#it-save"); await p.waitForTimeout(300);
console.log("after air:", await row("air_filter"));
// spark plugs unknown -> set
await p.evaluate(() => document.querySelector('#car-state [data-item="spark_plugs"]').click()); await p.waitForTimeout(200);
await p.fill("#it-km", "60000"); await p.click("#it-save"); await p.waitForTimeout(300);
console.log("plugs:", await row("spark_plugs"));
// correct oil filter down to 35000: removes it from the 55k service
await p.evaluate(() => document.querySelector('#car-state [data-item="oil_filter"]').click()); await p.waitForTimeout(200);
await p.fill("#it-km", "35000"); await p.click("#it-save"); await p.waitForTimeout(300);
console.log("oil filter:", await row("oil_filter"));
// cabin filter -> unknown
await p.evaluate(() => document.querySelector('#car-state [data-item="cabin_filter"]').click()); await p.waitForTimeout(200);
await p.click("#it-unknown"); await p.waitForTimeout(300);
console.log("cabin:", await row("cabin_filter"));
const st = await p.evaluate(() => JSON.parse(localStorage.getItem("tipulit")).cars[0].history.map(h => `${h.source || h.kind}@${h.km}[${h.items.join(" ")}]`));
console.log("history:", st);
const histText = await p.evaluate(() => document.querySelector("#car-history").innerText.replace(/\s+/g, " "));
console.log("history list:", histText.slice(0, 200));
console.log(/מסנן אוויר למנוע: עדכנת/.test(histText) && /מצתים: עדכנת/.test(histText) ? "OK   manual updates show in all records" : "FAIL manual updates missing from all records");
console.log(await p.evaluate(() => document.querySelectorAll("#car-state .state .edit").length) > 0 ? "OK   item rows show the edit mark" : "FAIL no edit mark on item rows");
await p.click('#nav button[data-go="home"]'); await p.waitForTimeout(300);
console.log("hero:", (await p.locator("#home-body .card.ink .items").innerText()).replace(/\s+/g, " "));
await p.click('#nav button[data-go="car"]').catch(() => {}); await p.waitForTimeout(200);
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/state-edit.png" });
console.log("errors:", errs);
await b.close(); srv.close();
