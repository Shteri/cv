-- Run with: sh scripts/test-db.sh
-- community_garages (migration 0013): drivers, not visits; the caller's own cars are left out.
\set ON_ERROR_STOP 1
insert into auth.users (id, email) values ('00000000-0000-0000-0000-00000000c0d1','d1@x'),('00000000-0000-0000-0000-00000000c0d2','d2@x'),('00000000-0000-0000-0000-00000000c0d3','d3@x');
create function pg_temp.as_user(u text) returns void language plpgsql as $$ begin perform set_config('request.jwt.claim.sub', u, false); end $$;
create function pg_temp.check(cond boolean, label text) returns void language plpgsql as $$ begin if cond then raise notice 'OK  %', label; else raise exception 'FAIL %', label; end if; end $$;
set role authenticated;
-- d1 went to the same garage three times, happy once and then not
select pg_temp.as_user('00000000-0000-0000-0000-00000000c0d1');
insert into public.cars (id, user_id, schedule_id, km) values ('dddddddd-0000-0000-0000-00000000c0d1','00000000-0000-0000-0000-00000000c0d1','comm-x', 90000);
insert into public.records (car_id, user_id, kind, km, "where", garage, city, price, back, share) values
  ('dddddddd-0000-0000-0000-00000000c0d1','00000000-0000-0000-0000-00000000c0d1','service', 30000,'independent','מוסך בדיקה','נתניה', 900, 'yes', true),
  ('dddddddd-0000-0000-0000-00000000c0d1','00000000-0000-0000-0000-00000000c0d1','service', 60000,'independent','מוסך בדיקה','נתניה', 1100, 'yes', true),
  ('dddddddd-0000-0000-0000-00000000c0d1','00000000-0000-0000-0000-00000000c0d1','service', 90000,'independent','מוסך בדיקה','נתניה', 1300, 'no', true);
-- d2 went once
select pg_temp.as_user('00000000-0000-0000-0000-00000000c0d2');
insert into public.cars (id, user_id, schedule_id, km) values ('dddddddd-0000-0000-0000-00000000c0d2','00000000-0000-0000-0000-00000000c0d2','comm-x', 40000);
insert into public.records (car_id, user_id, kind, km, "where", garage, city, price, back, share) values
  ('dddddddd-0000-0000-0000-00000000c0d2','00000000-0000-0000-0000-00000000c0d2','service', 30000,'independent','מוסך בדיקה','נתניה', 1000, 'yes', true);
-- a third driver sees two drivers, and each counts once, by their latest visit
select pg_temp.as_user('00000000-0000-0000-0000-00000000c0d3');
select pg_temp.check((select n from public.community_garages('comm-x') where garage = 'מוסך בדיקה') = 2, 'two drivers, not four visits');
select pg_temp.check((select back_pct from public.community_garages('comm-x') where garage = 'מוסך בדיקה') = 50, 'each driver''s latest opinion counts once');
select pg_temp.check((select avg_price from public.community_garages('comm-x') where garage = 'מוסך בדיקה') = 1075, 'average price over all reports');
-- d1 sees only d2: the app adds d1 from the device
select pg_temp.as_user('00000000-0000-0000-0000-00000000c0d1');
select pg_temp.check((select n from public.community_garages('comm-x') where garage = 'מוסך בדיקה') = 1, 'own car left out');
-- anonymous sees both
reset role; set role anon; select set_config('request.jwt.claim.sub', '', false);
select pg_temp.check((select n from public.community_garages('comm-x') where garage = 'מוסך בדיקה') = 2, 'anonymous sees all drivers');
reset role;
