-- Run with: sh scripts/test-db.sh
-- Modules, job catalog, inspection results and line-by-line approval (migration 0008).
\set ON_ERROR_STOP 1
insert into auth.users (id, email) values ('00000000-0000-0000-0000-0000000000c7','c1@x'),('00000000-0000-0000-0000-0000000000c8','c2@x'),('00000000-0000-0000-0000-0000000000c9','cadm@x');
update public.profiles set is_admin = true where id = '00000000-0000-0000-0000-0000000000c9';
create function pg_temp.as_user(u text) returns void language plpgsql as $$ begin perform set_config('request.jwt.claim.sub', u, false); end $$;
create function pg_temp.expect_fail(q text, label text) returns void language plpgsql as $$
begin begin execute q; exception when others then raise notice 'OK  % (blocked: %)', label, sqlerrm; return; end; raise exception 'FAIL % was allowed', label; end $$;
create function pg_temp.check(cond boolean, label text) returns void language plpgsql as $$ begin if cond then raise notice 'OK  %', label; else raise exception 'FAIL %', label; end if; end $$;
set role authenticated;
select pg_temp.as_user('00000000-0000-0000-0000-0000000000c7');
insert into public.garage_profiles (id, garage_id, owner_id, name, city) values ('d1000000-0000-0000-0000-000000000001', 701, '00000000-0000-0000-0000-0000000000c7', 'מוסך מחירון', 'יבנה');
select pg_temp.as_user('00000000-0000-0000-0000-0000000000c8');
insert into public.garage_profiles (id, garage_id, owner_id, name, city) values ('d2000000-0000-0000-0000-000000000002', 702, '00000000-0000-0000-0000-0000000000c8', 'מוסך שכן', 'יבנה');
select pg_temp.as_user('00000000-0000-0000-0000-0000000000c9');
select public.set_garage_status('d1000000-0000-0000-0000-000000000001','verified'), public.set_garage_status('d2000000-0000-0000-0000-000000000002','verified');

-- owner: modules, labour rate, catalog
select pg_temp.as_user('00000000-0000-0000-0000-0000000000c7');
update public.garage_profiles set modules = array['stock','catalog'], labor_rate = 280 where id = 'd1000000-0000-0000-0000-000000000001';
select pg_temp.check((select modules = array['stock','catalog'] and labor_rate = 280 and status = 'verified' from public.garage_profiles where id = 'd1000000-0000-0000-0000-000000000001'), 'garage saves its modules and labour rate, stays verified');
insert into public.job_templates (id, garage_id, name, category, hours, parts) values ('d1b00000-0000-0000-0000-000000000001', 'd1000000-0000-0000-0000-000000000001', 'רפידות קדמיות', 'בלמים', 1, '[{"item":"brake_pads","qty":1}]');
select pg_temp.check((select count(*) from public.job_templates) = 1, 'owner sees its catalog');
select pg_temp.expect_fail($q$insert into public.job_templates (garage_id, name, hours) values ('d1000000-0000-0000-0000-000000000001', 'שלילי', -1)$q$, 'negative hours');

-- an inspection sent as an approval with three recommended lines
insert into public.work_approvals (id, garage_id, car_label, message, lines, total, checks, km) values ('d1a00000-0000-0000-0000-000000000001', 'd1000000-0000-0000-0000-000000000001', 'מאזדה 3', 'תוצאות בדיקת הרכב',
  '[{"desc":"רפידות קדמיות","price":420},{"desc":"מגבים","price":90},{"desc":"נוזל בלמים","price":180}]', 690,
  '[{"key":"brakes_front","label":"בלמים קדמיים","status":"now","photos":["https://x/p.jpg"]},{"key":"wipers","label":"מגבים","status":"soon"},{"key":"lights","label":"אורות","status":"ok"}]', 81200);
insert into public.work_approvals (id, garage_id, message, lines, total) values ('d1a00000-0000-0000-0000-000000000002', 'd1000000-0000-0000-0000-000000000001', 'עבודה', '[{"desc":"מצבר","price":450}]', 450);

