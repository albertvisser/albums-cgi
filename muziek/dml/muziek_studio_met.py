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

class FindAlbum(ContentHandler):
    "Bevat de gegevens van een bepaald item"
    def __init__(self, item):
        self.search_item = item		# keywaarde
        # Initialize the flags to false
        self.founditem = 0
        self.itemfound = 0
        self.inArtiestContent = 0
        self.Artiest= ""
        self.inTitelContent = 0
        self.Titel= ""
        self.inLabelContent = 0
        self.Label= ""
        self.inJaarContent = 0
        self.Jaar= ""
        self.inVolgnrContent = 0
        self.Volgnr= ""
        self.inProducerContent = 0
        self.Producer= ""
        self.inCreditsContent = 0
        self.Credits= ""
        self.inBezettingContent = 0
        self.Bezetting= ""
        self.Tracks = []
        self.inTrackContent = 0
        self.Opnames = []

    def startElement(self, name, attrs):
        if name == 'album':
            item = attrs.get('id', None)
            if item == self.search_item:
                self.founditem = 1
                self.Artiest = attrs.get('artiest',None)
        elif name == 'titel':
            if self.founditem:
                self.inTitelContent = 1
                self.Titel = ""
        elif name == 'label':
            if self.founditem:
                self.inLabelContent = 1
                self.Label = ""
        elif name == 'jaar':
            if self.founditem:
                self.inJaarContent = 1
                self.Jaar = ""
        elif name == 'volgnr':
            if self.founditem:
                self.inVolgnrContent = 1
                self.Volgnr = ""
        elif name == 'producer':
            if self.founditem:
                self.inProducerContent = 1
                self.Producer = ""
        elif name == 'credits':
            if self.founditem:
                self.inCreditsContent = 1
                self.Credits = ""
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
        if self.inTitelContent:
            self.Titel = self.Titel + ch
        elif self.inLabelContent:
            self.Label = self.Label + ch
        elif self.inJaarContent:
            self.Jaar = self.Jaar + ch
        elif self.inVolgnrContent:
            self.Volgnr = self.Volgnr + ch
        elif self.inProducerContent:
            self.Producer = self.Producer + ch
        elif self.inCreditsContent:
            self.Credits = self.Credits + ch
        elif self.inBezettingContent:
            self.Bezetting = self.Bezetting + ch
        elif self.inTrackContent:
            self.ditTrack = self.ditTrack + ch

    def endElement(self, name):
        if name == 'album':
            if self.founditem:
                self.itemfound = 1
                self.founditem = 0
        elif name == 'titel':
            if self.inTitelContent:
                self.inTitelContent = 0
        elif name == 'label':
            if self.inLabelContent:
                self.inLabelContent = 0
        elif name == 'jaar':
            if self.inJaarContent:
                self.inJaarContent = 0
        elif name == 'volgnr':
            if self.inVolgnrContent:
                self.inVolgnrContent = 0
        elif name == 'producer':
            if self.inProducerContent:
                self.inProducerContent = 0
        elif name == 'credits':
            if self.inCreditsContent:
                self.inCreditsContent = 0
        elif name == 'bezetting':
            if self.inBezettingContent:
                self.inBezettingContent = 0
        elif name == 'track':
            if self.inTrackContent:
                self.Tracks.append([self.ditTracknr, self.ditTrack])
                self.inTrackContent = 0


class FindLaatste(ContentHandler):
    "Bevat het id van het laatst opgevoerde Album "
    def __init__(self):
        self.Id = "0"

    def startElement(self, name, attrs):
        if name == "album":
            item = attrs.get("id", None)
            if int(item) > int(self.Id):
                self.Id = item

