-- Run with: sh scripts/test-db.sh
-- Garage book (migration 0005): own customers, joined drivers, work orders, shared history.
\set ON_ERROR_STOP 1
insert into auth.users (id, email) values ('00000000-0000-0000-0000-00000000006a','ga@x'),('00000000-0000-0000-0000-00000000006b','gb@x'),('00000000-0000-0000-0000-0000000000d2','d2@x'),('00000000-0000-0000-0000-0000000000a2','ad2@x');
update public.profiles set is_admin = true where id = '00000000-0000-0000-0000-0000000000a2';
create function pg_temp.as_user(u text) returns void language plpgsql as $$ begin perform set_config('request.jwt.claim.sub', u, false); end $$;
create function pg_temp.expect_fail(q text, label text) returns void language plpgsql as $$
begin begin execute q; exception when others then raise notice 'OK  % (blocked: %)', label, sqlerrm; return; end; raise exception 'FAIL % was allowed', label; end $$;
create function pg_temp.check(cond boolean, label text) returns void language plpgsql as $$ begin if cond then raise notice 'OK  %', label; else raise exception 'FAIL %', label; end if; end $$;
set role authenticated;
-- two verified garages A and B
select pg_temp.as_user('00000000-0000-0000-0000-00000000006a');
insert into public.garage_profiles (id, garage_id, owner_id, name, city) values ('a0000000-0000-0000-0000-00000000000a', 501, '00000000-0000-0000-0000-00000000006a', 'מוסך א', 'חולון');
select pg_temp.as_user('00000000-0000-0000-0000-00000000006b');
insert into public.garage_profiles (id, garage_id, owner_id, name, city) values ('b0000000-0000-0000-0000-00000000000b', 502, '00000000-0000-0000-0000-00000000006b', 'מוסך ב', 'בת ים');
select pg_temp.as_user('00000000-0000-0000-0000-0000000000a2');
select public.set_garage_status('a0000000-0000-0000-0000-00000000000a', 'verified'), public.set_garage_status('b0000000-0000-0000-0000-00000000000b', 'verified');
-- garage A adds its own customer (no app) and a work order
select pg_temp.as_user('00000000-0000-0000-0000-00000000006a');
insert into public.garage_customers (id, garage_id, name, phone, contact_consent) values ('c0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-00000000000a', 'יוסי', '052-1111111', true);
insert into public.garage_cars (id, garage_id, customer_id, plate, schedule_id, year, km) values ('ca000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-00000000000a', 'c0000000-0000-0000-0000-000000000001', '5556667', 'kia-picanto-2017-2025', 2019, 70000);
insert into public.work_orders (garage_id, garage_car_id, kind, svc_km, km, date, items, lines, total) values ('a0000000-0000-0000-0000-00000000000a', 'ca000000-0000-0000-0000-000000000001', 'service', 75000, 70000, '2026-09-20', '{engine_oil,oil_filter}', '[{"type":"part","desc":"מסנן שמן","qty":1,"price":45}]', 690);
select pg_temp.check((select count(*) from public.garage_book('a0000000-0000-0000-0000-00000000000a')) = 1, 'garage sees its own customer');
select pg_temp.check((select visits from public.garage_book('a0000000-0000-0000-0000-00000000000a')) = 1 and (select last_visit from public.garage_book('a0000000-0000-0000-0000-00000000000a')) = '2026-09-20', 'visits and last visit');
-- garage B cannot read or write A's book
select pg_temp.as_user('00000000-0000-0000-0000-00000000006b');
select pg_temp.check((select count(*) from public.garage_customers) = 0 and (select count(*) from public.work_orders) = 0, 'other garage reads nothing');
select pg_temp.expect_fail($q$select * from public.garage_book('a0000000-0000-0000-0000-00000000000a')$q$, 'other garage reads the book');
select pg_temp.expect_fail($q$insert into public.garage_customers (garage_id, name) values ('a0000000-0000-0000-0000-00000000000a', 'x')$q$, 'other garage writes the book');
insert into public.garage_customers (id, garage_id, name) values ('c0000000-0000-0000-0000-0000000000b1', 'b0000000-0000-0000-0000-00000000000b', 'שלי');
select pg_temp.expect_fail($q$insert into public.garage_cars (garage_id, customer_id, plate) values ('b0000000-0000-0000-0000-00000000000b', 'c0000000-0000-0000-0000-000000000001', '1')$q$, 'car under another garage''s customer');
-- driver D joins garage B, with full history shared but no garage names; D has history from garage A and own entries
select pg_temp.as_user('00000000-0000-0000-0000-0000000000d2');
insert into public.cars (id, user_id, plate, schedule_id, year, km, km_month, gov) values ('cd000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-0000000000d2','7778889','hyundai-i10-2014-2019',2016,90000,1200,'{"test_expiry":"2026-12-01"}');
insert into public.records (car_id, user_id, kind, svc_km, km, date, garage, price, source, items) values
  ('cd000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-0000000000d2','service',75000,74800,'2025-06','מוסך א',820,'garage','{engine_oil}'),
  ('cd000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-0000000000d2','repair',null,80000,'2025-11','',300,'log','{battery}');
