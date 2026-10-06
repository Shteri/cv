// Timeline: a past service tells what was done, in the past tense: "הוחלף" from its record, "לא נרשם" for what the
// book called for and the record lacks; a past service with no record says so and offers to log it.
import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const srv = createServer((q, r) => { let f = SITE + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8150);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 400, height: 900 } });
const errs = []; p.on("pageerror", e => errs.push(e.message));
const ok = (c, m) => console.log((c ? "OK   " : "FAIL ") + m);
await p.route("https://**", r => r.abort());
await p.goto("http://localhost:8150/"); await p.waitForTimeout(200);
// the 55,000 was done (oil and filter only), the 35,000 was not recorded
await p.evaluate(() => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "guest" }, cars: [{ plate: "12-345-67", schedule: "hyundai-i10-2014-2019", year: 2017, km: 88000, kmMonth: 1500, lastService: "2024-06",
  history: [{ id: "s60", kind: "service", svcKm: 55000, km: 56000, date: "2024-06", items: ["engine_oil", "oil_filter"], garage: "מוסך יוסי", price: 900, receipts: [], share: false }] }], active: 0 })));
await p.reload(); await p.waitForTimeout(600);
await p.click('#nav button[data-go="tl"]'); await p.waitForTimeout(400);
const items = await p.$$eval("#tl-body .tl-item", l => l.map(e => ({ cls: e.className, text: e.textContent.replace(/\s+/g, " "), acts: [...e.querySelectorAll(".act")].map(a => a.textContent.trim()) })));
const s60 = items.find(x => /55,000 ק"מ/.test(x.text)), s75 = items.find(x => /35,000 ק"מ/.test(x.text)); // this schedule: 35,000, 55,000, 75,000…
console.log("heads:", items.map(x => x.text.slice(0, 40)).join(" / ")); console.log("60k:", s60 && s60.text.slice(0, 220)); console.log("75k:", s75 && s75.text.slice(0, 200));
ok(s60 && /בוצע/.test(s60.text) && /מוסך יוסי/.test(s60.text) && s60.acts.includes("הוחלף") && !s60.acts.some(a => a === "החלפה" || a === "בדיקה"), "a recorded past service says what was replaced, in the past tense");
ok(s60 && /לא נרשם/.test(s60.text), "and what the book called for that isn't in the record");
ok(s75 && /missed/.test(s75.cls) && /לא נרשם טיפול/.test(s75.text) && /עשיתי את הטיפול הזה/.test(s75.text), "a past service with no record says so and offers to log it");
console.log("errors:", errs);
await b.close(); srv.close();
