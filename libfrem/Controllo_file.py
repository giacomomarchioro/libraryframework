import os
from datetime import datetime 

root = r"/Users/giacomo/Desktop/Progetto capitolare/Struttura capitolare/"
watching_folders = ['Imaging MWIR',
 'Imaging NIR ',
 'Imaging SWIR',
 'Imaging visibile',
 'Spettroscopia UV-VIS-NIR',]

subfolders = [
 'Master files',
 'Monitoraggio performance',
 'Quality control results',
 'RAW files']

dirl1 = [os.path.join(root,i) for i in watching_folders] 

times_maindirs = [os.path.getctime(i) for i in dirl1]

for i in times_maindirs:
    print(datetime.fromtimestamp(i))

dirnames = filter(os.path.isdir, os.listdir(root))

records = {}
for wfolder in watching_folders:
    print("*****")
    print(wfolder)
    print("******")
    pathdir = os.path.join(root,wfolder)
    os.chdir(pathdir)
    dirnames = filter(os.path.isdir, os.listdir(pathdir))
    #times_paths = dict(zip(map(os.path.getctime,filespath),filespath))
    records[wfolder]={ os.path.getctime(i):i for i in dirnames }
    #we sort the files this will speed up the search
    times_paths_sorted = sorted(times_paths.items())
    i=0

for wfolder in watching_folders:
    print "*****"
    print wfolder
    print "******"
    os.chdir(wfolder)
    filenames = filter(os.path.isfile, os.listdir(wfolder))
    filespath = [os.path.join(wfolder, fi) for fi in filenames] # add path to each file
    #times_paths = dict(zip(map(os.path.getctime,filespath),filespath))
    times_paths = { os.path.getctime(i):i for i in filespath }
    #we sort the files this will speed up the search
    times_paths_sorted = sorted(times_paths.items())
    i=0
    for t,fname in times_paths_sorted:
#               path = os.path.join(wfolder,wfile)
#                ct = time.ctime(os.path.getmtime(path))
#                mt = time.ctime(os.path.getctime(path))

        #print i

        ct = datetime.fromtimestamp(t) #time of the file

        if ct>=ranges[i] and ct < ranges[i+1]:
            print fname, tags[i]
#                if ct> ranges[i+1]:
#                    print fname, tags[i+1]
#                    i+=1
        #we have to skip any work package where we did not create file    
        while ct > ranges[i] and ct > ranges[i+1]:
            i+=1
        print fname, tags[i] 