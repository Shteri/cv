// All records: one short line each (no notes), 6 shown with "הצג את כל", select several and delete them.
// The registry is read again, so a renewed test date replaces the old one.
import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const srv = createServer((q, r) => { let f = SITE + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8145);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 400, height: 900 } });
const errs = []; p.on("pageerror", e => errs.push(e.message)); p.on("dialog", d => d.accept());
const ok = (c, m) => console.log((c ? "OK   " : "FAIL ") + m);
// the registry answers with a renewed test
await p.route("https://data.gov.il/**", r => r.request().url().includes("053cea08") ? r.fulfill({ contentType: "application/json", body: JSON.stringify({ result: { records: [{ mispar_rechev: 6599432, tozeret_nm: "אלפא רומיאו", kinuy_mishari: "GIULIETTA", shnat_yitzur: 2014, tokef_dt: "2027-09-20", mivchan_acharon_dt: "2026-09-21" }] } }) }) : r.fulfill({ contentType: "application/json", body: JSON.stringify({ result: { records: [] } }) }));
await p.goto("http://localhost:8145/"); await p.waitForTimeout(200);
const hist = Array.from({ length: 9 }, (_, i) => ({ id: "r" + i, kind: i % 3 ? "service" : "repair", svcKm: 15000 * (i + 1), text: i % 3 ? "" : "החלפת משאבת ואקום ובדיקת מערכת הבלמים המלאה כולל צנרת", km: 15000 * (i + 1), date: `20${15 + i}-03`,
  items: ["engine_oil", "oil_filter", "air_filter"], garage: "מוסך התלתן", city: "פתח תקווה", where: "independent", price: 900 + i, extra: "הנחה באישור תומר", receipts: [], share: false }));
await p.evaluate(h => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "guest" }, cars: [{ plate: "65-994-32", schedule: "hyundai-i10-2014-2019", year: 2014, km: 150000, kmMonth: 1500, lastService: "2023-03", gov: { test_expiry: "2026-09-20" }, history: h }], active: 0 })), hist);
await p.reload(); await p.waitForTimeout(800);
const gov = await p.evaluate(() => JSON.parse(localStorage.getItem("tipulit")).cars[0].gov);
ok(gov.test_expiry === "2027-09-20", "the renewed test date replaces the old one: " + gov.test_expiry);
await p.click('#nav button[data-go="car"]'); await p.waitForTimeout(300);
ok(/2027/.test(await p.textContent("#car-sub")), "the car screen shows it: " + await p.textContent("#car-sub"));
const rows = () => p.$$eval("#car-history .hist", l => l.length);
const text = await p.textContent("#car-history");
ok(await rows() === 6 && /הצג את כל 9/.test(text), "six records, then 'show all 9'");
ok(!/תומר/.test(text) && !/שמן מנוע/.test(text) && !/מוסך פרטי/.test(text), "no notes, parts or garage type in the list");
ok(await p.$$eval("#car-history .hist .edit", l => l.length) === 6, "every row has the edit mark");
ok(/2023/.test(await p.$eval("#car-history .hist", e => e.textContent)), "newest first");
await p.click("#hist-more"); await p.waitForTimeout(200); ok(await rows() === 9, "show all");
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/hist.png" });
// select two and delete them
await p.click("#hist-select"); await p.waitForTimeout(200);
await p.click('[data-pick="r8"]'); await p.click('[data-pick="r7"]'); await p.waitForTimeout(100);
ok(/מחק 2 רשומות/.test(await p.textContent("#hist-del")), "the delete button counts the picked");
await p.click("#hist-del"); await p.waitForTimeout(300);
const left = await p.evaluate(() => JSON.parse(localStorage.getItem("tipulit")).cars[0].history.map(h => h.id));
ok(left.length === 7 && !left.includes("r8") && !left.includes("r7"), "two deleted: " + left.join());
ok(await p.isVisible("#hist-select"), "back out of select mode");
console.log("errors:", errs);
await b.close(); srv.close();
