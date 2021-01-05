#ch.basic_ack(delivery_tag=method.delivery_tag)
import pika
from elasticsearch import Elasticsearch
import json
es = Elasticsearch(["172.16.1.103:9200"])

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.queue_declare(queue="elasticsearch")


def callback(ch, method, properties, body):
    print("[x] Received %r" % body)
    res_dict = body.decode('utf-8')
    replace_string = res_dict.replace("'", '"')
    print(replace_string)
    json_output= json.loads(replace_string)
    print(json_output)
    get_os_output(json_output)
def get_os_output(body_get):
    print(body_get['index'])
    #response_change = es.body_get['search'](index=body_get['index'], doc_type=body_get['doc_type'])
    response_status = es.search(
        index=body_get['index'], doc_type=body_get['doc_type'])
    print(response_status)
    get = response_status['hits']['hits']
    array_field = []
    for i in range(len(get)):
        iterate_field = get[i]['_source']
        array_field.append(iterate_field)
    print(array_field)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost"))


    channel = connection.channel()
    channel.queue_declare(queue='get_array')
    channel.basic_publish(exchange='', routing_key='get_array',body=str(array_field))
    print("published_array")
    connection.close()


channel.basic_consume(
    queue='elasticsearch', on_message_callback=callback, auto_ack=True)
print("receiving")
channel.start_consuming()
