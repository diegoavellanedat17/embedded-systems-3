# Proyecto Final Sistemas Embebidos 

> En el siguiente diagrama de se representan los elementos para el proyecto final. Los tags el RSSI del enlace y el hardware que los escanea se tomará como un bloque y se simularán
las tramas, estas se envian de manera serial al la RPI. Una vez recibidas las tramas en se ingresan en en una cola para ejecutar en procesos independientes. Allí se realiza el procesamiento 
que es acondicionar el formato de la trama. Dependiendo de los cambios en la trama se realiza una publicación como cliente MQTT desde el mismo RPI. Las tramas se envian para que se escriban
en un archivo de texto de otra RPI donde se pordran ver los archivos. Estos se ejecutan es systemd como servicios.

![alt text](https://github.com/diegoavellanedat17/embedded-systems-3/blob/master/diagram.JPG)

![alt text](https://github.com/diegoavellanedat17/embedded-systems-3/blob/master/diagram2.JPG)


Los siguientes corresponden a las herramientas a usar para implementar la funcionalidad vista en los diagramas:

- **Comunicación serial**: Para recibir las tramas de los dispositivos de escaneo. 
- **Multihilos**: Con las Tramas que se reciben de manera serial.
- **MQTT**: Para conectarse a un broker y publicar información.
- **Keygen**: Para conectarse sin contraseña al otro dispositivo.
- **SCP**: Para transferir información a un archivo en otro dispositivo.
- **Bash**: Para ejecutar el archivo que escribe en la otra máquina.
- **Systemd**: Para ejecutar los servicios en segundo plano.

