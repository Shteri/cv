// Privacy: the policy and terms pages exist and are linked from sign-in and from "אני"; "הורד את המידע שלי"
// downloads the driver's data; deleting the account calls the server, then clears this device.
import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const srv = createServer((q, r) => { let f = SITE + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8148);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const ctx = await b.newContext({ viewport: { width: 400, height: 860 }, acceptDownloads: true });
await ctx.addInitScript(() => {
  const user = { id: "u-p", email: "p@x", user_metadata: { full_name: "מקס" } };
  window.__deleted = false;
  const stub = { enabled: true, authError: null, hasAuthParams: false, currentUser: async () => user, onAuth: cb => setTimeout(() => cb(user, "INITIAL_SESSION"), 0), signInWithGoogle: async () => {}, signOut: async () => {}, handleRedirect: async () => {},
    loadCars: async () => [], saveCar: async () => {}, deleteCar: async () => {}, deleteRecord: async () => {}, communityPrices: async () => null, communityGarages: async () => [],
    myGarageProfiles: async () => [{ id: "g1", name: "מוסך בדיקה", city: "נתניה", status: "verified" }], garageProfiles: async () => [], myGarageLinks: async () => [], pendingGarageEntries: async () => [], pendingPlateRequests: async () => [], plateStatus: async () => "mine",
    deleteAccount: async () => { window.__deleted = true; return { ok: true }; } };
  Object.defineProperty(window, "TipulitCloud", { configurable: true, set() {}, get() { return stub; } });
});
const p = await ctx.newPage(); const errs = []; p.on("pageerror", e => errs.push(e.message + " @ " + (e.stack || "").split("\n").slice(1, 3).join(" ")));
const dialogs = []; p.on("dialog", d => { dialogs.push(d.message()); d.accept(); });
const ok = (c, m) => console.log((c ? "OK   " : "FAIL ") + m);
for (const u of ["https://cdn.jsdelivr.net/npm/@supabase/**", "https://fonts.g**", "https://data.gov.il/**"]) await p.route(u, r => r.abort());
// the pages
for (const [path, h] of [["privacy/", "מדיניות פרטיות"], ["terms/", "תנאי שימוש"]]) { await p.goto("http://localhost:8148/" + path); ok((await p.textContent("h1")) === h, path + " page"); }
ok(/תיקון 13/.test(await (await p.goto("http://localhost:8148/privacy/"), p.textContent("main"))) && /אין עליך חובה לפי חוק/.test(await p.textContent("main")), "the policy names the law and the duty to provide data");
await p.goto("http://localhost:8148/");
await p.evaluate(() => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "google", email: "p@x", id: "u-p" }, cars: [{ plate: "65-994-32", schedule: "hyundai-i10-2014-2019", year: 2014, km: 160000, kmMonth: 1500, history: [{ id: "r1", kind: "service", km: 150000, date: "2024-06", items: ["engine_oil"], receipts: ["data:image/jpeg;base64,AAAA"], share: false }] }], active: 0 })));
await p.reload(); await p.waitForTimeout(600);
await p.click('#nav button[data-go="me"]'); await p.waitForTimeout(300);
ok(await p.isVisible('#s-me a[href="privacy/"]') && await p.isVisible("#me-export") && await p.isVisible("#me-delete"), "the privacy card in 'אני'");
const [dl] = await Promise.all([p.waitForEvent("download"), p.click("#me-export")]);
const data = JSON.parse(readFileSync(await dl.path(), "utf8"));
ok(data.cars[0].plate === "65-994-32" && data.cars[0].records[0].km === 150000 && !("receipts" in data.cars[0].records[0]) && data.user.email === "p@x", "the download holds the driver's data (without image data)");
await p.click("#me-delete"); await p.waitForTimeout(500);
ok(dialogs.some(m => /מוסך בדיקה/.test(m)) && dialogs.some(m => /אי אפשר לשחזר/.test(m)), "the warning names the garage that goes too");
ok(await p.evaluate(() => window.__deleted), "the server deletes the account");
ok(await p.evaluate(() => !localStorage.getItem("tipulit") || JSON.parse(localStorage.getItem("tipulit")).cars.length === 0) && !(await p.isHidden("#s-onb")), "this device is cleared, back to the start");
console.log("errors:", errs);
await b.close(); srv.close();
