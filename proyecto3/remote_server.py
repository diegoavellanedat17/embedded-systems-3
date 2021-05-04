
from Adafruit_IO import Client
import time
import RPi.GPIO as GPIO
import subprocess
import time
import threading
import queue
import config
# Importar las librerias correspondientes a GPIO i a Adafruit 

aio = Client(config.USER, config.TOKEN)
output_pin = 24
# Deshabilitar Warnings cuando se ejecuta el código
GPIO.setwarnings(False)
# Manjear la asignacion en BCM
GPIO.setmode(GPIO.BCM)
#Definir como salida
GPIO.setup(output_pin, GPIO.OUT)
# Enviar el valor del sensor


TEMP_FACTOR=1000

#Tener un hilo para cada que llegue un dato de temperatura ingresarlo a la cola
#y publicar en el servidor de adafruit
qTemp = queue.Queue()
qButton = queue.Queue()

def new_timer():
    global timer
    timer = threading.Timer(30.0, temp_send)

def temp_send():
    timer.cancel
    new_timer()
    timer.start()
    temperatura = subprocess.run(["cat","/sys/bus/w1/devices/28-3c01d0754b88/temperature"],stdout=subprocess.PIPE,text=True)
    temperatura= str(int(temperatura.stdout)/TEMP_FACTOR)
    print(temperatura)
    aio.send('temperatura-ds18b20', temperatura)

def worker_button():
    while True:
        #tomar el valos de la cola de temperatura
        item = qButton.get()
        #print('Temperatura = ',item)
        if(item.value=='ON'):
            print('encendido')
            GPIO.output(output_pin, GPIO.HIGH) # GPIO ON
        else:
            GPIO.output(output_pin, GPIO.LOW)  # GPIO OFF

threading.Thread(target=worker_button, daemon=True).start()
new_timer()
timer.start()
while True:
    data = aio.receive('led')
    qButton.put(data)


    