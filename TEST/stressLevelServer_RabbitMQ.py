import pika
import time
import csv
import os

num_mensajes = int(input("¿Cuántos insultos envías para la prueba de stress? "))
N = num_mensajes  # Número de mensajes a enviar
insult_queue = 'insult_queue'

insults = ["Tonto", "Ceporro", "Zoquete", "Inútil", "Bocachancla", "Torpe", "Cabezón",
           "Bobalicón", "Lelo", "Bobalón", "Cretino", "Patán", "Zopenco", "Mediocre",
           "Lerdos", "Burrito", "Papanatas", "Cabezón", "Tontorrón", "Capdesuro"]

num_workers = int(input("¿Cuántos consumers tienes corriendo? (1, 2, 3, etc.): "))
input("Lanza los RMQConsumer.py en otras terminales y pulsa Enter aquí para continuar...")

def clean_queue(channel, queue_name):
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_purge(queue=queue_name)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
clean_queue(channel, insult_queue)

start = time.time()
for i in range(N):
    insult = insults[i % len(insults)]
    channel.basic_publish(
        exchange='',
        routing_key=insult_queue,
        body=insult.encode(),
        properties=pika.BasicProperties(delivery_mode= pika.DeliveryMode.Persistent) 
    )
end_send = time.time()

print("Esperando a que todos los insultos sean procesados...")
def get_queue_count():
    return channel.queue_declare(queue=insult_queue, passive=True).method.message_count

while get_queue_count() > 0:
    time.sleep(0.1)

# TODO: Implementar una cola de resultados si es necesario

end = time.time()
total_time = end - start
time_sending = end_send - start
processing_time = end - end_send

req_per_sec = N / total_time
t_media = (total_time / N) * 1000  # ms

csv_file = 'stress_insultserver.csv'
write_header = not os.path.isfile(csv_file) or os.path.getsize(csv_file) == 0

with open(csv_file, 'a', newline='') as f:
    writer = csv.writer(f)
    if write_header:
        writer.writerow(['sistema', 'servicio', 'n_peticiones', 'workers', 'tiempo_total', 'req/s', 't_media'])
    writer.writerow(['RabbitMQ', 'InsultServer', N, num_workers, total_time, req_per_sec, t_media])

print(f"\nEnvío de {N} insultos terminado en {total_time:.3f} segundos.")
print(f"Tiempo de envío: {time_sending:.3f}s | Tiempo de procesado: {processing_time:.3f}s")
print(f"Resultados guardados en {csv_file}")
print(f"Requests/s: {req_per_sec:.2f} | Tiempo medio por mensaje: {t_media:.2f} ms")
