import os
import csv 
from itertools import cycle
from datetime import datetime
import json

def get_dir(folder):
    try: 
        return len([i for i in os.listdir(os.path.join(os.getcwd(),folder)) if i.endswith('.nef')])
    except FileNotFoundError:
        return 0
    

try:
    import Tkinter as tk     ## Python 2.x
    import tkMessageBox as messagebox
except ImportError:
    import tkinter as tk     ## Python 3.x
    from tkinter import messagebox


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
            sides = cycle(('r','v'))
            path = os.path.join(os.getcwd(),codexid,'%s_%s.csv' %(codexid,datetime.now().year))
            if os.path.exists(path):
                messagebox.showwarning(title="Struttura già esistente.", message="La struttura è già esistente")
                return False
            self.loaded = False
            os.mkdir(codexid)
            data = {
                "fogli_guardia_ante":fogli_guardia_ante,
                "fogli_guardia_post":fogli_guardia_post,
                "fogli":fogli,
                "targets":ck(self.targets),
                "tagli":ck(self.tagli)}
            with open(self.session_path, 'w') as outfile:
                json.dump(data, outfile)
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

            
            folders = ['Recto','Dorso e tagli','Target','Verso']
            for folder in folders:
                os.mkdir(os.path.join(codexid,folder))

        B = tk.Button(self.win, text ="Genera struttura", command = genera_struttura)

        B.grid(row=3,column=1)

        # CONTATORI
        # Tagli
        self.tk_varta = tk.StringVar()
        self.tk_varta.set("Tagli")
        labt=tk.Label(self.win, textvariable=self.tk_varta,
                       font=("Helvetica",size)) # bg='#40E0D0', fg='#FF0000',
        labt.place(x=20, y=200)
        # Recti
        self.tk_varr = tk.StringVar()
        self.tk_varr.set("Recto")
        labr=tk.Label(self.win, textvariable=self.tk_varr,
                       font=("Helvetica",size)) # bg='#40E0D0', fg='#FF0000',
        labr.place(x=20, y=250)
        # Versi
        self.tk_varv = tk.StringVar()
        self.tk_varv.set("Versi")
        labv=tk.Label(self.win, textvariable=self.tk_varv,
                      font=("Helvetica",size)) # bg='#40E0D0', fg='#FF0000',
        labv.place(x=20, y=300)
        # Target
        self.tk_vartg = tk.StringVar()
        self.tk_vartg.set("Targets")
        labtg=tk.Label(self.win, textvariable=self.tk_vartg,
                       font=("Helvetica",size))
        labtg.place(x=20, y=150)
        # Progresso
        self.tk_varcp = tk.StringVar()
        self.tk_varcp.set("Completezza:")
        labcp=tk.Label(self.win, textvariable=self.tk_varcp,
                       font=("Helvetica",size))
        labcp.place(x=20, y=400)
        
        
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