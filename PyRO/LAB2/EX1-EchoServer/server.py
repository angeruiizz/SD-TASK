'''o The EchoServer class is exposed with @Pyro4.expose.
o The server creates a Pyro Daemon, locates the Name Server,
registers the object, and then registers it with the Name Server
using the name "echo.server".
o The code then enters the request loop to wait for incoming
requests.'''

import Pyro4

@Pyro4.expose
class EchoServer(object):
    def echo(self, message): #creamos el metodo echo para mandar mensajes
        return message

daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(EchoServer)
ns.register("echo.server", uri)

print("Ready. Object uri =", uri)      # print the uri so we can use it in the client later
daemon.requestLoop()                   # start the event loop of the server to wait for calls