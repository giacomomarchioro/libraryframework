#https://iiif.io/api/presentation/3.0/#b-example-manifest-response
import sys
import glob
from IIIFpres import iiifpapi3
import pandas as pd
from subprocess import check_output

iiifpapi3.BASE_URL = "https://example.org/iiif/book1"

data = pd.read_csv("lista manoscritti - Versione_con_aggiunte.csv")
data.loc[data['numero_del_codice'].isin(['IX'])]

folder = sys.argv[2]

manifest = buildManifest(manifest, folder, config)
images = [image for image in glob.glob(folder+"/*.jp2")]
if len(images) != 0:
    ic = 1
    for image in sorted(images):
        canvas = copy.deepcopy(canvas_template)
        manifest = addCanvasToManifest(manifest,canvas,config,image,ic)
        ic = ic +1
    filename = "presentationapi/manifests/"+id+".json"
    print("writing: "+filename)
    with open(filename, 'w') as outfile:
        json.dump(manifest, outfile, sort_keys=True, indent=4, separators=(',', ': '))

    out = check_output(["exiftool", image])
    Metadata = dict((e[:32].strip(),e[33:].strip()) for e in out.decode('utf8').split('\n'))
    width = Metadata['Image Width']
    height = Metadata['Image Height']
manifest = iiifpapi3.Manifest()
manifest.set_id(extendbase_url="manifest")
manifest.add_label("en","Book 1")
manifest.add_metadata(label="Author",value="Anne Author",language_l="en")
# more complex entry can be mapped directly to a dictionary and inserted using entry arguments
entry = {
        "label": { "en": [ "Published" ] },
        "value": {
        "en": [ "Paris, circa 1400" ],
        "fr": [ "Paris, environ 1400" ]
        }
        }
manifest.add_metadata(entry=entry)
manifest.add_metadata(label="Notes",value=["Text of note 1","Text of note 2"],language_l="en",language_v="en")
manifest.add_metadata(label="Source",value="<span>From: <a href=\"https://example.org/db/1.html\">Some Collection</a></span>",language_l="en", language_v="none")
manifest.add_summary("Book 1, written be Anne Author, published in Paris around 1400.",language="en")
manifest.add_behavior("paged")
manifest.set_navDate("1856-01-01T00:00:00Z")
manifest.set_rights("https://creativecommons.org/licenses/by/4.0/")
manifest.add_requiredStatement(label="Attribution",value="Provided by Example Organization",language_l="en",language_v="en")
prov = manifest.add_provider()
prov.add_label("en","Example Organization")
prov.set_id("https://example.org/about")
homp = prov.add_homepage()
homp.set_id("https://example.org/")
homp.set_type("Text")
homp.add_label("en","Example Organization Homepage")
homp.set_format("text/html")
logo = prov.add_logo()
logo.set_id("https://example.org/service/inst1/full/max/0/default.png")
logo.set_type("Image")
logo.set_format("image/png")
serv1 = logo.add_service()
serv1.set_id("https://example.org/service/inst1")
serv1.set_type("ImageService3")
serv1.set_profile("level2")
seeAl = prov.add_seeAlso()
seeAl.set_id("https://data.example.org/about/us.jsonld")
seeAl.set_type("Dataset")
seeAl.set_format("application/ld+json")
seeAl.set_profile("https://schema.org/")
manifest.add_provider(prov)
homp2 = manifest.add_homepage()
homp2.set_id("https://example.org/info/book1/")
homp2.set_type("Text")
homp2.add_label("en","Home page for Book 1")
homp2.set_format("text/html")
serv2 = manifest.add_service()
serv2.set_id("https://example.org/service/example")
serv2.set_type("ExampleExtensionService")
serv2.set_profile("https://example.org/docs/example-service.html")
sal2 = manifest.add_seeAlso()
sal2.set_id("https://example.org/library/catalog/book1.xml")
sal2.set_type("Dataset")
sal2.set_format("text/xml")
sal2.set_profile("https://example.org/profiles/bibliographic")
ren = manifest.add_rendering()
ren.set_id("https://example.org/iiif/book1.pdf")
ren.set_type("Text")
ren.add_label("en","Download as PDF")
ren.set_format("application/pdf")
po = manifest.add_partOf()
po.set_id("https://example.org/collections/books/")
po.set_type("Collection")
start = iiifpapi3.start()
start.set_id("https://example.org/iiif/book1/canvas/p2")
start.set_type("Canvas")
manifest.set_start(start)
mycomplexserv =  {
      "@id": "https://example.org/iiif/auth/login",
      "@type": "AuthCookieService1",
      "profile": "http://iiif.io/api/auth/1/login",
      "label": "Login to Example Institution",
      "service": [
        {
          "@id": "https://example.org/iiif/auth/token",
          "@type": "AuthTokenService1",
          "profile": "http://iiif.io/api/auth/1/token"          
        }
      ]
    }
