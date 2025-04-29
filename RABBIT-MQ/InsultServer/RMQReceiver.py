#Receiver RabbitMQ 
# Código del tutorial de RabbitMQ
# https://www.rabbitmq.com/tutorials/tutorial-three-python adaptado

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='insult_exchange', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='insult_exchange', queue=queue_name)

print('Iniciando el receptor de insultos...')
print(' [*] Waiting for insults. To exit press CTRL+C')

def callback(ch, method, properties, body):
    body = body.decode('utf-8') # Decodificar el mensaje para que salga el formato correcto
    print(f" [x] {body}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()