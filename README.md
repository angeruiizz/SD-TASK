# Middleware Services: InsultService & InsultFilter

Este proyecto implementa dos servicios distribuidos usando cuatro middlewares diferentes: **XMLRPC, PyRO, Redis y RabbitMQ**.

- **InsultService**: Recibe insultos remotamente, los almacena sin duplicados y difunde insultos aleatorios a los clientes cada 5 segundos.
- **InsultFilter**: Recibe textos de clientes, filtra insultos (los reemplaza por “CENSORED”) y almacena los resultados usando el patrón Work Queue.



## Middlewares y patrones usados

- **XMLRPC**  
  Comunicación directa y síncrona (cliente-servidor). Simula difusión (broadcast) usando polling, no soporta pub/sub real.

- **PyRO**  
  Comunicación directa con objetos remotos. Permite callbacks para pub/sub real (Observer pattern) y trabajo en paralelo con work queues.

- **Redis**  
  Comunicación indirecta y asíncrona mediante pub/sub y listas (work queues). Productores y consumidores están desacoplados.

- **RabbitMQ**  
  Comunicación indirecta y asíncrona usando colas y exchanges. Soporta point-to-point, publish/subscribe y balanceo de carga real.


## Estructura y ejecución

Cada middleware tiene dos servicios:
- **InsultService** (difusión de insultos)
- **InsultFilter** (filtrado de textos)

Cada carpeta contiene scripts de servidor y clientes/productores/consumidores.

### Ejecución básica

1. Instala Python 3.8+ y las librerías requeridas (`pip install -r requirements.txt` si hay).
2. Ve al directorio de la tecnología y servicio deseados.
3. Ejecuta:

```bash
python ./execInsultServer.py
# o para el filtro:
python ./execInsultFilter.py
```

# Arquitecturas de los Servicios

## XMLRPC

### InsultService
- El servidor expone métodos remotos (`añadir_insulto`, `listar`, `obtener_insulto_aleatorio`).
- Los clientes llaman directamente al servidor para añadir o consultar insultos.
- **No hay eventos ni callbacks**; la difusión/broadcast se simula mediante polling por parte de los clientes (los clientes preguntan periódicamente).

### InsultFilter
- El servidor central mantiene una **cola de textos** y una lista de resultados filtrados.
- Productores envían textos al servidor.
- Los workers piden un texto, lo filtran y devuelven el resultado.
- **Todo está centralizado** en el servidor: tanto la cola como la lógica de filtrado.


## PyRO

### InsultService
- El servidor central registra insultos y mantiene una lista de **observadores** (Observer pattern).
- Cada 5 segundos, el servidor llama al método `update` de cada observer registrado (**callback**, difusión real).
- Hay verdadera difusión tipo **publish/subscribe** implementada por callbacks remotos.

### InsultFilter
- El servidor expone métodos remotos para encolar textos y registrar resultados filtrados.
- Productores encolan textos remotamente.
- Workers obtienen textos, los filtran localmente y mandan el resultado filtrado al servidor.
- **La lógica de filtrado reside en los workers** y la comunicación se gestiona mediante objetos PyRO (RPC).


## Redis

### InsultService
- El InsultProducer publica insultos en un canal (`INSULTS_input`).
- El observable (servidor) los escucha, los almacena (evitando duplicados en un SET/LIST) y publica insultos a otro canal (`INSULTS_broadcast`) cada 5 segundos.
- Los observadores se suscriben y reciben insultos en tiempo real.
- **Arquitectura basada en Pub/Sub y colecciones SET/LIST de Redis.**

### InsultFilter
- Productores hacen `RPUSH` a una lista (cola de trabajo, `work_queue`).
- Workers hacen `BLPOP` para consumir textos, los filtran y almacenan el resultado en otra lista (`RESULTS`).
- Los clientes pueden consultar la lista de resultados mediante `LRANGE`.
- **Arquitectura de cola compartida y procesamiento distribuido** (Work Queue Pattern).


## RabbitMQ

### InsultService
- El InsultProducer publica insultos en una cola.
- Los consumers se suscriben y reciben insultos (**modelo point-to-point**).
- Para difusión se usa un **exchange fanout**: los mensajes se replican a todas las colas de los subscriptores (**publish/subscribe real**).
- RabbitMQ se encarga del enrutado y almacenamiento temporal.

### InsultFilter
- Productores envían textos a la cola `text_queue`.
- Workers consumen de esa cola, filtran, y mandan el resultado a la cola `result_queue`.
- ResultCollector recoge los resultados para su consulta.
- **Arquitectura de Work Queue y Result Queue, ideal para procesamiento paralelo real.**

