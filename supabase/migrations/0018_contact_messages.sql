-- Contact page (/contact/): requests from drivers and garages, including privacy requests (access, correction,
-- deletion). Anyone may send through contact_send (checked, rate-limited); nobody reads the table but the
-- service role (RLS on, no policies). Run after 0017. Safe to run more than once.
create table if not exists public.contact_messages (
  id bigint generated always as identity primary key,
  at timestamptz not null default now(),
  user_id uuid references auth.users(id) on delete set null,
  name text, email text, phone text,
  topic text not null,
  message text not null,
  handled boolean not null default false
);
alter table public.contact_messages enable row level security;
create index if not exists contact_messages_at_idx on public.contact_messages(at desc);
create or replace function public.contact_send(p_name text, p_email text, p_phone text, p_topic text, p_message text)
returns void language plpgsql security definer set search_path = '' as $$
begin
  if coalesce(trim(p_message), '') = '' or length(p_message) > 4000 then raise exception 'bad message'; end if;
  if coalesce(trim(p_email), '') = '' and coalesce(trim(p_phone), '') = '' then raise exception 'contact needed'; end if;
  if p_topic not in ('privacy','support','garage','other') then raise exception 'bad topic'; end if;
  if (select count(*) from public.contact_messages where at > now() - interval '1 hour' and (email = lower(trim(p_email)) or phone = trim(p_phone))) >= 5 then raise exception 'too many'; end if;
  insert into public.contact_messages (user_id, name, email, phone, topic, message)
  values (auth.uid(), left(trim(p_name), 120), nullif(lower(left(trim(p_email), 200)), ''), nullif(left(trim(p_phone), 40), ''), p_topic, trim(p_message));
end $$;
revoke execute on function public.contact_send(text, text, text, text, text) from public;
grant execute on function public.contact_send(text, text, text, text, text) to anon, authenticated;
