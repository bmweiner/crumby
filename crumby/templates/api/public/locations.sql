select
	v.state,
	v.country,
  count(*) as users
from (
  select distinct
    cid,
    country,
		subdivision_1 as state
  from visits
	where date(datetime) between date("{{t0}}") and date("{{t1}}")
) as v
group by v.country, v.state
order by users desc
