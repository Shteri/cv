-- Garage side, phase 3: parts inventory, suppliers, purchase orders, stock used by work orders, invoices.
-- Run after 0006. Safe to run more than once.
--
-- Stock is a ledger: every change is a row in stock_moves and a trigger keeps parts.stock in step.
--   receive  a purchase order arrived (po_receive)
--   use      a work order used the part (wo_consume, re-run on every save of the work order)
--   adjust   a count or a correction by hand
-- Invoices are issued by the garage's invoicing provider (Morning) through the issue-document edge function,
-- or recorded by hand when the garage issues them elsewhere. The provider secret is write-only for the client.

-- ---------- suppliers ----------
create table if not exists public.suppliers (
  id uuid primary key default gen_random_uuid(),
  garage_id uuid not null references public.garage_profiles(id) on delete cascade,
  name text not null,
  phone text,
  email text,
  contact text,
  notes text,
  created_at timestamptz not null default now()
);
create index if not exists suppliers_garage_idx on public.suppliers(garage_id);
alter table public.suppliers enable row level security;
drop policy if exists "suppliers: owner" on public.suppliers;
create policy "suppliers: owner" on public.suppliers for all to authenticated
  using (public.owns_verified_garage(garage_id)) with check (public.owns_verified_garage(garage_id));

