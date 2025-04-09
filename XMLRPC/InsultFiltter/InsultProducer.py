import xmlrpc.client
import time
import random

# Conectar al servidor XML-RPC
server = xmlrpc.client.ServerProxy("http://localhost:9000/") #para conectarse al servidor

INSULTS = ["Tonto", "Cap de suro", "Inútil", "BocaChancla"] #insultos que se enviaran al servidorç

textos = [
    "Eres un tonto, ¿por qué vas tan lento?",
    "Eres tan estúpido que no se que haces aqui",
    "La gente te considera un imbécil por cómo actúas.",
    "No puedo creer que seas tan idiota.",
    "Ets un cap de suro"
    "Puedes ser mas gilipollas????"
]

while True:
    text = random.choice(textos) #selecciona un texto aleatorio
    response = server.add_text(text) #envia el insulto al servidor
    print(response)
    time.sleep(5) #espera 5 segundos antes de enviar el siguiente insulto

