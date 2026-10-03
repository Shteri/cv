import { createRequire } from "module";
const require = createRequire("/opt/node-tools/node_modules/");
const { chromium } = require("playwright");
const OUT = process.argv[2], scheme = process.argv[3] || "light";
const state = {
  onboarded: true, user: { name: "מקס", via: "guest" }, active: 0, city: "רמת גן",
  cars: [{ plate: "12-345-67", schedule: "alfa-romeo-giulia-2016-2025-2.0", year: 2021, km: 52300, kmMonth: 1500, lastService: "2025-11", added: Date.now(),
    history: [
      { id: "a1", kind: "service", svcKm: 45000, text: "", items: ["engine_oil", "oil_filter", "cabin_filter"], date: "2025-11", km: 45200, where: "independent", garage: "מוסך השלום", city: "רמת גן", price: 780, extra: "", receipts: [], receipt: null, share: false, back: "yes", source: "log", at: 1 },
      { id: "a2", kind: "service", svcKm: 30000, text: "", items: ["engine_oil", "oil_filter", "cabin_filter", "air_filter"], date: "2024-08", km: 30400, where: "dealer", garage: "", city: "", price: 1150, extra: "", receipts: [], receipt: null, share: false, back: null, source: "log", at: 2 },
      { id: "a0", kind: "service", svcKm: 15000, text: "", items: ["engine_oil", "oil_filter", "brake_fluid"], date: "2023-07", km: 15200, where: "dealer", garage: "", city: "", price: 690, extra: "", receipts: [], receipt: null, share: false, back: null, source: "log", at: 3 }
    ] }]
};
const b = await chromium.launch();
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, colorScheme: scheme, locale: "he-IL", timezoneId: "Asia/Jerusalem" });
await ctx.addInitScript(s => { try { localStorage.setItem("tipulit", s); } catch (e) {} }, JSON.stringify(state));
const GF = "/tmp/claude-0/-home-user-cv/5708ed44-0317-5aa0-81b0-b42ec72148c9/scratchpad/gfonts/";
const fs = await import("fs");
await ctx.route("https://fonts.googleapis.com/**", r => r.fulfill({ status: 200, contentType: "text/css", body: fs.readFileSync(GF + "fonts.css", "utf8") }));
await ctx.route("https://fonts.gstatic.com/**", r => { const f = r.request().url().replace("https://fonts.gstatic.com/", "").replace(/\//g, "_"); r.fulfill({ status: 200, contentType: "font/woff2", body: fs.readFileSync(GF + f) }); });
const p = await ctx.newPage();
p.on("pageerror", e => console.log("ERR", e.message));
await p.goto("http://localhost:8765/index.html", { waitUntil: "networkidle" });
await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(1200); console.log("fonts", await p.evaluate(() => [...document.fonts].filter(f => f.status === "loaded").map(f => f.family).join(",")));
const shot = async (name) => { await p.waitForTimeout(900); await p.screenshot({ path: `${OUT}/${name}.png`, fullPage: true }); console.log("shot", name); };
const R = {};
const rects = async (name) => R[name] = await p.evaluate(() => { const out = {}; const add = (k, e) => { if (!e) return; const r = e.getBoundingClientRect(); if (r.width && r.bottom > 0 && r.top < innerHeight) out[k] = [r.left, r.top, r.width, r.height].map(v => Math.round(v * 3)); };
  document.querySelectorAll(".screen:not([hidden]) .card, .screen:not([hidden]) h1, .screen:not([hidden]) .counts, .screen:not([hidden]) .ring, .screen:not([hidden]) .plate, .screen:not([hidden]) .odometer, .screen:not([hidden]) .toggle, .screen:not([hidden]) .state-row, .screen:not([hidden]) .row.between, .screen:not([hidden]) .chip, .screen:not([hidden]) .garage, .screen:not([hidden]) [class*=hero], .screen:not([hidden]) .big, .screen:not([hidden]) .num, .screen:not([hidden]) .item, .screen:not([hidden]) .state").forEach((e, i) => add(i + ":" + e.tagName.toLowerCase() + "." + [...e.classList].join(".") + (e.id ? "#" + e.id : "") + " " + (e.textContent || "").trim().replace(/\s+/g, " ").slice(0, 28), e)); return out; });
const vshot = async (name) => { await p.waitForTimeout(700); await rects(name); await p.screenshot({ path: `${OUT}/${name}.png` }); console.log("v", name); };
const eshot = async (sel, name) => { const el = p.locator(sel).first(); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(600); await el.screenshot({ path: `${OUT}/${name}.png` }); console.log("e", name); };
const scrollTo = async (sel, off = 90) => { await p.evaluate(([s, o]) => { const e = document.querySelector(s); window.scrollTo(0, e.getBoundingClientRect().top + window.scrollY - o); }, [sel, off]); };
await vshot("v_home");
await eshot("#s-home .hero, #s-home .card.hero, #s-home [class*=hero]", "el_hero");
await scrollTo("#s-home [class*=hero]", 110); await vshot("v_next");
await p.click(`#nav button[data-go="car"]`); await p.waitForTimeout(800); await p.evaluate(() => window.scrollTo(0,0)); await vshot("v_condition");
await eshot("#car-counts", "el_counts");
await p.evaluate(() => { const c = document.querySelector("#car-state").closest(".card"); c.id = c.id || "state-card"; });
await eshot("#car-state", "el_state");
await p.click(`#nav button[data-go="me"]`); await p.waitForTimeout(800);
await p.evaluate(() => { const t = document.querySelector("#t1").closest(".card"); t.id = "rem-card"; });
await eshot("#rem-card", "el_reminders");
await scrollTo("#rem-card", 200); await vshot("v_reminders");
await p.click(`#nav button[data-go="home"]`); await p.waitForTimeout(500);
await p.evaluate(() => { const t = document.querySelector("#to-garages") || document.querySelector("#me-garage-find"); t && t.click(); });
await p.waitForTimeout(2500); await p.evaluate(() => window.scrollTo(0,0)); await vshot("v_garages");
await eshot("#gr-list > *:nth-child(1)", "el_garage1");
await eshot("#gr-list > *:nth-child(2)", "el_garage2");
await p.screenshot({ path: `${OUT}/full_garages.png`, fullPage: true });
fs.writeFileSync(`${OUT}/rects.json`, JSON.stringify(R, null, 1));
await b.close();
