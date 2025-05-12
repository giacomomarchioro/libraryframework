import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import rawpy
import numpy as np
import os
import io
import csv
import subprocess
import hashlib
import os
import json
import datetime
import sys

rawformat = ".nef"

# Initialize the image index
index = 0
rectos = []
versos = []
path = ""
versoRotation = -1
rectoRotation = 1
rectosMD = None
versosMD = None
RENAMED = False
EXPORTED = False


def rename(FolderPath,test=True,configurazione="aVISNMV",fileFormat = ".nef",verobose=False):
    def isImage(filename):
        return filename.endswith(fileFormat) and not filename.startswith(".")

    csvFiles = [ i for i in os.listdir(FolderPath) if not i.startswith(".") and i.endswith(".csv")]
    assert len(csvFiles) == 1, "Found multiple csv files in the folder"
    csvFileName = csvFiles[0]
    numero_codice = "ASVr_UR_"+os.path.basename(FolderPath)+"_"
    nomiRecto = []
    nomiVerso = []



    def create_name(identification,
                    elementType,
                    element,
                    subelement,
                    disambiguator,
                    configuration,
                    counter,
                    fileFormat):
        # BCVRm1853_0_x0001r0001r__aVISPKV00.jp2
        assert len(identification) < 13, "Folder name should not exceed 13 characters was %s" %identification
        if len(identification) == 11:
            identification = identification + "_"
        dis = "__"
        if disambiguator != "":
            dis = disambiguator.zfill(2)
        idPagina = f"{element.zfill(4)}{subelement}"*2
        fileNamesParts = [
            identification,
            elementType,
            idPagina,
            dis,
            configuration,
            counter,
            fileFormat
        ]
        imageName = "".join(fileNamesParts)
        assert len(imageName) == 38, "Image name should have 38 characters. was %s" %imageName
        return imageName

    with open(os.path.join(FolderPath,csvFileName)) as f:
        csvDicts = csv.DictReader(f)
        # skip the first line is the dorso.
        next(csvDicts)
        for csvDict in csvDicts:
            tipo = csvDict['tipo']
            elemento = csvDict['elemento']
            sottoElemento = csvDict['sottoelemento']
            disambiguatore = csvDict['disambiguatore']
            name = create_name(numero_codice,
                            tipo,
                            elemento,
                            sottoElemento,
                            disambiguatore,
                            configuration=configurazione,
                            counter="00",
                            fileFormat=fileFormat
                            )
            if sottoElemento == "r":
                nomiRecto.append(name)
            elif sottoElemento == "v":
                nomiVerso.append(name)
            else:
                raise ValueError("No recto verso indication found.")
    logging = []

    def renameImage(folderPath,fileName,newFileName):
        org = os.path.join(folderPath,fileName)
        new = os.path.join(folderPath,newFileName)
        if test:
            print(folderPath)
            message ="->".join((fileName,newFileName))
            logging.append((folderPath,message))
            print(message)
            print("---")
        else:
            os.rename(org,new)
            with open(os.path.join(path,"renamelist.txt"),"a") as f:
                f.write("->".join((org,newFileName))+"\n")



    # RECTO
    rect_p = os.path.join(FolderPath,'Recto')
    imgs_recto = sorted([i for i in os.listdir(rect_p) if isImage(i)])
    for ind,i in enumerate(imgs_recto):
        renameImage(rect_p,i,newFileName=nomiRecto[ind])

    # VERSO
    ver_p = os.path.join(FolderPath,'Verso')
    # il primo è il secondo della serie rovesciato
    imgs_ver = reversed(sorted([i for i in os.listdir(ver_p) if isImage(i)]))
    for ind,i in enumerate(imgs_ver):
        renameImage(ver_p,i,newFileName=nomiVerso[ind])


    det_p = os.path.join(FolderPath,'Dorso e tagli')
    img_det = sorted([i for i in os.listdir(det_p) if isImage(i)])
    dorso = True # il prossimo sarà il dorso
    count = 1
    for fname in img_det:
        # il dorso (prima immagine) la poniamo a zero
        org = os.path.join(det_p,fname)
        if dorso:
            newName = create_name(numero_codice,
                        elementType="d",
                        element="0",
                        subelement="r",
                        disambiguator="__",
                        configuration=configurazione,
                        counter="00",
                        fileFormat=fileFormat
                        )
            dorso = False
        else:
            newName = create_name(numero_codice,
                elementType="y",
                element=str(count),
                subelement="_",
                disambiguator="__",
                configuration=configurazione,
                counter="00",
                fileFormat=fileFormat
                )
            count +=1
        renameImage(det_p,fname,newFileName=newName)


    tg_p = os.path.join(FolderPath,'Target')
    imgs_tg = sorted([i for i in os.listdir(tg_p) if isImage(i)])
    count = 0
    for k in imgs_tg:
        newName = create_name(numero_codice,
        elementType="z",
        element=str(count),
        subelement="_",
        disambiguator="__",
        configuration=configurazione,
        counter="00",
        fileFormat=fileFormat
        )
        count+=1
        renameImage(tg_p,k,newFileName=newName)
    print("RENAMED %s" %test)


