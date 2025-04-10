'''► Notification Script:
o The separate script to notify observers creates a proxy for
"PYRONAME:example.observable" and calls
notify_observers("Hello, Observers!"'''

import Pyro4

def main():
    ns = Pyro4.locateNS()  # Localizar el Name Server
    uri = ns.lookup("example.observable")  # Buscar el objeto observable
    print("Uri encontrada:", uri)

    observable = Pyro4.Proxy(uri)  # Crear un proxy para el objeto observable
    observable.notify("Hello, Observers!")  # Enviar mensaje a los observers
    print("Notificación enviada.")

if __name__ == "__main__":
    main()
