select
  city,
  subdivision_1 as state,
  country,
	count(distinct ip) as users,
  count(distinct cid) as clients,
  count(distinct concat(cid, date(datetime))) as sessions,
  count(id) as views
from visits
where ip != '127.0.0.1' and
      CAST(datetime AS DATE) between date("{{t0}}") and date("{{t1}}")
group by city, subdivision_1, country
order by country, subdivision_1, city asc
