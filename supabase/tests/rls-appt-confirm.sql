-- Run with: sh scripts/test-db.sh
-- Appointment link: confirm / cancel by token, late cancellations, no-show strikes (migration 0010).
\set ON_ERROR_STOP 1
insert into auth.users (id, email) values ('00000000-0000-0000-0000-000000000071','r1@x'),('00000000-0000-0000-0000-000000000072','r2@x'),('00000000-0000-0000-0000-00000000007a','radm@x');
update public.profiles set is_admin = true where id = '00000000-0000-0000-0000-00000000007a';
create function pg_temp.as_user(u text) returns void language plpgsql as $$ begin perform set_config('request.jwt.claim.sub', u, false); end $$;
create function pg_temp.expect_fail(q text, label text) returns void language plpgsql as $$
begin begin execute q; exception when others then raise notice 'OK  % (blocked: %)', label, sqlerrm; return; end; raise exception 'FAIL % was allowed', label; end $$;
create function pg_temp.check(cond boolean, label text) returns void language plpgsql as $$ begin if cond then raise notice 'OK  %', label; else raise exception 'FAIL %', label; end if; end $$;
create function pg_temp.sun(h int) returns timestamptz language sql as $$ select (date_trunc('week', now() at time zone 'Asia/Jerusalem') + interval '13 days' + make_interval(hours => h)) at time zone 'Asia/Jerusalem' $$;
set role authenticated;
select pg_temp.as_user('00000000-0000-0000-0000-000000000071');
insert into public.garage_profiles (id, garage_id, owner_id, name, city) values ('71000000-0000-0000-0000-000000000001', 951, '00000000-0000-0000-0000-000000000071', 'מוסך תזכורת', 'רחובות');
select pg_temp.as_user('00000000-0000-0000-0000-000000000072');
insert into public.garage_profiles (id, garage_id, owner_id, name, city) values ('72000000-0000-0000-0000-000000000002', 952, '00000000-0000-0000-0000-000000000072', 'מוסך אחר', 'רחובות');
select pg_temp.as_user('00000000-0000-0000-0000-00000000007a');
select public.set_garage_status('71000000-0000-0000-0000-000000000001','verified'), public.set_garage_status('72000000-0000-0000-0000-000000000002','verified');
select pg_temp.as_user('00000000-0000-0000-0000-000000000071');
update public.garage_profiles set booking_enabled = true, bays = 1, slot_minutes = 60 where id = '71000000-0000-0000-0000-000000000001';
select pg_temp.check((select cancel_hours = 12 and noshow_limit = 2 from public.garage_profiles where id = '71000000-0000-0000-0000-000000000001'), 'default policy: free cancellation until 12 hours, approval after 2 strikes');

-- a customer books and gets a link token
reset role; set role anon; select pg_temp.as_user('');
create temp table t (k text primary key, v jsonb); grant all on t to anon, authenticated;
insert into t select 'a', public.book_slot('71000000-0000-0000-0000-000000000001', pg_temp.sun(10), 'נועה', '052-1111111', '', 'service', '');
select pg_temp.check((select (v ->> 'token') is not null and (v ->> 'needs_ok')::boolean = false from t where k = 'a'), 'booking returns a token, no approval needed');
select pg_temp.check((select public.appt_get((v ->> 'token')::uuid) ->> 'status' = 'booked' and public.appt_get((v ->> 'token')::uuid) ->> 'garage' = 'מוסך תזכורת' from t where k = 'a'), 'the link shows the appointment');
select pg_temp.check((select public.appt_get(gen_random_uuid()) is null), 'a made-up token shows nothing');
select pg_temp.check((select (public.appt_respond((v ->> 'token')::uuid, 'confirm') ->> 'confirmed_at') is not null from t where k = 'a'), 'customer confirms');
select pg_temp.expect_fail($q$select public.appt_respond(gen_random_uuid(), 'confirm')$q$, 'respond with a made-up token');
select pg_temp.expect_fail($q$select public.appt_respond((select (v ->> 'token')::uuid from t where k = 'a'), 'delete')$q$, 'unknown action');
select pg_temp.check((select count(*) = 0 from public.appointments), 'anonymous still cannot read appointments');
select pg_temp.expect_fail($q$select public.appt_strikes('71000000-0000-0000-0000-000000000001', '052-1111111')$q$, 'anonymous counts strikes');
-- early cancellation frees the slot and is not a strike
insert into t select 'b', public.book_slot('71000000-0000-0000-0000-000000000001', pg_temp.sun(12), 'נועה', '052-1111111', '', 'service', '');
select pg_temp.check((select public.appt_respond((v ->> 'token')::uuid, 'cancel') ->> 'status' = 'cancelled' from t where k = 'b'), 'customer cancels');
select pg_temp.check((select public.appt_respond((v ->> 'token')::uuid, 'confirm') ->> 'confirmed_at' is null from t where k = 'b'), 'a cancelled appointment cannot be confirmed');
insert into t select 'b2', public.book_slot('71000000-0000-0000-0000-000000000001', pg_temp.sun(12), 'דן', '052-2222222', '', 'service', '');
select pg_temp.check((select v ? 'token' from t where k = 'b2'), 'the cancelled slot can be booked again');
-- the old entry point still works
select pg_temp.check(public.book_appointment('71000000-0000-0000-0000-000000000001', pg_temp.sun(14), 'דן', '052-2222222', '', 'repair', '') is not null, 'old booking function still books');

