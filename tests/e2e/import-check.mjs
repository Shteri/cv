import { chromium } from "playwright";
import XLSX from "xlsx";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
import { createRequire } from "node:module";
// Service history from a spreadsheet: a dealer-system export (one row per line) becomes visits to review, then records;
// the car's km, last service and km per month follow the file.
const require = createRequire(import.meta.url), XLSX_JS = require.resolve("xlsx/dist/xlsx.full.min.js");
const types = { js: "text/javascript", css: "text/css", json: "application/json", svg: "image/svg+xml" };
const srv = createServer((q, r) => { let f = SITE + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", types[f.split(".").pop()] || "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8159);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 400, height: 860 } });
const errs = []; let fail = 0; p.on("pageerror", e => errs.push(e.message));
const check = (label, ok, got) => { console.log(`${ok ? "OK  " : "FAIL"} ${label}${ok ? "" : " got " + JSON.stringify(got)}`); if (!ok) fail++; };
await p.route("https://cdn.jsdelivr.net/npm/xlsx@*/**", r => r.fulfill({ status: 200, contentType: "text/javascript", body: readFileSync(XLSX_JS) }));
for (const u of ["https://fonts.googleapis.com/**", "https://fonts.gstatic.com/**", "https://data.gov.il/**"]) await p.route(u, r => r.abort());
await p.goto("http://localhost:8159/"); await p.waitForTimeout(300);
await p.evaluate(() => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "guest" }, cars: [{ plate: "12-345-67", schedule: "hyundai-i10-2014-2019", year: 2015, km: 90000, kmMonth: 1500, history: [
  { id: "old", kind: "service", svcKm: 95000, km: 96229, date: "2021-07", items: ["engine_oil"], receipts: [], share: false }] }], active: 0 })));
await p.reload(); await p.waitForTimeout(500);
await p.evaluate(() => document.querySelector('#nav button[data-go="car"]').click()); await p.waitForTimeout(400);
// a dealer export, written as a real .xlsx
const H = ["תא.פתיחה", "מוסך", "כרטיס", "מד אוץ", "סוג", "מספר פריט/עבודה", "תיאור פריט/עבודה", "כמות", "שם מוסך"];
const L = (d, km, type, code, desc) => [d, 10, 1000 + km % 997, km, type, code, desc, 1, "מוסך הדוגמה"];
const rows = [H, L("27/06/2022", 110405, "ע", "0010H01", "טיפול שנה שמינית"), L("27/06/2022", 110405, "חלק", "1", "מסנן שמן"), L("27/06/2022", 110405, "חלק", "2", "שמן מנוע 5W40"), L("27/06/2022", 110405, "חלק", "3", "חולצה ממותגת"),
  L("17/03/2022", 104903, "ע", "3330D30", "פ + ה משאבת ואקום"),
  L("29/07/2021", 96229, "ע", "0010H6", "טיפול שנה שביעית"), L("29/07/2021", 96229, "חלק", "4", "מסנן שמן"),
  L("07/10/2019", 69777, "ע", "1032B10", "פ + ה רצועת תזמון"), L("07/10/2019", 69777, "חלק", "5", "מצת מנוע"),
  L("26/04/2021", 91744, "ע", "*", "מתלונן על העברת הילוכים")];
const wb = XLSX.utils.book_new(); XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(rows), "גיליון1");
await p.setInputFiles("#car-xls", { name: "CarHist.xlsx", mimeType: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", buffer: XLSX.write(wb, { type: "buffer", bookType: "xlsx" }) });
await p.waitForTimeout(800);
check("preview opens with the visits", await p.locator("#xls").evaluate(e => e.classList.contains("show")) && (await p.$$("#xls-list .xls-row")).length === 5, await p.$$eval("#xls-list .xls-row", l => l.map(e => e.innerText.replace(/\s+/g, " "))));
const txt = (await p.locator("#xls-list").innerText()).replace(/\s+/g, " ");
check("a visit already in the history is marked and left out", /כבר קיים/.test(txt));
check("parts are named, merchandise is not", /מסנן שמן/.test(txt) && /רצועת תזמון/.test(txt) && !/חולצה/.test(txt), txt.slice(0, 300));
check("button counts what is ticked (dup and notes-only unticked)", /ייבא 3 ביקורים/.test(await p.locator("#xls-go").innerText()), await p.locator("#xls-go").innerText());
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/xls-preview.png" });
await p.click("#xls-go"); await p.waitForTimeout(500);
const car = await p.evaluate(() => JSON.parse(localStorage.getItem("tipulit")).cars[0]);
const imp = car.history.filter(h => h.source === "import");
check("three records imported", imp.length === 3, imp.map(h => h.date + " " + h.kind));
check("service records get a schedule service km", imp.filter(h => h.kind === "service").every(h => h.svcKm > 0), imp.map(h => h.svcKm));
check("car km follows the file", car.km === 110405, car.km);
check("km per month from the history", car.kmMonth >= 1000 && car.kmMonth <= 1300, car.kmMonth);
check("last service from the file", car.lastService === "2022-06", car.lastService);
check("the timing belt shows in the car's state", /רצועת תזמון[\s\S]*הוחלף ב-69,777/.test(await p.locator("#car-state").innerText()) || /רצועת תזמון/.test(await p.locator("#car-history").innerText()));
console.log("errors:", errs);
await b.close(); srv.close();
process.exit(fail ? 1 : 0);
