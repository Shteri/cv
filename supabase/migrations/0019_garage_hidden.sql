-- A garage profile can be hidden: only its owner sees it in lists (for a test garage); its booking link still works.
-- Run after 0018. Safe to run more than once.
alter table public.garage_profiles add column if not exists hidden boolean not null default false;
alter policy "garage_profiles: public read verified" on public.garage_profiles using (status = 'verified' and not hidden);
