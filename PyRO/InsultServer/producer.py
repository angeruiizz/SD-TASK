import Pyro4
import random
import time

INSULTS = ["Tonto", "Ceporro", "Zoquete", "Inútil", "Bocachancla"]

def main():
    ns = Pyro4.locateNS()
    insult_service = Pyro4.Proxy(ns.lookup("example.insultservice"))
    while True:
        insult = random.choice(INSULTS)
        insult_service.add_insult(insult)
        time.sleep(3)

if __name__ == "__main__":
    main()
