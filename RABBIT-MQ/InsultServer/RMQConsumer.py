import pika
import time

stored_insults = []

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='insult_queue', durable=True)
print(' [*] Esperando insultos del producer. Para salir presione CTRL+C')
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    insult = body.decode()

    if insult not in stored_insults:
        stored_insults.append(insult)
        print(f"[+] Insulto nuevo guardado: {insult}")
    else:
        print(f"[=] Insulto duplicado ignorado: {insult}")

    # Confirma que se ha procesado correctamente
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1) # Asegura que solo se procesa un mensaje a la vez
channel.basic_consume(queue='insult_queue', on_message_callback=callback) # Configura el callback para procesar los mensajes

channel.start_consuming()
