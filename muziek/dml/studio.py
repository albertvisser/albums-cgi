import os
import shutil
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
from artiest import Artiest, artiestenlijst
import _globals
datafile = os.path.join(_globals.xmlpad, "studio_met.xml") # naam van het xml bestand
backup = os.path.join(_globals.xmlpad, "studio_met.xml.old") # naam van de backup van het xml bestand

class FindAlbum(ContentHandler):
    "Bevat de gegevens van een bepaald item"
    def __init__(self, item):
        self.search_item = item		# keywaarde
        # Initialize the flags to false
        self.founditem = self.itemfound = False
        self.in_artiest = self.in_titel = self.in_label = self.in_jaar = False
        self.in_volgnr = self.in_producer = self.in_credits = False
        self.in_bezetting = self.in_track = False
        self.artiest = self.titel = self.label = self.jaar = ""
        self.volgnr = self.producer = self.credits = self.bezetting = ""
        self.tracks = []
        self.opnames = []

    def startElement(self, name, attrs):
        if name == 'album':
            item = attrs.get('id', None)
            if item == self.search_item:
                self.founditem = True
                self.artiest = attrs.get('artiest',None)
        elif name == 'titel':
            if self.founditem:
                self.in_titel = True
                self.titel = ""
        elif name == 'label':
            if self.founditem:
                self.in_label = True
                self.label = ""
        elif name == 'jaar':
            if self.founditem:
                self.in_jaar = True
                self.jaar = ""
        elif name == 'volgnr':
            if self.founditem:
                self.in_volgnr = True
                self.volgnr = ""
        elif name == 'producer':
            if self.founditem:
                self.in_producer = True
                self.producer = ""
        elif name == 'credits':
            if self.founditem:
                self.in_credits = True
                self.credits = ""
        elif name == 'bezetting':
            if self.founditem:
                self.in_bezetting = True
                self.bezetting = ""
        elif name == 'track':
            if self.founditem:
                self.dittracknr = attrs.get('volgnr', None)
                self.dittrack = ""
                self.in_track = True
        elif name == 'opname':
            if self.founditem:
                h1 = attrs.get('type', None)
                h2 = attrs.get('desc', "")
                self.opnames.append([h1, h2])

    def characters(self, ch):
        if self.in_titel:
            self.titel = self.titel + ch
        elif self.in_label:
            self.label = self.label + ch
        elif self.in_jaar:
            self.jaar = self.jaar + ch
        elif self.in_volgnr:
            self.volgnr = self.volgnr + ch
        elif self.in_producer:
            self.producer = self.producer + ch
        elif self.in_credits:
            self.credits = self.credits + ch
        elif self.in_bezetting:
            self.bezetting = self.bezetting + ch
        elif self.in_track:
            self.dittrack = self.dittrack + ch

    def endElement(self, name):
        if name == 'album':
            if self.founditem:
                self.itemfound = True
                self.founditem = False
        elif name == 'titel':
            if self.in_titel:
                self.in_titel = False
        elif name == 'label':
            if self.in_label:
                self.in_label = False
        elif name == 'jaar':
            if self.in_jaar:
                self.in_jaar = False
        elif name == 'volgnr':
            if self.in_volgnr:
                self.in_volgnr = False
        elif name == 'producer':
            if self.in_producer:
                self.in_producer = False
        elif name == 'credits':
            if self.in_credits:
                self.in_credits = False
        elif name == 'bezetting':
            if self.in_bezetting:
                self.in_bezetting = False
        elif name == 'track':
            if self.in_track:
                self.tracks.append([self.dittracknr, self.dittrack])
                self.in_track = False


class FindLaatste(ContentHandler):
    "Bevat het id van het laatst opgevoerde Album "
    def __init__(self):
        self.id = "0"

    def startElement(self, name, attrs):
        if name == "album":
            item = attrs.get("id", None)
            if int(item) > int(self.id):
                self.id = item

