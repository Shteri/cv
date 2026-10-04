-- Garage platform: modules per garage, job catalog, vehicle inspection on approval links.
-- Run after 0007. Safe to run more than once. Written without DROP/DELETE statements.

-- ---------- which modules the garage uses (null = follow the professions it is licensed for) ----------
alter table public.garage_profiles add column if not exists modules text[];
