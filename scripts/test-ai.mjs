// Offline checks for supabase/functions/ai-assist/tasks.ts: the schemas convert to Claude structured-output
// formats, and clean() drops ids and keys that are not in the context. No API calls.
// Needs zod and @anthropic-ai/sdk resolvable (e.g. npm i --no-save zod @anthropic-ai/sdk). Usage: node scripts/test-ai.mjs
import assert from "node:assert/strict";
let t, sdk;
try { t = await import("../supabase/functions/ai-assist/tasks.ts"); sdk = await import("@anthropic-ai/sdk/helpers/beta/zod"); }
catch (e) { console.log("ai tests skipped (install zod and @anthropic-ai/sdk to run): " + e.message.split("\n")[0]); process.exit(0); }

for (const k of Object.keys(t.schemas)) {
  const f = sdk.betaZodOutputFormat(t.schemas[k]);
  assert.equal(f.type, "json_schema", k); assert.ok(f.schema && f.schema.type === "object", k);
  assert.ok(t.SYSTEM[k] && t.EFFORT[k], k);
}
const ctx = { items: [{ key: "brake_pads", he: "רפידות בלם" }, { key: "engine_oil", he: "שמן מנוע" }], stock: [{ id: "p1", name: "רפידות" }], catalog: [{ id: "j1", name: "רפידות קדמיות" }],
  checklist: [{ key: "brakes_front" }, { key: "wipers" }], item_state: [{ item: "brake_pads" }] };
const wo = t.clean("wo", { kind: "repair", svc_km: null, km: null, notes: null, lines: [
  { type: "part", desc: "רפידות", qty: 1, price: null, hours: null, part_id: "p1", item: "brake_pads", job_id: null },
  { type: "part", desc: "דיסקים", qty: 0, price: null, hours: null, part_id: "ghost", item: "brake_discs", job_id: null },
  { type: "labor", desc: "עבודה", qty: 1, price: null, hours: 1.5, part_id: null, item: null, job_id: "j9" },
  { type: "labor", desc: " ", qty: 1, price: null, hours: null, part_id: null, item: null, job_id: null }] }, ctx);
assert.equal(wo.lines.length, 3); assert.equal(wo.lines[0].part_id, "p1"); assert.equal(wo.lines[1].part_id, null); assert.equal(wo.lines[1].item, null); assert.equal(wo.lines[1].qty, 1); assert.equal(wo.lines[2].job_id, null);
const insp = t.clean("insp", { rest_ok: true, checks: [{ key: "brakes_front", status: "now", note: "2 מ\"מ" }, { key: "made_up", status: "ok", note: null }] }, ctx);
assert.deepEqual(insp.checks.map(c => c.key), ["brakes_front"]);
const rec = t.clean("record", { kind: "service", date: "2026-09", km: 60000, price: 950, garage: null, city: null, where: "independent", svc_km: 60000, items: ["engine_oil", "nope"], text: null }, ctx);
assert.deepEqual(rec.items, ["engine_oil"]);
const rcpt = t.clean("receipt", { kind: "service", date: "2021-07", km: 96229, price: 1450, garage: "מוסך אמיר", city: null, where: null, svc_km: null, items: ["engine_oil", "invented"], text: null, confidence: "high", notes: null }, ctx);
assert.deepEqual(rcpt.items, ["engine_oil"]);
assert.ok(t.FILE_TYPES.includes("application/pdf") && t.MAX_FILE > 1e6);
const q = t.clean("quote", { lines: [{ desc: "רפידות", price: 400, item: "brake_pads", due: "due", note: null }, { desc: "x", price: 1, item: "zzz", due: "unknown", note: null }], total: 401, price_verdict: "unknown", summary: "s", questions: ["a", "b", "c", "d"] }, ctx);
assert.equal(q.lines[1].item, null); assert.equal(q.questions.length, 3);
assert.match(t.userMessage("wo", "החלפתי רפידות", ctx), /CONTEXT:[\s\S]*NOTE \(wo\):\nהחלפתי רפידות$/);
console.log("ai tests passed");
