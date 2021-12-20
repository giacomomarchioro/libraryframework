import json
import os

from multiprocessing.pool import ThreadPool
import subprocess

folders = [i for i in os.listdir('processed_images/') if os.path.isdir("processed_images/"+i)]

foldn = os.path.basename(os.getcwd())

with open("tavolaconversione.json") as t: 
        tavolaconversione = json.load(t)

# https://stackoverflow.com/questions/26774781/python-multiple-subprocess-with-a-pool-queue-recover-output-as-soon-as-one-finis
inpputfile = "processed_images/8/m0040_0_0324r0324r__s730PE_10.tif"
outputfile = "m0040_0/m0040_0_0324r0324r__s425PEV21"

def work(inputfile,outputfile):
    command = f"""opj_compress -i {inputfile} -o {outputfile}.jp2 -r 2.5 -n 7 -c "[256,256]" -b "64,64" -p RPCL -SOP"""
    #command = ["opj_compress", "-i",inputfile,"-o",outputfile+".jp2","-r", "2.5","-n", "7","-c", '"[256,256]"',"-b",'"64,64"', "-p", "RPCL","-SOP"]
    my_tool_subprocess = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    my_tool_subprocess.wait()
    print(my_tool_subprocess)
    return my_tool_subprocess

num = 4  # set to the number of workers you want (it defaults to the cpu count of your machine)
tp = ThreadPool(num)

for i in tavolaconversione:
    idman = tavolaconversione[i]['id_manoscritto']
    if not os.path.exists(idman):
        os.mkdir(idman)
    folder_path = os.path.join('processed_images',i)
    images = [ j for j in os.listdir(folder_path)if j.endswith('.tif')]

   
    print("Created thread")
    for image in images:
        destilename = os.path.join(idman,image)
        outputfile = os.path.splitext(destilename)[0][:-2] + "21"
        inpputfile = os.path.join(folder_path,image)
        print(outputfile)
        print(inpputfile)
        tp.apply_async(work, (inpputfile,outputfile))
        print("Sent new command")


tp.close()
print("Closed")
tp.join()
