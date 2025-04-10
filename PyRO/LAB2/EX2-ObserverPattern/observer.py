'''o The Observer class is defined with an update method that prints
received messages.
o The observer script locates the Name Server, retrieves the Observable
object (using ns.lookup("example.observable")), and registers itself
with the observable using its remote URI.
o The observer then waits in a request loop to receive notifications.'''

#La gracia es que el observer puede hacer de servidor y cliente a la vez, es decir, puede recibir notificaciones y enviarlas a otros observers
#Por un lado se registra como observer para recibir notificaciones
#Por otro lado, actua como servidor para permitir que le notifiquen, en este caso observable

import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Observer(object):
    def update(self, message): #metodo que accede el observable para notificar a los observers
        print("Received message:", message)


def main():
    #Localizar el NS 
    ns = Pyro4.locateNS()  # Localizar el Name Server
    uri = ns.lookup("example.observable")  # Buscar el objeto observable
    print("Uri encontrada:", uri)
    observable = Pyro4.Proxy(uri)  # Crear un proxy para el objeto observable para acceder a sus metodos

    daemon = Pyro4.Daemon()  # Daemon para exponer el observer
    observer = Observer()  # Instanciar el observer
    observer_uri = daemon.register(observer)  # Registrar instancia Observer en Pyro4
    print("Observer URI:", observer_uri)


    observable.register(observer_uri)  #registrar observer en observable
    print("Observer registered.")

    daemon.requestLoop()  # Esperar en un loop para recibir notificaciones

if __name__ == "__main__":
    main()