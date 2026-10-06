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
    extractReceipt: async () => { calls++; await new Promise(r => setTimeout(r, 150));
      if (calls === 2) throw new Error("ai 400: Your credit balance is too low to access the Anthropic API");
      return { kind: "service", date: "2025-01", km: 157000, price: 1552, garage: "מוסך התלתן", city: "פתח תקווה", where: "independent", svc_km: null, items: ["engine_oil", "oil_filter", "air_filter", "brake_pads"], text: null, confidence: "high", notes: null }; } };
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
await p.click("#log-save"); await p.waitForTimeout(300);
r = await rows();
ok(await p.$eval("#scan", e => e.classList.contains("show")) && /נשמר/.test(r[0]), "saving returns to the sheet, marked saved");
// retry the failed one: now it reads
await p.click('[data-scan-retry="1"]'); await p.waitForTimeout(600);
r = await rows(); ok(/^(?!.*לא נקרא).*בדוק ושמור/.test(r[1]), "retry reads it");
// a failed document can be filled by hand: closing the form returns to the sheet
await p.click('[data-scan-open="1"]'); await p.waitForTimeout(300);
ok(await p.$eval("#log", e => e.classList.contains("show")), "manual / review opens the form");
await p.click("#log-close"); await p.waitForTimeout(200);
ok(await p.$eval("#scan", e => e.classList.contains("show")), "closing the form goes back to the sheet");
const hist = await p.evaluate(() => JSON.parse(localStorage.getItem("tipulit")).cars[0].history.map(h => `${h.km}:${h.source}:${h.items.join("+")}`));
ok(hist.length === 1 && hist[0].startsWith("157000:upload:"), "one record saved: " + hist.join());
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/scan.png" });
console.log("errors:", errs);
await b.close(); srv.close();
