import random
import time
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
import paho.mqtt.client as mqtt
import re
import json

def on_connect(client, userdata, flags, rc):
    # This will be called once the client connects
    print(f"Connected with result code {rc}")
    # Subscribe here!
    client.subscribe("station1")
    client.subscribe("station2")
    client.subscribe("station3")
    client.subscribe("station4")
    client.subscribe("station5")

def on_message(client, userdata, msg):
    global rssi_vector
    payload = msg.payload.decode("utf-8")
    #print(f'Topic {msg.topic} ---> Payload {msg.payload}')
    #payload = payload.replace("\\", "")
    try:
        payload = json.loads(payload)
        topic = msg.topic
        now = datetime.now()
        station_number = re.findall(r'[0-9]|$', topic)[0]
        tags_tupple = get_tags(payload)
        for tag_info in tags_tupple:
            if rssi_vector[tag_info[0]-1][int(station_number)-1] != 0:
                print('dato repetido')
            else:
                rssi_vector[tag_info[0]-1][int(station_number)-1] = tag_info[1]
                complete_count = 0
                for i in range(0, 3):
                    if not is_zero(rssi_vector[i]):
                        complete_count = complete_count + 1
                if complete_count == 3:
                    print('complete vector')
                    print(rssi_vector, time_map(datetime.now()))
                    for i in range(0, 3):
                        save_data(f'TAG{i+1}.txt', f'{rssi_vector[i]},{time_map(datetime.now())}')
                    rssi_vector = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    except:
        print('algo raro')


def save_data(filename,line):
    f = open(f"{filename}", "a")
    f.write(f"\n{line}")
    f.close()


def time_map(now):
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

def is_zero(vector):
    zero = False
    for item in vector:
        if item == 0:
            return True
    return zero

def get_tags(payload):
    tags_list = []
    devices = payload['devices']
    for tag in devices:
        tag_number = re.findall(r'[0-9]|$', tag['name'])[0]
        tags_list.append([int(tag_number), tag['rssi']])

    for i in range(1, 4):
        exist_flag = False
        for tag_iterator in tags_list:
          if i == tag_iterator[0]:
              exist_flag = True

        if not exist_flag:
            tags_list.append([i, -100])

    return tags_list

# Crear vector
rssi_vector = [ [0, 0, 0, 0,0], [0, 0, 0, 0, 0], [ 0, 0, 0, 0,0]]
client = mqtt.Client("mqtt-test") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("diego", "1020785214")
client.connect('192.168.20.45', 1883)
client.loop_forever()  # Start networking daemon


