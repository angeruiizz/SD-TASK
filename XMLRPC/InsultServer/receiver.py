# receiver_xmlrpc.py

import xmlrpc.client
import time

server = xmlrpc.client.ServerProxy("http://localhost:9000/")

print("Receiver is polling for new insults...")

while True:
    new_insults = server.get_new_insults()
    for insult in new_insults:
        print(f"Received insult: {insult}")
    time.sleep(5)  # Espera 5 segundos antes de volver a preguntar
