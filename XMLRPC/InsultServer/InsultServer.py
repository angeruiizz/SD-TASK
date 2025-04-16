# InsulraServer.py : Lanza todos los scripts en ventanas de terminal separadas

import os
import time

scripts = {
    "Server": "consumer.py",
    "Producer": "producer.py",
    "Receiver": "receiver.py"
}

# Ejecutar cada script en una nueva ventana de terminal (cmd)
for name, script in scripts.items():
    print(f"Lanzando {name} en una nueva ventana de terminal...")
    os.system(f'start cmd /k "python {script}"')
    time.sleep(1)  # Espera para evitar solapamientos

print("Scripts lanzados. Presiona Ctrl+C en cada ventana para detenerlos.")
