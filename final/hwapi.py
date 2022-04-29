import serial
import time
import threading as th

def hw_worker():
    # Serial port
    ino = serial.Serial('COM6', 9600)

    while True:
        ino.flush()
        #read line from serial port
        # line = ino.readline()
        # #print line
        # print(line)
        
        ino.write(b'1.1.1')
        time.sleep(1)
        ino.write(b'0.0.0')
        time.sleep(1)

p1 = th.Thread(target=hw_worker)
p1.start()