insert into public.garage_links (id, garage_id, car_id, user_id, first_name, phone, allow_contact, share_history) values ('1d000000-0000-0000-0000-000000000001','b0000000-0000-0000-0000-00000000000b','cd000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-0000000000d2','דנה','050-2222222', false, true);
select pg_temp.as_user('00000000-0000-0000-0000-00000000006b');
select pg_temp.check((select count(*) from public.garage_book('b0000000-0000-0000-0000-00000000000b') where linked) = 1, 'joining driver appears in the book');
select pg_temp.check((select phone from public.garage_book('b0000000-0000-0000-0000-00000000000b') where linked) is null, 'no phone without contact consent');
select pg_temp.check((select km from public.garage_book('b0000000-0000-0000-0000-00000000000b') where linked) = 90000, 'live km from the driver');
select pg_temp.check((select count(*) from public.garage_car_history((select car_id from public.garage_book('b0000000-0000-0000-0000-00000000000b') where linked))) = 2, 'shared history visible');
select pg_temp.check((select garage from public.garage_car_history((select car_id from public.garage_book('b0000000-0000-0000-0000-00000000000b') where linked)) where kind = 'service') = 'מוסך אחר', 'other garage name hidden by default');
select pg_temp.check((select verified from public.garage_car_history((select car_id from public.garage_book('b0000000-0000-0000-0000-00000000000b') where linked)) where kind = 'service'), 'garage-entered record marked verified');
select pg_temp.check(not (select verified from public.garage_car_history((select car_id from public.garage_book('b0000000-0000-0000-0000-00000000000b') where linked)) where kind = 'repair'), 'driver-entered record not verified');
-- the driver turns names on, then stops sharing history
select pg_temp.as_user('00000000-0000-0000-0000-0000000000d2');
update public.garage_links set show_garage_names = true, allow_contact = true where id = '1d000000-0000-0000-0000-000000000001';
select pg_temp.as_user('00000000-0000-0000-0000-00000000006b');
select pg_temp.check((select garage from public.garage_car_history((select car_id from public.garage_book('b0000000-0000-0000-0000-00000000000b') where linked)) where kind = 'service') = 'מוסך א', 'names shown when the driver allows');
select pg_temp.check((select phone from public.garage_book('b0000000-0000-0000-0000-00000000000b') where linked) = '050-2222222', 'phone after consent');
select pg_temp.as_user('00000000-0000-0000-0000-0000000000d2');
update public.garage_links set share_history = false where id = '1d000000-0000-0000-0000-000000000001';
select pg_temp.as_user('00000000-0000-0000-0000-00000000006b');
select pg_temp.check((select count(*) from public.garage_car_history((select car_id from public.garage_book('b0000000-0000-0000-0000-00000000000b') where linked))) = 0, 'history hidden after the driver turns it off');
-- garage B logs a work order and sends it to the driver
insert into public.work_orders (id, garage_id, garage_car_id, kind, svc_km, km, date, total, notes) values ('e0000000-0000-0000-0000-000000000001','b0000000-0000-0000-0000-00000000000b',(select car_id from public.garage_book('b0000000-0000-0000-0000-00000000000b') where linked),'service',95000,94000,'2026-10-01',950,'שמן ומסנן');
select public.work_order_send('e0000000-0000-0000-0000-000000000001', 'independent');
select pg_temp.check((select pending from public.garage_book('b0000000-0000-0000-0000-00000000000b') where linked) = 1, 'sent work order waits for the driver');
select pg_temp.as_user('00000000-0000-0000-0000-00000000006a');
select pg_temp.expect_fail($q$select public.work_order_send('e0000000-0000-0000-0000-000000000001', 'independent')$q$, 'another garage sends B''s work order');
-- A driver who already was A's customer joins A: connected, not duplicated
select pg_temp.as_user('00000000-0000-0000-0000-0000000000d2');
update public.cars set plate = '5556667' where id = 'cd000000-0000-0000-0000-000000000001';
insert into public.garage_links (garage_id, car_id, user_id, first_name, allow_contact) values ('a0000000-0000-0000-0000-00000000000a','cd000000-0000-0000-0000-000000000001','00000000-0000-0000-0000-0000000000d2','דנה', true);
select pg_temp.as_user('00000000-0000-0000-0000-00000000006a');
select pg_temp.check((select count(*) from public.garage_book('a0000000-0000-0000-0000-00000000000a')) = 1 and (select linked from public.garage_book('a0000000-0000-0000-0000-00000000000a')), 'existing customer connected, not duplicated');
-- the driver leaves garage B: app contact details are cleared, the garage keeps its own work order
select pg_temp.as_user('00000000-0000-0000-0000-0000000000d2');
delete from public.garage_links where id = '1d000000-0000-0000-0000-000000000001';
select pg_temp.as_user('00000000-0000-0000-0000-00000000006b');
select pg_temp.check((select phone is null and not can_contact and not linked from public.garage_book('b0000000-0000-0000-0000-00000000000b') where name = 'דנה'), 'contact cleared after the driver leaves');
select pg_temp.check((select count(*) from public.work_orders) = 1, 'garage keeps its own work order');
