import sqlalchemy as db
from datetime import datetime
import os
from pathlib import Path
import glob
jp2acqu = len(glob.glob1(myPath,"*.jp2"))

#dirlist = [filename for filename in os.listdir(os.getcwd()) if os.path.isdir(filename)]

with os.scandir(os.getcwd()) as mydir:
    dirs = [i.name for i in mydir if i.is_dir()]

jp2acqu = len(glob.glob1(myPath,"*.jp2"))


# campi fissi
stanza = 205
# Create the database or access it.
engine = db.create_engine('sqlite:///acquisizioni_server.sqlite' %stanza)
connection = engine.connect()
metadata = db.MetaData()

emp = db.Table('movimenti_stanza_%s'%stanza, metadata,
              db.Column('Time_stamp', db.DateTime()),
              db.Column('ID_bene', db.Integer()),
              db.Column('manifest', db.String())    ,
              db.Column('peso_cg', db.Integer()),
              # codice bilancia?
              # utente loggato?
              # motivazione spostamento?
              )
metadata.create_all(engine) #  Creates the table

    # query = db.insert(emp).values(Time_stamp=now,
    #                               ID_bene=int(object_ID),
    #                               destinazione=int(destinazione_ID),
    #                               peso_cg=int(peso*100))
    # ResultProxy = connection.execute(query)
