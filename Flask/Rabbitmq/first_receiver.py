import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host= "localhost"))
channel =  connection.channel()
channel.queue_declare(queue="hello")
def callback(ch,method,properties,body):
    print("[x] Received %r"%body)
    #ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue = 'hello',on_message_callback=callback,auto_ack=True)
print("receiving")
channel.start_consuming()
