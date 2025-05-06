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
    # 1. Revisar si llega algún insulto nuevo
    message = pubsub.get_message(ignore_subscribe_messages=True)  # <<< IGNORA el mensaje de suscripción
    if message:
        insult = message['data']
        added = client.sadd(INSULT_SET, insult)
        if added:
            client.rpush(INSULT_LIST, insult)
            print(f"[ADD] New insult added: {insult}")
        else:
            print(f"[SKIP] Duplicate insult ignored: {insult}")

    # 2. Hacer broadcast cada 5 segundos
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

    time.sleep(0.1)  # Pequeño delay para no saturar la CPU
