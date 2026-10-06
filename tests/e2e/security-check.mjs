// Security: pages run under the site's real headers (netlify.toml, and the per-page CSP that build-site writes to
// _headers) with no CSP violations; an injected inline script or on…= handler is blocked; system errors never
// reach the screen; the contact and booking honeypots swallow bots; a session idle for 30 days is signed out.
import { chromium } from "playwright";
const SITE = process.env.SITE_DIR || new URL("../../site", import.meta.url).pathname;
import { createServer } from "node:http"; import { readFileSync, existsSync } from "node:fs";
const toml = readFileSync(new URL("../../netlify.toml", import.meta.url), "utf8");
const header = name => (toml.match(new RegExp(`^\\s*${name} = "([^"]+)"`, "m")) || [])[1];
const ok = (c, m) => console.log((c ? "OK   " : "FAIL ") + m);
const rules = {}; for (const m of readFileSync(SITE + "/_headers", "utf8").matchAll(/^(\/\S*)\n\s+Content-Security-Policy: (.+)$/gm)) rules[m[1]] = m[2];
const CSP = rules["/"];
ok(Object.keys(rules).length >= 20 && CSP && /frame-ancestors 'none'/.test(CSP) && /object-src blob:/.test(CSP) && !/unsafe-eval|script-src[^;]*unsafe-inline/.test(CSP) && /'sha256-/.test(CSP), "every page has a CSP: scripts by hash, no eval, no framing");
ok(!/Content-Security-Policy\s*=/.test(toml), "the CSP is set in one place (_headers), never twice");
ok(/max-age=\d{7,}/.test(header("Strict-Transport-Security") || ""), "HSTS is on");
ok(/microphone=\(\)/.test(header("Permissions-Policy") || ""), "Permissions-Policy limits device access");
// served like Netlify (upgrade-insecure-requests dropped: the test server is plain http)
const srv = createServer((q, r) => { let f = SITE + q.url.split("?")[0]; if (f.endsWith("/")) f += "index.html"; if (!existsSync(f)) { r.statusCode = 404; return r.end(); }
  const csp = rules[q.url.split("?")[0]]; if (csp) r.setHeader("content-security-policy", csp.replace(/;\s*upgrade-insecure-requests/, ""));
  r.setHeader("content-type", f.endsWith(".js") ? "text/javascript" : f.endsWith(".css") ? "text/css" : f.endsWith(".json") ? "application/json" : f.endsWith(".svg") ? "image/svg+xml" : f.endsWith(".png") ? "image/png" : f.endsWith(".webmanifest") ? "application/manifest+json" : "text/html; charset=utf-8"); r.end(readFileSync(f)); }).listen(8161);
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const ctx = await b.newContext({ viewport: { width: 400, height: 860 } });
// supabase-js stand-in from the CDN: records sign-outs and RPCs
const SB = `window.supabase = { createClient: () => ({ auth: { signOut: async o => { window.__signedOut = o || {}; }, getSession: async () => ({ data: { session: { user: { id: "u1", email: "a@b.c" } } } }), onAuthStateChange: () => {} },
  rpc: async (n, a) => { (window.__rpc = window.__rpc || []).push(n); return { error: null }; }, from: () => ({ select: () => ({ eq: async () => ({ data: [], error: null }) }) }) }) };`;
await ctx.route("https://cdn.jsdelivr.net/npm/@supabase/**", r => r.fulfill({ contentType: "text/javascript", body: SB }));
await ctx.route("https://fonts.g**", r => r.abort()); await ctx.route("https://data.gov.il/**", r => r.abort());
const p = await ctx.newPage(); const errs = [], csp = [];
p.on("pageerror", e => errs.push(e.message)); p.on("console", m => { if (/Content Security Policy/i.test(m.text())) csp.push(m.text().slice(0, 160)); });
const base = "http://localhost:8161/";
for (const path of ["", "?demo", "welcome/", "privacy/", "terms/", "contact/", "accessibility/", "licenses/", "book/?demo", "approve/?demo", "appt/?demo", "garage/?demo"]) { await p.goto(base + path); await p.waitForTimeout(500); }
ok(!csp.length, "no CSP violations on any page" + (csp.length ? ": " + csp.slice(0, 3).join(" | ") : ""));
await p.goto(base + "?demo"); await p.waitForTimeout(300);
await p.evaluate(() => { document.body.insertAdjacentHTML("beforeend", '<img src="data:," onerror="window.__xss=1"><script>window.__xss=2<\/script>'); const s = document.createElement("script"); s.textContent = "window.__xss=3"; document.body.appendChild(s); }); await p.waitForTimeout(300);
ok(!(await p.evaluate(() => window.__xss)), "injected markup cannot run script (inline handler, inline script)");
const injected = csp.length; csp.length = 0;
ok(injected > 0, "and the browser reported the attempt as a CSP violation");
// the driver app under CSP: a guest car loads, the garage tab renders
await p.goto(base); await p.evaluate(() => localStorage.setItem("tipulit", JSON.stringify({ onboarded: true, user: { name: "מקס", via: "guest" }, city: "נתניה", cars: [{ plate: "12-345-67", schedule: "hyundai-i10-2014-2019", year: 2017, km: 88000, kmMonth: 1500, history: [] }], active: 0 })));
await p.reload(); await p.waitForTimeout(600); await p.click('#nav button[data-go="garages"]'); await p.waitForTimeout(600);
ok((await p.$$("#s-garages .garage, .garage")).length > 0 && !csp.length, "the app and the garage list work under the CSP");
// errors: a raw server message becomes a short Hebrew sentence
await p.goto(base + "contact/"); await p.waitForTimeout(300);
const w = await p.evaluate(() => [TipulitCloud.why(new Error('relation "public.x" does not exist')), TipulitCloud.why(new Error("Failed to fetch")), TipulitCloud.why({ message: "new row violates row-level security policy" })]);
ok(!/relation|public\.|row-level/.test(w.join(" ")) && /אינטרנט/.test(w[1]) && /הרשאה/.test(w[2]), "system errors are translated, never shown raw: " + w.join(" / "));
const code = readFileSync(SITE + "/index.html", "utf8") + readFileSync(SITE + "/garage/core.js", "utf8");
ok(!/\+ (e|err)\.message\b|\((e|err)\.message \|\| \1\)/.test(code), "no screen text is built from e.message");
// honeypots
await p.evaluate(() => { window.__rpc = []; });
await p.fill("#c-msg", "שלום"); await p.fill("#c-email", "bot@x.io"); await p.fill("#c-web", "http://spam");
await p.click("#c-go"); await p.waitForTimeout(300);
ok(await p.isVisible("#c-done") && !(await p.evaluate(() => window.__rpc || [])).includes("contact_send"), "contact: a filled honeypot looks sent but nothing is stored");
ok(await p.evaluate(() => { const l = document.querySelector("#c-web").closest("label"); const r = l.getBoundingClientRect(); return l.getAttribute("aria-hidden") === "true" && document.querySelector("#c-web").tabIndex === -1 && (r.right < 0 || r.left > innerWidth || r.width <= 1); }), "the honeypot is out of sight, out of tab order and hidden from screen readers");
await p.goto(base + "contact/"); await p.waitForTimeout(300); await p.evaluate(() => { window.__rpc = []; });
await p.fill("#c-msg", "שלום"); await p.fill("#c-email", "me@x.io"); await p.click("#c-go"); await p.waitForTimeout(300);
ok((await p.evaluate(() => window.__rpc || [])).includes("contact_send"), "contact: a person's message is sent");
ok(/id="b-web"/.test(readFileSync(SITE + "/book/index.html", "utf8")) && /\$\("#b-web"\)\.value/.test(readFileSync(SITE + "/book/index.html", "utf8")), "booking has the same honeypot");
// idle sign-out
const idle = async (daysAgo, hash = "") => { await p.goto(base + "contact/"); await p.evaluate(t => localStorage.setItem("tipulit-active", String(t)), Date.now() - daysAgo * 864e5); await p.goto(base + "contact/" + hash); await p.waitForTimeout(400); return p.evaluate(() => ({ out: window.__signedOut || null, active: +localStorage.getItem("tipulit-active") })); };
const r40 = await idle(40), r3 = await idle(3), rAuth = await idle(40, "#access_token=x&expires_in=3600");
ok(r40.out && r40.out.scope === "local" && Date.now() - r40.active < 60000, "a session unused for 40 days is signed out on this device, and the clock restarts");
ok(!r3.out, "a session used 3 days ago stays signed in");
ok(!rAuth.out, "a fresh sign-in redirect is never signed out");
console.log("errors:", errs);
await b.close(); srv.close();
