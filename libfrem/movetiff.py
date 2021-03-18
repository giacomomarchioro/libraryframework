import os
os.mkdir("Converted")
ext = ".tif"
folders = ["Dorso e tagli","Recto","Verso","Target"]
for folder in folders:
    path_dt = os.path.join(folder,'converted')
    dt = [i for i in os.listdir(path_dt) if i.endswith(ext)]
    for i in dt:
        os.rename(os.path.join(path_dt,i),os.path.join('Converted',i)) 
