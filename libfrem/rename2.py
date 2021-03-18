import os


def create_name(fondo,romanid,dis,config,page,pagedis,imgtyp,imageform):
    romanid = str(int(romanid)).zfill(4)
    page = str(int(page)).zfill(4)
    if dis is None:
        dis = "_0"
    if len(dis) > 2:
        raise ValueError("Dis must have lenght 2!")
    
    n = "".join([fondo,romanid,dis,config,page,pagedis,imgtyp])
    return ".".join([n,imageform])

# listafile = os.listdir(os.getcwd())
# imgs = sorted([i for i in listafile if i.endswith('.jp2') or i.endswith('.JP2')])
# for idx,fname in enumerate(imgs):
#      os.rename(fname,create_name("m",41,None,"visn18_",idx,"a","1","jp2"))


det_p = os.path.join(os.getcwd(),'Dorso e tagli')
rect_p = os.path.join(os.getcwd(),'Recto')
ver_p = os.path.join(os.getcwd(),'Verso')
tg_p = os.path.join(os.getcwd(),'Target')

numero_codice = 257

idx = 1
imgs_rec = sorted([i for i in os.listdir(rect_p) if i.endswith('.nef')])
for i in imgs_rec:
    org = os.path.join(rect_p,i)
    new = os.path.join(rect_p,create_name("m",numero_codice,None,"visn20_",idx,"a","0","nef"))
    os.rename(org,new)
    idx += 2

# il primo è il secondo della serie rovesciato
count = 2 
imgs_ver = reversed(sorted([i for i in os.listdir(ver_p) if i.endswith('.nef')]))
for j in imgs_ver:
    org = os.path.join(ver_p,j)
    new = os.path.join(ver_p,create_name("m",numero_codice,None,"visn20_",count,"a","0","nef"))
    os.rename(org,new)
    count += 2
count-=1 # ritorno all'ultimo

img_det = sorted([i for i in os.listdir(det_p) if i.endswith('.nef')])
dorso = True # il prossimo sarà il dorso
for fname in img_det:
    # il dorso (prima immagine) la poniamo a zero
    org = os.path.join(det_p,fname) 
    if dorso:
        new = os.path.join(det_p,create_name("m",numero_codice,None,"visn20_","0","a","0","nef"))
        dorso = False
    else: 
        new = os.path.join(det_p,create_name("m",numero_codice,None,"visn20_",count,"a","0","nef"))
        count +=1
    os.rename(org,new)
    

imgs_tg = sorted([i for i in os.listdir(tg_p) if i.endswith('.nef')])
for k in imgs_tg:
    org = os.path.join(tg_p,k)
    new = os.path.join(tg_p,create_name("m",numero_codice,None,"visn20_",count,"a","0","nef"))
    os.rename(org,new)
    count+=1

