import Pyro4
import time
import csv
import os

N = int(input("¿Cuántos insultos quieres enviar en la prueba de stress? "))
num_services = int(input("¿Cuántas instancias de InsultService quieres utilizar? "))



INSULTS = [
    "Tonto", "Cap de suro", "Inútil", "BocaChancla", "Cabezón",
    "Papanatas", "Bobalicón", "Cretino", "Lelo", "Bocazas", "QUEPASABALA"
]

# Conecta con el Name Server
ns = Pyro4.locateNS()

# Prepara proxies a los servicios (ejemplo: example.insultservice1, 2, 3...)
services = []
for i in range(1, num_services + 1):
    name = f"example.insultservice{i}"
    uri = ns.lookup(name)
    proxy = Pyro4.Proxy(uri)
    services.append(proxy)


# Enviar insultos round-robin entre instancias
start = time.time()
for i in range(N):
    insult = INSULTS[i % len(INSULTS)]
    service = services[i % num_services]
    service.add_insult(insult)
end = time.time()

print("Esperando a que todos los mensajes sean procesados...")
while True:
    total_count = sum([s.get_add_count() for s in services])
    if total_count >= N:
        break
    time.sleep(0.1)

total_time = end - start
req_per_sec = N / total_time
t_media = (total_time / N) * 1000  # ms

csv_file = 'stress_insultserver.csv'
write_header = not os.path.isfile(csv_file) or os.path.getsize(csv_file) == 0

with open(csv_file, 'a', newline='') as f:
    writer = csv.writer(f)
    if write_header:
        writer.writerow(['sistema', 'servicio', 'n_peticiones', 'workers', 'tiempo_total', 'req/s', 't_media'])
    writer.writerow(['Pyro', 'InsultServer', N, num_services, total_time, req_per_sec, t_media])

print(f"\nEnvío de {N} insultos terminado en {total_time:.3f} segundos.")
print(f"Resultados guardados en {csv_file}")
print(f"Requests/s: {req_per_sec:.2f} | Tiempo medio por mensaje: {t_media:.2f} ms")