class UpdateAlbum(XMLGenerator):
    "item updaten"
    def __init__(self, item):
        self.dh = item
        self.search_item = self.dh.id
        self._out = open(self.dh.fn, 'w', encoding='utf-8')
        self.founditem = self.itemfound = self.nowrite = False
        XMLGenerator.__init__(self, self._out, encoding='utf-8')

    def startElement(self, name, attrs):
    #-- kijk of we met het te wijzigen item bezig zijn
        if name == 'album':
            item = attrs.get('id', None)
            if item == str(self.search_item):
                self.founditem = self.itemfound = True
        #-- xml element (door)schrijven
        if not self.founditem:
            XMLGenerator.startElement(self, name, attrs)

    def characters(self, ch):
        if not self.founditem:
            if not self.nowrite:
                XMLGenerator.characters(self,ch)

    def endElement(self, name):
        if name == 'laatste':
            nowrite = False
        else:
            if not self.founditem:
                if name == 'studio':
                    if not self.itemfound:
                        self.startElement("album", {"id": self.dh.id})
                        self.endElement("album")
                        ## self._out.write("\n  ")
                        ## self._out.write("\n")
                    self._out.write('</studio>\n')
                else:
                    XMLGenerator.endElement(self, name)
            else:
                if name == 'album':
                    self._out.write('<album id="%s"' % self.dh.id)
                    self._out.write(' artiest="%s">\n' % self.dh.artiestid)
                    self._out.write('  <titel>%s</titel>\n' % self.dh.titel)
                    self._out.write('  <label>%s</label>\n' % self.dh.label)
                    self._out.write('  <jaar>%s</jaar>\n' % self.dh.jaar)
                    self._out.write('  <volgnr>%s</volgnr>\n' % self.dh.volgnr)
                    self._out.write('  <producer>%s</producer>\n' %
                        self.dh.producer)
                    self._out.write('  <credits>%s</credits>\n' %
                        self.dh.credits)
                    self._out.write('  <bezetting>%s</bezetting>\n' %
                        self.dh.bezetting)
                    for ix, x in enumerate(self.dh.tracks):
                        self._out.write('  <track volgnr="%i">%s</track>\n' %
                            (ix + 1, x))
                    for x in self.dh.opnames:
                        self._out.write('  <opname ')
                        test = x.split(' - ', 1)
                        type = test[0]
                        if len(test) > 1:
                            oms = test[1]
                            self._out.write('desc="%s" ' % oms)
                        self._out.write('type="%s" />\n' % type)
                    self._out.write('</album>\n')
                    self.founditem = False

    def endDocument(self):
##        XMLGenerator.endDocument(self)
        self._out.close()

