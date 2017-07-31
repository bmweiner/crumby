select
	substr(doc_uri, instr(doc_uri, '//') + 2) as uri,
	doc_title,
	count(*) as views
from visits
where date(datetime) between date("{{t0}}") and date("{{t1}}")
group by uri, doc_title
having
	uri not like 'localhost%%' and
	uri not like '127.0.0.1%%'
order by views desc
