// Morning (Green Invoice) API: authentication and document payloads. No I/O beyond the fetch passed in,
// so it runs under Deno (edge function) and Node (scripts/test-morning.mjs).
//
// Auth: since June 2026 Morning uses OAuth client credentials on a separate domain; the old
// /account/token (id + secret) is kept as a fallback for keys issued before the change.

export type Line = { type?: string; desc?: string; qty?: number | string; price?: number | string };
export type Kind = "invoice_receipt" | "tax_invoice" | "receipt";
export type Payment = "cash" | "card" | "transfer" | "app" | "check" | "other";

export const hosts = (sandbox: boolean) => sandbox
  ? { auth: "https://api.sandbox.morning.dev", api: "https://sandbox.d.greeninvoice.co.il/api/v1" }
  : { auth: "https://api.morning.co", api: "https://api.greeninvoice.co.il/api/v1" };

// document types in Morning
export const DOC_TYPE: Record<Kind, number> = { tax_invoice: 305, invoice_receipt: 320, receipt: 400 };
// payment types in Morning
export const PAY_TYPE: Record<Payment, number> = { cash: 1, check: 2, card: 3, transfer: 4, app: 10, other: 11 };

type Fetch = (url: string, init?: RequestInit) => Promise<Response>;

export async function token(f: Fetch, sandbox: boolean, id: string, secret: string): Promise<string> {
  const h = hosts(sandbox), headers = { "content-type": "application/json" };
  const r = await f(`${h.auth}/idp/v1/oauth/token`, { method: "POST", headers, body: JSON.stringify({ grant_type: "client_credentials", client_id: id, client_secret: secret }) });
  const d = await r.json().catch(() => ({}));
  if (r.ok && (d.accessToken || d.access_token)) return d.accessToken || d.access_token;
  const old = await f(`${h.api}/account/token`, { method: "POST", headers, body: JSON.stringify({ id, secret }) });
  const o = await old.json().catch(() => ({}));
  if (old.ok && o.token) return o.token;
  throw new Error("auth: " + (d.error_description || o.errorMessage || d.error || `HTTP ${r.status}/${old.status}`));
}

const num = (v: unknown) => { const n = Number(String(v ?? "").replace(/[^\d.-]/g, "")); return Number.isFinite(n) ? n : 0; };
const round2 = (n: number) => Math.round(n * 100) / 100;

// Work-order prices are what the customer pays, VAT included (vatType 1 on each row).
export function documentBody(o: {
  kind: Kind; payment: Payment; date: string; lines: Line[]; total?: number | null; description: string;
  client: { name: string; phone?: string | null; email?: string | null }; remarks?: string;
}) {
  const income = o.lines
    .map(l => ({ description: String(l.desc || (l.type === "labor" ? "עבודה" : "חלק")).slice(0, 200), quantity: num(l.qty) || 1, price: round2(num(l.price)), currency: "ILS", vatType: 1 }))
    .filter(l => l.description && l.price > 0);
  const sum = round2(income.reduce((s, l) => s + l.quantity * l.price, 0));
  const total = round2(o.total && o.total > 0 ? o.total : sum);
  if (!(total > 0)) throw new Error("nothing to bill");
  const client: Record<string, unknown> = { name: o.client.name || "לקוח", add: true };
  if (o.client.phone) client.phone = o.client.phone;
  if (o.client.email) client.emails = [o.client.email];
  const body: Record<string, unknown> = { type: DOC_TYPE[o.kind], date: o.date, lang: "he", currency: "ILS", description: o.description.slice(0, 200), client };
  if (o.remarks) body.remarks = o.remarks.slice(0, 500);
  if (o.kind !== "receipt") {
    // a single summary row when the lines don't add up to the total (discounts, rounding)
    body.income = Math.abs(sum - total) < 0.5 && income.length ? income : [{ description: o.description.slice(0, 200), quantity: 1, price: total, currency: "ILS", vatType: 1 }];
  }
  if (o.kind !== "tax_invoice") {
    const p: Record<string, unknown> = { type: PAY_TYPE[o.payment] ?? 11, price: total, date: o.date, currency: "ILS" };
    if (o.payment === "card") { p.dealType = 1; p.numPayments = 1; }
    body.payment = [p];
  }
  return { body, total };
}

// Morning returns url either as a string or as {origin, he, en}
export function pickUrl(u: unknown): string | null {
  if (!u) return null;
  if (typeof u === "string") return u;
  const o = u as Record<string, string>;
  return o.he || o.origin || o.en || null;
}
