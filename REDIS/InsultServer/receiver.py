# se suscribe al canal y recibe los insultos

import redis

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
channel_name = "INSULTS_channel"

# Función que se suscribe al canal y recibe los insultos
def receive_insults():
    pubsub = client.pubsub()  # Crea un objeto pubsub
    pubsub.subscribe(channel_name)  # Se suscribe al canal INSULTS_channel

    print(f"Subscribed to channel: {channel_name}")
    
    # Bucle para recibir mensajes
    for message in pubsub.listen():
        if message['type'] == 'message':  # Si se recibe un mensaje
            insult = message['data']
            print(f"Received insult: {insult}")

# Ejecuta el receptor
receive_insults()
