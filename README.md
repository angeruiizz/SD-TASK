# Middleware services

## XMLRPC
En el caso del XMLRCP, permite que un cliente llame a la función de un servidor de forma remota usando XML para codificar mensajes y HTTP como protocolo de transporte.
El servidor, al recibir la solicitud XML, la procesa y ejecuta el método solicitado. El servidor tiene que estar preparado para recibir y entender los mensajes XML y ejecutar las funciones que el cliente le pida.
Una vez que el servidor ha procesado la solicitud, genera una respuesta en formato XML, que incluye el resultado de la ejecución del método.  El cliente recibe la respuesta del servidor, procesa la información y continúa con su ejecución.

### InsultServer

### InsultFilter


## PyRO

### InsultServer

### InsultFilter

## REDIS

### InsultServer

### InsultFilter

## RabbitMQ
En el caso de RabbitMQ, se tarta de un servicio de comunicación indirecta. Se basa en el modelo publisher-subscriber, donde los productores envían mensajes a un intercambio (exchange) y los consumidores se suscriben a colas (queues) que reciben esos mensajes. RabbitMQ se encarga de enrutar los mensajes desde el productor hasta el consumidor adecuado, permitiendo una comunicación asíncrona y desacoplada entre ellos.
RabbitMQ utiliza el protocolo AMQP (Advanced Message Queuing Protocol) para la comunicación entre productores y consumidores. Los mensajes se envían a través de un intercambio, que actúa como un intermediario entre los productores y las colas. Los consumidores se suscriben a las colas y reciben los mensajes que se envían a esas colas.

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
El Insult Filtter sigue la estructura de WorkQueue, donde el productor envía mensajes a una cola y los consumidores se suscriben a esa cola para recibir los mensajes. En este caso, el insultFilter actúa como un consumidor de mensajes que recibe insultos del servidor y los procesa.
Código del InsultFilter:
- insultConsumer.py: Cuando el cliente recibe una frase lo decodifica y lo limpia.
- insultProducer.py: Se encarga de enviar frases con y sin insultos a la cola de RabbitMQ

**Para ejecutar simplemente ejecutar en la terminal el siguiente comando dentro de la ruta del insultServer (RabbitMQ/InsultFiltter)**
```bash
 python .\execInsultFilter.py
```