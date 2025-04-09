# insult_server_xmlrpc.py
import random
from xmlrpc.server import SimpleXMLRPCServer

# Clase para gestionar insultos
class InsultServer:
    def __init__(self):
        self.insults = []
        self.broadcasted = []

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

    def insult_me(self):
        if self.insults:
            return random.choice(self.insults)
        return "No hay insultos disponibles."

    def get_new_insults(self):
        # Devuelve los insultos que aún no han sido "broadcasted"
        new_insults = [i for i in self.insults if i not in self.broadcasted]
        self.broadcasted.extend(new_insults)
        return new_insults


# servidor XML-RPC
server = SimpleXMLRPCServer(("localhost", 9000), allow_none=True)
server.register_introspection_functions()

# Registrar el servicio
service = InsultServer()
server.register_instance(service)



print("Insult XML-RPC Server is running on port 9000...")
server.serve_forever()