def exportJPEG(folderPath):
    lastPart = os.path.basename(os.path.normpath(folderPath))
    outputFolderPath = os.path.join(folderPath, lastPart)
    if not os.path.exists(outputFolderPath):
        os.mkdir(outputFolderPath)
    rawTherapeePath = r"C:\Program Files\RawTherapee\5.9\rawtherapee-cli.exe"
    versoPP3File = r"E:\UFFICIO DEL REGISTRO\verso.pp3"
    rectoPP3File = r"E:\UFFICIO DEL REGISTRO\recto.pp3"
    tagliPP3File = r"E:\UFFICIO DEL REGISTRO\tagli.pp3"

    commands = [
        [rawTherapeePath, "-p", versoPP3File, "-j70", "-o", outputFolderPath, "-c", f"{folderPath}\\Verso"],
        [rawTherapeePath, "-p", rectoPP3File, "-j70", "-o", outputFolderPath, "-c", f"{folderPath}\\Recto"],
        [rawTherapeePath, "-p", tagliPP3File, "-j70", "-o", outputFolderPath, "-c", f"{folderPath}\\Dorso e tagli"],
        [rawTherapeePath, "-p", rectoPP3File, "-j70", "-o", outputFolderPath, "-c", f"{folderPath}\\Target"]
    ]
    print(outputFolderPath)

    for index, command in enumerate(commands):
        print(f"Executing command {index + 1}: {' '.join(command)}")
        subprocess.run(command)

def checkIntegrity():
    ROOT_PATH = path
    cpt = sum([len(files) for r, d, files in os.walk(ROOT_PATH)])
    data_structure = dict()
    CheckSum_label.config(text='Checksum: calculating ... ')
    def updt(total, progress):
        """
        Displays or updates a console progress bar.

        Original source: https://stackoverflow.com/a/15860757/1391441
        """
        barLength, status = 20, ""
        progress = float(progress) / float(total)
        if progress >= 1.:
            progress, status = 1, "\r\n"
        block = int(round(barLength * progress))
        text = "\r[{}] {:.0f}% {}".format(
            "#" * block + "-" * (barLength - block), round(progress * 100, 0),
            status)
        sys.stdout.write(text)
        sys.stdout.flush()

    data_structure['original_folder'] = ROOT_PATH
    data_structure['date'] = str(datetime.datetime.now())
    data_structure['algorithm'] = "sha256 from haslib Python library"
    data_structure['checksums'] = dict()

    # General-purpose solution that can process large files
    def file_hash(file_path):
        # https://stackoverflow.com/questions/22058048/hashing-a-file-in-python

        sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            while True:
                data = f.read(65536) # arbitrary number to reduce RAM usage
                if not data:
                    break
                sha256.update(data)

        return sha256.hexdigest()


    def compare_dicts(d1, d2, path=""):
        differences = {}
        for key in d1.keys() | d2.keys():
            new_path = f"{path}.{key}" if path else key
            if key not in d1:
                differences[new_path] = ("Key not in dict1", d2[key])
            elif key not in d2:
                differences[new_path] = (d1[key], "Key not in dict2")
            else:
                if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                    differences.update(compare_dicts(d1[key], d2[key], new_path))
                elif d1[key] != d2[key]:
                    differences[new_path] = (d1[key], d2[key])
        return differences

    print("Computing hash for each file")

    elementCnt = [1]
    def createFolderStructure(path,datalevel):
        elem = [i for i in os.listdir(path) if not i.startswith(".")]
        for i in elem:
            new_path = os.path.join(path,i)
            if os.path.isdir(new_path):
                datalevel[i] = dict()
                createFolderStructure(new_path,datalevel[i])
            else:
                datalevel[i] = file_hash(new_path)
            updt(cpt,elementCnt[0])
            elementCnt[0]+=1
    hash_file = os.path.join(ROOT_PATH,"checksums.json")
    if os.path.exists(hash_file):
        createFolderStructure(ROOT_PATH,data_structure['checksums'])
        with open(hash_file, "r") as f:
            previous_data_structure = json.load(f)
        del data_structure['checksums']["checksums.json"]
        if previous_data_structure['checksums'] != data_structure['checksums']:
            differences = compare_dicts(previous_data_structure['checksums'],data_structure['checksums'])
            print("DETECTED DIFFERENCES!!")
            print(differences)
            CheckSum_label.config(text='Checksum: difference detected!')

        else:
            print("OK")
            CheckSum_label.config(text='Checksum: ✓ verified')

    else:
        with open(hash_file, "w") as f:
            createFolderStructure(ROOT_PATH,data_structure['checksums'])
            del data_structure['checksums']["checksums.json"]
            json.dump(data_structure,f,indent=2)
            CheckSum_label.config(text='Checksum: ✓ written to disk.')


