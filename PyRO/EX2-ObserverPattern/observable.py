'''o The Observable class is defined and exposed using both
@Pyro4.expose and @Pyro4.behavior(instance_mode="single").
o It contains methods to register and unregister observers, as well as to
notify them.
o The server registers the Observable object with the Name Server under
"example.observable" and enters the request loop.'''
#Sigleton -> Una clase tiene una unica instanica, proporciona un punto de acceso global a ella.

import Pyro4

@Pyro4.expose #Sirve para indicar que se puede acceder de forma remota, son los metodos que puede llamar el cliente
@Pyro4.behavior(instance_mode="single") # Singleton, solo una instancia de la clase
class Observable(object): 
    def __init__(self):
        self.observers = []     # Lista paara guardar los observers

    def register(self, observer): #Registar observer
        if observer not in self.observers:
            self.observers.append(observer)
            print("Se ha registrado un nuevo observer", observer)

    def unregister(self, observer): #Eliminar observer 
        if observer in self.observers:
            self.observers.remove(observer)
            print("Observer eliminado", observer)

    def notify(self, message): # Notificar a los observers
        for observer in self.observers:
            observer = Pyro4.Proxy(observer)  # Crear un proxy del observer
            observer.update(message)  # se conecta al observer y llama al metodo update
            print("Notified observer:", observer)
    

daemon = Pyro4.Daemon() # Crear un servidor Pyro4
uri = daemon.register(Observable) # Registrar el objeto observable
ns = Pyro4.locateNS() # Localizar el Name Server
ns.register("example.observable", uri) # Registrar el objeto observable en el Name Server
print("Server is ready.")
daemon.requestLoop() # Esperar en un loop para recibir notificaciones
    
