# Proyecto Final Sistemas Embebidos SCANIO
![alt text](https://github.com/diegoavellanedat17/embedded-systems-3/blob/master/portadaFinal.JPG)

A continuación se explica el proyecto a grandes rasgos y en las posteriores secciones se entrará más en detalle. El objetivo del sistema es consolidar los datos del escaneo de dispositivos BLE que se encuentran haciendo "advertising" (anunciando su presencia) en el área de cobertura de nuestro dispositivo central. El funcionamiento es el siguiente:

La RPi Zero: Se encuentra conectada a través del puerto serial a un ESP32 el cual esta escaneando dispositivos BLE en una ventana de tiempo de 5 segundos. Este envía una trama en formato JSON de los dispositivos escaneados junto con el RSSI asociado. La RPI Zero tiene 2 servicios, el primero es el encargado de recibir los datos a través del serial y generar archivos en una carpeta. El segundo servicio valida que tenga una conexión con la segunda Raspberry Pi, si puede conectarse a través de ssh y tiene archivos por enviar, los encripta y luego los envía a través de SCP.

La segunda Raspberry tiene un servicio que identifica si tiene archivos nuevos, en caso de que existan, primero desencripta la llave simetrica con la llave publica asimetrica y posteriormente con la llave simetrica decifrada, desencripta el archivo y hace append a un archivo llamado ble_data.txt

## VIDEO DEL PROYECTO

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/tXbs2OFO7R8/0.jpg)](https://www.youtube.com/watch?v=tXbs2OFO7R8)




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

## Escaneo y Envío por Serial

El probrama que se carga en el ESP32 se encuentra en la carpeta BLE Scanner (usando un ESP32 Wrover debe cargarse con el FTDI).

La conexión serial entre el ESP32 y la Raspberry Pi Zero debe ser como se muestra en la siguiente imagen. 

![alt text](https://github.com/diegoavellanedat17/embedded-systems-3/blob/master/circuito.JPG)

## Servicio de BLE_scanner

Este corresponde al servicio que corre en la Raspberry Pi Zero y ejecuta el script de python llamado scanner.py, debe activarse a través del siguiente comando 

```
sudo systemctl start BLE.service
```

## Servicio de Envío de información

Este corresponde al servicio que corre en la Raspberry Pi Zero y ejecuta el script de BASH llamdo filesTransferir.sh que toma los archivos de la carpeta, encripta y envía

```
sudo systemctl start scanner.service
```
## Servicio de desencripción de datos

Este corresponde al servicio que corre en la Raspberry Pi 3 y ejecuta el script de BASH llamado decrypt_check.sh que toma los archivos encriptados, y hace append en el archivo ble_data.txt

```
sudo systemctl start scanner.service
```

## Transferencia de archivos
Para la transferencia de archivos se haace a través del envío usando el comando scp entre los dos sistemas, para esto es necesario habilitar las claves y permitir la transferencia sin necesidad de la autenticación, esto se hace a través de los siguientes comandos. 

En la maquina de origen:
```
ssh-keygen -t rsa
```
En la maquina de destino:
```
ssh-copy-id user@remote_machine
```
Para comprimir el directorio que se enviará se realiza por medio de:
```
tar -zcvf nombre-archivo-resultante.tar.gz nombre-directorio-o-archivo
```

Para descomprimir en la maquina receptora por medio de:
```
tar -xvzf archivo-comprimido.tar.gz
```
## Encriptación de archivos para la tranferencia

En el sistema de destino se generan las llaves publica y privada. 

```
openssl genrsa -out private.pem 512
$openssl rsa -in private.pem -out public.pem -outform PEM -pubout

```
Luego se copia la llave pública en el transmisor para la encriptación de la llave simetrica. 