# Function to load and process images
def load_images(index):
    try:
        imr = rawpy.imread(os.path.join(path, "Recto", rectos[index]))
        imv = rawpy.imread(os.path.join(path, "Verso", versos[index]))
        if useRaw.get():
            img1 = np.rot90(imv.raw_image[::10, ::10],versoRotation)
            img2 = np.rot90(imr.raw_image[::10, ::10],rectoRotation)

            # Normalize and convert to 8-bit for display
            img1 = ((img1 / 2**13) * 255).astype(np.uint8)
            img2 = ((img2 / 2**13) * 255).astype(np.uint8)

            # Convert numpy arrays to Image objects
            img1 = Image.fromarray(img1)
            img2 = Image.fromarray(img2)
        else:
            img1 = Image.open(io.BytesIO(imv.extract_thumb().data))
            img2 = Image.open(io.BytesIO(imr.extract_thumb().data))

            # zoomed detailed
            xCenter = int(img1.size[0]/2)
            yCenter = int(img1.size[1]/2)
            det1 = img1.crop((xCenter, yCenter, xCenter+100, yCenter+100))
            det1 = det1.rotate(90*versoRotation,expand=1)
            xCenter2 = int(img2.size[0]/2)
            yCenter2 = int(img2.size[1]/2)
            det2 = img2.crop((xCenter2, yCenter2, xCenter2+100, yCenter2+100))
            det2 = det2.rotate(90*versoRotation,expand=1)
            # resized
            base_width = 800
            # img1
            wpercent = (base_width / float(img1.size[0]))
            hsize = int((float(img1.size[1]) * float(wpercent)))
            img1 = img1.resize((base_width, hsize), Image.Resampling.LANCZOS)
            # img2
            wpercent = (base_width / float(img2.size[0]))
            hsize = int((float(img2.size[1]) * float(wpercent)))
            img2 = img2.resize((base_width, hsize), Image.Resampling.LANCZOS)

            img1 = img1.rotate(90*versoRotation,expand=1)
            img2 = img2.rotate(90*rectoRotation,expand=1)
        # Convert Image objects to ImageTk objects
        imgtk1 = ImageTk.PhotoImage(image=img1)
        imgtk2 = ImageTk.PhotoImage(image=img2)
        # details 
        det1Tk1 = ImageTk.PhotoImage(image=det1)
        label1det.config(image=det1Tk1)
        label1det.image = det1Tk1
        det2Tk1 = ImageTk.PhotoImage(image=det2)
        label1det2.config(image=det2Tk1)
        label1det2.image = det2Tk1
        # Update the labels with the new images
        label1.config(image=imgtk1)
        label1.image = imgtk1
        label2.config(image=imgtk2)
        label2.image = imgtk2
        # Update titles (if needed)
        rectoMD = rectosMD[index] if rectosMD is not None else ""
        versoMD = versosMD[index] if versosMD is not None else ""
        label1_title.config(text=f"{index+1}v {versos[index]} {versoMD}")
        label2_title.config(text=f"{index+2}r {rectos[index]} {rectoMD}")

    except IndexError:
        print("Index out of range")

