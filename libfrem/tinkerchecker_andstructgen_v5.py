import os
import csv
from itertools import cycle
from datetime import datetime
import json

try:
    from AcquireQR import acquireQR
except:
    acquireQR = None


def get_dir(folder,fileFormat):
    try:
        return len(
            [
                i
                for i in os.listdir(os.path.join(os.getcwd(), folder))
                if i.endswith("."+fileFormat)
            ]
        )
    except FileNotFoundError:
        return 0


try:
    import Tkinter as tk  ## Python 2.x
    import tkMessageBox as messagebox
except ImportError:
    import tkinter as tk  ## Python 3.x
    from tkinter import messagebox


# For windows downloads
# Right-click on the .dll
# "Properties"
# Under "General", click "Unblock"

import os


def carica_lista(self):
    codexid = self.segnatura.get()
    if os.path.isdir(codexid):
        self.verso = []
        self.recto = []
        data = [i for i in os.listdir(codexid) if i.endswith(".csv")]
        if len(data) != 1:
            print("Lista non caricata!")
            return
        file_path = os.path.join(codexid, data[0])
        with open(file_path) as f:
            csvfile = csv.DictReader(f)
            for i in csvfile:
                if i["sottoelemento"] == "r":
                    self.recto.append(i)
                elif i["sottoelemento"] == "v":
                    self.verso.append(i)
        self.loaded = True
        self.tk_CSV.set("CSV:🟢")
        print("LOADED CSV!")
    else:
        self.tk_CSV.set("CSV:🔴")


