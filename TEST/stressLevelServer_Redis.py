import redis
import time
import csv
import os

N = int(input("¿Cuántos insultos quieres enviar en la prueba de stress? "))
num_producers = int(input("¿Cuánto servidores quieres escalar: "))
input("Lanza observable.py (según el num se server q deseas) en otras terminales y pulsa Enter aquí para continuar...")

INSULTS = ["Tonto", "Cap de suro", "Inútil", "BocaChancla", "Cabezón", "Papanatas", "Bobalicón", "Cretino", "Lelo", "Bocazas", "QUEPASABALA"]
INPUT_CHANNEL = "INSULTS_input"
INSULT_SET = "INSULTS_set"
INSULT_LIST = "INSULTS_list"

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Limpiar estado previo
client.delete(INSULT_SET)
client.delete(INSULT_LIST)

# 1. Envío rápido de mensajes al canal de entrada
start = time.time()
for i in range(N):
    insult = INSULTS[i % len(INSULTS)]
    client.rpush("insults_queue", insult)
end_send = time.time()

# 2. Espera a que se procesen todos (es decir, que todos estén en el set/lista)
print("Esperando a que todos los insultos hayan sido procesados y guardados en el set...")

end = time.time()
total_time = end - start
time_sending = end_send - start

req_per_sec = N / total_time
t_media = (total_time / N) * 1000  # ms

csv_file = 'stress_insultserver.csv'
write_header = not os.path.isfile(csv_file) or os.path.getsize(csv_file) == 0

with open(csv_file, 'a', newline='') as f:
    writer = csv.writer(f)
    if write_header:
        writer.writerow(['sistema', 'servicio', 'n_peticiones', 'producers', 'tiempo_total', 'req/s', 't_media'])
    writer.writerow(['Redis', 'InsultServer', N, num_producers, total_time, req_per_sec, t_media])

print(f"\nEnvío de {N} insultos terminado en {total_time:.3f} segundos.")
print(f"Resultados guardados en {csv_file}")
print(f"Requests/s: {req_per_sec:.2f} | Tiempo medio por mensaje: {t_media:.2f} ms")
print(f"Insultos únicos almacenados: {client.scard(INSULT_SET)}")