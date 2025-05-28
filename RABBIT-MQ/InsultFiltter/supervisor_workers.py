import pika
import time
import subprocess

MIN_WORKERS = 1
MAX_WORKERS = 10
UPPER_THRESHOLD = 10
LOWER_THRESHOLD = 1
WORKER_SCRIPT = "worker.py"

def get_queue_length(queue_name='text_queue'):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    queue = channel.queue_declare(queue=queue_name, passive=True)
    message_count = queue.method.message_count
    connection.close()
    return message_count

def launch_worker():
    # Lanza el worker y devuelve el objeto proceso real
    return subprocess.Popen(["python", WORKER_SCRIPT])

def main():
    workers = []
    for _ in range(MIN_WORKERS):
        p = launch_worker()
        workers.append(p)

    try:
        while True:
            queue_len = get_queue_length()
            print(f"Mensajes en cola: {queue_len} | Workers activos: {len(workers)}")

            # Escalar
            if queue_len > UPPER_THRESHOLD and len(workers) < MAX_WORKERS:
                print("Escalando: lanzando un nuevo worker.")
                p = launch_worker()
                workers.append(p)

            # Desescalar
            elif queue_len < LOWER_THRESHOLD and len(workers) > MIN_WORKERS:
                print("Reduciendo: parando un worker.")
                p = workers.pop()
                p.terminate()
                p.wait()
            time.sleep(1)

    except KeyboardInterrupt:
        print("Terminando supervisor y todos los workers...")
        for p in workers:
            p.terminate()
            p.wait()

if __name__ == "__main__":
    main()
