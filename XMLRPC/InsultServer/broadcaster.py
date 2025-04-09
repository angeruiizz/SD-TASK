# broadcast_xmlrpc.py
import xmlrpc.client
import time

# Conectar al servidor XML-RPC
server = xmlrpc.client.ServerProxy("http://localhost:9000/")

def broadcast_insults():
    while True:
        insults = server.get_insults()
        if insults:
            print("Broadcasting insults:")
            for insult in insults:
                print(f"  -> {insult}")
        else:
            print("No insults to broadcast.")
        time.sleep(5)

broadcast_insults()
