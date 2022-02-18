import random
import time
from datetime import datetime, timedelta
import paho.mqtt.client as mqtt
import paho.mqtt.client as mqtt
import re
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

    payload = msg.payload.decode("utf-8")
    topic = msg.topic
    now = datetime.now()
    mapped_time = time_map(now)
    #print(f"Topic [{topic}]: Payload {payload} Time: {mapped_time}")
    #devices = re.findall(r'\[.*?\]|$', payload)[0]
    devices = re.findall(r'\[.*?\]', payload)
    replacers = {'[\'': ''}
    #print(devices)
    #f = open("rawData.txt", "a")
    if len(devices) > 1:
        current_time = datetime.now()
        for device in reversed(devices):
            mapped_current_time = time_map(current_time)
            #f = open(f"{msg.topic}.txt", "a")
            #f.write(f"\n{get_rssi_info(str(device))},{mapped_current_time}")
            #f.close()
            #f.write(f" \n Topic: {msg.topic}, Devices : {device}, Time: {mapped_current_time}")
            current_time = current_time - timedelta(seconds=4)
            print(f"Topic [{msg.topic}]: Payload {device} Time: {mapped_current_time}")
    else:
        #f.write(f" \n Topic: {msg.topic}, Devices : {devices}, Time: {mapped_time}")
        print(f"Topic: [{msg.topic}], Devices : {devices}, Time: {mapped_time}")
        #f = open(f"{msg.topic}.txt", "a")
        #f.write(f"\n{get_rssi_info(str(devices))},{mapped_time}")
        #f.close()
    #f.close()

def time_map(now):
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

def get_rssi_info(payload):
    tag_info = re.findall(r'-[0-9]{2}|$', payload)[0]
    if not tag_info:
        tag_info = -100
    #tag_info = tag_info.replace('', '-100')
    return tag_info

client = mqtt.Client("mqtt-test") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("diego", "1020785214")
client.connect('192.168.20.45', 1883)
client.loop_forever()  # Start networking daemon


