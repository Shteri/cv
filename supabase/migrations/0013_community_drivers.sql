-- community_garages counts drivers, not visits: one car that went to a garage 16 times is one driver.
-- The caller's own cars are left out; the app adds them from the device, so nobody is counted twice.
-- Run after 0012. Same signature, so it replaces the function in place.
create or replace function public.community_garages(p_schedule_id text)
returns table (garage text, city text, "where" text, n bigint, avg_price numeric, back_pct numeric, latest timestamptz)
language sql security definer set search_path = '' stable as $$
  with per_car as (
    -- each driver's say about a garage is their latest visit there
    select distinct on (r.car_id, p.garage, coalesce(p.city,''), p."where")
           r.car_id, p.garage, coalesce(p.city,'') as city, p."where", p.back, p.reported_at
    from public.price_reports p join public.records r on r.id = p.record_id
    where p.schedule_id = p_schedule_id and p.garage is not null and p."where" in ('importer','independent')
      and r.user_id is distinct from auth.uid()
    order by r.car_id, p.garage, coalesce(p.city,''), p."where", r.km desc, p.reported_at desc
  ), prices as (
    select p.garage, coalesce(p.city,'') as city, p."where", round(avg(p.price)) as avg_price
    from public.price_reports p join public.records r on r.id = p.record_id
    where p.schedule_id = p_schedule_id and p.garage is not null and p."where" in ('importer','independent')
      and r.user_id is distinct from auth.uid()
    group by 1, 2, 3
  )
  select c.garage, c.city, c."where", count(*) as n, max(x.avg_price) as avg_price,
         round(100.0 * count(*) filter (where c.back = 'yes') / nullif(count(*) filter (where c.back is not null), 0)) as back_pct,
         max(c.reported_at) as latest
  from per_car c join prices x on x.garage = c.garage and x.city = c.city and x."where" = c."where"
  group by c.garage, c.city, c."where"
  order by back_pct desc nulls last, n desc
  limit 50;
$$;
