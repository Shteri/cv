// End-to-end: driver joins via invite link, garage sees customer, logs a visit, driver approves.
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
// The cloud layer is replaced by an in-memory model that mirrors the SQL functions in migration 0003.
import { chromium } from "playwright";
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const ct = f => f.endsWith(".css") ? "text/css" : f.endsWith(".js") ? "text/javascript" : f.endsWith(".json") ? "application/json" : f.endsWith(".svg") ? "image/svg+xml" : "text/html; charset=utf-8";
const srv = createServer((q, r) => { const f = SITE + (q.url.split("?")[0] === "/" ? "/index.html" : q.url.split("?")[0]); if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", ct(f)); r.end(readFileSync(f)); }).listen(8140);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium", args: ["--ignore-certificate-errors"] });
const GID = "11111111-0000-0000-0000-000000000001";
// shared fake server state lives in node, pages talk to it through exposed functions
const db = { links: [], entries: [], cars: {} };
const mkCtx = async () => { const ctx = await b.newContext({ viewport: { width: 400, height: 860 }, deviceScaleFactor: 2 });
await ctx.exposeFunction("__db", dbfn);
await ctx.addInitScript(initFn, { GID });
return ctx; };
function dbfn(op, arg) {
  if (op === "saveCar") { const id = arg.cloudId || "car-" + Object.keys(db.cars).length; db.cars[id] = { ...arg, cloudId: id, updated_at: new Date().toISOString() }; return id; }
  if (op === "join") { db.links = db.links.filter(l => !(l.garage_id === arg.garageId && l.car_id === arg.carCloudId)); const id = "link-" + db.links.length; db.links.push({ id, garage_id: arg.garageId, car_id: arg.carCloudId, first_name: arg.firstName, phone: arg.phone, allow_contact: arg.allowContact, share_history: !!arg.shareHistory, show_garage_names: false, created_at: new Date().toISOString() }); return id; }
  if (op === "updLink") { const l = db.links.find(x => x.id === arg.id); Object.assign(l, arg.patch); return null; }
  if (op === "myLinks") return db.links.map(l => ({ ...l, garage_profiles: { id: GID, name: "מוסך ליה בע\"מ", city: "חולון", booking_enabled: true } }));
  if (op === "leave") { db.links = db.links.filter(l => l.id !== arg); return null; }
  if (op === "customers") return db.links.filter(l => l.garage_id === arg).map(l => { const c = db.cars[l.car_id]; return { link_id: l.id, first_name: l.first_name, phone: l.allow_contact ? l.phone : null, allow_contact: l.allow_contact, plate: (c.plate || "").replace(/\D/g, ""), schedule_id: c.schedule, year: c.year, km: c.km, km_month: c.kmMonth, last_service: c.lastService, test_expiry: (c.gov || {}).test_expiry || null, car_updated_at: c.updated_at, linked_at: l.created_at, last_visit: null, pending: db.entries.filter(e => e.car_id === l.car_id && e.status === "pending").length }; });
  if (op === "addEntry") { const l = db.links.find(x => x.id === arg.link); const id = "entry-" + db.entries.length; db.entries.push({ id, car_id: l.car_id, garage_id: l.garage_id, status: "pending", created_at: new Date().toISOString(), kind: arg.e.kind, svc_km: arg.e.svcKm, km: arg.e.km, date: arg.e.date, price: arg.e.price, text: arg.e.text, where: arg.e.where }); return id; }
  if (op === "pending") return db.entries.filter(e => e.status === "pending").map(e => ({ ...e, garage_profiles: { name: "מוסך ליה בע\"מ", city: "חולון" } }));
  if (op === "decide") { const e = db.entries.find(x => x.id === arg.id); e.status = arg.accept ? "accepted" : "rejected"; return null; }
}
function initFn({ GID }) {
  const role = localStorage.getItem("__role") || "driver";
  const user = role === "garage" ? { id: "u-g", email: "g@x", user_metadata: { full_name: "יוסי מוסך" } } : { id: "u-d", email: "d@x", user_metadata: { full_name: "דני כהן" } };
  const prof = { id: GID, garage_id: 1731, name: "מוסך ליה בע\"מ", city: "חולון", address: "הפלד 40", phone: "03-7267307", status: "verified", owner_id: "u-g", hours: {}, makes: [], services: ["mech"], prices: [], photos: [] };
  const stub = { enabled: true, authError: null, hasAuthParams: false,
    currentUser: async () => user, onAuth: cb => setTimeout(() => cb(user, "INITIAL_SESSION"), 0), signInWithGoogle: async () => {}, signOut: async () => {}, handleRedirect: async () => ({ handled: false }),
    loadCars: async () => [], saveCar: (() => { const q = new WeakMap(); return c => { const n = (q.get(c) || Promise.resolve()).then(async () => { c.cloudId = await window.__db("saveCar", c); }); q.set(c, n); return n; }; })(), deleteCar: async () => {}, communityPrices: async () => ({}), communityGarages: async () => [], extractReceipt: async () => { throw new Error("no"); },
    myGarageProfiles: async () => role === "garage" ? [prof] : [], garageProfiles: async () => [], saveGarageProfile: async p => p, deleteGarageProfile: async () => {}, photoUrl: p => p,
    startPhoneVerify: async () => {}, confirmPhoneVerify: async () => {}, claimGarage: async () => ({}), pendingGarageClaims: async () => [], setGarageStatus: async () => {},
    garagePublic: async id => id === GID ? prof : null,
    joinGarage: o => window.__db("join", o), myGarageLinks: () => window.__db("myLinks"), updateGarageLink: (id, patch) => window.__db("updLink", { id, patch }), leaveGarage: id => window.__db("leave", id),
    pendingGarageEntries: () => window.__db("pending"), decideGarageEntry: (id, accept) => window.__db("decide", { id, accept }),
    garageCustomers: id => window.__db("customers", id), garageAddEntry: (link, e) => window.__db("addEntry", { link, e }) };
  Object.defineProperty(window, "TipulitCloud", { configurable: true, set() {}, get() { return stub; } });
}
const errs = [];
const page = async () => { const ctx = await mkCtx(); const p = await ctx.newPage(); p.on("pageerror", e => errs.push(e.message)); p.on("console", m => { if (m.type() === "error") console.log("CONSOLE", m.text(), JSON.stringify(m.location())); }); for (const u of ["https://cdn.jsdelivr.net/npm/@supabase/**", "https://fonts.g**"]) await p.route(u, r => r.abort()); return p; };

