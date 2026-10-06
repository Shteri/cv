-- Fewer no-shows: reminders with a link where the customer confirms, reschedules or cancels, and garage approval
-- for online bookings from a phone that did not show up before. Run after 0009. Safe to run more than once.
--
-- Public (no sign-in) entry points, SECURITY DEFINER with narrow inputs and outputs:
--   book_slot                 for /book/: books like book_appointment and returns the appointment's link token
--   appt_get / appt_respond   for /appt/?t=<token>  (the random token is the access key)

-- ---------- appointment fields ----------
alter table public.appointments add column if not exists token uuid not null default gen_random_uuid();
alter table public.appointments add column if not exists confirmed_at timestamptz;   -- the customer said they are coming
alter table public.appointments add column if not exists reminded_at timestamptz;    -- the garage sent a reminder
alter table public.appointments add column if not exists cancelled_by text;          -- customer | garage
alter table public.appointments add column if not exists cancelled_late boolean not null default false;
alter table public.appointments add column if not exists needs_ok boolean not null default false; -- waits for the garage
do $$ begin
  alter table public.appointments add constraint appointments_cancelled_by_check check (cancelled_by in ('customer','garage'));
exception when duplicate_object then null; end $$;
create unique index if not exists appointments_token_idx on public.appointments(token);

-- ---------- garage policy ----------
alter table public.garage_profiles add column if not exists cancel_hours int not null default 12;  -- free cancellation until this many hours before
alter table public.garage_profiles add column if not exists noshow_limit int not null default 2;   -- strikes before online bookings need approval; 0 = off
do $$ begin
  alter table public.garage_profiles add constraint garage_profiles_cancel_hours_check check (cancel_hours between 0 and 72);
exception when duplicate_object then null; end $$;
do $$ begin
  alter table public.garage_profiles add constraint garage_profiles_noshow_limit_check check (noshow_limit between 0 and 10);
exception when duplicate_object then null; end $$;

-- Strikes: no-shows and late cancellations by this phone at this garage in the last 12 months.
-- SECURITY INVOKER: the garage owner sees only their own garage; inside book_slot it runs with the definer's rights.
create or replace function public.appt_strikes(p_garage uuid, p_phone text)
returns int language sql stable set search_path = '' as $$
  select count(*)::int from public.appointments a
  where a.garage_id = p_garage
    and length(regexp_replace(coalesce(p_phone, ''), '\D', '', 'g')) >= 9
    and regexp_replace(coalesce(a.phone, ''), '\D', '', 'g') = regexp_replace(coalesce(p_phone, ''), '\D', '', 'g')
    and a.starts_at > now() - interval '12 months' and a.starts_at < now()
    and (a.status = 'no_show' or (a.status = 'cancelled' and a.cancelled_late));
$$;

-- ---------- public booking, with the link token ----------
-- Same checks as book_appointment; a phone with enough strikes books a slot that waits for the garage's approval.
create or replace function public.book_slot(p_garage uuid, p_starts_at timestamptz, p_name text, p_phone text, p_plate text, p_kind text, p_note text)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare g record; v_local timestamp; v_day jsonb; v_end timestamptz; v_busy int; v_token uuid; v_needs boolean;
        v_phone text := regexp_replace(coalesce(p_phone, ''), '\D', '', 'g');
begin
  select id, booking_enabled, bays, slot_minutes, noshow_limit, public.garage_hours(hours) as hours into g
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
  v_needs := g.noshow_limit > 0 and public.appt_strikes(p_garage, v_phone) >= g.noshow_limit;
  insert into public.appointments (garage_id, garage_car_id, customer_name, phone, plate, kind, note, starts_at, minutes, source, needs_ok)
  values (p_garage,
          (select c.id from public.garage_cars c where c.garage_id = p_garage and c.plate is not null and c.plate = nullif(regexp_replace(coalesce(p_plate, ''), '\D', '', 'g'), '')),
          left(trim(p_name), 80), left(p_phone, 30), nullif(regexp_replace(coalesce(p_plate, ''), '\D', '', 'g'), ''),
          case when p_kind in ('service','repair','test','other') then p_kind else 'service' end,
          nullif(left(trim(coalesce(p_note, '')), 300), ''), p_starts_at, g.slot_minutes, 'online', v_needs)
  returning token into v_token;
  return jsonb_build_object('token', v_token, 'needs_ok', v_needs);
end $$;

-- The old entry point (pages cached before this migration) books through the same rules.
create or replace function public.book_appointment(p_garage uuid, p_starts_at timestamptz, p_name text, p_phone text, p_plate text, p_kind text, p_note text)
returns uuid language plpgsql security definer set search_path = '' as $$
declare v jsonb;
begin
  v := public.book_slot(p_garage, p_starts_at, p_name, p_phone, p_plate, p_kind, p_note);
  return (select a.id from public.appointments a where a.token = (v ->> 'token')::uuid);
end $$;

-- ---------- the customer's appointment page ----------
create or replace function public.appt_get(p_token uuid)
returns jsonb language sql security definer set search_path = '' stable as $$
  select jsonb_build_object('garage', g.name, 'garage_id', g.id, 'garage_phone', g.phone, 'address', g.address, 'city', g.city,
    'booking_enabled', g.booking_enabled, 'cancel_hours', g.cancel_hours,
    'name', a.customer_name, 'plate', a.plate, 'kind', a.kind, 'starts_at', a.starts_at, 'minutes', a.minutes,
    'status', a.status, 'confirmed_at', a.confirmed_at, 'needs_ok', a.needs_ok, 'cancelled_by', a.cancelled_by)
  from public.appointments a join public.garage_profiles g on g.id = a.garage_id
  where a.token = p_token;
$$;

-- confirm: "I'm coming". cancel: frees the slot; after the garage's free-cancellation window it is marked late.
-- Only a future appointment that is still booked can change.
create or replace function public.appt_respond(p_token uuid, p_action text)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare a record;
begin
  if p_action not in ('confirm','cancel') then raise exception 'bad action'; end if;
  select x.id, x.status, x.starts_at, g.cancel_hours into a
  from public.appointments x join public.garage_profiles g on g.id = x.garage_id
  where x.token = p_token for update of x;
  if a.id is null then raise exception 'not found'; end if;
  if a.status = 'booked' and a.starts_at > now() then
    if p_action = 'confirm' then
      update public.appointments set confirmed_at = coalesce(confirmed_at, now()), updated_at = now() where id = a.id;
    else
      update public.appointments set status = 'cancelled', cancelled_by = 'customer',
        cancelled_late = now() > a.starts_at - make_interval(hours => a.cancel_hours), updated_at = now()
      where id = a.id;
    end if;
  end if;
  return public.appt_get(p_token);
end $$;

revoke execute on function public.appt_strikes(uuid, text) from public;
grant execute on function public.appt_strikes(uuid, text) to authenticated;
revoke execute on function public.book_slot(uuid, timestamptz, text, text, text, text, text) from public;
grant execute on function public.book_slot(uuid, timestamptz, text, text, text, text, text) to anon, authenticated;
revoke execute on function public.appt_get(uuid) from public;
grant execute on function public.appt_get(uuid) to anon, authenticated;
revoke execute on function public.appt_respond(uuid, text) from public;
grant execute on function public.appt_respond(uuid, text) to anon, authenticated;
