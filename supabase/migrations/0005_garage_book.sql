-- Garage book (phase 1 of the garage side): customers the garage owns, their cars, work orders,
-- and the driver's full history when the driver chose to share it. Run after 0004. Safe to run more than once.
--
-- Whose data is what:
--   garage_customers / garage_cars / work_orders  belong to the garage (its business records).
--   records (the driver's history) belong to the driver; a garage reads them only through garage_car_history()
--   and only when the driver set garage_links.share_history. Prices from other garages are never returned.

-- ---------- consent level 2 on the driver's link ----------
alter table public.garage_links add column if not exists share_history boolean not null default false;
alter table public.garage_links add column if not exists show_garage_names boolean not null default false;

-- ---------- customers and cars the garage keeps ----------
create table if not exists public.garage_customers (
  id uuid primary key default gen_random_uuid(),
  garage_id uuid not null references public.garage_profiles(id) on delete cascade,
  name text not null,
  phone text,
  contact_consent boolean not null default false, -- the garage confirms the customer agreed to reminders
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
  plate text,                       -- digits
  schedule_id text,                 -- null when the model has no schedule yet
  year int,
  km int,
  km_month int not null default 1500,
  km_at timestamptz not null default now(),   -- when km was recorded, for the estimate
  last_service text,                -- YYYY-MM
  test_expiry text,                 -- YYYY-MM-DD
  gov jsonb,
  link_id uuid unique references public.garage_links(id) on delete set null, -- when the driver joined in the app
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
  date text,                        -- YYYY-MM-DD
  items text[] not null default '{}',              -- item keys replaced (data/items.json)
  lines jsonb not null default '[]',               -- [{"type":"part"|"labor","desc":"...","qty":1,"price":120}]
  total int,
  notes text,
  entry_id uuid references public.garage_entries(id) on delete set null, -- sent to the driver for approval
  created_at timestamptz not null default now()
);
create index if not exists work_orders_garage_idx on public.work_orders(garage_id);
create index if not exists work_orders_car_idx on public.work_orders(garage_car_id);

alter table public.garage_customers enable row level security;
alter table public.garage_cars enable row level security;
alter table public.work_orders enable row level security;
-- The owner of a verified garage manages its own book (owns_verified_garage from 0003).
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

-- ---------- a driver joining adds (or connects) the car in the garage book ----------
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

-- When a driver stops sharing, contact details they gave through the app are cleared from customers the app created.
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

-- ---------- what the dashboard reads ----------
-- One row per car in the book. Linked cars take live values from the driver's car (km, km per month, last service,
-- test expiry), and contact details only with consent.
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

-- The driver's history for one car in the book, only when the driver shares it. No prices.
-- verified = entered by a garage and approved by the driver (source 'garage').
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

-- Send a work order to the driver (when the car is linked): it waits in the driver's app for approval.
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
