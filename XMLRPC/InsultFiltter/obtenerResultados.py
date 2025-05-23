# obtenerResults.py
import xmlrpc.client

server = xmlrpc.client.ServerProxy("http://localhost:9000/")
results = server.get_results()

print("Mensajes filtrados:")
for i, msg in enumerate(results, 1):
    print(f"{i}. {msg}")
