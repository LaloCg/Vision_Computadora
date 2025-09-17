import serial
import  time

arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)
#time.sleep(2)

def send(estado):
    if estado == True:
        arduino.write('1')
    else:
        arduino.write('0')
    arduino.close()