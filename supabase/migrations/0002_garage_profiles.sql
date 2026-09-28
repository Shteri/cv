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
create policy "garage_profiles: owner all" on public.garage_profiles
  for all to authenticated using ((select auth.uid()) = owner_id) with check ((select auth.uid()) = owner_id);
-- Everyone can read verified profiles (business data, shown in the app).
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
create policy "garage-photos: public read" on storage.objects for select to anon, authenticated
  using (bucket_id = 'garage-photos');
create policy "garage-photos: own folder write" on storage.objects for insert to authenticated
  with check (bucket_id = 'garage-photos' and (storage.foldername(name))[1] = (select auth.uid())::text);
create policy "garage-photos: own folder update" on storage.objects for update to authenticated
  using (bucket_id = 'garage-photos' and (storage.foldername(name))[1] = (select auth.uid())::text);
create policy "garage-photos: own folder delete" on storage.objects for delete to authenticated
  using (bucket_id = 'garage-photos' and (storage.foldername(name))[1] = (select auth.uid())::text);