-- ---------- parts ----------
create table if not exists public.parts (
  id uuid primary key default gen_random_uuid(),
  garage_id uuid not null references public.garage_profiles(id) on delete cascade,
  sku text,
  name text not null,
  item_key text,                       -- maintenance item it serves (data/items.json), links the forecast to stock
  brand text,
  fits text,                           -- free text: models or engines it fits
  unit text not null default 'unit' check (unit in ('unit','liter')),
  stock numeric(10,2) not null default 0,
  min_stock numeric(10,2) not null default 0,
  cost numeric(10,2),
  price numeric(10,2),
  supplier_id uuid references public.suppliers(id) on delete set null,
  location text,
  active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists parts_garage_idx on public.parts(garage_id);
create index if not exists parts_supplier_idx on public.parts(supplier_id);
create unique index if not exists parts_sku_uniq on public.parts(garage_id, lower(sku)) where sku is not null and sku <> '';
alter table public.parts enable row level security;
drop policy if exists "parts: owner" on public.parts;
create policy "parts: owner" on public.parts for all to authenticated
  using (public.owns_verified_garage(garage_id))
  with check (public.owns_verified_garage(garage_id)
    and (parts.supplier_id is null or exists (select 1 from public.suppliers s where s.id = parts.supplier_id and s.garage_id = parts.garage_id)));

-- ---------- purchase orders ----------
create table if not exists public.purchase_orders (
  id uuid primary key default gen_random_uuid(),
  garage_id uuid not null references public.garage_profiles(id) on delete cascade,
  supplier_id uuid references public.suppliers(id) on delete set null,
  number int,
  status text not null default 'draft' check (status in ('draft','sent','received','cancelled')),
  lines jsonb not null default '[]',   -- [{"part_id":"…","sku":"…","name":"…","qty":4,"cost":32,"received":4}]
  total numeric(10,2) not null default 0,
  note text,
  sent_at timestamptz,
  received_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists purchase_orders_garage_idx on public.purchase_orders(garage_id, created_at desc);
create index if not exists purchase_orders_supplier_idx on public.purchase_orders(supplier_id);
alter table public.purchase_orders enable row level security;
drop policy if exists "purchase_orders: owner" on public.purchase_orders;
create policy "purchase_orders: owner" on public.purchase_orders for all to authenticated
  using (public.owns_verified_garage(garage_id))
  with check (public.owns_verified_garage(garage_id)
    and (purchase_orders.supplier_id is null or exists (select 1 from public.suppliers s where s.id = purchase_orders.supplier_id and s.garage_id = purchase_orders.garage_id)));

-- running number per garage
create or replace function public.purchase_order_number() returns trigger
language plpgsql set search_path = '' as $$
begin
  perform pg_advisory_xact_lock(hashtext('po:' || new.garage_id::text));
  select coalesce(max(number), 0) + 1 into new.number from public.purchase_orders where garage_id = new.garage_id;
  return new;
end $$;
drop trigger if exists purchase_order_number on public.purchase_orders;
create trigger purchase_order_number before insert on public.purchase_orders for each row execute function public.purchase_order_number();

-- ---------- stock ledger ----------
create table if not exists public.stock_moves (
  id uuid primary key default gen_random_uuid(),
  garage_id uuid not null references public.garage_profiles(id) on delete cascade,
  part_id uuid not null references public.parts(id) on delete cascade,
  qty numeric(10,2) not null check (qty <> 0),
  reason text not null check (reason in ('receive','use','adjust')),
  purchase_order_id uuid references public.purchase_orders(id) on delete set null,
  work_order_id uuid references public.work_orders(id) on delete cascade,
  note text,
  created_at timestamptz not null default now()
);
create index if not exists stock_moves_part_idx on public.stock_moves(part_id, created_at desc);
create index if not exists stock_moves_wo_idx on public.stock_moves(work_order_id);
create index if not exists stock_moves_po_idx on public.stock_moves(purchase_order_id);
create index if not exists stock_moves_garage_idx on public.stock_moves(garage_id);
alter table public.stock_moves enable row level security;
drop policy if exists "stock_moves: owner read" on public.stock_moves;
drop policy if exists "stock_moves: owner insert" on public.stock_moves;
drop policy if exists "stock_moves: owner delete" on public.stock_moves;
create policy "stock_moves: owner read" on public.stock_moves for select to authenticated using (public.owns_verified_garage(garage_id));
create policy "stock_moves: owner insert" on public.stock_moves for insert to authenticated
  with check (public.owns_verified_garage(garage_id)
    and exists (select 1 from public.parts p where p.id = stock_moves.part_id and p.garage_id = stock_moves.garage_id)
    and (stock_moves.work_order_id is null or exists (select 1 from public.work_orders w where w.id = stock_moves.work_order_id and w.garage_id = stock_moves.garage_id))
    and (stock_moves.purchase_order_id is null or exists (select 1 from public.purchase_orders o where o.id = stock_moves.purchase_order_id and o.garage_id = stock_moves.garage_id)));
create policy "stock_moves: owner delete" on public.stock_moves for delete to authenticated using (public.owns_verified_garage(garage_id));
revoke update on public.stock_moves from anon, authenticated;  -- the ledger is append-only (rows are removed only with their work order)

-- keeps parts.stock equal to the sum of its moves (moves are never updated, only added or removed)
create or replace function public.stock_moves_apply() returns trigger
language plpgsql set search_path = '' as $$
begin
  if tg_op = 'INSERT' then
    update public.parts set stock = stock + new.qty, updated_at = now() where id = new.part_id;
    return new;
  end if;
  update public.parts set stock = stock - old.qty, updated_at = now() where id = old.part_id;
  return old;
end $$;
drop trigger if exists stock_moves_apply on public.stock_moves;
create trigger stock_moves_apply after insert or delete on public.stock_moves for each row execute function public.stock_moves_apply();

-- Receive a purchase order: p_lines = [{"part_id":"…","qty":4,"cost":32}]. Runs as the caller, so RLS applies.
create or replace function public.po_receive(p_po uuid, p_lines jsonb)
returns public.purchase_orders language plpgsql set search_path = '' as $$
declare o public.purchase_orders; l jsonb; v_qty numeric; v_cost numeric;
begin
  select * into o from public.purchase_orders where id = p_po for update;
  if o.id is null then raise exception 'not found'; end if;
  if o.status in ('received','cancelled') then raise exception 'already %', o.status; end if;
  for l in select * from jsonb_array_elements(coalesce(p_lines, '[]'::jsonb)) loop
    v_qty := nullif(l ->> 'qty', '')::numeric; v_cost := nullif(l ->> 'cost', '')::numeric;
    if v_qty is null or v_qty <= 0 or nullif(l ->> 'part_id', '') is null then continue; end if;
    insert into public.stock_moves (garage_id, part_id, qty, reason, purchase_order_id)
    values (o.garage_id, (l ->> 'part_id')::uuid, v_qty, 'receive', o.id);
    if v_cost is not null and v_cost >= 0 then
      update public.parts set cost = v_cost, supplier_id = coalesce(supplier_id, o.supplier_id) where id = (l ->> 'part_id')::uuid;
    end if;
  end loop;
  update public.purchase_orders set status = 'received', received_at = now(), updated_at = now(),
    lines = (select coalesce(jsonb_agg(x || jsonb_build_object('received', coalesce((select (r ->> 'qty')::numeric from jsonb_array_elements(coalesce(p_lines, '[]'::jsonb)) r where r ->> 'part_id' = x ->> 'part_id' limit 1), 0))), '[]'::jsonb)
             from jsonb_array_elements(o.lines) x)
  where id = o.id returning * into o;
  return o;
end $$;

-- Re-sync the stock a work order used with its lines that point at a part. Runs as the caller.
create or replace function public.wo_consume(p_wo uuid)
returns int language plpgsql set search_path = '' as $$
declare w public.work_orders; n int;
begin
  select * into w from public.work_orders where id = p_wo;
  if w.id is null then raise exception 'not found'; end if;
  delete from public.stock_moves where work_order_id = w.id and reason = 'use';
  insert into public.stock_moves (garage_id, part_id, qty, reason, work_order_id)
  select w.garage_id, p.id, -sum((l ->> 'qty')::numeric), 'use', w.id
  from jsonb_array_elements(w.lines) l join public.parts p on p.id::text = l ->> 'part_id' and p.garage_id = w.garage_id
  where coalesce(nullif(l ->> 'qty', '')::numeric, 0) > 0
  group by p.id;
  get diagnostics n = row_count;
  return n;
end $$;

-- ---------- invoices ----------
create table if not exists public.invoices (
  id uuid primary key default gen_random_uuid(),
  garage_id uuid not null references public.garage_profiles(id) on delete cascade,
  work_order_id uuid references public.work_orders(id) on delete set null,
  kind text not null check (kind in ('invoice_receipt','tax_invoice','receipt','other')),
  provider text not null default 'manual' check (provider in ('morning','manual')),
  number text,
  provider_id text,
  url text,
  customer_name text,
  total numeric(10,2),
  payment text check (payment in ('cash','card','transfer','app','check','other','unpaid')),
  issued_at timestamptz not null default now()
);
create index if not exists invoices_garage_idx on public.invoices(garage_id, issued_at desc);
create index if not exists invoices_wo_idx on public.invoices(work_order_id);
alter table public.invoices enable row level security;
drop policy if exists "invoices: owner read" on public.invoices;
drop policy if exists "invoices: owner records" on public.invoices;
drop policy if exists "invoices: owner removes manual" on public.invoices;
create policy "invoices: owner read" on public.invoices for select to authenticated using (public.owns_verified_garage(garage_id));
-- the client only records invoices issued elsewhere; provider invoices are written by the edge function
create policy "invoices: owner records" on public.invoices for insert to authenticated
  with check (public.owns_verified_garage(garage_id) and provider = 'manual'
    and (invoices.work_order_id is null or exists (select 1 from public.work_orders w where w.id = invoices.work_order_id and w.garage_id = invoices.garage_id)));
create policy "invoices: owner removes manual" on public.invoices for delete to authenticated using (public.owns_verified_garage(garage_id) and provider = 'manual');

-- ---------- invoicing provider settings (secret is write-only) ----------
create table if not exists public.garage_billing (
  garage_id uuid primary key references public.garage_profiles(id) on delete cascade,
  provider text not null default 'morning' check (provider in ('morning')),
  api_id text,
  api_secret text,
  has_secret boolean generated always as (coalesce(api_secret, '') <> '') stored,
  sandbox boolean not null default false,
  vat_exempt boolean not null default false,   -- עוסק פטור: receipts only
  updated_at timestamptz not null default now()
);
alter table public.garage_billing enable row level security;
drop policy if exists "garage_billing: owner read" on public.garage_billing;
drop policy if exists "garage_billing: owner delete" on public.garage_billing;
create policy "garage_billing: owner read" on public.garage_billing for select to authenticated using (public.owns_verified_garage(garage_id));
create policy "garage_billing: owner delete" on public.garage_billing for delete to authenticated using (public.owns_verified_garage(garage_id));
revoke all on public.garage_billing from anon, authenticated;
grant select (garage_id, provider, api_id, has_secret, sandbox, vat_exempt, updated_at) on public.garage_billing to authenticated;
grant delete on public.garage_billing to authenticated;

-- writes go through here; an empty secret keeps the stored one
create or replace function public.billing_save(p_garage uuid, p_api_id text, p_secret text, p_sandbox boolean, p_vat_exempt boolean)
returns void language plpgsql security definer set search_path = '' as $$
begin
  if not public.owns_verified_garage(p_garage) then raise exception 'not allowed'; end if;
  insert into public.garage_billing (garage_id, api_id, api_secret, sandbox, vat_exempt, updated_at)
  values (p_garage, nullif(trim(coalesce(p_api_id, '')), ''), nullif(trim(coalesce(p_secret, '')), ''), coalesce(p_sandbox, false), coalesce(p_vat_exempt, false), now())
  on conflict (garage_id) do update set
    api_id = excluded.api_id,
    api_secret = coalesce(excluded.api_secret, public.garage_billing.api_secret),
    sandbox = excluded.sandbox, vat_exempt = excluded.vat_exempt, updated_at = now();
end $$;

revoke execute on function public.po_receive(uuid, jsonb) from public, anon;
grant execute on function public.po_receive(uuid, jsonb) to authenticated;
revoke execute on function public.wo_consume(uuid) from public, anon;
grant execute on function public.wo_consume(uuid) to authenticated;
revoke execute on function public.billing_save(uuid, text, text, boolean, boolean) from public, anon;
grant execute on function public.billing_save(uuid, text, text, boolean, boolean) to authenticated;
revoke execute on function public.purchase_order_number() from public, anon, authenticated;
revoke execute on function public.stock_moves_apply() from public, anon, authenticated;
