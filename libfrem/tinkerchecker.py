import os
from datetime import datetime

def get_dir(folder):
    try: 
        return len(os.listdir(os.path.join(os.getcwd(),folder)))
    except FileNotFoundError:
        return 0
    

try:
    import Tkinter as tk     ## Python 2.x
except ImportError:
    import tkinter as tk     ## Python 3.x

class UpdateLabel():
    def __init__(self,fogli_guardia_ante,fogli):
        size = 28
        self.fogli_guardia_ante = fogli_guardia_ante
        self.fogli = fogli
        self.win = tk.Tk()
        self.win.title("Scan checker")
        self.win.minsize(800, 600)
        self.ctr = 0

        tk.Label(self.win, text="First Name").grid(row=0)
        tk.Label(self.win, text="Last Name").grid(row=1)

        e1 = tk.Entry(self.win)
        e2 = tk.Entry(self.win)

        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        labf=tk.Label(self.win, text='Fogli',
                       bg='#40E0D0', fg='#FF0000',font=("Helvetica",size))
        labf.place(x=20, y=10)
        # Tagli
        self.tk_varta = tk.StringVar()
        self.tk_varta.set("Tagli")
        labt=tk.Label(self.win, textvariable=self.tk_varta,
                       bg='#40E0D0', fg='#FF0000',font=("Helvetica",size))
        labt.place(x=20, y=50)
        # Recti
        self.tk_varr = tk.StringVar()
        self.tk_varr.set("Recto")
        labr=tk.Label(self.win, textvariable=self.tk_varr,
                       bg='#40E0D0', fg='#FF0000',font=("Helvetica",size))
        labr.place(x=20, y=100)
        # Versi
        self.tk_varv = tk.StringVar()
        self.tk_varv.set("Versi")
        labv=tk.Label(self.win, textvariable=self.tk_varv,
                       bg='#40E0D0', fg='#FF0000',font=("Helvetica",size))
        labv.place(x=20, y=150)
        # Target
        self.tk_vartg = tk.StringVar()
        self.tk_vartg.set("Targets")
        labtg=tk.Label(self.win, textvariable=self.tk_vartg,
                       bg='#40E0D0', fg='#FF0000',font=("Helvetica",size))
        labtg.place(x=20, y=200)
        
        
        # Updated
        self.updater()
        self.win.mainloop()

    def updater(self):
        self.ctr += 1
        cr = get_dir('Recto')
        self.tk_varr.set("Recto: %s/%s Corrente: %s recto" %(cr,self.fogli,cr - self.fogli_guardia_ante))
        # Verso è invertito comincia dai numeri alti
        cr = get_dir('Verso')
        self.tk_varv.set("Verso: %s/%s Corrente: %s verso" %(cr,self.fogli,self.fogli - self.fogli_guardia_ante-cr))
        cr = get_dir('Target')
        self.tk_vartg.set("Target: %s/%s Corrente: %s" %(cr,4,cr))
        cr = get_dir('Dorso e tagli')
        self.tk_varta.set("Tagli: %s/%s Corrente: %s" %(cr,4,cr))
        self.win.after(1000, self.updater)


UL=UpdateLabel(20,4)