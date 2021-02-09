import serial
from datetime import datetime
from collections import deque
import glob



serial_port = 'COM1'
baud_rate = 9600
data = datetime.now().strftime("%Y-%m-%d %H:%M")
numero_cod = "I (1)"
peso = '1234.5'
titolo = 'Psalterium com caonticis greaco-latinum'
postazione = '4'
collocazione = 'V III 4'
ser = serial.Serial(serial_port, baud_rate, parity='N',stopbits=1)

ser.write(b'\x1e         \r\n')
ser.write(b'\x1e    Biblioteca    \r\n')
ser.write(b'\x1e    Capitolare    \r\n')
ser.write(b'\x1e         \r\n')
ser.write(b'          %s \r\n' %data.encode())
ser.write(b'         \r\n')
ser.write(b' Codice  %s \r\n' %numero_cod.encode())
ser.write(b' %s\r\n' %titolo.encode())
ser.write(b'         \r\n')
ser.write(b' Collocazione: %s \r\n' %collocazione.encode())
ser.write(b' Peso: %s g Postazione: %s\r\n' %(peso.encode(),postazione.encode()))
ser.write(b'\x1e         \r\n')
#ser.write(b' Postazione: %s \r\n' %)
ser.write(b'\x1e         \r\n')
ser.write(b'\x1e         \r\n')
ser.write(b'\x1e         \r\n')
ser.write(b'\x1e         \r\n')

#ser.write(b'\x0E Biblioteca   \x0A')
#ser.write(b'\x0E Capitolare  \x0A')
#ser.write(b'\x1C\x57\x01 Biblioteca \x0A')
#ser.write(b'\x1C\x57\x01 Capitolare \x0A')
#ser.write(b' di \x0A')
#ser.write(b'\x1C\x57\x01 Verona \x0A')
#ser.write(b'\x1C\x57\x00')
# with serial.Serial(serial_port, baud_rate, parity='N', stopbits=1) as ser:
#     ser.flushInput()  # maybe should be also output
#     print("Start reading from: %s" % (ser.name))
#     while True:
#         try:
#             ser_line = ser.readline()
#             # We check if the packet is complete S at the begining
#             # and E a the end [-3] (E\n).
#             print(ser_line.split(' '))
#             print(len(ser_line))

#         except KeyboardInterrupt:
#             print("Keyboard Interrupt")
#             break