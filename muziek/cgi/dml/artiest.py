# zoek een artiest met naam en geeft het id terug of andersom
import os
import shutil
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
import _globals
artiestenfile = os.path.join(_globals.xmlpad, "Artiesten.xml")

class ZoekopNaam(ContentHandler):
    def __init__(self, naam):
        self.search_naam = naam
        self.founditem = 0

    def startElement(self, name, attrs):
        if name == 'artiest':
            naam = attrs.get('naam', None)
            if naam == self.search_naam:
                self.founditem = 1
                self.id = attrs.get('id', None)
                self.sort = attrs.get('sort', None)

class ZoekopId(ContentHandler):
    def __init__(self, id):
        self.search_id = id
        self.founditem = 0

    def startElement(self, name, attrs):
        if name == 'artiest':
            id = attrs.get('id', None)
            if id == self.search_id:
                self.founditem = 1
                self.naam = attrs.get('naam', None)
                self.sort = attrs.get('sort', None)

class ZoekNamen(ContentHandler):
    def __init__(self):
        self.namenlijst = []

    def startElement(self, name, attrs):
        if name == 'artiest':
            id = attrs.get('id', None)
            naam = attrs.get('naam', None)
            sort = attrs.get('sort', None)
            self.namenlijst.append((sort, id, naam))

class UpdateArtiest(XMLGenerator):
    "schrijf nieuwe songgegevens weg in XML-document"
    def __init__(self, item):
        self.ah = item
        self.search_item = self.ah.Id
        self.fh = open(self.ah.fn,'w')
        self.founditem = 0
        self.itemfound = 0
        XMLGenerator.__init__(self,self.fh)

    def startElement(self, name, attrs):
    #-- kijk of we met de te wijzigen song bezig zijn
        if name == 'artiest':
            item = attrs.get('id', None)
            if item == str(self.search_item):
                self.founditem = 1
                self.itemfound = 1
    #-- xml element (door)schrijven
        if name == 'artiest':
            id_ = attrs.get('id', None)
            naam = attrs.get('naam', None)
            sort = attrs.get('sort', None)
            if self.founditem == 1:
                id_ = self.ah.id_
                naam = self.ah.naam
                sort = self.ah.sort
            self._out.write('<%s id="%s" naam="%s" sort="%s" />' % (name, id_,
                escape(naam), escape(sort)))
        else:
            XMLGenerator.startElement(self, name, attrs)

    def characters(self,content):
        XMLGenerator.characters(self,content)
#        pass

    def endElement(self, name):
        if name != 'artiest':
            if self.itemfound == 0:
                id_ = self.ah.id_
                naam = self.ah.naam
                sort = self.ah.sort
                self._out.write('<artiest id="%s" naam="%s" sort="%s" />\n' % (id_,
                    escape(naam), escape(sort)))
            XMLGenerator.endElement(self, name)

    def endDocument(self):
##        XMLGenerator.endDocument(self)
        self.fh.close()

class FindLaatste(ContentHandler):
    "Bevat het id van de laatst opgevoerde Artiest "
    def __init__(self):
        self.id = "0"

    def startElement(self, name, attrs):
        if name == "artiest":
            item = attrs.get("id", None)
            if int(item) > int(self.id):
                self.id = item

def artiestenlijst():
    namen = []
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = ZoekNamen()
    parser.setContentHandler(dh)
    parser.parse(artiestenfile)
    if len(dh.namenlijst) > 0:
        ## s = []
        ## for x in dh.namenlijst:
            ## h = ("%s;#;%s;#;%s" % (x[0], x[1], x[2]))
            ## s.append(h)
        ## s.sort()
        ## for x in s:
            ## y = x.split(";#;")
            ## namen.append([y[1], y[2], y[0]])
        for x, y, z in sorted(dh.namenlijst):
            namen.append((y, z, x))
        return namen

class Artiest(object):
    def __init__(self,item,sel="0"):
        self.fn = artiestenfile
        self.fno = "_oud".join(os.path.splitext(self.fn))
        self.zoek_item = item
        zoek_id = 0
        zoek_naam = 0
        self.id = 0
        self.naam = ""
        self.sort = ""
        if self.zoek_item == "0" or self.zoek_item == 0:
            parser = make_parser()
            parser.setFeature(feature_namespaces, 0)
            dh = FindLaatste()
            parser.setContentHandler(dh)
            parser.parse(self.fn)
            self.id = str(int(dh.id) + 1)
            self.naam = ""
            self.sort = ""
        else:
            self.id = 0
            self.naam = ""
            if sel == 0 or sel == "0":
                zoek_id = 1
                self.naam = item
            if sel == 1 or sel == "1":
                zoek_naam = 1
                self.id = item
            # Create a parser
            parser = make_parser()
            # Tell the parser we are not interested in XML namespaces
            parser.setFeature(feature_namespaces, 0)
            # Create the handler
            if self.id == "0" or self.id == 0:
                parser = make_parser()
                parser.setFeature(feature_namespaces, 0)
                dh = FindLaatste()
                parser.setContentHandler(dh)
                parser.parse(self.fn)
                self.id = str(int(dh.id) + 1)
            if zoek_id:
                dh = ZoekopNaam(item)
            if zoek_naam:
                dh = ZoekopId(item)
            # Tell the parser to use our handler
            parser.setContentHandler(dh)
            # Parse the input
            parser.parse(self.fn)
            if dh.founditem:
                if zoek_id:
                    self.id = dh.id
                if zoek_naam:
                    self.naam = dh.naam
                self.sort = dh.sort

    def write(self):
        shutil.copyfile(self.fn,self.fno)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = UpdateArtiest(self)
        parser.setContentHandler(dh)
        parser.parse(self.fno)
