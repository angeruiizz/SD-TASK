# RabbitMQ Broadcast
# Codigo del tutorial de RabbitMQ 
# https://www.rabbitmq.com/tutorials/tutorial-three-python adaptado

import pika
import time
import random

# Lista de insultos o cualquier otro mensaje que desees transmitir
insults = ["Tonto", "Ceporro", "Zoquete", "Inútil", "Bocachancla", "Torpe","Cabezón",
           "Bobalicón", "Lelo", "Bobalón", "Cretino", "Patán", "Zopenco", "Mediocre",
           "Lerdos", "Burrito", "Papanatas", "Cabezón", "Tontorrón", "Capdesuro"]

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declaramos el exchange tipo fanout para el broadcast
channel.exchange_declare(exchange='insult_exchange', exchange_type='fanout')

# Enviar los insultos cada 5 segundos
print("Iniciando broadcast de insultos...")
while True:
    insult = random.choice(insults)  # Elegir un insulto aleatorio de la lista
    channel.basic_publish(exchange='insult_exchange', routing_key='', body=insult.encode())
    print(f"[BROADCAST] {insult}")
    
    time.sleep(5)  # Esperar 5 segundos antes de volver a emitir los mensajes
