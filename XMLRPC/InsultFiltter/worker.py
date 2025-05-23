# worker.py
import xmlrpc.client
import time

INSULTS = ["tonto", "cap de suro", "inútil", "bocachancla", "idiota", "estúpido", "imbécil", "gilipollas"]

def clean_text(text):
    for insult in INSULTS:
        text = text.replace(insult, "CENSORED")
        text = text.replace(insult.lower(), "CENSORED")
        text = text.replace(insult.capitalize(), "CENSORED")
    return text

server = xmlrpc.client.ServerProxy("http://localhost:9000/")

while True:
    print("Worker: pidiendo trabajo...")
    text = server.get_next_text()
    if text:
        print(f"Worker: Processing - {text}")
        clean_message = clean_text(text)
        server.submit_result(clean_message)
    else:
        print("Worker: nada que hacer, esperando...")
        time.sleep(1)
