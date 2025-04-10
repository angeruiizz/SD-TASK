import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Observer:
    def update(self, message):
        print(f"Insulto recibido: {message}")

def main():
    ns = Pyro4.locateNS()
    insult_service = Pyro4.Proxy(ns.lookup("example.insultservice"))

    daemon = Pyro4.Daemon()
    observer = Observer()
    observer_uri = daemon.register(observer)

    insult_service.register(observer_uri)
    print(f"Observer registrado y esperando insultos...")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
