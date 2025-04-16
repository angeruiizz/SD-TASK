# Tasca 2
Sistema basado en una cola de mensajes con productores y consumidores

Tiene dos productores:
- TextProducer: Envia mensjaes sin insultos cada 5 seg
- AngryProducer: Envia mensajes con insultos cada 3 seg

Tiene un consumidor:
- InsultConsumer: Recuper los mensajes de la cola y sustituye los insultos por *CENSORED*
                  Guarda los mensajes limpios en una lista 
Y acyua como productor de estos mensjaes al cliente final 