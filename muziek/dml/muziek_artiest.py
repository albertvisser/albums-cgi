# zoek een artiest met naam en geeft het id terug of andersom

from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
from string import index
from globals import xmlpad

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
            self.namenlijst.append([sort,id,naam])

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
            id = attrs.get('id', None)
            naam = attrs.get('naam', None)
            sort = attrs.get('sort', None)
            if self.founditem == 1:
                id = self.ah.Id
                naam = self.ah.Naam
                sort = self.ah.sort
            self._out.write('<%s id="%s" naam="%s" sort="%s" />' % (name,id,escape(naam),escape(sort)))
        else:
            XMLGenerator.startElement(self, name, attrs)


    def characters(self,content):
        XMLGenerator.characters(self,content)
#        pass

    def endElement(self, name):
        if name != 'artiest':
            if self.itemfound == 0:
                id = self.ah.Id
                naam = self.ah.Naam
                sort = self.ah.sort
                self._out.write('<artiest id="%s" naam="%s" sort="%s" />\n' % (id,escape(naam),escape(sort)))
            XMLGenerator.endElement(self, name)


    def endDocument(self):
##        XMLGenerator.endDocument(self)
        self.fh.close()

class FindLaatste(ContentHandler):
    "Bevat het id van de laatst opgevoerde Artiest "
    def __init__(self):
        self.Id = "0"

    def startElement(self, name, attrs):
        if name == "artiest":
            item = attrs.get("id", None)
            if int(item) > int(self.Id):
                self.Id = item

class ArtiestenLijst:
    def __init__(self):
        self.fn = xmlpad + "Artiesten.xml"
        self.Namen = []
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        dh = ZoekNamen()
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fn)
        if len(dh.namenlijst) > 0:
            s = []
            for x in dh.namenlijst:
#                h = x[0] + ";#;" + x[1] +  ";#;" + x[2]
                h = ("%s;#;%s;#;%s" % (x[0],x[1],x[2]))
                s.append(h)
##            for x in s:
##                print x
            s.sort()
##            for x in s:
##                print x
            for x in s:
                y = x.split(";#;")
                self.Namen.append([y[1].encode('iso-8859-1'),y[2].encode('iso-8859-1'),y[0].encode('iso-8859-1')])

class Artiest:
    def __init__(self,item,sel="0"):
        self.fn = xmlpad + "Artiesten.xml"
        self.fno = xmlpad + "Artiesten_oud.xml"
        self.zoek_item = item
        zoekId = 0
        zoekNaam = 0
        self.Id = 0
        self.Naam = ""
        self.sort = ""
        if self.zoek_item == "0" or self.zoek_item == 0:
            parser = make_parser()
            parser.setFeature(feature_namespaces, 0)
            dh = FindLaatste()
            parser.setContentHandler(dh)
            parser.parse(self.fn)
            self.Id = str(int(dh.Id) + 1)
            self.Naam = ""
            self.sort = ""
        else:
            self.Id = 0
            self.Naam = ""
            if sel == 0 or sel == "0":
                zoekId = 1
                self.Naam = item
            if sel == 1 or sel == "1":
                zoekNaam = 1
                self.Id = item
            # Create a parser
            parser = make_parser()
            # Tell the parser we are not interested in XML namespaces
            parser.setFeature(feature_namespaces, 0)
            # Create the handler
            if self.Id == "0" or self.Id == 0:
                parser = make_parser()
                parser.setFeature(feature_namespaces, 0)
                dh = FindLaatste()
                parser.setContentHandler(dh)
                parser.parse(self.fn)
                self.Id = str(int(dh.Id) + 1)
            if zoekId:
                dh = ZoekopNaam(item)
            if zoekNaam:
                dh = ZoekopId(item)
            # Tell the parser to use our handler
            parser.setContentHandler(dh)
            # Parse the input
            parser.parse(self.fn)
            if dh.founditem:
                if zoekId:
                    self.Id = dh.id
                if zoekNaam:
                    self.Naam = dh.naam
                self.sort = dh.sort.encode('iso-8859-1')

    def setNaam(self,value):
        self.Naam = value

    def setSort(self,value):
        self.sort = value

    def write(self):
        from shutil import copyfile
        from os import remove
        copyfile(self.fn,self.fno)
#        remove(self.fn)
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = UpdateArtiest(self)
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fno)

def test():
##    dh = Artiest('27', '1')
##    print dh.Id, dh.Naam, dh.sort
##    dh = Artiest('Elvis Costello', '0')
##    print dh.Id, dh.Naam, dh.sort
##    dh = Artiest(0)
##    print dh.Id, dh.Naam, dh.sort
##    dh.setNaam("Testvogeltje")
##    dh.setSort("Test")
##    print dh.Id, dh.Naam, dh.sort
##    dh.write()
    dh = ArtiestenLijst()
    for x in dh.Namen:
        print x

if __name__ == '__main__':
	test()
