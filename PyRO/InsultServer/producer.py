import Pyro4
import random

def main():
    ns = Pyro4.locateNS()
    uri = ns.lookup("example.insultservice")
    insult_service = Pyro4.Proxy(uri)

    INSULTS = ["Tonto", "Ceporro", "Zoquete", "Inútil", "Bocachancla"]

    while True:
        insult = random.choice(INSULTS)
        if insult.lower() == 'exit':
            break
        added = insult_service.add_insult(insult)
        if added:
            print("Insulto añadido correctamente.")

if __name__ == "__main__":
    main()
