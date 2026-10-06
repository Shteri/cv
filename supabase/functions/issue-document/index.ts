// Issues an invoice for a work order through the garage's own Morning (Green Invoice) account and records it.
// The caller must own the (verified) garage. The provider keys are read here with the service role and never
// leave the server. POST { work_order_id, kind, payment, email?, label? }  or  { garage_id, test: true } to check the keys.
// Deploy: supabase functions deploy issue-document
import { createClient } from "npm:@supabase/supabase-js@2";
import { documentBody, hosts, pickUrl, token, type Kind, type Payment } from "./morning.ts";

const cors = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type" };
const KINDS: Kind[] = ["invoice_receipt", "tax_invoice", "receipt"];
const PAYS: Payment[] = ["cash", "card", "transfer", "app", "check", "other"];

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  const json = (b: unknown, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { ...cors, "content-type": "application/json" } });
  try {
    const user = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_ANON_KEY")!, { global: { headers: { Authorization: req.headers.get("Authorization") || "" } } });
    const { data: me } = await user.auth.getUser();
    if (!me?.user) return json({ error: "not signed in" }, 401);
    const input = await req.json().catch(() => ({}));
    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

    // which garage, and is it the caller's
    let wo: Record<string, any> | null = null, garageId = input.garage_id as string | undefined;
    if (!input.test) {
      const r = await admin.from("work_orders").select("id, garage_id, garage_car_id, kind, svc_km, km, date, lines, total").eq("id", input.work_order_id).maybeSingle();
      wo = r.data; if (!wo) return json({ error: "work order not found" }, 404);
      garageId = wo.garage_id;
    }
    const { data: g } = await admin.from("garage_profiles").select("id, name, owner_id, status").eq("id", garageId).maybeSingle();
    if (!g || g.owner_id !== me.user.id || g.status !== "verified") return json({ error: "not allowed" }, 403);
    const { data: bill } = await admin.from("garage_billing").select("api_id, api_secret, sandbox, vat_exempt").eq("garage_id", g.id).maybeSingle();
    if (!bill?.api_id || !bill?.api_secret) return json({ error: "no invoicing account" }, 400);

    const tok = await token(fetch, bill.sandbox, bill.api_id, bill.api_secret);
    if (input.test) return json({ ok: true, sandbox: bill.sandbox });

    // one provider document per work order: return the existing one instead of issuing twice
    const { data: prev } = await admin.from("invoices").select("*").eq("work_order_id", wo!.id).eq("provider", "morning").limit(1).maybeSingle();
    if (prev) return json({ invoice: prev, existing: true });

    const kind: Kind = bill.vat_exempt ? "receipt" : (KINDS.includes(input.kind) ? input.kind : "invoice_receipt");
    const payment: Payment = PAYS.includes(input.payment) ? input.payment : "other";
    const { data: car } = await admin.from("garage_cars").select("plate, year, gov, garage_customers(name, phone)").eq("id", wo!.garage_car_id).maybeSingle();
    const cust = (car?.garage_customers || {}) as { name?: string; phone?: string };
    const label = String(input.label || [car?.gov?.kinuy_mishari, car?.year].filter(Boolean).join(" ")).slice(0, 80);
    const plate = car?.plate ? String(car.plate) : "";
    const description = `${wo!.kind === "repair" ? "תיקון" : "טיפול"}${wo!.svc_km ? " " + Number(wo!.svc_km).toLocaleString("he-IL") + ' ק"מ' : ""}${label ? " · " + label : ""}${plate ? " · " + plate : ""}`;
    const date = new Date().toLocaleDateString("en-CA", { timeZone: "Asia/Jerusalem" });
    const { body, total } = documentBody({
      kind, payment, date, lines: wo!.lines || [], total: wo!.total, description,
      client: { name: cust.name || "לקוח", phone: cust.phone || null, email: input.email || null },
      remarks: wo!.km ? `ק"מ ברכב: ${Number(wo!.km).toLocaleString("he-IL")}` : undefined,
    });
    const r = await fetch(`${hosts(bill.sandbox).api}/documents`, { method: "POST", headers: { "content-type": "application/json", Authorization: `Bearer ${tok}` }, body: JSON.stringify(body) });
    const d = await r.json().catch(() => ({}));
    if (!r.ok || !d.id) return json({ error: "morning: " + (d.errorMessage || d.message || `HTTP ${r.status}`) }, 502);

    const row = { garage_id: g.id, work_order_id: wo!.id, kind, provider: "morning", number: d.number != null ? String(d.number) : null, provider_id: String(d.id),
      url: pickUrl(d.url), customer_name: cust.name || null, total, payment: kind === "tax_invoice" ? "unpaid" : payment };
    const { data: inv, error } = await admin.from("invoices").insert(row).select("*").single();
    if (error) { console.error(error); return json({ invoice: row, warning: "issued but not recorded" }); }
    return json({ invoice: inv });
  } catch (e) {
    console.error(e);
    // the garage's own keys or an empty order are the garage's to fix; anything else stays in the log
    const m = String((e as Error)?.message || e);
    if (/^auth/.test(m)) return json({ error: "auth failed" }, 502);
    if (/nothing to bill/.test(m)) return json({ error: "nothing to bill" }, 400);
    return json({ error: "server error" }, 500);
  }
});
