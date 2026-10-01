-- One plate, one account. A plate linked to a car in one account cannot be linked in another.
-- When a car is sold, the new owner takes the plate over:
--   automatically, when the Ministry of Transport ownership history (data.gov.il) shows an ownership change
--   after the current holder registered the plate; otherwise
--   manually, by sending a photo of the vehicle licence that the admin approves.
-- The previous holder keeps the car and its history; only the plate is released.
-- Safe to run more than once.

-- HTTP from SQL, for the ownership check (Supabase ships the pgsql-http extension).
do $$ begin
  create extension if not exists http with schema extensions;
exception when others then raise notice 'http extension not available: automatic ownership check disabled (%).', sqlerrm;
end $$;

alter table public.cars add column if not exists plate_claimed_at timestamptz;
alter table public.cars add column if not exists plate_released_at timestamptz;
alter table public.cars add column if not exists released_plate text;

-- digits only, one format everywhere
update public.cars set plate = nullif(regexp_replace(plate, '\D', '', 'g'), '') where plate is not null and plate ~ '\D';
update public.cars set plate_claimed_at = created_at where plate is not null and plate_claimed_at is null;

-- Existing duplicates (before this rule): the earliest registration keeps the plate, later ones are released.
with d as (
  select id, row_number() over (partition by plate order by created_at, id) as rn
  from public.cars where plate is not null
)
update public.cars c set released_plate = c.plate, plate = null, plate_released_at = now()
from d where d.id = c.id and d.rn > 1;

create unique index if not exists cars_plate_unique on public.cars(plate) where plate is not null;

-- Normalize the plate and stamp when it was claimed (the app upserts the same plate on every sync; that keeps the stamp).
create or replace function public.cars_plate_guard() returns trigger
language plpgsql set search_path = '' as $$
begin
  new.plate := nullif(regexp_replace(coalesce(new.plate, ''), '\D', '', 'g'), '');
  if tg_op = 'INSERT' or new.plate is distinct from old.plate then
    new.plate_claimed_at := case when new.plate is null then null else now() end;
  end if;
  return new;
end $$;
drop trigger if exists cars_plate_guard on public.cars;
create trigger cars_plate_guard before insert or update of plate on public.cars
  for each row execute function public.cars_plate_guard();

-- free | mine | taken, for the signed-in caller. Never says who holds it.
create or replace function public.plate_status(p_plate text) returns text
language plpgsql security definer set search_path = '' stable as $$
declare v_plate text := regexp_replace(coalesce(p_plate, ''), '\D', '', 'g'); v_owner uuid;
begin
  if (select auth.uid()) is null then raise exception 'not allowed'; end if;
  select user_id into v_owner from public.cars where plate = v_plate;
  if v_owner is null then return 'free'; end if;
  if v_owner = (select auth.uid()) then return 'mine'; end if;
  return 'taken';
end $$;

-- Month (YYYYMM) of the latest ownership change in the MoT registry, or null when unknown.
-- Dataset "היסטוריית כלי רכב פרטיים", resource bb2355dc-...: one row per ownership period (baalut_dt).
create or replace function public.registry_owner_month(p_plate text) returns int
language plpgsql security definer set search_path = '' as $$
declare v_res record; v_url text;
begin
  v_url := 'https://data.gov.il/api/3/action/datastore_search?resource_id=bb2355dc-9ec7-4f06-9c3f-3344672171da'
        || '&filters=%7B%22mispar_rechev%22%3A' || regexp_replace(p_plate, '\D', '', 'g') || '%7D&sort=baalut_dt%20desc&limit=1';
  execute 'select status, content from extensions.http_get($1)' into v_res using v_url;
  if v_res.status <> 200 then return null; end if;
  return nullif((v_res.content::jsonb -> 'result' -> 'records' -> 0 ->> 'baalut_dt'), '')::int;
exception when others then return null;
end $$;

-- Release a plate from its current holder (internal).
create or replace function public.release_plate(p_plate text) returns void
language sql security definer set search_path = '' as $$
  update public.cars set released_plate = plate, plate = null, plate_released_at = now() where plate = p_plate;
$$;

