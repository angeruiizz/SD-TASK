# broadcast_xmlrpc.py
# hace de servidor y de cliente a la vez -> patron singleton

import xmlrpc.client
import xmlrpc.server
import time
from threading import Thread

# Conectarse al servidor de insultos
insult_server = xmlrpc.client.ServerProxy("http://localhost:9000/")

class InsultBroadcaster:
    def __init__(self):
        self.insults = []

    def fetch_insults(self):
        while True:
            try:
                new_insults = insult_server.get_insults()
                if new_insults:
                    self.insults = new_insults  # Sobrescribe la lista con los últimos insultos
                    print("Fetched and stored insults from server.")
                else:
                    print("No insults found.")
            except Exception as e:
                print(f"Error fetching insults: {e}")
            time.sleep(5)

    def get_insults(self):
        return self.insults

#parte de servidor 
broadcaster = InsultBroadcaster()
server = xmlrpc.server.SimpleXMLRPCServer(('localhost', 9001), allow_none=True)
server.register_instance(broadcaster)

# Hilo para que el broadcaster vaya actualizando insultos cada 5 segundos
fetch_thread = Thread(target=broadcaster.fetch_insults)
fetch_thread.daemon = True
fetch_thread.start()

print("Broadcaster running on port 9001...")
server.serve_forever()
