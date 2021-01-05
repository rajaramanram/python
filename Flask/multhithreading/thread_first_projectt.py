from flask import Flask,request,jsonify
from elasticsearch import Elasticsearch
from time import gmtime
import time
import json
#import datetime
from time import mktime
from datetime import datetime
import threading


es = Elasticsearch(["172.16.1.103:9200"])

app=Flask(__name__)
def thread_method():
  @app.route('/receive', methods=['GET','POST'])
  def receive_data():
      if request.method == 'GET':
        response_status = es.search(
            index="first_project", doc_type='_doc')
        get = response_status['hits']['hits']
        array_field = []
        for i in range(len(get)):
          iterate_field = get[i]['_source']
          array_field.append(iterate_field)
        print(array_field)
        return jsonify({'status': True, 'data': 'Data Sent'})
      else:
        data= request.get_json()
        if not data and data != '':
          return jsonify({'status': False, 'data': 'No Data Found'})
        mandatory_field_list=["CINAME","SEVERITY","SOURCE","SOURCE_TIME"]
        for i in mandatory_field_list:
            if i not in data:
              return jsonify({'status': False, 'data': 'No Data Found'})
        
        #check for same alert
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
                              "CINAME": data["CINAME"]
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
                              "SUMMARY": data["SUMMARY"]
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
                            "IP": data["IP"]
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
        response_status = es.search(index="first_project", doc_type='_doc', body=check_already)
        if len(response_status['hits']['hits']) != 0:
          id = response_status['hits']['hits'][0]['_id']
          print("id", id)
          update_count_body={
              "script" : {
                "source": "ctx._source.COUNT += params.count",
                "lang": "painless",
                "params" : {
                  "count" : 1
                }
              }
            }
          update_count = es.update(index="first_project",doc_type='_doc',id=id,body=update_count_body)
          print(update_count)
        else:
          gmt_time = time.gmtime()
          gmt_time_to_dt = datetime.fromtimestamp(mktime(gmt_time))
          conversion_gmt = datetime.strftime(gmt_time_to_dt, '%Y-%m-%dT%H:%M:%S.%fZ')
          #GETTNG document count from es for incrementing ALERT_ID
          refresh=es.indices.refresh(index='first_project')
          get_count_es=es.cat.count(index='first_project', params={"format": "json"})
          update_count = int(get_count_es[0]['count']) + 1
          alert_id_string = "AL0000000"
          len_count = len(str(update_count))
          put_alert_id = alert_id_string[:-len_count]+str(update_count)
          #print(put_alert_id)
          data["ALERT_ID"] = put_alert_id
          data["COUNT"] = 1
          data["STATUS"] = "open"
          if data["ENVIRONMENT"] == '':
            data["ENVIRONMENT"] = "default"
          data["CREATED_TIME"] = conversion_gmt
          #print(data)
          res = es.index(index='first_project', doc_type='_doc', body=data)
          #print(res)
        return jsonify({'status': True, 'data': 'Data Sent'})
def thread_call():
  threading.Thread(target=thread_method).start()
thread_call()
if __name__=="__main__":
    app.run(debug=True)
