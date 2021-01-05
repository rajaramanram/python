=reter
from flask import Flask
from elasticsearch import Elasticsearch
import json, requests
from time import gmtime
import time
#import datetime
from time import mktime
from datetime import datetime


json_input={
  "ALERT_ID": "AL0000004",
  "COUNT": 6,
  "CINAME": "devserver",
  "ENVIRONMENT":"DOCKER",
  "IP": "172.16.1.103",
  "SUMMARY": "WARNING: MEM USAGE IS 80%",
  "SOURCE": "NAGIOS",
  "SEVERITY": "CRITICAL",
  "SOURCE_TIME": "2020-11-29T06:19:04.212298Z",
  "STATUS": "acknowledged"
}
#"SEVERITY": "CRITICAL",
#"CREATED_TIME": "2020-11-29T06:19:04.212298Z",
#"MODIFIED_BY": "sam",
es = Elasticsearch(["localhost:9200"])

#check json have CINAME,SEVERITY,SOUTCE,SOURCE_TIME
'''mandatory_field_list=["CINAME","SEVERITY","SOURCE","SOURCE_TIME"]
for i in mandatory_field_list:
    if i not in json_input and json_input != '':
        print(i)
#checking for ciname
    if not data["CINAME"] and data != '':
        return jsonify({'status': False, 'data': 'No Data Found'})

#checking for same alert
count_field=["CINAME","SUMMARY","IP"]
search_ciname = {
    "query": {
        "term": {
          "CINAME": {
            "value": json_input["CINAME"]
            }
        }
    }
}

# get a response from the cluster
response_ciname= es.search(index="first_project",doc_type='_doc', body=search_ciname)
print ('response_ciname:', response_ciname)
#if json_input["CINAME"]
print(response_ciname['took'])
#BOOL QUERY
search_summary={
  "query": {
    "bool": {
      "must": [
        {
          "match_phrase": {
            "SUMMARY": json_input["SUMMARY"]
          }
        }
      ]
    }
  }
}
response_summary= es.search(index="first_project",doc_type='_doc', body=search_summary)
print ('response_summary:', response_summary)
#if json_input["CINAME"]
print(response_summary["hits"]['max_score'])

search_ip = {
    "query": {
        "term": {
          "IP": {
            "value": json_input["IP"]
            }
        }
    }
}

# get a response from the cluster
response_ip= es.search(index="first_project",doc_type='_doc', body=search_ip)
print ('response_ip:', response_ip)
#if json_input["CINAME"]
print(response_ip['took'])
search_status = {
    "query": {
        "term": {
          "STATUS": {
            "value": json_input["STATUS"]
            }
        }
    }
}

# get a response from the cluster
response_status= es.search(index="first_project",doc_type='_doc', body=search_status)
print ('response_status:', response_status)
#if json_input["CINAME"]
print(response_status['took'])

check_status={
  "size" : 1000,
  "query" : {
    "match" : {
      "STATUS" : {
        "query" : "acknowledged",
        "operator" : "OR",
        "prefix_length" : 0,
        "max_expansions" : 50,
        "fuzzy_transpositions" : true,
        "lenient" : false,
        "zero_terms_query" : "NONE",
        "auto_generate_synonyms_phrase_query" : true,
        "boost" : 1.0
      }
    }
  }
}

count=0
if response_ciname["took"] >= 1 and response_summary["hits"]["max_score"] != None and response_ip["took"]>=1 and response_status["took"]>=1:
    count +=1
print(count)'''

'''else:
   
    gmt_time=time.gmtime()
    #print(gmt_time)
    gmt_time_to_dt = datetime.datetime.fromtimestamp(mktime(gmt_time))
    conversion_gmt=datetime.datetime.strftime(gmt_time_to_dt, '%Y-%m-%dT%H:%M:%S.%fZ')
    print(conversion_gmt)
    json_input["CREATED_TIME"]  = conversion_gmt
    json_input["MODIFIED_BY"]="Ravi"
    json_input[ "LAST_MODIFIED_TIME"]=conversion_gmt
    res=es.index(index='first_project', doc_type='_doc', body=json_input)
    print(res)'''

'''app=Flask(__name__)
@app.route('/receive', methods=['GET','POST'])
def receive_data():
    data= request.get_json()
    if not data and data != '':
        return jsonify({'status': False, 'data': 'No Data Found'})

    #checking for ciname
    if not data["CINAME"] and data != '':
        return jsonify({'status': False, 'data': 'No Data Found'})
    # checking for mandatory fields
    elif not data["CINAME"] or data =='':
        return jsonify({'status': False, 'data': 'No Data Found'})
    elif not data["SEVERITY"] or data =='':
        return jsonify({'status': False, 'data': 'No Data Found'})
    elif not data["SOURCE"] or data =='':
        return jsonify({'status': False, 'data': 'No Data Found'})
    elif not data["SOURCE_TIME"] or data =='':
        return jsonify({'status': False, 'data': 'No Data Found'})
    else:
        return jsonify({'status': True, 'data': 'Data Received'})
@app.route('/count',methods=['POST'])
def count_query():
    data= request.get_json()
    if not data and data != '':
        return jsonify({'status': False, 'data': 'No Data Found'})
    
 
if __name__=="__main__":
    app.run(debug=True)'''
check_already={
"query": {
    "bool": {
      "must": [],
      "filter": [
        {
          "bool": { 
            "should": [
              {
                "match_phrase": {
                  "CINAME": "devserver2"
                 }
              }
            ],
          "minimum_should_match":1
            }
          },
          {
          "bool": { 
            "should": [
              {
                "match_phrase": {
                  "SUMMARY": "WARNING: MEM USAGE IS 90%"
                }
              }
            ],
          "minimum_should_match":1
            }
          },
          {
          "bool": { 
            "should": [
              {
                "match_phrase": {
                "IP": "172.16.1.103"
                }
              }
            ],
          "minimum_should_match":1
            }
          },
          {
          "bool": { 
            "should": [
              {
                "match_phrase": {
                "STATUS":"open"
                 }
              }
            ],
          "minimum_should_match":1
            }
          }
        ]
    }
  }
}

# get a response from the cluster
response_status= es.search(index="first_project",doc_type='_doc', body=check_already)
print ('response_status:', response_status)
#if json_input["CINAME"]
print(response_status['hits']['hits'][0]['_id'])
id=response_status['hits']['hits'][0]['_id']
print("id",id)
'''update_count_body={
  "script" : {
    "source": "ctx._source.COUNT += params.count",
    "lang": "painless",
    "params" : {
      "count" : 1
    }
  }
}
update_count = es.update(index="first_project",doc_type='_doc',id="QY89LHYBxNTY2L1QRQlJ",body=update_count_body)
print(update_count)'''



