import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost"))
channel = connection.channel()
channel.queue_declare(queue="get_array")


def callback(ch, method, properties, body):
    print("[es_array] Received %r" % body)
    #ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue='get_array', on_message_callback=callback, auto_ack=True)
print("receiving_array")
channel.start_consuming()
