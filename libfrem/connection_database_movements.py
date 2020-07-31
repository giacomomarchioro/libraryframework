import sqlalchemy as db
from datetime import datetime
from AcquireQR import acquireQR
# campi fissi
stanza = 205
# Create the database or access it.
engine = db.create_engine('sqlite:///movements_%s.sqlite' %stanza)
connection = engine.connect()
metadata = db.MetaData()

emp = db.Table('emp', metadata,
              db.Column('Time_stamp', db.DateTime()),
              db.Column('ID_bene', db.Integer()),
              db.Column('operatore', db.Integer()),
              db.Column('destinazione', db.Integer()),
              db.Column('Motivo', db.Integer()),
              db.Column('peso', db.Integer()),
              )
metadata.create_all(engine) #  Creates the table

# operatore
operatore = 'Giacomo'



# lettura dalla bilancia se connessa inizielizzera il peso a zero
# peso = 0
peso = 2345
while peso < 3:
    # se il peso è minore di una soglia l
    time.sleep(1)
    # peso = bilancia.read()

# quando rileva il peso il programma parte


# campo da lettura ettichetta
etichetta = acquireQR()
campi = etichetta.split(' # ')
object_ID = campi[0]

# confronto peso
# peso_previsto = modellotermoigrometrico(ID)
# differenza_peso = peso_attuale - peso_previsto
# if abs(differenza_peso) > soglia:
#   print("Peso del bene discosta di %s" %(differenza_peso) 


def dictchoose(dictionary):
        for i in sorted(dictionary):
            print( ' %s - %s' %(i, dictionary[i]))
        answ = input('Select number or type new option: ')
        if answ in dictionary.keys():
            return dictionary[answ]
        else:
            return answ

motivi = {
    '1':'consultazione',
    '2':'digitalizzazione',
    '3':'conservazione',
    '4':'analisi',
}

stanze = {
    '1':'sala digitalizzazione',
    '2':'segreteria',
    '3':'sala mss',
}


motivicod = {
    'consultazione':'1',
    'digitalizzazione':'2',
    'conservazione':'3',
    'analisi':'4',
}

stanzecod = {
    'sala digitalizzazione':'1',
    'segreteria':'2',
    'sala mss':'3',
}

print("Selezionare il motivo della movimentazione")
Motivo = dictchoose(motivi)

print("Selezionare la stanza di destinazione (0 se il bene resta nel luogo)")
destinazione = dictchoose(stanze)

query = db.insert(emp).values(
                            Time_stamp=datetime.utcnow(),
                            ID_bene=object_ID,
                            stanza=stanza,
                            operatore=operatore,
                            # convertiamo il nome nel codice per ottimizzare lo spazio
                            destinazione=stanzecod[destinazione],
                            Motivo=motivicod[Motivo],
                            peso=peso)
ResultProxy = connection.execute(query)

print("%s  %s ha movimentato per %s il bene %s ( %s g)  registrato in stanza %s (transito verso %s)" \
    %(datetime.utcnow(),operatore,Motivo,object_ID,peso,stanza,destinazione ))
