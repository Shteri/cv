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

// failures go to public.ai_errors (migration 0014) as well as the log; never the document or the key
const admin = () => createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
async function report(userId: string | null, task: unknown, status: number, message: string) {
  console.error("ai-assist failed", task, status, message);
  try { await admin().from("ai_errors").insert({ user_id: userId, task: typeof task === "string" ? task.slice(0, 20) : null, status, message: message.slice(0, 500) }); } catch (_) { /* table missing: the log line is enough */ }
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  let userId: string | null = null, task: unknown = null;
  try {
    // the secret is ANTHROPIC_API_KEY; a key saved under another name (e.g. SCAN_KEY) is found by its sk-ant- prefix
    const key = Deno.env.get("ANTHROPIC_API_KEY") || Object.values(Deno.env.toObject()).find(v => typeof v === "string" && v.trim().startsWith("sk-ant-"))?.trim();
    if (!key) return json({ error: "ai not configured" }, 503);
    const user = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_ANON_KEY")!, { global: { headers: { Authorization: req.headers.get("Authorization") || "" } } });
    const { data: me } = await user.auth.getUser();
    if (!me?.user) return json({ error: "not signed in" }, 401);
    userId = me.user.id;

    const body = await req.json().catch(() => ({}));
    task = body.task;
    const { note, context, file } = body;
    if (typeof task !== "string" || !(task in schemas)) return json({ error: "unknown task" }, 400);
    const isFile = task === "receipt";
    const text = isFile ? "Extract the service record from this document." : String(note || "").trim();
    if (!text) return json({ error: "empty note" }, 400);
    if (isFile && (!file || !FILE_TYPES.includes(file.media_type) || typeof file.data !== "string" || !file.data)) return json({ error: "bad file" }, 400);
    if (text.length > MAX_NOTE || JSON.stringify(context ?? {}).length > MAX_CONTEXT || (isFile && file.data.length > MAX_FILE)) return json({ error: "too long" }, 413);

    const db = admin();
    const garage = GARAGE_TASKS.includes(task as Task);
    if (garage) {
      const { data: g } = await db.from("garage_profiles").select("id").eq("owner_id", me.user.id).eq("status", "verified").limit(1);
      if (!g?.length) return json({ error: "not allowed" }, 403);
    }
    const { data: used, error: bumpErr } = await db.rpc("ai_bump", { p_user: me.user.id });
    if (bumpErr) { console.error("usage", bumpErr); return json({ error: "server error" }, 500); }
    if (used > (garage ? LIMITS.garage : LIMITS.driver)) return json({ error: "daily limit" }, 429);

    // a key that isn't scoped to a workspace needs the workspace id (secret ANTHROPIC_WORKSPACE_ID, or any secret holding a wrkspc_ value)
    const ws = Deno.env.get("ANTHROPIC_WORKSPACE_ID") || Object.values(Deno.env.toObject()).find(v => typeof v === "string" && v.trim().startsWith("wrkspc_"))?.trim();
    const client = new Anthropic({ apiKey: key, defaultHeaders: ws ? { "anthropic-workspace-id": ws } : undefined });
    const t = task as Task, t0 = Date.now();
    const response = await client.beta.messages.parse({
      model: "claude-opus-5-5",
      max_tokens: 16000,  // thinking is always on and counts toward this; a dense receipt needs room
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
    // tokens and time per call (public.ai_calls, migration 0015)
    try { await db.from("ai_calls").insert({ user_id: userId, task: t, model: response.model, input_tokens: response.usage?.input_tokens ?? null, output_tokens: response.usage?.output_tokens ?? null, ms: Date.now() - t0, ok: !!response.parsed_output }); } catch (_) { /* table missing */ }
    if (response.stop_reason === "refusal") { await report(userId, t, 422, "refused " + JSON.stringify(response.stop_details)); return json({ error: "refused" }, 422); }
    if (!response.parsed_output) { await report(userId, t, 502, `no result: ${response.stop_reason} ${JSON.stringify(response.usage)}`); return json({ error: "no result" }, 502); }
    return json({ result: clean(t, response.parsed_output as any, context) });
  } catch (e) {
    await report(userId, task, e instanceof Anthropic.APIError ? (e.status ?? 0) : 500, e instanceof Anthropic.APIError ? String(e.message) : String((e as Error)?.stack || e));
    if (e instanceof Anthropic.RateLimitError) return json({ error: "busy" }, 503);
    if (e instanceof Anthropic.APIError) return json({ error: `ai ${e.status}` }, 502);
    return json({ error: "server error" }, 500);
  }
});
