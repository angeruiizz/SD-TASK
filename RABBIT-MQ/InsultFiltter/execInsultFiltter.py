import os
import time
import subprocess

def is_rabbitmq_running():
    result = subprocess.run(
        ['docker', 'ps', '--filter', 'name=rabbitmq', '--filter', 'status=running', '--format', '{{.Names}}'],
        capture_output=True, text=True
    )
    return 'rabbitmq' in result.stdout

def start_rabbitmq():
    result = subprocess.run(['docker', 'ps', '-a', '--format', '{{.Names}}'], capture_output=True, text=True)
    if 'rabbitmq' in result.stdout:
        print("Iniciando contenedor RabbitMQ existente...")
        subprocess.run(['docker', 'start', 'rabbitmq'])
    else:
        print("Contenedor RabbitMQ no existe. Descargando e iniciando...")
        subprocess.run(['docker', 'pull', 'rabbitmq:management'])
        subprocess.run([
            'docker', 'run', '-d',
            '--name', 'rabbitmq',
            '-p', '5672:5672',
            '-p', '15672:15672',
            'rabbitmq:management'
        ])
    time.sleep(10)  # Espera más por seguridad

# --- INICIO ---
print("Verificando estado de RabbitMQ...")
if not is_rabbitmq_running():
    start_rabbitmq()
else:
    print("RabbitMQ ya está corriendo.")

# Test de conexión a RabbitMQ antes de lanzar los scripts
import pika
for i in range(10):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        connection.close()
        print("RabbitMQ responde correctamente.")
        break
    except Exception:
        print("Esperando que RabbitMQ esté disponible...")
        time.sleep(2)
else:
    print("No se pudo conectar a RabbitMQ. Saliendo.")
    exit(1)

# Scripts que se ejecutan
scripts = {
    "worker": "worker.py",
    "angryProducer": "textangryProducer.py"
}

for name, script in scripts.items():
    print(f"Lanzando {name} en una nueva ventana de terminal...")
    os.system(f'start cmd /k "python {script}"')
    time.sleep(1)

print("Todos los procesos RabbitMQ han sido lanzados.")
