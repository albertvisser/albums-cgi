# selecteer alle opnames met hetzelfde album-id en geeft types en items terug

from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
from string import index

class FindOpnames(ContentHandler):
    "bevat de gegevens van een bepaalde user"
    def __init__(self, album):
        self.search_album = album
        # Initialize the flags to false
        self.itemfound = 0
        self.founditem = 0
        self.gegs = []

    def startElement(self, name, attrs):
        if name == 'opname':
            album = attrs.get('album', None)
            if album == self.search_album:
                self.founditem = 1
                type = attrs.get("type", None)
                item = attrs.get("item", None)
                self.gegs.append([type,item])

class Opnames:
    "lees een bepaalde user en controleer of deze een bepaald password heeft"
    def __init__(self,album): # user aanmaken
        self.fn = "C:/Program Files/Xitami/webpages/muziek/opnames.xml"
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = FindOpnames(str(album))
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fn)
        self.gegs = []
        self.found = dh.founditem
        if self.found:
            for x in dh.gegs:
                item1 = x[0].encode("iso-8859-1")
                if x[1] != None:
                    item2 = x[1].encode("iso-8859-1")
                else:
                    item2 = ""
                self.gegs.append([item1,item2])

def test():
    dh = Opnames('202')
    if dh.found:
        for x in dh.gegs:
            print x
    else:
        print "opnames not found"
    
if __name__ == '__main__':
	test()
