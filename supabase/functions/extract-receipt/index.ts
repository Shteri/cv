// Supabase Edge Function: extract a service record from a receipt or invoice photo.
// Deploy: supabase functions deploy extract-receipt
// Secret:  supabase secrets set ANTHROPIC_API_KEY=sk-ant-...
// Request (JSON, from a signed-in user): { image_base64, media_type, context: { make, model, year, items: [{ key, he }] } }
// Response: the structured record below, or { error }.

import Anthropic from "npm:@anthropic-ai/sdk";
import { z } from "npm:zod";
import { zodOutputFormat } from "npm:@anthropic-ai/sdk/helpers/zod";

const Record = z.object({
  kind: z.enum(["service", "repair", "other"]).describe("service = periodic maintenance; repair = a fault fixed or a part replaced outside the routine; other = anything else"),
  date: z.string().nullable().describe("Service date as YYYY-MM, or null if not on the document"),
  km: z.number().int().nullable().describe("Odometer reading in km if printed on the document, else null"),
  price: z.number().int().nullable().describe("Total paid in ILS including VAT, else null"),
  garage: z.string().nullable().describe("Garage or business name as printed, else null"),
  city: z.string().nullable().describe("City of the garage if printed, else null"),
  where: z.enum(["importer", "independent"]).nullable().describe("importer = an importer's own service center (e.g. יוניון מוטורס, כלמוביל, טלקאר, דלק מוטורס, צ'מפיון); independent = any other garage; null if unclear"),
  items: z.array(z.string()).describe("Keys from the provided item list that were REPLACED according to the document (not just inspected)"),
  text: z.string().nullable().describe("One short Hebrew line describing non-routine work, e.g. 'החלפת מצבר', else null"),
  confidence: z.enum(["high", "medium", "low"]).describe("How readable and complete the document was"),
  notes: z.string().nullable().describe("Anything the driver should double-check, in Hebrew, else null"),
});

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
  try {
    const { image_base64, media_type, context } = await req.json();
    if (!image_base64 || !media_type) return json({ error: "image_base64 and media_type are required" }, 400);

    const itemList = (context?.items ?? []).map((i: { key: string; he: string }) => `${i.key}: ${i.he}`).join("\n");
    const client = new Anthropic({ apiKey: Deno.env.get("ANTHROPIC_API_KEY") });

    const response = await client.messages.parse({
      model: "claude-opus-5",
      max_tokens: 4000,
      system: `You read Israeli car service receipts and invoices (Hebrew, sometimes English) and turn them into one structured record.
Vehicle: ${context?.make ?? ""} ${context?.model ?? ""} ${context?.year ?? ""}.
Only report what the document shows. Never guess a km or a date; use null. Prices are in ILS; use the final total including VAT.
Map replaced parts to these item keys only (key: Hebrew name):
${itemList}
Ignore inspections and checks; list only items that were replaced or refilled.`,
      messages: [{
        role: "user",
        content: [
          { type: "image", source: { type: "base64", media_type, data: image_base64 } },
          { type: "text", text: "Extract the service record from this document." },
        ],
      }],
      output_config: { format: zodOutputFormat(Record) },
    });

    if (response.stop_reason === "refusal") return json({ error: "refused", detail: response.stop_details?.explanation ?? null }, 422);
    if (!response.parsed_output) return json({ error: "could not parse document" }, 422);
    return json(response.parsed_output);
  } catch (e) {
    if (e instanceof Anthropic.RateLimitError) return json({ error: "rate_limited" }, 429);
    if (e instanceof Anthropic.APIError) return json({ error: "api_error", status: e.status }, 502);
    return json({ error: String(e) }, 500);
  }
});

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { ...corsHeaders, "Content-Type": "application/json" } });
}
