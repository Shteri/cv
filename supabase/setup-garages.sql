-- Tipulit: garage profiles + garage customers (migrations 0002 and 0003 in one file).
-- Safe to run more than once: tables, indexes and functions are created if missing, policies are replaced.
-- Paste into Supabase -> SQL Editor -> New query -> Run.

-- ===== 0002_garage_profiles.sql =====
-- Garage profiles: a licensed garage (from the MoT registry bundled in the app) claimed by its owner.
-- Run after 0001_init.sql in the Supabase SQL editor.
-- Statuses: pending (claimed, not yet verified), verified (phone matched the registry, or an admin approved), rejected.

alter table public.profiles add column if not exists is_admin boolean not null default false;

create table if not exists public.garage_profiles (
  id uuid primary key default gen_random_uuid(),
  garage_id int not null,                      -- mispar_mosah in the registry (data/garages.json)
  owner_id uuid not null references auth.users(id) on delete cascade,
  name text not null,
  city text not null,
  address text,
  phone text,                                  -- phone shown to drivers (defaults to the registry phone)
  registry_phone text,                         -- registry phone at claim time, for the manual check
  whatsapp text,
  booking_url text,
  about text,
  makes text[] not null default '{}',          -- brands the garage specializes in (Hebrew names as in data/models.json)
  services text[] not null default '{}',       -- mech | elec | ac | body | tires | test
  hours jsonb not null default '{}',           -- {"0":{"open":"08:00","close":"17:00"}, ..., "6":null}; 0 = Sunday
  prices jsonb not null default '[]',          -- [{"label":"טיפול קטן","price":450}]
  photos text[] not null default '{}',         -- object paths in bucket garage-photos
  status text not null default 'pending' check (status in ('pending','verified','rejected')),
  verified_via text,                           -- phone | admin
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (garage_id, owner_id)
);
create index if not exists garage_profiles_city_idx on public.garage_profiles(city) where status = 'verified';
create index if not exists garage_profiles_owner_idx on public.garage_profiles(owner_id);
alter table public.garage_profiles enable row level security;

-- Owners manage their own rows. Status is protected by the trigger below.
drop policy if exists "garage_profiles: owner all" on public.garage_profiles;
create policy "garage_profiles: owner all" on public.garage_profiles
  for all to authenticated using ((select auth.uid()) = owner_id) with check ((select auth.uid()) = owner_id);
-- Everyone can read verified profiles (business data, shown in the app).
drop policy if exists "garage_profiles: public read verified" on public.garage_profiles;
create policy "garage_profiles: public read verified" on public.garage_profiles
  for select to anon, authenticated using (status = 'verified');

-- Owners cannot set their own status; only the functions below (security definer) can.
create or replace function public.garage_profiles_guard() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  new.updated_at := now();
  if tg_op = 'INSERT' then
    new.status := 'pending'; new.verified_via := null;
  elsif new.status is distinct from old.status or new.verified_via is distinct from old.verified_via then
    if coalesce(current_setting('tipulit.allow_status', true), '') <> 'on' then
      new.status := old.status; new.verified_via := old.verified_via;
    end if;
  end if;
  return new;
end $$;
drop trigger if exists garage_profiles_guard on public.garage_profiles;
create trigger garage_profiles_guard before insert or update on public.garage_profiles
  for each row execute function public.garage_profiles_guard();

-- Admin approval (the project owner: update public.profiles set is_admin = true where id = '<uid>').
create or replace function public.set_garage_status(p_id uuid, p_status text)
returns void language plpgsql security definer set search_path = '' as $$
begin
  if not coalesce((select is_admin from public.profiles where id = (select auth.uid())), false) then
    raise exception 'not allowed';
  end if;
  if p_status not in ('pending','verified','rejected') then raise exception 'bad status'; end if;
  perform set_config('tipulit.allow_status', 'on', true);
  update public.garage_profiles set status = p_status, verified_via = case when p_status = 'verified' then 'admin' else null end where id = p_id;
end $$;

-- Automatic verification: the signed-in user confirmed (via SMS OTP) the phone number the registry lists for the garage.
-- The registry phone is passed by the claim-garage Edge Function, which reads it from the published garages.json,
-- so it cannot be spoofed by the client. Called with the service role only.
create or replace function public.verify_garage_by_phone(p_id uuid, p_registry_phone text)
returns boolean language plpgsql security definer set search_path = '' as $$
declare v_owner uuid; v_phone text;
begin
  select owner_id into v_owner from public.garage_profiles where id = p_id;
  if v_owner is null then return false; end if;
  select phone into v_phone from auth.users where id = v_owner and phone_confirmed_at is not null;
  if v_phone is null then return false; end if;
  if regexp_replace(v_phone, '\D', '', 'g') not like '%' || right(regexp_replace(p_registry_phone, '\D', '', 'g'), 9) then return false; end if;
  perform set_config('tipulit.allow_status', 'on', true);
  update public.garage_profiles set status = 'verified', verified_via = 'phone' where id = p_id;
  return true;
