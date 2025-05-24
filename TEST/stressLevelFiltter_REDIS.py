import redis
import time
import csv
import os

num_mensajes = int(input("¿Cuántos mensjaes enviamos para la prueba de stress?"))
N = num_mensajes  # Número de mensajes a enviar

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
work_queue = "work_queue"
results_list = "RESULTS"

# Limpieza de colas ya que REDIS si que lo permite
client.delete(work_queue)
client.delete(results_list)

base_texts = [
    "Eres un tonto, ¿por qué vas tan lento?",
    "Eres tan estúpido que no sé qué haces aquí.",
    "La gente te considera un imbécil por cómo actúas.",
    "No puedo creer que seas tan idiota.",
    "Ets un cap de suro.",
    "Puedes ser más gilipollas????",
    "Apruebo SD",
    "Ayer fui a la playa",
    "De aquí poco es mi graduación"
]

num_workers = int(input("¿Cuántos workers tienes corriendo? (1, 2, 3, etc.): "))
input("Lanza los workers.py en otras terminales y pulsa Enter aquí para continuar...")

start = time.time()
for i in range(N):
    text = base_texts[i % len(base_texts)]
    client.rpush(work_queue, text)
end_send = time.time()

print("Esperando a que todos los mensajes sean procesados...")
while client.llen(results_list) < N:
    time.sleep(0.1)

end = time.time()
total_time = end - start
time_sending = end_send - start
processing_time = end - end_send

req_per_sec = N / total_time
t_media = (total_time / N) * 1000  # ms

csv_file = 'stress_insultfiltter.csv'
write_header = not os.path.isfile(csv_file) or os.path.getsize(csv_file) == 0

with open(csv_file, 'a', newline='') as f:
    writer = csv.writer(f)
    if write_header:
        writer.writerow(['sistema', 'servicio', 'n_peticiones', 'workers', 'tiempo_total', 'req/s', 't_media'])
    writer.writerow(['Redis', 'InsultFilter', N, num_workers, total_time, req_per_sec, t_media])

print(f"\nEnvío de {N} mensajes terminado en {total_time:.3f} segundos.")
print(f"Tiempo de envío: {time_sending:.3f}s | Tiempo de procesado: {processing_time:.3f}s")
print(f"Resultados guardados en {csv_file}")
print(f"Requests/s: {req_per_sec:.2f} | Tiempo medio por mensaje: {t_media:.2f} ms")
