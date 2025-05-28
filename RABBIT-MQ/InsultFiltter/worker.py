# worker.py
from time import sleep
import pika

insults = ["tonto", "estúpido", "imbécil", "idiota", "lento", "cap de suro", "gilipollas"]

def filter_insults(text):
    for insult in insults:
        text = text.replace(insult, "CENSORED")
    return text

print("INICIO WORKER")

# Conexión a RabbitMQ para consumir
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='text_queue')

# Conexión a RabbitMQ para publicar resultados
connection_result = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel_result = connection_result.channel()
channel_result.queue_declare(queue='result_queue')

def callback(ch, method, properties, body):
    original = body.decode()
    cleaned = filter_insults(original)
    #print(f"Filtrado: {cleaned}")
    # Enviar a la cola de resultados
    channel_result.basic_publish(exchange='', routing_key='result_queue', body=cleaned)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    sleep(1)

print(" [*] Esperando textos para filtrar...")
channel.basic_consume(queue='text_queue', on_message_callback=callback, auto_ack=False)
channel.start_consuming()
