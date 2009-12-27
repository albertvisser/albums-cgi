from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
from string import index
from muziek_artiest import Artiest
from muziek_artiest import ArtiestenLijst
from globals import xmlpad

class SearchAlbum(ContentHandler):
    "Opnames op type en beschrijving"
    def __init__(self, item):
        self.search_item = item		# keywaarde
        # Initialize the flags to false
        self.Id
        self.Artiest= ""
        self.inTitelContent = 0
        self.Titel= ""
        self.Opnames = [] # type, desc, artiest, naam

    def startElement(self, name, attrs):
        if name == 'album':
            self.Id = attrs.get('id', None)
            self.Artiest = attrs.get('artiest',None)
        elif name == 'titel':
            self.inTitelContent = 1
            self.Titel = ""
        elif name == 'opname':
            h1 = attrs.get('type', None)
            h2 = attrs.get('desc', "")
            self.Opnames.append([h1,h2,self.Id,self.Artiest,self.Titel])

    def characters(self, ch):
        if self.inTitelContent:
            self.Titel = self.Titel + ch

    def endElement(self, name):
        if name == 'album':
            pass
        elif name == 'titel':
            if self.inTitelContent:
                self.inTitelContent = 0

class AlbumList:
    "lijst met gegevens van een selectie van items"
    def __init__(self, element_list=None, selection_criteria=None):
        dh = Artiestenlijst()
        al = {}
        for x in dh.Namen:
            al[x[0]] = x[1]
        self.fn = xmlpad + "studio_met.xml" # naam van het xml bestand
        self.fno = xmlpad + "studio_met.xml.old" # naam van de backup van het xml bestand
        self.Items = []
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = SearchAlbum(element_list, selection_criteria)
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fn)
        if len(dh.Opnames) > 0:
            for x in dh.Opnames: # type, desc, artiest, naam
                items = []
                for i in range(4):
                    if i == 2:
                        items.append(al[x[i]])
                    else:
                        try:
                            items.append(x[i].encode('ISO-8859-1'))
                        except:
                            items.append(x[i])
                self.Items.append(items)

if __name__ == '__main__':
    #~ lh = AlbumList(['artiest','titel','jaar','volgnr'],{'artiest': '55'})
    lh = AlbumList()
    if len(lh.Items) > 0:
        s = lh.Items
        s.sort()
        for x in s:
            print x
    else:
        print "No studio albums found"
