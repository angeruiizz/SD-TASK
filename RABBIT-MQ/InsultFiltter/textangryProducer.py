import pika
import time
import random

texts = [
    "Eres un tonto, ¿por qué vas tan lento?",
    "Eres tan estúpido que no sé qué haces aquí.",
    "Ejemplo de texto sin insultos.",
    "¡Apruebo SD :)!",
]

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='text_queue')

while True:
    text = random.choice(texts)
    print(f"Enviando texto: {text}")
    channel.basic_publish(exchange='', routing_key='text_queue', body=text)
    time.sleep(3)