manifest.add_services(mycomplexserv)



data = (("p. 1",750,1000, "https://example.org/iiif/book1/page1","/full/max/0/default.jpg","annotation",True),
        ("p. 2",750,1000, "https://example.org/iiif/book1/page2","/full/max/0/default.jpg",False,False),
        )
for idx,d in enumerate(data):
    idx+=1 
    canvas = manifest.add_canvastoitems()
    canvas.set_id(extendbase_url=["canvas","p%s"%idx]) # in this case we use the base url
    canvas.set_height(d[2])
    canvas.set_width(d[1])
    canvas.add_label("none",d[0])
    annopage = canvas.add_annotationpage_to_items()
    annopage.set_id(extendbase_url=["page","p%s"%idx,"1"])
    annotation = iiifpapi3.Annotation(target=canvas.id)
    annotation.set_id(extendbase_url=["annotation","p%s-image"%str(idx).zfill(4)])
    annotation.set_motivation("painting")
    annotation.body.set_id("".join(d[3:-2]))
    annotation.body.set_type("Image")
    annotation.body.set_format("image/jpeg")
    annotation.body.set_width(1500)
    annotation.body.set_height(2000)
    s = iiifpapi3.service()
    s.set_id(d[3])
    s.set_type("ImageService3")
    s.set_profile("level2")
    if d[6]:
        subserv =  {
                "@id": "https://example.org/iiif/auth/login",
                "@type": "AuthCookieService1"
                }
        s.add_service(subserv)
    annotation.body.add_service(s)
    annopage.add_item(annotation)
    canvas.add_item(annopage)
    # if has annotation
    if d[5]:
        annopage2 = iiifpapi3.AnnotationPage()
        annopage2.set_id("https://example.org/iiif/book1/comments/p%s/1" %idx)
        canvas.add_annotation(annopage2)
    
rng = iiifpapi3.Range()
rng.set_id(extendbase_url=["range","r0"])
rng.add_label("en","Table of Contents")
rng2 = iiifpapi3.Range()
rng2.set_id(extendbase_url=["range","r1"])
rng2.add_label("en","Introduction")
rng2.set_supplementary("https://example.org/iiif/book1/annocoll/introTexts")
rng2.add_canvas_to_items("https://example.org/iiif/book1/canvas/p1")
sr = iiifpapi3.SpecificResource()
sr.set_source("https://example.org/iiif/book1/canvas/p2")
fs = iiifpapi3.FragmentSelector()
fs.set_xywh(0,0,750,300)
sr.set_selector(fs)
rng2.add_item(sr)
rng.add_item(rng2)
manifest.add_structure(rng)
annopage3 = iiifpapi3.AnnotationPage()
annopage3.set_id("https://example.org/iiif/book1/page/manifest/1")
anno = iiifpapi3.Annotation(manifest.id)
anno.set_id("https://example.org/iiif/book1/page/manifest/a1")
anno.set_motivation("commenting")
anno.body.set_language("en")
anno.body.set_value("I love this manifest!")
annopage3.add_item(anno)
annopage3.set_id("https://example.org/iiif/book1/page/manifest/1")        
manifest.add_annotation(annopage3)

manifest.json_save("manifest.json")