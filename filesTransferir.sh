#!/bin/bash
#Este script debe contar la cantidad de archivos que hay en una carpeta
#Cuando la carpeta tiene los 10 archivos la envía al segundo sistema
CANTIDAD=$(ls /home/diego/Documents/folderTest | wc -l)


if [ $CANTIDAD = 10 ];
then
#La idea de aca es comprimir, encriptar y enviar el archivo
tar -czvf ../data.tar.gz ../folderTest
echo 'Enviar por ssh al otro equipo'
scp ../data.tar.gz pi@192.168.20.45:/home/pi/Documents
else
#La idea aca es seguir en el while
echo 'Aun no es tiempo de enviar'
fi