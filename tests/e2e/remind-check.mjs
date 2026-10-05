import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
// Reminders and confirmations (migration 0010) in the demo: the garage sends a reminder, the customer confirms on
// /appt/, reschedules through /book/?move=, a repeat no-show's booking waits for the garage, and the policy saves.
const types = { js: "text/javascript", css: "text/css", json: "application/json", svg: "image/svg+xml" };
const srv = createServer((q, r) => { let f = SITE + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", types[f.split(".").pop()] || "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8152);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const ctx = await b.newContext({ viewport: { width: 1300, height: 900 } });
const errs = []; let fail = 0;
const check = (label, ok, got) => { console.log(`${ok ? "OK  " : "FAIL"} ${label}${ok ? "" : " got " + JSON.stringify(got)}`); if (!ok) fail++; };
const g = await ctx.newPage(); g.on("pageerror", e => errs.push("garage: " + e.message)); g.on("dialog", d => d.accept());
await g.goto("http://localhost:8152/garage/?demo"); await g.waitForTimeout(1200);
const focus = async () => { await g.bringToFront(); await g.evaluate(() => window.dispatchEvent(new Event("focus"))); await g.waitForTimeout(300); };
const appt = id => g.evaluate(id => { const a = window.Garage.DEMO.appts.find(x => x.id === id); return a && { status: a.status, confirmed_at: a.confirmed_at, cancelled_by: a.cancelled_by, needs_ok: a.needs_ok, reminded_at: a.reminded_at }; }, id);

// 1. the garage opens tomorrow's reminders and sends one
await g.click('.tab[data-tab="calendar"]'); await g.waitForTimeout(400);
await g.click("#cal-remind"); await g.waitForTimeout(400);
const sum = await g.locator("#rm-sum").innerText();
check("reminders list tomorrow's appointments", /תורים/.test(sum) && await g.locator("#rm-list .approval").count() > 3, sum);
const target = await g.evaluate(() => { const b = document.querySelector('#rm-list [data-rm]'); return b && b.dataset.rm; });
await g.click(`#rm-list [data-rm="${target}"]`); await g.waitForTimeout(300);
const msg = await g.locator("#msg-text").inputValue();
check("reminder message carries the appointment link", /appt\/\?demo&t=/.test(msg) && /תזכורת לתור/.test(msg), msg);
check("reminder marked as sent", !!(await appt(target)).reminded_at, await appt(target));
const link = await g.locator("#msg-note a").getAttribute("href");
await g.evaluate(() => { document.querySelector("#dlg-msg").close(); document.querySelector("#dlg-remind").close(); });

// 2. the customer confirms
const c = await ctx.newPage(); c.on("pageerror", e => errs.push("appt: " + e.message)); c.on("dialog", d => d.accept());
await c.goto(link); await c.waitForTimeout(400);
check("appointment page shows the garage and the time", (await c.locator("#t-garage").innerText()) === "מוסך הדגמה" && (await c.locator("#t-when").innerText()).length > 5);
await c.click("#t-yes"); await c.waitForTimeout(300);
check("customer confirmed", /אישרת הגעה/.test(await c.locator("#t-state").innerText()));
await focus();
check("garage sees the confirmation", !!(await appt(target)).confirmed_at, await appt(target));

// 3. another customer reschedules: new booking first, then the old one is cancelled
const other = await g.evaluate(t => { const a = window.Garage.DEMO.appts.find(x => x.status === "booked" && !x.needs_ok && x.id !== t && Date.parse(x.starts_at) > Date.now() + 86400000 / 2); return { id: a.id, token: a.token }; }, target);
await c.goto("http://localhost:8152/appt/?demo&t=" + other.token); await c.waitForTimeout(400);
await c.click('a[href*="move="]'); await c.waitForTimeout(500);
await c.click("#b-slots .chip"); await c.fill("#b-cust", "לקוח שמזיז"); await c.fill("#b-phone", "0529998877"); await c.click("#b-go"); await c.waitForTimeout(400);
check("rescheduled booking done, old one cancelled", /התור הקודם בוטל/.test(await c.locator("#b-extra").innerText()) && !(await c.locator("#b-manage").isHidden()));
await focus();
check("garage sees the old appointment cancelled by the customer", (await appt(other.id)).cancelled_by === "customer", await appt(other.id));

// 4. a repeat no-show books online: it waits for the garage, which approves it
const nsPhone = await g.evaluate(() => window.Garage.DEMO.appts.find(x => x.id === "dap-ns-0").phone);
await c.goto("http://localhost:8152/book/?demo"); await c.waitForTimeout(400);
await c.click("#b-slots .chip"); await c.fill("#b-cust", "לקוח מבריז"); await c.fill("#b-phone", nsPhone); await c.click("#b-go"); await c.waitForTimeout(400);
check("booking by a phone with two no-shows waits for approval", !(await c.locator("#b-needs").isHidden()));
await focus();
const nsDay = await g.evaluate(() => window.Garage.DEMO.appts.find(x => x.id === "dap-ns-0").starts_at);
await g.evaluate(d => { const p = document.querySelector("#cal-pick"); const x = new Date(d); p.value = `${x.getFullYear()}-${String(x.getMonth() + 1).padStart(2, "0")}-${String(x.getDate()).padStart(2, "0")}`; p.dispatchEvent(new Event("change")); }, nsDay);
await g.waitForTimeout(400);
check("calendar marks the booking that needs approval", /צריך אישור שלך/.test(await g.locator('[data-appt="dap-ns-0"]').innerText()));
await g.click('[data-appt="dap-ns-0"]'); await g.waitForTimeout(400);
check("card shows the no-shows", /2 פעמים/.test(await g.locator("#ap-ok").innerText()), await g.locator("#ap-ok").innerText());
await g.click("#ap-ok-yes"); await g.waitForTimeout(300);
check("garage approved it", (await appt("dap-ns-0")).needs_ok === false, await appt("dap-ns-0"));
await g.evaluate(() => { document.querySelector("#dlg-msg").close(); document.querySelector("#dlg-appt").close(); });

// 5. the policy saves
await g.click("#cal-remind"); await g.waitForTimeout(300);
await g.evaluate(() => { document.querySelector("#dlg-remind details").open = true; });
await g.selectOption("#rm-cancel", "24"); await g.selectOption("#rm-limit", "3"); await g.click("#rm-save"); await g.waitForTimeout(200);
check("policy saved", await g.evaluate(() => window.Garage.st.garage.cancel_hours === 24 && window.Garage.st.garage.noshow_limit === 3));
console.log("errors:", errs);
await b.close(); srv.close();
process.exit(fail ? 1 : 0);
