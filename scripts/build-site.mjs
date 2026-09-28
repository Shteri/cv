// Builds the deployable static site into the repository ROOT (served by GitHub Pages from main).
// app/index.html is written for the claude.ai artifact wrapper (no <html>/<head>),
// so here we wrap it in a full document, add PWA files, and copy the data bundle.
import { mkdirSync, readFileSync, writeFileSync, copyFileSync, readdirSync } from "node:fs";
import { createHash } from "node:crypto";
const root = new URL("../", import.meta.url).pathname;
const src = readFileSync(root + "app/index.html", "utf8");
const title = (src.match(/<title>(.*?)<\/title>/) || [, "טיפולית"])[1];
// Stylesheet links in the fragment move to <head> so tokens and components load before first paint.
const headLinks = (src.match(/<link [^>]*>/g) || []).join("\n");
const body = src.replace(/<title>.*?<\/title>\s*/, "").replace(/<link [^>]*>\s*/g, "");
const html = `<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#F1F2F4" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#08090B" media="(prefers-color-scheme: dark)">
<meta name="description" content="הטיפול הבא לרכב שלך לפי ספר היבואן, ומה לוודא במוסך.">
<title>${title}</title>
<meta property="og:title" content="${title}">
<meta property="og:description" content="הטיפול הבא לרכב שלך לפי ספר היבואן, ומה לוודא במוסך.">
<meta property="og:type" content="website">
<meta property="og:image" content="icon-512.png">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
${headLinks}
<style>
  /* document-level resets only; every colour and font comes from styles/tokens.css */
  :root { padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
  img { max-width: 100%; }
  [hidden] { display: none !important; }
</style>
</head>
<body>
${body}
<script>
if ("serviceWorker" in navigator) navigator.serviceWorker.register("sw.js").catch(() => {});
</script>
</body>
</html>
`;
const out = (process.env.SITE_OUT ? process.env.SITE_OUT.replace(/\/?$/, "/") : root);
mkdirSync(out, { recursive: true });
writeFileSync(out + "index.html", html);
copyFileSync(root + "app/data.js", out + "data.js");
copyFileSync(root + "app/lookup.js", out + "lookup.js");
copyFileSync(root + "app/config.js", out + "config.js");
copyFileSync(root + "app/cloud.js", out + "cloud.js");
mkdirSync(out + "styles", { recursive: true });
for (const f of ["tokens.css", "app.css"]) copyFileSync(root + "app/styles/" + f, out + "styles/" + f);
for (const f of ["icon-192.png", "icon-512.png"]) copyFileSync(root + "app/" + f, out + "" + f);

