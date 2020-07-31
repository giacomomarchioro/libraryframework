import serial
from datetime import datetime
from collections import deque

serial_port = '/dev/ttyUSB0'
baud_rate = 9600


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


def detect_weight_rise(threshold_g=1,start_value=0):
    """detect any variation of the weight measured by the scale.
    """
    with serial.Serial(serial_port, baud_rate, parity='N', stopbits=1) as ser:
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
                grams = float(ser_line[4:-6].strip())
                diff = abs(previous_value - grams)
                if diff > threshold_g:
                    print("Detected wight raise")
                    return True
            previous_value = grams
            print(previous_value)


def persistent_stablemasurement(consecutivevalues=5):
    with serial.Serial(serial_port, baud_rate, parity='N', stopbits=1) as ser:
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
                grams = float(ser_line[4:-6].strip())
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

def average_stablemasurement(numberofmeasurment=5):
    with serial.Serial(serial_port, baud_rate, parity='N', stopbits=1) as ser:
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
                grams = float(ser_line[4:-6].strip())
                # the character g is printed if the measurement is stable
                if ser_line[-5] == 'g':
                    values.append(grams)
            if len(values) == numberofmeasurment:
                average = round(sum(values)/float(numberofmeasurment),2)
                return average
            print(ser_line)
