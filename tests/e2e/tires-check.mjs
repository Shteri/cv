// Tires per wheel: replacing the front pair shows both pairs on the tires row, the item sheet lists every replacement.
import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const srv = createServer((q, r) => { let f = SITE + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8142);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 400, height: 900 } });
const errs = []; p.on("pageerror", e => errs.push(e.message)); p.on("dialog", d => d.accept());
const ok = (c, m) => console.log((c ? "OK   " : "FAIL ") + m);
await p.goto("http://localhost:8142/"); await p.waitForTimeout(200);
const hist = [{ id: "a", kind: "service", svcKm: 30000, km: 30000, date: "2022-01", items: ["engine_oil", "tires"], receipts: [], share: false, garage: "מוסך אמיר" },
  { id: "b", kind: "service", svcKm: 45000, km: 45000, date: "2023-01", items: ["engine_oil"], receipts: [], share: false }];
await p.evaluate(h => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "guest" }, cars: [{ plate: "12-345-67", schedule: "hyundai-i10-2014-2019", year: 2017, km: 70000, kmMonth: 1500, lastService: "2025-01", history: h }], active: 0 })), hist);
await p.reload(); await p.waitForTimeout(400);
await p.click('#nav button[data-go="car"]'); await p.waitForTimeout(300);
const row = () => p.evaluate(() => document.querySelector('#car-state [data-item="tires"]').textContent.replace(/\s+/g, " "));
ok(/30,000/.test(await row()) && !/זוג/.test(await row()), "all four from one record: one line: " + await row());
// the engine oil sheet lists both services
await p.evaluate(() => document.querySelector('#car-state [data-item="engine_oil"]').click()); await p.waitForTimeout(200);
ok(await p.locator("#it-hist > div").count() === 2 && await p.locator("#it-tires").isHidden(), "oil sheet: two replacements, no wheel picker");
await p.click("#it-close"); await p.waitForTimeout(200);
// front pair at 60,000
await p.evaluate(() => document.querySelector('#car-state [data-item="tires"]').click()); await p.waitForTimeout(200);
ok(await p.locator("#it-tires").isVisible() && await p.locator("#it-pos .chip.on").count() === 4, "tires sheet: wheel picker, all four on");
await p.click('#it-pos-quick [data-q="1"]'); await p.waitForTimeout(100);
ok(await p.locator("#it-pos .chip.on").count() === 2, "front pair picks two wheels");
await p.fill("#it-km", "60000"); await p.fill("#it-date", "2025-03"); await p.click("#it-save"); await p.waitForTimeout(300);
const r1 = await row(); console.log("row:", r1);
ok(/זוג קדמי: 60,000/.test(r1) && /זוג אחורי: 30,000/.test(r1), "row shows each pair");
const st = await p.evaluate(() => JSON.parse(localStorage.getItem("tipulit")).cars[0].history.filter(h => (h.items || []).includes("tires")).map(h => `${h.km}:${(h.tires || ["all"]).join("+")}`));
ok(st.join() === "30000:all,60000:fl+fr", "records: " + st.join());
// the sheet now lists both, with the pair tagged
await p.evaluate(() => document.querySelector('#car-state [data-item="tires"]').click()); await p.waitForTimeout(200);
ok(await p.locator("#it-hist > div").count() === 2 && /זוג קדמי/.test(await p.locator("#it-hist").innerText()), "tires history shows both, the newer one tagged");
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/tires-sheet.png" });
// correction: the rear right was actually done at 50,000
await p.click('#it-pos [data-pos="fl"]'); await p.click('#it-pos [data-pos="fr"]'); await p.click('#it-pos [data-pos="rl"]');
await p.fill("#it-km", "50000"); await p.fill("#it-date", ""); await p.click("#it-save"); await p.waitForTimeout(300);
const r2 = await row(); console.log("row:", r2);
ok(/זוג קדמי: 60,000/.test(r2) && /אחורי שמאל: 30,000/.test(r2) && /אחורי ימין: 50,000/.test(r2), "single wheel tracked on its own");
// the history list names the wheels
ok(/צמיגים \(זוג קדמי\)/.test(await p.locator("#car-history").innerText()), "all records names the wheels");
// unknown for the rear-left only
await p.evaluate(() => document.querySelector('#car-state [data-item="tires"]').click()); await p.waitForTimeout(200);
await p.click('#it-pos-quick [data-q="0"]'); for (const w of ["fl", "fr", "rr"]) await p.click(`#it-pos [data-pos="${w}"]`);
await p.click("#it-unknown"); await p.waitForTimeout(300);
const r3 = await row(); console.log("row:", r3);
ok(/אחורי שמאל: לא ידוע/.test(r3) && /זוג קדמי: 60,000/.test(r3), "one wheel unknown keeps the others");
await p.click('#nav button[data-go="home"]'); await p.waitForTimeout(300);
console.log("errors:", errs);
await b.close(); srv.close();
