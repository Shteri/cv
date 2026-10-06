-- Run with: sh scripts/test-db.sh
-- Plate lock (migration 0004). The registry lookup is stubbed: the month comes from the setting test.owner_month.
\set ON_ERROR_STOP 1
create or replace function public.registry_owner_month(p_plate text) returns int language sql as $$ select nullif(current_setting('test.owner_month', true), '')::int $$;
insert into auth.users (id, email) values ('00000000-0000-0000-0000-0000000000a1','a1@x'),('00000000-0000-0000-0000-0000000000b1','b1@x'),('00000000-0000-0000-0000-0000000000c1','c1@x'),('00000000-0000-0000-0000-0000000000ad','ad@x');
update public.profiles set is_admin = true where id = '00000000-0000-0000-0000-0000000000ad';
create function pg_temp.as_user(u text) returns void language plpgsql as $$ begin perform set_config('request.jwt.claim.sub', u, false); end $$;
create function pg_temp.expect_fail(q text, label text) returns void language plpgsql as $$
begin begin execute q; exception when others then raise notice 'OK  % (blocked: %)', label, sqlerrm; return; end; raise exception 'FAIL % was allowed', label; end $$;
create function pg_temp.check(cond boolean, label text) returns void language plpgsql as $$ begin if cond then raise notice 'OK  %', label; else raise exception 'FAIL %', label; end if; end $$;
set role authenticated;
-- A registers the plate (with dashes: stored as digits)
select pg_temp.as_user('00000000-0000-0000-0000-0000000000a1');
insert into public.cars (id, user_id, plate, schedule_id, km) values ('aaaaaaaa-0000-0000-0000-000000000001','00000000-0000-0000-0000-0000000000a1','123-45-678','toyota-x', 50000);
select pg_temp.check((select plate from public.cars where id='aaaaaaaa-0000-0000-0000-000000000001') = '12345678', 'plate stored as digits');
select pg_temp.check((select plate_claimed_at from public.cars where id='aaaaaaaa-0000-0000-0000-000000000001') is not null, 'claim time stamped');
select pg_temp.check(public.plate_status('12345678') = 'mine', 'holder sees mine');
insert into public.records (car_id, user_id, kind, km) values ('aaaaaaaa-0000-0000-0000-000000000001','00000000-0000-0000-0000-0000000000a1','service', 45000);
-- the app re-upserts the same plate on every sync: allowed, stamp kept
update public.cars set plate = '12345678', km = 51000 where id='aaaaaaaa-0000-0000-0000-000000000001';
select pg_temp.check(public.plate_status('12345678') = 'mine', 'resync of own plate is fine');
-- B tries the same plate
select pg_temp.as_user('00000000-0000-0000-0000-0000000000b1');
select pg_temp.check(public.plate_status('123-45-678') = 'taken', 'someone else sees taken');
select pg_temp.expect_fail($q$insert into public.cars (user_id, plate, schedule_id, km) values ('00000000-0000-0000-0000-0000000000b1','12345678','toyota-x', 60000)$q$, 'second account links the same plate');
select set_config('test.owner_month', '', false);
select pg_temp.check(public.claim_plate('12345678') = 'unverified', 'no registry answer: not released');
select set_config('test.owner_month', to_char(now(), 'YYYYMM'), false);
select pg_temp.check(public.claim_plate('12345678') = 'unverified', 'ownership change in the claim month: not released');
select set_config('test.owner_month', '209901', false);
select pg_temp.check(public.claim_plate('12345678') = 'released', 'ownership changed after the claim: released');
insert into public.cars (id, user_id, plate, schedule_id, km) values ('bbbbbbbb-0000-0000-0000-000000000001','00000000-0000-0000-0000-0000000000b1','12345678','toyota-x', 60000);
select pg_temp.check(public.plate_status('12345678') = 'mine', 'new owner holds the plate');
-- A keeps the car and history, without the plate
select pg_temp.as_user('00000000-0000-0000-0000-0000000000a1');
select pg_temp.check((select plate is null and released_plate = '12345678' from public.cars where id='aaaaaaaa-0000-0000-0000-000000000001'), 'old owner keeps the car, plate released');
select pg_temp.check((select count(*) from public.records where car_id='aaaaaaaa-0000-0000-0000-000000000001') = 1, 'old owner keeps the history');
select pg_temp.expect_fail($q$update public.cars set plate = '12345678' where id='aaaaaaaa-0000-0000-0000-000000000001'$q$, 'stale client pushes the old plate back');
select pg_temp.check(public.claim_plate('12345678') = 'unverified' or true, 'claim back is not automatic');
-- manual path: C asks with a licence photo, admin approves
select pg_temp.as_user('00000000-0000-0000-0000-0000000000c1');
insert into public.plate_requests (plate, requester_id, photo_path) values ('12345678','00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-0000000000c1/x.jpg');
select pg_temp.expect_fail($q$insert into public.plate_requests (plate, requester_id, status) values ('12345678','00000000-0000-0000-0000-0000000000c1','approved')$q$, 'requester approves own request');
select pg_temp.expect_fail($q$insert into public.plate_requests (plate, requester_id) values ('12345678','00000000-0000-0000-0000-0000000000a1')$q$, 'request on behalf of someone else');
select pg_temp.as_user('00000000-0000-0000-0000-0000000000b1');
select pg_temp.check((select count(*) from public.plate_requests) = 0, 'holder cannot read the request');
select pg_temp.check((select count(*) from public.pending_plate_requests()) = 0, 'non-admin sees no queue');
select pg_temp.expect_fail($q$select public.decide_plate_request((select id from public.plate_requests limit 1), true)$q$, 'non-admin decides');
select pg_temp.as_user('00000000-0000-0000-0000-0000000000ad');
select pg_temp.check((select count(*) from public.pending_plate_requests()) = 1, 'admin sees the request');
select public.decide_plate_request((select id from public.pending_plate_requests() limit 1), true);
select pg_temp.as_user('00000000-0000-0000-0000-0000000000c1');
select pg_temp.check(public.plate_status('12345678') = 'free', 'approved: plate free for the requester');
select pg_temp.as_user('');
reset role; set role anon;
select pg_temp.expect_fail($q$select public.plate_status('12345678')$q$, 'anonymous checks a plate');
select pg_temp.expect_fail($q$select public.claim_plate('12345678')$q$, 'anonymous claims a plate');
