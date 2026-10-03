import { createRequire } from "module";
const require = createRequire("/opt/node-tools/node_modules/");
const { chromium } = require("playwright");
const fs = await import("fs");
const OUT = process.argv[2];
const GF = "/tmp/claude-0/-home-user-cv/5708ed44-0317-5aa0-81b0-b42ec72148c9/scratchpad/gfonts/";
const b = await chromium.launch();
async function ctxFor(vp, dpr) {
  const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: dpr, colorScheme: "light", locale: "he-IL", timezoneId: "Asia/Jerusalem" });
  await ctx.route("https://fonts.googleapis.com/**", r => r.fulfill({ status: 200, contentType: "text/css", body: fs.readFileSync(GF + "fonts.css", "utf8") }));
  await ctx.route("https://fonts.gstatic.com/**", r => { const f = r.request().url().replace("https://fonts.gstatic.com/", "").replace(/\//g, "_"); try { r.fulfill({ status: 200, contentType: "font/woff2", body: fs.readFileSync(GF + f) }); } catch (e) { r.abort(); } });
  return ctx;
}
const d = await ctxFor({ width: 1440, height: 900 }, 2);
const p = await d.newPage(); p.on("pageerror", e => console.log("ERR", e.message));
await p.goto("http://localhost:8765/garage/?demo", { waitUntil: "networkidle" }); await p.waitForTimeout(1500);
const R = {};
const rects = (name, sels) => p.evaluate(sels => { const o = {}; for (const [k, sel] of Object.entries(sels)) { const e = document.querySelector(sel); if (e) { const r = e.getBoundingClientRect(); o[k] = [r.left, r.top, r.width, r.height].map(v => Math.round(v * 2)); } } return o; }, sels).then(v => R[name] = v);
await rects("g_customers", { kpis: ".kpis, #kpis, .stats", firstRow: "#rows tr", wa: "#rows [data-msg]", wo: "#rows [data-wo]", table: "#rows" });
await p.screenshot({ path: `${OUT}/g_customers.png` });
await p.click("#rows [data-msg]"); await p.waitForTimeout(800);
await rects("g_msg", { dlg: "#dlg-msg" }); await p.screenshot({ path: `${OUT}/g_msg.png` });
await p.keyboard.press("Escape"); await p.waitForTimeout(500);
await p.click("#rows [data-wo]"); await p.waitForTimeout(900);
await rects("g_wo", { dlg: "#dlg-wo", items: "#wo-items", lines: "#wo-lines", total: "#wo-total", send: "#wo-send-row" }); await p.screenshot({ path: `${OUT}/g_wo.png` });
await p.keyboard.press("Escape"); await p.waitForTimeout(500);
await p.click('button.tab[data-tab="calendar"]'); await p.waitForTimeout(700);
for (let i = 0; i < 3; i++) { const n = await p.evaluate(() => document.querySelectorAll("#view-calendar .appt, #view-calendar [data-appt]").length); if (n > 2) break; await p.click("#cal-prev"); await p.waitForTimeout(700); }
await rects("g_calendar", { grid: "#view-calendar .cal, #view-calendar .grid, #view-calendar table" }); await p.screenshot({ path: `${OUT}/g_calendar.png` });
await p.click('button.tab[data-tab="order"]'); await p.waitForTimeout(800);
await rects("g_order", { table: "#view-order table" }); await p.screenshot({ path: `${OUT}/g_order.png` });
fs.writeFileSync(`${OUT}/rects.json`, JSON.stringify(R, null, 1));
const m = await ctxFor({ width: 390, height: 844 }, 3);
const q = await m.newPage(); q.on("pageerror", e => console.log("ERR", e.message));
for (const [u, n] of [["approve/?demo", "m_approve"], ["book/?demo", "m_book"]]) { await q.goto("http://localhost:8765/" + u, { waitUntil: "networkidle" }); await q.waitForTimeout(1200); await q.screenshot({ path: `${OUT}/${n}.png` }); }
await b.close();