class UpdateAlbum(XMLGenerator):
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
        if name == 'album':
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
                if name == 'studio':
                    if self.itemfound == 0:
                        self.startElement("album",{"id":self.dh.Id})
                        self.endElement("album")
                        self._out.write("\n  ")
                    self._out.write('</studio>\n')
                else:
                    XMLGenerator.endElement(self, name)
            else:
                if name == 'album':
                    self._out.write('  <album id="%s"' % self.dh.Id)
                    self._out.write(' artiest="%s"' % self.dh.Artiest)
                    self._out.write(">\n")
                    self._out.write('    <titel>%s</titel>\n' % self.dh.Titel)
                    self._out.write('    <label>%s</label>\n' % self.dh.Label)
                    self._out.write('    <jaar>%s</jaar>\n' % self.dh.Jaar)
                    self._out.write('    <volgnr>%s</volgnr>\n' % self.dh.Volgnr)
                    self._out.write('    <producer>%s</producer>\n' % self.dh.Producer)
                    self._out.write('    <credits>%s</credits>\n' % self.dh.Credits)
                    self._out.write('    <bezetting>%s</bezetting>\n' % self.dh.Bezetting)
                    i = 0
                    for x in self.dh.Tracks:
                        i = i + 1
                        self._out.write('    <track volgnr="%i">%s</track>\n' % (i,x))
                    for x in self.dh.Opnames:
                        self._out.write('    <opname type="%s" />\n' % (x))
                    self._out.write('  </album>\n')
                    self.founditem = 0

    def endDocument(self):
##        XMLGenerator.endDocument(self)
        self.fh.close()

class SearchAlbum(ContentHandler):
    "Bevat de gegevens van een bepaald item"
    def __init__(self, itemlist, searchlist):
        self.listArtiest = 0
        self.listTitel = 0
        self.listLabel = 0
        self.listJaar = 0
        self.listProducer = 0
        self.listCredits = 0
        self.listBezetting = 0
        for z in itemlist:
            if z == "artiest":
                self.listArtiest = 1
            if z == "titel":
                self.listTitel = 1
            if z == "label":
                self.listLabel = 1
            if z == "jaar":
                self.listJaar = 1
            if z == "producer":
                self.listProducer = 1
            if z == "credits":
                self.listCredits = 1
            if z == "bezetting":
                self.listBezetting = 1
        self.selAlles = 0
        self.selArtiest = 0
        self.selTitel = 0
        self.selLabel = 0
        self.selJaar = 0
        self.selProducer = 0
        self.selCredits = 0
        self.selBezetting = 0
        self.zoekArtiest = ""
        self.zoekTitel = ""
        self.zoekLabel = ""
        self.zoekJaar = ""
        self.zoekProducer = ""
        self.zoekCredits = ""
        self.zoekBezetting = ""
        if searchlist == None:
            self.selAlles = 1
        else:
            if searchlist.has_key('artiest'):
                self.selArtiest = 1
                self.zoekArtiest = searchlist['artiest'].upper()
            if searchlist.has_key('titel'):
                self.selTitel = 1
                self.zoekTitel = searchlist['titel'].upper()
            if searchlist.has_key('label'):
                self.selLabel = 1
                self.zoekLabel = searchlist['label'].upper()
            if searchlist.has_key('jaar'):
                self.selJaar = 1
                self.zoekJaar = searchlist['jaar'].upper()
            if searchlist.has_key('producer'):
                self.selProducer = 1
                self.zoekProducer = searchlist['producer'].upper()
            if searchlist.has_key('credits'):
                self.selCredits = 1
                self.zoekCredits = searchlist['credits'].upper()
            if searchlist.has_key('bezetting'):
                self.selBezetting = 1
                self.zoekBezetting = searchlist['bezetting'].upper()
        self.Items = []
        self.inTitelContent = 0
        self.Titel= ""
        self.inLabelContent = 0
        self.Label= ""
        self.inJaarContent = 0
        self.Jaar= ""
        self.inVolgnrContent = 0
        self.Volgnr= ""
        self.inProducerContent = 0
        self.Producer= ""
        self.inCreditsContent = 0
        self.Credits= ""
        self.inBezettingContent = 0
        self.Bezetting= ""
        self.Opname= ""
        self.Artiesten = {}
        dh = ArtiestenLijst()
        for x in dh.Namen:
            self.Artiesten[x[0]] = x[1]

    def startElement(self, name, attrs):
        if name == 'album':
            self.SelectThis = 0
            item = attrs.get('id', None)
            self.listitem = [item]
            v = attrs.get('artiest',None)
            if self.listArtiest:
                self.listitem.append(self.Artiesten[v])
            if self.selArtiest:
                if v.upper() == self.zoekArtiest:
                    self.SelectThis = 1
        elif name == 'titel':