end $$;

revoke execute on function public.set_garage_status(uuid, text) from public;
grant execute on function public.set_garage_status(uuid, text) to authenticated;
revoke execute on function public.verify_garage_by_phone(uuid, text) from public, anon, authenticated;
revoke execute on function public.garage_profiles_guard() from public, anon, authenticated;

-- Pending claims for the admin (name, city, phones side by side).
create or replace function public.pending_garage_claims()
returns table (id uuid, garage_id int, name text, city text, registry_phone text, phone text, owner_email text, created_at timestamptz)
language sql security definer set search_path = '' stable as $$
  select g.id, g.garage_id, g.name, g.city, g.registry_phone, g.phone, u.email, g.created_at
  from public.garage_profiles g join auth.users u on u.id = g.owner_id
  where g.status = 'pending' and coalesce((select is_admin from public.profiles where id = (select auth.uid())), false)
  order by g.created_at;
$$;
revoke execute on function public.pending_garage_claims() from public;
grant execute on function public.pending_garage_claims() to authenticated;

-- ---------- storage: garage photos (public read, owner writes to own folder) ----------
insert into storage.buckets (id, name, public) values ('garage-photos', 'garage-photos', true)
on conflict (id) do nothing;
drop policy if exists "garage-photos: public read" on storage.objects;
create policy "garage-photos: public read" on storage.objects for select to anon, authenticated
  using (bucket_id = 'garage-photos');
drop policy if exists "garage-photos: own folder write" on storage.objects;
create policy "garage-photos: own folder write" on storage.objects for insert to authenticated
  with check (bucket_id = 'garage-photos' and (storage.foldername(name))[1] = (select auth.uid())::text);
drop policy if exists "garage-photos: own folder update" on storage.objects;
create policy "garage-photos: own folder update" on storage.objects for update to authenticated
  using (bucket_id = 'garage-photos' and (storage.foldername(name))[1] = (select auth.uid())::text);
drop policy if exists "garage-photos: own folder delete" on storage.objects;
create policy "garage-photos: own folder delete" on storage.objects for delete to authenticated
  using (bucket_id = 'garage-photos' and (storage.foldername(name))[1] = (select auth.uid())::text);

-- ===== 0003_garage_customers.sql =====
-- Garage customers: a driver links a car to a verified garage (with consent), the garage sees a minimal
-- view of linked cars (next service, test expiry, contact if allowed), and can log a visit that the driver
-- approves before it enters their history. Run after 0002_garage_profiles.sql.

