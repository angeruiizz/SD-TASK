import redis
import time

# Conectar a Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

work_queue = "work_queue"

# Mensajes sin insultos
texts = [
    "Ejemplo text sin insultos.",
    "Todo va bien hoy.",
    "Se acerca verano",
    "Apruebo SD :)"
]

while True:
    for text in texts:
        client.rpush(work_queue, text)  # Envia el mensaje a la cola
        print(f"TextProducer: Produced text - {text}")
        time.sleep(5)  # Espera 5 segundos antes de enviar el siguiente mensaje
