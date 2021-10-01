import os
import csv 
from itertools import cycle
from datetime import datetime
import json
try:
    from AcquireQR import acquireQR
except:
    acquireQR = None

def get_dir(folder):
    try: 
        return len([i for i in os.listdir(os.path.join(os.getcwd(),folder)) if i.endswith('.IIQ')])
    except FileNotFoundError:
        return 0

os.chdir('C:/Users/PhaseONE-Rainbow/Desktop/')


try:
    import Tkinter as tk     ## Python 2.x
    import tkMessageBox as messagebox
except ImportError:
    import tkinter as tk     ## Python 3.x
    from tkinter import messagebox


#For windows downloads
#Right-click on the .dll
#"Properties"
#Under "General", click "Unblock"


#Requirements: This requires the pythonnet library. This is availible via pip from https://pypi.python.org/pypi/pythonnet. For more details see http://stackoverflow.com/questions/14633695/how-to-install-python-for-net-on-windows.

import clr
#This assumes that the Dlls are in the same folder as the python script
clr.AddReference(r"C:\Users\PhaseONE-Rainbow\Documents\Optec\HSFW_CustomDriverTools(2.0.9)\HSFW_CustomDriverTools\OptecHID_FilterWheelAPI")
from OptecHID_FilterWheelAPI import FilterWheels
from OptecHID_FilterWheelAPI import FilterWheel
my_instance = FilterWheels()

if my_instance.AttachedDeviceCount == 0:
    print("NO filterwheel found")

for HSFW in my_instance.FilterWheelList:
    print("Wheel Found")
HSFW.ClearErrorState()
HSFW.HomeDevice()
print("Number of Filters")
print(HSFW.NumberOfFilters)
print("Current Position")
print(HSFW.CurrentPosition)

def set_position(position):
    try:
        HSFW.CurrentPosition = position
    except Exception as e:
        print(e)
        HSFW.ClearErrorState()
        HSFW.HomeDevice()
        print('Moving to home again')
print("Current Position")
print(HSFW.CurrentPosition)

p = {
    'No filter':1,
    "UG1 (UV)":2,
    "BG39 (Visible)":3,
    "IR 830":4,
    "Baader + BG39":5}

import os 
from ctypes import windll
import time
mydll=windll.LoadLibrary(r"C:\Users\PhaseONE-Rainbow\Desktop\USBswitchE\Nuova cartella\USBaccessX64.dll")
cw=mydll.FCWInitObject()
devCnt=mydll.FCWOpenCleware(0)
print("found ", devCnt, " devices")
if devCnt < 2:
    print("One device is not connected")
#print("first serNum = ", serNum_left)
#print("first serNum = ", serNum_right)
serNum_left = mydll.FCWGetSerialNumber(0,0)
serNum_right = mydll.FCWGetSerialNumber(0,1)


