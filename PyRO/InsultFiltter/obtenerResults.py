# obtenerResults.py
import Pyro4

insult_filter = Pyro4.Proxy("PYRONAME:example.insult_filter")

results = insult_filter.get_results()
print("Mensajes filtrados:")
for i, msg in enumerate(results, 1):
    print(f"{i}. {msg}")
