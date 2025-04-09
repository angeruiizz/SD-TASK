# producer_xmlrpc.py
import xmlrpc.client
import time
import random

# Conectar al servidor XML-RPC
server = xmlrpc.client.ServerProxy("http://localhost:9000/")

INSULTS = ["Tonto", "Cap de suro", "Inútil", "BocaChancla"]

while True:
    insult = random.choice(INSULTS)
    added = server.add_insult(insult)
    if added:
        print(f"Produced new insult: {insult}")
    else:
        print(f"Insult already exists: {insult}")
    time.sleep(5)
