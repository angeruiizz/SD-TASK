# worker.py
import Pyro4
import time

insult_filter = Pyro4.Proxy("PYRONAME:example.insult_filter")
insults = ["tonto", "estúpido", "imbécil", "idiota", "lento", "cap de suro", "gilipollas"]

def clean_text(text):
    for insult in insults:
        text = text.replace(insult, "CENSORED")
    return text

while True:
    print("Worker: pidiendo trabajo...")
    text = insult_filter.get_next_text()
    if text:
        print(f"Worker: Processing - {text}")
        clean_message = clean_text(text)
        insult_filter.submit_result(clean_message)
    else:
        print("Worker: nada que hacer, esperando...")
        time.sleep(1)
