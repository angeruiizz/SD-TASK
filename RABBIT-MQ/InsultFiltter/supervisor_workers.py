import pika
import time
import subprocess

MIN_WORKERS = 1
MAX_WORKERS = 20
TARGET_RESPONSE_TIME = 2  # Segundos objetivo para vaciar la cola
WORKER_SCRIPT = "worker.py"

def get_queue_length(queue_name='text_queue'):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    queue = channel.queue_declare(queue=queue_name, passive=True)
    message_count = queue.method.message_count
    connection.close()
    return message_count

def launch_worker():
    return subprocess.Popen(["python", WORKER_SCRIPT])

def main():
    workers = []
    for _ in range(MIN_WORKERS):
        p = launch_worker()
        workers.append(p)

    try:
        while True:
            queue_len = get_queue_length()
            # Calcula el número recomendado de workers usando backlog / tiempo objetivo
            workers_needed = max(MIN_WORKERS, min(MAX_WORKERS, int(queue_len / TARGET_RESPONSE_TIME)))
            current_workers = len(workers)

            # Escalar
            if workers_needed > current_workers:
                for _ in range(workers_needed - current_workers):
                    print("Escalando: lanzando un nuevo worker.")
                    p = launch_worker()
                    workers.append(p)
            # Desescalar
            elif workers_needed < current_workers:
                for _ in range(current_workers - workers_needed):
                    if len(workers) > MIN_WORKERS:
                        print("Reduciendo: parando un worker.")
                        p = workers.pop()
                        p.terminate()
                        p.wait()
            print(f"Mensajes en cola: {queue_len} | Workers activos: {len(workers)} | Workers recomendados: {workers_needed}")
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Terminando supervisor y todos los workers...")
        for p in workers:
            p.terminate()
            p.wait()

if __name__ == "__main__":
    main()
