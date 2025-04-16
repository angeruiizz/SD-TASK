# insult_service.py
import Pyro4
import random
import threading
import time

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class InsultService(object):
    def __init__(self):
        self.insults = []
        self.observers = []

    def add_insult(self, insult):
        if insult not in self.insults:
            self.insults.append(insult)
            print(f"Insulto añadido: {insult}")
            return True
        else:
            print(f"El insulto '{insult}' ya existe.")
            return False

    def get_insults(self): 
        return self.insults

    def register(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
            print("Se ha registrado un nuevo observer", observer) 

    def notify_random_insult(self):
        if not self.insults:
            return
        insult = random.choice(self.insults)
        for observer in self.observers:
            try:
                obs_proxy = Pyro4.Proxy(observer)
                obs_proxy.update(insult)
            except Exception as e:
                print("Error al notificar observer:", e)

    def start_broadcasting(self):
        def broadcast():
            while True:
                self.notify_random_insult()
                time.sleep(5)

        thread = threading.Thread(target=broadcast, daemon=True)
        thread.start()


def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    service = InsultService()
    uri = daemon.register(service)
    ns.register("example.insultservice", uri)
    print("InsultService corriendo...")

    service.start_broadcasting()
    daemon.requestLoop()

if __name__ == "__main__":
    main()