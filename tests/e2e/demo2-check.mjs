import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const root = SITE;
const srv = createServer((q, r) => { let f = root + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : f.endsWith(".svg") ? "image/svg+xml" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8133);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const ctx = await b.newContext({ viewport: { width: 1300, height: 900 } });
const errs = []; ctx.on("page", p => p.on("pageerror", e => errs.push(p.url().split("/").slice(3).join("/") + ": " + e.message)));
const g = await ctx.newPage(); g.on("pageerror", e => errs.push("garage: " + e.message));
await g.goto("http://localhost:8133/garage/?demo"); await g.waitForTimeout(1500);
const sum = await g.evaluate(() => { const G = window.Garage, st = G.st; const per = st.rows.map(r => st.wos.filter(w => w.garage_car_id === r.car_id).length);
  const lv = k => st.rows.filter(r => r.n && r.n.level === k).length;
  return { rows: st.rows.length, wos: st.wos.length, perCar: per.join(","), repairs: st.wos.filter(w => w.kind === "repair").length, good: lv("good"), warn: lv("warn"), crit: lv("crit"), windows: st.rows.filter(r => r.n && r.n.windowFrom !== r.n.windowTo).length, skips: st.rows.filter(r => r.n && r.n.plan.skip.length).length,
    invoices: st.invoices.length, uninvoiced: st.wos.filter(w => !st.invoices.some(i => i.work_order_id === w.id)).slice(0, 5).map(w => w.date).join(","), appts: G.DEMO.appts.length, stored: !!localStorage.getItem("tipulit-garage-demo") }; });
console.log("garage:", sum);
const sample = await g.evaluate(() => { const st = window.Garage.st, r = st.rows.find(x => st.wos.filter(w => w.garage_car_id === x.car_id).length > 4); return { car: r.model + " " + r.year, km: r.km, hist: st.wos.filter(w => w.garage_car_id === r.car_id).map(w => `${w.date} ${w.kind} ${w.svc_km || ""}@${w.km} [${w.items.join(" ")}] ₪${w.total}`).reverse() }; });
console.log(sample);
// customer approves the pending request
const ap = await g.evaluate(() => window.Garage.DEMO.approvals.find(x => x.status === "pending"));
const c = await ctx.newPage(); await c.goto("http://localhost:8133/approve/?demo&id=" + ap.id); await c.waitForTimeout(500);
console.log("approve page:", (await c.locator("#a-garage").innerText()), "|", await c.locator("#a-car").innerText(), "|", await c.locator("#a-msg").innerText());
await c.click("#a-yes"); await c.waitForTimeout(300);
await g.bringToFront(); await g.evaluate(() => window.dispatchEvent(new Event("focus"))); await g.waitForTimeout(300);
console.log("garage sees:", await g.evaluate(id => window.Garage.DEMO.approvals.find(x => x.id === id).status, ap.id));
// customer books online
const bk = await ctx.newPage(); await bk.goto("http://localhost:8133/book/?demo"); await bk.waitForTimeout(500);
await bk.click("#b-slots .chip"); await bk.fill("#b-cust", "לקוח חדש"); await bk.fill("#b-phone", "0521234567"); await bk.click("#b-go"); await bk.waitForTimeout(300);
console.log("booked:", await bk.locator("#b-when").innerText());
await g.bringToFront(); await g.evaluate(() => window.dispatchEvent(new Event("focus"))); await g.waitForTimeout(300);
console.log("garage online appts:", await g.evaluate(() => window.Garage.DEMO.appts.filter(a => a.id.startsWith("dap-web")).map(a => a.customer_name + " " + a.starts_at)));
// change survives reload
await g.evaluate(() => { window.Garage.st.rows[0].notes = "הערה לבדיקה"; }); await g.waitForTimeout(3300);
await g.reload(); await g.waitForTimeout(1200);
console.log("after reload note:", await g.evaluate(() => window.Garage.st.rows[0].notes), "| approval:", await g.evaluate(id => window.Garage.DEMO.approvals.find(x => x.id === id).status, ap.id));
await g.click('.tab[data-tab="calendar"]').catch(() => {}); await g.waitForTimeout(500); await g.screenshot({ path: (process.env.SHOTS || "/tmp") + "/demo2-cal.png" });
await g.click('.tab[data-tab="customers"]').catch(() => {}); await g.waitForTimeout(300); await g.screenshot({ path: (process.env.SHOTS || "/tmp") + "/demo2-cust.png" });
console.log("errors:", errs);
await b.close(); srv.close();
