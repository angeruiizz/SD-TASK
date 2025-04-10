'''
o The client locates the Name Server, looks up the object
"example.remote.object", and creates a proxy.
o It calls both the greet and add methods, prints their results, and
then performs dynamic introspection by listing _pyroMethods.
'''

import Pyro4

ns = Pyro4.locateNS() #localizamos NS
uri = ns.lookup("example.remote.object") #buscamos el objeto exemplo.remote.object
print("URI encontrada:", uri)
remote_object = Pyro4.Proxy(uri) #creamos el cliente a la URI indicada

print(remote_object.greet("Alice"))  # Output esperado: "Hello, Alice!"
print(remote_object.add(5, 3))  # Output esperado: 8

# Introspección dinámica
print("Available methods:", remote_object._pyroMethods)