-- the customer, not signed in
reset role; set role anon; select pg_temp.as_user('');
select pg_temp.check((public.approval_get('d1a00000-0000-0000-0000-000000000001') -> 'checks' -> 0 ->> 'status') = 'now' and (public.approval_get('d1a00000-0000-0000-0000-000000000001') ->> 'km')::int = 81200, 'customer page gets the checks and km');
select pg_temp.check((public.approval_choose('d1a00000-0000-0000-0000-000000000001', array[2, 0, 0, 7, -1]) ->> 'status') = 'approved', 'customer approves some lines');
select pg_temp.check((public.approval_get('d1a00000-0000-0000-0000-000000000001') -> 'approved_lines')::text = '[0, 2]', 'only valid lines kept, sorted, no duplicates');
select pg_temp.check((public.approval_choose('d1a00000-0000-0000-0000-000000000001', array[1]) -> 'approved_lines')::text = '[0, 2]', 'second answer changes nothing');
select pg_temp.check((public.approval_choose('d1a00000-0000-0000-0000-000000000002', array[]::int[]) ->> 'status') = 'declined', 'approving nothing declines');
select pg_temp.expect_fail($q$select public.approval_choose('d1a00000-0000-0000-0000-0000000000ff', array[0])$q$, 'unknown approval');
select pg_temp.check((select count(*) from public.job_templates) = 0, 'anonymous sees no catalog');

-- an inspection points at the garage's own car only
reset role; set role authenticated; select pg_temp.as_user('00000000-0000-0000-0000-0000000000c7');
insert into public.garage_customers (id, garage_id, name) values ('d1c00000-0000-0000-0000-000000000001', 'd1000000-0000-0000-0000-000000000001', 'נועה');
insert into public.garage_cars (id, garage_id, customer_id, plate) values ('d1ca0000-0000-0000-0000-000000000001', 'd1000000-0000-0000-0000-000000000001', 'd1c00000-0000-0000-0000-000000000001', '5556667');
insert into public.work_approvals (garage_id, garage_car_id, message, lines, total) values ('d1000000-0000-0000-0000-000000000001', 'd1ca0000-0000-0000-0000-000000000001', 'בדיקה', '[]', 0);
select pg_temp.check((select count(*) from public.work_approvals where garage_car_id = 'd1ca0000-0000-0000-0000-000000000001') = 1, 'inspection saved for the car');
-- another garage
reset role; set role authenticated; select pg_temp.as_user('00000000-0000-0000-0000-0000000000c8');
select pg_temp.check((select count(*) from public.job_templates) = 0, 'other garage sees no catalog');
select pg_temp.expect_fail($q$insert into public.job_templates (garage_id, name) values ('d1000000-0000-0000-0000-000000000001', 'זר')$q$, 'adding to another garage''s catalog');
select pg_temp.expect_fail($q$insert into public.work_approvals (garage_id, garage_car_id, lines, total) values ('d2000000-0000-0000-0000-000000000002', 'd1ca0000-0000-0000-0000-000000000001', '[]', 0)$q$, 'inspection on another garage''s car');
update public.garage_profiles set modules = array['x'] where id = 'd1000000-0000-0000-0000-000000000001';
select pg_temp.as_user('00000000-0000-0000-0000-0000000000c7');
select pg_temp.check((select modules from public.garage_profiles where id = 'd1000000-0000-0000-0000-000000000001') = array['stock','catalog'], 'other garage cannot change the modules');

-- photos go only into the garage's own folder
insert into storage.objects (bucket_id, name) values ('inspection-photos', 'd1000000-0000-0000-0000-000000000001/a.jpg');
select pg_temp.check(true, 'owner uploads into its folder');
select pg_temp.expect_fail($q$insert into storage.objects (bucket_id, name) values ('inspection-photos', 'd2000000-0000-0000-0000-000000000002/b.jpg')$q$, 'upload into another garage''s folder');
select pg_temp.expect_fail($q$insert into storage.objects (bucket_id, name) values ('inspection-photos', 'nofolder.jpg')$q$, 'upload outside a garage folder');
reset role;
select pg_temp.check((select public from storage.buckets where id = 'inspection-photos'), 'photo bucket is public-read');
