# Middleware services

## XMLRPC
XMLRPC proporciona un modelo de comunicación directa y síncrona. El cliente invoca métodos remotos directamente en el servidor a través de solicitudes HTTP, recibiendo la respuesta en la misma conexión.
No existe un componente intermedio ni almacenamiento de mensajes: cada llamada implica una interacción directa entre cliente y servidor, que deben estar activos al mismo tiempo.
Esta arquitectura es adecuada para escenarios request-response, pero no permite comunicación asíncrona ni desacoplada entre procesos.

### InsultServer
El servidor no tiene que estar preparado para recibir mensajes de los clientes, sino que simplemente responde a las solicitudes de los clientes. En este caso, XMLRCP esta escuchando de forma continua en el puerto 9000 y el cliente se conecta a ese puerto para enviar solicitudes al servidor. El servidor procesa la solicitud y devuelve una respuesta al cliente.

Este middleware no soporta publicación/subscripción. Solo permite invocaciones a métodos remotos desde el cliente hacia el servidor. Para somular un broadcast, los clientes (osea suscriptores) preguntan periodicamnete al servidor por nuevo insulto, osea lo que se conoce como 'polling'. En este caso, el servidor no envía mensajes a los clientes, sino que estos tienen que preguntar al servidor si hay nuevos insultos disponibles. El servidor responde con un insulto aleatorio cada vez que un cliente lo solicita. Esto permite que varios clientes obtengan insultos del servidor, pero no es una verdadera comunicación de publicación/suscripción.

Por tanto tenemos:
- Producer: Se encraga de generar los insultos y enviarlos al servidor. En este caso, el productor es el cliente del servidor. Cada 5 segundos ejecuta el metodo getInsult del servidor, que escoje un insulto aleatorio y se lo manda al consumidor.
- Consumer: Esta iniciado el servidor y espera a que el cliente le envíe una solicitud. Cuando el cliente le envía una solicitud, el servidor ejecuta el método getInsult y devuelve un insulto aleatorio al cliente. O ejecuta el metodo broadcastInsult, que devuelve un insulto aleatorio a todos los clientes que lo han solicitado (simulando la difusion de un broadcast y suscriptores).
- Receiver: Es el suscriptor que recibe el insulto del servidor. En este caso, el cliente se conecta al servidor y le envía una solicitud para obtener un insulto cada segundo. El servidor, que ejecuta la función broadcast, escoge un insulto aleatorio de la lista y lo devuelve. 

En la salida del servidor se puede ver el insulto que ha devuelto al cliente. Además podemos observar las peticiones que ha recibido el servidor con el timestamp: _127.0.0.1 - - [timestamp] "POST / HTTP/1.1" 200_

**Para ejecutar todo el servicio, se puede utilizar el siguiente comando en la terminal dentro de la ruta del InsultServer (XMLRPC/InsultServer):**

```bash
python .\execInsultServer.py
```


### InsultFilter
Este servicio se encarga de recibir textos desde clientes XML-RPC y comprobar si contienen insultos. Si detecta insultos, los sustituye por la palabra "CENSORED" y almacena tanto el texto original como el filtrado. El filtro es una lógica simple de Work Queue, donde los productores envían textos y el servidor los procesa uno a uno.

En InsultFilter, el sistema implementa un work queue pattern centralizado en el servidor XMLRPC:

1. El servidor (insultConsumer.py) mantiene una cola de textos pendientes y una lista de resultados filtrados.
2. Productores (insultProducer.py, textProducer.py) envían textos usando el método enqueue_text.
3. Workers (uno o varios) solicitan trabajo con get_next_text, filtran el texto localmente, y devuelven el resultado al servidor usando submit_result.

El servidor guarda los resultados y los puede devolver con get_results.

Scripts:

- insultProducer.py y textProducer.py: Productores que encolan frases en el servidor.
- worker.py: Procesa textos pendientes, los filtra, y devuelve los resultados filtrados.
- insultConsumer.py (servidor): Gestiona la cola y la lista de resultados.

**Para ejecutar todo el servicio, se puede utilizar el siguiente comando en la terminal dentro de la ruta del InsultServer (XMLRPC/InsultFilter):**

```bash 
python .\execInsultFilter.py
```

