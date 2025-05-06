import redis
import time
import random

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

INSULTS = ["Tonto", "Cap de suro", "Inútil", "BocaChancla", "Cabezón", "Papanatas", "Bobalicón", "Cretino", "Lelo", "Bocazas", "QUEPASABALA"]
INPUT_CHANNEL = "INSULTS_input"

print("Producer started...")

while True:
    insult = random.choice(INSULTS)
    client.publish(INPUT_CHANNEL, insult)
    print(f"Produced insult: {insult}")
    time.sleep(5)  # Emite un insulto cada 5 segundos
