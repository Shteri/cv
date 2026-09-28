// Runtime configuration. Leave SUPABASE_URL empty to run fully on-device (no server).
// Fill both values from Supabase → Project Settings → API. The anon key is public by design;
// row-level security in supabase/migrations protects the data.
window.TIPULIT_CONFIG = {
  SUPABASE_URL: "https://enzwltbsbamqtfflkzgi.supabase.co",
  SUPABASE_ANON_KEY: "",
  // Minimum reports before a community price bucket is shown (mirrors the SQL function).
  MIN_REPORTS: 3
};
