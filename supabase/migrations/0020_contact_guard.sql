-- Contact form: an "accessibility" topic (the accessibility statement points here), and a global hourly cap
-- on top of the per-sender one, so a bot rotating emails cannot flood the table. Run after 0019. Safe to rerun.
create or replace function public.contact_send(p_name text, p_email text, p_phone text, p_topic text, p_message text)
returns void language plpgsql security definer set search_path = '' as $$
begin
  if coalesce(trim(p_message), '') = '' or length(p_message) > 4000 then raise exception 'bad message'; end if;
  if coalesce(trim(p_email), '') = '' and coalesce(trim(p_phone), '') = '' then raise exception 'contact needed'; end if;
  if p_topic not in ('privacy','support','garage','accessibility','other') then raise exception 'bad topic'; end if;
  if (select count(*) from public.contact_messages where at > now() - interval '1 hour' and (email = lower(trim(p_email)) or phone = trim(p_phone))) >= 5 then raise exception 'too many'; end if;
  if (select count(*) from public.contact_messages where at > now() - interval '1 hour') >= 100 then raise exception 'too many'; end if;
  insert into public.contact_messages (user_id, name, email, phone, topic, message)
  values (auth.uid(), left(trim(p_name), 120), nullif(lower(left(trim(p_email), 200)), ''), nullif(left(trim(p_phone), 40), ''), p_topic, trim(p_message));
end $$;
revoke execute on function public.contact_send(text, text, text, text, text) from public;
grant execute on function public.contact_send(text, text, text, text, text) to anon, authenticated;