-- owner: late cancellation and two past no-shows for one phone
reset role; set role authenticated; select pg_temp.as_user('00000000-0000-0000-0000-000000000071');
insert into public.appointments (id, garage_id, customer_name, phone, starts_at, status) values
  ('71a00000-0000-0000-0000-000000000001', '71000000-0000-0000-0000-000000000001', 'גיל', '054-3333333', now() + interval '3 hours', 'booked'),
  ('71a00000-0000-0000-0000-000000000002', '71000000-0000-0000-0000-000000000001', 'גיל', '054-3333333', now() - interval '20 days', 'no_show'),
  ('71a00000-0000-0000-0000-000000000003', '71000000-0000-0000-0000-000000000001', 'גיל', '0543333333', now() - interval '400 days', 'no_show');
select pg_temp.check((select token is not null from public.appointments where id = '71a00000-0000-0000-0000-000000000001'), 'owner sees the token for the reminder link');
insert into t select 'late', to_jsonb(token) from public.appointments where id = '71a00000-0000-0000-0000-000000000001';
reset role; set role anon; select pg_temp.as_user('');
select pg_temp.check((select public.appt_respond((v #>> '{}')::uuid, 'cancel') ->> 'status' = 'cancelled' from t where k = 'late'), 'cancel 3 hours before');
reset role; set role authenticated; select pg_temp.as_user('00000000-0000-0000-0000-000000000071');
select pg_temp.check((select cancelled_late and cancelled_by = 'customer' from public.appointments where id = '71a00000-0000-0000-0000-000000000001'), 'inside 12 hours it is a late cancellation');
select pg_temp.check(public.appt_strikes('71000000-0000-0000-0000-000000000001', '054-333-3333') = 1, 'one strike: the no-show older than a year does not count, the late cancellation is still in the future');
update public.appointments set starts_at = now() - interval '1 hour' where id = '71a00000-0000-0000-0000-000000000001';
select pg_temp.check(public.appt_strikes('71000000-0000-0000-0000-000000000001', '0543333333') = 2, 'two strikes once the late-cancelled time has passed');
reset role; set role anon; select pg_temp.as_user('');
insert into t select 'c', public.book_slot('71000000-0000-0000-0000-000000000001', pg_temp.sun(15), 'גיל', '054-3333333', '', 'service', '');
select pg_temp.check((select (v ->> 'needs_ok')::boolean from t where k = 'c'), 'a phone with two strikes books a slot that waits for the garage');
select pg_temp.check((select public.appt_get((v ->> 'token')::uuid) ->> 'needs_ok' = 'true' from t where k = 'c'), 'the link says it waits for the garage');
reset role; set role authenticated; select pg_temp.as_user('00000000-0000-0000-0000-000000000071');
update public.garage_profiles set noshow_limit = 0 where id = '71000000-0000-0000-0000-000000000001';
reset role; set role anon; select pg_temp.as_user('');
insert into t select 'd', public.book_slot('71000000-0000-0000-0000-000000000001', pg_temp.sun(16), 'גיל', '054-3333333', '', 'service', '');
select pg_temp.check((select not (v ->> 'needs_ok')::boolean from t where k = 'd'), 'limit 0 turns approval off');

-- another garage sees nothing
reset role; set role authenticated; select pg_temp.as_user('00000000-0000-0000-0000-000000000072');
select pg_temp.check(public.appt_strikes('71000000-0000-0000-0000-000000000001', '054-3333333') = 0, 'another garage cannot count this garage''s strikes');
select pg_temp.expect_fail($q$update public.garage_profiles set cancel_hours = 100 where id = '72000000-0000-0000-0000-000000000002'$q$, 'cancellation window over 72 hours');
reset role;
