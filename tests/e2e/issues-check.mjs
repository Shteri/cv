// "דברים לבדוק": a repair that names front tires without marking them, next to a manual tire update of the same
// change, is offered as one; km that goes back and two records of one visit are flagged; "התעלם" hides one.
import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const srv = createServer((q, r) => { let f = SITE + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8146);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 400, height: 900 } });
const errs = []; p.on("pageerror", e => errs.push(e.message));
const ok = (c, m) => console.log((c ? "OK   " : "FAIL ") + m);
await p.route("https://data.gov.il/**", r => r.abort());
await p.goto("http://localhost:8146/"); await p.waitForTimeout(200);
const R = (id, o) => ({ id, receipts: [], share: false, items: [], ...o });
const hist = [
  R("s1", { kind: "service", svcKm: 150000, km: 147000, date: "2024-06", items: ["engine_oil"], price: 1030 }),
  R("s2", { kind: "service", svcKm: 150000, km: 140000, date: "2024-09", items: ["engine_oil"], price: 900 }),         // km back
  R("t1", { kind: "repair", km: 175943, date: "2026-09", text: "צמיגים קדמיים הוחלפו", price: 950 }),
  R("m1", { kind: "other", source: "state", text: "עדכון מצב: צמיגים", km: 175000, date: null, items: ["tires"], tires: ["fl", "fr"] }),
  R("d1", { kind: "repair", km: 160000, date: "2025-03", text: "מצבר", price: 600, items: ["battery_12v"] }),
  R("d2", { kind: "repair", km: 160100, date: "2025-03", text: "החלפת מצבר", price: 600, items: ["battery_12v"] }),       // same visit twice
];
await p.evaluate(h => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "guest" }, cars: [{ plate: "65-994-32", schedule: "hyundai-i10-2014-2019", year: 2014, km: 176000, kmMonth: 1500, lastService: "2024-09", history: h }], active: 0 })), hist);
await p.reload(); await p.waitForTimeout(600);
await p.click('#nav button[data-go="car"]'); await p.waitForTimeout(300);
const box = () => p.textContent("#car-issues");
let t = await box(); console.log("issues:", t.replace(/\s+/g, " "));
ok(/צמיגים קדמיים הוחלפו/.test(t) && /אותה החלפה/.test(t) && /חבר לרשומה אחת/.test(t), "the repair and the manual tire update are offered as one");
ok(/הק"מ יורד/.test(t), "km going back is flagged");
ok(/אותו ביקור/.test(t), "two records of one visit are flagged");
// connect: the repair now marks the front tires, the manual update is gone
await p.click('#car-issues [data-issue-fix="0"]'); await p.waitForTimeout(300);
const car = await p.evaluate(() => JSON.parse(localStorage.getItem("tipulit")).cars[0]);
const t1 = car.history.find(h => h.id === "t1"), m1 = car.history.find(h => h.id === "m1");
ok(t1.items.includes("tires") && t1.tires.join() === "fl,fr" && !m1.items.includes("tires"), "connected: the record marks the front tires, the manual one gives way");
ok(/זוג קדמי: 175,943/.test(await p.textContent('#car-state [data-item="tires"]')), "the tires row now counts from the record");
// dismiss one
const before = await p.$$eval("#car-issues [data-issue-off]", l => l.length);
await p.click('#car-issues [data-issue-off="0"]'); await p.waitForTimeout(200);
ok(await p.$$eval("#car-issues [data-issue-off]", l => l.length) === before - 1, "'התעלם' hides it");
console.log("errors:", errs);
await b.close(); srv.close();
