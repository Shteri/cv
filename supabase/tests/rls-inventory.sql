-- Run with: sh scripts/test-db.sh
-- Parts, suppliers, purchase orders, stock ledger, invoices and invoicing settings (migration 0007).
\set ON_ERROR_STOP 1
insert into auth.users (id, email) values ('00000000-0000-0000-0000-0000000000e1','i1@x'),('00000000-0000-0000-0000-0000000000e2','i2@x'),('00000000-0000-0000-0000-0000000000ea','iadm@x');
update public.profiles set is_admin = true where id = '00000000-0000-0000-0000-0000000000ea';
create function pg_temp.as_user(u text) returns void language plpgsql as $$ begin perform set_config('request.jwt.claim.sub', u, false); end $$;
create function pg_temp.expect_fail(q text, label text) returns void language plpgsql as $$
begin begin execute q; exception when others then raise notice 'OK  % (blocked: %)', label, sqlerrm; return; end; raise exception 'FAIL % was allowed', label; end $$;
create function pg_temp.check(cond boolean, label text) returns void language plpgsql as $$ begin if cond then raise notice 'OK  %', label; else raise exception 'FAIL %', label; end if; end $$;
set role authenticated;
select pg_temp.as_user('00000000-0000-0000-0000-0000000000e1');
insert into public.garage_profiles (id, garage_id, owner_id, name, city) values ('e1000000-0000-0000-0000-000000000001', 801, '00000000-0000-0000-0000-0000000000e1', 'מוסך מלאי', 'רמלה');
select pg_temp.as_user('00000000-0000-0000-0000-0000000000e2');
insert into public.garage_profiles (id, garage_id, owner_id, name, city) values ('e2000000-0000-0000-0000-000000000002', 802, '00000000-0000-0000-0000-0000000000e2', 'מוסך אחר', 'לוד');
-- before verification the garage cannot keep stock
select pg_temp.expect_fail($q$insert into public.parts (garage_id, name) values ('e2000000-0000-0000-0000-000000000002', 'מסנן')$q$, 'parts before the garage is verified');
select pg_temp.as_user('00000000-0000-0000-0000-0000000000ea');
select public.set_garage_status('e1000000-0000-0000-0000-000000000001','verified'), public.set_garage_status('e2000000-0000-0000-0000-000000000002','verified');

-- owner 1: supplier, parts, a car with a work order
select pg_temp.as_user('00000000-0000-0000-0000-0000000000e1');
insert into public.suppliers (id, garage_id, name, phone) values ('e1500000-0000-0000-0000-000000000001', 'e1000000-0000-0000-0000-000000000001', 'חלפים בע"מ', '03-1111111');
insert into public.parts (id, garage_id, sku, name, item_key, unit, min_stock, cost, price, supplier_id) values
  ('e1a00000-0000-0000-0000-000000000001', 'e1000000-0000-0000-0000-000000000001', 'OF-100', 'מסנן שמן', 'oil_filter', 'unit', 5, 25, 60, 'e1500000-0000-0000-0000-000000000001'),
  ('e1a00000-0000-0000-0000-000000000002', 'e1000000-0000-0000-0000-000000000001', 'OIL-5W30', 'שמן 5W-30', 'engine_oil', 'liter', 20, 30, 55, null);
select pg_temp.expect_fail($q$insert into public.parts (garage_id, sku, name) values ('e1000000-0000-0000-0000-000000000001', 'of-100', 'כפול')$q$, 'same SKU twice (case-insensitive)');
insert into public.garage_customers (id, garage_id, name) values ('e1c00000-0000-0000-0000-000000000001','e1000000-0000-0000-0000-000000000001','שרה');
insert into public.garage_cars (id, garage_id, customer_id, plate) values ('e1ca0000-0000-0000-0000-000000000001','e1000000-0000-0000-0000-000000000001','e1c00000-0000-0000-0000-000000000001','7778889');

-- purchase order with running number, then receive
insert into public.purchase_orders (id, garage_id, supplier_id, status, lines, total) values
  ('e1b00000-0000-0000-0000-000000000001', 'e1000000-0000-0000-0000-000000000001', 'e1500000-0000-0000-0000-000000000001', 'sent',
   '[{"part_id":"e1a00000-0000-0000-0000-000000000001","name":"מסנן שמן","qty":10,"cost":25},{"part_id":"e1a00000-0000-0000-0000-000000000002","name":"שמן","qty":40,"cost":30}]', 1450);
