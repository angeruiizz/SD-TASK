import xmlrpc.client
import time
import csv
import os

N = int(input("¿Cuántos insultos quieres enviar en la prueba de stress? "))
num_servers = int(input("¿Cuántos servidores XML-RPC quieres utilizar? "))

INSULTS = [
    "Tonto", "Cap de suro", "Inútil", "BocaChancla", 
    "Cabezón", "Papanatas", "Bobalicón", "Cretino", 
    "Lelo", "Bocazas", "QUEPASABALA"
]

# Asume que cada servidor está en un puerto consecutivo (9000, 9001, 9002, ...)
servers = []
for i in range(num_servers):
    port = 9000 + i
    url = f"http://localhost:{port}/"
    servers.append(xmlrpc.client.ServerProxy(url))

# Limpiar insultos en todos los servidores (si tienes clear_insults)
for server in servers:
    try:
        server.clear_insults()
    except Exception:
        pass

start = time.time()
for i in range(N):
    insult = INSULTS[i % len(INSULTS)]
    # Reparte los insultos round-robin entre los servidores
    server = servers[i % num_servers]
    server.add_insult(insult)
end = time.time()

total_time = end - start
req_per_sec = N / total_time
t_media = (total_time / N) * 1000  # ms

csv_file = 'stress_insultserver.csv'
write_header = not os.path.isfile(csv_file) or os.path.getsize(csv_file) == 0

with open(csv_file, 'a', newline='') as f:
    writer = csv.writer(f)
    if write_header:
        writer.writerow(['sistema', 'servicio', 'n_peticiones', 'workers', 'tiempo_total', 'req/s', 't_media'])
    writer.writerow(['XMLRPC', 'InsultServer', N, num_servers, total_time, req_per_sec, t_media])

print(f"\nEnvío de {N} insultos terminado en {total_time:.3f} segundos usando {num_servers} servidores.")
print(f"Resultados guardados en {csv_file}")
print(f"Requests/s: {req_per_sec:.2f} | Tiempo medio por mensaje: {t_media:.2f} ms")
