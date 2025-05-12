"""
Rinomina i file PhaseONE, contenuti nella gerarchia delle cartelle:
- Dorso e tagli
- Recto
- Verso
- Target

"""

import os
import csv

test = True
fileFormat = ".nef"
configurazione = "aVISNMV"

def isImage(filename):
    return filename.endswith(fileFormat) and not filename.startswith(".")

csvFiles = [ i for i in os.listdir(os.getcwd()) if not i.startswith(".") and i.endswith(".csv")]
assert len(csvFiles) == 1, "Found multiple csv files in the folder"
csvFileName = csvFiles[0]
numero_codice = "ASVr_UR_"+os.path.basename(os.getcwd())+"_"
nomiRecto = []
nomiVerso = []



def create_name(identification,
                elementType,
                element,
                subelement,
                disambiguator,
                configuration,
                counter,
                fileFormat):
    # BCVRm1853_0_x0001r0001r__aVISPKV00.jp2
    assert len(identification) < 13, "Folder name should not exceed 13 characters"
    if len(identification) == 11:
        identification = identification + "_"
    dis = "__"
    if disambiguator != "":
        dis = disambiguator.zfill(2)
    idPagina = f"{element.zfill(4)}{subelement}"*2
    fileNamesParts = [
        identification,
        elementType,
        idPagina,
        dis,
        configuration,
        counter,
        fileFormat
    ]
    imageName = "".join(fileNamesParts)
    assert len(imageName) == 38, "Image name should have 38 characters."
    return imageName

with open(os.path.join(os.getcwd(),csvFileName)) as f:
    csvDicts = csv.DictReader(f)
    # skip the first line
    next(csvDicts)
    for csvDict in csvDicts:
        tipo = csvDict['tipo']
        elemento = csvDict['elemento']
        sottoElemento = csvDict['sottoelemento']
        disambiguatore = csvDict['disambiguatore']
        name = create_name(numero_codice,
                        tipo,
                        elemento,
                        sottoElemento,
                        disambiguatore,
                        configuration=configurazione,
                        counter="00",
                        fileFormat=fileFormat
                        )
        if sottoElemento == "r":
            nomiRecto.append(name)
        elif sottoElemento == "v":
            nomiVerso.append(name)
        else:
            raise ValueError("No recto verso indication found.")
logging = []

def renameImage(folderPath,fileName,newFileName):
    org = os.path.join(folderPath,fileName)
    new = os.path.join(folderPath,newFileName)
    if test:
        print(folderPath)
        message ="→".join((fileName,newFileName))
        logging.append((folderPath,message))
        print(message)
        print("---")
    else:
        os.rename(org,new)


# RECTO
rect_p = os.path.join(os.getcwd(),'Recto')
imgs_recto = sorted([i for i in os.listdir(rect_p) if isImage(i)])
for ind,i in enumerate(imgs_recto):
    renameImage(rect_p,i,newFileName=nomiRecto[ind])

# VERSO
ver_p = os.path.join(os.getcwd(),'Verso')
# il primo è il secondo della serie rovesciato
imgs_ver = reversed(sorted([i for i in os.listdir(ver_p) if isImage(i)]))
for ind,i in enumerate(imgs_ver):
    renameImage(ver_p,i,newFileName=nomiVerso[ind])


det_p = os.path.join(os.getcwd(),'Dorso e tagli')
img_det = sorted([i for i in os.listdir(det_p) if isImage(i)])
dorso = True # il prossimo sarà il dorso
count = 1
for fname in img_det:
    # il dorso (prima immagine) la poniamo a zero
    org = os.path.join(det_p,fname)
    if dorso:
        newName = create_name(numero_codice,
                    elementType="d",
                    element="0",
                    subelement="r",
                    disambiguator="__",
                    configuration=configurazione,
                    counter="00",
                    fileFormat=fileFormat
                    )
        dorso = False
    else:
        newName = create_name(numero_codice,
            elementType="y",
            element=str(count),
            subelement="_",
            disambiguator="__",
            configuration=configurazione,
            counter="00",
            fileFormat=fileFormat
            )
        count +=1
    renameImage(det_p,fname,newFileName=newName)


tg_p = os.path.join(os.getcwd(),'Target')
imgs_tg = sorted([i for i in os.listdir(tg_p) if isImage(i)])
count = 0
for k in imgs_tg:
    newName = create_name(numero_codice,
    elementType="z",
    element=str(count),
    subelement="_",
    disambiguator="__",
    configuration=configurazione,
    counter="00",
    fileFormat=fileFormat
    )
    count+=1
    renameImage(tg_p,k,newFileName=newName)

