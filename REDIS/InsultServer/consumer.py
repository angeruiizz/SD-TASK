# lee los insultos de la cola y los guarda en la lista INSULTS si no existen

import redis
import time

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
queue_name = "INSULTS_queue"
existing_list_name = "INSULTS"
client.delete("INSULTS")

print("Consumer is waiting for tasks...")

while True:
    task = client.blpop(queue_name, timeout=0)  # Blocks indefinitely until a task is available
    if task:
        insult = task[1]  # Extrae el insulto de la cola
        existing_insults = client.lrange(existing_list_name, 0, -1)  # Obtiene los insultos existentes en la lista
        
        if insult not in existing_insults:
            client.rpush(existing_list_name, insult)  # Guarda el insulto si es nuevo
            print(f"Saved new insult: {insult}")
        else:
            print(f"Insult already exists: {insult}")