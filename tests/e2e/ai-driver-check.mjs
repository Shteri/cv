import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const ct = f => f.endsWith(".css") ? "text/css" : f.endsWith(".js") ? "text/javascript" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8";
const srv = createServer((q, r) => { let u = q.url.split("?")[0]; if (u.endsWith("/")) u += "index.html"; const f = SITE + u; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", ct(f)); r.end(readFileSync(f)); }).listen(8151);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const errs = [];
const ctx = await b.newContext({ viewport: { width: 400, height: 860 }, deviceScaleFactor: 2 });
await ctx.addInitScript(() => {
  const user = { id: "u-d", email: "d@x", user_metadata: { full_name: "דני" } };
  const stub = { enabled: true, authError: null, hasAuthParams: false, currentUser: async () => user, onAuth: cb => setTimeout(() => cb(user, "INITIAL_SESSION"), 0), signInWithGoogle: async () => {}, signOut: async () => {}, handleRedirect: async () => ({ handled: false }),
    loadCars: async () => [], saveCar: async () => {}, deleteCar: async () => {}, communityPrices: async () => ({ independent: { med: 900, lo: 800, hi: 1050, n: 12 } }), communityGarages: async () => [], extractReceipt: async () => { throw new Error("no"); },
    myGarageProfiles: async () => [], garageProfiles: async () => [], myGarageLinks: async () => [], pendingGarageEntries: async () => [], plateStatus: async () => "mine",
    aiAssist: async (task, note, context) => { window.__ai = { task, note, context };
      if (task === "record") return { kind: "service", date: "2026-09", km: 61000, price: 950, garage: "יוסי", city: "חולון", where: "independent", svc_km: 60000, items: ["engine_oil", "oil_filter", "wipers", "bogus"], text: null };
      return { lines: [{ desc: "רפידות ודיסקים קדמיים", price: 1800, item: "brake_pads", due: "not_yet", note: "הוחלפו לפני 10,000 ק\"מ" }, { desc: "שמן גיר", price: 450, item: null, due: "not_in_schedule", note: null }], total: 2250, price_verdict: "unknown", summary: "הרפידות הוחלפו לא מזמן לפי מה שרשמת. כדאי לשאול מה מצבן.", questions: ["כמה רפידה נשארה?", "למה צריך שמן גיר עכשיו?"] }; } };
  Object.defineProperty(window, "TipulitCloud", { configurable: true, set() {}, get() { return stub; } });
});
const p = await ctx.newPage(); p.on("pageerror", e => errs.push(e.message));
for (const u of ["https://cdn.jsdelivr.net/npm/@supabase/**", "https://fonts.g**", "https://data.gov.il/**"]) await p.route(u, r => r.abort());
await p.goto("http://localhost:8151/");
await p.evaluate(() => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "דני", via: "google", email: "d@x", id: "u-d" }, cars: [{ plate: "10-006-32", schedule: "hyundai-i10-2014-2019", year: 2016, km: 60500, kmMonth: 1500, lastService: "2025-11", history: [{ id: "h1", kind: "repair", text: "רפידות", items: ["brake_pads"], km: 51000, date: "2025-06", at: 1 }] }], active: 0 })));
await p.reload(); await p.waitForTimeout(1500);
// record from a description
await p.evaluate(() => { const b = [...document.querySelectorAll("button")].find(x => /עשיתי טיפול|רשום טיפול/.test(x.textContent) && x.offsetParent); b && b.click(); });
await p.waitForTimeout(400);
console.log("log open:", await p.$eval("#log", e => e.classList.contains("show")), "| ai row visible:", !(await p.$eval("#log-ai-row", e => e.hidden)));
await p.fill("#log-ai", "טיפול 60 אלף אצל יוסי בחולון, 950 שח, החליפו גם מגבים"); await p.click("#log-ai-go"); await p.waitForTimeout(400);
const ai = await p.evaluate(() => window.__ai);
console.log("sent:", ai.task, "items ctx:", ai.context.items.length, "| filled:", await p.inputValue("#log-km"), await p.inputValue("#log-price"), await p.inputValue("#log-garage"), await p.inputValue("#log-city"), await p.inputValue("#log-svc"), "| chips on:", await p.$$eval("#log-items .on", l => l.map(e => e.textContent).join(",")));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/ai-log.png", fullPage: false });
await p.click("#log-close");
// quote check on the car screen
await p.evaluate(() => { const t = [...document.querySelectorAll("nav button, .tabs button, [data-go]")].find(x => /רכב|מצב/.test(x.textContent)); t && t.click(); });
await p.waitForTimeout(400);
console.log("car screen:", await p.$eval("#s-car", e => !e.hidden), "| quote card:", !(await p.$eval("#car-quote-card", e => e.hidden)));
await p.click("#car-quote"); await p.fill("#quote-text", "רפידות ודיסקים קדמיים 1,800, ושמן גיר 450"); await p.click("#quote-go"); await p.waitForTimeout(500);
const q = await p.evaluate(() => window.__ai);
console.log("quote ctx:", q.task, "| item_state:", q.context.item_state.length, "| brake_pads state:", JSON.stringify(q.context.item_state.find(x => x.item === "brake_pads")), "| prices:", JSON.stringify(q.context.community_prices), "| next:", JSON.stringify(q.context.schedule).slice(0, 120));
console.log("quote out:", (await p.textContent("#quote-out")).replace(/\s+/g, " ").slice(0, 260));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/ai-quote.png", fullPage: true });
console.log("errors:", errs); await b.close(); srv.close();
