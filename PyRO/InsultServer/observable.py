import Pyro4
import random
import time
#Sigleton -> Una clase tiene una unica instanica, proporciona un punto de acceso global a ella.

@Pyro4.expose #Sirve para indicar que se puede acceder de forma remota, son los metodos que puede llamar el cliente
@Pyro4.behavior(instance_mode="single") # Singleton, solo una instancia de la clase
class InsultService:
    def __init__(self):
        self.insults = set()
        self.observers = []

    def add_insult(self, insult):
        if insult not in self.insults:
            self.insults.add(insult)
            print(f"Insulto añadido: {insult}")
            return True
        return False

    def get_insults(self):
        return list(self.insults)

    def register(self, observer): #Registar observer
        if observer not in self.observers:
            self.observers.append(observer)
            print("Se ha registrado un nuevo observer", observer)

    def notify(self, message): # Notificar a los observers
        for observer in self.observers:
            observer = Pyro4.Proxy(observer)  # Crear un proxy del observer
            observer.update(message)  # se conecta al observer y llama al metodo update
            print("Notified observer:", observer)

    def _broadcast_loop(self):
        while True:
            time.sleep(5)
            if self.insults and self.observers:
                insult = random.choice(list(self.insults))
                print(f"Enviando insulto: {insult}")
                for observer_uri in self.observers[:]:
                    try:
                        observer = Pyro4.Proxy(observer_uri)
                        observer.update(insult)
                    except Exception as e:
                        print(f"Error notificando a {observer_uri}: {e}")
                        self.observers.remove(observer_uri)

def main():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(InsultService)
    ns.register("example.insultservice", uri)
    print("InsultService corriendo...")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
