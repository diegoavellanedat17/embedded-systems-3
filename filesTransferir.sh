#!/bin/bash
#Este script debe contar la cantidad de archivos que hay en una carpeta
#Cuando la carpeta tiene los 10 archivos la envía al segundo sistema
CANTIDAD=$(ls /home/pi/Documents/filesTrans | wc -l)




if [ $CANTIDAD = 10 ];
then
#La idea de aca es comprimir, encriptar y enviar el archivo
tar -czvf filesTrans.tar.gz /home/pi/Documents/filesTrans 
echo 'Enviar por ssh al otro equipo'
else
#La idea aca es seguir en el while
echo 'Aun no es tiempo de enviar'
fi