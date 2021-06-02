import paho.mqtt.client as mqtt
from time import sleep
import serial
import time
import threading
import queue
import json
from datetime import datetime
import os
import config

#funcion al conectarse al broker

def on_connect(client, userdata, flags, rc):
    print("Connected with result code" + str(rc))
#funcion al publicar
def on_publish(client, obj, mid):
    print("mid: " + str(mid))

#Tener un hilo para que cada que reciba un dato serial imprima en pantalla

mqttc = mqtt.Client(config.client_device)
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
found=False
flag=False

try:
    mqttc.username_pw_set(config.user, config.password)
    mqttc.connect(config.broker_address, config.port)
    mqttc.loop_start()
except Exception as e:
    file_object = open('../dataFolder/MQTT_problem.txt', 'a')
    file_object.write(str(e))
    file_object.write("\n")
    file_object.close()

try:
    ser = serial.Serial ("/dev/ttyS0", 115200)    #Open port with baud rate
except Exception as e:
    file_object = open('../dataFolder/SerialProblem.txt', 'a')
    file_object.write(str(e))
    file_object.write("\n")
    file_object.close()


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
            now=now.strftime("%Y-%m-%d%H:%M:%S")
            now=str(now)
            path="../dataFolder/"
            filename=path+'data'+now+".txt"
            os.rename('../dataFolder/temp.txt', filename) 
            

            
    # Aqui se hará append al archivo

threading.Thread(target=serial_worker, daemon=True).start()

while True:
    received_data = ser.read()              #read serial port
    sleep(0.03)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)	
    received_data=received_data.decode('utf8')

    if found and not flag:
        mqttc.publish(config.topic,"L1ON")
        flag=True
    elif not found and flag:
        mqttc.publish(config.topic,"L1OFF")
        flag=False
    else:
        pass
    
    try:
        json_data_incoming=json.loads(received_data)
        json_size=len(json_data_incoming['devices'])
        now = datetime.now()
        #sin espacio para generar archivo
        now=now.strftime("%Y-%m-%d %H:%M:%S")
        now=str(now)
        tiempo={"time":now}
        #print(json_data_incoming)
        json_data_incoming.update(tiempo)
        #print(json_data_incoming)
        qBLE_Data.put(json_data_incoming)
        try:
            found=False
            for i in range(json_size):
                name_to_save=json_data_incoming['devices'][i]['name']
                print(name_to_save)
                if name_to_save=="DiegoPhone":
                    found=True
        except:
            nombre= 'No devices'
    except Exception as e:
        print(e)
        print("entra en la excepcion")
        

    	