-- The caller says they bought the car. Returns: free | mine | released | unverified | bad.
create or replace function public.claim_plate(p_plate text) returns text
language plpgsql security definer set search_path = '' as $$
declare v_plate text := regexp_replace(coalesce(p_plate, ''), '\D', '', 'g'); v_car record; v_month int;
begin
  if (select auth.uid()) is null then raise exception 'not allowed'; end if;
  if length(v_plate) not between 7 and 8 then return 'bad'; end if;
  select user_id, plate_claimed_at into v_car from public.cars where plate = v_plate;
  if v_car.user_id is null then return 'free'; end if;
  if v_car.user_id = (select auth.uid()) then return 'mine'; end if;
  v_month := public.registry_owner_month(v_plate);
  if v_month is not null and v_month > to_char(v_car.plate_claimed_at at time zone 'Asia/Jerusalem', 'YYYYMM')::int then
    perform public.release_plate(v_plate);
    return 'released';
  end if;
  return 'unverified';
end $$;

-- ---------- manual path: licence photo, approved by the admin ----------
create table if not exists public.plate_requests (
  id uuid primary key default gen_random_uuid(),
  plate text not null,
  requester_id uuid not null references auth.users(id) on delete cascade,
  photo_path text,                         -- object path in bucket plate-proofs
  note text,
  status text not null default 'pending' check (status in ('pending','approved','rejected')),
  created_at timestamptz not null default now(),
  decided_at timestamptz
);
create index if not exists plate_requests_requester_idx on public.plate_requests(requester_id);
create index if not exists plate_requests_pending_idx on public.plate_requests(created_at) where status = 'pending';
alter table public.plate_requests enable row level security;
drop policy if exists "plate_requests: own select" on public.plate_requests;
create policy "plate_requests: own select" on public.plate_requests for select to authenticated
  using ((select auth.uid()) = requester_id);
drop policy if exists "plate_requests: own insert" on public.plate_requests;
create policy "plate_requests: own insert" on public.plate_requests for insert to authenticated
  with check ((select auth.uid()) = requester_id and status = 'pending');

create or replace function public.is_admin() returns boolean
language sql security definer set search_path = '' stable as $$
  select coalesce((select is_admin from public.profiles where id = (select auth.uid())), false);
$$;

create or replace function public.pending_plate_requests()
returns table (id uuid, plate text, photo_path text, note text, requester_email text, holder_since timestamptz, created_at timestamptz)
language sql security definer set search_path = '' stable as $$
  select r.id, r.plate, r.photo_path, r.note, u.email, c.plate_claimed_at, r.created_at
  from public.plate_requests r join auth.users u on u.id = r.requester_id
  left join public.cars c on c.plate = r.plate
  where r.status = 'pending' and public.is_admin()
  order by r.created_at;
$$;

create or replace function public.decide_plate_request(p_id uuid, p_approve boolean) returns void
language plpgsql security definer set search_path = '' as $$
declare v_plate text;
begin
  if not public.is_admin() then raise exception 'not allowed'; end if;
  update public.plate_requests set status = case when p_approve then 'approved' else 'rejected' end, decided_at = now()
  where id = p_id and status = 'pending' returning plate into v_plate;
  if v_plate is null then raise exception 'not found'; end if;
  if p_approve then perform public.release_plate(v_plate); end if;
end $$;

revoke execute on function public.plate_status(text) from public, anon;
grant execute on function public.plate_status(text) to authenticated;
revoke execute on function public.claim_plate(text) from public, anon;
grant execute on function public.claim_plate(text) to authenticated;
revoke execute on function public.registry_owner_month(text) from public, anon, authenticated;
revoke execute on function public.release_plate(text) from public, anon, authenticated;
revoke execute on function public.cars_plate_guard() from public, anon, authenticated;
revoke execute on function public.is_admin() from public, anon;
grant execute on function public.is_admin() to authenticated;
revoke execute on function public.pending_plate_requests() from public, anon;
grant execute on function public.pending_plate_requests() to authenticated;
revoke execute on function public.decide_plate_request(uuid, boolean) from public, anon;
grant execute on function public.decide_plate_request(uuid, boolean) to authenticated;

-- licence photos: private; the requester writes to their own folder, the admin reads
insert into storage.buckets (id, name, public) values ('plate-proofs', 'plate-proofs', false)
on conflict (id) do nothing;
drop policy if exists "plate-proofs: own write" on storage.objects;
create policy "plate-proofs: own write" on storage.objects for insert to authenticated
  with check (bucket_id = 'plate-proofs' and (storage.foldername(name))[1] = (select auth.uid())::text);
drop policy if exists "plate-proofs: own or admin read" on storage.objects;
create policy "plate-proofs: own or admin read" on storage.objects for select to authenticated
  using (bucket_id = 'plate-proofs' and ((storage.foldername(name))[1] = (select auth.uid())::text or public.is_admin()));
