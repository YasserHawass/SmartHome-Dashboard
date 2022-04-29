import serial
import time
import datetime

arduino = serial.Serial('COM3', 9600, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)  #todo auto detection for arduino UNO
time.sleep(2)
arduino.write(b'255.0.0')
