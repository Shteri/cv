import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const srv = createServer((q, r) => { const f = SITE + (q.url === "/" ? "/index.html" : q.url.split("?")[0]); if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".css") ? "text/css" : f.endsWith(".svg") ? "image/svg+xml" : f.endsWith(".png") ? "image/png" : f.endsWith(".js") ? "text/javascript" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8134);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await b.newPage({ viewport: { width: 400, height: 860 }, deviceScaleFactor: 2 });
const errs = []; p.on("pageerror", e => { errs.push(e.message); console.log("PE", e.message, (e.stack || "").split("\n")[1]); }); p.on("console", m => { if (m.type() === "error" && !/ERR_|net::/.test(m.text())) errs.push(m.text()); });
for (const u of ["https://data.gov.il/**", "https://cdn.jsdelivr.net/**", "https://fonts.googleapis.com/**", "https://fonts.gstatic.com/**"]) await p.route(u, r => r.abort());
// Stub the cloud layer: intercept the assignment cloud.js makes to window.TipulitCloud.
await p.addInitScript(() => {
  const user = { id: "u1", email: "max@gmail.com", user_metadata: { full_name: "מקס" } };
  const db = { profiles: [] };
  const stub = { enabled: true, authError: null, hasAuthParams: false,
    currentUser: async () => user, onAuth: cb => setTimeout(() => cb(user, "SIGNED_IN"), 0), signInWithGoogle: async () => {}, signOut: async () => {}, handleRedirect: async () => ({ handled: false }),
    loadCars: async () => [], saveCar: async () => {}, deleteCar: async () => {}, communityPrices: async () => ({}), communityGarages: async () => [], extractReceipt: async () => { throw new Error("no"); },
    myGarageProfiles: async () => db.profiles, garageProfiles: async city => db.profiles.filter(x => x.city === city && x.status === "verified"),
    saveGarageProfile: async p => { const row = { ...p, id: p.id || "gp1", status: p.id ? p.status : "pending", photos: (p.photos || []).map((x, i) => x.startsWith("data:") ? "u1/photo" + i + ".jpg" : x) }; db.profiles = db.profiles.filter(x => x.id !== row.id).concat(row); return row; },
    deleteGarageProfile: async id => { db.profiles = db.profiles.filter(x => x.id !== id); }, photoUrl: p => p.startsWith("data:") ? p : "https://x/" + p,
    startPhoneVerify: async () => { throw new Error("SMS provider not configured"); }, confirmPhoneVerify: async () => {}, claimGarage: async () => ({ verified: true }),
    pendingGarageClaims: async () => db.profiles.filter(x => x.status === "pending").map(x => ({ ...x, registry_phone: x.registry_phone, owner_email: "max@gmail.com" })),
    setGarageStatus: async (id, st) => { const x = db.profiles.find(x => x.id === id); if (x) x.status = st; } };
  window.__db = db;
  Object.defineProperty(window, "TipulitCloud", { configurable: true, set() {}, get() { return stub; } });
});
await p.goto("http://localhost:8134/"); await p.waitForTimeout(300);
await p.evaluate(() => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "google", email: "max@gmail.com", id: "u1" }, city: "חולון", cars: [{ plate: "12-345-67", schedule: "kia-picanto-2017-2025", year: 2020, km: 43800, kmMonth: 1500 }], active: 0 })));
await p.reload(); await p.waitForTimeout(700);
await p.waitForTimeout(1000); console.log("screen0:", await p.$$eval(".screen", l => l.filter(e => !e.hidden).map(e => e.id)), "hash:", await p.evaluate(() => location.hash)); await p.click("#to-garages"); await p.waitForTimeout(500); console.log("screen1:", await p.$$eval(".screen", l => l.filter(e => !e.hidden).map(e => e.id)));
// drivers' list has no "is this my garage" any more; owners register from the profile screen
const claimLinks = await p.$$eval("#gr-list [data-claim]", l => l.length);
console.log(claimLinks === 0 ? "OK   no claim link in the drivers' list" : "FAIL claim link still in the drivers' list");
await p.click('#nav [data-go="me"]'); await p.waitForTimeout(500);
await p.click("#me-garage-find"); await p.waitForTimeout(400);
console.log(!(await p.$eval("#s-gclaim", e => e.hidden)) ? "OK   owners' registration screen opens" : "FAIL registration screen did not open");
await p.fill("#gcl-q", "אשכנזי"); await p.waitForTimeout(200);
await p.click("#gcl-list [data-gcl]"); await p.waitForTimeout(300);
console.log("edit screen:", !(await p.$eval("#s-gedit", e => e.hidden)), "name:", await p.textContent("#ge-name"), "phone:", await p.inputValue("#ge-phone"));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/gp-edit.png", fullPage: true });
await p.fill("#ge-wa", "050-1234567");
await p.click('#ge-hours .toggle[data-day="6"]'); await p.waitForTimeout(100); // open Saturday
await p.click('#ge-makes .chip[data-m="קיה"]'); 
await p.fill('#ge-prices input[data-i="0"][data-k="price"]', "450"); await p.fill('#ge-prices input[data-i="1"][data-k="price"]', "890");
await p.fill("#ge-about", "מוסך משפחתי מ-1990");
await p.click("#ge-save"); await p.waitForTimeout(400);
const saved = await p.evaluate(() => window.__db.profiles[0]);
console.log("saved:", saved && { status: saved.status, wa: saved.whatsapp, makes: saved.makes, prices: saved.prices, sat: saved.hours[6], reg: saved.registry_phone });
console.log("status card:", (await p.textContent("#ge-status")).replace(/\s+/g, " ").slice(0, 80));
await p.click("#ge-send"); await p.waitForTimeout(300);
console.log("sms fallback:", (await p.textContent("#ge-verify")).includes("ידנית"));
// admin approves via profile screen
await p.click("#ge-back"); await p.waitForTimeout(300);
await p.click('#nav [data-go="me"]'); await p.waitForTimeout(500);
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/gp-me.png", fullPage: true });
console.log("me lists garage:", (await p.textContent("#me-garages")).includes("אשכנזי"), "pending claims shown:", await p.$$eval("[data-ok]", l => l.length));
await p.click("[data-ok]"); await p.waitForTimeout(400);
console.log("after approve:", (await p.textContent("#me-garages")).includes("מאומת"));
// finder now shows verified profile with hours/whatsapp/details
await p.click('#nav [data-go="home"]'); await p.waitForTimeout(400); await p.click("#to-garages"); await p.waitForTimeout(500);
await p.fill("#gr-q", "אשכנזי"); await p.waitForTimeout(200);
const row = await p.$eval("#gr-list .garage", e => ({ ver: e.textContent.includes("מאומת"), hrs: e.querySelector(".hrs")?.textContent, wa: !!e.querySelector('a[href*="wa.me"]') }));
console.log("row:", row);
// tapping the garage opens everything the owner filled in
await p.click("#gr-list .garage .nm"); await p.waitForTimeout(400);
const gv = (await p.textContent("#gv-body")).replace(/\s+/g, " ");
console.log(!(await p.$eval("#s-gview", e => e.hidden)) && /מחירון/.test(gv) && /450/.test(gv) && /מוסך משפחתי/.test(gv) && /שעות פתיחה/.test(gv) && /קיה/.test(gv) ? "OK   garage page shows price list, about, hours and makes" : "FAIL garage page incomplete: " + gv.slice(0, 200));
console.log(await p.$("#gv-edit") ? "OK   the owner sees edit on their garage's page" : "FAIL no edit for the owner");
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/gp-view.png", fullPage: true });
await p.click("#gv-back"); await p.waitForTimeout(300);
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/gp-row.png" });
await p.fill("#gr-q", ""); await p.waitForTimeout(200);
console.log("verified first (after none recommended):", (await p.$eval("#gr-list .garage", e => e.textContent)).includes("אשכנזי"));
console.log("errors:", errs);
await b.close(); srv.close();
