// Runtime configuration. Leave SUPABASE_URL empty to run fully on-device (no server).
// Fill both values from Supabase → Project Settings → API. The anon key is public by design;
// row-level security in supabase/migrations protects the data.
window.TIPULIT_CONFIG = {
  SUPABASE_URL: "https://enzwltbsbamqtfflkzgi.supabase.co",
  SUPABASE_ANON_KEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVuendsdGJzYmFtcXRmZmxremdpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA1ODY5NzksImV4cCI6MjEwNjE2Mjk3OX0.bgBLCSmZOa1ZhY1HWN95Mw-KGwT-rBXqlZII6KIjS00",
  // Minimum reports before a community price bucket is shown (mirrors the SQL function).
  MIN_REPORTS: 3,
  // Where privacy requests go (the privacy policy and the "פרטיות" card show it). Empty: the in-app tools only.
  PRIVACY_EMAIL: ""
};
