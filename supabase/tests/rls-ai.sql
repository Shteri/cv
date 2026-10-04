-- Run with: sh scripts/test-db.sh
-- AI usage counter (migration 0009): only the service role (the edge function) can count.
\set ON_ERROR_STOP 1
insert into auth.users (id, email) values ('00000000-0000-0000-0000-0000000000c3','ai@x');
create function pg_temp.as_user(u text) returns void language plpgsql as $$ begin perform set_config('request.jwt.claim.sub', u, false); end $$;
create function pg_temp.expect_fail(q text, label text) returns void language plpgsql as $$
begin begin execute q; exception when others then raise notice 'OK  % (blocked: %)', label, sqlerrm; return; end; raise exception 'FAIL % was allowed', label; end $$;
create function pg_temp.check(cond boolean, label text) returns void language plpgsql as $$ begin if cond then raise notice 'OK  %', label; else raise exception 'FAIL %', label; end if; end $$;
set role service_role;
select pg_temp.check(public.ai_bump('00000000-0000-0000-0000-0000000000c3') = 1 and public.ai_bump('00000000-0000-0000-0000-0000000000c3') = 2, 'service role counts requests per day');
reset role; set role authenticated; select pg_temp.as_user('00000000-0000-0000-0000-0000000000c3');
select pg_temp.expect_fail($q$select public.ai_bump('00000000-0000-0000-0000-0000000000c3')$q$, 'signed-in user bumping the counter');
select pg_temp.check((select count(*) from public.ai_usage) = 0, 'signed-in user cannot read usage');
reset role; set role anon; select pg_temp.as_user('');
select pg_temp.expect_fail($q$select public.ai_bump('00000000-0000-0000-0000-0000000000c3')$q$, 'anonymous bumping the counter');
reset role;