class UpdateLabel:
    def __init__(self):
        size = 28
        self.win = tk.Tk()
        self.win.title("Scan checker")
        self.win.minsize(500, 500)
        self.ctr = 0

        tk.Label(self.win, text="Segnatura:").grid(row=0)
        tk.Label(self.win, text="Formato file:").grid(row=0, column=2)
        tk.Label(self.win, text="Tagli:").grid(row=2, column=0)
        tk.Label(self.win, text="Targets:").grid(row=2, column=2)

        self.segnatura = tk.Entry(self.win)
        self.fileFormat = tk.Entry(self.win)
        self.segnatura.grid(row=0, column=1)
        self.fileFormat.grid(row=0, column=3)
        self.fileFormat.insert(tk.END, "IIQ")
        self.tagli = tk.Entry(self.win)
        self.tagli.insert(tk.END, "4")
        self.tagli.grid(row=2, column=1)
        self.targets = tk.Entry(self.win)
        self.targets.insert(tk.END, "3")
        self.targets.grid(row=2, column=3)
        self.loaded = False
        self.session_path = ""
        # checkbox
        self.glass = tk.IntVar()
        self.black_background = tk.IntVar()
        self.white_background = tk.IntVar()
        self.target_in_scene = tk.IntVar()
        self.verso = []
        self.recto = []
        self.old_segnatura = None

        def QRsegn():
            label = acquireQR()  # autoreturn
            self.segnatura.delete(0, tk.END)
            self.segnatura.insert(0, label[:7])

        def ck(myentry):
            if myentry.get().isdigit():
                return int(myentry.get())
            else:
                return 0

        def genera_struttura():
            codexid = self.segnatura.get()
            targets = ck(self.targets)
            tagli = ck(self.tagli)
            self.loaded = False
            if os.path.exists(codexid):
                messagebox.showwarning(
                    title="Struttura già esistente.",
                    message="La struttura è già esistente",
                )
                return False
            print("Struttura creata: %s" % codexid)
            os.mkdir(codexid)
            data = {
                "targets": targets,
                "tagli": tagli,
                "glass": self.glass.get(),
                "black_background": self.black_background.get(),
                "white_background": self.white_background.get(),
                "target_in_scene": self.target_in_scene.get(),
            }

            with open(self.session_path, "w") as outfile:
                json.dump(data, outfile, indent=2)

            folders = ["Recto", "Dorso e tagli", "Target", "Verso", "Inserti"]
            for folder in folders:
                os.mkdir(os.path.join(codexid, folder))

        # WIDGETS:

        B = tk.Button(self.win, text="Genera struttura", command=genera_struttura)

        B.grid(row=4, column=1)

        BQ = tk.Button(self.win, text="Acquisici codice QR", command=QRsegn)
        BQ.grid(row=4, column=0)

        C = tk.Button(self.win, text="Carica lista acquisizioni", command=carica_lista)

        C.grid(row=4, column=2)

        # Caricato
        self.tk_CSV = tk.StringVar()
        self.tk_CSV.set("CSV:🔴")
        labcp = tk.Label(self.win, textvariable=self.tk_CSV, font=("Helvetica", 20))
        labcp.grid(row=4, column=3)
        # CONTATORI
        # Luce

        # Tagli
        self.tk_varta = tk.StringVar()
        self.tk_varta.set("Tagli")
        labt = tk.Label(
            self.win, textvariable=self.tk_varta, font=("Helvetica", size)
        )  # bg='#40E0D0', fg='#FF0000',
        labt.place(x=20, y=220)
        # Recti
        self.tk_varr = tk.StringVar()
        self.tk_varr.set("Recto")
        labr = tk.Label(
            self.win, textvariable=self.tk_varr, font=("Helvetica", size)
        )  # bg='#40E0D0', fg='#FF0000',
        labr.place(x=20, y=270)
        # Versi
        self.tk_varv = tk.StringVar()
        self.tk_varv.set("Versi")
        labv = tk.Label(
            self.win, textvariable=self.tk_varv, font=("Helvetica", size)
        )  # bg='#40E0D0', fg='#FF0000',
        labv.place(x=20, y=320)
        # Target
        self.tk_vartg = tk.StringVar()
        self.tk_vartg.set("Targets")
        labtg = tk.Label(self.win, textvariable=self.tk_vartg, font=("Helvetica", size))
        labtg.place(x=20, y=170)
        # Progresso
        self.tk_varcp = tk.StringVar()
        self.tk_varcp.set("Completezza:")
        labcp = tk.Label(self.win, textvariable=self.tk_varcp, font=("Helvetica", size))
        labcp.place(x=20, y=420)
        tk.Checkbutton(self.win, text="vetro", variable=self.glass).grid(
            row=3, column=0
        )
        tk.Checkbutton(
            self.win, text="sfondo nero", variable=self.black_background
        ).grid(row=3, column=1)
        tk.Checkbutton(
            self.win, text="sfondo bianco", variable=self.white_background
        ).grid(row=3, column=2)
        tk.Checkbutton(
            self.win, text="target in scene", variable=self.target_in_scene
        ).grid(row=3, column=3)
        # LIGHT



        # Updated
        self.updater()
        self.win.mainloop()

    def updater(self):
        def ck(myentry):
            if myentry.get().isdigit():
                return int(myentry.get())
            else:
                return 0

        if self.segnatura.get() != self.old_segnatura:
            self.loaded = False
        self.old_segnatura = self.segnatura.get()
        self.session_path = os.path.join(
            os.getcwd(), self.segnatura.get(), "session.json"
        )
        self.ctr += 1
        if not self.loaded:
            if os.path.exists(self.session_path):
                with open(self.session_path) as json_file:
                    data = json.load(json_file)
                    self.targets.delete(0, tk.END)
                    self.targets.insert(0, data["targets"])
                    self.tagli.delete(0, tk.END)
                    self.tagli.insert(0, data["tagli"])
            carica_lista(self)

        tagli = ck(self.tagli)
        targets = ck(self.targets)
        # numero di acquisizione nella cartella

        def get_ident(listOfAcquisitions, cr):

            numaqu = len(listOfAcquisitions)
            ident = ""
            hint = ""
            if numaqu > cr:
                row = listOfAcquisitions[cr]
                desc = row["descrizione"]
                tipo = row["tipo"]
                elemento = row["elemento"]
                sottoelemento = row["sottoelemento"]
                numerazione = row["numerazione_A"]
                if numerazione != "":
                    numerazione = "(%s)" % numerazione
                ident = f"{desc} {tipo}{elemento}{sottoelemento}{numerazione}"
            elif cr == numaqu:
                hint = "✅"
            elif cr > numaqu:
                more = cr - numaqu
                if more > 1:
                    hint = "⚠️ %s acquisizioni" %more
                else:
                    hint = "⚠️ Un'acquisizione in più."
                
            return numaqu, ident, hint
        fileFormat = self.fileFormat.get()
        cr = get_dir(os.path.join(self.segnatura.get(), "Recto"),fileFormat)
        numrecto, ident, hint = get_ident(self.recto, cr)
        self.tk_varr.set("Recto: %s/%s Corrente: %s %s" % (cr, numrecto, ident, hint))
        cr2 = get_dir(os.path.join(self.segnatura.get(), "Verso"),fileFormat)
        numverso, ident2, hint2 = get_ident(list(reversed(self.verso)), cr2)
        try:
            _, ident2r, hint2r = get_ident(list(reversed(self.recto)), cr2-1)
        except IndexError:
            ident2r, hint2r = "",""
        self.tk_varv.set(
            f"Verso: {cr2}/{numverso} Corrente: {ident2} {hint2} \n (recto {ident2r} {hint2r})"
        )
        cr3 = get_dir(os.path.join(self.segnatura.get(), "Target"),fileFormat)
        self.tk_vartg.set("Target: %s/%s Corrente: %s" % (cr3, targets, cr3 + 1))
        cr4 = get_dir(os.path.join(self.segnatura.get(), "Dorso e tagli"),fileFormat)
        self.tk_varta.set("Tagli: %s/%s Corrente: %s" % (cr4, tagli, cr4 + 1))
        acqu_tot = len(self.verso) + len(self.recto) + tagli + targets
        tot_now = cr + cr2 + cr3 + cr4
        prc = tot_now / acqu_tot * 100
        self.tk_varcp.set("Completezza: %s/%s  %.1f %%" % (tot_now, acqu_tot, prc))
        self.win.after(1000, self.updater)


UL = UpdateLabel()
