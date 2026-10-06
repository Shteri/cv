// Uploading receipts opens the reading sheet: each document is read in turn; a read one opens the form filled
// for review, a failed one says why and offers "מלא ידנית" or "נסה שוב". Saving returns to the sheet.
import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const srv = createServer((q, r) => { let f = SITE + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8144);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const ctx = await b.newContext({ viewport: { width: 400, height: 860 } });
await ctx.addInitScript(() => {
  const user = { id: "u-s", email: "s@x", user_metadata: { full_name: "מקס" } };
  let calls = 0;
  const stub = { enabled: true, authError: null, hasAuthParams: false, currentUser: async () => user, onAuth: cb => setTimeout(() => cb(user, "INITIAL_SESSION"), 0), signInWithGoogle: async () => {}, signOut: async () => {}, handleRedirect: async () => {},
    loadCars: async () => [], saveCar: async () => {}, deleteCar: async () => {}, communityPrices: async () => null, communityGarages: async () => [],
    myGarageProfiles: async () => [], garageProfiles: async () => [], myGarageLinks: async () => [], pendingGarageEntries: async () => [], pendingPlateRequests: async () => [], plateStatus: async () => "mine",
    // the first document reads, the second fails the first time (no AI credit) and reads on retry
    extractReceipt: async () => { calls++; window.__calls = calls; await new Promise(r => setTimeout(r, 150));
      if (calls === 2) throw new Error("ai 400: Your credit balance is too low to access the Anthropic API");
      // the retry: a receipt with no km printed
      if (calls === 3) return { kind: "repair", date: "2026-08", km: null, price: 2800, garage: "מוסך התלתן", city: "פתח תקווה", where: "independent", svc_km: null, items: ["engine_oil", "ac_refrigerant"], text: "החלפת צינור מזגן", confidence: "high", notes: null };
      return { kind: "service", date: "2025-01", km: 157000, price: 1552, garage: "מוסך התלתן", city: "פתח תקווה", where: "independent", svc_km: null, items: ["engine_oil", "oil_filter", "air_filter", "brake_pads"], text: "החלפת רפידות אחוריות", confidence: "high", notes: null }; } };
  Object.defineProperty(window, "TipulitCloud", { configurable: true, set() {}, get() { return stub; } });
});
const p = await ctx.newPage(); const errs = []; p.on("pageerror", e => errs.push(e.message));
const ok = (c, m) => console.log((c ? "OK   " : "FAIL ") + m);
for (const u of ["https://cdn.jsdelivr.net/npm/@supabase/**", "https://fonts.g**", "https://data.gov.il/**"]) await p.route(u, r => r.abort());
await p.goto("http://localhost:8144/");
await p.evaluate(() => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "google", email: "s@x", id: "u-s" }, cars: [{ plate: "65-994-32", schedule: "hyundai-i10-2014-2019", year: 2014, km: 160000, kmMonth: 1500, lastService: "2024-06", history: [] }], active: 0 })));
await p.reload(); await p.waitForTimeout(800);
await p.click('#nav button[data-go="car"]'); await p.waitForTimeout(300);
ok(await p.locator("#car-manual").isVisible(), "car screen has a separate manual button");
// a tiny PNG and a PDF stand in for receipts
const png = Buffer.from("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=", "base64");
await p.setInputFiles("#car-upload", [{ name: "r1.png", mimeType: "image/png", buffer: png }, { name: "r2.pdf", mimeType: "application/pdf", buffer: Buffer.from("%PDF-1.4\n%%EOF") }]);
await p.waitForTimeout(100);
ok(await p.$eval("#scan", e => e.classList.contains("show")) && !(await p.$eval("#log", e => e.classList.contains("show"))), "upload opens the reading sheet, not the form");
await p.waitForTimeout(800);
const rows = () => p.$$eval("#scan-list .scan-row", l => l.map(e => e.textContent.replace(/\s+/g, " ").trim()));
let r = await rows(); console.log("rows:", r);
ok(/נקרא/.test(r[0]) && /בדוק ושמור/.test(r[0]) && /157,000/.test(r[0]), "first: read, with what was read");
ok(/לא נקרא/.test(r[1]) && /אין קרדיט/.test(r[1]) && /מלא ידנית/.test(r[1]) && /נסה שוב/.test(r[1]), "second: says why, offers manual and retry");
// review the read one: the form opens filled, saving goes back to the sheet
await p.click('[data-scan-open="0"]'); await p.waitForTimeout(300);
ok(await p.inputValue("#log-km") === "157000" && await p.inputValue("#log-garage") === "מוסך התלתן", "the form opens filled from the receipt");
ok(await p.isVisible("#log-text") && await p.inputValue("#log-text") === "החלפת רפידות אחוריות", "a service with a repair: the repair shows in the same record");
await p.click("#log-save"); await p.waitForTimeout(300);
r = await rows();
ok(await p.$eval("#scan", e => e.classList.contains("show")) && /נשמר/.test(r[0]), "saving returns to the sheet, marked saved");
// retry the failed one: now it reads
await p.click('[data-scan-retry="1"]'); await p.waitForTimeout(600);
r = await rows(); ok(/^(?!.*לא נקרא).*בדוק ושמור/.test(r[1]), "retry reads it");
// a failed document can be filled by hand: closing the form returns to the sheet
await p.click('[data-scan-open="1"]'); await p.waitForTimeout(300);
ok(await p.$eval("#log", e => e.classList.contains("show")), "manual / review opens the form");
const estKm = await p.inputValue("#log-km"); console.log("estimated km:", estKm, "|", await p.textContent("#log-km-est"));
ok(estKm && +estKm < 160000 && +estKm > 157000 && await p.isVisible("#log-km-est"), "no km on the receipt: estimated for its month, not today's odometer, and said so");
await p.click("#log-close"); await p.waitForTimeout(200);
ok(await p.$eval("#scan", e => e.classList.contains("show")), "closing the form goes back to the sheet");
const hist = await p.evaluate(() => JSON.parse(localStorage.getItem("tipulit")).cars[0].history.map(h => `${h.km}:${h.source}:${h.items.join("+")}`));
ok(hist.length === 1 && hist[0].startsWith("157000:upload:"), "one record saved: " + hist.join());
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/scan.png" });
// the same file again: recognised without reading it (no AI call)
const callsBefore = await p.evaluate(() => window.__calls || 0);
await p.setInputFiles("#car-upload", [{ name: "r1-again.png", mimeType: "image/png", buffer: png }]); await p.waitForTimeout(500);
r = await rows(); console.log("rows after re-upload:", r);
ok(/כבר קיים/.test(r[r.length - 1]) && /דלג/.test(r[r.length - 1]) && /שמור בכל זאת/.test(r[r.length - 1]), "same file again: 'already here', skip or save anyway");
ok(await p.evaluate(() => window.__calls || 0) === callsBefore, "it was not read again");
await p.click(`[data-scan-skip="${r.length - 1}"]`); await p.waitForTimeout(150);
ok(/דולג/.test((await rows()).slice(-1)[0]), "skip marks it");
// another photo of a receipt that is already saved (same month and total): read, then flagged
await p.setInputFiles("#car-upload", [{ name: "r1-photo2.png", mimeType: "image/png", buffer: Buffer.concat([png, Buffer.from([0])]) }]); await p.waitForTimeout(600);
r = await rows(); ok(/כבר קיים/.test(r.slice(-1)[0]) && /ינואר 2025/.test(r.slice(-1)[0]), "another photo of a saved receipt is flagged: " + r.slice(-1)[0]);
// a saved record opens for editing: fix the km, then delete it
await p.click("#scan-close"); await p.waitForTimeout(200);
await p.evaluate(() => document.querySelector("#car-history [data-rec]").click()); await p.waitForTimeout(300);
ok(await p.inputValue("#log-km") === "157000" && await p.isVisible("#log-del"), "tapping a record opens it with its values and a delete button");
await p.fill("#log-km", "156500"); await p.click("#log-save"); await p.waitForTimeout(300);
let h2 = await p.evaluate(() => JSON.parse(localStorage.getItem("tipulit")).cars[0].history.map(h => `${h.km}:${h.garage}`));
ok(h2.length === 1 && h2[0] === "156500:מוסך התלתן", "editing updates the record in place: " + h2.join());
ok(/טיפול .* \+ החלפת רפידות אחוריות/.test(await p.textContent("#car-history")), "the list says service + repair");
await p.evaluate(() => document.querySelector("#car-history [data-rec]").click()); await p.waitForTimeout(300);
p.once("dialog", d => d.accept()); await p.click("#log-del"); await p.waitForTimeout(300);
h2 = await p.evaluate(() => JSON.parse(localStorage.getItem("tipulit")).cars[0].history.length);
ok(h2 === 0, "delete removes it");
console.log("errors:", errs);
await b.close(); srv.close();
