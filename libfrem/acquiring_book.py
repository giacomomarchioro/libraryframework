from itertools import cycle
from datetime import datetime
import os
from NamingNStructure import createRAWdir, generatefilename
from savecamera import acquirephoto
from AcquireQR import acquireQR


etichetta = acquireQR()
campi = etichetta.split(' # ')
object_ID = campi[0]
now = datetime.now()
RAWpath = os.path.join('Imaging visibile','RAW files')

elementi = ['piatto anteriore','risguardia anteriore','dorso','taglio centrale', 'taglio di testa','taglio di piede','risguardia posteriore','piatto posteriore']
modality = ['vis1','vil2',]
elementi_abr = ['pan','ran','dor','tdt','tdp','tcn','rps','pps']

# per ogni libro
rawdir = createRAWdir(object_ID, RAWpath)
v = cycle(('r', 'v'))
elem = zip(elementi, elementi_abr)
counter = 1
while True:
    abr = elementi_abr[ind]
    elem = elementi[ind]
    filename = generatefilename(object_ID=counter, path=rawdir, book_element=abr, modality='vis', version=1)
    command = acquirephoto(filename=os.path.join(os.getcwd(), RAWpath, rawdir, filename + '.jpg'),
                           instruction="Acquisisci %s" %elem)
    counter+=1
    if command == 'esc':
        break

while True:
    abr = "f%s%s" %(i, next(v))
    filename = generatefilename(object_ID=counter, path=rawdir, book_element=abr, modality='vis', version=1)
    command = acquirephoto(filename = os.path.join(os.getcwd(),RAWpath,rawdir,filename+'.jpg'), instruction= "Acquisisci foglio %s" %abr)
    counter+=1
    if command == 'esc':
        break
    abr = "f%s%s" %(i,next(v))
    filename = generatefilename(object_ID=counter, path=rawdir, book_element=abr, modality='vis', version=1)
    command = acquirephoto(filename=os.path.join(os.getcwd(),RAWpath,rawdir,filename+'.jpg'),instruction="Acquisisci foglio %s" %abr)
    counter+=1
    if command == 'esc':
        break
    


for ind in range(3,len(elementi)+1):
    abr = elementi_abr[ind]
    elem = elementi[ind]
    filename = generatefilename(object_ID= counter,path = rawdir,book_element=abr,modality='vis',version=1)
    acquirephoto(filename = os.path.join(os.getcwd(), rawdir, filename+'.jpg'), instruction= "Acquisisci %s" %elem)
    counter+=1
