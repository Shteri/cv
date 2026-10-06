-- The name on the sign is often not the licence holder's name in the Ministry of Transport registry.
-- garage_profiles.name is the name the owner shows (defaults to the registry name at claim); aka holds other names
-- customers use ("המוסך של שמעון"), so drivers' free-text reports and searches still find the garage.
-- Run after 0010. Safe to run more than once.
alter table public.garage_profiles add column if not exists aka text[] not null default '{}';
do $$ begin
  alter table public.garage_profiles add constraint garage_profiles_aka_check check (coalesce(array_length(aka, 1), 0) <= 6);
exception when duplicate_object then null; end $$;
