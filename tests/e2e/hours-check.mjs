// The garage's opening hours and the booking page agree; the demo's sample appointments can be cleared for a clean test.
import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const ct = f => f.endsWith(".css") ? "text/css" : f.endsWith(".js") ? "text/javascript" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8";
const srv = createServer((q, r) => { let u = q.url.split("?")[0]; if (u.endsWith("/")) u += "index.html"; const f = SITE + u; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", ct(f)); r.end(readFileSync(f)); }).listen(8160);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const errs = [], fail = m => console.log("FAIL " + m);
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, timezoneId: "Asia/Jerusalem" });
const g = await ctx.newPage(); g.on("pageerror", e => errs.push("garage: " + e.message));
await g.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort());
await g.goto("http://localhost:8160/garage/?demo"); await g.waitForTimeout(1500);
await g.click('.tab[data-tab="calendar"]'); await g.waitForTimeout(400);
const store = () => g.evaluate(() => JSON.parse(localStorage.getItem("tipulit-garage-demo")));
const samples0 = (await store()).appts.filter(a => a.sample || /^dap-(\d+-\d+|ns-)/.test(a.id)).length;
console.log("sample appointments at start:", samples0); if (!samples0) fail("demo has no sample appointments");
// 1. new week: Sunday 10-14 only, the rest closed
await g.click("#cal-settings"); await g.waitForTimeout(300);
for (let i = 1; i < 7; i++) { const cb = await g.$(`#bk-hours [data-hd="${i}"]`); if (await cb.isChecked()) await cb.uncheck(); }
const sun = await g.$('#bk-hours [data-hd="0"]'); if (!(await sun.isChecked())) await sun.check();
await g.fill('#bk-hours [data-ho="0"]', "10:00"); await g.fill('#bk-hours [data-hc="0"]', "14:00");
await g.click("#bk-save"); await g.waitForTimeout(500);
const st1 = await store();
console.log("saved hours:", JSON.stringify(st1.garage.hours));
if (!st1.garage.hours || !st1.garage.hours[0] || st1.garage.hours[0].open !== "10:00" || st1.garage.hours[1] !== null) fail("hours not saved");
// checked in the page, in Israel time
const outside = await g.evaluate(() => JSON.parse(localStorage.getItem("tipulit-garage-demo")).appts.filter(a => (a.sample || /^dap-\d+-\d+/.test(a.id)) && (() => { const d = new Date(a.starts_at), m = d.getHours() * 60 + d.getMinutes(); return d.getDay() !== 0 || m < 600 || m + a.minutes > 840; })()).map(a => a.id));
console.log("sample appointments outside the new week:", outside.length); if (outside.length) fail("samples not redrawn inside the new hours");
// 2. the booking page offers only Sunday 10:00-13:00 starts
const c = await ctx.newPage(); c.on("pageerror", e => errs.push("book: " + e.message));
await c.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort());
await c.goto("http://localhost:8160/book/?demo"); await c.waitForTimeout(800);
const days = await c.$$eval("#b-days .chip", l => l.map(e => e.textContent)), slots = await c.$$eval("#b-slots .chip", l => l.map(e => e.textContent));
console.log("booking days:", days.slice(0, 4), "slots:", slots);
if (!days.length || days.some(d => !/א[׳']|ראשון/.test(d))) fail("booking page offers days other than Sunday");
if (slots.some(s => s < "10:00" || s > "13:00")) fail("booking page slots outside 10:00-14:00");
// 3. clear the samples: the calendar and the booking page are empty of them, and they stay gone after a reload
await g.click("#cal-settings"); await g.waitForTimeout(300); await g.click("#bk-clear"); await g.waitForTimeout(400);
console.log("toast:", await g.textContent("#toast"));
await g.reload(); await g.waitForTimeout(1500);
const st2 = await store(), left = st2.appts.filter(a => a.sample || /^dap-(\d+-\d+|ns-)/.test(a.id)).length;
console.log("samples after clear + reload:", left, "noSample:", st2.noSample); if (left) fail("samples came back");
await c.reload(); await c.waitForTimeout(800);
const free = await c.$$eval("#b-slots .chip", l => l.length);
console.log("free slots on the first Sunday after clearing:", free); if (free < 4) fail("booking page still blocked after clearing");
console.log("errors:", errs);
await b.close(); srv.close();
