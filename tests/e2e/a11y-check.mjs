// Accessibility: axe-core (WCAG 2.0 A and AA rules, the basis of Israeli standard 5568) finds no violations on the
// public pages, the landing page, booking, the garage demo and every tab of the driver app, in light and dark.
import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const AXE = readFileSync(new URL("node_modules/axe-core/axe.min.js", import.meta.url), "utf8");
const srv = createServer((q, r) => { let f = SITE + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : f.endsWith(".svg") ? "image/svg+xml" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8162);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const ok = (c, m) => console.log((c ? "OK   " : "FAIL ") + m);
const errs = [];
const scan = async (p, label) => {
  await p.addScriptTag({ content: AXE });
  const v = await p.evaluate(async () => (await axe.run(document, { runOnly: ["wcag2a", "wcag2aa"] })).violations.map(v => `${v.id} ×${v.nodes.length}: ${v.nodes.slice(0, 2).map(n => n.target.join(" ") + ((n.failureSummary || "").match(/contrast of [\d.]+ \(foreground color: #\w+, background color: #\w+/) || [""])[0]).join(", ")}`));
  ok(!v.length, label + (v.length ? "\n       " + v.join("\n       ") : ""));
};
const STATE = { onboarded: true, user: { name: "מקס", via: "guest" }, city: "נתניה", cars: [{ plate: "12-345-67", schedule: "hyundai-i10-2014-2019", year: 2017, km: 88000, kmMonth: 1500, lastService: "2024-06",
  history: [{ id: "s60", kind: "service", svcKm: 55000, km: 56000, date: "2024-06", items: ["engine_oil", "oil_filter"], garage: "מוסך יוסי", price: 900, receipts: [], share: false }] }], active: 0 };
for (const scheme of ["light", "dark"]) {
  const ctx = await b.newContext({ viewport: { width: 400, height: 860 }, colorScheme: scheme, reducedMotion: "reduce" });
  const p = await ctx.newPage(); p.on("pageerror", e => errs.push(e.message));
  await p.route("https://**", r => r.abort());
  for (const path of ["welcome/", "privacy/", "terms/", "contact/", "accessibility/", "licenses/", "book/?demo", "garage/?demo"]) {
    await p.goto("http://localhost:8162/" + path); await p.waitForTimeout(500); await scan(p, `${scheme} ${path}`);
  }
  await p.goto("http://localhost:8162/"); await p.waitForTimeout(200); await scan(p, `${scheme} sign-in`);
  await p.evaluate(s => localStorage.setItem("tipulit", JSON.stringify(s)), STATE);
  await p.reload(); await p.waitForTimeout(600);
  for (const tab of ["home", "car", "tl", "garages", "me"]) {
    await p.click(`#nav button[data-go="${tab}"]`); await p.waitForTimeout(400);
    await p.keyboard.press("Escape").catch(() => {}); await scan(p, `${scheme} app: ${tab}`);
  }
  await ctx.close();
}
console.log("errors:", errs);
await b.close(); srv.close();
