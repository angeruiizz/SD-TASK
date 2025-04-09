# Genera insultos y los envia a la cola bloquenate cada 5 seg

import redis
import time
import random

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

queue_name = "INSULTS_queue"

# Send multiple messages
INSULTS = ["Tonto", "Cap de suro", "Inutil","BocaChancla"]

while True:
    insult = random.choice(INSULTS)  # Selecciona un insulto aleatorio
    client.rpush(queue_name, insult)
    print(f"Produced: {insult}")
    time.sleep(5)  # Espera 5 segundos entre cada envío