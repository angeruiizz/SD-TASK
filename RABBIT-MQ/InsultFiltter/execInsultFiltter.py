import os
import time
import subprocess

def is_rabbitmq_running():
    """Comprueba si el contenedor 'rabbitmq' ya está corriendo."""
    result = subprocess.run(
        ['docker', 'ps', '--filter', 'name=rabbitmq', '--filter', 'status=running', '--format', '{{.Names}}'],
        capture_output=True, text=True
    )
    return 'rabbitmq' in result.stdout

def start_rabbitmq():
    """Inicia el contenedor de RabbitMQ, o lo lanza si no existe."""
    # Verificar si existe el contenedor
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
    time.sleep(5)  # Espera para asegurarse de que RabbitMQ arranca

# --- INICIO ---
print(" Verificando estado de RabbitMQ...")
if not is_rabbitmq_running():
    start_rabbitmq()
else:
    print("RabbitMQ ya está corriendo.")

# Scripts que se ejecutan
scripts = {
    "insultFilterConsumer": "insultConsumer.py",
    "angryProducer": "textangryProducer.py"
}

# Ejecutar los scripts en nuevas ventanas de terminal (Windows)
for name, script in scripts.items():
    print(f"Lanzando {name} en una nueva ventana de terminal...")
    os.system(f'start cmd /k "python {script}"')
    time.sleep(1)

print("Todos los procesos RabbitMQ han sido lanzados.")