def set_path():
    global rectos
    global versos
    global path
    global rectosMD
    global versosMD
    global RENAMED
    global EXPORTED
    global index
    index = 0
    RENAMED = False
    EXPORTED = False
    path = filedialog.askdirectory()
    try:
        if os.path.exists(os.path.join(path,"renamelist.txt")):
            print("ALREADY RENAMED")
            rectos = sorted([i for i in os.listdir(os.path.join(path, "Recto")) if i.endswith(rawformat)])[1:]  # Skip the first recto
            versos = [i for i in os.listdir(os.path.join(path, "Verso")) if i.endswith(rawformat)][:-1]  # Skip the last verso
            RENAMED = True
            ExportStatus_label.config(text="Rename ✓ JPEG  ❌")
            if os.path.exists(os.path.join(path,"FolderStructure.txt")):
                ExportStatus_label.config(text="Rename ✓ JPEG ✓")

        else:
            rectos = sorted([i for i in os.listdir(os.path.join(path, "Recto")) if i.endswith(rawformat)])[1:]  # Skip the first recto
            versos = list(reversed([i for i in os.listdir(os.path.join(path, "Verso")) if i.endswith(rawformat)][1:]))  # Skip the last verso
        slider.config(to=len(rectos)-1)
        # Load the first pair of images
        load_images(index)
        root.title(f"Image viewer {path}")
        try:
            csvList = [i for i in os.listdir(os.path.join(path)) if i.endswith(".csv")]
            with open(os.path.join(path,csvList[0])) as f:
                data = csv.DictReader(f)
                records = [" ".join((i['descrizione'],i['elemento'],i['tipo'],i['numerazione_A'],i['numerazione_B'],i['numerazione_C'])) for i in data]
            rectosMD = records[3::2]
            versosMD = records[1:-1:2]
            status_label.config(text="Folder: ✓ CSV: ✓ ")
        except:
            status_label.config(text="Folder: ✓ CSV:❌ ")
    except FileNotFoundError:
        status_label.config(text="❌")

# Callback function for the button
def on_next_image():
    global index
    if index < len(rectos) - 1:
        index += 1
        load_images(index)
        slider.set(index)

def on_previous_image():
    global index
    if index > 0:
        index -= 1
        load_images(index)
        slider.set(index)

def on_10next_image():
    global index
    if index < len(rectos) - 1:
        index += 10
        load_images(index)
        slider.set(index)

def on_10previous_image():
    global index
    if index > 0:
        index -= 10
        load_images(index)
        slider.set(index)

def go_to_image(val):
    global index
    index = int(val)
    load_images(index)
    slider.set(index)

def go_to_the_end():
    global index
    index = len(rectos)
    load_images(index)
    slider.set(index)

# Create the main window
root = tk.Tk()
root.title("Image Viewer")
useRaw = tk.BooleanVar()

# Set the window to take the full screen
root.state('zoomed')

# Left side for buttons and controls
button_frame = ttk.Frame(root)
button_frame.grid(row=0, column=0, rowspan=5, sticky='ns', padx=10, pady=10)

# Create and grid the buttons in the button_frame
path_button = ttk.Button(button_frame, text="Select Path", command=set_path)
path_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

status_label = ttk.Label(button_frame, text="❌")
status_label.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

prev_button = ttk.Button(button_frame, text="Previous Image", command=on_previous_image)
prev_button.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

next_button = ttk.Button(button_frame, text="Next Image", command=on_next_image)
next_button.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

prev10_button = ttk.Button(button_frame, text="Previous 10 Images", command=on_10previous_image)
prev10_button.grid(row=4, column=0, padx=5, pady=5, sticky='ew')

next10_button = ttk.Button(button_frame, text="Next 10 Images", command=on_10next_image)
next10_button.grid(row=5, column=0, padx=5, pady=5, sticky='ew')

goend_button = ttk.Button(button_frame, text="Go to the end", command=go_to_the_end)
goend_button.grid(row=6, column=0, padx=5, pady=5, sticky='ew')



slider = tk.Scale(button_frame, from_=0, to=len(rectos)-1, orient=tk.HORIZONTAL, command=go_to_image, label="Folio:")
slider.grid(row=7, column=0, padx=5, pady=5, sticky='ew')

def rotateVerso():
    global versoRotation
    versoRotation +=1
    load_images(index)

def rotateRecto():
    global rectoRotation
    rectoRotation +=1
    load_images(index)

button = ttk.Button(button_frame, text='⟲ verso', command=rotateVerso).grid(row=8, column=0, padx=5, pady=5, sticky='ew')
button = ttk.Button(button_frame, text='⟲ recto', command=rotateRecto).grid(row=9, column=0, padx=5, pady=5, sticky='ew')

