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

class FindConcert(ContentHandler):
    "Bevat de gegevens van een bepaald item"
    def __init__(self, item):
        self.search_item = item		# keywaarde
        # Initialize the flags to false
        self.founditem = 0
        self.itemfound = 0
        self.inArtiestContent = 0
        self.Artiest= ""
        self.inLocatieContent = 0
        self.Locatie= ""
        self.inDatumContent = 0
        self.Datum= ""
        self.inBezettingContent = 0
        self.Bezetting= ""
        self.inBezettingContent = 0
        self.Bezetting= ""
        self.Tracks = []
        self.inTrackContent = 0
        self.Opnames = []

    def startElement(self, name, attrs):
        if name == 'concert':
            item = attrs.get('id', None)
            if item == self.search_item:
                self.founditem = 1
                self.Artiest = attrs.get('artiest',None)
        elif name == 'locatie':
            if self.founditem:
                self.inLocatieContent = 1
                self.Locatie = ""
        elif name == 'datum':
            if self.founditem:
                self.inDatumContent = 1
                self.Datum = ""
        elif name == 'bezetting':
            if self.founditem:
                self.inBezettingContent = 1
                self.Bezetting = ""
        elif name == 'track':
            if self.founditem:
                self.ditTracknr = attrs.get('volgnr', None)
                self.ditTrack = ""
                self.inTrackContent = 1
        elif name == 'opname':
            if self.founditem:
                h1 = attrs.get('type', None)
                h2 = attrs.get('desc', "")
                self.Opnames.append([h1,h2])

    def characters(self, ch):
        if self.inLocatieContent:
            self.Locatie = self.Locatie + ch
        elif self.inDatumContent:
            self.Datum = self.Datum + ch
        elif self.inBezettingContent:
            self.Bezetting = self.Bezetting + ch
        elif self.inTrackContent:
            self.ditTrack = self.ditTrack + ch

    def endElement(self, name):
        if name == 'concert':
            if self.founditem:
                self.itemfound = 1
                self.founditem = 0
        elif name == 'locatie':
            if self.inLocatieContent:
                self.inLocatieContent = 0
        elif name == 'datum':
            if self.inDatumContent:
                self.inDatumContent = 0
        elif name == 'bezetting':
            if self.inBezettingContent:
                self.inBezettingContent = 0
        elif name == 'track':
            if self.inTrackContent:
                self.Tracks.append([self.ditTracknr, self.ditTrack])
                self.inTrackContent = 0

class FindLaatste(ContentHandler):
    "Bevat het id van het laatst opgevoerde Concert "
    def __init__(self):
        self.Id = "0"

    def startElement(self, name, attrs):
        if name == "concert":
            item = attrs.get("id", None)
            if int(item) > int(self.Id):
                self.Id = item

class UpdateConcert(XMLGenerator):
    "item updaten"
    def __init__(self, item):
        self.dh = item
        self.search_item = self.dh.Id
        self.fh = open(self.dh.fn,'w')
        self.founditem = 0
        self.itemfound = 0
        self.nowrite = 0
        XMLGenerator.__init__(self,self.fh)

    def startElement(self, name, attrs):
    #-- kijk of we met het te wijzigen item bezig zijn
        if name == 'concert':
            item = attrs.get('id', None)
            if item == str(self.search_item):
                self.founditem = 1
                self.itemfound = 1
        #-- xml element (door)schrijven
        if self.founditem != 1:
            XMLGenerator.startElement(self, name, attrs)

    def characters(self, ch):
        if self.founditem != 1:
            if self.nowrite == 0:
                XMLGenerator.characters(self,ch)

    def endElement(self, name):
        if name == 'laatste':
            nowrite = 0
        else:
            if self.founditem != 1:
                if name == 'live':
                    if self.itemfound == 0:
                        self.startElement("concert",{"id":self.dh.Id})
                        self.endElement("concert")
                        self._out.write("\n  ")
                    self._out.write('</live>\n')
                else:
                    XMLGenerator.endElement(self, name)
            else:
                if name == 'concert':
                    self._out.write('  <concert id="%s"' % self.dh.Id)
                    self._out.write(' artiest="%s"' % self.dh.Artiest)
                    self._out.write(">\n")
                    self._out.write('    <locatie>%s</locatie>\n' % self.dh.Locatie)
                    self._out.write('    <datum>%s</datum>\n' % self.dh.Datum)
                    self._out.write('    <bezetting>%s</bezetting>\n' % self.dh.Bezetting)
                    i = 0
                    for x in self.dh.Tracks:
                        i = i + 1
                        self._out.write('    <track volgnr="%i">%s</track>\n' % (i,x))
                    for x in self.dh.Opnames:
                        self._out.write('    <opname type="%s" />\n' % (x))
                    self._out.write('  </concert>\n')
                    self.founditem = 0

    def endDocument(self):
