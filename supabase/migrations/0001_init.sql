-- Tipulit backend, first migration. Run in the Supabase SQL editor or with `supabase db push`.
-- Tables: profiles (one per auth user), cars (per user), records (services, repairs, documents),
-- price_reports (anonymized copies of shared records, the community data).
-- Storage bucket: receipts (private, per-user folders).

create extension if not exists "pgcrypto";

-- ---------- profiles ----------
create table if not exists public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  created_at timestamptz not null default now()
);
alter table public.profiles enable row level security;
create policy "profiles: own row" on public.profiles
  for all using (auth.uid() = id) with check (auth.uid() = id);

create or replace function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, display_name)
  values (new.id, coalesce(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name'))
  on conflict (id) do nothing;
  return new;
end $$;
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();

-- ---------- cars ----------
create table if not exists public.cars (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  plate text,                      -- digits only, e.g. 1234567
  schedule_id text not null,       -- data/schedules/<id>.json
  year int,
  km int not null default 0,
  km_month int not null default 1500,
  last_service text,               -- YYYY-MM
  gov jsonb,                       -- normalized registry record (make, name, test expiry, ...)
  updated_at timestamptz not null default now(),
  created_at timestamptz not null default now()
);
create index if not exists cars_user_idx on public.cars(user_id);
alter table public.cars enable row level security;
create policy "cars: own rows" on public.cars
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- ---------- records ----------
create table if not exists public.records (
  id uuid primary key default gen_random_uuid(),
  car_id uuid not null references public.cars(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  kind text not null check (kind in ('service','repair','other')),
  svc_km int,                      -- scheduled service km when kind = service
  text text,                       -- free description (repairs)
  items text[] not null default '{}', -- item keys replaced (data/items.json)
  date text,                       -- YYYY-MM
  km int not null,
  "where" text check ("where" in ('importer','independent','self')),
  garage text,
  city text,
  price int,
  back text check (back in ('yes','no')),
  extra text,
  receipt_paths text[] not null default '{}', -- storage object paths in bucket receipts
  share boolean not null default false,
  source text not null default 'log',
  client_id text,                  -- id from the device, for idempotent sync
  created_at timestamptz not null default now(),
  unique (car_id, client_id)
);
create index if not exists records_car_idx on public.records(car_id);
alter table public.records enable row level security;
create policy "records: own rows" on public.records
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- ---------- community: anonymized price and garage reports ----------
-- Copied from records with share = true. No user id, no plate, no free text.
create table if not exists public.price_reports (
  id uuid primary key default gen_random_uuid(),
  record_id uuid unique references public.records(id) on delete cascade,
  schedule_id text not null,
  svc_km int,
  kind text not null,
  items text[] not null default '{}',
  "where" text,
  garage text,
  city text,
  price int,
  back text,
  verified boolean not null default false, -- true when a receipt was attached
  reported_at timestamptz not null default now()
);
create index if not exists price_reports_sched_idx on public.price_reports(schedule_id, svc_km);
alter table public.price_reports enable row level security;
-- Nobody reads rows directly; aggregates are exposed through the functions below.

create or replace function public.sync_price_report() returns trigger
language plpgsql security definer set search_path = public as $$
declare sched text;
begin
  select schedule_id into sched from public.cars where id = new.car_id;
  if new.share and new.price is not null then
    insert into public.price_reports (record_id, schedule_id, svc_km, kind, items, "where", garage, city, price, back, verified)
    values (new.id, sched, new.svc_km, new.kind, new.items, new."where", nullif(new.garage,''), nullif(new.city,''), new.price, new.back, cardinality(new.receipt_paths) > 0)
    on conflict (record_id) do update set svc_km = excluded.svc_km, items = excluded.items, "where" = excluded."where",
      garage = excluded.garage, city = excluded.city, price = excluded.price, back = excluded.back, verified = excluded.verified;
  else
    delete from public.price_reports where record_id = new.id;
  end if;
  return new;
end $$;
drop trigger if exists records_sync_price_report on public.records;
create trigger records_sync_price_report after insert or update on public.records
  for each row execute function public.sync_price_report();

-- Median and quartiles per garage type for one scheduled service. Buckets under 3 reports are hidden.
create or replace function public.community_prices(p_schedule_id text, p_svc_km int)
returns table ("where" text, n bigint, p25 numeric, med numeric, p75 numeric, verified bigint, latest timestamptz)
language sql security definer set search_path = public stable as $$
  select "where", count(*) as n,
         percentile_cont(0.25) within group (order by price) as p25,
         percentile_cont(0.5)  within group (order by price) as med,
         percentile_cont(0.75) within group (order by price) as p75,
         count(*) filter (where verified) as verified,
         max(reported_at) as latest
  from public.price_reports
  where schedule_id = p_schedule_id and svc_km = p_svc_km and kind = 'service' and "where" in ('importer','independent')
  group by "where"
  having count(*) >= 3;
$$;

-- Garages other drivers of the same model reported. Needs a name; grouped by name + city.
create or replace function public.community_garages(p_schedule_id text)
returns table (garage text, city text, "where" text, n bigint, avg_price numeric, back_pct numeric, latest timestamptz)
language sql security definer set search_path = public stable as $$
  select garage, coalesce(city,'') as city, "where", count(*) as n,
         round(avg(price)) as avg_price,
         round(100.0 * count(*) filter (where back = 'yes') / nullif(count(*) filter (where back is not null), 0)) as back_pct,
         max(reported_at) as latest
  from public.price_reports
  where schedule_id = p_schedule_id and garage is not null and "where" in ('importer','independent')
  group by garage, coalesce(city,''), "where"
  order by back_pct desc nulls last, n desc
  limit 50;
$$;

grant execute on function public.community_prices(text, int) to anon, authenticated;
grant execute on function public.community_garages(text) to anon, authenticated;

-- ---------- storage: receipts ----------
insert into storage.buckets (id, name, public) values ('receipts', 'receipts', false)
on conflict (id) do nothing;
create policy "receipts: own folder read" on storage.objects for select
  using (bucket_id = 'receipts' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "receipts: own folder write" on storage.objects for insert
  with check (bucket_id = 'receipts' and (storage.foldername(name))[1] = auth.uid()::text);
create policy "receipts: own folder delete" on storage.objects for delete
  using (bucket_id = 'receipts' and (storage.foldername(name))[1] = auth.uid()::text);
