from flask import Flask,request,jsonify
from elasticsearch import Elasticsearch
from time import gmtime
import time
import json
#import datetime
from time import mktime
from datetime import datetime
import pika

es = Elasticsearch(["172.16.1.103:9200"])
app=Flask(__name__)
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
      connection = pika.BlockingConnection(pika.ConnectionParameters(host = "localhost"))
      channel = connection.channel()
      channel.queue_declare(queue='post_request')
      response_status = {"input_alert":data,"index":"first_project"}
      channel.basic_publish(exchange = '',routing_key = 'post_request',body = str(response_status))
      #print("published_post")
      #connection.close()
      return jsonify({'status': True, 'data': 'Data Sent'})
if __name__=="__main__":
    app.run(debug=True,threaded=True)
