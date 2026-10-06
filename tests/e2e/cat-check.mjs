import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const ct = f => f.endsWith(".css") ? "text/css" : f.endsWith(".js") ? "text/javascript" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8";
const srv = createServer((q, r) => { let u = q.url.split("?")[0]; if (u.endsWith("/")) u += "index.html"; const f = SITE + u; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", ct(f)); r.end(readFileSync(f)); }).listen(8148);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const errs = [];
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.5, timezoneId: "Asia/Jerusalem" });
const p = await ctx.newPage(); p.on("pageerror", e => errs.push(e.message));
await p.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort());
await p.goto("http://localhost:8148/garage/?demo"); await p.waitForTimeout(1500);
const close = () => p.evaluate(() => document.querySelectorAll("dialog[open]").forEach(d => d.close()));
console.log("tabs:", await p.$$eval(".tab", l => l.filter(e => !e.hidden).map(e => e.textContent).join(",")));
// catalog tab
await p.click('.tab[data-tab="catalog"]'); await p.waitForTimeout(300);
console.log("jobs:", await p.$$eval("#cg-rows tr", l => l.length), "| rate:", await p.inputValue("#cg-rate"), "| first:", await p.$eval("#cg-rows tr", e => e.textContent.replace(/\s+/g, " ").trim().slice(0, 100)));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/cat-tab.png" });
await p.fill("#cg-rate", "300"); await p.dispatchEvent("#cg-rate", "change"); await p.waitForTimeout(200);
console.log("after rate 300:", await p.$eval("#cg-rows tr", e => e.textContent.replace(/\s+/g, " ").trim().slice(0, 100)));
await p.click("#cg-new"); await p.fill("#jb-name", "החלפת משאבת מים"); await p.fill("#jb-cat", "מנוע"); await p.fill("#jb-hours", "2.5"); await p.click('#jb-items .chip[data-it="coolant"]');
await p.fill('#jb-qty input[data-i="0"]', "2"); await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/cat-job.png" }); await p.click("#jb-save"); await p.waitForTimeout(200);
console.log("job added:", await p.textContent("#toast"), (await p.$$eval("#cg-rows tr", l => l.length)));
await p.click("#cg-suggest"); console.log("suggest left:", await p.$$eval("#sg-list [data-sg]", l => l.length)); await close();
// work order: add from catalog
await p.click('.tab[data-tab="customers"]'); await p.click('#rows [data-wo]'); await p.waitForTimeout(300);
const before = await p.$$eval("#wo-lines tr", l => l.length);
await p.click("#wo-add-job"); await p.fill("#pk-q", "רפידות"); await p.waitForTimeout(100);
console.log("pick:", await p.$$eval("#pk-list [data-pk]", l => l.map(e => e.textContent.replace(/\s+/g, " ").trim())));
await p.click("#pk-list [data-pk]"); await p.waitForTimeout(200);
console.log("wo lines:", before, "->", await p.$$eval("#wo-lines tr", l => l.map(e => e.children[0].textContent.trim() + ":" + e.querySelector("input").value + " ₪" + e.querySelectorAll("input")[2].value).slice(-3)));
await close();
// appointment: inspection
await p.click('.tab[data-tab="calendar"]'); await p.waitForTimeout(300);
await p.locator('#cal .appt[data-st="in_progress"], #cal .appt[data-st="booked"]').first().click(); await p.waitForTimeout(200); // which statuses the demo day has depends on the hour
console.log("appt actions:", await p.$$eval("#ap-actions .btn", l => l.map(e => e.textContent.trim()).join(" | ")));
await p.locator('#ap-actions [data-act-appt]', { hasText: "בדיקת רכב" }).click(); await p.waitForTimeout(300);
console.log("insp rows:", await p.$$eval("#in-rows .insp-row", l => l.length));
await p.click('#in-rows .insp-row[data-i="0"] .seg button[data-v="now"]'); await p.waitForTimeout(100);
await p.fill('#in-rows .insp-row[data-i="0"] input[data-k="note"]', "נשארו 2 מ\"מ");
await p.click('#in-rows .insp-row[data-i="12"] .seg button[data-v="soon"]');
await p.setInputFiles('#in-rows [data-photo="0"]', { name: "a.png", mimeType: "image/png", buffer: readFileSync((process.env.SHOTS || "/tmp") + "/cat-tab.png") }); await p.waitForTimeout(800);
await p.click("#in-allok"); await p.waitForTimeout(100);
console.log("insp sum:", await p.textContent("#in-sum"), "| total:", await p.textContent("#in-total"), "| fixes:", await p.$$eval("#in-rows .insp-fix", l => l.map(e => (e.querySelector("select") ? e.querySelector("select").selectedOptions[0].textContent : "-") + " " + e.querySelector("input").value)), "| thumbs:", await p.$$eval("#in-rows .thumb", l => l.length));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/insp.png" });
await p.click("#in-send"); await p.waitForTimeout(400);
console.log("sent msg:", (await p.inputValue("#msg-text")).slice(0, 200));
await close();
console.log("statuses after:", await p.$$eval("#cal .appt", l => l.map(e => e.dataset.st).join(",")));
// customer card: inspection in history + car action
await p.click('.tab[data-tab="customers"]'); await p.click('#rows [data-cust="dcus-1"]'); await p.waitForTimeout(400);
console.log("card insp rows:", await p.$$eval("#cc-timeline .tl-row", l => l.filter(e => e.textContent.includes("בדיקת רכב")).map(e => e.textContent.replace(/\s+/g, " ").trim().slice(0, 120))), "| car actions:", await p.$$eval("#cc-cars [data-act-car]", l => l.map(e => e.textContent)));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/insp-card.png" });
await close();
// modules dialog lists the new ones
await p.click("#btn-modules"); console.log("modules:", await p.$$eval("#md-list b", l => l.map(e => e.textContent).join(", ")));
console.log("errors:", errs); await b.close(); srv.close();
