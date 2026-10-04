-- AI assist (edge function ai-assist): a per-user daily counter, so each user has a fair daily limit.
-- Run after 0008. Safe to run more than once. Written without DROP/DELETE/REVOKE statements.
create table if not exists public.ai_usage (
  user_id uuid not null references auth.users(id) on delete cascade,
  day date not null,
  n int not null default 0,
  primary key (user_id, day)
);
alter table public.ai_usage enable row level security;   -- no policies: only the service role (the edge function) reads or writes

-- Counts one request and returns today's total. SECURITY INVOKER: with RLS and no policies, only the service role can use it.
create or replace function public.ai_bump(p_user uuid) returns int
language sql set search_path = '' as $$
  insert into public.ai_usage (user_id, day, n) values (p_user, (now() at time zone 'Asia/Jerusalem')::date, 1)
  on conflict (user_id, day) do update set n = public.ai_usage.n + 1
  returning n;
$$;