// 1. driver opens the invite link
const d = await page();
await d.goto("http://localhost:8140/"); await d.evaluate(() => { localStorage.setItem("__role", "driver"); localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "דני כהן", via: "google", email: "d@x", id: "u-d" }, cars: [{ plate: "10-006-32", schedule: "hyundai-i10-2014-2019", year: 2016, km: 74500, kmMonth: 1500, lastService: "2025-11", gov: { test_expiry: "2026-10-25" } }], active: 0 })); });
await d.goto(`http://localhost:8140/?join=${GID}`); await d.waitForTimeout(1200);
console.log("join param stripped from URL:", !(await d.evaluate(() => location.search)).includes("join"));
console.log("dbg:", await d.evaluate(() => [sessionStorage.getItem("tipulit-join"), document.querySelector("#toast").textContent, [...document.querySelectorAll(".screen")].filter(e => !e.hidden).map(e => e.id).join()]), errs);
console.log("consent sheet open:", await d.$eval("#joinsheet", e => e.classList.contains("show")), "|", await d.textContent("#join-name"), "|", await d.inputValue("#join-first"));
await d.screenshot({ path: (process.env.SHOTS || "/tmp") + "/gc-join.png" });
await d.click("#join-go"); await d.waitForTimeout(300);
console.log("phone required when contact on:", await d.$eval("#join-err", e => !e.hidden));
await d.fill("#join-phone", "050-1234567"); await d.click("#join-history"); await d.click("#join-go"); await d.waitForTimeout(500);
console.log("history shared on join:", await d.evaluate(() => window.__db("myLinks").then(l => l[0].share_history)));
console.log("joined:", !(await d.$eval("#joinsheet", e => e.classList.contains("show"))), "toast:", await d.textContent("#toast"));
await d.click('#nav [data-go="me"]'); await d.waitForTimeout(500);
console.log("driver sees shared garage:", (await d.textContent("#me-links")).includes("מוסך ליה"), "|", (await d.textContent("#me-links")).replace(/\s+/g, " ").slice(0, 120));
console.log("book link:", await d.$eval("#me-links a.btn", a => a.getAttribute("href")).catch(() => "none"));
await d.click("[data-lk-names]"); await d.waitForTimeout(300); console.log("names toggled:", await d.evaluate(() => window.__db("myLinks").then(l => l[0].show_garage_names)));

