import pika


connection = pika.BlockingConnection(pika.ConnectionParameters(host = "localhost"))
channel = connection.channel()
channel.queue_declare(queue='elasticsearch')


response_status = {"search":"search","index":"first_project","doc_type":"_doc"}
channel.basic_publish(exchange = '',routing_key = 'elasticsearch',body = str(response_status))
print("published")
connection.close()


