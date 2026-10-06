-- Garage platform: modules per garage, job catalog, vehicle inspection on approval links.
-- Run after 0007. Safe to run more than once. Written without DROP/DELETE statements.

-- ---------- which modules the garage uses (null = follow the professions it is licensed for) ----------
alter table public.garage_profiles add column if not exists modules text[];
alter table public.garage_profiles add column if not exists labor_rate numeric(8,2);   -- ₪ per labour hour, for the job catalog

-- ---------- job catalog: the garage's standard jobs with hours and the parts they take ----------
create table if not exists public.job_templates (
  id uuid primary key default gen_random_uuid(),
  garage_id uuid not null references public.garage_profiles(id) on delete cascade,
  name text not null,
  category text,
  hours numeric(5,2) not null default 0 check (hours >= 0),
  price numeric(10,2),                 -- fixed labour price; null = hours x garage labour rate
  parts jsonb not null default '[]',   -- [{"item":"brake_pads","qty":1}] (items from data/items.json; the part comes from stock per car)
  active boolean not null default true,
  created_at timestamptz not null default now()
);
create index if not exists job_templates_garage_idx on public.job_templates(garage_id);
alter table public.job_templates enable row level security;
do $$ begin
  create policy "job_templates: owner" on public.job_templates for all to authenticated
    using (public.owns_verified_garage(garage_id)) with check (public.owns_verified_garage(garage_id));
exception when duplicate_object then null; end $$;

-- ---------- vehicle inspection rides on the approval link ----------
-- checks: [{"key":"brakes_front","label":"בלמים קדמיים","status":"ok|soon|now","note":"…","photos":["https://…"]}]
-- the customer approves line by line; approved_lines holds the indexes into lines
alter table public.work_approvals add column if not exists checks jsonb not null default '[]';
alter table public.work_approvals add column if not exists km int;
alter table public.work_approvals add column if not exists approved_lines int[];
alter table public.work_approvals add column if not exists garage_car_id uuid references public.garage_cars(id) on delete set null;  -- the car an inspection was for
do $$ begin
  create policy "work_approvals: car of the same garage" on public.work_approvals as restrictive for all to authenticated
    using (true)
    with check (work_approvals.garage_car_id is null or exists (select 1 from public.garage_cars c where c.id = work_approvals.garage_car_id and c.garage_id = work_approvals.garage_id));
exception when duplicate_object then null; end $$;

create or replace function public.approval_get(p_id uuid)
returns jsonb language sql security definer set search_path = '' stable as $$
  select jsonb_build_object('id', w.id, 'garage', g.name, 'garage_phone', g.phone, 'car', w.car_label, 'message', w.message,
                            'lines', w.lines, 'total', w.total, 'status', w.status, 'created_at', w.created_at, 'decided_at', w.decided_at,
                            'checks', w.checks, 'km', w.km, 'approved_lines', w.approved_lines)
  from public.work_approvals w join public.garage_profiles g on g.id = w.garage_id
  where w.id = p_id;
$$;

-- The customer picks which lines to approve (none = declined). Decides once; afterwards it reports the decision.
create or replace function public.approval_choose(p_id uuid, p_lines int[])
returns jsonb language plpgsql security definer set search_path = '' as $$
declare w public.work_approvals; v_lines int[];
begin
  select * into w from public.work_approvals where id = p_id for update;
  if w.id is null then raise exception 'not found'; end if;
  if w.status <> 'pending' then return jsonb_build_object('status', w.status, 'approved_lines', w.approved_lines); end if;
  select coalesce(array_agg(distinct i order by i), '{}') into v_lines
  from unnest(coalesce(p_lines, '{}')) i where i >= 0 and i < jsonb_array_length(w.lines);
  update public.work_approvals set status = case when cardinality(v_lines) > 0 then 'approved' else 'declined' end,
    approved_lines = v_lines, decided_at = now()
  where id = w.id returning * into w;
  update public.appointments set status = 'in_progress', updated_at = now() where id = w.appointment_id and status = 'waiting_approval';
  return jsonb_build_object('status', w.status, 'approved_lines', w.approved_lines);
end $$;
grant execute on function public.approval_choose(uuid, int[]) to anon, authenticated;

-- ---------- inspection photos: public by unguessable path, written only into the garage's own folder ----------
insert into storage.buckets (id, name, public) values ('inspection-photos', 'inspection-photos', true) on conflict (id) do nothing;
do $$ begin
  create policy "inspection-photos: garage writes own folder" on storage.objects for insert to authenticated
    with check (bucket_id = 'inspection-photos' and exists (select 1 from public.garage_profiles g
      where g.id::text = (storage.foldername(objects.name))[1] and g.owner_id = (select auth.uid()) and g.status = 'verified'));
exception when duplicate_object then null; end $$;
