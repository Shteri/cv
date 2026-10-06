// The owner's real garage (not the demo) and its booking page share one week and one calendar: hours saved in the
// dashboard are the only times the booking page offers, a customer's booking appears in the garage's calendar and
// its slot is gone from the booking page. The real dashboard has no invented appointments.
import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const srv = createServer((q, r) => { let f = SITE + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8163);
const ok = (c, m) => console.log((c ? "OK   " : "FAIL ") + m);
// one fake server for both pages
const garage = { id: "8014b365-f33c-4e2e-ac7b-95eec2102ffb", garage_id: 900001, name: "Tester · מוסך בדיקה", city: "נתניה", address: "לבדיקה", phone: "050-0000000", status: "verified", hidden: true, booking_enabled: true, bays: 1, slot_minutes: 60, hours: {}, services: ["mech"] };
const appts = [], saves = [];
const DEFAULT = { 0: { open: "08:00", close: "17:00" }, 1: { open: "08:00", close: "17:00" }, 2: { open: "08:00", close: "17:00" }, 3: { open: "08:00", close: "17:00" }, 4: { open: "08:00", close: "17:00" }, 5: { open: "08:00", close: "13:00" }, 6: null };
const server = {
  myGarageProfiles: () => [garage],
  updateGarageSettings: ([id, patch]) => { saves.push(patch); Object.assign(garage, patch); return garage; },
  bookingInfo: () => ({ id: garage.id, name: garage.name, city: garage.city, address: garage.address, phone: garage.phone, hours: Object.keys(garage.hours || {}).length ? garage.hours : DEFAULT, bays: garage.bays, slot_minutes: garage.slot_minutes, enabled: garage.booking_enabled, busy: appts.map(a => [a.starts_at, a.minutes]) }),
  bookSlot: ([a]) => { appts.push({ id: "a" + appts.length, garage_id: garage.id, customer_name: a.name, phone: a.phone, plate: a.plate, kind: a.kind, starts_at: a.startsAt, minutes: garage.slot_minutes, bay: 1, status: "booked", source: "online", token: "t" + appts.length }); return { token: "t" + (appts.length - 1), needs_ok: false }; },
  appointments: ([gid, from, to]) => appts.filter(a => a.starts_at >= from && a.starts_at < to),
};
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, timezoneId: "Asia/Jerusalem" });
await ctx.exposeFunction("__srv", (name, args) => (server[name] ? server[name](args) : []));
await ctx.addInitScript(() => {
  const user = { id: "u-max", email: "m@x", user_metadata: { full_name: "מקס" } };
  const base = { enabled: true, authError: null, hasAuthParams: false, currentUser: async () => user, onAuth: cb => setTimeout(() => cb(user, "INITIAL_SESSION"), 0), handleRedirect: async () => ({}), signOut: async () => {}, why: e => e && e.userMessage || "נסו שוב בעוד רגע." };
  const stub = new Proxy(base, { get: (t, k) => k in t ? t[k] : typeof k === "string" ? (...a) => window.__srv(k, a) : undefined });
  Object.defineProperty(window, "TipulitCloud", { configurable: true, set() {}, get() { return stub; } });
});
await ctx.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort()); await ctx.route("https://fonts.g**", r => r.abort());
const errs = [];
const g = await ctx.newPage(); g.on("pageerror", e => errs.push("garage: " + e.message));
await g.goto("http://localhost:8163/garage/"); await g.waitForTimeout(1500);
ok(await g.isHidden("#demo-note"), "the owner's dashboard is the real garage, not the demo");
await g.click('.tab[data-tab="calendar"]'); await g.waitForTimeout(600);
ok(!(await g.$$(".cal .appt, .cal-appt, [data-appt]")).length, "no invented appointments in the real calendar");
// the week: Tuesday only, 10:00-12:00; a bad row is explained in words
await g.click("#cal-settings"); await g.waitForTimeout(300);
for (let i = 0; i < 7; i++) { const cb = await g.$(`#bk-hours [data-hd="${i}"]`); if ((i === 2) !== (await cb.isChecked())) await cb.click(); }
await g.fill('#bk-hours [data-ho="2"]', "12:00"); await g.fill('#bk-hours [data-hc="2"]', "10:00"); await g.click("#bk-save"); await g.waitForTimeout(300);
ok(/שעת הסגירה/.test(await g.textContent("#bk-err")) && !saves.length, "closing before opening is explained, nothing saved: " + (await g.textContent("#bk-err")));
await g.fill('#bk-hours [data-ho="2"]', "10:00"); await g.fill('#bk-hours [data-hc="2"]', "12:00"); await g.click("#bk-save"); await g.waitForTimeout(400);
ok(saves.length === 1 && saves[0].hours && saves[0].hours[2] && saves[0].hours[2].open === "10:00" && saves[0].hours[0] === null, "the week is saved to the garage profile");
// the customer's booking page offers exactly that week
const c = await ctx.newPage(); c.on("pageerror", e => errs.push("book: " + e.message));
await c.setViewportSize({ width: 400, height: 860 });
await c.goto("http://localhost:8163/book/?g=8014b365-f33c-4e2e-ac7b-95eec2102ffb"); await c.waitForTimeout(800);
const days = await c.$$eval("#b-days .chip, #b-days button", l => l.map(x => x.textContent.replace(/\s+/g, " ").trim()));
ok(days.length > 0 && days.every(d => /ג׳|ג'|שלישי/.test(d)), "the booking page offers only Tuesdays: " + days.slice(0, 3).join(" | "));
await c.click("#b-days .chip, #b-days button"); await c.waitForTimeout(200);
const slots = await c.$$eval("#b-slots .chip", l => l.map(x => x.textContent.trim()));
ok(slots.join(",") === "10:00,10:30,11:00", "and only start times that end by 12:00: " + slots.join(","));
await c.click("#b-slots .chip"); await c.fill("#b-cust", "לקוח בדיקה"); await c.fill("#b-phone", "0501234567"); await c.click("#b-go"); await c.waitForTimeout(500);
ok(appts.length === 1, "the customer booked 10:00");
// the garage sees it; the booking page no longer offers it
await c.goto("http://localhost:8163/book/?g=8014b365-f33c-4e2e-ac7b-95eec2102ffb"); await c.waitForTimeout(800);
await c.click("#b-days .chip, #b-days button"); await c.waitForTimeout(200);
const left = await c.$$eval("#b-slots .chip", l => l.map(x => x.textContent.trim()));
ok(left.join(",") === "11:00", "a second customer sees 10:00-11:00 taken: " + left.join(","));
console.log("errors:", errs);
await b.close(); srv.close();
