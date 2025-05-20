# insultWorker.py
import redis

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

work_queue = "work_queue"
results_list = "RESULTS"
insults = ["tonto", "estúpido", "imbécil", "idiota", "lento", "cap de suro", "gilipollas"]

def clean_text(text):
    for insult in insults:
        text = text.replace(insult, "CENSORED")
    return text

if __name__ == "__main__":
    print("InsultWorker iniciado. Esperando mensajes...")
    while True:
        task = client.blpop(work_queue, timeout=0)
        if task:
            text = task[1]
            clean_message = clean_text(text)
            client.rpush(results_list, clean_message)
            print(f"InsultWorker: Processed - {clean_message}")
