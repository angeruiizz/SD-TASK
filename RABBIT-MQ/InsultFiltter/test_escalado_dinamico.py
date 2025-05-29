import pika
import time

def burst_producer(queue_name='text_queue', n_messages=1000000):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    print(f"=== [PRODUCER] Enviando {n_messages} mensajes de golpe ===")
    start = time.time()
    for i in range(n_messages):
        channel.basic_publish(exchange='', routing_key=queue_name, body=f'TEST_MESSAGE {i}')
    end = time.time()
    print(f"=== [PRODUCER] Burst enviado en {end - start:.2f} segundos ===")
    connection.close()

if __name__ == "__main__":
    burst_producer(n_messages=20000)  # Puedes probar con 50000 o más si tu RAM y CPU lo permiten
    print("Burst test finalizado.")
