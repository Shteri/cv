-- Tires per wheel: which wheels a record replaced (fl, fr, rl, rr). Null means all four, as before.
-- Run after 0011. Safe to run more than once.
alter table public.records add column if not exists tires text[];
do $$ begin
  alter table public.records add constraint records_tires_check check (tires is null or (cardinality(tires) between 1 and 4 and tires <@ array['fl','fr','rl','rr']));
exception when duplicate_object then null; end $$;
