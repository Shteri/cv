-- Run with: sh scripts/test-db.sh
-- Appointments, online booking and extra-work approvals (migration 0006).
\set ON_ERROR_STOP 1
insert into auth.users (id, email) values ('00000000-0000-0000-0000-0000000000f1','g1@x'),('00000000-0000-0000-0000-0000000000f2','g2@x'),('00000000-0000-0000-0000-0000000000fa','adm@x');
update public.profiles set is_admin = true where id = '00000000-0000-0000-0000-0000000000fa';
create function pg_temp.as_user(u text) returns void language plpgsql as $$ begin perform set_config('request.jwt.claim.sub', u, false); end $$;
create function pg_temp.expect_fail(q text, label text) returns void language plpgsql as $$
begin begin execute q; exception when others then raise notice 'OK  % (blocked: %)', label, sqlerrm; return; end; raise exception 'FAIL % was allowed', label; end $$;
create function pg_temp.check(cond boolean, label text) returns void language plpgsql as $$ begin if cond then raise notice 'OK  %', label; else raise exception 'FAIL %', label; end if; end $$;
-- a Sunday 10:00 Israel time, 7 to 13 days ahead
create function pg_temp.sun(h int) returns timestamptz language sql as $$ select (date_trunc('week', now() at time zone 'Asia/Jerusalem') + interval '13 days' + make_interval(hours => h)) at time zone 'Asia/Jerusalem' $$;
set role authenticated;
select pg_temp.as_user('00000000-0000-0000-0000-0000000000f1');
insert into public.garage_profiles (id, garage_id, owner_id, name, city, phone) values ('f1000000-0000-0000-0000-000000000001', 901, '00000000-0000-0000-0000-0000000000f1', 'מוסך תור', 'חולון', '03-5555555');
select pg_temp.as_user('00000000-0000-0000-0000-0000000000f2');
insert into public.garage_profiles (id, garage_id, owner_id, name, city) values ('f2000000-0000-0000-0000-000000000002', 902, '00000000-0000-0000-0000-0000000000f2', 'מוסך שכן', 'חולון');
select pg_temp.as_user('00000000-0000-0000-0000-0000000000fa');
select public.set_garage_status('f1000000-0000-0000-0000-000000000001','verified'), public.set_garage_status('f2000000-0000-0000-0000-000000000002','verified');
-- owner: a customer in the book, booking settings (1 bay, 60 minutes), booking still off
select pg_temp.as_user('00000000-0000-0000-0000-0000000000f1');
insert into public.garage_customers (id, garage_id, name) values ('f1c00000-0000-0000-0000-000000000001','f1000000-0000-0000-0000-000000000001','רון');
insert into public.garage_cars (id, garage_id, customer_id, plate) values ('f1ca0000-0000-0000-0000-000000000001','f1000000-0000-0000-0000-000000000001','f1c00000-0000-0000-0000-000000000001','4445556');
update public.garage_profiles set bays = 1, slot_minutes = 60 where id = 'f1000000-0000-0000-0000-000000000001';
select pg_temp.check((select status from public.garage_profiles where id='f1000000-0000-0000-0000-000000000001') = 'verified', 'settings update keeps verification');
reset role; set role anon; select pg_temp.as_user('');
select pg_temp.check((public.booking_info('f1000000-0000-0000-0000-000000000001') ->> 'enabled')::boolean = false, 'booking page sees booking is off');
select pg_temp.expect_fail(format($q$select public.book_appointment('f1000000-0000-0000-0000-000000000001', %L, 'דנה', '050-1234567', '', 'service', '')$q$, pg_temp.sun(10)), 'book while booking is off');
reset role; set role authenticated; select pg_temp.as_user('00000000-0000-0000-0000-0000000000f1');
update public.garage_profiles set booking_enabled = true where id = 'f1000000-0000-0000-0000-000000000001';
-- anonymous customer books
reset role; set role anon; select pg_temp.as_user('');
select public.book_appointment('f1000000-0000-0000-0000-000000000001', pg_temp.sun(10), 'דנה', '050-1234567', '444-55-56', 'service', 'רעש בבלמים') as appt \gset
select pg_temp.check(jsonb_array_length(public.booking_info('f1000000-0000-0000-0000-000000000001') -> 'busy') = 1, 'busy slot visible to the booking page');
select pg_temp.check(public.booking_info('f1000000-0000-0000-0000-000000000001')::text not like '%דנה%' and public.booking_info('f1000000-0000-0000-0000-000000000001')::text not like '%050%', 'booking page shows no names or phones');
select pg_temp.expect_fail(format($q$select public.book_appointment('f1000000-0000-0000-0000-000000000001', %L, 'יוסי', '052-7654321', '', 'service', '')$q$, pg_temp.sun(10)), 'same slot when the only bay is taken');
select pg_temp.expect_fail(format($q$select public.book_appointment('f1000000-0000-0000-0000-000000000001', %L, 'יוסי', '052-7654321', '', 'service', '')$q$, pg_temp.sun(10) + interval '30 minutes'), 'overlapping slot');
select pg_temp.expect_fail(format($q$select public.book_appointment('f1000000-0000-0000-0000-000000000001', %L, 'יוסי', '052-7654321', '', 'service', '')$q$, pg_temp.sun(20)), 'after closing time');
select pg_temp.expect_fail(format($q$select public.book_appointment('f1000000-0000-0000-0000-000000000001', %L, 'יוסי', '052-7654321', '', 'service', '')$q$, pg_temp.sun(10) - interval '1 day'), 'on Saturday');
select pg_temp.expect_fail(format($q$select public.book_appointment('f1000000-0000-0000-0000-000000000001', %L, 'יוסי', '052-7654321', '', 'service', '')$q$, now() - interval '1 hour'), 'in the past');
select pg_temp.expect_fail(format($q$select public.book_appointment('f1000000-0000-0000-0000-000000000001', %L, '', '052-7654321', '', 'service', '')$q$, pg_temp.sun(12)), 'without a name');
select pg_temp.check((select count(*) from public.appointments) = 0, 'anonymous sees no appointments');
select public.book_appointment('f1000000-0000-0000-0000-000000000001', pg_temp.sun(12), 'דנה', '0501234567', '', 'service', '');
select public.book_appointment('f1000000-0000-0000-0000-000000000001', pg_temp.sun(13), 'דנה', '050-123-4567', '', 'service', '');
select pg_temp.expect_fail(format($q$select public.book_appointment('f1000000-0000-0000-0000-000000000001', %L, 'דנה', '050 1234567', '', 'service', '')$q$, pg_temp.sun(14)), 'fourth open booking for the same phone');
-- owner sees the booking, linked to the car in the book; neighbour garage does not
reset role; set role authenticated; select pg_temp.as_user('00000000-0000-0000-0000-0000000000f1');
select pg_temp.check((select garage_car_id from public.appointments where id = :'appt') = 'f1ca0000-0000-0000-0000-000000000001', 'online booking linked to the car by plate');
select pg_temp.check((select count(*) from public.appointments) = 3, 'owner sees the bookings');
select pg_temp.as_user('00000000-0000-0000-0000-0000000000f2');
select pg_temp.check((select count(*) from public.appointments) = 0, 'other garage sees nothing');
update public.appointments set status = 'cancelled' where id = :'appt';
select pg_temp.expect_fail($q$insert into public.appointments (garage_id, customer_name, starts_at) values ('f1000000-0000-0000-0000-000000000001', 'x', now() + interval '1 day')$q$, 'other garage inserts into the calendar');
select pg_temp.expect_fail(format($q$insert into public.work_approvals (garage_id, appointment_id) values ('f2000000-0000-0000-0000-000000000002', %L)$q$, :'appt'), 'approval tied to another garage''s appointment');
-- owner asks the customer to approve extra work
select pg_temp.as_user('00000000-0000-0000-0000-0000000000f1');
select pg_temp.check((select status from public.appointments where id = :'appt') = 'booked', 'other garage could not cancel the booking');
update public.appointments set status = 'waiting_approval' where id = :'appt';
insert into public.work_approvals (id, garage_id, appointment_id, car_label, message, lines, total) values ('f1a00000-0000-0000-0000-0000000000a1','f1000000-0000-0000-0000-000000000001', :'appt', 'קיה פיקנטו 2019', 'מצאנו רפידות שחוקות', '[{"desc":"רפידות קדמיות","price":480}]', 480);
reset role; set role anon; select pg_temp.as_user('');
select pg_temp.check((public.approval_get('f1a00000-0000-0000-0000-0000000000a1') ->> 'total')::int = 480, 'customer opens the approval link');
select pg_temp.check(public.approval_decide('f1a00000-0000-0000-0000-0000000000a1', true) = 'approved', 'customer approves');
select pg_temp.check(public.approval_decide('f1a00000-0000-0000-0000-0000000000a1', false) = 'approved', 'second answer does not change the first');
select pg_temp.check(public.approval_get('00000000-0000-0000-0000-00000000dead') is null, 'unknown approval id returns nothing');
select pg_temp.check((select count(*) from public.work_approvals) = 0, 'anonymous cannot list approvals');
reset role; set role authenticated; select pg_temp.as_user('00000000-0000-0000-0000-0000000000f1');
select pg_temp.check((select status from public.appointments where id = :'appt') = 'in_progress', 'appointment back to work after the answer');
select pg_temp.check((select decided_at is not null from public.work_approvals where id = 'f1a00000-0000-0000-0000-0000000000a1'), 'decision time recorded');
