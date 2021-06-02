#!/bin/bash

#El script esta todo el tiempo revisando, si aparece alguno, lo desencripta y a lo que haya adentro de hace append a otro file
FILE=../sendingData.enc
if [ -f "$FILE" ]; then
    echo "$FILE exists."
else 
    echo "$FILE does not exist."
fi

