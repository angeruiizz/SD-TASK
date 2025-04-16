# observable.py 
import redis
import time

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
queue_name = "INSULTS_queue"
existing_list_name = "INSULTS"
channel_name = "INSULTS_channel"

client.delete(existing_list_name)  # Limpiar lista al iniciar

print("InsultService (observable) is running...")

while True:
    task = client.blpop(queue_name, timeout=0)
    if task:
        insult = task[1]
        existing_insults = client.lrange(existing_list_name, 0, -1)
        
        if insult not in existing_insults:
            client.rpush(existing_list_name, insult)  # Añadir insulto
            print(f"New insult saved: {insult}")
            client.publish(channel_name, insult)  # Notificar a los observers
        else:
            print(f"Insult already exists: {insult}")
