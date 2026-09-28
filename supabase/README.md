# Tipulit backend (Supabase)

What the server adds over the local-only app: Google sign-in and sync between devices,
shared price and garage reports from other drivers, private storage for receipt photos,
and automatic extraction of a record from a receipt photo (Claude vision).

The app works without any of this. `app/config.js` decides: with an empty
`SUPABASE_URL` the app stays local (browser storage); once the URL and anon key are
filled in, every feature below switches on.

## One-time setup (about 20 minutes, done by the project owner)

1. **Create a project** at https://supabase.com (free tier). Pick a region in Europe.
2. **Run the migration**: open SQL Editor, paste `migrations/0001_init.sql`, run.
   This creates the tables, the row-level security rules, the community functions
   and the private `receipts` storage bucket.
3. **Google sign-in**: Authentication → Providers → Google → enable. It needs an OAuth
   client from Google Cloud Console (APIs & Services → Credentials → OAuth client ID,
   type Web). Authorized redirect URI: `https://<project-ref>.supabase.co/auth/v1/callback`.
   Paste the client ID and secret into Supabase.
   Then Authentication → URL Configuration → Site URL: `https://shteri.github.io/cv/`
   and add it to Redirect URLs (plus `http://localhost:*` for local testing).
4. **Receipt extraction**: install the Supabase CLI, then
   ```
   supabase login
   supabase link --project-ref <project-ref>
   supabase secrets set ANTHROPIC_API_KEY=sk-ant-...
   supabase functions deploy extract-receipt
   ```
   The Anthropic key comes from https://platform.claude.com. The function uses
   `claude-opus-5`; a receipt costs a fraction of a cent to a few cents.
5. **Point the app at the project**: in `app/config.js` set `SUPABASE_URL` and
   `SUPABASE_ANON_KEY` (Project Settings → API). The anon key is public by design;
   row-level security is what protects the data. Rebuild and push.

## What is stored where

| Data | Where | Who can read |
|---|---|---|
| Cars, records, receipt paths | `cars`, `records` tables | Only the owning user (RLS) |
| Receipt photos | bucket `receipts/<user-id>/...` | Only the owning user |
| Shared price and garage reports | `price_reports` | Nobody directly; only the aggregate functions `community_prices` and `community_garages` (no user id, no plate, no free text; buckets under 3 reports are hidden) |

## Local development

```
supabase start            # local Postgres + auth + storage
supabase db reset         # applies migrations/
supabase functions serve extract-receipt --env-file .env.local
```