##            if self.listTitel:
                self.inTitelContent = 1
                self.Titel = ""
        elif name == 'label':
##            if self.listLabel:
                self.inLabelContent = 1
                self.Label = ""
        elif name == 'jaar':
##            if self.listJaar:
                self.inJaarContent = 1
                self.Jaar = ""
        elif name == 'volgnr':
##            if self.listJaar:
                self.inVolgnrContent = 1
                self.Volgnr = ""
        elif name == 'producer':
##            if self.listProducer:
                self.inProducerContent = 1
                self.Producer = ""
        elif name == 'credits':
##            if self.listCredits:
                self.inCreditsContent = 1
                self.Credits = ""
        elif name == 'bezetting':
##            if self.listBezetting:
                self.inBezettingContent = 1
                self.Bezetting = ""

    def characters(self, ch):
        if self.inTitelContent:
            self.Titel = self.Titel + ch
        elif self.inLabelContent:
            self.Label = self.Label + ch
        elif self.inJaarContent:
            self.Jaar = self.Jaar + ch
        elif self.inVolgnrContent:
            self.Volgnr = self.Volgnr + ch
        elif self.inProducerContent:
            self.Producer = self.Producer + ch
        elif self.inCreditsContent:
            self.Credits = self.Credits + ch
        elif self.inBezettingContent:
            self.Bezetting = self.Bezetting + ch

    def endElement(self, name):
        if name == 'album':
            if self.selAlles or self.SelectThis:
                self.Items.append(self.listitem)
        elif name == 'titel':
            if self.inTitelContent:
                self.inTitelContent = 0
                if self.listTitel:
                    self.listitem.append(self.Titel)
                if self.selTitel and self.Titel.upper().find(self.zoekTitel) >= 0:
                    self.SelectThis = 1
        elif name == 'label':
            if self.inLabelContent:
                self.inLabelContent = 0
                if self.listLabel:
                    self.listitem.append(self.Label)
                if self.selLabel and self.Titel.upper().find(self.zoekTitel) >= 0:
                    self.SelectThis = 1
        elif name == 'jaar':
            if self.inJaarContent:
                self.inJaarContent = 0
                if self.listJaar:
                    self.listitem.append(self.Jaar)
                if self.selJaar and self.Jaar.upper().find(self.zoekJaar) >= 0:
                    self.SelectThis = 1
        elif name == 'volgnr':
            if self.inVolgnrContent:
                self.inVolgnrContent = 0
                if self.listJaar:
                    self.listitem.append(self.Volgnr)
##                if self.selVolgnr and self.Volgnr.upper().find(self.zoekVolgnr) >= 0:
##                    self.SelectThis = 1
        elif name == 'producer':
            if self.inProducerContent:
                self.inProducerContent = 0
                if self.listProducer:
                    self.listitem.append(self.Producer)
                if self.selProducer and self.Producer.upper().find(self.zoekProducer) >= 0:
                    self.SelectThis = 1
        elif name == 'credits':
            if self.inCreditsContent:
                self.inCreditsContent = 0
                if self.listCredits:
                    self.listitem.append(self.Credits)
                if self.selCredits and self.Credits.upper().find(self.zoekCredits) >= 0:
                    self.SelectThis = 1
        elif name == 'bezetting':
            if self.inBezettingContent:
                self.inBezettingContent = 0
                if self.listBezetting:
                    self.listitem.append(self.Bezetting)
                if self.selBezetting and self.Bezetting.upper().find(self.zoekBezetting) >= 0:
                    self.SelectThis = 1