class SearchAlbum(ContentHandler):
    "Bevat de gegevens van een bepaald item"
    def __init__(self, itemlist, searchlist):
        self.list_artiest = self.list_titel = self.list_label = self.list_jaar = \
        self.list_producer = self.list_credits = self.list_bezetting = False
        for z in itemlist:
            if z == "artiest":
                self.list_artiest = True
            if z == "titel":
                self.list_titel = True
            if z == "label":
                self.list_label = True
            if z == "jaar":
                self.list_jaar = True
            if z == "producer":
                self.list_producer = True
            if z == "credits":
                self.list_credits = True
            if z == "bezetting":
                self.list_bezetting = True
        self.sel_alles = self.sel_artiest = self.sel_titel = self.sel_label = \
        self.sel_jaar = self.sel_producer = self.sel_credits = \
        self.sel_bezetting = False
        self.zoek_artiest = self.zoek_titel = self.zoek_label = self.zoek_jaar = \
        self.zoek_producer = self.zoek_credits = self.zoek_bezetting = ""
        if searchlist == None:
            self.sel_alles = True
        else:
            if 'artiest' in searchlist:
                self.sel_artiest = True
                self.zoek_artiest = searchlist['artiest'].upper()
            if 'titel' in searchlist:
                self.sel_titel = True
                self.zoek_titel = searchlist['titel'].upper()
            if 'label' in searchlist:
                self.sel_label = True
                self.zoek_label = searchlist['label'].upper()
            if 'jaar' in searchlist:
                self.sel_jaar = True
                self.zoek_jaar = searchlist['jaar'].upper()
            if 'producer' in searchlist:
                self.sel_producer = True
                self.zoek_producer = searchlist['producer'].upper()
            if 'credits' in searchlist:
                self.sel_credits = True
                self.zoek_credits = searchlist['credits'].upper()
            if 'bezetting' in searchlist:
                self.sel_bezetting = True
                self.zoek_bezetting = searchlist['bezetting'].upper()
        self.items = []
        self.titel = self.label = self.jaar = self.volgnr = ""
        self.producer = self.credits = self.bezetting = self.opname = ""
        self.in_titel = self.in_label = self.in_jaar = self.in_volgnr = False
        self.in_producer = self.in_credits = self.in_bezetting = False
        self.artiesten = {}
        for x in artiestenlijst():
            self.artiesten[x[0]] = x[1]

    def startElement(self, name, attrs):
        if name == 'album':
            self.select_this = False
            item = attrs.get('id', None)
            self.listitem = [item]
            v = attrs.get('artiest',None)
            if self.list_artiest:
                self.listitem.append(self.artiesten[v])
            if self.sel_artiest:
                if v.upper() == self.zoek_artiest:
                    self.select_this = 1
        elif name == 'titel':
##            if self.list_titel:
                self.in_titel = True
                self.titel = ""
        elif name == 'label':
##            if self.list_label:
                self.in_label = True
                self.label = ""
        elif name == 'jaar':
##            if self.list_jaar:
                self.in_jaar = True
                self.jaar = ""
        elif name == 'volgnr':
##            if self.list_volgnr:
                self.in_volgnr = True
                self.volgnr = ""
        elif name == 'producer':
##            if self.list_producer:
                self.in_producer = True
                self.producer = ""
        elif name == 'credits':
##            if self.list_credits:
                self.in_credits = True
                self.credits = ""
        elif name == 'bezetting':
##            if self.list_bezetting:
                self.in_bezetting = True
                self.bezetting = ""

    def characters(self, ch):
        if self.in_titel:
            self.titel = self.titel + ch
        elif self.in_label:
            self.label = self.label + ch
        elif self.in_jaar:
            self.jaar = self.jaar + ch
        elif self.in_volgnr:
            self.volgnr = self.volgnr + ch
        elif self.in_producer:
            self.producer = self.producer + ch
        elif self.in_credits:
            self.credits = self.credits + ch
        elif self.in_bezetting:
            self.bezetting = self.bezetting + ch

    def endElement(self, name):
        if name == 'album':
            if self.sel_alles or self.select_this:
                self.items.append(self.listitem)
        elif name == 'titel':
            if self.in_titel:
                self.in_titel = False
                if self.list_titel:
                    self.listitem.append(self.titel)
                if self.sel_titel and self.zoek_titel in self.titel.upper():
                    self.select_this = True
        elif name == 'label':
            if self.in_label:
                self.in_label = False
                if self.list_label:
                    self.listitem.append(self.label)
                if self.sel_label and self.zoek_label in self.label.upper():
                    self.select_this = True
        elif name == 'jaar':
            if self.in_jaar:
                self.in_jaar = False
                if self.list_jaar:
                    self.listitem.append(self.jaar)
                if self.sel_jaar and self.zoek_jaar in self.jaar.upper():
                    self.select_this = True
        elif name == 'volgnr':
            if self.in_volgnr:
                self.in_volgnr = False
                if self.list_jaar:
                    self.listitem.append(self.volgnr)