## PyRO
Redis, en modo pub/sub, permite una comunicación indirecta y asíncrona entre productores y consumidores, actuando como intermediario.
Los productores publican mensajes en canales y los consumidores suscritos a esos canales los reciben en tiempo real. Además, mediante listas (work queues), Redis permite almacenar mensajes para ser procesados posteriormente por los consumidores, desacoplando la producción y el consumo de información.
Esta comunicación asíncrona es adecuada para arquitecturas donde los procesos pueden no estar disponibles simultáneamente, y se necesita un intermediario que almacene temporalmente los mensajes.



### InsultServer
El servidor central actúa como difusor de insultos. Mantiene una lista de suscriptores (clientes que han registrado su objeto remoto) y, cada 5 segundos, invoca el método receive_insult(insult) en cada uno de ellos, enviando un insulto aleatorio de forma proactiva.
Este comportamiento implementa un verdadero modelo de publicación/suscripción (patrón Observer), ya que:
Los clientes no necesitan consultar periódicamente si hay nuevos insultos (polling).
El servidor envía automáticamente los mensajes a todos los clientes suscritos.

Roles:

- Producer: Genera insultos aleatorios y los difunde a los suscriptores registrados. En este caso, el productor está integrado en el propio servidor.
- Consumer / Receiver: Son los clientes que se han registrado como observadores. Implementan el método receive_insult, que recibe y muestra los insultos enviados por el servidor.

### InsultFilter
PyRO también implementa el patrón work queue, pero usando objetos distribuidos remotos:

- El servidor (server.py) expone métodos para encolar textos, obtener textos para procesar y guardar resultados.
- Productores (angryProducer.py, textProducer.py) usan enqueue_text.
- Workers (worker.py) llaman a get_next_text, filtran y luego usan submit_result.

Scripts:

- angryProducer.py, textProducer.py: Productores de frases.
- worker.py: Worker de filtrado.
- server.py: Mantiene cola y resultados.



## REDIS
Redis (REmote DIctionary Server) es una base de datos en memoria de estructura clave-valor, extremadamente rápida y ligera. Aunque originalmente fue diseñada como sistema de almacenamiento, también permite implementar sistemas de comunicación entre procesos mediante su mecanismo de publicación y suscripción (pub/sub).

Redis no utiliza un protocolo de mensajería estándar como AMQP (usado en RabbitMQ), sino su propio sistema de canales. Los mensajes publicados en un canal se entregan en tiempo real a todos los clientes que estén suscritos en ese momento. Sin embargo, estos mensajes no se almacenan: si no hay suscriptores conectados cuando se publica un mensaje, este se pierde.

Además de pub/sub, Redis proporciona estructuras como SET y LIST que permiten almacenar datos persistentes de manera eficiente y evitar duplicados o mantener el orden de inserción, respectivamente.

Sistema de comunicación en Redis
Pub/Sub: los productores publican mensajes en un canal, y los consumidores que estén suscritos a ese canal los reciben automáticamente.

SET: almacena elementos sin duplicados.
LIST: mantiene el orden de inserción, permitiendo acceder a los elementos por índice.

En este caso, Redis tiene comunicación indirecta, ya que los productores y consumidores no se comunican directamente entre sí. En su lugar, utilizan Redis como intermediario para enviar y recibir mensajes, a traves de canales pub/sub, listas y colas compartidas.


### InsultServer
Este proyecto implementa un servicio de difusión de insultos utilizando Redis como sistema de comunicación. Está compuesto por varios módulos que colaboran de forma asíncrona:

Componentes
InsultProducer -> Genera un insulto aleatorio cada 5 segundos y lo publica en el canal INSULTS_input.

InsultService/observable -> Escucha el canal INSULTS_input:
- Si el insulto es nuevo (no duplicado), lo guarda en un SET y lo añade a una LIST para mantener el orden.
- Cada 5 segundos, selecciona un insulto aleatorio de la lista y lo publica en el canal INSULTS_broadcast.

InsultObserver -> Se suscribe al canal INSULTS_broadcast y muestra los insultos recibidos.

### InsultFilter
En Redis, la arquitectura work queue se basa en listas Redis:

- Productores (angryProducer.py, textProducer.py) hacen rpush en la cola work_queue.
- Workers (insultConsumer.py) hacen blpop para sacar y filtrar textos, guardando resultados en RESULTS.
- Cualquier cliente puede consultar los resultados con lrange("RESULTS", 0, -1).

