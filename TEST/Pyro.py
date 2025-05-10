import threading
import time
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from consumer import InsultServer  # Usa tu clase original

class TestXMLRPC:
    def __init__(self):
        self.server_thread = None
        self.server = None
        self.proxy = None

    def start_server(self, host="localhost", port=9000):
        def server_target():
            self.server = SimpleXMLRPCServer((host, port), allow_none=True, logRequests=False)
            self.server.register_instance(InsultServer())
            print(f"[SERVER] XML-RPC InsultServer lanzado en {host}:{port}")
            self.server.serve_forever()

        self.server_thread = threading.Thread(target=server_target, daemon=True)
        self.server_thread.start()
        time.sleep(1)  # Espera a que arranque
        self.proxy = xmlrpc.client.ServerProxy(f"http://{host}:{port}/")
    
    def test_add_insults(self):
        print("\n== Añadiendo insultos ==")
        print(self.proxy.add_insult("Tonto"))
        print(self.proxy.add_insult("Cap de suro"))
        print(self.proxy.add_insult("Tonto"))  # Duplicado

    def test_get_insults(self):
        print("\n== Obteniendo insultos ==")
        print("Insults:", self.proxy.get_insults())

    def test_broadcast(self):
        print("\n== Probar broadcast ==")
        for i in range(10):
            result = self.proxy.broadcast()
            print(f"[{i}] Broadcasted: {result}")
            time.sleep(1)

    def run_all(self):
        self.start_server()
        self.test_add_insults()
        self.test_get_insults()
        self.test_broadcast()


if __name__ == "__main__":
    tester = TestXMLRPC()
    tester.run_all()
