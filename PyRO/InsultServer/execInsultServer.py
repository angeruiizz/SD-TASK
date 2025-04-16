# execInsultServer.py : Lanza Name Server + los 4 componentes Pyro en terminales separadas

import os
import time

print("Lanzando Pyro Name Server...")
os.system('start cmd /k "python -m Pyro4.naming"')
time.sleep(2)  # Esperar un poco más para asegurarse de que arranca

#scripts que se ejecutan
scripts = {
    "Observable": "observable.py",
    "Observer": "observer.py",
    "Producer": "producer.py"
}

# ejecutar los scripts en nuevas ventanas de terminal
for name, script in scripts.items():
    print(f"Lanzando {name} en una nueva ventana de terminal...")
    os.system(f'start cmd /k "python {script}"')
    time.sleep(1)

print("Todo ha sido lanzado. Cierra las ventanas o usa Ctrl+C para parar cada proceso.")
