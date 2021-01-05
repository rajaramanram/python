''''alert_id =0000000
add_count =1
total = alert_id + add_count
print(total)
from elasticsearch import Elasticsearch
es = Elasticsearch(["localhost:9200"])
refresh=es.indices.refresh(index='first_project')
get_count_es=es.cat.count(index='first_project', params={"format": "json"})
print(get_count_es[0]['count'])
update_count = get_count_es[0]['count'] + 1
alert_id_string = "AL0000000"
print(alert_id_string[:-2])'''
alert_id_string = "AL0000000"
get_count =100
'''if get_count < 10:
   put_alert_id = alert_id_string[:-1] + str(get_count)
   print(put_alert_id)
elif get_count > 9 and get_count < 100:
   put_alert_id = alert_id_string[:-1] + str(get_count)
   print(put_alert_id)'''

len_count = len(str(get_count))
put_alert_id = alert_id_string[:-len_count]+str(get_count)
print(put_alert_id)
