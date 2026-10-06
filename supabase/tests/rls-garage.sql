\set ON_ERROR_STOP 1
-- Run with: sh scripts/test-db.sh
-- users: driver D, garage owner G, stranger X, admin A
insert into auth.users (id, email) values
 ('00000000-0000-0000-0000-00000000000d','d@x'),('00000000-0000-0000-0000-00000000000a','a@x'),
 ('00000000-0000-0000-0000-000000000006','g@x'),('00000000-0000-0000-0000-000000000009','x@x');
update public.profiles set is_admin = true where id = '00000000-0000-0000-0000-00000000000a';
create function pg_temp.as_user(u text) returns void language plpgsql as $$ begin perform set_config('request.jwt.claim.sub', u, false); end $$;
create function pg_temp.expect_fail(q text, label text) returns void language plpgsql as $$
begin begin execute q; exception when others then raise notice 'OK  % (blocked: %)', label, sqlerrm; return; end; raise exception 'FAIL % was allowed', label; end $$;
create function pg_temp.check(cond boolean, label text) returns void language plpgsql as $$ begin if cond then raise notice 'OK  %', label; else raise exception 'FAIL %', label; end if; end $$;

set role authenticated;
-- garage owner claims, driver and stranger add cars
select pg_temp.as_user('00000000-0000-0000-0000-000000000006');
insert into public.garage_profiles (id, garage_id, owner_id, name, city, status) values ('11111111-0000-0000-0000-000000000001', 1731, '00000000-0000-0000-0000-000000000006', 'מוסך ליה', 'חולון', 'verified');
select pg_temp.check((select status from public.garage_profiles where id='11111111-0000-0000-0000-000000000001')='pending', 'claim starts pending even if client sends verified');
update public.garage_profiles set status='verified' where id='11111111-0000-0000-0000-000000000001';
select pg_temp.check((select status from public.garage_profiles where id='11111111-0000-0000-0000-000000000001')='pending', 'owner cannot verify own garage');
select pg_temp.as_user('00000000-0000-0000-0000-00000000000d');
insert into public.cars (id, user_id, plate, schedule_id, year, km, km_month, gov) values ('22222222-0000-0000-0000-00000000000d','00000000-0000-0000-0000-00000000000d','1000632','hyundai-i10-2014-2019',2016,80000,1500,'{"test_expiry":"2026-11-10"}');
select pg_temp.expect_fail($q$insert into public.garage_links (garage_id, car_id, user_id) values ('11111111-0000-0000-0000-000000000001','22222222-0000-0000-0000-00000000000d','00000000-0000-0000-0000-00000000000d')$q$, 'join an unverified garage');
select pg_temp.as_user('00000000-0000-0000-0000-000000000009');
insert into public.cars (id, user_id, schedule_id, km) values ('22222222-0000-0000-0000-000000000009','00000000-0000-0000-0000-000000000009','kia-picanto-2017-2025', 10000);
-- admin verifies
select pg_temp.as_user('00000000-0000-0000-0000-00000000000a');
select public.set_garage_status('11111111-0000-0000-0000-000000000001','verified');
select pg_temp.as_user('00000000-0000-0000-0000-000000000009');
select pg_temp.expect_fail($q$select public.set_garage_status('11111111-0000-0000-0000-000000000001','rejected')$q$, 'non-admin changes status');
-- driver joins
select pg_temp.as_user('00000000-0000-0000-0000-00000000000d');
insert into public.garage_links (id, garage_id, car_id, user_id, first_name, phone, allow_contact) values ('33333333-0000-0000-0000-000000000001','11111111-0000-0000-0000-000000000001','22222222-0000-0000-0000-00000000000d','00000000-0000-0000-0000-00000000000d','דני','050-1234567', false);
select pg_temp.expect_fail($q$insert into public.garage_links (garage_id, car_id, user_id) values ('11111111-0000-0000-0000-000000000001','22222222-0000-0000-0000-000000000009','00000000-0000-0000-0000-00000000000d')$q$, 'link someone else''s car');
-- garage reads customers
select pg_temp.as_user('00000000-0000-0000-0000-000000000006');
select pg_temp.check((select count(*) from public.garage_links) = 0, 'garage cannot read links table directly');
select pg_temp.check((select count(*) from public.garage_customers('11111111-0000-0000-0000-000000000001')) = 1, 'garage sees its customer');
select pg_temp.check((select phone from public.garage_customers('11111111-0000-0000-0000-000000000001')) is null, 'phone hidden without contact consent');
select pg_temp.check((select test_expiry from public.garage_customers('11111111-0000-0000-0000-000000000001')) = '2026-11-10', 'test expiry exposed');
select pg_temp.as_user('00000000-0000-0000-0000-00000000000d');
update public.garage_links set allow_contact = true where id = '33333333-0000-0000-0000-000000000001';
select pg_temp.as_user('00000000-0000-0000-0000-000000000006');
select pg_temp.check((select phone from public.garage_customers('11111111-0000-0000-0000-000000000001')) = '050-1234567', 'phone visible after consent');
select pg_temp.as_user('00000000-0000-0000-0000-000000000009');
select pg_temp.expect_fail($q$select * from public.garage_customers('11111111-0000-0000-0000-000000000001')$q$, 'stranger reads garage customers');
select pg_temp.expect_fail($q$select public.garage_add_entry('33333333-0000-0000-0000-000000000001','service',75000,80500,'2026-10',890,'x','independent')$q$, 'stranger logs an entry');
-- garage logs a visit
select pg_temp.as_user('00000000-0000-0000-0000-000000000006');
select public.garage_add_entry('33333333-0000-0000-0000-000000000001','service',75000,80500,'2026-10',890,'החלפת שמן ומסנן','independent') as entry_id \gset
select pg_temp.check((select pending from public.garage_customers('11111111-0000-0000-0000-000000000001')) = 1, 'pending count shows');
select pg_temp.expect_fail($q$select public.garage_add_entry('33333333-0000-0000-0000-000000000001','paint',null,1,'',0,'','independent')$q$, 'bad kind rejected');
select pg_temp.check((select count(*) from public.garage_entries) = 0, 'garage cannot read entries table directly');
-- driver decides
select pg_temp.as_user('00000000-0000-0000-0000-000000000009');
select pg_temp.check((select count(*) from public.garage_entries) = 0, 'stranger cannot see the entry');
select pg_temp.expect_fail(format($q$select public.decide_garage_entry(%L, true)$q$, :'entry_id'), 'stranger accepts the entry');
select pg_temp.as_user('00000000-0000-0000-0000-00000000000d');
select pg_temp.check((select count(*) from public.garage_entries where status='pending') = 1, 'driver sees the pending entry');
select public.decide_garage_entry(:'entry_id', true);
select pg_temp.expect_fail(format($q$select public.decide_garage_entry(%L, false)$q$, :'entry_id'), 'decide twice');
select pg_temp.as_user('00000000-0000-0000-0000-000000000006');
select pg_temp.check((select last_visit from public.garage_customers('11111111-0000-0000-0000-000000000001')) is not null, 'last visit recorded');
-- driver revokes
select pg_temp.as_user('00000000-0000-0000-0000-00000000000d');
delete from public.garage_links where id = '33333333-0000-0000-0000-000000000001';
select pg_temp.as_user('00000000-0000-0000-0000-000000000006');
select pg_temp.check((select count(*) from public.garage_customers('11111111-0000-0000-0000-000000000001')) = 0, 'garage loses access after revoke');
select pg_temp.as_user('');
reset role; set role anon;
select pg_temp.expect_fail($q$select * from public.garage_customers('11111111-0000-0000-0000-000000000001')$q$, 'anonymous reads customers');