##                if self.sel_volgnr and self.zoekvolgnr in self.volgnr.upper():
##                    self.select_this = True
        elif name == 'producer':
            if self.in_producer:
                self.in_producer = False
                if self.list_producer:
                    self.listitem.append(self.producer)
                if self.sel_producer and self.zoek_producer in self.producer.upper():
                    self.select_this = True
        elif name == 'credits':
            if self.in_credits:
                self.in_credits = False
                if self.list_credits:
                    self.listitem.append(self.credits)
                if self.sel_credits and self.zoek_credits in self.credits.upper():
                    self.select_this = True
        elif name == 'bezetting':
            if self.in_bezetting:
                self.in_bezetting = False
                if self.list_bezetting:
                    self.listitem.append(self.bezetting)
                if self.sel_bezetting and self.zoek_bezetting in self.bezetting.upper():
                    self.select_this = True

def albumlist(element_list, selection_criteria=None):
    "lijst met gegevens van een selectie van items"
    itemlist = []
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = SearchAlbum(element_list, selection_criteria)
    parser.setContentHandler(dh)
    parser.parse(datafile)
    for x in dh.items:
        items = []
        for y in x:
            try:
                items.append(y)
            except:
                items.append(y)
        itemlist.append(items)
    return itemlist

class Album:
    "lijst alle gegevens van een bepaald item"
    def __init__(self, id_):
        self.id = id_
        self.fn = datafile
        self.fno = backup
        self.found = False
        self.artiestid = self.artiest = self.titel = self.label = self.jaar = ""
        self.volgnr = self.producer = self.credits = self.bezetting = ""
        self.tracks = []
        self.opnames = []
        if self.id == "0" or self.id == 0:
            parser = make_parser()
            parser.setFeature(feature_namespaces, 0)
            dh = FindLaatste()
            parser.setContentHandler(dh)
            parser.parse(self.fn)
            self.id = str(int(dh.id) + 1)

    def read(self):
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = FindAlbum(str(self.id))
        parser.setContentHandler(dh)
        parser.parse(self.fn)
        self.found = dh.itemfound
        if self.found:
            if dh.artiest is not None:
                self.artiestid = dh.artiest
                ah = Artiest(dh.artiest)
                self.artiest = ah.naam
            if dh.titel is not None:
                self.titel = dh.titel
            if dh.label is not None:
                self.label = dh.label
            if dh.jaar is not None:
                self.jaar = dh.jaar
            if dh.volgnr is not None:
                self.volgnr = dh.volgnr
            if dh.producer is not None:
                self.producer = dh.producer
            if dh.credits is not None:
                self.credits = dh.credits
            if dh.bezetting is not None:
                self.bezetting = dh.bezetting
            if len(dh.tracks) > 0:
                # tracks op volgorde zetten
                l = len(dh.tracks)
                for x in range(l):
                    self.tracks.append("")
                for x in range(l):
                    y = x + 1
                    for z in dh.tracks:
                        if int(z[0]) == y:
                            self.tracks[x] = z[1]
            if len(dh.opnames) > 0:
                for x in dh.opnames:
                    y = x[0]
                    if x[1] != "":
                        y = y + " - " + x[1]
                    self.opnames.append(y)

    def write(self):
        shutil.copyfile(self.fn,self.fno)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = UpdateAlbum(self)
        parser.setContentHandler(dh)
        parser.parse(self.fno)

    def add_track(self,track):
        self.tracks.append(track)

    def rem_track(self,track):
        for x in self.tracks:
            if x == track:
                self.tracks.remove(track)
                break

    def edit_track(self,oldtrack,newtrack):
        for x in self.tracks:
            if x == oldtrack:
                i = self.tracks.index(oldtrack)
                self.tracks[i] = newtrack
                break

    def ins_track(self,oldtrack,newtrack):
        "let op: insert BEFORE"
        i = self.tracks.index(oldtrack)
        self.tracks.insert(i,newtrack)

    def add_opname(self,opname):
        self.opnames.append(opname)

    def rem_opname(self,opname):
        for x in self.opnames:
            if x == opname:
                self.opnames.remove(opname)
                break
