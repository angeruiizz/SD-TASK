# receiver_xmlrpc.py
import xmlrpc.client
import time

server = xmlrpc.client.ServerProxy("http://localhost:9000/")

print("Receiver is polling for insults...")

known_insults = set()

while True:
    all_insults = server.get_insults()
    new_insults = [i for i in all_insults if i not in known_insults]
    
    for insult in new_insults:
        print(f"Received insult: {insult}")
        known_insults.add(insult)
    
    time.sleep(5)
