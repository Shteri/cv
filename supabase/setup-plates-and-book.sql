-- Tipulit: one plate per account (0004) + garage book (0005), in one file for the SQL editor. Safe to run more than once.

do $$ begin
  create extension if not exists http with schema extensions;
exception when others then raise notice 'http extension not available: automatic ownership check disabled (%).', sqlerrm;
end $$;

alter table public.cars add column if not exists plate_claimed_at timestamptz;
alter table public.cars add column if not exists plate_released_at timestamptz;
alter table public.cars add column if not exists released_plate text;

update public.cars set plate = nullif(regexp_replace(plate, '\D', '', 'g'), '') where plate is not null and plate ~ '\D';
update public.cars set plate_claimed_at = created_at where plate is not null and plate_claimed_at is null;

with d as (
  select id, row_number() over (partition by plate order by created_at, id) as rn
  from public.cars where plate is not null
)
update public.cars c set released_plate = c.plate, plate = null, plate_released_at = now()
from d where d.id = c.id and d.rn > 1;

create unique index if not exists cars_plate_unique on public.cars(plate) where plate is not null;

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

create or replace function public.release_plate(p_plate text) returns void
language sql security definer set search_path = '' as $$
  update public.cars set released_plate = plate, plate = null, plate_released_at = now() where plate = p_plate;
$$;

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