insert into public.purchase_orders (id, garage_id, status) values ('e1b00000-0000-0000-0000-000000000002', 'e1000000-0000-0000-0000-000000000001', 'draft');
select pg_temp.check((select array_agg(number order by number) from public.purchase_orders where garage_id = 'e1000000-0000-0000-0000-000000000001') = array[1,2], 'purchase orders numbered 1, 2');
select public.po_receive('e1b00000-0000-0000-0000-000000000001', '[{"part_id":"e1a00000-0000-0000-0000-000000000001","qty":10,"cost":24},{"part_id":"e1a00000-0000-0000-0000-000000000002","qty":36}]');
select pg_temp.check((select stock from public.parts where id = 'e1a00000-0000-0000-0000-000000000001') = 10 and (select stock from public.parts where id = 'e1a00000-0000-0000-0000-000000000002') = 36, 'receiving adds stock (short delivery counted as delivered)');
select pg_temp.check((select cost from public.parts where id = 'e1a00000-0000-0000-0000-000000000001') = 24, 'receiving updates the cost');
select pg_temp.check((select status from public.purchase_orders where id = 'e1b00000-0000-0000-0000-000000000001') = 'received'
  and (select (lines -> 1 ->> 'received')::numeric from public.purchase_orders where id = 'e1b00000-0000-0000-0000-000000000001') = 36, 'order marked received with quantities');
select pg_temp.expect_fail($q$select public.po_receive('e1b00000-0000-0000-0000-000000000001', '[{"part_id":"e1a00000-0000-0000-0000-000000000001","qty":10}]')$q$, 'receiving the same order twice');

-- work order uses stock; saving again re-syncs, deleting gives it back
insert into public.work_orders (id, garage_id, garage_car_id, kind, lines, total) values ('e1d00000-0000-0000-0000-000000000001', 'e1000000-0000-0000-0000-000000000001', 'e1ca0000-0000-0000-0000-000000000001', 'service',
  '[{"type":"part","desc":"מסנן שמן","qty":1,"price":60,"part_id":"e1a00000-0000-0000-0000-000000000001"},{"type":"part","desc":"שמן","qty":4.5,"price":55,"part_id":"e1a00000-0000-0000-0000-000000000002"},{"type":"labor","desc":"עבודה","qty":1,"price":200}]', 507);
select public.wo_consume('e1d00000-0000-0000-0000-000000000001');
select pg_temp.check((select stock from public.parts where id = 'e1a00000-0000-0000-0000-000000000002') = 31.5, 'work order uses 4.5 liters of oil');
update public.work_orders set lines = jsonb_set(lines, '{1,qty}', '4') where id = 'e1d00000-0000-0000-0000-000000000001';
select public.wo_consume('e1d00000-0000-0000-0000-000000000001');
select pg_temp.check((select stock from public.parts where id = 'e1a00000-0000-0000-0000-000000000002') = 32 and (select stock from public.parts where id = 'e1a00000-0000-0000-0000-000000000001') = 9, 'saving again re-syncs instead of using twice');
insert into public.stock_moves (garage_id, part_id, qty, reason, note) values ('e1000000-0000-0000-0000-000000000001', 'e1a00000-0000-0000-0000-000000000001', -1, 'adjust', 'ספירה');
select pg_temp.check((select stock from public.parts where id = 'e1a00000-0000-0000-0000-000000000001') = 8, 'manual count adjusts stock');
delete from public.work_orders where id = 'e1d00000-0000-0000-0000-000000000001';
select pg_temp.check((select stock from public.parts where id = 'e1a00000-0000-0000-0000-000000000001') = 9 and (select stock from public.parts where id = 'e1a00000-0000-0000-0000-000000000002') = 36, 'deleting the work order returns its parts');
select pg_temp.expect_fail($q$update public.stock_moves set qty = 100 where part_id = 'e1a00000-0000-0000-0000-000000000001'$q$, 'editing a ledger row');
select pg_temp.check((select stock from public.parts where id = 'e1a00000-0000-0000-0000-000000000001') = 9, 'ledger rows cannot be edited');

