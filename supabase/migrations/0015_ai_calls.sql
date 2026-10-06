-- One row per AI call: tokens and time, to see what each feature costs. Written by ai-assist with the service
-- role; nobody else can read or write it (RLS on, no policies). No documents, no text. Run after 0014.
create table if not exists public.ai_calls (
  id bigint generated always as identity primary key,
  at timestamptz not null default now(),
  user_id uuid references auth.users(id) on delete cascade,
  task text,
  model text,
  input_tokens int,
  output_tokens int,
  ms int,
  ok boolean
);
alter table public.ai_calls enable row level security;
create index if not exists ai_calls_at_idx on public.ai_calls(at desc);