##        XMLGenerator.endDocument(self)
        self.fh.close()

class SearchConcert(ContentHandler):
    "Bevat de gegevens van een bepaald item"
    def __init__(self, itemlist, searchlist):
        self.listArtiest = 0
        self.listLocatie = 0
        self.listDatum = 0
        self.listBezetting = 0
        for z in itemlist:
            if z == "artiest":
                self.listArtiest = 1
            if z == "locatie":
                self.listLocatie = 1
            if z == "datum":
                self.listDatum = 1
            if z == "bezetting":
                self.listBezetting = 1
        self.selAlles = 0
        self.selArtiest = 0
        self.selLocatie = 0
        self.selDatum = 0
        self.selBezetting = 0
        self.zoekArtiest = ""
        self.zoekLocatie = ""
        self.zoekDatum = ""
        self.zoekBezetting = ""
        if searchlist == None:
            self.selAlles = 1
        else:
            if searchlist.has_key('artiest'):
                self.selArtiest = 1
                self.zoekArtiest = searchlist['artiest'].upper()
            if searchlist.has_key('locatie'):
                self.selLocatie = 1
                self.zoekLocatie = searchlist['locatie'].upper()
            if searchlist.has_key('datum'):
                self.selDatum = 1
                self.zoekDatum = searchlist['datum'].upper()
            if searchlist.has_key('bezetting'):
                self.selBezetting = 1
                self.zoekBezetting = searchlist['bezetting'].upper()
        self.Items = []
        self.inLocatieContent = 0
        self.Locatie= ""
        self.inDatumContent = 0
        self.Datum= ""
        self.inBezettingContent = 0
        self.Bezetting= ""
        self.Artiesten = {}
        dh = ArtiestenLijst()
        for x in dh.Namen:
            self.Artiesten[x[0]] = x[1]

    def startElement(self, name, attrs):
        if name == 'concert':
            self.SelectThis = 0
            item = attrs.get('id', None)
            self.listitem = [item]
            v = attrs.get('artiest',None)
            if  self.listArtiest:
                self.listitem.append(self.Artiesten[v])
            if self.selArtiest:
                if v.upper() == self.zoekArtiest:
                    self.SelectThis = 1
        elif name == 'locatie':
##            if self.listLocatie:
                self.inLocatieContent = 1
                self.Locatie = ""
        elif name == 'datum':
##            if self.listDatum:
                self.inDatumContent = 1
                self.Datum = ""
        elif name == 'bezetting':
##            if self.listBezetting:
                self.inBezettingContent = 1
                self.Bezetting = ""

    def characters(self, ch):
        if self.inLocatieContent:
            self.Locatie = self.Locatie + ch
        elif self.inDatumContent:
            self.Datum = self.Datum + ch
        elif self.inBezettingContent:
            self.Bezetting = self.Bezetting + ch

    def endElement(self, name):
        if name == 'concert':
            if self.selAlles or self.SelectThis:
                self.Items.append(self.listitem)
        elif name == 'locatie':
            if self.inLocatieContent:
                self.inLocatieContent = 0
                if self.listLocatie:
                    self.listitem.append(self.Locatie)
                if self.selLocatie and self.Locatie.upper().find(self.zoekLocatie) >= 0:
                    self.SelectThis = 1
        elif name == 'datum':
            if self.inDatumContent:
                self.inDatumContent = 0
                if self.listDatum:
                    self.listitem.append(self.Datum)
                if self.selDatum and self.Datum.upper().find(self.zoekDatum) >= 0:
                    self.SelectThis = 1
        elif name == 'bezetting':
            if self.inBezettingContent:
                self.inBezettingContent = 0
                if self.listBezetting:
                    self.listitem.append(self.Bezetting)
                if self.selBezetting and self.Bezetting.upper().find(self.zoekBezetting) >= 0:
                    self.SelectThis = 1

