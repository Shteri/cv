import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
// Garage names: the name on the sign shows with the registry name under it, and drivers' reports under any of the
// garage's names count for it. Plates: a plate the registry does not know is reported, never guessed.
const types = { js: "text/javascript", css: "text/css", json: "application/json", svg: "image/svg+xml" };
const srv = createServer((q, r) => { let f = SITE + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", types[f.split(".").pop()] || "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8158);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const errs = []; let fail = 0;
const check = (label, ok, got) => { console.log(`${ok ? "OK  " : "FAIL"} ${label}${ok ? "" : " got " + JSON.stringify(got)}`); if (!ok) fail++; };
async function page(profiles) {
  const p = await b.newPage({ viewport: { width: 400, height: 860 } });
  p.on("pageerror", e => errs.push(e.message));
  for (const u of ["https://cdn.jsdelivr.net/**", "https://fonts.googleapis.com/**", "https://fonts.gstatic.com/**"]) await p.route(u, r => r.abort());
  await p.addInitScript(profs => {
    const user = { id: "u1", email: "max@gmail.com", user_metadata: { full_name: "מקס" } };
    const stub = { enabled: true, authError: null, hasAuthParams: false, currentUser: async () => user, onAuth: cb => setTimeout(() => cb(user, "SIGNED_IN"), 0), signInWithGoogle: async () => {}, signOut: async () => {}, handleRedirect: async () => ({ handled: false }),
      loadCars: async () => [], saveCar: async () => {}, deleteCar: async () => {}, communityPrices: async () => ({}), communityGarages: async () => [], myGarageProfiles: async () => [], garageProfiles: async city => profs.filter(x => x.city === city), myGarageLinks: async () => [], pendingGarageEntries: async () => [] };
    Object.defineProperty(window, "TipulitCloud", { configurable: true, set() {}, get() { return stub; } });
  }, profiles);
  return p;
}

// 1. plates
const p1 = await page([]);
let mode = "empty";
await p1.route("https://data.gov.il/**", r => mode === "down" ? r.abort() : r.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ success: true, result: { records: [] } }) }));
await p1.goto("http://localhost:8158/"); await p1.waitForTimeout(300);
await p1.evaluate(() => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "guest" }, cars: [], active: 0 })));
await p1.reload(); await p1.waitForTimeout(600);
await p1.fill("#plate", "1234567"); await p1.click("#plate-go"); await p1.waitForTimeout(600);
check("unknown plate: says it was not found", !(await p1.locator("#plate-miss").isHidden()) && /לא נמצא במאגר/.test(await p1.locator("#plate-miss-text").innerText()), await p1.locator("#plate-miss-text").innerText());
check("unknown plate: no car is guessed", await p1.locator("#add-step-confirm").isHidden() && await p1.locator("#add-step-plate").isVisible());
mode = "down"; await p1.click("#plate-go"); await p1.waitForTimeout(600);
check("registry down: says so", /לא הצלחנו להגיע/.test(await p1.locator("#plate-miss-text").innerText()), await p1.locator("#plate-miss-text").innerText());
await p1.fill("#plate", "12345678"); check("typing hides the message", await p1.locator("#plate-miss").isHidden());

// 2. garage names (registry garage 4581 in Holon, known on its sign as "מוסך הכוכב")
const prof = { id: "gp1", garage_id: 4581, name: "מוסך הכוכב", aka: ["המוסך של איסמעיל"], city: "חולון", address: "המנור 9", phone: "03-5550000", status: "verified", hours: {}, makes: [], services: [], prices: [], photos: [] };
const p2 = await page([prof]);
await p2.route("https://data.gov.il/**", r => r.abort());
await p2.goto("http://localhost:8158/"); await p2.waitForTimeout(300);
const hist = [{ id: "h1", kind: "service", svcKm: 60000, km: 60200, date: "2025-05", items: ["engine_oil"], where: "independent", garage: "המוסך של איסמעיל", city: "חולון", price: 700, back: "yes", receipts: [] }];
await p2.evaluate(h => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "guest" }, city: "חולון", cars: [{ plate: "12-345-67", schedule: "kia-picanto-2017-2025", year: 2020, km: 65000, kmMonth: 1500, history: h }], active: 0 })), hist);
await p2.reload(); await p2.waitForTimeout(800);
await p2.click("#to-garages"); await p2.waitForTimeout(800);
const rows = await p2.$$eval("#gr-list .garage", l => l.map(e => e.innerText.replace(/\s+/g, " ")));
const star = rows.find(t => t.includes("מוסך הכוכב")) || "";
check("the sign's name shows, the registry name under it", /רשום במשרד התחבורה: אבו רמדאן איסמעיל מוסך/.test(star), star);
check("a report under another name counts for the garage", /דיווחת/.test(star) && /ביקרת כאן/.test(star) && !/מומלץ/.test(star), star);
check("no separate row for the other name", !rows.some(t => t.startsWith("המוסך של איסמעיל")), rows.slice(0, 3));
await p2.fill("#gr-q", "כוכב"); await p2.waitForTimeout(300);
check("search finds the sign's name", (await p2.$$eval("#gr-list .garage", l => l.length)) === 1 && /מוסך הכוכב/.test(await p2.locator("#gr-list").innerText()));
await p2.fill("#gr-q", "רמדאן"); await p2.waitForTimeout(300);
check("search finds the registry name", /מוסך הכוכב/.test(await p2.locator("#gr-list").innerText()));
console.log("errors:", errs);
await b.close(); srv.close();
process.exit(fail ? 1 : 0);
