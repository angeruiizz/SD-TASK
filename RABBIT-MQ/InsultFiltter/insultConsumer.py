import pika
import time

# Lista para almacenar los textos filtrados
filtered_texts = []

# Lista de insultos
insults = ["tonto", "estúpido", "imbécil", "idiota", "lento", "cap de suro", "gilipollas"]

# Función para filtrar los insultos
def filter_insults(text):
    for insult in insults:
        text = text.replace(insult, "CENSORED")
    return text

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declarar la cola de entrada (productores envían aquí)
channel.queue_declare(queue='text_queue')

# Callback que filtra y almacena los resultados
def callback(ch, method, properties, body):
    original = body.decode()  # Decodificar el mensaje
    cleaned = filter_insults(original)  # Filtrar el insulto
    print(f"Filtrado: {cleaned}")
    
    # Almacenar el texto filtrado en la lista
    filtered_texts.append(cleaned)
    
    # Confirmar que el mensaje ha sido procesado
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Función para devolver la lista de resultados filtrados
def get_filtered_texts():
    return filtered_texts

print(" [*] Esperando textos para filtrar...")

# Consumiendo los mensajes de la cola
channel.basic_consume(queue='text_queue', on_message_callback=callback, auto_ack=False)
channel.start_consuming()
c