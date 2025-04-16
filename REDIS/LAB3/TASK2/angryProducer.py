import redis
import time
import random

# Conectar a Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

work_queue = "work_queue"

# Insultos que serán insertados en los mensajes
insults = ["tonto", "estúpido", "imbécil", "idiota", "lento"]

# Mensajes base que contienen insultos insertados aleatoriamente
base_texts = [
    "Eres un tonto, ¿por qué no puedes ser más rápido?",
    "Eres tan estúpido que no sabes lo que haces.",
    "La gente te considera un imbécil por cómo actúas.",
    "No puedo creer que seas tan idiota.",
    "¿Por qué eres tan lento? ¡Apúrate!"
]

while True:
    text = random.choice(base_texts)  # Selecciona un texto con insultos aleatorios
    client.rpush(work_queue, text)  # Envia el mensaje con insultos a la cola
    print(f"AngryProducer: Produced angry text - {text}")
    time.sleep(3)  # Espera 3 segundos antes de enviar el siguiente mensaje
