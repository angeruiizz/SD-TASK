import redis
import time
import random

# Conexión al servidor Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Nombres de claves y canales
INSULT_SET = "INSULTS_set"             # Conjunto para evitar duplicados
INSULT_LIST = "INSULTS_list"           # Lista para mantener el orden
INPUT_CHANNEL = "INSULTS_input"        # Canal de entrada (productores)
OUTPUT_CHANNEL = "INSULTS_broadcast"   # Canal de salida (difusión)

# Limpiar estado anterior (solo si se reinicia todo)
client.delete(INSULT_SET)
client.delete(INSULT_LIST)

# Suscripción al canal de entrada
pubsub = client.pubsub()
pubsub.subscribe(INPUT_CHANNEL)

print("InsultService is running...")

last_broadcast = time.time()

while True:
    _, insult = client.blpop("insults_queue")  # Espera bloqueante
    added = client.sadd(INSULT_SET, insult)
    client.rpush("insults_processed", insult)
    if added:
        client.rpush(INSULT_LIST, insult)
        client.rpush("insults_processed", insult)
        print(f"[ADD] New insult added: {insult}")
    else:
        print(f"[SKIP] Duplicate insult ignored: {insult}")

    #PARTE BROADCAST
    current_time = time.time()
    if current_time - last_broadcast >= 5:
        insults = client.lrange(INSULT_LIST, 0, -1)
        if insults:
            insult = random.choice(insults)
            client.publish(OUTPUT_CHANNEL, insult)
            print(f"[BROADCAST] Sent insult: {insult}")
        else:
            print("[BROADCAST] No insults to send yet.")
        last_broadcast = current_time
