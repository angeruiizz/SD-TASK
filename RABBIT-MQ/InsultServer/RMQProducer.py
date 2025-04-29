# RabbitMQ Producer
# Se encarga de enviar insultos a la cola de RabbitMQ. Codigo del tutorial de RabbitMQ
# https://www.rabbitmq.com/tutorials/tutorial-two-python.html adaptado
import pika
import random
import time

insults = ["Tonto", "Ceporro", "Zoquete", "Inútil", "Bocachancla", "Torpe","Cabezón",
           "Bobalicón", "Lelo", "Bobalón", "Cretino", "Patán", "Zopenco", "Mediocre",
           "Lerdos", "Burrito", "Papanatas", "Cabezón", "Tontorrón", "Capdesuro"]

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='insult_queue', durable=True)

print(' [*] Enviando insultos del producer. Para salir presione CTRL+C')
while True:
    insult = random.choice(insults)
    channel.basic_publish(
        exchange='',
        routing_key='insult_queue',
        body=insult.encode(),
        properties=pika.BasicProperties(delivery_mode= pika.DeliveryMode.Persistent) 
    )
    print(f"[x] Enviado: {insult}")
    time.sleep(5)  # Espera 5 segundo entre mensajes

connection.close()