-- invoices: manual record only
insert into public.work_orders (id, garage_id, garage_car_id, kind, lines, total) values ('e1d00000-0000-0000-0000-000000000002', 'e1000000-0000-0000-0000-000000000001', 'e1ca0000-0000-0000-0000-000000000001', 'repair', '[]', 300);
insert into public.invoices (garage_id, work_order_id, kind, provider, number, total, payment) values ('e1000000-0000-0000-0000-000000000001', 'e1d00000-0000-0000-0000-000000000002', 'invoice_receipt', 'manual', '10234', 300, 'card');
select pg_temp.expect_fail($q$insert into public.invoices (garage_id, kind, provider, number) values ('e1000000-0000-0000-0000-000000000001', 'invoice_receipt', 'morning', '1')$q$, 'client pretending an invoice came from Morning');

-- invoicing settings: secret is write-only
select public.billing_save('e1000000-0000-0000-0000-000000000001', 'api-id-1', 'top-secret', true, false);
select pg_temp.check((select has_secret and api_id = 'api-id-1' and sandbox from public.garage_billing where garage_id = 'e1000000-0000-0000-0000-000000000001'), 'owner sees id and that a secret is set');
select pg_temp.expect_fail($q$select api_secret from public.garage_billing$q$, 'owner reads the secret back');
select pg_temp.expect_fail($q$update public.garage_billing set api_id = 'x'$q$, 'direct update of settings');
select public.billing_save('e1000000-0000-0000-0000-000000000001', 'api-id-2', '', false, true);
reset role;
select pg_temp.check((select api_secret = 'top-secret' and api_id = 'api-id-2' and vat_exempt from public.garage_billing where garage_id = 'e1000000-0000-0000-0000-000000000001'), 'empty secret keeps the stored one');
set role authenticated;

-- another garage sees and touches nothing
select pg_temp.as_user('00000000-0000-0000-0000-0000000000e2');
select pg_temp.check((select count(*) from public.parts) = 0 and (select count(*) from public.suppliers) = 0 and (select count(*) from public.purchase_orders) = 0
  and (select count(*) from public.stock_moves) = 0 and (select count(*) from public.invoices) = 0 and (select count(*) from public.garage_billing) = 0, 'other garage sees no stock, orders, invoices or settings');
select pg_temp.expect_fail($q$insert into public.stock_moves (garage_id, part_id, qty, reason) values ('e2000000-0000-0000-0000-000000000002', 'e1a00000-0000-0000-0000-000000000001', 100, 'adjust')$q$, 'moving another garage''s part');
select pg_temp.expect_fail($q$select public.po_receive('e1b00000-0000-0000-0000-000000000002', '[]')$q$, 'receiving another garage''s order');
select pg_temp.expect_fail($q$select public.billing_save('e1000000-0000-0000-0000-000000000001', 'evil', 'evil', false, false)$q$, 'changing another garage''s invoicing settings');
insert into public.parts (id, garage_id, name) values ('e2a00000-0000-0000-0000-000000000001', 'e2000000-0000-0000-0000-000000000002', 'שלי');
select pg_temp.expect_fail($q$insert into public.parts (garage_id, name, supplier_id) values ('e2000000-0000-0000-0000-000000000002', 'x', 'e1500000-0000-0000-0000-000000000001')$q$, 'linking another garage''s supplier');
select pg_temp.expect_fail($q$select public.wo_consume('e1d00000-0000-0000-0000-000000000002')$q$, 'consuming stock on another garage''s work order');
reset role; set role anon; select pg_temp.as_user('');
select pg_temp.check((select count(*) from public.parts) = 0 and (select count(*) from public.invoices) = 0, 'anonymous sees no stock or invoices');
select pg_temp.expect_fail($q$select public.billing_save('e1000000-0000-0000-0000-000000000001', 'a', 'b', false, false)$q$, 'anonymous changes invoicing settings');
select pg_temp.expect_fail($q$select public.po_receive('e1b00000-0000-0000-0000-000000000002', '[]')$q$, 'anonymous receives an order');
reset role;
