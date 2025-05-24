import Pyro4
import random
import time
import sys

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class InsultService(object):
    def __init__(self):
        self.insults = []
        self.observers = []
        self.last_broadcast = time.time()

    def add_insult(self, insult):
        if insult not in self.insults:
            self.insults.append(insult)
            print(f"Insulto añadido: {insult}")
            return True
        else:
            return False

    def get_insults(self): 
        return self.insults

    def register(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
            print("Se ha registrado un nuevo observer", observer)

    def notify_random_insult(self):
        print("Broadcasitng insulto a los observers...")
        if not self.insults:
            return
        insult = random.choice(self.insults)
        for observer in self.observers:
            try:
                obs_proxy = Pyro4.Proxy(observer)
                obs_proxy.update(insult)
            except Exception as e:
                print("Error al notificar observer:", e)

def main():
    if len(sys.argv) < 2:
        print("Uso: python observable.py <service_name>")
        sys.exit(1)
    service_name = sys.argv[1]

    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    service = InsultService()
    uri = daemon.register(service)
    ns.register(service_name, uri) 
    print(f"InsultService corriendo como {service_name}")

    # Bucle principal del servidor
    def loop_condition():
        now = time.time()
        if now - service.last_broadcast >= 5.0:
            service.notify_random_insult()
            service.last_broadcast = now
        return True  # Siempre continuar

    daemon.requestLoop(loop_condition)

if __name__ == "__main__":
    main()
