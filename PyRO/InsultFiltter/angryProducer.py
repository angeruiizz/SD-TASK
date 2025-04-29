# angry_producer_pyro.py
import Pyro4
import time
import random

insults = ["tonto", "estúpido", "imbécil", "idiota", "lento", "cap de suro", "gilipollas"]
texts = [
    "Eres un tonto, ¿por qué vas tan lento?",
    "Eres tan estúpido que no se qué haces aquí.",
    "La gente te considera un imbécil por cómo actúas.",
    "No puedo creer que seas tan idiota.",
    "Ets un cap de suro.",
    "Puedes ser más gilipollas????"
]

insult_filter = Pyro4.Proxy("PYRONAME:example.insult_filter")

while True:
    text = random.choice(texts)
    print(f"AngryProducer: Sending - {text}")
    insult_filter.submit_text(text)
    time.sleep(3)
