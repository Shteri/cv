import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const ct = f => f.endsWith(".css") ? "text/css" : f.endsWith(".js") ? "text/javascript" : "text/html; charset=utf-8";
const srv = createServer((q, r) => { let u = q.url.split("?")[0]; if (u.endsWith("/")) u += "index.html"; const f = SITE + u; if (!existsSync(f)) { r.statusCode = 404; return r.end(); } r.setHeader("content-type", ct(f)); r.end(readFileSync(f)); }).listen(8149);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const errs = [];
const m = await b.newContext({ viewport: { width: 400, height: 860 }, deviceScaleFactor: 2 });
const p = await m.newPage(); p.on("pageerror", e => errs.push(e.message)); p.on("dialog", d => d.accept());
await p.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort());
await p.goto("http://localhost:8149/approve/?demo&insp"); await p.waitForTimeout(600);
console.log("title:", await p.textContent("#a-title"), "| car:", await p.textContent("#a-car"), "| groups:", await p.$$eval("#a-checks h3", l => l.map(e => e.textContent)), "| ok summary:", await p.textContent("#a-checks summary"));
console.log("ticked:", await p.$$eval("#a-lines input:checked", l => l.length), "| total:", await p.textContent("#a-total"), "| yes:", await p.textContent("#a-yes"));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/appr-insp.png", fullPage: true });
await p.check('#a-lines [data-l="2"]'); console.log("after tick battery:", await p.textContent("#a-total"), await p.textContent("#a-yes"));
await p.click("#a-yes"); await p.waitForTimeout(200);
console.log("result:", (await p.textContent("#a-result")).slice(0, 40), "| line tags:", await p.$$eval("#a-lines .tag", l => l.map(e => e.textContent).join(",")), "| total:", await p.textContent("#a-total-label"), await p.textContent("#a-total"));
await p.screenshot({ path: (process.env.SHOTS || "/tmp") + "/appr-insp-done.png", fullPage: true });
await p.goto("http://localhost:8149/approve/?demo"); await p.waitForTimeout(500);
console.log("plain: checkboxes", await p.$$eval("#a-lines input", l => l.length), "| total", await p.textContent("#a-total"), "| yes", await p.textContent("#a-yes"));
await p.click("#a-yes"); await p.waitForTimeout(200); console.log("plain result:", (await p.textContent("#a-result")).slice(0, 25));
// real mode: approval_choose, then an old server without it
for (const old of [false, true]) {
  const q = await m.newPage(); q.on("pageerror", e => errs.push(e.message)); q.on("dialog", d => d.accept());
  await q.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.abort());
  await q.addInitScript(old => { const s = { enabled: true, approvalGet: async id => ({ id, garage: "מוסך", garage_phone: "03", car: "i10", lines: [{ desc: "רפידות", price: 400, urgent: true }, { desc: "מגבים", price: 90 }], checks: [{ key: "b", label: "בלמים", status: "now", photos: ["https://example.com/a.jpg"] }], total: 490, status: "pending" }),
    approvalChoose: async (id, l) => { if (old) throw new Error("function not found"); window.__ch = l; return { status: l.length ? "approved" : "declined", approved_lines: l }; }, approvalDecide: async (id, y) => { window.__dec = y; return y ? "approved" : "declined"; } };
    Object.defineProperty(window, "TipulitCloud", { get: () => s, set: () => {} }); }, old);
  await q.goto("http://localhost:8149/approve/?id=33333333-3333-3333-3333-333333333333"); await q.waitForTimeout(500);
  console.log(old ? "old server:" : "real:", "photos", await q.$$eval("#a-checks img", l => l.length));
  let alerted = null; q.on("dialog", d => { alerted = d.message(); });
  await q.click("#a-yes"); await q.waitForTimeout(300);
  console.log("   chose:", JSON.stringify(await q.evaluate(() => window.__ch)), "| result:", (await q.textContent("#a-result")).slice(0, 30), "| alert:", alerted);
}
console.log("errors:", errs); await b.close(); srv.close();
