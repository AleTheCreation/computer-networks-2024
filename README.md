# Descripción de la Implementación del Protocolo IRC

La implementación propuesta del protocolo IRC (Internet Relay Chat) consiste en dos partes: un cliente y un servidor.

## Cliente IRC:

- El cliente IRC es una aplicación de escritorio desarrollada en Python utilizando la biblioteca Tkinter para la interfaz gráfica.
- Permite a los usuarios conectarse a un servidor IRC proporcionando su apodo (nickname), el servidor al que desean conectarse, y el puerto (opcionalmente el modo SSL también puede ser habilitado).
- Una vez conectado, el cliente puede enviar y recibir mensajes en los canales de chat.
- Ofrece funcionalidades básicas como enviar mensajes, unirse y abandonar canales, y desconectarse del servidor.
- Implementa manejo de excepciones para gestionar errores de conexión, resolución DNS, y envío y recepción de mensajes.

## Servidor IRC:

- El servidor IRC es un programa que escucha conexiones entrantes en un puerto específico y gestiona la comunicación entre los clientes conectados.
- Cada cliente que se conecta al servidor se identifica mediante un apodo (nickname).
- El servidor gestiona múltiples clientes simultáneamente, asignando a cada uno un hilo de ejecución para manejar su comunicación.
- Permite a los clientes unirse a canales de chat, enviar y recibir mensajes dentro de esos canales, enviar mensajes privados entre usuarios, y desconectarse del servidor.
- Implementa un sistema básico de canales donde los usuarios pueden unirse y dejar canales, y el servidor envía mensajes a todos los miembros de un canal específico.
- Se ha agregado la capacidad de manejar excepciones para garantizar una ejecución robusta del servidor, capturando errores en la comunicación con los clientes y gestionando adecuadamente la terminación de los hilos de ejecución.

En resumen, la implementación proporciona una base funcional para un sistema de chat IRC, con un cliente que ofrece una interfaz gráfica simple para la interacción del usuario y un servidor que gestiona la comunicación entre múltiples clientes conectados simultáneamente.
