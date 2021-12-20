# -*- coding: utf-8 -*-
from subprocess import check_output
import glob
import sys
import os 
from IIIFpres import iiifpapi3
from itertools import cycle
from pymongo import MongoClient
#folder = sys.argv[1]
connectionstring = "mongodb+srv://giacomo:univr@cluster0.wjdtk.mongodb.net/testcapit?retryWrites=true&w=majority"
client = MongoClient(connectionstring)
idsegnatura = "m0061_0"
var = client.capitolare.codici.find_one({"segnatura_idx":idsegnatura})
iiifpapi3.BASE_URL = "http://lezioni.meneghetti.univr.it" 
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="%s_iiif30.json" %idsegnatura)
manifest.add_label(None,var['descrizione_esterna'][0]['Segnatura'])
manifest.add_summary('it',var['sommario_desc'])

folder = r"imageapi/LXI"
de = var['descrizione_esterna'][0]
manifest.add_metadata(label='Datazione',value=de['datazione'],language_l='it')
manifest.add_metadata(label='Tipo di supporto e qualità',value=de['tipo_di_supporto_e_qualita'],language_l='it')
manifest.add_metadata(label='Consistenza',value=de['consistenza'],language_l='it')
manifest.add_metadata(label='Carte di guardia' ,value=de['carte_di_guardia' ],language_l='it')
manifest.add_metadata(label='Prospetto fascicolazione',value=de['prospetto_fascicolazione'],language_l='it')
manifest.add_metadata(label='Arrangiamento fogli',value=de['arrangiamento_fogli_gregory'],language_l='it')
manifest.add_metadata(label='Dimensioni',value=de['dimensioni'],language_l='it')
manifest.add_metadata(label='Rigatura',value=de['rigatura'],language_l='it')
manifest.add_metadata(label='Foratura',value=de['foratura'],language_l='it')
manifest.add_metadata(label='Legatura',value=de['legatura'],language_l='it')
manifest.add_metadata(label='Numero di fascicolo',value=de['numero_di_fascicolo'],language_l='it')
manifest.add_metadata(label='Decorazioni',value=de['decorazioni'],language_l='it')
manifest.add_metadata(label='Filigrana',value=de['filigrana'],language_l='it')
manifest.add_metadata(label='Autore della scheda',value=de['utenti_email'],language_l='it')
manifest.add_metadata(label='orchid',value=de['orchid'],language_l='it')
manifest.set_viewingDirection("left-to-right")
manifest.add_behavior("paged")
#manifest.set_navDate(f"{['datazione_i']}-01-01T00:00:00Z")
manifest.set_rights("http://creativecommons.org/licenses/by/4.0/")
manifest.add_requiredStatement(label="Attribution",value="Provided by University of Verona and Biblioteca Capitolare di Verona",language_l="en",language_v="en")
prov = manifest.add_provider()
prov.add_label("it","Università di Verona")
prov.set_id("https://www.univr.it/it/")
prov2 = manifest.add_provider()
prov2.add_label("it","Biblioteca Capitolare di Verona   ")
prov2.set_id("http://bibliotecacapitolare.org/")
homp = prov.add_homepage()
homp.set_id("https://sites.hss.univr.it/laboratori_integrati/laboratorio-lamedan/")
homp.set_type("Text")
homp.add_label("en","Laboratorio integrati - LAboratorio di Studi MEdievale e DANteschi")
homp.set_format("text/html")
logo = prov.add_logo()
logo.set_id("https://cdn.univr.it/o/aol-theme/images/logo-univr-colori-80.png")
logo.set_format("image/png")


images = sorted([image for image in glob.glob(folder+"/*.jp2")])
piatti_e_carte_di_guardia_ant = 4
fogli = 259
piatti_e_carte_di_guardia_post = 4
plabels = ['dorso','piatto anteriore','risguardia anteriore',]
sidesg1 = cycle(('recto','verso'))
for i in range(1,piatti_e_carte_di_guardia_ant+1):
    plabels.append("guardia anteriore %i %s" %(i,next(sidesg1)))
    plabels.append("guardia anteriore %i %s" %(i,next(sidesg1)))

