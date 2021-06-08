#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pip install requests
from __future__ import print_function
import requests
# when you use a proxy you might have to use the original link e.g. "http://localhost:1080/iipsrv/iipsrv.fcgi?iiif=/imageapi//m0171_0/m0171_0visn20_0001a21.jp2/info.json"
iiifimageurl = "http://lezioni.meneghetti.univr.it//imageapi/m0171_0/m0171_0visn20_0001a21.jp2/info.json" 
imageinfo =  requests.get(iiifimageurl)
jsoninfo = imageinfo.json()
imgwidth = jsoninfo['width']
imgheight = jsoninfo['height']


import pymongo
import glob
import base64
import json
import cv2
import glob
import hashlib
import copy
import subprocess
import sys
from PIL import Image
from subprocess import check_output
import os 

folder = sys.argv[1]
image_dir = os.path.join(os.getcwd(),folder)
segnatura_id = os.path.basename(os.path.dirname(folder))
databaseaddress_capitolare_mongo ="mongodb+srv://giacomo:univr@cluster0.wjdtk.mongodb.net/testcapit?retryWrites=true&w=majority"
client = pymongo.MongoClient(databaseaddress_capitolare_mongo)
var = client.capitolare.codici.find_one({'segnatura_idx': segnatura_id})





def buildManifest(manifest,folder,config):
    uri = config['baseurl']+"/manifests/"+id+".json"
    manifest['@id'] = uri
    manifest['label'] = folder.split('/')[1].replace('_',' ')
    manifest['attribution'] = "Biblioteca Captiolare di Verona, digitalizzato dall'Università degli studi di Verona"
    manifest['description'] = config['description']
    manifest['sequences'][0]['@id'] = uri+"/sequence/1"
    manifest['metadata'].append( { 'label' : 'Digitalizzato da:' , 'value' : "Università degli studi di Verona" } )
    return manifest

def addCanvasToManifest(manifest,canvas,config,image,ic):
    uri = manifest['@id']
    # set IDs
    canvas['@id'] = uri+"/canvas/%d" % ic
    canvas['images'][0]['@id'] = uri+"/image/%d" % ic
    canvas['images'][0]['resource']['@id'] = uri+"/resource/%d" % ic
    # linke IDs
    canvas['images'][0]['on'] = canvas['@id']
    print(folder)
    print(image)
    # set image dimensions
    # output = subprocess.check_output(["./get_image_dim.sh", image[:-5]])
    # width, height = [int(v) for v in output.strip().split('x')]
    #im=Image.open(image[:-5])
    #width=im.size[0]
    #height=im.size[1]
    #out = check_output(["exiftool", image])
    #Metadata = dict((e[:32].strip(),e[33:].strip()) for e in out.decode('utf8').split('\n'))
    #width = Metadata['Image Width']
    #height = Metadata['Image Height']
    
    iiifimageurl = r"http://localhost:1080/iipsrv/iipsrv.fcgi?iiif=/imageapi//"+folder+"/"+image+"/info.json"
    imageinfo =  requests.get(iiifimageurl)
    jsoninfo = imageinfo.json()
    width = jsoninfo['width']
    height = jsoninfo['height']
    
    canvas['width'] = width
    canvas['images'][0]['resource']['width'] = width
    canvas['height'] = height
    canvas['images'][0]['resource']['height'] = height
    # set license
    canvas['images'][0]['license'] = config['license']
    # set labels
    label = image.split('/')[1].replace('_',' ')
    canvas['label'] = ic
    canvas['images'][0]['resource']['label'] = label
    # set service
    try:
        canvas['images'][0]['resource']['service']['@id'] = config['baseurl']+"/"+image
    except UnicodeDecodeError:
        canvas['images'][0]['resource']['service']['@id'] = config['baseurl']+"/"+image.decode('utf-8')
    # append canvas to manifest
    manifest['sequences'][0]['canvases'].append(canvas)
    print("done")
    return manifest

with open('config.json', 'r') as f:
    config = json.load(f)

with open('manifest_template.json', 'r') as f:
    manifest_template = json.load(f)

with open('canvas_template.json', 'r') as f:
    canvas_template = json.load(f)

manifest = copy.deepcopy(manifest_template)
id = hashlib.md5(folder.encode()).hexdigest()
manifest = buildManifest(manifest, folder, config)
images = [image for image in glob.glob(folder+"/*.jp2")]
if len(images) != 0:
    ic = 1
    for image in sorted(images):
        canvas = copy.deepcopy(canvas_template)
        manifest = addCanvasToManifest(manifest,canvas,config,image,ic)
        ic = ic +1
    filename = "presentationapi/manifests/"+segnatura_id+"_iiif21.json"
    print("writing: "+filename)
    with open(filename, 'w') as outfile:
        json.dump(manifest, outfile, sort_keys=True, indent=4, separators=(',', ': '))
