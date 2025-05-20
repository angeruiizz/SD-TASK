import redis

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
results_list = "RESULTS"

resultados = client.lrange(results_list, 0, -1)

print("Mensajes filtrados:")
for i, mensaje in enumerate(resultados, 1):
    print(f"{i}. {mensaje}")
