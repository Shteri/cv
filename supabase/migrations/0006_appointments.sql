-- Garage side, phase 2: appointment calendar, online booking link, extra-work approval by link, car-ready status.
-- Run after 0005. Safe to run more than once.
--
-- Public (no sign-in) entry points are SECURITY DEFINER functions with narrow inputs and outputs:
--   booking_info / book_appointment     for /book/?g=<garage id>  (busy slots only, never names or phones)
--   approval_get / approval_decide      for /approve/?id=<approval id>  (the random id is the access key)

-- ---------- booking settings on the garage profile ----------
alter table public.garage_profiles add column if not exists booking_enabled boolean not null default false;
alter table public.garage_profiles add column if not exists bays int not null default 2;
alter table public.garage_profiles add column if not exists slot_minutes int not null default 60;
do $$ begin
  alter table public.garage_profiles add constraint garage_profiles_bays_check check (bays between 1 and 30);
exception when duplicate_object then null; end $$;
do $$ begin
  alter table public.garage_profiles add constraint garage_profiles_slot_check check (slot_minutes between 15 and 240);
exception when duplicate_object then null; end $$;

-- ---------- appointments ----------
create table if not exists public.appointments (
  id uuid primary key default gen_random_uuid(),
  garage_id uuid not null references public.garage_profiles(id) on delete cascade,
  garage_car_id uuid references public.garage_cars(id) on delete set null,
  customer_name text not null,
  phone text,
  plate text,
  kind text not null default 'service' check (kind in ('service','repair','test','other')),
  note text,
  starts_at timestamptz not null,
  minutes int not null default 60 check (minutes between 15 and 600),
  bay int,                                   -- 1..bays; null = not assigned yet
  status text not null default 'booked' check (status in ('booked','arrived','in_progress','waiting_approval','ready','done','cancelled','no_show')),
  source text not null default 'garage' check (source in ('garage','online')),
  work_order_id uuid references public.work_orders(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists appointments_garage_time_idx on public.appointments(garage_id, starts_at);
create index if not exists appointments_car_idx on public.appointments(garage_car_id);
create index if not exists appointments_wo_idx on public.appointments(work_order_id);
alter table public.appointments enable row level security;
drop policy if exists "appointments: owner" on public.appointments;
create policy "appointments: owner" on public.appointments for all to authenticated
  using (public.owns_verified_garage(garage_id))
  with check (public.owns_verified_garage(garage_id)
    and (appointments.garage_car_id is null or exists (select 1 from public.garage_cars c where c.id = appointments.garage_car_id and c.garage_id = appointments.garage_id))
    and (appointments.work_order_id is null or exists (select 1 from public.work_orders w where w.id = appointments.work_order_id and w.garage_id = appointments.garage_id)));

-- ---------- extra-work approvals ----------
create table if not exists public.work_approvals (
  id uuid primary key default gen_random_uuid(),   -- also the access key in the customer's link
  garage_id uuid not null references public.garage_profiles(id) on delete cascade,
  appointment_id uuid references public.appointments(id) on delete set null,
  car_label text,
  message text,
  lines jsonb not null default '[]',              -- [{"desc":"רפידות בלם קדמיות","price":480}]
  total int not null default 0,
  status text not null default 'pending' check (status in ('pending','approved','declined')),
  created_at timestamptz not null default now(),
  decided_at timestamptz
);
create index if not exists work_approvals_garage_idx on public.work_approvals(garage_id, created_at desc);
create index if not exists work_approvals_appt_idx on public.work_approvals(appointment_id);
alter table public.work_approvals enable row level security;
drop policy if exists "work_approvals: owner" on public.work_approvals;
create policy "work_approvals: owner" on public.work_approvals for all to authenticated
  using (public.owns_verified_garage(garage_id))
  with check (public.owns_verified_garage(garage_id)
    and (work_approvals.appointment_id is null or exists (select 1 from public.appointments a where a.id = work_approvals.appointment_id and a.garage_id = work_approvals.garage_id)));

-- ---------- public booking ----------
-- Opening hours: garage_profiles.hours {"0":{"open":"08:00","close":"17:00"}, ..., "6":null}; 0 = Sunday.
-- Garages that never set hours get Sun-Thu 08:00-17:00 and Fri 08:00-13:00.
create or replace function public.garage_hours(p_hours jsonb) returns jsonb
language sql immutable set search_path = '' as $$
  select case when p_hours is null or p_hours = '{}'::jsonb then
    '{"0":{"open":"08:00","close":"17:00"},"1":{"open":"08:00","close":"17:00"},"2":{"open":"08:00","close":"17:00"},"3":{"open":"08:00","close":"17:00"},"4":{"open":"08:00","close":"17:00"},"5":{"open":"08:00","close":"13:00"},"6":null}'::jsonb
  else p_hours end;
$$;

-- What the booking page needs: the garage, its hours and settings, and busy intervals for the next 30 days.
create or replace function public.booking_info(p_garage uuid)
returns jsonb language sql security definer set search_path = '' stable as $$
  select jsonb_build_object(
    'id', g.id, 'name', g.name, 'city', g.city, 'address', g.address, 'phone', g.phone,
    'hours', public.garage_hours(g.hours), 'bays', g.bays, 'slot_minutes', g.slot_minutes, 'enabled', g.booking_enabled,
    'busy', coalesce((select jsonb_agg(jsonb_build_array(a.starts_at, a.minutes)) from public.appointments a
                      where a.garage_id = g.id and a.status not in ('cancelled','no_show')
                        and a.starts_at > now() - interval '1 day' and a.starts_at < now() + interval '31 days'), '[]'::jsonb))
  from public.garage_profiles g
  where g.id = p_garage and g.status = 'verified';
$$;

-- Book a slot. Checks: booking enabled, within opening hours, in the next 30 days, a free bay, and at most
-- 3 open online bookings per phone at this garage. A per-garage lock serializes concurrent bookings.
create or replace function public.book_appointment(p_garage uuid, p_starts_at timestamptz, p_name text, p_phone text, p_plate text, p_kind text, p_note text)
returns uuid language plpgsql security definer set search_path = '' as $$
declare g record; v_local timestamp; v_day jsonb; v_end timestamptz; v_busy int; v_id uuid; v_phone text := regexp_replace(coalesce(p_phone, ''), '\D', '', 'g');
begin
  select id, booking_enabled, bays, slot_minutes, public.garage_hours(hours) as hours into g
  from public.garage_profiles where id = p_garage and status = 'verified';
  if g.id is null or not g.booking_enabled then raise exception 'booking closed'; end if;
  if coalesce(trim(p_name), '') = '' or length(v_phone) < 9 then raise exception 'name and phone required'; end if;
  if p_starts_at < now() + interval '30 minutes' or p_starts_at > now() + interval '30 days' then raise exception 'time out of range'; end if;
  v_local := p_starts_at at time zone 'Asia/Jerusalem';
  v_day := g.hours -> extract(dow from v_local)::int::text;
  if v_day is null or jsonb_typeof(v_day) <> 'object'
     or v_local::time < (v_day ->> 'open')::time
     or (v_local + make_interval(mins => g.slot_minutes))::time > (v_day ->> 'close')::time then
    raise exception 'outside opening hours';
  end if;
  perform pg_advisory_xact_lock(hashtext('book:' || p_garage::text));
  v_end := p_starts_at + make_interval(mins => g.slot_minutes);
  select count(*) into v_busy from public.appointments a
  where a.garage_id = p_garage and a.status not in ('cancelled','no_show')
    and a.starts_at < v_end and a.starts_at + make_interval(mins => a.minutes) > p_starts_at;
  if v_busy >= g.bays then raise exception 'slot taken'; end if;
  if (select count(*) from public.appointments a where a.garage_id = p_garage and a.source = 'online'
        and regexp_replace(coalesce(a.phone, ''), '\D', '', 'g') = v_phone and a.starts_at > now() and a.status = 'booked') >= 3 then
    raise exception 'too many bookings';
  end if;
  insert into public.appointments (garage_id, garage_car_id, customer_name, phone, plate, kind, note, starts_at, minutes, source)
  values (p_garage,
          (select c.id from public.garage_cars c where c.garage_id = p_garage and c.plate is not null and c.plate = nullif(regexp_replace(coalesce(p_plate, ''), '\D', '', 'g'), '')),
          left(trim(p_name), 80), left(p_phone, 30), nullif(regexp_replace(coalesce(p_plate, ''), '\D', '', 'g'), ''),
          case when p_kind in ('service','repair','test','other') then p_kind else 'service' end,
          nullif(left(trim(coalesce(p_note, '')), 300), ''), p_starts_at, g.slot_minutes, 'online')
  returning id into v_id;
  return v_id;
end $$;

-- ---------- public approval of extra work ----------
create or replace function public.approval_get(p_id uuid)
returns jsonb language sql security definer set search_path = '' stable as $$
  select jsonb_build_object('id', w.id, 'garage', g.name, 'garage_phone', g.phone, 'car', w.car_label, 'message', w.message,
                            'lines', w.lines, 'total', w.total, 'status', w.status, 'created_at', w.created_at, 'decided_at', w.decided_at)
  from public.work_approvals w join public.garage_profiles g on g.id = w.garage_id
  where w.id = p_id;
$$;

create or replace function public.approval_decide(p_id uuid, p_approve boolean)
returns text language plpgsql security definer set search_path = '' as $$
declare v_status text; v_appt uuid;
begin
  update public.work_approvals set status = case when p_approve then 'approved' else 'declined' end, decided_at = now()
  where id = p_id and status = 'pending' returning status, appointment_id into v_status, v_appt;
  if v_status is null then
    select status into v_status from public.work_approvals where id = p_id;
    if v_status is null then raise exception 'not found'; end if;
    return v_status;                        -- already decided: report it, change nothing
  end if;
  -- the car goes back to work once the customer answered
  update public.appointments set status = 'in_progress', updated_at = now() where id = v_appt and status = 'waiting_approval';
  return v_status;
end $$;

revoke execute on function public.garage_hours(jsonb) from public;
grant execute on function public.garage_hours(jsonb) to anon, authenticated;
revoke execute on function public.booking_info(uuid) from public;
grant execute on function public.booking_info(uuid) to anon, authenticated;
revoke execute on function public.book_appointment(uuid, timestamptz, text, text, text, text, text) from public;
grant execute on function public.book_appointment(uuid, timestamptz, text, text, text, text, text) to anon, authenticated;
revoke execute on function public.approval_get(uuid) from public;
grant execute on function public.approval_get(uuid) to anon, authenticated;
revoke execute on function public.approval_decide(uuid, boolean) from public;
grant execute on function public.approval_decide(uuid, boolean) to anon, authenticated;