create table if not exists public.plate_requests (
  id uuid primary key default gen_random_uuid(),
  plate text not null,
  requester_id uuid not null references auth.users(id) on delete cascade,
  photo_path text,
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

insert into storage.buckets (id, name, public) values ('plate-proofs', 'plate-proofs', false)
on conflict (id) do nothing;
drop policy if exists "plate-proofs: own write" on storage.objects;
create policy "plate-proofs: own write" on storage.objects for insert to authenticated
  with check (bucket_id = 'plate-proofs' and (storage.foldername(name))[1] = (select auth.uid())::text);
drop policy if exists "plate-proofs: own or admin read" on storage.objects;
create policy "plate-proofs: own or admin read" on storage.objects for select to authenticated
  using (bucket_id = 'plate-proofs' and ((storage.foldername(name))[1] = (select auth.uid())::text or public.is_admin()));

alter table public.garage_links add column if not exists share_history boolean not null default false;
alter table public.garage_links add column if not exists show_garage_names boolean not null default false;

create table if not exists public.garage_customers (
  id uuid primary key default gen_random_uuid(),
  garage_id uuid not null references public.garage_profiles(id) on delete cascade,
  name text not null,
  phone text,
  contact_consent boolean not null default false,
  source text not null default 'manual' check (source in ('manual','import','app')),
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists garage_customers_garage_idx on public.garage_customers(garage_id);

create table if not exists public.garage_cars (
  id uuid primary key default gen_random_uuid(),
  garage_id uuid not null references public.garage_profiles(id) on delete cascade,
  customer_id uuid not null references public.garage_customers(id) on delete cascade,
  plate text,
  schedule_id text,
  year int,
  km int,
  km_month int not null default 1500,
  km_at timestamptz not null default now(),
  last_service text,
  test_expiry text,
  gov jsonb,
  link_id uuid unique references public.garage_links(id) on delete set null,
  created_at timestamptz not null default now()
);
create index if not exists garage_cars_garage_idx on public.garage_cars(garage_id);
create index if not exists garage_cars_customer_idx on public.garage_cars(customer_id);
create unique index if not exists garage_cars_plate_idx on public.garage_cars(garage_id, plate) where plate is not null;

create table if not exists public.work_orders (
  id uuid primary key default gen_random_uuid(),
  garage_id uuid not null references public.garage_profiles(id) on delete cascade,
  garage_car_id uuid not null references public.garage_cars(id) on delete cascade,
  kind text not null default 'service' check (kind in ('service','repair')),
  svc_km int,
  km int,
  date text,
  items text[] not null default '{}',
  lines jsonb not null default '[]',
  total int,
  notes text,
  entry_id uuid references public.garage_entries(id) on delete set null,
  created_at timestamptz not null default now()
);
create index if not exists work_orders_garage_idx on public.work_orders(garage_id);
create index if not exists work_orders_car_idx on public.work_orders(garage_car_id);

alter table public.garage_customers enable row level security;
alter table public.garage_cars enable row level security;
alter table public.work_orders enable row level security;
drop policy if exists "garage_customers: owner" on public.garage_customers;
create policy "garage_customers: owner" on public.garage_customers for all to authenticated
  using (public.owns_verified_garage(garage_id)) with check (public.owns_verified_garage(garage_id));
drop policy if exists "garage_cars: owner" on public.garage_cars;
create policy "garage_cars: owner" on public.garage_cars for all to authenticated
  using (public.owns_verified_garage(garage_id))
  with check (public.owns_verified_garage(garage_id)
    and exists (select 1 from public.garage_customers c where c.id = garage_cars.customer_id and c.garage_id = garage_cars.garage_id)
    and (garage_cars.link_id is null or exists (select 1 from public.garage_links l where l.id = garage_cars.link_id and l.garage_id = garage_cars.garage_id)));
drop policy if exists "work_orders: owner" on public.work_orders;
create policy "work_orders: owner" on public.work_orders for all to authenticated
  using (public.owns_verified_garage(garage_id))
  with check (public.owns_verified_garage(garage_id)
    and exists (select 1 from public.garage_cars c where c.id = work_orders.garage_car_id and c.garage_id = work_orders.garage_id));

create or replace function public.garage_links_to_book() returns trigger
language plpgsql security definer set search_path = '' as $$
declare v_car record; v_gc uuid; v_cust uuid;
begin
  select plate, schedule_id, year, km, km_month, last_service, gov into v_car from public.cars where id = new.car_id;
  select id into v_gc from public.garage_cars where garage_id = new.garage_id and plate is not null and plate = v_car.plate;
  if v_gc is not null then
    update public.garage_cars set link_id = new.id where id = v_gc and link_id is null;
  else
    insert into public.garage_customers (garage_id, name, phone, contact_consent, source)
    values (new.garage_id, coalesce(nullif(new.first_name, ''), 'לקוח מהאפליקציה'), new.phone, new.allow_contact, 'app')
    returning id into v_cust;
    insert into public.garage_cars (garage_id, customer_id, plate, schedule_id, year, km, km_month, last_service, test_expiry, gov, link_id)
    values (new.garage_id, v_cust, v_car.plate, v_car.schedule_id, v_car.year, v_car.km, coalesce(v_car.km_month, 1500), v_car.last_service, v_car.gov->>'test_expiry', v_car.gov, new.id);
  end if;
  return new;
end $$;
drop trigger if exists garage_links_to_book on public.garage_links;
create trigger garage_links_to_book after insert on public.garage_links
  for each row execute function public.garage_links_to_book();

create or replace function public.garage_links_revoked() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  update public.garage_customers c set phone = null, contact_consent = false
  from public.garage_cars gc where gc.link_id = old.id and gc.customer_id = c.id and c.source = 'app';
  return old;
end $$;
drop trigger if exists garage_links_revoked on public.garage_links;
create trigger garage_links_revoked before delete on public.garage_links
  for each row execute function public.garage_links_revoked();

create or replace function public.garage_book(p_garage uuid)
returns table (car_id uuid, customer_id uuid, name text, phone text, can_contact boolean, source text, notes text,
               plate text, schedule_id text, year int, km int, km_month int, km_at timestamptz, last_service text, test_expiry text,
               linked boolean, share_history boolean, last_visit text, visits int, pending int, created_at timestamptz)
language plpgsql security definer set search_path = '' stable as $$
begin
  if not public.owns_verified_garage(p_garage) then raise exception 'not allowed'; end if;
  return query
  select gc.id, cu.id, cu.name,
         case when l.id is not null and l.allow_contact then coalesce(l.phone, cu.phone) when cu.contact_consent then cu.phone end,
         coalesce(l.allow_contact, cu.contact_consent), cu.source, cu.notes,
         gc.plate, coalesce(c.schedule_id, gc.schedule_id), coalesce(c.year, gc.year),
         case when c.id is not null and (c.updated_at > gc.km_at or gc.km is null) then c.km else gc.km end,
         coalesce(c.km_month, gc.km_month),
         case when c.id is not null and (c.updated_at > gc.km_at or gc.km is null) then c.updated_at else gc.km_at end,
         greatest(c.last_service, gc.last_service), coalesce(c.gov->>'test_expiry', gc.test_expiry),
         l.id is not null, coalesce(l.share_history, false),
         (select max(w.date) from public.work_orders w where w.garage_car_id = gc.id),
         (select count(*)::int from public.work_orders w where w.garage_car_id = gc.id),
         (select count(*)::int from public.garage_entries e where e.garage_id = p_garage and l.car_id is not null and e.car_id = l.car_id and e.status = 'pending'),
         gc.created_at
  from public.garage_cars gc
  join public.garage_customers cu on cu.id = gc.customer_id
  left join public.garage_links l on l.id = gc.link_id
  left join public.cars c on c.id = l.car_id
  where gc.garage_id = p_garage
  order by cu.name;
end $$;

create or replace function public.garage_car_history(p_garage_car uuid)
returns table (date text, km int, kind text, svc_km int, items text[], text text, garage text, verified boolean, own boolean)
language plpgsql security definer set search_path = '' stable as $$
declare v_gc record; v_link record; v_name text;
begin
  select garage_id, link_id into v_gc from public.garage_cars where id = p_garage_car;
  if v_gc.garage_id is null or not public.owns_verified_garage(v_gc.garage_id) then raise exception 'not allowed'; end if;
  select car_id, share_history, show_garage_names into v_link from public.garage_links where id = v_gc.link_id;
  if v_link.car_id is null or not v_link.share_history then return; end if;
  select name into v_name from public.garage_profiles where id = v_gc.garage_id;
  return query
  select r.date, r.km, r.kind, r.svc_km, r.items, r.text,
         case when r.garage is null or r.garage = '' then null
              when r.garage = v_name then r.garage
              when v_link.show_garage_names then r.garage else 'מוסך אחר' end,
         r.source = 'garage', coalesce(r.garage = v_name, false)
  from public.records r
  where r.car_id = v_link.car_id
  order by r.km desc nulls last, r.created_at desc;
end $$;

create or replace function public.work_order_send(p_work_order uuid, p_where text)
returns uuid language plpgsql security definer set search_path = '' as $$
declare v_wo record; v_car uuid; v_id uuid;
begin
  select w.id, w.garage_id, w.kind, w.svc_km, w.km, w.date, w.total, w.notes, w.entry_id, gc.link_id into v_wo
  from public.work_orders w join public.garage_cars gc on gc.id = w.garage_car_id where w.id = p_work_order;
  if v_wo.id is null or not public.owns_verified_garage(v_wo.garage_id) then raise exception 'not allowed'; end if;
  if v_wo.entry_id is not null then return v_wo.entry_id; end if;
  select car_id into v_car from public.garage_links where id = v_wo.link_id;
  if v_car is null then raise exception 'not linked'; end if;
  insert into public.garage_entries (garage_id, car_id, kind, svc_km, km, date, price, text, "where")
  values (v_wo.garage_id, v_car, v_wo.kind, v_wo.svc_km, coalesce(v_wo.km, 0), left(v_wo.date, 7), v_wo.total, nullif(left(v_wo.notes, 500), ''),
          case when p_where in ('importer','independent') then p_where else 'independent' end)
  returning id into v_id;
  update public.work_orders set entry_id = v_id where id = v_wo.id;
  return v_id;
end $$;

revoke execute on function public.garage_links_to_book() from public, anon, authenticated;
revoke execute on function public.garage_links_revoked() from public, anon, authenticated;
revoke execute on function public.garage_book(uuid) from public, anon;
grant execute on function public.garage_book(uuid) to authenticated;
revoke execute on function public.garage_car_history(uuid) from public, anon;
grant execute on function public.garage_car_history(uuid) to authenticated;
revoke execute on function public.work_order_send(uuid, text) from public, anon;
grant execute on function public.work_order_send(uuid, text) to authenticated;

