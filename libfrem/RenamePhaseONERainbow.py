import json
import os

folders = [i for i in os.listdir('processed_images/') if os.path.isdir("processed_images/"+i)]

foldn = os.path.basename(os.getcwd())

if not os.path.exists("tavolaconversione.json"):
    manuscript = foldn
    if len(manuscript) != 7:
        manuscript = "m0000_0"
    entries = dict()
    for fold in folders:
        
        entry =  {
        "locus_a": "0001r",
        "locus_b": "0001r",
        "id_manoscritto":manuscript,
        "disambiguatore":"__",
        "rotazione_senso_orario":0,
        "tipologia":"s"
        }
        entries[fold] = entry
    with open('tavolaconversione.json', 'w') as outfile:
        json.dump(entries, outfile,indent=4)

else:
    with open(foldn+".json") as f, open("tavolaconversione.json") as t: 
        data = json.load(f)
        tavolaconversione = json.load(t)     
    lights = {'Eureka' : 'E'}
    filters = {'No filter':'_',
            'VIS pass':'V',
            'UV pass':'U',
            'Baader+BG38':'B'}

    nameconve = {
                "IRR" : "IRR",
                "VIS" : "VIS",
                "UVR" : "UVR",
                "UVL": "UVL",
                "IRRFC" : "IFC",
                "UVIL" : "UIL",
                "UVRFC" : "UFC" }

    for fold in folders:
        folder_path = os.path.join('processed_images',fold)
        images = [ i for i in os.listdir(folder_path)if i.endswith('.tif')]
        m = tavolaconversione[fold]
        for img in images:
            name, imgformat = img.split('.')
            print(name)
            sdata = next(item for item in data if item["name"] == name)
            if name in nameconve:
                wavelength = nameconve[name]
            else:
                wavelength = sdata['illuminant'].split()[-1]
            source = lights[sdata['light']]
            optfilter = filters[sdata['filter']]
            tipologia = m['tipologia']
            configurazione = f"{tipologia}{wavelength}P{source}{optfilter}"
            #"m0001_0_0001r__aVISNB_00.jp2"
            fname = f"{m['id_manoscritto']}_{m['locus_a']}{m['locus_b']}{m['disambiguatore']}{configurazione}10.{imgformat}"
            old_file = os.path.join(folder_path, img)
            new_file = os.path.join(folder_path, fname)
            os.rename(old_file, new_file)
