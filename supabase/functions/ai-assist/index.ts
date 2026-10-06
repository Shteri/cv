// AI assist: turns a short Hebrew note (or a receipt) into structured data for five screens.
//   wo      garage work order lines          (garage owners)
//   insp    vehicle inspection checklist     (garage owners)
//   record  driver's service record          (drivers)
//   quote   is a garage quote due / fair     (drivers)
//   receipt a receipt photo or PDF -> record (drivers)
// POST { task, note, context } (receipt: { task, file: { data, media_type }, context }) with the user's session. Needs the ANTHROPIC_API_KEY secret.
// Signed-in users only, with a daily limit per user (public.ai_bump). Results are shown for review, never saved here.
import Anthropic from "@anthropic-ai/sdk";
import { betaZodOutputFormat } from "@anthropic-ai/sdk/helpers/beta/zod";
import { createClient } from "@supabase/supabase-js";
import { clean, EFFORT, FILE_TYPES, GARAGE_TASKS, LIMITS, MAX_CONTEXT, MAX_FILE, MAX_NOTE, schemas, SYSTEM, type Task, userMessage } from "./tasks.ts";

const cors = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type" };
const json = (b: unknown, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { ...cors, "content-type": "application/json" } });

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const key = Deno.env.get("ANTHROPIC_API_KEY");
    if (!key) return json({ error: "ai not configured" }, 503);
    const user = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_ANON_KEY")!, { global: { headers: { Authorization: req.headers.get("Authorization") || "" } } });
    const { data: me } = await user.auth.getUser();
    if (!me?.user) return json({ error: "not signed in" }, 401);

    const { task, note, context, file } = await req.json().catch(() => ({}));
    if (!(task in schemas)) return json({ error: "unknown task" }, 400);
    const isFile = task === "receipt";
    const text = isFile ? "Extract the service record from this document." : String(note || "").trim();
    if (!text) return json({ error: "empty note" }, 400);
    if (isFile && (!file || !FILE_TYPES.includes(file.media_type) || typeof file.data !== "string" || !file.data)) return json({ error: "bad file" }, 400);
    if (text.length > MAX_NOTE || JSON.stringify(context ?? {}).length > MAX_CONTEXT || (isFile && file.data.length > MAX_FILE)) return json({ error: "too long" }, 413);

    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    const garage = GARAGE_TASKS.includes(task);
    if (garage) {
      const { data: g } = await admin.from("garage_profiles").select("id").eq("owner_id", me.user.id).eq("status", "verified").limit(1);
      if (!g?.length) return json({ error: "not allowed" }, 403);
    }
    const { data: used, error: bumpErr } = await admin.rpc("ai_bump", { p_user: me.user.id });
    if (bumpErr) return json({ error: "usage: " + bumpErr.message }, 500);
    if (used > (garage ? LIMITS.garage : LIMITS.driver)) return json({ error: "daily limit" }, 429);

    const client = new Anthropic({ apiKey: key });
    const t = task as Task;
    const response = await client.beta.messages.parse({
      model: "claude-opus-5-5",
      max_tokens: 4000,
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
      system: SYSTEM[t],
      output_config: { effort: EFFORT[t], format: betaZodOutputFormat(schemas[t]) },
      messages: [{ role: "user", content: isFile
        ? [file.media_type === "application/pdf"
            ? { type: "document" as const, source: { type: "base64" as const, media_type: "application/pdf" as const, data: file.data } }
            : { type: "image" as const, source: { type: "base64" as const, media_type: file.media_type as "image/jpeg" | "image/png" | "image/webp", data: file.data } },
           { type: "text" as const, text: userMessage(t, text, context) }]
        : userMessage(t, text, context) }],
    });
    if (response.stop_reason === "refusal") return json({ error: "refused" }, 422);
    if (!response.parsed_output) return json({ error: "no result" }, 502);
    return json({ result: clean(t, response.parsed_output as any, context) });
  } catch (e) {
    if (e instanceof Anthropic.RateLimitError) return json({ error: "busy" }, 503);
    if (e instanceof Anthropic.APIError) return json({ error: `ai ${e.status}` }, 502);
    return json({ error: String((e as Error).message || e) }, 500);
  }
});
