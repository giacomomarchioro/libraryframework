import sqlalchemy as db
from datetime import datetime
from AcquireQR import acquireQRandInfo
from bilance import balance
import os
from pathlib import Path

import winsound


# campi fissi
stanza = 205
# Create the database or access it.
engine = db.create_engine('sqlite:///movimenti_%s.sqlite' %stanza)
connection = engine.connect()
metadata = db.MetaData()

emp = db.Table('movimenti_stanza_%s'%stanza, metadata,
              db.Column('Time_stamp', db.DateTime()),
              db.Column('ID_bene', db.String()),
              db.Column('destinazione', db.Integer()),
              db.Column('peso_cg', db.Integer()),
              # codice bilancia?
              # utente loggato?
              # motivazione spostamento?
              )
metadata.create_all(engine) #  Creates the table

imagedir = os.path.join(Path(os.getcwd()),'foto controllo')
if not os.path.isdir(imagedir):
    os.mkdir(imagedir)
    

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
    winsound.Beep(1500, 300)
    winsound.Beep(1500, 300)
    print('Aspetto che tu posizioni il bene:')
    mybalance.waiting_forvalue()

    # campo da lettura ettichetta
    now = datetime.now()
    name = now.strftime("%Y%m%d%H%M%S")
    # we add the date for assuring is not overwritten
    imgpath = os.path.join('foto controllo',name)
    results = acquireQRandInfo(choices=choices,
                               frase='Selezionare destinazione:',
                               saveimage=True,
                               filename=imgpath)
    if results:
        etichetta,destinazione = results
    else:
        break
    object_ID = etichetta[:7]
    destinazione_ID = int(destinazione.split('_')[-1])
    print('Peso il manoscritto.')
    peso = int(mybalance.get_average_stablemasurement()*100)
    winsound.Beep(2500, 500)
    print('Bene pesato')
    # confronto peso
    # peso_previsto = modellotermoigrometrico(ID)
    # differenza_peso = peso_attuale - peso_previsto
    # if abs(differenza_peso) > soglia:
    #   print("Peso del bene discosta di %s" %(differenza_peso) 

    print("inserisco dati nel database")

    query = db.insert(emp).values(Time_stamp=now,
                                  ID_bene=object_ID,
                                  destinazione=int(destinazione_ID),
                                  peso_cg=int(peso))
    ResultProxy = connection.execute(query)
    
    # acquirephoto(path,'Acquire image')
    print("Rimuovere il bene.")
    #mybalance.waiting_forvalue(autotare=True)

    print("Bene con ID %s (%s) peso (%s cg) movimentato verso %s (S. %s) in data %s" %(object_ID,etichetta[7:].strip(),peso,destinazione,destinazione_ID,str(now)))
    #print("%s  %s ha movimentato per %s il bene %s ( %s g)  registrato in stanza %s (transito verso %s)" \
    #    %(datetime.utcnow(),operatore,Motivo,object_ID,peso,stanza,destinazione ))