class AlbumList:
    "lijst met gegevens van een selectie van items"
    def __init__(self, element_list, selection_criteria=None):
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
        if len(dh.Items) > 0:
            for x in dh.Items:
                items = []
                for y in x:
                    try:
                        items.append(y.encode('ISO-8859-1'))
                    except:
                        items.append(y)
                self.Items.append(items)

class Album:
    "lijst alle gegevens van een bepaald item"
    def __init__(self, id):
        self.Id = id
        self.fn = xmlpad + "studio_met.xml" # naam van het xml bestand
        self.fno = xmlpad + "studio_met.xml.old" # naam van de backup van het xml bestand
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
        self.Titel = ""
        self.Label = ""
        self.Jaar = ""
        self.Volgnr = ""
        self.Producer = ""
        self.Credits = ""
        self.Bezetting = ""
        self.Tracks = []
        self.Opnames = []

    def read(self):
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = FindAlbum(str(self.Id))
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fn)
        self.found = dh.itemfound
        if self.found:
            if dh.Artiest != None:
#                self.Artiest = dh.Artiest.encode('ISO-8859-1')
                ah = Artiest(dh.Artiest, '1')
                self.Artiest = ah.Naam
            if dh.Titel != None:
                self.Titel = dh.Titel.encode('ISO-8859-1')
            if dh.Label != None:
                self.Label = dh.Label.encode('ISO-8859-1')
            if dh.Jaar != None:
                self.Jaar = dh.Jaar.encode('ISO-8859-1')
            if dh.Volgnr != None:
                self.Volgnr = dh.Volgnr.encode('ISO-8859-1')
            if dh.Producer != None:
                self.Producer = dh.Producer.encode('ISO-8859-1')
            if dh.Credits != None:
                self.Credits = dh.Credits.encode('ISO-8859-1')
            if dh.Bezetting != None:
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
        dh = UpdateAlbum(self)
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fno)

    def wijzigArtiest(self,Artiest):
        self.Artiest = Artiest

    def wijzigTitel(self,Titel):
        self.Titel = Titel

    def wijzigLabel(self,Label):
        self.Label = Label

    def wijzigJaar(self,Jaar):
        self.Jaar = Jaar

    def wijzigVolgnr(self,Volgnr):
        self.Volgnr = Volgnr

    def wijzigProducer(self,Producer):
        self.Producer = Producer

    def wijzigCredits(self,Credits):
        self.Credits = Credits

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

##    test = 595
##    ih = Album(test)
##    ih.read()
##    if ih.found:
##        print 'Artiest: ' + ih.Artiest
##        print 'Titel: ' + ih.Titel
##        print 'Label: ' + ih.Label
##        print 'Jaar: ' + ih.Jaar
##        print 'Volgnr: ' + ih.Volgnr
##        print 'Producer: ' + ih.Producer
##        print 'Credits: ' + ih.Credits
##        print 'Bezetting: ' + ih.Bezetting
##        if len(ih.Tracks) > 0:
##            print "Tracks:"
##            for x in ih.Tracks:
##                print x
##        if len(ih.Opnames) > 0:
##            print "Opnames:"
##            for x in ih.Opnames:
##                print x
##        ih.remTrack("Track 3")
##        ih.insTrack("Track 4","Track 4-")
##        ih.addTrack("Track 3")
##        ih.editTrack("Track 2","Dit is even heel iets anders")
##        ih.remOpname("Opname 1")
##        ih.addOpname("Opname 2")
##        ih.remOpname("Opname 3")
##        ih.addOpname("Opname 4")
##        ih.write()
##    else:
##        print "Studio album not found"

##    lh = AlbumList(['artiest','titel','jaar','volgnr'],{'artiest': '55'})
    list = ['artiest','titel']
    sel = {"artiest": '6'}
##    lh = AlbumList(list,sel)
    lh = AlbumList(list)
    if len(lh.Items) > 0:
        s = lh.Items
        s.sort()
        for x in s:
            print x[1],x[2]
    else:
        print "No studio albums found"