-- ---------- links (driver-owned consent) ----------
create table if not exists public.garage_links (
  id uuid primary key default gen_random_uuid(),
  garage_id uuid not null references public.garage_profiles(id) on delete cascade,
  car_id uuid not null references public.cars(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,  -- the driver
  first_name text,
  phone text,
  allow_contact boolean not null default false,  -- may the garage call or WhatsApp about service
  created_at timestamptz not null default now(),
  unique (garage_id, car_id)
);
create index if not exists garage_links_garage_idx on public.garage_links(garage_id);
create index if not exists garage_links_car_idx on public.garage_links(car_id);
create index if not exists garage_links_user_idx on public.garage_links(user_id);
alter table public.garage_links enable row level security;

-- The driver reads, changes and deletes (= revokes) their own links. Garages never read this table directly.
drop policy if exists "garage_links: driver select" on public.garage_links;
create policy "garage_links: driver select" on public.garage_links for select to authenticated
  using ((select auth.uid()) = user_id);
drop policy if exists "garage_links: driver insert" on public.garage_links;
create policy "garage_links: driver insert" on public.garage_links for insert to authenticated
  with check (
    (select auth.uid()) = user_id
    and exists (select 1 from public.cars c where c.id = garage_links.car_id and c.user_id = (select auth.uid()))
    and exists (select 1 from public.garage_profiles g where g.id = garage_links.garage_id and g.status = 'verified')
  );
drop policy if exists "garage_links: driver update" on public.garage_links;
create policy "garage_links: driver update" on public.garage_links for update to authenticated
  using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
drop policy if exists "garage_links: driver delete" on public.garage_links;
create policy "garage_links: driver delete" on public.garage_links for delete to authenticated
  using ((select auth.uid()) = user_id);

-- ---------- entries a garage logs for a customer (pending until the driver decides) ----------
create table if not exists public.garage_entries (
  id uuid primary key default gen_random_uuid(),
  garage_id uuid not null references public.garage_profiles(id) on delete cascade,
  car_id uuid not null references public.cars(id) on delete cascade,
  kind text not null check (kind in ('service','repair')),
  svc_km int,
  km int not null,
  date text,                                   -- YYYY-MM
  price int,
  text text,
  "where" text check ("where" in ('importer','independent')),
  status text not null default 'pending' check (status in ('pending','accepted','rejected')),
  created_at timestamptz not null default now(),
  decided_at timestamptz
);
create index if not exists garage_entries_garage_idx on public.garage_entries(garage_id);
create index if not exists garage_entries_car_idx on public.garage_entries(car_id) where status = 'pending';
alter table public.garage_entries enable row level security;
-- The driver sees entries for their cars. Writes go through the functions below only.
drop policy if exists "garage_entries: driver select" on public.garage_entries;
create policy "garage_entries: driver select" on public.garage_entries for select to authenticated
  using (exists (select 1 from public.cars c where c.id = garage_entries.car_id and c.user_id = (select auth.uid())));

-- Caller owns this garage profile and it is verified.
create or replace function public.owns_verified_garage(p_garage uuid) returns boolean
language sql security definer set search_path = '' stable as $$
  select exists (select 1 from public.garage_profiles g where g.id = p_garage and g.owner_id = (select auth.uid()) and g.status = 'verified');
$$;

-- What a garage sees about its customers. Contact details only when the driver allowed contact.
-- No records, receipts or visits to other garages.
create or replace function public.garage_customers(p_garage uuid)
returns table (link_id uuid, first_name text, phone text, allow_contact boolean, plate text, schedule_id text, year int,
               km int, km_month int, last_service text, test_expiry text, car_updated_at timestamptz,
               linked_at timestamptz, last_visit timestamptz, pending int)
language plpgsql security definer set search_path = '' stable as $$
begin
  if not public.owns_verified_garage(p_garage) then raise exception 'not allowed'; end if;
  return query
  select l.id, l.first_name, case when l.allow_contact then l.phone end, l.allow_contact, c.plate, c.schedule_id, c.year,
         c.km, c.km_month, c.last_service, c.gov->>'test_expiry', c.updated_at, l.created_at,
         (select max(e.created_at) from public.garage_entries e where e.garage_id = p_garage and e.car_id = c.id and e.status = 'accepted'),
         (select count(*)::int from public.garage_entries e where e.garage_id = p_garage and e.car_id = c.id and e.status = 'pending')
  from public.garage_links l join public.cars c on c.id = l.car_id
  where l.garage_id = p_garage
  order by l.created_at desc;
end $$;

-- The garage logs a visit for a linked customer. It waits for the driver's approval.
create or replace function public.garage_add_entry(p_link uuid, p_kind text, p_svc_km int, p_km int, p_date text, p_price int, p_text text, p_where text)
returns uuid language plpgsql security definer set search_path = '' as $$
declare v_garage uuid; v_car uuid; v_id uuid;
begin
  select garage_id, car_id into v_garage, v_car from public.garage_links where id = p_link;
  if v_garage is null or not public.owns_verified_garage(v_garage) then raise exception 'not allowed'; end if;
  if p_km is null or p_km < 0 or p_km > 2000000 then raise exception 'bad km'; end if;
  insert into public.garage_entries (garage_id, car_id, kind, svc_km, km, date, price, text, "where")
  values (v_garage, v_car, p_kind, p_svc_km, p_km, nullif(p_date, ''), p_price, nullif(left(p_text, 500), ''), p_where)
  returning id into v_id;
  return v_id;
end $$;

-- The driver accepts or rejects an entry. Accepting does not copy anything: the app adds the record to the
-- car's history (so it goes through the normal sync) and then calls this.
create or replace function public.decide_garage_entry(p_id uuid, p_accept boolean)
returns void language plpgsql security definer set search_path = '' as $$
begin
  update public.garage_entries e set status = case when p_accept then 'accepted' else 'rejected' end, decided_at = now()
  where e.id = p_id and e.status = 'pending'
    and exists (select 1 from public.cars c where c.id = e.car_id and c.user_id = (select auth.uid()));
  if not found then raise exception 'not allowed'; end if;
end $$;

revoke execute on function public.owns_verified_garage(uuid) from public, anon;
revoke execute on function public.garage_customers(uuid) from public, anon;
revoke execute on function public.garage_add_entry(uuid, text, int, int, text, int, text, text) from public, anon;
revoke execute on function public.decide_garage_entry(uuid, boolean) from public, anon;
grant execute on function public.owns_verified_garage(uuid) to authenticated;
grant execute on function public.garage_customers(uuid) to authenticated;
grant execute on function public.garage_add_entry(uuid, text, int, int, text, int, text, text) to authenticated;
grant execute on function public.decide_garage_entry(uuid, boolean) to authenticated;
