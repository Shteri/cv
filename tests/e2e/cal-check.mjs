import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const ct = f => f.endsWith(".css") ? "text/css" : f.endsWith(".js") ? "text/javascript" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8";
const srv = createServer((q, r) => { let u = q.url.split("?")[0]; if (u.endsWith("/")) u += "index.html"; const f = SITE + u; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", ct(f)); r.end(readFileSync(f)); }).listen(8144);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const errs = [];
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.5, timezoneId: "Asia/Jerusalem" });
const p = await ctx.newPage(); p.on("pageerror", e => errs.push("cal: " + e.message));
await p.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort());
await p.goto("http://localhost:8144/garage/?demo"); await p.waitForTimeout(1500);
await p.click('.tab[data-tab="calendar"]'); await p.waitForTimeout(400);
console.log("cal date:", await p.textContent("#cal-date"), "| kpis:", (await p.textContent("#cal-kpis")).replace(/\s+/g, " "));
console.log("cal blocks:", await p.$$eval("#cal .appt", l => l.map(e => e.dataset.st + ":" + e.querySelector("b").textContent)), "cells:", await p.$$eval("#cal .cal-cell", l => l.length));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/cal-day.png" });
// open first appointment
await p.click("#cal .appt"); await p.waitForTimeout(300);
console.log("appt:", await p.textContent("#ap-title"), "|", await p.textContent("#ap-sub"));
console.log("appt actions:", await p.$$eval("#ap-actions .btn", l => l.map(e => e.textContent.trim())));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/cal-appt.png" });
await p.click('#ap-status .chip[data-st="in_progress"]'); await p.waitForTimeout(300);
console.log("status set:", await p.textContent("#toast"), "| chip on:", await p.$eval("#ap-status .chip.on", e => e.dataset.st));
// approval request
await p.click("#ap-approve"); await p.waitForTimeout(300);
await p.fill("#aw-msg", "הרפידות שחוקות");
await p.fill('#aw-lines input[data-k="desc"]', "רפידות קדמיות"); await p.fill('#aw-lines input[data-k="price"]', "380");
await p.click("#aw-add"); await p.fill('#aw-lines tr:nth-child(2) input[data-k="desc"]', "עבודה"); await p.fill('#aw-lines tr:nth-child(2) input[data-k="price"]', "150");
console.log("approval total:", await p.textContent("#aw-total"));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/cal-approval.png" });
await p.click("#aw-send"); await p.waitForTimeout(400);
console.log("approval msg open:", await p.$eval("#dlg-msg", e => e.open), "| text:", (await p.inputValue("#msg-text")).slice(0, 140));
await p.click('#dlg-msg button[value="close"]').catch(() => p.keyboard.press("Escape")); await p.waitForTimeout(200);
console.log("block now:", await p.$$eval("#cal .appt", l => l.map(e => e.dataset.st)));
// ready
await p.click("#cal .appt"); await p.waitForTimeout(300);
console.log("approvals row:", (await p.textContent("#ap-approvals")).replace(/\s+/g, " ").slice(0, 120));
if (await p.$("#ap-ready")) { await p.click("#ap-ready"); await p.waitForTimeout(400); console.log("ready msg:", (await p.inputValue("#msg-text")).slice(0, 140)); await p.evaluate(() => document.querySelectorAll("dialog[open]").forEach(d => d.close())); }
else { console.log("no ready button (no phone)"); await p.evaluate(() => document.querySelectorAll("dialog[open]").forEach(d => d.close())); }
await p.waitForTimeout(200);
// new appointment via empty cell, then clash
const cell = await p.$('#cal .cal-cell[data-slot="960"][data-bay="3"]');
await cell.click({ force: true }); await p.waitForTimeout(300);
console.log("new appt prefill:", await p.inputValue("#na-date"), await p.inputValue("#na-time"), "bay", await p.inputValue("#na-bay"));
await p.fill("#na-find", "דני בדיקה"); await p.fill("#na-phone", "0501234567"); await p.fill("#na-plate", "1234567"); await p.click("#na-save"); await p.waitForTimeout(500);
console.log("new appt:", await p.textContent("#toast"), "| blocks:", await p.$$eval("#cal .appt", l => l.length));
await p.click("#cal-new"); await p.fill("#na-time", "16:00"); await p.selectOption("#na-bay", "3");
await p.fill("#na-find", "התנגשות"); await p.click("#na-save"); await p.waitForTimeout(300);
console.log("clash err:", await p.textContent("#na-err"), "hidden:", await p.$eval("#na-err", e => e.hidden));
await p.keyboard.press("Escape"); await p.waitForTimeout(200);
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/cal-day2.png" });
// settings
await p.click("#cal-settings"); await p.waitForTimeout(500);
console.log("settings link:", await p.inputValue("#bk-link"), "on:", await p.isChecked("#bk-on"), "bays:", await p.inputValue("#bk-bays"));
await p.fill("#bk-bays", "4"); await p.click("#bk-save"); await p.waitForTimeout(300);
console.log("bays after:", await p.$$eval("#cal .cal-h", l => l.length - 1));
await p.click("#cal-next"); await p.waitForTimeout(300); console.log("next day:", await p.textContent("#cal-date"), await p.$$eval("#cal .appt", l => l.length));
// ---------- book page demo, phone ----------
const m = await b.newContext({ viewport: { width: 400, height: 860 }, deviceScaleFactor: 2, timezoneId: "Asia/Jerusalem" });
const bp = await m.newPage(); bp.on("pageerror", e => errs.push("book: " + e.message));
await bp.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort());
await bp.goto("http://localhost:8144/book/?demo&name=%D7%9E%D7%A7%D7%A1&phone=0501112222"); await bp.waitForTimeout(800);
console.log("book days:", await bp.$$eval("#b-days .chip", l => l.length), "slots:", await bp.$$eval("#b-slots .chip", l => l.length), "name:", await bp.inputValue("#b-cust"));
await bp.screenshot({ path: (process.env.SHOTS || "/tmp") + "/book-form.png", fullPage: true });
await bp.click("#b-go"); console.log("book no slot err:", await bp.textContent("#b-err"));
await bp.click("#b-days .chip:nth-child(2)"); await bp.click("#b-slots .chip:nth-child(3)"); await bp.click("#b-go"); await bp.waitForTimeout(300);
console.log("book done:", await bp.isVisible("#b-done"), await bp.textContent("#b-when"), "|", await bp.textContent("#b-where"));
await bp.screenshot({ path: (process.env.SHOTS || "/tmp") + "/book-done.png", fullPage: true });
// book page: stubbed real mode
const bp2 = await m.newPage(); bp2.on("pageerror", e => errs.push("book2: " + e.message));
await bp2.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort());
await bp2.addInitScript(() => {
  const h = { open: "08:00", close: "12:00" }; let calls = 0;
  const t = new Date(); t.setDate(t.getDate() + 1); t.setHours(8, 0, 0, 0);
  const stub = { enabled: true, bookingInfo: async () => ({ id: "x", name: "מוסך אמת", city: "חולון", address: "", phone: "035555555", hours: { 0: h, 1: h, 2: h, 3: h, 4: h, 5: h, 6: h }, bays: 1, slot_minutes: 60, enabled: true, busy: [[t.toISOString(), 60]] }),
    bookAppointment: async a => { window.__booked = a; if (++calls === 1) throw new Error("slot taken"); return "id"; } };
  Object.defineProperty(window, "TipulitCloud", { get: () => stub, set: () => {} });
});
await bp2.goto("http://localhost:8144/book/?g=11111111-1111-1111-1111-111111111111"); await bp2.waitForTimeout(800);
const before = await bp2.$$eval("#b-slots .chip", l => l.map(e => e.textContent));
console.log("real slots day1:", before.join(","));
await bp2.fill("#b-cust", "רות"); await bp2.fill("#b-phone", "0521234567"); await bp2.click("#b-days .chip:nth-child(2)"); await bp2.click("#b-slots .chip"); await bp2.click("#b-go"); await bp2.waitForTimeout(300);
console.log("real taken err:", await bp2.textContent("#b-err"), "| slots now:", await bp2.$$eval("#b-slots .chip", l => l.map(e => e.textContent)).then(x => x.join(",")));
await bp2.click("#b-slots .chip"); await bp2.click("#b-go"); await bp2.waitForTimeout(300); console.log("real done:", await bp2.isVisible("#b-done"), JSON.stringify(await bp2.evaluate(() => window.__booked)));
const bp3 = await m.newPage(); await bp3.goto("http://localhost:8144/book/?g=bad"); await bp3.waitForTimeout(500); console.log("bad link:", await bp3.textContent("#b-closed-title"));
// approve page
const ap = await m.newPage(); ap.on("pageerror", e => errs.push("approve: " + e.message));
await ap.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort());
await ap.goto("http://localhost:8144/approve/?demo"); await ap.waitForTimeout(500);
console.log("approve demo:", await ap.textContent("#a-garage"), await ap.textContent("#a-total"), await ap.$$eval("#a-lines tr", l => l.length));
await ap.screenshot({ path: (process.env.SHOTS || "/tmp") + "/approve-view.png", fullPage: true });
await ap.click("#a-yes"); await ap.waitForTimeout(200); console.log("approve result:", (await ap.textContent("#a-result")).slice(0, 40));
await ap.screenshot({ path: (process.env.SHOTS || "/tmp") + "/approve-done.png", fullPage: true });
const ap2 = await m.newPage(); ap2.on("pageerror", e => errs.push("approve2: " + e.message));
await ap2.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort());
await ap2.addInitScript(() => { const stub = { enabled: true, approvalGet: async id => ({ id, garage: "מוסך אמת", garage_phone: "03", car: "i10", message: null, lines: [{ desc: "מצבר", price: 450 }], total: 450, status: "pending" }), approvalDecide: async (id, y) => { window.__dec = [id, y]; return y ? "approved" : "declined"; } }; Object.defineProperty(window, "TipulitCloud", { get: () => stub, set: () => {} }); });
ap2.on("dialog", d => d.accept());
await ap2.goto("http://localhost:8144/approve/?id=22222222-2222-2222-2222-222222222222"); await ap2.waitForTimeout(500);
await ap2.click("#a-no"); await ap2.waitForTimeout(200); console.log("decline:", JSON.stringify(await ap2.evaluate(() => window.__dec)), (await ap2.textContent("#a-result")).slice(0, 30));
const ap3 = await m.newPage(); await ap3.goto("http://localhost:8144/approve/?id=nope"); await ap3.waitForTimeout(400); console.log("missing shown:", await ap3.isVisible("#a-missing"));
console.log("errors:", errs); await b.close(); srv.close();
