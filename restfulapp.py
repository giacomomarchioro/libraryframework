from flask import Flask
from flask_restful import Resource, Api
import xml.etree.ElementTree as gfg
from xml.etree import ElementTree

root = gfg.Element("Catalog") 
  
m1 = gfg.Element("mobile") 
root.append (m1) 
  
b1 = gfg.SubElement(m1, "brand") 
b1.text = "Redmi"
b2 = gfg.SubElement(m1, "price") 
b2.text = "6999"
  
m2 = gfg.Element("mobile") 
root.append (m2) 
  
c1 = gfg.SubElement(m2, "brand") 
c1.text = "Samsung"
c2 = gfg.SubElement(m2, "price") 
c2.text = "9999"
  
m3 = gfg.Element("mobile") 
root.append (m3) 
  
d1 = gfg.SubElement(m3, "brand") 
d1.text = "RealMe"
d2 = gfg.SubElement(m3, "price") 
d2.text = "11999"
  
tree = gfg.ElementTree(root) 


app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    @api.representation('application/xml')
    def get(self):
        return ElementTree.tostring(root)

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
