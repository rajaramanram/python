'''import requests
from time import gmtime
import time
import json
#import datetime
from time import mktime
from datetime import datetime
gmt_time=time.gmtime()
print(gmt_time)
gmt_time_to_dt = datetime.fromtimestamp(mktime(gmt_time))
conversion_gmt=datetime.strftime(gmt_time_to_dt, '%Y-%m-%dT%H:%M:%S.%fZ')
print(conversion_gmt)'''
import requests
import time
start_time = time.time()
for i in range(5000):
	url = "http://127.0.0.1:5000/receive"

	payload = "{\n  \"CINAME\": \"devserver31\",\n  \"IP\": \"172.16.1.101\",\n  \"SEVERITY\": \"WARNING\",\n  \"ENVIRONMENT\":\"Docker\",\n  \"SUMMARY\": \"WARNING: MEM USAGE IS 80%\",\n  \"SOURCE\": \"NAGIOS\",\n  \"SOURCE_TIME\": \"2020-11-26T06:19:04.212298Z\",\n  \"TAGS\":\"MEMORY,LINUX\"\n}"
	headers = {
	'content-type': "application/json",
	'cache-control': "no-cache",
	'postman-token': "355445b3-0866-bb7c-a505-aae19e5b2015"
        }

	response = requests.request("POST", url, data=payload, headers=headers)
#print(response.status_code)
#print(response.elapsed.total_seconds())
print("Total_time","--- %s seconds ---" % (time.time() - start_time))
print(response.text)
'''response = {'hits': {'hits': [{'_source': {'CINAME': 'devserver10', 'ENVIRONMENT': 'DOCKER', 'IP': '172.16.1.103', 'SEVERITY': 'CRITICAL', 'SUMMARY': 'WARNING: MEM USAGE IS 80%', 'SOURCE': 'NAGIOS', 'SOURCE_TIME': '2020-11-29', 'TAGS': 'MEMORY,LINUX,SERVER', 'ALERT_ID': 'AL0000004', 'COUNT': 2, 'STATUS': 'open', 'CREATED_TIME': '2020-12-08T07:08:00.000000Z', 'MODIFIED_BY': 'Ravi', 'LAST_MODIFIED_TIME': '2020-12-08T07:08:00.000000Z'}}, {'_source': {'ALERT_ID': 'AL0000010', 'COUNT': 5, 'CINAME': 'devserver2', 'CREATED_TIME': '2020-11-27', 'ENVIRONMENT': 'DOCKER2', 'IP': '172.16.1.103', 'SEVERITY': 'CRITICAL', 'SUMMARY': 'WARNING: MEM USAGE IS 90%', 'SOURCE': 'NAGIOS', 'SOURCE_TIME': '2020-11-27', 'LAST_MODIFIED_TIME': '2020-11-27', 'STATUS': 'open', 'MODIFIED_BY': 'samen', 'TAGS': 'MEMORY,LINUX,SERVER'}}, {'_source': {'COUNT': 23, 'STATUS': 'open', 'MODIFIED_BY': 'Ravi', 'SEVERITY': 'WARNING', 'SOURCE_TIME': '2020-11-26T06:19:04.212298Z', 'CINAME': 'devserver', 'IP': '172.16.1.105', 'TAGS': 'MEMORY,LINUX', 'SUMMARY': 'WARNING: MEM USAGE IS 80%', 'ENVIRONMENT': 'DOCKER', 'SOURCE': 'NAGIOS', 'ALERT_ID': 'AL0000005', 'LAST_MODIFIED_TIME': '2020-12-08T14:39:52.000000Z', 'CREATED_TIME': '2020-12-08T14:39:52.000000Z'}}, {'_source': {'CINAME': 'devserver12', 'ENVIRONMENT': 'DOCKER', 'IP': '172.16.1.105', 'SEVERITY': 'CRITICAL', 'SUMMARY': 'WARNING: CPU USAGE IS 80%', 'SOURCE': 'NAGIOS', 'SOURCE_TIME': '2020-11-29', 'TAGS': 'MEMORY,LINUX', 'ALERT_ID': 'AL0000006', 'COUNT': 1, 'STATUS': 'open', 'CREATED_TIME': '2020-12-09T09:01:11.000000Z', 'MODIFIED_BY': 'Ravi', 'LAST_MODIFIED_TIME': '2020-12-09T09:01:11.000000Z'}}, {'_source': {'ALERT_ID': 'AL0000005', 'COUNT': 3, 'CINAME': 'devserver2', 'CREATED_TIME': '2020-11-26','ENVIRONMENT': 'DOCKER', 'IP': '172.16.1.105', 'SEVERITY': 'WARNING', 'SUMMARY': 'WARNING: MEM USAGE IS 90%', 'SOURCE': 'NAGIOS', 'SOURCE_TIME': '2020-11-26', 'LAST_MODIFIED_TIME': '2020-11-26', 'STATUS': 'acknowledged', 'MODIFIED_BY': 'same', 'TAGS': 'MEMORY,LINUX'}}, {'_source': {'ALERT_ID': 'AL0000003', 'COUNT': 3, 'CINAME': 'devserver', 'CREATED_TIME': '2020-11-26T06:19:04.212298Z', 'ENVIRONMENT': 'DOCKER', 'IP': '172.16.1.105', 'SEVERITY': 'WARNING', 'SUMMARY': 'WARNING: MEM USAGE IS 80%', 'SOURCE': 'NAGIOS', 'SOURCE_TIME': '2020-11-26T06:19:04.212298Z', 'LAST_MODIFIED_TIME': '2020-11-26', 'STATUS': 'acknowledged', 'MODIFIED_BY': 'sam', 'TAGS': 'MEMORY,LINUX'}}, {'_source': {'CINAME': 'devserver19', 'IP': '172.16.1.105', 'SEVERITY': 'WARNING', 'ENVIRONMENT': 'Linode', 'SUMMARY': 'WARNING: MEM USAGE IS 80%', 'SOURCE': 'NAGIOS', 'SOURCE_TIME': '2020-11-26T06:19:04.212298Z', 'TAGS': 'MEMORY,LINUX', 'ALERT_ID': 'AL0000008', 'COUNT': 501, 'STATUS': 'open', 'CREATED_TIME': '2020-12-09T20:36:17.000000Z'}}, {'_source': {'CINAME': 'devserver19', 'IP': '172.16.1.105', 'SEVERITY': 'WARNING', 'ENVIRONMENT': 'Linode', 'SUMMARY': 'WARNING: MEM USAGE IS 80%', 'SOURCE': 'NAGIOS', 'SOURCE_TIME': '2020-11-26T06:19:04.212298Z', 'TAGS': 'MEMORY,LINUX', 'ALERT_ID': 'AL0000009', 'COUNT': 499, 'STATUS': 'open', 'CREATED_TIME': '2020-12-09T20:36:17.000000Z'}}, {'_source': {'CINAME': 'devserver18', 'IP': '172.16.1.105', 'SEVERITY': 'WARNING', 'ENVIRONMENT': 'Linode', 'SUMMARY': 'WARNING: MEM USAGE IS 80%', 'SOURCE': 'NAGIOS', 'SOURCE_TIME': '2020-11-26T06:19:04.212298Z', 'TAGS': 'MEMORY,LINUX', 'ALERT_ID': 'AL0000007', 'COUNT': 10, 'STATUS': 'open', 'CREATED_TIME': '2020-12-09T20:33:57.000000Z'}}]}}
get= response['hits']['hits']
array_field = []
for i in range(len(get)):
	iterate_field = get[i]['_source']
	array_field.append(iterate_field)
print(array_field)'''