// 2. garage owner opens customers
const g = await page();
await g.goto("http://localhost:8140/"); await g.evaluate(() => { localStorage.setItem("__role", "garage"); localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "יוסי מוסך", via: "google", email: "g@x", id: "u-g" }, cars: [{ plate: "", schedule: "kia-picanto-2017-2025", year: 2020, km: 10000, kmMonth: 1000 }], active: 0 })); });
await g.reload(); await g.waitForTimeout(800);
await g.click('#nav [data-go="me"]'); await g.waitForTimeout(600);
await g.click("[data-gc]"); await g.waitForTimeout(800);
console.log("customers screen:", await g.$$eval(".screen", l => l.filter(e => !e.hidden).map(e => e.id)), "rows:", await g.$$eval("#gc-list .garage", l => l.length));
console.log("row:", (await g.textContent("#gc-list .garage")).replace(/\s+/g, " ").trim().slice(0, 170));
const wa = await g.$eval('#gc-list a[href*="wa.me"]', e => decodeURIComponent(e.getAttribute("href")));
console.log("whatsapp:", wa.slice(0, 200));
console.log("counts:", (await g.textContent("#gc-counts")).replace(/\s+/g, " ").trim());
await g.click('#gc-filter .chip[data-v="test"]'); await g.waitForTimeout(200); console.log("test filter rows:", await g.$$eval("#gc-list .garage", l => l.length), "msg:", decodeURIComponent(await g.$eval('#gc-list a[href*="wa.me"]', e => e.getAttribute("href"))).split("text=")[1].slice(0, 80));
await g.click('#gc-filter .chip[data-v="lapsed"]'); await g.waitForTimeout(200); console.log("lapsed filter rows:", await g.$$eval("#gc-list .garage", l => l.length));
await g.click('#gc-filter .chip[data-v="all"]'); await g.waitForTimeout(200);
await g.screenshot({ path: (process.env.SHOTS || "/tmp") + "/gc-list.png", fullPage: true });
await g.click("#gc-invite"); await g.waitForTimeout(2500);
console.log("invite link:", await g.inputValue("#inv-link"), "qr svg:", await g.$$eval("#inv-qr svg", l => l.length));
await g.screenshot({ path: (process.env.SHOTS || "/tmp") + "/gc-invite.png" });
await g.click("#inv-close"); await g.waitForTimeout(200);
await g.click("#gc-list [data-gx-log]"); await g.waitForTimeout(300);
console.log("entry sheet:", await g.textContent("#gx-who"), "| svc:", await g.$eval("#gx-svc", e => e.selectedOptions[0].textContent), "| km:", await g.inputValue("#gx-km"));
await g.fill("#gx-price", "890"); await g.fill("#gx-text", "הוחלפו גם מגבים"); await g.click("#gx-save"); await g.waitForTimeout(400);
console.log("sent:", await g.textContent("#toast"), "pending tag:", (await g.textContent("#gc-list")).includes("ממתין לאישור"));

// 3. driver approves
await d.click('#nav [data-go="home"]'); await d.reload(); await d.waitForTimeout(1500);
console.log("dbg2:", await d.evaluate(async () => [JSON.parse(localStorage.getItem("tipulit")).cars[0].cloudId, JSON.stringify(await window.__db("pending")).slice(0, 120), [...document.querySelectorAll(".screen")].filter(e => !e.hidden).map(e => e.id).join()]));
console.log("pending card on home:", (await d.textContent("#home-body")).includes("מוסך רשם ביקור"));
await d.screenshot({ path: (process.env.SHOTS || "/tmp") + "/gc-approve.png" });
await d.click("[data-gx-ok]"); await d.waitForTimeout(500);
const car = await d.evaluate(() => JSON.parse(localStorage.getItem("tipulit")).cars[0]);
const h = car.history.find(x => x.source === "garage");
console.log("history added:", !!h, h && { svcKm: h.svcKm, km: h.km, garage: h.garage, price: h.price, items: h.items.length, where: h.where }, "lastService:", car.lastService);
await d.click('#nav [data-go="car"]'); await d.waitForTimeout(400); console.log("verified tag in car history:", await d.$$eval("#car-history .tag.ver", l => l.length)); await d.click('#nav [data-go="home"]'); await d.waitForTimeout(300);
console.log("card gone:", !(await d.textContent("#home-body")).includes("מוסך רשם ביקור"));
// 4. driver revokes
await d.click('#nav [data-go="me"]'); await d.waitForTimeout(400); await d.click("[data-lk-leave]"); await d.click("[data-lk-leave]"); await d.waitForTimeout(400);
console.log("links left after revoke:", await d.evaluate(() => window.__db("myLinks").then(l => l.length)));
console.log("errors:", errs);
await b.close(); srv.close();
