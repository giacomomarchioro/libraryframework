"""
This script was made for comunicating with KERN balances 572/573/KB/DS/FKB.

Some functions work only if the right modality is set.
To set the modality pres MODE buttton until you reach PRINTER? menu. Then
pres YES (REF) and MODE again until you reach the parameter you need.

AUTOPRINT if YES print stable value to serial when weight is loaded or
unloaded.

AUTOPRT PC if YES keeps sending values to the serial port. (must be used 
for detect_weight_rise(),persistent_stablemasurement(),average_stablemasurement() )
"""
import serial
from datetime import datetime
from collections import deque

serial_port = '/dev/ttyUSB0'
class balance:
    """ This class define the balance instrument. The methods allow to communicate
    with the balance.
    """
    def __init__(self, port, boudrate=9600, linesmemory=10):
        self.serial_port = port
        self.baud_rate = boudrate
        self.last_value = deque(maxlen=linesmemory)
        self.last_read = deque(maxlen=linesmemory)
        self.last_command = deque(maxlen=linesmemory)

    def read_value(self):
        with serial.Serial(self.serial_port,
                           self.baud_rate,
                           parity='N',
                           stopbits=1) as ser:
            ser.flushInput()  # maybe should be also output
            print("Start reading from: %s" % (ser.name))
            ser_line = ser.readline()
            self.last_read.append(ser_line)
                
    def write_value(self, command):
        with serial.Serial(self.serial_port,
                           self.baud_rate,
                           parity='N',
                           stopbits=1) as ser:
            ser.flushInput()  # maybe should be also output
            ser.write(command)
            ser_line = ser.readline()
            self.last_read.append(ser_line)
            self.last_command.append(command)

    def stable_weight(self):
        self.write_value('s')

    def tare(self):
        self.write_value('t')

    def weight(self):
        self.write_value('w')
    
    def convert_line_to_grams(self,ser_line):
        return float(ser_line[4:-6].strip())

    def waiting_forvalue(self,autotare=False,autotarethreshold=3):
        with serial.Serial(self.serial_port,
                           self.baud_rate,
                           parity='N',
                           stopbits=1) as ser:
            while True:
                ser_line = ser.readline()
                if "=Overload=" in ser_line:
                    print("Overload detected")
                    return False
                if len(ser_line) < 18:
                    # the aspected lenght is 18 character
                    continue
                else:
                    grams = self.convert_line_to_grams(ser_line)
                    if grams < autotarethreshold and autotare:
                        self.tare()
                    return grams
                print(grams)

    def detect_weight_rise(self,threshold_g=1,start_value=0):
        """detect any variation of the weight measured by the scale.
        """
        with serial.Serial(self.serial_port,
                           self.baud_rate,
                           parity='N',
                           stopbits=1) as ser:
            ser.flushInput()  # maybe should be also output
            print("Start reading from: %s" % (ser.name))
            previous_value = start_value
            while True:
                ser_line = ser.readline()
                if "=Overload=" in ser_line:
                    return True
                if len(ser_line) < 18:
                    # the aspected lenght is 18 character
                    continue
                else:
                    grams = self.convert_line_to_grams(ser_line)
                    diff = abs(previous_value - grams)
                    if diff > threshold_g:
                        print("Detected weight raise")
                        return True
                previous_value = grams
                print(previous_value)


    def persistent_stablemasurement(self,consecutivevalues=5):
        with serial.Serial(self.serial_port,
                           self.baud_rate,
                           parity='N',
        stopbits=1) as ser:
            ser.flushInput()  # maybe should be also output
            print("Start reading from: %s" % (ser.name))
            values = deque(range(consecutivevalues),maxlen=consecutivevalues)
            unstables = 0
            while True:
                ser_line = ser.readline()
                if "=Overload=" in ser_line:
                    return False
                if len(ser_line) < 18:
                    # the aspected lenght is 18 character
                    continue
                else:
                    grams = self.convert_line_to_grams(ser_line)
                    # the character g is printed if the measurement is stable
                    if ser_line[-5] == 'g':
                        values.append(grams)
                    else:
                        unstables+=1
                if unstables > 10:
                    print("Sample unstable, seems not at equilibrium")
                if len(set(values)) == 1:
                    return values[0]
                print(ser_line)

    def average_stablemasurement(self,numberofmeasurment=5):
        with serial.Serial(self.serial_port,
                           self.baud_rate,
                           parity='N',
                           stopbits=1) as ser:
            ser.flushInput()  # maybe should be also output
            print("Start reading from: %s" % (ser.name))
            values =[]
            while True:
                ser_line = ser.readline()
                if "=Overload=" in ser_line:
                    return False
                if len(ser_line) < 18:
                    # the aspected lenght is 18 character
                    continue
                else:
                    grams = self.convert_line_to_grams(ser_line)
                    # the character g is printed if the measurement is stable
                    if ser_line[-5] == 'g':
                        values.append(grams)
                if len(values) == numberofmeasurment:
                    average = round(sum(values)/float(numberofmeasurment),2)
                    return average
                print(ser_line)

    def get_average_stablemasurement(self,numberofmeasurment=3):
        values = [self.convert_line_to_grams(self.stable_weight()) for i in range(numberofmeasurment)]
        average = round(sum(values)/float(numberofmeasurment),2)
        return average
