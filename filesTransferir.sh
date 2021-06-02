#!/bin/bash
#Este script debe contar la cantidad de archivos que hay en una carpeta
#Cuando la carpeta tiene los 10 archivos la envía al segundo sistema


while :
do

      #Lo primero en este script es verificar si se encuentra el host activo 
      ssh -q pi@192.168.20.45 exit
      HOST=$(echo $?)
      echo $HOST
      #La variable host toma el valor de 0 si esta activo o de 255 si esta inactivo 
      if [[ "$HOST" -eq  0 ]];
      then
            echo "host conectado"
            # Verificar si existe algun archivo con prefijo data

            ARCHIVO=$(echo $(ls -t ../dataFolder/data* | head -1))
            # solo tomamos el ultimo archivo

            #si la variable tiene algo se guarda, si no queda vacia

            if [ -z "$ARCHIVO" ]
            then
            #Si hay archivos, se toma el archivo y se prepara para la transferencia 
                  echo "No hay archivos"
            else
                  echo "Si hay archivos"
                  echo $ARCHIVO
                  #Encriptamos el archivo con la llave simetrica
                  openssl enc -aes-256-cbc -salt -in $ARCHIVO -out ../dataFolder/sendingData.enc -pass file:../aesKey.txt
                  #Transferir los archivos
                  scp ../dataFolder/sendingData.enc pi@192.168.20.45:/home/pi/Documents/proyecto-final
                  #Transferir la llave
                  scp ../aesKey.txt.crypted pi@192.168.20.45:/home/pi/Documents/proyecto-final
                  rm $ARCHIVO
                  rm -f ../dataFolder/sendingData.enc
            fi
      else
            echo "host desconectado"
      fi

      sleep 10
done

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
