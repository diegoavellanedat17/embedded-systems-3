
from time import sleep
import serial
import time
import threading
import queue
import json
from datetime import datetime
import os


#Tener un hilo para que cada que reciba un dato serial imprima en pantalla

ser = serial.Serial ("/dev/ttyS0", 115200)    #Open port with baud rate

qBLE_Data=queue.Queue()
global count
def serial_worker():
    count=0
    while True:
        
        item=qBLE_Data.get()
        print("entra en item")
        print(item)
        file_object = open('../dataFolder/temp.txt', 'a')
        file_object.write(str(item))
        file_object.write("\n")
        file_object.close()
        qBLE_Data.task_done()
        print(count)
        count=count+1 
        if count>10:
            count=0
            now = datetime.now()
            now=str(now)
            filename=now+".txt"
            os.rename('../dataFolder/temp.txt', filename) 
            

            
    # Aqui se hará append al archivo

threading.Thread(target=serial_worker, daemon=True).start()

while True:
    received_data = ser.read()              #read serial port
    sleep(0.03)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)	
    received_data=received_data.decode('utf8')

    #print(received_data)
    try:
        json_data_incoming=json.loads(received_data)
        json_size=len(json_data_incoming['devices'])
        now = datetime.now()
        now=str(now)
        tiempo={"time":now}
        #print(json_data_incoming)
        json_data_incoming.update(tiempo)
        #print(json_data_incoming)
        qBLE_Data.put(json_data_incoming)
    except:
        print("entra en la excepcion")
        

    	


