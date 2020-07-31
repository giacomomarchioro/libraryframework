from datetime import datetime
import os





object_ID = 5
now = datetime.now()
version = 1

RAWpath = os.path.join('Imaging visibile','RAW files')

def createdir(func):
    def function_wrapper(object_ID,path, year,version):
        if year == None:
            year = now.year

        dirname = func(object_ID,path, year,version)

        while os.path.isdir(os.path.join(path,dirname)):
            version+=1
            dirname = func(object_ID,path, year,version)
        os.mkdir(os.path.join(path,dirname))
        return True
    return function_wrapper

    
    
   



@createdir
def createRAWdird(object_ID,path, year,version):
    return "RAW_%s_%s_v%s" %(str(object_ID).zfill(4),year,version)


def createRAWdir(object_ID,path= RAWpath, year=None,version=1):
    if year == None:
        year = now.year
    dirnameRAW = "RAW_%s_%s_v%s" %(str(object_ID).zfill(4),year,version)
    while os.path.isdir(os.path.join(RAWpath,dirnameRAW)):
        version+=1
        dirnameRAW = "RAW_%s_%s_v%s" %(str(object_ID).zfill(4),year,version)
    os.mkdir(os.path.join(RAWpath,dirnameRAW))
    return dirnameRAW
    

order = ['piattoanteriore','risguardia_anteriore','risguardia_posteriore','dorso','taglio centrale','piatto posteriore']
modality = ['vis1','vil2',]
order2 = ['pan','ran','rps','dor','tcn','pps']
# 00054_f1v_vis1_v1

def generatefilename(object_ID,path,book_element,modality,version=1):
    filename = "%s_%s_%s_v%s" %(str(object_ID).zfill(4),book_element,modality,version)
    while os.path.exists(os.path.join(path,filename)):
        version+=1
        filename = "%s_%s_%s_v%s" %(str(object_ID).zfill(4),book_element,modality,version)
    return filename
