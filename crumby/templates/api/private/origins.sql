select
  substr(referrer, instr(referrer, '//') + 2) as origin,
  count(id) as views
from visits
where CAST(datetime AS DATE) between date("{{t0}}") and date("{{t1}}")
group by referrer
having
	origin not like 'localhost%%' and
	origin not like '127.0.0.1%%'
order by views desc
