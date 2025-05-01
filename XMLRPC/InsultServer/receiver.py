# receiver_xmlrpc.py - suscriptor que llama al broadcast()
import xmlrpc.client
import time

server = xmlrpc.client.ServerProxy("http://localhost:9000/")
print("Receiver listening to broadcasted insults...")


while True:
    current = server.broadcast() # Llama al método broadcast() del servidor
    print(f"[Received Broadcast] {current}")
    time.sleep(1)  # Hace polling cada segundo
