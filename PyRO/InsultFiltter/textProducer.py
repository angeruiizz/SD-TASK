# text_producer_pyro.py
import Pyro4
import time

texts = [
    "Ejemplo texto sin insultos.",
    "Todo va bien hoy.",
    "Se acerca el verano.",
    "¡Apruebo SD :)!"
]

insult_filter = Pyro4.Proxy("PYRONAME:example.insult_filter")

while True:
    for text in texts:
        print(f"TextProducer: Sending - {text}")
        insult_filter.submit_text(text)
        time.sleep(5)
