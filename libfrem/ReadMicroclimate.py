import sqlalchemy as db
import serial
from datetime import datetime
# ID Stanza
stanza = 205
# ID sensore
sensore = "BME"
# Create the database or access it.
engine = db.create_engine('sqlite:///climite_S%s_%s.sqlite' %(stanza,sensore))
connection = engine.connect()
metadata = db.MetaData()

emp = db.Table('environmental_data', metadata,
               db.Column('T_DegcC', db.Integer()),
               db.Column('P_Pascal', db.Integer()),
               db.Column('RH_times100', db.Integer()),
               db.Column('GasResistence_Ohms', db.Integer()),
               db.Column('Time_stamp', db.DateTime())
               )

metadata.create_all(engine) #  Creates the table
# Serial interface.
serial_port = 'COM3'
baud_rate = 9600


with serial.Serial(serial_port, baud_rate) as ser:
    ser.flushInput()  # maybe should be also output
    print("Start reading from: %s" % (ser.name))
    while True:
        try:
            ser_line = ser.readline().decode('utf-8')
            # We check if the packet is complete S at the begining
            # and E a the end [-3] (E\n).
            if ser_line[0] == 'S' and ser_line[-3] == 's':
                values = ser_line.split(';')[1::2]
                query = db.insert(emp).values(
                                              T_DegcC=values[0],
                                              P_Pascal=values[1],
                                              RH_times100=values[2],
                                              GasResistence_Ohms=values[3],
                                              Time_stamp=datetime.now())
                ResultProxy = connection.execute(query)
            else:
                print('Missed reading at %s' % (datetime.now()))
                print('Read: %s' % (ser_line))

        except:
            print("Keyboard Interrupt")
            break