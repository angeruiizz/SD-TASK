'''
The MyRemoteObject class is defined with methods greet and
add.
o The class is exposed with @Pyro4.expose and registered with
the Name Server under "example.remote.object".
o The server prints the URI and enters the request loop.'''
import Pyro4

@Pyro4.expose
class MyRemoteObject:
    def greet(self, name):
        return "Hello, " + name + "!"
    
    def add(self, a, b):
        return a + b
    
deamon = Pyro4.Daemon() #Iniciar servidor
uri = deamon.register(MyRemoteObject) #Registrar objeto
ns = Pyro4.locateNS() #Localizar Name Server
ns.register("example.remote.object", uri) #Registrar objeto en el NS
print("Server is ready.")
print("URI:", uri)
deamon.requestLoop() #Esperar en un loop para recibir notificaciones