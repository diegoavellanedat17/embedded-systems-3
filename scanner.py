
from time import sleep
import serial
import time
import threading
import queue
#Tener un hilo para que cada que reciba un dato serial imprima en pantalla

ser = serial.Serial ("/dev/ttyS0", 115200)    #Open port with baud rate

qBLE_Data=queue.Queue()

def serial_worker():
    item=qBLE_Data.get()
    print(item)
    # Aqui se hará append al archivo

threading.Thread(target=serial_worker, daemon=True).start()

while True:
    received_data = ser.read()              #read serial port
    sleep(0.03)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)	
    received_data=received_data.decode('utf8')
    qBLE_Data.put(received_data)

    	