sidesf = cycle(('r','v'))
for i in range(1,fogli+1):
    plabels.append("%i%s" %(i,next(sidesf)))
    plabels.append("%i%s" %(i,next(sidesf)))

sidesg2 = cycle(('r','v'))
for i in range(1,piatti_e_carte_di_guardia_post+1):
    plabels.append("guardia posteriore %i %s" %(i,next(sidesg2)))
    plabels.append("guardia posteriore %i %s" %(i,next(sidesg2)))

post_elements = ['risguardia posteriore', 'piatto posteriore']
for i in post_elements:
    plabels.append(i)
    
for idx,d in enumerate(images):
    manloc = "/manifests/%s" %idsegnatura
    image = d
    canvas = manifest.add_canvas_to_items()
    if plabels[idx] in ['dorso','piatto anteriore']:
        canvas.add_behavior("paged")
    canvas.set_id(extendbase_url=["manifests",idsegnatura,"canvas","p%s"%(idx+1)]) # in this case we use the base url
    out = check_output(["exiftool", image])
    Metadata = dict((e[:32].strip(),e[33:].strip()) for e in out.decode('utf8').split('\n'))
    width = Metadata['Image Width']
    height = Metadata['Image Height']
    canvas.set_height(width)
    canvas.set_width(height)
    canvas.add_label("it",plabels[idx])
    annopage = canvas.add_annotationpage_to_items()
    annopage.set_id(extendbase_url=["manifests",idsegnatura,"page","p%s"%(idx+1),"1"])
    annotation = annopage.add_annotation_to_items(target=canvas.id)
    annotation.set_id(extendbase_url=["manifests",idsegnatura,"annotation","p%s-image"%str(idx+1).zfill(4)])
    annotation.set_motivation("painting")
    annotation.body.set_id(extendbase_url=[image,"/full/max/0/default.jpg"])
    annotation.body.set_type("Image")
    annotation.body.set_format("image/jp2")
    annotation.body.set_width(width)
    annotation.body.set_height(height)
    s = annotation.body.add_service()
    s.set_id(extendbase_url=[image])
    s.set_type("ImageService2")
    s.set_profile("level2")


##
# Creazione degli indici
##
desc_int = var['descrizione_interna']
# assuming them sorted
manifest.structures = []
rng = manifest.add_range_to_structures()
rng.set_id(extendbase_url="range/r")
rng.add_label('it',"Indice")
strdic = {'base':rng}
for ind,di in enumerate(desc_int):
    if len(di['Descrizione_interna_id'].split('.')) == 1:
        parent = 'base'
        url = str(di['Descrizione_interna_id'])
        nested = False
    else:
        # abbiamo una sotto descrizione
        parent = ".".join(di['Descrizione_interna_id'].split('.')[:-1])
        url = "/".join(di['Descrizione_interna_id'].split('.'))
        nested = True
    strdic[di['Descrizione_interna_id']] = strdic[parent].add_range_to_items()
    strdic[di['Descrizione_interna_id']].set_id(extendbase_url="/".join(["range/r",url]))
    lab = di['titolo']
    if lab == '':
        lab = di['rubrica']

    labeltxt= " ".join((di['Descrizione_interna_id'],lab))
    strdic[di['Descrizione_interna_id']].add_label(None,labeltxt)
    if nested:
        startcnv = int(di['incipit_url'].split('&indx=')[-1])
        if ind+1 < len(desc_int): 
            endcnv = int(desc_int[ind+1]['incipit_url'].split('&indx=')[-1])
        else:
            endcnv = int(desc_int[len(desc_int)-1]['incipit_url'].split('&indx=')[-1])
        if startcnv != endcnv:
            for i in range(startcnv,endcnv):
                strdic[di['Descrizione_interna_id']].add_canvas_to_items(manifest.items[i].id)
        else:
            strdic[di['Descrizione_interna_id']].add_canvas_to_items(manifest.items[startcnv].id)
 
manifest.json_save(os.path.join("presentationapi","manifests","%s.json" %idsegnatura))