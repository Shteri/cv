-- The private receipts bucket (0001 created it, but production was missing it, so receipt uploads failed quietly).
-- Images and PDFs up to 10 MB, each user in their own folder. Run after 0016. Safe to run more than once.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('receipts', 'receipts', false, 10485760, array['image/jpeg','image/png','image/webp','application/pdf'])
on conflict (id) do update set public = false, file_size_limit = excluded.file_size_limit, allowed_mime_types = excluded.allowed_mime_types;
do $$ begin
  create policy "receipts: own folder read" on storage.objects for select to authenticated
    using (bucket_id = 'receipts' and (storage.foldername(name))[1] = (select auth.uid())::text);
exception when duplicate_object then null; end $$;
do $$ begin
  create policy "receipts: own folder write" on storage.objects for insert to authenticated
    with check (bucket_id = 'receipts' and (storage.foldername(name))[1] = (select auth.uid())::text);
exception when duplicate_object then null; end $$;
do $$ begin
  create policy "receipts: own folder update" on storage.objects for update to authenticated
    using (bucket_id = 'receipts' and (storage.foldername(name))[1] = (select auth.uid())::text);
exception when duplicate_object then null; end $$;
do $$ begin
  create policy "receipts: own folder delete" on storage.objects for delete to authenticated
    using (bucket_id = 'receipts' and (storage.foldername(name))[1] = (select auth.uid())::text);
exception when duplicate_object then null; end $$;