// Landing page at /welcome/: model coverage is generated from the schedules, so the page never overstates it.
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
// One entry per model (generations merged), plus make facts. Scales to hundreds of models: the page searches and filters it.
const models = new Map(), makes = new Map();
for (const f of readdirSync(root + "data/schedules").filter(f => f.endsWith(".json")).sort()) {
  const s = JSON.parse(readFileSync(root + "data/schedules/" + f, "utf8"));
  const key = s.make_he + "|" + s.model_he;
  const m = models.get(key) || { mk: s.make_he, mkEn: s.make, md: s.model_he, mdEn: s.model, imp: s.importer || "", y0: 9999, y1: 0, hy: false };
  m.y0 = Math.min(m.y0, s.years[0]); m.y1 = Math.max(m.y1, s.years[1]); m.hy = m.hy || s.fuel === "hybrid";
  models.set(key, m);
  if (!makes.has(s.make_he)) makes.set(s.make_he, { en: s.make, imp: s.importer || "", n: 0 });
}
for (const m of models.values()) makes.get(m.mk).n++;
const modelCount = models.size;
const logoSlug = { "Toyota": "toyota", "Hyundai": "hyundai", "Kia": "kia", "Mazda": "mazda", "Skoda": "skoda", "Alfa Romeo": "alfaromeo" };
const logo = en => {
  const f = root + "app/welcome/logos/" + (logoSlug[en] || "_") + ".svg";
  try { return readFileSync(f, "utf8").replace(/<title>.*?<\/title>/, "").replace("<svg ", '<svg fill="currentColor" aria-hidden="true" focusable="false" '); } catch (e) { return ""; }
};
const makeList = [...makes].sort((a, b) => b[1].n - a[1].n || a[0].localeCompare(b[0], "he")).map(([he, v]) => ({ he, ...v, logo: logo(v.en) }));
const rank = new Map(makeList.map((m, i) => [m.he, i]));
const catalog = { makes: makeList, models: [...models.values()].sort((a, b) => rank.get(a.mk) - rank.get(b.mk) || a.md.localeCompare(b.md, "he")) };
// JSON inside a <script> tag: escape "<" so no string can close the tag
const catalogJSON = JSON.stringify(catalog).replace(/</g, "\\u003c");
const welcomeSrc = root + "app/welcome/";
mkdirSync(out + "welcome", { recursive: true });
writeFileSync(out + "welcome/index.html", readFileSync(welcomeSrc + "index.html", "utf8")
  .replaceAll("{{MODEL_COUNT}}", String(modelCount)).replace("{{MAKE_COUNT}}", String(makeList.length))
  .replace("{{CATALOG}}", () => catalogJSON)
  .replace(/\{\{ICON:([a-z-]+)\}\}/g, (m, n) => readFileSync(welcomeSrc + "icons/" + n + ".svg", "utf8").replace("<svg ", '<svg aria-hidden="true" focusable="false" ')));
for (const f of ["home.png", "timeline.png", "condition.png", "welcome.css"]) copyFileSync(welcomeSrc + f, out + "welcome/" + f);
writeFileSync(out + "manifest.webmanifest", JSON.stringify({
  name: "טיפולית", short_name: "טיפולית", lang: "he", dir: "rtl", start_url: "./", scope: "./", display: "standalone",
  background_color: "#111418", theme_color: "#111418",
  description: "הטיפול הבא לרכב שלך לפי ספר היבואן, ומה לוודא במוסך.",
  icons: [{ src: "icon-192.png", sizes: "192x192", type: "image/png" }, { src: "icon-512.png", sizes: "512x512", type: "image/png" }, { src: "icon.svg", sizes: "any", type: "image/svg+xml" }]
}, null, 2));
// Content hash, so rebuilding unchanged sources yields identical files (no churn in git or in the service worker).
const version = createHash("sha1").update(html).update(readFileSync(root + "app/data.js")).update(readFileSync(root + "app/lookup.js")).update(readFileSync(root + "app/cloud.js")).update(readFileSync(root + "app/config.js")).update(readFileSync(root + "app/styles/tokens.css")).update(readFileSync(root + "app/styles/app.css")).digest("hex").slice(0, 10);
writeFileSync(out + "sw.js", `// Minimal offline cache for the app shell. Version: ${version}
const CACHE = "tipulit-${version}";
const ASSETS = ["./", "./index.html", "./styles/tokens.css", "./styles/app.css", "./data.js", "./lookup.js", "./config.js", "./cloud.js", "./manifest.webmanifest", "./icon.svg", "./icon-192.png", "./icon-512.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET" || !e.request.url.startsWith(self.location.origin)) return;
  e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; }).catch(() => caches.match(e.request)));
});
`);
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><rect width="512" height="512" rx="110" fill="#F7C948"/><rect x="18" y="18" width="476" height="476" rx="94" fill="none" stroke="#111418" stroke-width="20"/><text x="256" y="345" font-family="Rubik, Arial, sans-serif" font-weight="700" font-size="300" fill="#111418" text-anchor="middle">ט</text></svg>`;
writeFileSync(out + "icon.svg", svg);
console.log("site built into " + out);
