# InsulraServer.py : Lanza todos los scripts en ventanas de terminal separadas

import os
import time

scripts = {
    "Server": "insultConsumer.py",
    "ProducerText": "textProducer.py",
    "ProducerWInsults": "insultProducer.py",
    "Worker": "worker.py"   # <--- ¡AÑADE EL WORKER!
}

# Ejecutar cada script en una nueva ventana de terminal (cmd)
for name, script in scripts.items():
    print(f"Lanzando {name} en una nueva ventana de terminal...")
    os.system(f'start cmd /k "python {script}"')
    time.sleep(1)  # Espera para evitar solapamientos

print("Scripts lanzados. Presiona Ctrl+C en cada ventana para detenerlos.")
