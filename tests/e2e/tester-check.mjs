// A garage profile outside the registry (the owner's hidden test garage) shows in the city list with
// "בדיקה · רק לך", opens its page, and its "קבע תור" leads to the booking page.
import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const srv = createServer((q, r) => { let f = SITE + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8151);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const ctx = await b.newContext({ viewport: { width: 400, height: 860 } });
await ctx.addInitScript(() => {
  const user = { id: "u-t", email: "t@x", user_metadata: { full_name: "מקס" } };
  const tester = { id: "gp-test", garage_id: 900001, name: "Tester · מוסך בדיקה", city: "נתניה", address: "מוסך לבדיקה בלבד, לא קיים", phone: null, booking_enabled: true, hidden: true, services: ["mech"],
    hours: { 0: { open: "08:00", close: "17:00" } }, prices: [{ label: "טיפול קטן", price: 450 }], photos: [], makes: [], about: "מוסך בדיקה פנימי.", status: "verified", aka: [] };
  const stub = { enabled: true, authError: null, hasAuthParams: false, currentUser: async () => user, onAuth: cb => setTimeout(() => cb(user, "INITIAL_SESSION"), 0), signInWithGoogle: async () => {}, signOut: async () => {}, handleRedirect: async () => {},
    loadCars: async () => [], saveCar: async () => {}, deleteCar: async () => {}, communityPrices: async () => null, communityGarages: async () => [],
    myGarageProfiles: async () => [tester], garageProfiles: async city => city === "נתניה" ? [tester] : [], myGarageLinks: async () => [], pendingGarageEntries: async () => [], pendingPlateRequests: async () => [], plateStatus: async () => "mine" };
  Object.defineProperty(window, "TipulitCloud", { configurable: true, set() {}, get() { return stub; } });
});
const p = await ctx.newPage(); const errs = []; p.on("pageerror", e => errs.push(e.message));
const ok = (c, m) => console.log((c ? "OK   " : "FAIL ") + m);
for (const u of ["https://cdn.jsdelivr.net/npm/@supabase/**", "https://fonts.g**", "https://data.gov.il/**"]) await p.route(u, r => r.abort());
await p.goto("http://localhost:8151/");
await p.evaluate(() => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, city: "נתניה", user: { name: "מקס", via: "google", email: "t@x", id: "u-t" }, cars: [{ plate: "65-994-32", schedule: "hyundai-i10-2014-2019", year: 2014, km: 160000, kmMonth: 1500, history: [] }], active: 0 })));
await p.reload(); await p.waitForTimeout(800);
await p.evaluate(() => document.querySelector("#to-garages").click()); await p.waitForTimeout(900);
const row = await p.evaluate(() => { const e = [...document.querySelectorAll("#gr-list .garage")].find(x => x.textContent.includes("Tester")); return e ? e.textContent.replace(/\s+/g, " ") : null; });
console.log("row:", row);
ok(row && /בדיקה · רק לך/.test(row), "the test garage is in the list, marked as a test only you see");
await p.evaluate(() => [...document.querySelectorAll("#gr-list .garage")].find(x => x.textContent.includes("Tester")).click()); await p.waitForTimeout(400);
const book = await p.evaluate(() => { const a = [...document.querySelectorAll("#s-gview a")].find(x => /קביעת תור/.test(x.textContent)); return a ? a.getAttribute("href") : null; });
ok(!(await p.isHidden("#s-gview")) && book && /book\/\?g=gp-test/.test(book), "its page opens with קביעת תור to the booking page: " + book);
console.log("errors:", errs);
await b.close(); srv.close();
