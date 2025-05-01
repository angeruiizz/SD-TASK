# consumer.py - servidor XML-RPC sin hilos
import random
import time
from xmlrpc.server import SimpleXMLRPCServer

class InsultServer:
    def __init__(self):
        self.insults = []
        self.last_broadcasted = None
        self.last_broadcast_time = 0  # timestamp

    def add_insult(self, insult):
        if insult not in self.insults:
            self.insults.append(insult)
            print(f"Added insult: {insult}")
            return f"Added insult: {insult}"
        else:
            print(f"Insult already exists: {insult}")
            return f"Insult already exists: {insult}"

    def get_insults(self):
        return self.insults

    def get_last_broadcasted(self):
        return self.last_broadcasted

    def broadcast(self):
        """Simula el broadcast cada 5 segundos."""
        print("Broadcasting...")
        now = time.time()
        if now - self.last_broadcast_time >= 5 and self.insults:
            insult = random.choice(self.insults)
            self.last_broadcasted = insult
            self.last_broadcast_time = now
            print(f"[Broadcasted] {insult}")
        return self.last_broadcasted

server = SimpleXMLRPCServer(("localhost", 9000), allow_none=True)
server.register_introspection_functions()
service = InsultServer()
server.register_instance(service)

print("Insult XML-RPC Server is running on port 9000...")
server.serve_forever()
