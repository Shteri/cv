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
   Then Authentication → URL Configuration → Site URL: `https://tipulit.netlify.app/`
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
5. **Garage profiles** (owners claim a licensed garage): run `migrations/0002_garage_profiles.sql`
   in the SQL editor. Then make yourself admin so pending claims show up on your profile screen:
   `update public.profiles set is_admin = true where id = '<your auth user id>';`
   Automatic verification by SMS needs an SMS provider (Authentication → Providers → Phone, e.g. Twilio)
   and the Edge Function: `supabase functions deploy claim-garage`. Until then, claims stay "pending"
   and you approve them from the app after calling the registry phone.
6. **Garage customers** (drivers share a car with a garage, the garage sees who is due): run
   `migrations/0003_garage_customers.sql` in the SQL editor. Nothing else to configure.
   To check the migrations and permissions locally before running them: `sh scripts/test-db.sh`
   (needs Postgres installed; applies every migration to a throwaway database and runs `supabase/tests/rls-*.sql`).
7. **One plate, one account**: run `migrations/0004_plate_lock.sql`. It enables the `http` extension for the
   automatic ownership check against data.gov.il; if the extension is unavailable the check is skipped and
   transfers go through the manual (licence photo) path. Existing duplicate plates: the earliest registration keeps it.
8. **Garage book** (customers the garage owns, work orders, shared history): run `migrations/0005_garage_book.sql`.
9. **Appointments** (calendar per bay, public booking link, extra-work approval link): run
   `migrations/0006_appointments.sql`. The public pages `/book/` and `/approve/` call
   `booking_info`, `book_appointment`, `approval_get` and `approval_decide` without sign-in;
   they never return names or phones of other customers.
10. **Inventory and invoices** (parts, suppliers, purchase orders, stock ledger, Morning invoices): run
    `migrations/0007_inventory_billing.sql`, then deploy the invoicing function:
    `supabase functions deploy issue-document`. Each garage connects its own Morning account in the
    dashboard; the API secret is stored write-only (`billing_save`) and read only by the function.
11. **Modules, job catalog, vehicle inspection**: run `migrations/0008_modules_catalog.sql`
    (garage_profiles.modules and labor_rate, job_templates, inspection results and per-line approval on
    work_approvals via `approval_choose`, public bucket `inspection-photos` written only into the garage's folder).
    The file has no DROP/DELETE statements, so it can also be applied through the Supabase MCP.
12. **AI assist**: run `migrations/0009_ai_usage.sql` (daily counter per user), deploy
    `supabase functions deploy ai-assist`, and add the secret `ANTHROPIC_API_KEY` (Edge Functions → Secrets).
    Until the secret exists the function answers "ai not configured" and the screens say the service is not active.
13. **Point the app at the project**: in `app/config.js` set `SUPABASE_URL` and
   `SUPABASE_ANON_KEY` (Project Settings → API). The anon key is public by design;
   row-level security is what protects the data. Rebuild and push.

## What is stored where

| Data | Where | Who can read |
|---|---|---|
| Cars, records, receipt paths | `cars`, `records` tables | Only the owning user (RLS) |
| Receipt photos | bucket `receipts/<user-id>/...` | Only the owning user |
| Garage profiles | `garage_profiles` | Owner edits; everyone reads rows with status `verified` |
| Garage photos | bucket `garage-photos/<user-id>/...` | Public read, owner writes |
| Driver-garage links | `garage_links` | The driver only. The garage reads a minimal view through `garage_customers()`: car, estimated km inputs, test expiry, and name and phone only if the driver allowed contact |
| Visits a garage logged | `garage_entries` | The driver of that car; the garage writes through `garage_add_entry()` and sees only counts and last visit |
| Garage book | `garage_customers`, `garage_cars`, `work_orders` | The garage that owns them. The driver's own history reaches a garage only through `garage_car_history()`, only with `share_history`, without prices |
| Plate transfer requests | `plate_requests`, bucket `plate-proofs` | The requester and the admin |
| Shared price and garage reports | `price_reports` | Nobody directly; only the aggregate functions `community_prices` and `community_garages` (no user id, no plate, no free text; buckets under 3 reports are hidden) |

## Local development

```
supabase start            # local Postgres + auth + storage
supabase db reset         # applies migrations/
supabase functions serve extract-receipt --env-file .env.local
```
