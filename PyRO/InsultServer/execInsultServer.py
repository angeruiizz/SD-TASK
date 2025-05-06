# execInsultServer.py : Lanza Name Server + los 3 componentes Pyro en terminales separadas

import os
import time

print("Lanzando Pyro Name Server...")
os.system('start cmd /k "python -m Pyro4.naming"')
time.sleep(2)  # Esperar que arranque el Name Server

print("Lanzando Observable (servidor)...")
os.system('start cmd /k "python observable.py"')
time.sleep(3)  # Esperar a que el servidor se registre en el Name Server

# Ahora lanzar observer y producer
scripts = {
    "Observer": "observer.py",
    "Producer": "producer.py"
}

for name, script in scripts.items():
    print(f"Lanzando {name} en una nueva ventana de terminal...")
    os.system(f'start cmd /k "python {script}"')
    time.sleep(1)

print("Todo ha sido lanzado. Cierra las ventanas o usa Ctrl+C para parar cada proceso.")
