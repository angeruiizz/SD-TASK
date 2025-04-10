# broadcaster.py

import Pyro4
import random
import time

def main():
    # Localizar el Name Server
    ns = Pyro4.locateNS()
    # Buscar el objeto InsultService registrado
    uri = ns.lookup("example.observable")
    insult_service = Pyro4.Proxy(uri)

    print("Broadcaster conectado al InsultService.")
    
    while True:
        try:
            insults = insult_service.get_insults()
            if insults:
                insult = random.choice(insults)
                print(f"Broadcasting insult: {insult}")
                insult_service.notify(insult)
            else:
                print("No hay insultos para difundir.")
        except Exception as e:
            print(f"Error broadcasting insult: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    main()
