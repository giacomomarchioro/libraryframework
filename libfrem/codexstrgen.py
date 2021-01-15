import os
import csv 
from itertools import cycle
from datetime import datetime

fogli = 60
ante_elements = ['dorso','piatto anteriore','risguardia anteriore',]
post_elements = ['risguardia posteriore', 'piatto posteriore',]
header = ["ID","Elemento","Collation","Period","Written_page_number","Description","Conservative_notes","Requires_analysis","Scanned_byConfiguration","Width_mm","Height_mm","Content","Plannedscan_ProjectID","Online_links"]
codexid = '45dd6_B'
count = 1
period = 600
fogli_guardia_ante = 6
fogli_guardia_post = 4
sides = cycle(('r','v'))
with open('%s_%s.csv' %(codexid,datetime.now().year), 'w') as csvfile:
    cdxst = csv.writer(csvfile)
    cdxst.writerow(header)
    for i in ante_elements:
        cdxst.writerow([count,i,'1',period,"","test","damaged","UV","nik20","200","300","cont","dascabida",'wwww.test.it/esdasasdg.jp2'])
        count += 1
    for i in range(fogli_guardia_ante*2):
        side = next(sides) 
        sd = "g%s%s"%(i+1,side)
        cdxst.writerow([count,sd,'1',period,"","test","damaged","UV","nik20","200","300","cont","dascabida",'wwww.test.it/esdasasdg.jp2'])
        count += 1
    for i in range(fogli):
        side = next(sides) 
        sd = "%s%s"%(i+1,side)
        cdxst.writerow([count,sd,'1',period,"","test","damaged","UV","nik20","200","300","cont","dascabida",'wwww.test.it/esdasasdg.jp2'])
        count += 1
        side = next(sides)
        sd = "%s%s"%(i+1,side)
        cdxst.writerow([count,sd,'1',period,"","test","damaged","UV","nik20","200","300","cont","dascabida",'wwww.test.it/esdasasdg.jp2'])
        count += 1
    for i in range(fogli_guardia_post*2):
        side = next(sides) 
        sd = "g%s%s"%(i+1,side)
        cdxst.writerow([count,sd,'1',period,"","test","damaged","UV","nik20","200","300","cont","dascabida",'wwww.test.it/esdasasdg.jp2'])
        count += 1
    for i in post_elements:
        cdxst.writerow([count,i,'1',period,"","test","damaged","UV","nik20","200","300","cont","dascabida",'wwww.test.it/esdasasdg.jp2'])
        count += 1

os.mkdir(codexid)
folders = ['Recto','Tagli','Target','Verso']
for folder in folders:
    os.mkdir(os.path.join(codexid,folder))


    