path_label = ttk.Label(button_frame, text=path)
path_label.grid(row=7, column=0, padx=5, pady=5, sticky='ew')

useRawBtn = tk.Checkbutton(button_frame, text='Use RAW',variable=useRaw, onvalue=True, offvalue=False).grid(row=10, column=0, padx=5, pady=5, sticky='ew')

ExportStatus_label = ttk.Label(button_frame, text="Rename ❌ JPEG  ❌")
ExportStatus_label.grid(row=17, column=0, padx=5, pady=5, sticky='ew')
CheckSum_label = ttk.Label(button_frame, text="Checksum ❌")
CheckSum_label.grid(row=18, column=0, padx=5, pady=5, sticky='ew')

def renameFiles():
    global rectos
    global versos
    global RENAMED
    if not RENAMED:
        try:
            rename(path)
        except Exception as e:
            ExportStatus_label.config(text="Rename ⚠️ JPEG  ❌")
            print("RENAMED FAILED!")
            print(e)
            return
        rename(path,test=False)
        rectos = sorted([i for i in os.listdir(os.path.join(path, "Recto")) if i.endswith(rawformat)])[1:]  # Skip the first recto
        versos = [i for i in os.listdir(os.path.join(path, "Verso")) if i.endswith(rawformat)][:-1]  # Skip the last verso
        RENAMED = True
        ExportStatus_label.config(text="Rename ✓ JPEG  ❌")
        load_images(index)
    else:
        messagebox.showerror("showerror","File già rinominati.")


def generateFolderStructure():
    with open(os.path.join(path,"FolderStructure.txt"), 'w') as file:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            file.write(f"{item}\n")  # Write the name of the item (file/folder)

            # If the item is a directory, inspect its contents
            if os.path.isdir(item_path):
                for subitem in os.listdir(item_path):
                    subitem_path = os.path.join(item_path, subitem)

                    # Check if the subitem is a directory
                    if os.path.isdir(subitem_path):
                        # Count files in the subdirectory
                        n_files = len([f for f in os.listdir(subitem_path) if os.path.isfile(os.path.join(subitem_path, f))])
                        file.write(f"-  {subitem}  {n_files}\n")


def export():
    if RENAMED:
        exportJPEG(path)
        generateFolderStructure()
        ExportStatus_label.config(text="Rename ✓ JPEG  ✓")
        EXPORTED=True
        checkIntegrity()
    else:
        messagebox.showerror("showerror","Rinominare i file prima di esportarli!")

buttonRen = ttk.Button(button_frame, text='⚠️RENAME⚠️', command=renameFiles,).grid(row=14, column=0, padx=5, pady=5, sticky='ew')
buttonExp = ttk.Button(button_frame, text='⚠️EXPORT⚠️', command=export,).grid(row=15, column=0, padx=5, pady=5, sticky='ew')
buttonChkS = ttk.Button(button_frame, text='Checksum generate/verify', command=checkIntegrity,).grid(row=16, column=0, padx=5, pady=5, sticky='ew')



# detailslabel
label1det = ttk.Label(button_frame)
label1det.grid(row=11, column=0, padx=5, pady=5, sticky='nsew')
label1det2 = ttk.Label(button_frame)
label1det2.grid(row=12, column=0, padx=5, pady=5, sticky='nsew')



# Right side for images
image_frame = ttk.Frame(root)
image_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)


def copy_to_clipboard1(event):
    root.clipboard_clear()
    error = f"Errore tra {label1_title.cget('text')} e {label2_title.cget('text')}." 
    root.clipboard_append(error)

# Titles above images
label1_title = ttk.Label(image_frame, text="1v")
label1_title.grid(row=0, column=0, padx=5, pady=5)
label1_title.bind("<Double-1>", copy_to_clipboard1)


label2_title = ttk.Label(image_frame, text="2r")
label2_title.grid(row=0, column=1, padx=5, pady=5)
label2_title.bind("<Double-1>", copy_to_clipboard1)


# Labels to display images
label1 = ttk.Label(image_frame)
label1.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

label2 = ttk.Label(image_frame)
label2.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

# Make the grid cells expand with window resizing
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)
image_frame.grid_columnconfigure(0, weight=1)
image_frame.grid_columnconfigure(1, weight=1)
image_frame.grid_rowconfigure(1, weight=1)

# Start the main loop
root.mainloop()
