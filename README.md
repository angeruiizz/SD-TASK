# Middleware services

## XMLRPC
En el caso del XMLRCP, permite que un cliente llame a la función de un servidor de forma remota usando XML para codificar mensajes y HTTP como protocolo de transporte.
El servidor, al recibir la solicitud XML, la procesa y ejecuta el método solicitado. El servidor tiene que estar preparado para recibir y entender los mensajes XML y ejecutar las funciones que el cliente le pida.
Una vez que el servidor ha procesado la solicitud, genera una respuesta en formato XML, que incluye el resultado de la ejecución del método.  El cliente recibe la respuesta del servidor, procesa la información y continúa con su ejecución.


## PyRO

## REDIS

## RabbitMQ


# InsultServer
Esta primera parte tarta de implementar un Servidor de insultos. Este puede recibir insultos de forma remota y guardarlos en una lista si son nuevos. El servicio ofrece kmecanismos para tratar con lña lista de los insultos.

Básicamente la arquitectura principal independientemente del middleware utilizado (según la imoplementación, ver mas adelante):
- execInsultServer.py -> Con este script se pueden ejecutar los 3 scripts.
- observable.py -> Este script simula el servidor, estan definidos los metodos para getsionar los insutlos
- Producer.py -> Este script simula el cliente, que manda insultos de forma aleatoria al servidor
- observer.py -> Cliente conectado en el canal que recibe los insultos.

## Implementación XMLRPC
En este caso para el broadcaster no 'se publican en un canal' sino que obtiene los insultos y los hace disponibles para los clientes, como flujo de información. 
Cuando devuelve:
127.0.0.1 - - [16/Apr/2025 21:54:32] "POST / HTTP/1.1" 200 -
127.0.0.1 - - [16/Apr/2025 21:54:33] "POST / HTTP/1.1" 200 -
Significa que el servidor recibio la petición post desde la ip 127.0.0.1 y que la petición fue correcta (200). (POST es el método de la petición, y HTTP/1.1 es la versión del protocolo HTTP que se está utilizando).

## Implementación PyRO
En este caso, el servidor de insultos se convierte en un objeto remoto que puede ser accedido por los clientes a través de Pyro. El cliente se conecta al servidor Pyro y llama a los métodos del objeto remoto como si fueran métodos locales. Pyro maneja la comunicación entre el cliente y el servidor, permitiendo que los clientes interactúen con el servidor de insultos de manera transparente.

## Implementación Redis
En este caso, el servidor de insultos se convierte en un productor que publica mensajes en un canal de Redis. Los clientes se suscriben a ese canal y reciben los mensajes publicados por el servidor. Redis maneja la comunicación entre el productor y los consumidores, permitiendo que los clientes reciban los insultos en tiempo real.

## Implementación RabbitMQ



# InsultFiltter

////todo

## Implemenatcion XMLRPC
En este caso tenemos dos productores, uno que manda texto sin insultos y otro que manda texto con insultos. 
Entonces, estos se conectan al mismo servidor, que es el consumidor, y según si la frase lleva alguna palabara que esta etiquetada con insultos, los cambia por CENSORED, y los guarda en la lista de frases limpias, i si no tiene insultos simplemente los guarda en la lista. 
 
