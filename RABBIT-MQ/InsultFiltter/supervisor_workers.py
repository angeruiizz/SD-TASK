import pika
import time
import multiprocessing
import os

MIN_WORKERS = 1
MAX_WORKERS = 5
UPPER_THRESHOLD = 50
LOWER_THRESHOLD = 5
WORKER_SCRIPT = "worker.py"

def get_queue_length(queue_name='text_queue'):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    queue = channel.queue_declare(queue=queue_name, passive=True)
    message_count = queue.method.message_count
    connection.close()
    return message_count

def run_worker():
    os.system(f"python {WORKER_SCRIPT}")

def launch_worker():
    return multiprocessing.Process(target=run_worker)

def main():
    workers = []
    for _ in range(MIN_WORKERS):
        p = launch_worker()
        p.start()
        workers.append(p)

    try:
        while True:
            queue_len = get_queue_length()
            print(f"Mensajes en cola: {queue_len} | Workers activos: {len(workers)}")

            if queue_len > UPPER_THRESHOLD and len(workers) < MAX_WORKERS:
                print("Escalando: lanzando un nuevo worker.")
                p = launch_worker()
                p.start()
                workers.append(p)

            elif queue_len < LOWER_THRESHOLD and len(workers) > MIN_WORKERS:
                print("Reduciendo: parando un worker.")
                p = workers.pop()
                p.terminate()
                p.join()


    except KeyboardInterrupt:
        print("Terminando supervisor y todos los workers...")
        for p in workers:
            p.terminate()
            p.join()

if __name__ == "__main__":
    main()
