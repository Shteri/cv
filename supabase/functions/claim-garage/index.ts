// Verifies a garage claim automatically: the caller must be signed in and have a confirmed phone
// (Supabase phone OTP) that matches the registry phone of the garage. The registry is read from the
// published site (garages.json), so the client cannot supply a fake number.
// Deploy: supabase functions deploy claim-garage   (needs SITE_URL secret, default https://tipulit.netlify.app)
import { createClient } from "npm:@supabase/supabase-js@2";

const SITE = Deno.env.get("SITE_URL") || "https://tipulit.netlify.app";
const cors = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type" };
let registry: Map<number, string> | null = null;
async function registryPhone(id: number): Promise<string | null> {
  if (!registry) {
    const d = await fetch(`${SITE}/garages.json`).then(r => r.json());
    registry = new Map((d.garages as unknown[][]).map(r => [r[0] as number, r[4] as string]));
  }
  return registry.get(id) ?? null;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  const json = (b: unknown, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { ...cors, "content-type": "application/json" } });
  try {
    const auth = req.headers.get("Authorization") || "";
    const user = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_ANON_KEY")!, { global: { headers: { Authorization: auth } } });
    const { data: me } = await user.auth.getUser();
    if (!me?.user) return json({ error: "not signed in" }, 401);
    const { profile_id } = await req.json();
    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    const { data: gp } = await admin.from("garage_profiles").select("id, garage_id, owner_id, status").eq("id", profile_id).single();
    if (!gp || gp.owner_id !== me.user.id) return json({ error: "not your claim" }, 403);
    if (gp.status === "verified") return json({ verified: true });
    const phone = await registryPhone(gp.garage_id);
    if (!phone) return json({ verified: false, reason: "garage not in registry" });
    const { data: ok, error } = await admin.rpc("verify_garage_by_phone", { p_id: gp.id, p_registry_phone: phone });
    if (error) return json({ error: error.message }, 500);
    return json({ verified: !!ok, reason: ok ? null : "phone does not match the registry" });
  } catch (e) {
    return json({ error: String(e) }, 500);
  }
});
