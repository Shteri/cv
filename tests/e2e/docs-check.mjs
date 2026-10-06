// Receipts keep a readable copy: a photo at 1600px (not the 320px thumbnail) and a PDF as it is, on the device
// (IndexedDB) and, signed in, uploaded to the receipts bucket. A tile in "המסמכים שלך" opens the file.
import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const srv = createServer((q, r) => { let f = SITE + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8147);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const ctx = await b.newContext({ viewport: { width: 400, height: 860 } });
await ctx.addInitScript(() => {
  const user = { id: "u-d", email: "d@x", user_metadata: { full_name: "מקס" } };
  window.__uploads = [];
  const stub = { enabled: true, authError: null, hasAuthParams: false, currentUser: async () => user, onAuth: cb => setTimeout(() => cb(user, "INITIAL_SESSION"), 0), signInWithGoogle: async () => {}, signOut: async () => {}, handleRedirect: async () => {},
    loadCars: async () => [], deleteCar: async () => {}, deleteRecord: async () => {}, communityPrices: async () => null, communityGarages: async () => [],
    myGarageProfiles: async () => [], garageProfiles: async () => [], myGarageLinks: async () => [], pendingGarageEntries: async () => [], pendingPlateRequests: async () => [], plateStatus: async () => "mine",
    // like cloud.js: each file kept on the device goes up with its type
    saveCar: async car => { for (const r of car.history || []) for (const d of r.docs || []) if (!d.path) { const blob = await window.TipulitDocs.get(d.id); if (blob) { window.__uploads.push({ type: d.type, size: blob.size }); d.path = `u/${d.id}.${d.type === "application/pdf" ? "pdf" : "jpg"}`; } } car.cloudId = car.cloudId || "c1"; },
    docUrl: async path => "about:blank#" + path,
    extractReceipt: async () => ({ kind: "service", date: "2025-01", km: 157000, price: 1552, garage: "מוסך התלתן", city: "פתח תקווה", where: "independent", svc_km: null, items: ["engine_oil"], text: null, confidence: "high", notes: null }) };
  Object.defineProperty(window, "TipulitCloud", { configurable: true, set() {}, get() { return stub; } });
});
const p = await ctx.newPage(); const errs = []; p.on("pageerror", e => errs.push(e.message));
const ok = (c, m) => console.log((c ? "OK   " : "FAIL ") + m);
for (const u of ["https://cdn.jsdelivr.net/npm/@supabase/**", "https://fonts.g**", "https://data.gov.il/**"]) await p.route(u, r => r.abort());
await p.goto("http://localhost:8147/");
await p.evaluate(() => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "google", email: "d@x", id: "u-d" }, cars: [{ plate: "65-994-32", schedule: "hyundai-i10-2014-2019", year: 2014, km: 160000, kmMonth: 1500, lastService: "2024-06", history: [] }], active: 0 })));
await p.reload(); await p.waitForTimeout(800);
await p.click('#nav button[data-go="car"]'); await p.waitForTimeout(300);
// a 2000x2600 photo (made in the page) and a small PDF
const photo = await p.evaluate(async () => { const c = document.createElement("canvas"); c.width = 2000; c.height = 2600; const x = c.getContext("2d"); x.fillStyle = "#fff"; x.fillRect(0, 0, 2000, 2600); x.fillStyle = "#000"; x.font = "60px sans-serif"; for (let i = 0; i < 40; i++) x.fillText("שורה בקבלה " + i, 100, 80 + i * 60); return c.toDataURL("image/jpeg", .9).split(",")[1]; });
await p.setInputFiles("#car-upload", [{ name: "r.jpg", mimeType: "image/jpeg", buffer: Buffer.from(photo, "base64") }, { name: "r.pdf", mimeType: "application/pdf", buffer: Buffer.from("%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF") }]);
await p.waitForTimeout(1200);
for (const i of [0, 1]) { await p.click(`[data-scan-open="${i}"]`); await p.waitForTimeout(300); await p.click("#log-save"); await p.waitForTimeout(1500); if (i === 0) { const sheet = await p.$eval("#scan", e => e.classList.contains("show")); if (!sheet) break; } }
const car = await p.evaluate(() => JSON.parse(localStorage.getItem("tipulit")).cars[0]);
const docs = car.history.flatMap(h => h.docs || []);
ok(docs.length === 2 && docs.some(d => d.type === "image/jpeg") && docs.some(d => d.type === "application/pdf"), "both files kept with their records: " + docs.map(d => d.type).join());
const sizes = await p.evaluate(async ids => Promise.all(ids.map(async id => { const bl = await window.TipulitDocs.get(id); if (!bl) return null; if (!bl.type.startsWith("image")) return { size: bl.size }; const bm = await createImageBitmap(bl); return { w: bm.width, h: bm.height }; })), docs.map(d => d.id));
console.log("kept:", JSON.stringify(sizes));
ok(sizes.some(x => x && x.h === 1600), "the photo is kept at 1600px, readable");
ok(sizes.some(x => x && x.size > 20 && !x.h), "the PDF is kept as it is");
await p.waitForTimeout(1200);
const up = await p.evaluate(() => window.__uploads);
ok(up.length === 2 && up.some(u => u.type === "application/pdf"), "signed in: both files go up to the cloud: " + JSON.stringify(up));
await p.click("#scan-close").catch(() => {}); await p.waitForTimeout(200);
const tiles = await p.$$eval("#car-docs [data-doc]", l => l.map(e => e.textContent.trim()));
ok(tiles.length === 2 && tiles.some(t => /PDF/.test(t)), "documents strip shows both, the PDF as a PDF tile: " + tiles.join(" | "));
const [popup] = await Promise.all([p.waitForEvent("popup"), p.click('#car-docs [data-doc="0"]')]);
await p.waitForTimeout(300);
ok(/about:blank#u\//.test(popup.url()) || /^blob:/.test(popup.url()), "tapping a tile opens the file: " + popup.url());
console.log("errors:", errs);
await b.close(); srv.close();
