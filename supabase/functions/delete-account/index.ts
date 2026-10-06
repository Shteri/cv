// Deletes the signed-in user's account and everything in it: the files in their storage folders, then the auth
// user. Every table that holds their data references auth.users with on delete cascade (cars, records, garage
// profiles and through them the garage's data, links, plate requests, AI usage). POST { confirm: "delete" }.
import { createClient } from "@supabase/supabase-js";

const cors = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type" };
const json = (b: unknown, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { ...cors, "content-type": "application/json" } });

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const user = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_ANON_KEY")!, { global: { headers: { Authorization: req.headers.get("Authorization") || "" } } });
    const { data: me } = await user.auth.getUser();
    if (!me?.user) return json({ error: "not signed in" }, 401);
    const body = await req.json().catch(() => ({}));
    if (body.confirm !== "delete") return json({ error: "not confirmed" }, 400);
    const uid = me.user.id;
    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

    // every file under a folder, recursively (storage lists one level at a time)
    async function files(bucket: string, prefix: string): Promise<string[]> {
      const out: string[] = [];
      for (let offset = 0; ; offset += 1000) {
        const { data, error } = await admin.storage.from(bucket).list(prefix, { limit: 1000, offset });
        if (error || !data?.length) break;
        for (const o of data) { const p = `${prefix}/${o.name}`; if (o.id) out.push(p); else out.push(...await files(bucket, p)); }
        if (data.length < 1000) break;
      }
      return out;
    }
    const { data: garages } = await admin.from("garage_profiles").select("id").eq("owner_id", uid);
    const folders: [string, string][] = [["receipts", uid], ["plate-proofs", uid], ["garage-photos", uid], ...(garages || []).map(g => ["inspection-photos", g.id] as [string, string])];
    let removed = 0;
    for (const [bucket, prefix] of folders) {
      const list = await files(bucket, prefix);
      for (let i = 0; i < list.length; i += 100) { const { error } = await admin.storage.from(bucket).remove(list.slice(i, i + 100)); if (!error) removed += Math.min(100, list.length - i); }
    }
    const { error } = await admin.auth.admin.deleteUser(uid);
    if (error) return json({ error: "delete failed: " + error.message }, 500);
    return json({ ok: true, files: removed, garages: (garages || []).length });
  } catch (e) {
    return json({ error: String((e as Error).message || e) }, 500);
  }
});
