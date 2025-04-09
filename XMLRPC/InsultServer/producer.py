# producer_xmlrpc.py
import xmlrpc.client
import time
import random

# Conectar al servidor XML-RPC
server = xmlrpc.client.ServerProxy("http://localhost:9000/")

INSULTS = ["Tonto", "Cap de suro", "Inútil", "BocaChancla"]

while True:
    insult = random.choice(INSULTS)
    response = server.add_insult(insult)
    print(response)
    time.sleep(5)

