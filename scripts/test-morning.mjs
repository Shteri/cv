// Unit tests for the Morning payload builder used by supabase/functions/issue-document (no network).
// Usage: node scripts/test-morning.mjs
import assert from "node:assert/strict";
const m = await import("../supabase/functions/issue-document/morning.ts");

const lines = [{ type: "part", desc: "מסנן שמן", qty: 1, price: 60 }, { type: "part", desc: "שמן 5W-30", qty: 4.5, price: 55 }, { type: "labor", desc: "עבודה", qty: 1, price: "₪200" }];
const base = { date: "2026-10-01", lines, description: "טיפול 60,000 ק\"מ", client: { name: "שרה", phone: "050-1234567", email: "s@x.co" } };

let { body, total } = m.documentBody({ ...base, kind: "invoice_receipt", payment: "card", total: 507.5 });
assert.equal(body.type, 320); assert.equal(total, 507.5);
assert.equal(body.income.length, 3); assert.ok(body.income.every(r => r.vatType === 1 && r.currency === "ILS"));
assert.equal(body.income[1].quantity, 4.5); assert.equal(body.income[2].price, 200);
assert.deepEqual(body.payment, [{ type: 3, price: 507.5, date: "2026-10-01", currency: "ILS", dealType: 1, numPayments: 1 }]);
assert.deepEqual(body.client, { name: "שרה", add: true, phone: "050-1234567", emails: ["s@x.co"] });

// total differs from the lines (discount): one summary row with the total
({ body, total } = m.documentBody({ ...base, kind: "invoice_receipt", payment: "cash", total: 450 }));
assert.equal(body.income.length, 1); assert.equal(body.income[0].price, 450); assert.equal(body.payment[0].type, 1);

// tax invoice has no payment; receipt has no income
({ body } = m.documentBody({ ...base, kind: "tax_invoice", payment: "cash", total: null }));
assert.equal(body.type, 305); assert.equal(body.payment, undefined); assert.equal(body.income.length, 3);
({ body } = m.documentBody({ ...base, kind: "receipt", payment: "app", total: 507.5 }));
assert.equal(body.type, 400); assert.equal(body.income, undefined); assert.equal(body.payment[0].type, 10);
assert.throws(() => m.documentBody({ ...base, lines: [], kind: "receipt", payment: "cash", total: 0 }), /nothing to bill/);

assert.equal(m.pickUrl({ origin: "o", he: "h" }), "h"); assert.equal(m.pickUrl("s"), "s"); assert.equal(m.pickUrl(null), null);

// auth: OAuth first, legacy fallback, readable error
const calls = [];
const fake = routes => async (url, init) => { calls.push(url); const [status, body] = routes(url, JSON.parse(init.body)); return { ok: status < 300, status, json: async () => body }; };
assert.equal(await m.token(fake(() => [200, { accessToken: "new" }]), false, "i", "s"), "new");
assert.ok(calls[0].startsWith("https://api.morning.co/idp/v1/oauth/token"));
assert.equal(await m.token(fake(u => u.includes("oauth") ? [401, { error: "invalid_client" }] : [200, { token: "old" }]), true, "i", "s"), "old");
assert.ok(calls.at(-1).startsWith("https://sandbox.d.greeninvoice.co.il/api/v1/account/token"));
await assert.rejects(m.token(fake(u => u.includes("oauth") ? [401, { error: "invalid_client", error_description: "Invalid client credentials" }] : [401, { errorMessage: "גישה נדחתה" }]), false, "i", "s"), /Invalid client credentials/);
console.log("morning tests passed");
