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
create policy "garage_links: driver select" on public.garage_links for select to authenticated
  using ((select auth.uid()) = user_id);
create policy "garage_links: driver insert" on public.garage_links for insert to authenticated
  with check (
    (select auth.uid()) = user_id
    and exists (select 1 from public.cars c where c.id = garage_links.car_id and c.user_id = (select auth.uid()))
    and exists (select 1 from public.garage_profiles g where g.id = garage_links.garage_id and g.status = 'verified')
  );
create policy "garage_links: driver update" on public.garage_links for update to authenticated
  using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
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