Roles:

- Productores: Envían frases a la cola.
- Worker: Procesa y filtra en paralelo.
- Cliente de resultados: Consulta la lista RESULTS.

## RabbitMQ
RabbitMQ implementa un modelo de comunicación indirecta mediante colas de mensajes. Productores y consumidores nunca se comunican directamente entre sí, sino que intercambian mensajes a través de un broker central (RabbitMQ), que se encarga de almacenar y enrutar los mensajes de manera eficiente y fiable.
Esto permite una comunicación asíncrona y completamente desacoplada: los productores pueden enviar mensajes aunque no haya consumidores conectados en ese momento, y los consumidores pueden procesar los mensajes cuando estén disponibles.

### InsultServer
En este caso, al ser RabbitMQ un servicio de mensajería, el servidor InsultServer actúa como un productor de mensajes. En lugar de enviar respuestas directamente al cliente, el servidor envía mensajes a una cola de RabbitMQ. El cliente se suscribe a esa cola y recibe los mensajes que el servidor envía. Esto permite una comunicación asíncrona y desacoplada entre el servidor y el cliente.
Por tanto tenemos:
- El insultProducer -> cada 5 seg genera un insulto aleatorio y lo envía a la cola de RabbitMQ. Tipo de comunicación es point-to-point.
- El insultConsumer -> se suscribe a la cola de RabbitMQ y recibe los insultos que el productor envía. Tipo de comunicación es point-to-point.Podemos hacer load balancing entre varios consumidores, ya que cada uno de ellos se suscribe a la misma cola y RabbitMQ se encarga de distribuir los mensajes entre ellos. 
- El insultBroadcast -> Cada 5 seg, coje un insulto y lo publica para que cualquiera que este suscrito lo reciba. Tipo de comunicación es publish-subscribe.
- El insultSubscriber -> se suscribe a un fannout exchange de RabbitMQ y recibe los mensajes que se publican en ese exchange. Tipo de comunicación es publish-subscribe.

*El exchange se encarga de enrutar los mensajes a las colas adecuadas. Puede ser: direct, topic o fanout. En este caso, se utiliza un exchange de tipo fanout, que envía los mensajes a todas las colas suscritas a él. Direcrt: envía los mensajes a una cola específica. Topic: envía los mensajes a las colas que coinciden con un patrón de enrutamiento.

tutorial publicación y suscripción: https://www.rabbitmq.com/tutorials/tutorial-three-python

tutorial colas: https://www.rabbitmq.com/tutorials/tutorial-two-python

![alt text](imagenes-README/publishsubsRABBITMQ.png "RabbitMQ publish-subscribe")

**Para ejecutar simplemente ejecutar en la terminal el siguiente comando dentro de la ruta del insultServer (RabbitMQ/InsultServer)**
```bash
 python .\execInsultServer.py
```

### InsultFilter
Aquí el flujo implementa un work queue real y result queue:

- Productores (textProducer.py, angryProducer.py) envían mensajes a la cola text_queue.
- Workers (worker.py) consumen de text_queue, filtran insultos, y publican el resultado en result_queue.
- ResultCollector (resultCollector.py): consume de result_queue y almacena los textos filtrados para consulta centralizada.

Scripts:

- textAngryProducer.py: Productor de textos, en eeste caso manda tanto frases con insultos como sin insultos.
- worker.py: Filtra textos y los manda a la cola de resultados.
- resultCollector.py: Recoge y guarda todos los textos filtrados.

**Para ejecutar simplemente ejecutar en la terminal el siguiente comando dentro de la ruta del insultServer (RabbitMQ/InsultFiltter)**
```bash
 python .\execInsultFilter.py
```

# Como ejecutar los ejemplos
Para ejecutar los ejemplos, es necesario tener instalado Python 3.8 o superior y las librerías necesarias.
Una vez puesto en el directorio de cada ejemplo, se puede ejecutar el siguiente comando en la terminal:
```bash
python ./execInsultServer.py
```
```bash
python ./execInsultFilter.py
```
*Importante, sobretodo hay que estar en el directorio de cada ejercicio. Por ejemplo, si quisieramos ver el insult fitter de RabbitMQ, tendiramos que estar en la carpeta RabbitMQ/InsultFilter y ejecutar el comando anterior* 

