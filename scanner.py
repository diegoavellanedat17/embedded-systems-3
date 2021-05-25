
from time import sleep
import serial

ser = serial.Serial ("/dev/ttyS0", 115200)    #Open port with baud rate
while True:
    received_data = ser.read()              #read serial port
    sleep(0.03)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)
    try:    	
    	received_data=received_data.decode('utf8')
    	print(received_data)
    except Exception as e:
    	print(e)


