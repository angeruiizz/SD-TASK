import xmlrpc.client
import time
import random

# Conectar al servidor XML-RPC
server = xmlrpc.client.ServerProxy("http://localhost:9000/") #para conectarse al servidor

print("Enviando textos sin insultos al servidor...")
textos = [
    "Ejemplo text sin insultos.",
    "Todo va bien hoy.",
    "Se acerca verano",
    "Apruebo SD :)"
]

while True:
    text = random.choice(textos) #selecciona un texto aleatorio
    response = server.add_text(text) #envia el insulto al servidor
    print(response)
    time.sleep(5) #espera 5 segundos antes de enviar el siguiente insulto

