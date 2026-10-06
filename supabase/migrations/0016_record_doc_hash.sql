-- The SHA-256 of the receipt file a record was read from, so the same file uploaded again is recognised
-- before it is read a second time. Run after 0015. Safe to run more than once.
alter table public.records add column if not exists doc_hash text;