class UpdateLabel():
    def __init__(self):
        size = 28
        self.win = tk.Tk()
        self.win.title("Scan checker")
        self.win.minsize(500, 500)
        self.ctr = 0

        tk.Label(self.win, text="Segnatura:").grid(row=0)
        tk.Label(self.win, text="Numero fogli:").grid(row=1)
        tk.Label(self.win, text="Piatti e guardie ant.:").grid(row=0,column=2)
        tk.Label(self.win, text="Piatti e guardie post.:").grid(row=1,column=2)
        tk.Label(self.win, text="Tagli:").grid(row=2,column=0)
        tk.Label(self.win, text="Targets:").grid(row=2,column=2)

        self.segnatura = tk.Entry(self.win)
        self.fogli = tk.Entry(self.win)
        self.fogli_guardia_ante = tk.Entry(self.win)
        self.fogli_guardia_post = tk.Entry(self.win)
        self.segnatura.grid(row=0, column=1)
        self.fogli.grid(row=1, column=1)
        self.fogli_guardia_ante.grid(row=0, column=3)
        self.fogli_guardia_post.grid(row=1, column=3)
        self.tagli = tk.Entry(self.win)
        self.tagli.insert(tk.END, '4')
        self.tagli.grid(row=2,column=1)
        self.targets = tk.Entry(self.win)
        self.targets.insert(tk.END, '3')
        self.targets.grid(row=2,column=3)
        self.loaded = False
        self.session_path = 'test'
        # checkbox
        self.glass = tk.IntVar()
        self.black_background = tk.IntVar()
        self.white_background = tk.IntVar()
        self.target_in_scene = tk.IntVar()
        
    
        def No_filter():
            set_position(1)
        def UG1_UV():
            set_position(2)
        def BG39_VIS():
            set_position(3)
        def IR_803():
            set_position(4)
        def BaaderBG39():
            set_position(5)
            
        def KaiserON():
            status = mydll.FCWSetSwitch(0,serNum_left,19,1)
            status2 = mydll.FCWSetSwitch(0,serNum_right,19,1)
            return status, status2
        
        def KaiserOFF():
            status = mydll.FCWSetSwitch(0,serNum_left,19,0)
            status2 = mydll.FCWSetSwitch(0,serNum_right,19,0)
            return status, status2
        
        def IR_ON():
            status = mydll.FCWSetSwitch(0,serNum_left,18,1)
            status2 = mydll.FCWSetSwitch(0,serNum_right,18,1)
            return status, status2
        
        def IR_OFF():
            status = mydll.FCWSetSwitch(0,serNum_left,18,0)
            status2 = mydll.FCWSetSwitch(0,serNum_right,18,0)
            return status, status2
        
        def VIS_ON():
            status = mydll.FCWSetSwitch(0,serNum_left,17,1)
            status2 = mydll.FCWSetSwitch(0,serNum_right,17,1)
            return status, status2
        
        def VIS_OFF():
            status = mydll.FCWSetSwitch(0,serNum_left,17,0)
            status2 = mydll.FCWSetSwitch(0,serNum_right,17,0)
            return status, status2
        
        def UV_ON():
            status = mydll.FCWSetSwitch(0,serNum_left,16,1)
            status2 = mydll.FCWSetSwitch(0,serNum_right,16,1)
            return status, status2
        
        def UV_OFF():
            status = mydll.FCWSetSwitch(0,serNum_left,16,0)
            status2 = mydll.FCWSetSwitch(0,serNum_right,16,0)
            return status, status2
        
        def QRsegn():
            label = acquireQR() #autoreturn
            self.segnatura.delete(0,tk.END)
            self.segnatura.insert(0,label[:7])

        def ck(myentry):
            if myentry.get().isdigit():
                return int(myentry.get())
            else:
                return 0 

        def genera_struttura():
            fogli = ck(self.fogli)
            ante_elements = ['dorso','piatto anteriore','risguardia anteriore',]
            post_elements = ['risguardia posteriore', 'piatto posteriore',]
            header = ["ID","Elemento","Collation","Period","Written_page_number","Description","Conservative_notes","Requires_analysis","Scanned_byConfiguration","Width_mm","Height_mm","Content","Plannedscan_ProjectID","Online_links"]
            codexid = self.segnatura.get()
            count = 1
            period = 600
            fogli_guardia_ante = ck(self.fogli_guardia_ante)
            fogli_guardia_post = ck(self.fogli_guardia_post)
            targets = ck(self.targets)
            tagli = ck(self.tagli)
            sides = cycle(('r','v'))
            path = os.path.join(os.getcwd(),codexid,'%s_%s.csv' %(codexid,datetime.now().year))
            if os.path.exists(path):
                messagebox.showwarning(title="Struttura già esistente.", message="La struttura è già esistente")
                return 
            print("Struttura creata: %s" %path)
            self.loaded = False
            os.mkdir(codexid)
            data = {
                "fogli_guardia_ante":fogli_guardia_ante,
                "fogli_guardia_post":fogli_guardia_post,
                "fogli":fogli,
                "targets":targets,
                "tagli":tagli,
                "glass":self.glass.get(), 
                "black_background":self.black_background.get(),
                "white_background":self.white_background.get(), 
                "target_in_scene":self.target_in_scene.get()} 

            with open(self.session_path, 'w') as outfile:
                json.dump(data, outfile,indent=2)
            with open(path, 'w', newline='',) as csvfile:
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

            
            folders = ['Recto','Dorso e tagli','Target','Verso','Inserti']
            for folder in folders:
                os.mkdir(os.path.join(codexid,folder))
        

        # WIDGETS:

        B = tk.Button(self.win, text ="Genera struttura", command = genera_struttura)

        B.grid(row=4,column=3)

        BQ = tk.Button(self.win, text ="Acquisici codice QR", command = QRsegn)
        BQ.grid(row=4,column=1)
        # CONTATORI
        # Tagli
        self.tk_varta = tk.StringVar()
        self.tk_varta.set("Tagli")
        labt=tk.Label(self.win, textvariable=self.tk_varta,
                       font=("Helvetica",size)) # bg='#40E0D0', fg='#FF0000',
        labt.place(x=20, y=220)
        # Recti
        self.tk_varr = tk.StringVar()
        self.tk_varr.set("Recto")
        labr=tk.Label(self.win, textvariable=self.tk_varr,
                       font=("Helvetica",size)) # bg='#40E0D0', fg='#FF0000',
        labr.place(x=20, y=270)
        # Versi
        self.tk_varv = tk.StringVar()
        self.tk_varv.set("Versi")
        labv=tk.Label(self.win, textvariable=self.tk_varv,
                      font=("Helvetica",size)) # bg='#40E0D0', fg='#FF0000',
        labv.place(x=20, y=320)
        # Target
        self.tk_vartg = tk.StringVar()
        self.tk_vartg.set("Targets")
        labtg=tk.Label(self.win, textvariable=self.tk_vartg,
                       font=("Helvetica",size))
        labtg.place(x=20, y=170)
        # Progresso
        self.tk_varcp = tk.StringVar()
        self.tk_varcp.set("Completezza:")
        labcp=tk.Label(self.win, textvariable=self.tk_varcp,
                       font=("Helvetica",size))
        labcp.place(x=20, y=420)
        
   
        


        tk.Checkbutton(self.win, text="vetro", variable=self.glass).grid(row=3,column=0)
        tk.Checkbutton(self.win, text="sfondo nero", variable=self.black_background).grid(row=3,column=1)
        tk.Checkbutton(self.win, text="sfondo bianco", variable=self.white_background).grid(row=3,column=2)
        tk.Checkbutton(self.win, text="target in scene", variable=self.target_in_scene).grid(row=3,column=3)
        def toggleF(button,func):
            f1.config(relief="raised",bg="SystemButtonFace")
            f2.config(relief="raised",bg="SystemButtonFace")
            f3.config(relief="raised",bg="SystemButtonFace")
            f4.config(relief="raised",bg="SystemButtonFace")
            f5.config(relief="raised",bg="SystemButtonFace")
            button.config(relief="sunken",bg="SpringGreen2")
            func()
            time.sleep(0.25)
            
        def nof():
            toggleF(f1,No_filter)
        f1 = tk.Button(self.win, text ="No filter", command = nof)
        f1.grid(row=5,column=0)
        def ug1():
            toggleF(f2,UG1_UV)
        f2 = tk.Button(self.win, text ="UG1 (UV)", command = ug1)
        f2.grid(row=5,column=1)
        def bg39():
            toggleF(f3,BG39_VIS)
        f3 = tk.Button(self.win, text ="BG38 (Visible)", command = bg39)
        f3.grid(row=5,column=2)
        def ir8():
            toggleF(f4,IR_803)
        f4 = tk.Button(self.win, text ="IR 830", command = ir8)
        f4.grid(row=5,column=3)
        def bad39():
            toggleF(f5,BaaderBG39)
        f5 = tk.Button(self.win, text ="Baader + BG39", command = bad39)
        f5.grid(row=5,column=4)
 

        def toggle():

            if s1.config('relief')[-1] == 'sunken':
                s1.config(relief="raised",bg="SystemButtonFace")
                KaiserOFF()
            else:
                s1.config(relief="sunken",bg="SpringGreen2")
                KaiserON()
            time.sleep(0.25)
            
        s1 = tk.Button(self.win, text ="Kaiser LED",relief="raised",command=toggle)
        s1.grid(row=6,column=0)
        
        def toggle2():

            if s2.config('relief')[-1] == 'sunken':
                s2.config(relief="raised",bg="SystemButtonFace")
                IR_OFF()
            else:
                s2.config(relief="sunken",bg="SpringGreen2")
                IR_ON()
            time.sleep(0.25)

        s2 = tk.Button(self.win, text ="IR LED", command = toggle2)
        s2.grid(row=6,column=1)
        def toggle3():

            if s3.config('relief')[-1] == 'sunken':
                s3.config(relief="raised",bg="SystemButtonFace")
                VIS_OFF()
            else:
                s3.config(relief="sunken",bg="SpringGreen2")
                VIS_ON()
            time.sleep(0.25)

        s3 = tk.Button(self.win, text ="VIS Dedo", command = toggle3)
        s3.grid(row=6,column=2)
        def toggle4():

            if s4.config('relief')[-1] == 'sunken':
                s4.config(relief="raised",bg="SystemButtonFace")
                UV_OFF()
            else:
                s4.config(relief="sunken",bg="dark orange")
                UV_ON()
            time.sleep(0.25)
 
        s4 = tk.Button(self.win, text ="⚠ UV Dedo ⚠", command = toggle4)
        s4.grid(row=6,column=3)
  
        # Updated
        self.updater()
        self.win.mainloop()

    def updater(self):
        def ck(myentry):
            if myentry.get().isdigit():
                return int(myentry.get())
            else:
                return 0 
        self.session_path = os.path.join(os.getcwd(),self.segnatura.get(),'session.json')
        self.ctr += 1
        if os.path.exists(self.session_path):
            with open(self.session_path) as json_file:
                data = json.load(json_file)
                self.fogli_guardia_ante.delete(0,tk.END)
                self.fogli_guardia_ante.insert(0,data['fogli_guardia_ante'])
                self.fogli_guardia_post.delete(0,tk.END)
                self.fogli_guardia_post.insert(0,data['fogli_guardia_post'])
                self.fogli.delete(0,tk.END)
                self.fogli.insert(0,data['fogli'])
                self.targets.delete(0,tk.END)
                self.targets.insert(0,data['targets'])
                self.tagli.delete(0,tk.END)
                self.tagli.insert(0,data['tagli'])
            

        guardia_ante = ck(self.fogli_guardia_ante)
        guardia_post = ck(self.fogli_guardia_post)
        tagli = ck(self.tagli)
        targets = ck(self.targets)
        fogli = ck(self.fogli)
        totelem = fogli + guardia_post + guardia_ante
        cr = get_dir(os.path.join(self.segnatura.get(),'Recto'))
        # numero di acquisizione nella cartella
        curr = cr - guardia_ante +1
        hint = ""
        if curr < 1:
            if curr == (1 - guardia_ante):
                hint = "(copertina)"
            else:
                hint = "(guardia)"
        if curr > fogli:
            if curr == (fogli + guardia_post):
                hint = "(copertina)"
            elif curr > (fogli + guardia_post):
                hint = "COMPLETO"
            else:
                hint = "(guardia)"
        self.tk_varr.set("Recto: %s/%s Corrente: %s recto %s" %(cr,totelem,curr,hint))
        # Verso è invertito comincia dai numeri alti
        hint2 = ""
        cr2 = get_dir(os.path.join(self.segnatura.get(),'Verso'))
        tot = fogli + guardia_post - cr2
        if tot > fogli:
            if tot == (fogli + guardia_post):
                hint2 = "(piatto posteriore)"
            else:
                hint2 = "(guardia)"
        if tot < 1:
            if tot == (1 - guardia_ante):
                hint2 = "(copertina)"
            elif tot < (1 - guardia_ante) :
                hint2 = "COMPLETO"
            else:
                hint2 = "(guardia)"
        self.tk_varv.set("Verso: %s/%s Corrente: %s verso %s" %(cr2,totelem,tot,hint2))
        cr3 = get_dir(os.path.join(self.segnatura.get(),'Target'))
        self.tk_vartg.set("Target: %s/%s Corrente: %s" %(cr3,targets,cr3+1))
        cr4 = get_dir(os.path.join(self.segnatura.get(),'Dorso e tagli'))
        self.tk_varta.set("Tagli: %s/%s Corrente: %s" %(cr4,tagli,cr4+1))
        acqu_tot = guardia_post*2 + guardia_ante*2 + fogli*2 + tagli + targets
        tot_now = cr + cr2 + cr3 + cr4
        prc = tot_now/acqu_tot*100
        self.tk_varcp.set("Completezza: %s/%s  %.1f %%" %(tot_now,acqu_tot,prc))
        self.win.after(1000, self.updater)


UL=UpdateLabel()