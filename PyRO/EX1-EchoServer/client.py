''' The client sets the configuration for the Name Server (host and
port).
o It retrieves the remote object using "PYRONAME:echo.server"
and calls echo("HOLA").
o The response is printed.'''

import Pyro4

ns = Pyro4.locateNS("localhost", 9090)  #encontrar el name server
uri = ns.lookup("echo.server")           #encontrar el echo server
print("Server object uri:", uri)
echo_maker = Pyro4.Proxy(uri)            # creamos la proxy para esa uri 
print(echo_maker.echo("HOLA"))           #llamamos a echo
