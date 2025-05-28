import subprocess
import time
import pika

def stress_producer(queue_name='text_queue', burst_duration=40, slow_duration=5, messages_per_sec_fast=10000, 
                    messages_per_sec_slow=2):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    print("=== [PRODUCER] Inicio de carga alta (burst) ===")
    start = time.time()
    while time.time() - start < burst_duration:
        channel.basic_publish(exchange='', routing_key=queue_name, body='TEST_MESSAGE')
        time.sleep(1 / messages_per_sec_fast)
    print("=== [PRODUCER] Inicio de carga baja ===")
    start = time.time()
    while time.time() - start < slow_duration:
        channel.basic_publish(exchange='', routing_key=queue_name, body='TEST_MESSAGE')
        time.sleep(1 / messages_per_sec_slow)
    print("=== [PRODUCER] Productor de stress terminado ===")
    connection.close()

if __name__ == "__main__":
    stress_producer()
    print("Test de escalado dinámico finalizado.")
