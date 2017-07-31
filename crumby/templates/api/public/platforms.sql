select
	v.platform,
  count(*) as users
from (
  select distinct
    cid,
    platform
  from visits
	where date(datetime) between date("{{t0}}") and date("{{t1}}")
  ) as v
  group by v.platform
  order by users desc
