# producer.py
import redis
import time
import random

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
queue_name = "INSULTS_queue"

INSULTS = ["Tonto", "Cap de suro", "Inútil", "BocaChancla"]

print("Producer started...")

while True:
    insult = random.choice(INSULTS)
    client.rpush(queue_name, insult)
    print(f"Produced insult: {insult}")
    time.sleep(5)
