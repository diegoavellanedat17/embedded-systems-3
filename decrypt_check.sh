#!/bin/bash

#El script esta todo el tiempo revisando, si aparece alguno, lo desencripta y a lo que haya adentro de hace append a otro file
FILE=../sendingData.enc

while :
do
    if [ -f "$FILE" ]; then
        echo "$FILE exists."
        #Cuando el archivo existe se desecncripta
        openssl enc -d -aes-256-cbc -in file.enc -out file.txt.decrypted -pass file:../aesKey.txt.decrypted
        #tomo el archivo desencriptado y lo agrego a data
        echo $(cat ../file.txt.decrypted) >> ../ble_data.txt
        #Borrar los que ya no se necesiten
        rm -f ../sendingData.enc
        rm -f ../file.txt.decrypted

    else 
        echo "$FILE does not exist."
    fi
    sleep 5
done