class ConcertList:
    "lijst met gegevens van een selectie van items"
    def __init__(self, element_list, selection_criteria=None):
        self.fn = xmlpad + "live_met.xml" # naam van het xml bestand
        self.fno = xmlpad + "live_met.xml.old" # naam van de backup van het xml bestand
        self.Items = []
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = SearchConcert(element_list, selection_criteria)
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fn)
        if len(dh.Items) > 0:
            for x in dh.Items:
                items = []
                for y in x:
                    try:
                        items.append(y.encode('ISO-8859-1'))
                    except:
                        items.append(y)
                self.Items.append(items)

class Concert:
    "lijst alle gegevens van een bepaald item"
    def __init__(self, id):
        self.Id = id
        self.fn = xmlpad + "live_met.xml" # naam van het xml bestand
        self.fno = xmlpad + "live_met.xml.old" # naam van de backup van het xml bestand
        self.found = 0
        self.Artiest= ""
        if self.Id == "0" or self.Id == 0:
            parser = make_parser()
            parser.setFeature(feature_namespaces, 0)
            dh = FindLaatste()
            parser.setContentHandler(dh)
            parser.parse(self.fn)
            self.Id = str(int(dh.Id) + 1)
        self.Artiest = ""
        self.Locatie = ""
        self.Datum = ""
        self.Bezetting = ""
        self.Tracks = []
        self.Opnames = []

    def read(self):
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = FindConcert(str(self.Id))
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fn)
        self.found = dh.itemfound
        if self.found:
            if self.Artiest != None:
#                self.Artiest = dh.Artiest.encode('ISO-8859-1')
                ah = Artiest(str(dh.Artiest), '1')
                self.Artiest = ah.Naam
            if self.Locatie != None:
                self.Locatie = dh.Locatie.encode('ISO-8859-1')
            if self.Datum != None:
                self.Datum = dh.Datum.encode('ISO-8859-1')
            if self.Bezetting != None:
                self.Bezetting = dh.Bezetting.encode('ISO-8859-1')
            if len(dh.Tracks) > 0:
                # tracks op volgorde zetten
                l = len(dh.Tracks)
                for x in range(l):
                    self.Tracks.append("")
                for x in range(l):
                    y = x + 1
                    for z in dh.Tracks:
                        if int(z[0]) == y:
                            self.Tracks[x] = z[1].encode('ISO-8859-1')
            if len(dh.Opnames) > 0:
                for x in dh.Opnames:
                    y = x[0].encode('ISO-8859-1')
                    if x[1] != "":
                        y = y + " " + x[1].encode('ISO-8859-1')
                    self.Opnames.append(y)

    def write(self):
        from shutil import copyfile
        copyfile(self.fn,self.fno)
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = UpdateConcert(self)
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fno)

    def wijzigArtiest(self,Artiest):
        self.Artiest = Artiest

    def wijzigLocatie(self,Locatie):
        self.Locatie = Locatie

    def wijzigDatum(self,Datum):
        self.Datum = Datum

    def wijzigBezetting(self,Bezetting):
        self.Bezetting = Bezetting

    def addTrack(self,Track):
        self.Tracks.append(Track)

    def remTrack(self,Track):
        for x in self.Tracks:
            if x == Track:
                self.Tracks.remove(Track)
                break

    def editTrack(self,oldTrack,newTrack):
        for x in self.Tracks:
            if x == oldTrack:
                i = self.Tracks.index(oldTrack)
                self.Tracks[i] = newTrack
                break

    def insTrack(self,oldTrack,newTrack):
        "let op: insert BEFORE"
        i = self.Tracks.index(oldTrack)
        self.Tracks.insert(i,newTrack)

    def addOpname(self,Opname):
        self.Opnames.append(Opname)

    def remOpname(self,Opname):
        for x in self.Opnames:
            if x == Opname:
                self.Opnames.remove(Opname)
                break

if __name__ == '__main__':
##    test = 49
##    ih = Concert(test)
##    ih.read()
##    if ih.found:
##        print 'Artiest: ' + ih.Artiest
##        print 'Locatie: ' + ih.Locatie
##        print 'Datum: ' + ih.Datum
##        print 'Bezetting: ' + ih.Bezetting
##        if len(ih.Tracks) > 0:
##            print "Tracks:"
##            for x in ih.Tracks:
##                print x
##        if len(ih.Opnames) > 0:
##            print "Opnames:"
##            for x in ih.Opnames:
##                print x
    lh = ConcertList(['artiest','locatie','datum'],{'artiest': '1'})
    for x in lh.Items:
        print x
