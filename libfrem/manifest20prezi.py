"""iiif-prezi example code to build a manifest from a directory of images
"""
# http://localhost:1080/iipsrv/iipsrv.fcgi?iiif=/imageapi//m0171_0/m0171_0visn20_0001a21.jp2/info.json
from iiif_prezi.factory import ManifestFactory
import os
import pymongo
import glob 
databaseaddress_capitolare_mongo ="mongodb+srv://giacomo:univr@cluster0.wjdtk.mongodb.net/testcapit?retryWrites=true&w=majority"
client = pymongo.MongoClient(databaseaddress_capitolare_mongo)

folder = "imageapi/m0171_0"
image_dir = os.path.join(os.getcwd(),folder)
segnatura_id = os.path.basename(folder)
var = client.capitolare.codici.find_one({'segnatura_idx': segnatura_id})

prezi_dir = "/tmp"

fac = ManifestFactory()
fac.set_debug("error")
fac.set_base_image_uri(os.path.join("http://lezioni.meneghetti.univr.it//",folder))
fac.set_base_image_dir(image_dir)
fac.set_iiif_image_info()
fac.set_base_prezi_uri("http://lezioni.meneghetti.univr.it//manifests/")
fac.set_base_prezi_dir(prezi_dir)

mflbl = os.path.split(image_dir)[1].replace("_", " ").title()

mfst = fac.manifest(label=mflbl)
seq = mfst.sequence()
listadir = glob.glob(folder+"/*.jp2")
for fn in [i for i in os.listdir(image_dir) if i.endswith('.jp2')]:
    ident = fn[:-4]
    title = ident.replace("_", " ").title()
    cvs = seq.canvas(ident=ident, label=title)
    cvs.add_image_annotation(fn,iiif=True)

mfst.toFile(compact=False)