import redis
import time

# Conectar a Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

work_queue = "work_queue"
results_list = "RESULTS"
insults = ["tonto", "estúpido", "imbécil", "idiota", "lento"]

def clean_text(text):
    """Reemplaza los insultos por 'CENSORED'."""
    for insult in insults:
        text = text.replace(insult, "CENSORED")
    return text

while True:
    # Recupera el trabajo de la cola de manera bloqueante
    task = client.blpop(work_queue, timeout=0)
    if task:
        text = task[1]  # Extrae el mensaje
        clean_message = clean_text(text)  #Remplazar los mensajes por CENSORED
        client.rpush(results_list, clean_message)  # Almacena el texto limpio en la lista RESULTS
        print(f"InsultConsumer: Processed and saved cleaned text - {clean_message}")
