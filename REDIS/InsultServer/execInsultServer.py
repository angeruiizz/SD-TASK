# Lanza scripts en ventanas separadas y arranca Redis si no está activo

import os
import time
import redis

def check_or_start_redis():
    try:
        client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        client.ping()
        print("Redis ya está en ejecución.")
    except redis.exceptions.ConnectionError:
        print("⚠️ Redis no está en ejecución. Intentando lanzarlo con Docker...")
        os.system("docker rm -f insult_redis >nul 2>&1")  # Elimina contenedor anterior si existe
        os.system("docker run -d --name insult_redis -p 6379:6379 redis")
        time.sleep(2)  # Espera a que arranque
        print("Redis lanzado correctamente.")

check_or_start_redis()

scripts = {
    "Server": "observable.py",
    "ProducerText": "producer.py",
    "Observer": "observer.py",
}

for name, script in scripts.items():
    print(f"Lanzando {name} en una nueva ventana de terminal...")
    os.system(f'start cmd /k "python {script}"')
    time.sleep(1)

print("Todos los scripts han sido lanzados.")
