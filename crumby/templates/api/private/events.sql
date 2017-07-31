select
  doc_title as Title,
  name as Name,
  value as Value,
  count(value) as Count
from events
where id in (select max(id) from events group by cid, doc_title, name)
and date(datetime) between date("{{t0}}") and date("{{t1}}")
group by doc_title, name, value
