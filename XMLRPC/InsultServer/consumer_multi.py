from multiprocessing import Process
import sys
import time

def launch_server(port):
    import random
    from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

    class InsultServer:
        def __init__(self):
            self.insults = []
            self.last_broadcasted = None
            self.last_broadcast_time = 0

        def add_insult(self, insult):
            if insult not in self.insults:
                self.insults.append(insult)
                return f"Added insult: {insult}"
            else:
                return f"Insult already exists: {insult}"

        def get_insults(self):
            return self.insults

        def get_last_broadcasted(self):
            return self.last_broadcasted

        def broadcast(self):
            now = time.time()
            if now - self.last_broadcast_time >= 5 and self.insults:
                insult = random.choice(self.insults)
                self.last_broadcasted = insult
                self.last_broadcast_time = now
            return self.last_broadcasted

        def clear_insults(self):
            self.insults.clear()
            return "Cleared"

    server = SimpleXMLRPCServer(("localhost", port), allow_none=True)
    server.register_introspection_functions()
    service = InsultServer()
    server.register_instance(service)
    print(f"Server running on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    num_servers = int(input("¿Cuántos servidores lanzar en paralelo? "))
    base_port = 9000

    procs = []
    for i in range(num_servers):
        port = base_port + i
        p = Process(target=launch_server, args=(port,))
        p.start()
        procs.append(p)
        time.sleep(0.2)  # pequeño retardo para evitar colisiones

    print("¡Todos los servidores están lanzados! Pulsa Ctrl+C para terminar.")
    try:
        for p in procs:
            p.join()
    except KeyboardInterrupt:
        print("Cerrando servidores...")
        for p in procs:
            p.terminate()
