// Browser checks of the built site (driver app, garage demo, booking and approval pages), offline.
// Build first (node scripts/build-site.mjs), then: cd tests/e2e && npm install && node run.mjs [name...]
// A check fails when it exits non-zero, prints FAIL, or reports page errors ("errors: [ '...' ]").
import { spawn } from "node:child_process";
import { readdirSync } from "node:fs";
const dir = new URL(".", import.meta.url).pathname;
const only = process.argv.slice(2);
const checks = readdirSync(dir).filter(f => f.endsWith("-check.mjs")).map(f => f.replace(".mjs", "")).filter(n => !only.length || only.includes(n));
const run = name => new Promise(res => {
  const p = spawn(process.execPath, [dir + name + ".mjs"], { cwd: dir, env: process.env });
  let out = ""; p.stdout.on("data", d => out += d); p.stderr.on("data", d => out += d);
  const t = setTimeout(() => { p.kill(); out += "\nFAIL timeout"; }, 150000);
  p.on("close", code => { clearTimeout(t); const bad = code !== 0 || /\bFAIL\b/.test(out) || /errors: \[\s*['"]/.test(out); res({ name, ok: !bad, out }); });
});
const results = [];
for (const c of checks) { const r = await run(c); results.push(r); console.log(`${r.ok ? "ok  " : "FAIL"} ${c}`); if (!r.ok || process.env.VERBOSE) console.log(r.out.split("\n").map(l => "     " + l).join("\n")); }
const failed = results.filter(r => !r.ok);
console.log(`\n${results.length - failed.length}/${results.length} browser checks passed`);
process.exit(failed.length ? 1 : 0);
