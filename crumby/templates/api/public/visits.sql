select
  date(c.datetime) as date,
  coalesce(v.users, 0) as users,
  coalesce(v.views, 0) as views
from calendar c
left join(
  select
	  date(datetime) as date,
    count(distinct cid) as users,
	  count(id) as views
	from visits
	group by date) v
on date(c.datetime) = v.date
where date(c.datetime) between date("{{t0}}") and date("{{t1}}")
