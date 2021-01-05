#ch.basic_ack(delivery_tag=method.delivery_tag)
import pika
from elasticsearch import Elasticsearch
import json
from flask import Flask, request, jsonify
from time import gmtime
import time
import json
#import datetime
from time import mktime
from datetime import datetime
es = Elasticsearch(["172.16.1.103:9200"])

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.queue_declare(queue="post_request")


def callback(ch, method, properties, body):
    #print("[x] Received %r" % body)
    res_dict = body.decode('utf-8')
    replace_string = res_dict.replace("'", '"')
    #print(replace_string)
    json_output= json.loads(replace_string)
    #print(json_output)
    get_os_output(json_output)
def get_os_output(body_get):
    #print(body_get['input_alert'])
    data = body_get['input_alert']
    #response_change = es.body_get['search'](index=body_get['index'], doc_type=body_get['doc_type'])
    response_status = es.search(
        index=body_get['index'],body=body_get['body'])
    #print(response_status)
    if len(response_status['hits']['hits']) != 0:
        id = response_status['hits']['hits'][0]['_id']
        #print("id", id)
        update_count_body = {
            "script": {
                "source": "ctx._source.COUNT += params.count",
                "lang": "painless",
                "params": {
                "count": 1
                }
            }
        }
        update_count = es.update(
            index="first_project", id=id, body=update_count_body)
        #print(update_count)
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
        res = es.index(index='first_project', body=data)
        #print(res)
channel.basic_consume(
    queue="post_request", on_message_callback=callback, auto_ack=True)
print("receiving_post")
channel.start_consuming()
