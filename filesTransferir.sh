#!/bin/bash
#Este script debe contar la cantidad de archivos que hay en una carpeta
#Cuando la carpeta tiene los 10 archivos la envía al segundo sistema

#Guardar cualquier archivo que tenga el prefijo data
# Verificar si existe algun archivo llamado asi
FILE=../dataFolder/data*
if [ -f "$FILE" ]; then
    echo "$FILE exists."
else 
    echo "$FILE does not exist."
fi

# if [ $CANTIDAD = 10 ];
# then
# #La idea de aca es comprimir, encriptar y enviar el archivo
# #tar -czvf ../data.tar.gz ../folderTest

# #encriptar con la llave simetrica 
# openssl enc -aes-256-cbc -salt -in ../data.tar.gz -out ../data.enc -pass file:../aesKey.txt
# echo 'Enviar por ssh al otro equipo'
# #Enviar al otro equipo
# #scp ../data.tar.gz pi@192.168.20.45:/home/pi/Documents
# scp ../data.enc pi@192.168.20.45:/home/pi/Documents/proyecto-final
# scp ../aesKey.txt.crypted pi@192.168.20.45:/home/pi/Documents/proyecto-final

# #remover el archivo 
# rm ../data.tar.gz
# rm ../data.enc


# else
# #La idea aca es seguir en el while
# echo 'Aun no es tiempo de enviar'
# fi