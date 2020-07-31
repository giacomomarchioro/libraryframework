import sqlalchemy as db
from datetime import datetime
from AcquireQR import acquireQRandInfo
from bilance import balance
from savecamera import acquirephoto
import os
from pathlib import Path

# campi fissi
stanza = 205
# Create the database or access it.
engine = db.create_engine('sqlite:///movements_%s.sqlite' %stanza)
connection = engine.connect()
metadata = db.MetaData()

emp = db.Table('movimenti_stanza_%s'%stanza, metadata,
              db.Column('Time_stamp', db.DateTime()),
              db.Column('ID_bene', db.Integer()),
              db.Column('destinazione', db.Integer()),
              db.Column('peso_cg', db.Integer()),
              # codice bilancia?
              # utente loggato?
              # motivazione spostamento?
              )
metadata.create_all(engine) #  Creates the table

# operatore
operatore = 'Giacomo'
peso = 234.56

mybalance = balance('COM3')

choices = {0:'laboratorio_206',
           1:'sala consultazione_205',
           2:'vecchio lab. fotografico_209',
           3:'sala manoscritti_211',
           4:'archivio Fumanelli_207',
           5:'archivio_na',
           6:'loggia salone grande_212',
           7:'sala Galtarossa_210',
           8:'sala Zamboni_207'}

while True:
    # mybalance.waiting_forvalue()

    # campo da lettura ettichetta
    now = datetime.utcnow()
    name = str(now)[:-4]
    # we add the date for assuring is not overwritten
    imgpath = os.path.join(Path(os.getcwd()).parent,'foto controllo',name)
    results = acquireQRandInfo(choices=choices,
                               frase='Selezionare destinazione:',
                               saveimage=True,
                               filename=imgpath)
    if results:
        etichetta,destinazione = results
    else:
        break
    campi = etichetta.split(' # ')
    object_ID = int(campi[0])
    destinazione_ID = int(destinazione.split('_')[-1])
    # peso = int(mybalance.get_average_stablemasurement()*100)
    
    # confronto peso
    # peso_previsto = modellotermoigrometrico(ID)
    # differenza_peso = peso_attuale - peso_previsto
    # if abs(differenza_peso) > soglia:
    #   print("Peso del bene discosta di %s" %(differenza_peso) 



    query = db.insert(emp).values(Time_stamp=now,
                                  ID_bene=int(object_ID),
                                  destinazione=int(destinazione_ID),
                                  peso_cg=int(peso*100))
    ResultProxy = connection.execute(query)
    
    # acquirephoto(path,'Acquire image')
    # mybalance.waiting_forvalue(autotare=True)

    print("Bene con ID %s peso (%s g) movimentato verso %s (S. %s) in data %s" %(object_ID,peso,destinazione,destinazione_ID,str(now)))
    #print("%s  %s ha movimentato per %s il bene %s ( %s g)  registrato in stanza %s (transito verso %s)" \
    #    %(datetime.utcnow(),operatore,Motivo,object_ID,peso,stanza,destinazione ))