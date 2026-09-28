// Guards the split between content and design, so product changes cannot quietly break the look.
// Run: node scripts/check-design.mjs   (part of the Netlify and GitHub builds; exits 1 on any violation)
//
// Rules
// 1. Literal colours (hex, rgb/hsl, white/black) and font names live only in app/styles/tokens.css.
// 2. HTML files hold no <style> blocks. Inline style="" may set only custom properties (--name: value),
//    i.e. data handed to CSS, never a visual rule.
// 3. JavaScript may touch styles only through classes or el.style.setProperty("--name", ...).
// 4. SVG in markup takes colour from CSS: fill/stroke attributes may only be "none" or "currentColor".
// 5. Every var(--x) used resolves to a token, a property defined in the same stylesheet, or a known runtime property.
// 6. Every static class name in markup or JS templates exists in a stylesheet (or is a declared behaviour hook).
import { readFileSync } from "node:fs";

const root = new URL("../", import.meta.url).pathname;
const read = f => readFileSync(root + f, "utf8");
const TOKENS = "app/styles/tokens.css";
const CSS = ["app/styles/app.css", "app/welcome/welcome.css"];
const HTML = { "app/index.html": ["app/styles/app.css"], "app/welcome/index.html": ["app/welcome/welcome.css"] };

// Custom properties that markup or scripts set at runtime (documented in DESIGN.md, "Design in code").
const RUNTIME = new Set(["--i", "--k", "--r", "--s", "--c", "--n", "--h", "--x", "--y", "--mx", "--my", "--rx", "--ry", "--p", "--drag", "--vt", "--spin"]);
// Classes that exist only as behaviour hooks for scripts or tests; they carry no styling on purpose.
const HOOKS = new Set(["magnetic", "js"]);

const errors = [];
const fail = (file, line, msg) => errors.push(`${file}:${line}  ${msg}`);
const lineOf = (text, idx) => text.slice(0, idx).split("\n").length;
const stripComments = css => css.replace(/\/\*[\s\S]*?\*\//g, m => m.replace(/[^\n]/g, " "));

const COLOR = /#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?)\(|(?<![-\w])(?:white|black)(?![-\w])/;
const FONT = /["'](?:Rubik|IBM Plex Sans Hebrew|Heebo|Inter|Arial|Segoe UI)["']/;

// class="..." values, skipping ${...} template expressions (which may themselves contain quotes)
function* classAttrs(src) {
  const re = /class="/g; let m;
  while ((m = re.exec(src))) {
    let i = re.lastIndex, depth = 0, out = "";
    for (; i < src.length; i++) {
      const ch = src[i];
      if (depth === 0 && ch === "$" && src[i + 1] === "{") { depth = 1; i++; out += " "; continue; }
      if (depth > 0) { if (ch === "{") depth++; else if (ch === "}") depth--; continue; }
      if (ch === '"') break;
      out += ch;
    }
    yield { value: out, line: lineOf(src, m.index) };
    re.lastIndex = i + 1;
  }
}

// ---------- tokens ----------
const tokensCss = stripComments(read(TOKENS));
const tokens = new Set([...tokensCss.matchAll(/(--[\w-]+)\s*:/g)].map(m => m[1]));

// ---------- stylesheets ----------
const cssClasses = new Set();
for (const f of CSS) {
  const css = stripComments(read(f));
  for (const m of css.matchAll(/\.(-?[_a-zA-Z][\w-]*)/g)) cssClasses.add(m[1]);
  const local = new Set([...css.matchAll(/(--[\w-]+)\s*:/g)].map(m => m[1]));
  // declarations are the leaf blocks { ... } with no nested braces
  for (const blk of css.matchAll(/\{([^{}]*)\}/g)) {
    for (const decl of blk[1].split(";")) {
      const i = decl.indexOf(":"); if (i < 0) continue;
      const prop = decl.slice(0, i).trim(), val = decl.slice(i + 1);
      const at = lineOf(css, blk.index + blk[0].indexOf(decl));
      if (/^(?:src|content)$/.test(prop) || /^url\(/.test(val.trim())) continue; // data URIs (grain) carry no colour tokens
      if (COLOR.test(val.replace(/url\([^)]*\)/g, ""))) fail(f, at, `literal colour in "${prop}": use a token from ${TOKENS}`);
      if (FONT.test(val)) fail(f, at, `font name in "${prop}": use var(--font-text) or var(--font-display)`);
    }
  }
  for (const m of css.matchAll(/var\((--[\w-]+)/g)) {
    if (!tokens.has(m[1]) && !local.has(m[1]) && !RUNTIME.has(m[1])) fail(f, lineOf(css, m.index), `unknown custom property ${m[1]}`);
  }
}

// ---------- markup and scripts ----------
for (const [f, sheets] of Object.entries(HTML)) {
  const src = read(f);
  const own = new Set(sheets.flatMap(sh => [...stripComments(read(sh)).matchAll(/\.(-?[_a-zA-Z][\w-]*)/g)].map(m => m[1])));
  for (const m of src.matchAll(/<style[\s>]/g)) fail(f, lineOf(src, m.index), "<style> block: move the rules to a stylesheet");
  for (const m of src.matchAll(/\sstyle="([^"]*)"/g)) {
    const decls = m[1].split(";").map(d => d.trim()).filter(Boolean);
    for (const d of decls) {
      const name = d.split(":")[0].trim();
      if (!name.startsWith("--") && !name.startsWith("${")) fail(f, lineOf(src, m.index), `inline style "${d}": add a class; inline style may only pass --custom-properties`);
      else if (name.startsWith("--") && !RUNTIME.has(name)) fail(f, lineOf(src, m.index), `inline ${name} is not a declared runtime property`);
    }
  }
  for (const m of src.matchAll(/\.style\.(?!setProperty\(\s*["'`]--)(\w+)/g)) fail(f, lineOf(src, m.index), `el.style.${m[1]}: toggle a class or set a --custom-property instead`);
  for (const m of src.matchAll(/\b(fill|stroke|stop-color|color)="(?!none"|currentColor")([^"]*)"/g)) fail(f, lineOf(src, m.index), `${m[1]}="${m[2]}" in markup: give the element a class and colour it in CSS`);
  // (the browser-chrome <meta name="theme-color"> cannot read CSS variables, so it is the one allowed literal)
  const noMeta = src.replace(/<meta name="theme-color"[^>]*>/g, m => m.replace(/[^\n]/g, " "));
  for (const m of noMeta.matchAll(/["'`]#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{8})["'`]|\b(?:rgba?|hsla?)\(\s*\d/g)) fail(f, lineOf(src, m.index), `colour literal ${m[0]} in markup/JS: use a class and a token`);
  for (const m of src.matchAll(/font-family\s*[=:]/g)) fail(f, lineOf(src, m.index), "font-family in markup: use a class");
  // static class names (template expressions stripped) must exist in a stylesheet
  for (const m of classAttrs(src)) {
    const names = m.value.split(/\s+/).filter(n => /^[a-z][\w-]*$/i.test(n));
    for (const n of names) if (!own.has(n) && !cssClasses.has(n) && !HOOKS.has(n)) fail(f, m.line, `class "${n}" has no rule in ${sheets.join(", ")}`);
  }
}

if (errors.length) {
  console.error(`design check: ${errors.length} problem(s)\n` + errors.map(e => "  " + e).join("\n"));
  process.exit(1);
}
console.log(`design check: ok (${tokens.size} tokens; ${CSS.length} stylesheets and ${Object.keys(HTML).length} pages clean)`);
