-- Why AI calls failed, for debugging without depending on the function logs. Written by ai-assist with the
-- service role; nobody else can read or write it (RLS on, no policies). Holds no documents and no keys.
-- Run after 0013. Safe to run more than once.
create table if not exists public.ai_errors (
  id bigint generated always as identity primary key,
  at timestamptz not null default now(),
  user_id uuid references auth.users(id) on delete cascade,
  task text,
  status int,
  message text
);
alter table public.ai_errors enable row level security;
create index if not exists ai_errors_at_idx on public.ai_errors(at desc);
