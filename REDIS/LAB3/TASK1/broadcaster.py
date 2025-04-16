# publica insultos de INSULTS en un canal pub/sub

import redis
import time

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
channel_name = "INSULTS_channel"

# Función para enviar los insultos al canal
def broadcast_insults():
    # Obtiene todos los insultos de la lista INSULTS
    insults = client.lrange("INSULTS", 0, -1)

    for insult in insults:
        # Publica cada insulto en el canal
        client.publish(channel_name, insult)
        print(f"Broadcasted insult: {insult}")
        time.sleep(1)  # Opcional: agrega una pequeña espera entre insultos

# Ejecuta la función de transmisión
broadcast_insults()
