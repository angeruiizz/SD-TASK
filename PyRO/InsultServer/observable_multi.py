from multiprocessing import Process
import sys
import time
import Pyro4
import random

def launch_pyro_server(service_name):
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

        def clear_insults(self):
            self.insults.clear()
            print("Lista de insultos limpiada.")

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

    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    service = InsultService()
    uri = daemon.register(service)
    ns.register(service_name, uri)
    print(f"InsultService corriendo como {service_name}")

    def loop_condition():
        now = time.time()
        if now - service.last_broadcast >= 5.0:
            service.notify_random_insult()
            service.last_broadcast = now
        return True

    daemon.requestLoop(loop_condition)

if __name__ == "__main__":
    num_servers = int(input("¿Cuántos servidores Pyro lanzar en paralelo? "))

    procs = []
    for i in range(num_servers):
        service_name = f"example.insultservice{i+1}"
        p = Process(target=launch_pyro_server, args=(service_name,))
        p.start()
        procs.append(p)
        time.sleep(0.2)  # pequeño retardo para evitar colisiones

    print("¡Todos los servidores Pyro están lanzados! Pulsa Ctrl+C para terminar.")
    try:
        for p in procs:
            p.join()
    except KeyboardInterrupt:
        print("Cerrando servidores Pyro...")
        for p in procs:
            p.terminate()
