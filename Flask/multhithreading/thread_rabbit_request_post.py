from flask import Flask,request,jsonify
from elasticsearch import Elasticsearch
import json
import pika
import threading

es = Elasticsearch(["172.16.1.103:9200"])
app = Flask(__name__)
def thread_method():
  @app.route('/receive', methods=['GET','POST'])
  def receive_data():
      if request.method == 'GET':
        response_status = es.search(
            index="first_project")
        get = response_status['hits']['hits']
        array_field = []
        for i in range(len(get)):
          iterate_field = get[i]['_source']
          array_field.append(iterate_field)
        #print(array_field)
        return jsonify({'status': True, 'data':array_field})
      else:
        data= request.get_json()
        #print(data)
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

        connection = pika.BlockingConnection(pika.ConnectionParameters(host = "localhost"))
        channel = connection.channel()
        channel.queue_declare(queue='post_request')
        response_status = {"input_alert":data,"search":"search","index":"first_project","body":check_already}
        channel.basic_publish(exchange = '',routing_key = 'post_request',body = str(response_status))
        #print(threading.current_thread().name)
        #print("published_post")
        #connection.close()
        return jsonify({'status': True, 'data': 'Data Sent'})


def thread_call():
  threading.Thread(target=thread_method).start()
thread_call()
if __name__=="__main__":
    app.run(debug=True,threaded = True)