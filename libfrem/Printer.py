import serial
from datetime import datetime
from collections import deque
import glob
glob.glob('/dev/tty.*')


serial_port = '/dev/tty.usbserial'
baud_rate = 9600

ser = serial.Serial(serial_port, baud_rate, parity='N',stopbits=1)
ser.write(b'\x0E 1234567890  \x0D')
with serial.Serial(serial_port, baud_rate, parity='N', stopbits=1) as ser:
    ser.flushInput()  # maybe should be also output
    print("Start reading from: %s" % (ser.name))
    while True:
        try:
            ser_line = ser.readline()
            # We check if the packet is complete S at the begining
            # and E a the end [-3] (E\n).
            print(ser_line.split(' '))
            print(len(ser_line))

        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            break