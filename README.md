# Middleware services

## XMLRPC
En el caso del XMLRCP, permite que un cliente llame a la función de un servidor de forma remota usando XML para codificar mensajes y HTTP como protocolo de transporte.
El servidor, al recibir la solicitud XML, la procesa y ejecuta el método solicitado. El servidor tiene que estar preparado para recibir y entender los mensajes XML y ejecutar las funciones que el cliente le pida.
Una vez que el servidor ha procesado la solicitud, genera una respuesta en formato XML, que incluye el resultado de la ejecución del método.  El cliente recibe la respuesta del servidor, procesa la información y continúa con su ejecución.


## PyRO

## REDIS

## RabbitMQ


# InsultServer
Esta primera parte tarta de implementar un Servidor de insultos. Este puede recibir insultos de forma remota y guardarlos en una lista si son nuevos. El servicio ofrece kmecanismos para tratar con lña lista de los insultos. Un broadcaster peridoicamente publica insultos random para los susbcriptores que estan en el canal cada 5 seg. 

Básicamente la arquitectura principal independientemente del middleware utilizado (según la imoplementación, ver mas adelante):
- InsultServer.py -> Con este script se pueden ejecutar los 4 scripts.
- Consumer.py -> Este script simula el servidor, estan definidos los metodos para getsionar los insutlos
- Producer.py -> Este script simula el cliente, que manda insultos de forma aleatoria al servidor
- broadcaster.py -> Este script recoje los insultos y los publica en un canal 
- Receiver.py -> Cliente conectado en el canal que recibe los insultos.

## Implementación XMLRPC
En este caso para el broadcaster no 'se publican en un canal' sino que obtiene los insultos y los hace disponibles para los clientes, como flujo de información. 
El receiver lo que hace es solicitar los insultos de forma periodica al broadcaster.

# InsultFiltter

////todo

## Implemenatcion XMLRPC
En este caso tenemos dos productores, uno que manda texto sin insultos y otro que manda texto con insultos. 
Entonces, estos se conectan al mismo servidor, que es el consumidor, y según si la frase lleva alguna palabara que esta etiquetada con insultos, los cambia por CENSORED, y los guarda en la lista de frases limpias, i si no tiene insultos simplemente los guarda en la lista. 
 