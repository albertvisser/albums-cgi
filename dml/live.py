import os
import shutil
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
from artiest import Artiest
from artiest import artiestenlijst
import _globals
datafile = os.path.join(_globals.xmlpad, "live_met.xml") # naam van het xml bestand
backup = os.path.join(_globals.xmlpad, "live_met.xml.old") # naam van de backup van het xml bestand

class _FindConcert(ContentHandler):
    "Bevat de gegevens van een bepaald item"
    def __init__(self, item):
        self.search_item = item		# keywaarde
        self.founditem = self.itemfound = False
        self.in_artiest = self.in_locatie = self.in_datum = False
        self.in_bezetting = self.in_track = False
        self.artiest = self.locatie = self.datum = self.bezetting = ""
        self.tracks = []
        self.opnames = []

    def startElement(self, name, attrs):
        if name == 'concert':
            item = attrs.get('id', None)
            if item == self.search_item:
                self.founditem = True
                self.artiest = attrs.get('artiest',None)
        elif name == 'locatie':
            if self.founditem:
                self.in_locatie = True
                self.locatie = ""
        elif name == 'datum':
            if self.founditem:
                self.in_datum = True
                self.datum = ""
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
        if self.in_locatie:
            self.locatie = self.locatie + ch
        elif self.in_datum:
            self.datum = self.datum + ch
        elif self.in_bezetting:
            self.bezetting = self.bezetting + ch
        elif self.in_track:
            self.dittrack = self.dittrack + ch

    def endElement(self, name):
        if name == 'concert':
            if self.founditem:
                self.itemfound = True
                self.founditem = False
        elif name == 'locatie':
            if self.in_locatie:
                self.in_locatie = False
        elif name == 'datum':
            if self.in_datum:
                self.in_datum = False
        elif name == 'bezetting':
            if self.in_bezetting:
                self.in_bezetting = False
        elif name == 'track':
            if self.in_track:
                self.tracks.append([self.dittracknr, self.dittrack])
                self.in_track = False

class _FindLaatste(ContentHandler):
    "Bevat het id van het laatst opgevoerde Concert "
    def __init__(self):
        self.id = "0"

    def startElement(self, name, attrs):
        if name == "concert":
            item = attrs.get("id", None)
            if int(item) > int(self.id):
                self.id = item

class _UpdateConcert(XMLGenerator):
    "item updaten"
    def __init__(self, item):
        self.dh = item
        self.search_item = self.dh.id
        self._out = open(self.dh.fn, 'w', encoding='utf-8')
        self.founditem = self.itemfound = self.nowrite = False
        XMLGenerator.__init__(self, self._out, encoding='utf-8')

    def startElement(self, name, attrs):
    #-- kijk of we met het te wijzigen item bezig zijn
        if name == 'concert':
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
                if name == 'live':
                    if not self.itemfound:
                        self.startElement("concert", {"id":  self.dh.id})
                        self.endElement("concert")
                        self._out.write("\n  ")
                    self._out.write('</live>\n')
                else:
                    XMLGenerator.endElement(self, name)
            else:
                if name == 'concert':
                    self._out.write('<concert id="%s"' % self.dh.id)
                    self._out.write(' artiest="%s"' % self.dh.artiestid)
                    self._out.write(">\n")
                    self._out.write('  <locatie>%s</locatie>\n' % self.dh.locatie)
                    self._out.write('  <datum>%s</datum>\n' % self.dh.datum)
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
                    self._out.write('</concert>\n')
                    self.founditem = False

    def endDocument(self):
##        XMLGenerator.endDocument(self)
        self._out.close()

class _SearchConcert(ContentHandler):
    "Bevat de gegevens van een bepaald item"
    def __init__(self, itemlist, searchlist):
        self.list_artiest = self.list_locatie = self.list_datum = \
        self.list_bezetting = False
        for z in itemlist:
            if z == "artiest":
                self.list_artiest = True
            if z == "locatie":
                self.list_locatie = True
            if z == "datum":
                self.list_datum = True
            if z == "bezetting":
                self.list_bezetting = True
        self.sel_alles = self.sel_artiest = self.sel_locatie = \
        self.sel_datum = self.sel_bezetting = False
        self.zoek_artiest = self.zoek_locatie = self.zoek_datum = \
        self.zoek_bezetting = ""
        if searchlist == None:
            self.sel_alles = True
        else:
            if 'artiest' in searchlist:
                self.sel_artiest = True
                self.zoek_artiest = searchlist['artiest'].upper()
            if 'locatie' in searchlist:
                self.sel_locatie = True
                self.zoek_locatie = searchlist['locatie'].upper()
            if 'datum' in searchlist:
                self.sel_datum = True
                self.zoek_datum = searchlist['datum'].upper()
            if 'bezetting' in searchlist:
                self.sel_bezetting = True
                self.zoek_bezetting = searchlist['bezetting'].upper()
        self.items = []
        self.in_locatie = self.in_datum = self.in_bezetting = False
        self.locatie = self.datum = self.bezetting = ""
        self.artiesten = {}
        for x in artiestenlijst():
            self.artiesten[x[0]] = x[1]

    def startElement(self, name, attrs):
        if name == 'concert':
            self.select_this = False
            item = attrs.get('id', None)
            self.listitem = [item]
            v = attrs.get('artiest',None)
            if  self.list_artiest:
                self.listitem.append(self.artiesten[v])
            if self.sel_artiest:
                if v.upper() == self.zoek_artiest:
                    self.select_this = True
        elif name == 'locatie':
##            if self.list_locatie:
                self.in_locatie = True
                self.locatie = ""
        elif name == 'datum':
##            if self.list_datum:
                self.in_datum = True
                self.datum = ""
        elif name == 'bezetting':
##            if self.list_bezetting:
                self.in_bezetting = True
                self.bezetting = ""

    def characters(self, ch):
        if self.in_locatie:
            self.locatie = self.locatie + ch
        elif self.in_datum:
            self.datum = self.datum + ch
        elif self.in_bezetting:
            self.bezetting = self.bezetting + ch

    def endElement(self, name):
        if name == 'concert':
            if self.sel_alles or self.select_this:
                self.items.append(self.listitem)
        elif name == 'locatie':
            if self.in_locatie:
                self.in_locatie = False
                if self.list_locatie:
                    self.listitem.append(self.locatie)
                if self.sel_locatie and self.zoek_locatie in self.locatie.upper():
                    self.select_this = True
        elif name == 'datum':
            if self.in_datum:
                self.in_datum = False
                if self.list_datum:
                    self.listitem.append(self.datum)
                if self.sel_datum and self.zoek_datum in self.datum.upper():
                    self.select_this = True
        elif name == 'bezetting':
            if self.in_bezetting:
                self.in_bezetting = False
                if self.list_bezetting:
                    self.listitem.append(self.bezetting)
                if self.sel_bezetting and self.zoek_bezetting in self.bezetting.upper():
                    self.select_this = True

def concertlist(element_list, selection_criteria=None):
    "lijst met gegevens van een selectie van items"
    itemlist = []
    parser = make_parser()
    parser.setFeature(feature_namespaces, 0)
    dh = _SearchConcert(element_list, selection_criteria)
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

class Concert:
    "lijst alle gegevens van een bepaald item"
    def __init__(self, id_):
        self.id = id_
        self.fn = datafile # naam van het xml bestand
        self.fno = backup # naam van de backup van het xml bestand
        self.found = False
        self.artiestid = self.artiest = self.locatie = self.datum = ''
        self.bezetting = ""
        self.tracks = []
        self.opnames = []
        if self.id == "0" or self.id == 0:
            parser = make_parser()
            parser.setFeature(feature_namespaces, 0)
            dh = _FindLaatste()
            parser.setContentHandler(dh)
            parser.parse(self.fn)
            self.id = str(int(dh.id) + 1)

    def read(self):
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = _FindConcert(str(self.id))
        parser.setContentHandler(dh)
        parser.parse(self.fn)
        self.found = dh.itemfound
        if self.found:
            if dh.artiest is not None:
                self.artiestid = dh.artiest
                ah = Artiest(dh.artiest)
                self.artiest = ah.naam
            if dh.locatie is not None:
                self.locatie = dh.locatie
            if dh.datum is not None:
                self.datum = dh.datum
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
                        y += " " + x[1]
                    self.opnames.append(y)

    def write(self):
        shutil.copyfile(self.fn,self.fno)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = _UpdateConcert(self)
        parser.setContentHandler(dh)
        parser.parse(self.fno)

    def add_track(self, track):
        self.tracks.append(track)

    def rem_track(self, track):
        for x in self.tracks:
            if x == track:
                self.tracks.remove(track)
                break

    def edit_track(self, oldtrack, newtrack):
        for x in self.tracks:
            if x == oldtrack:
                i = self.tracks.index(oldtrack)
                self.tracks[i] = newtrack
                break

    def ins_track(self, oldtrack, newtrack):
        "let op: insert before"
        i = self.tracks.index(oldtrack)
        self.tracks.insert(i, newtrack)

    def add_opname(self, opname):
        self.opnames.append(opname)

    def rem_opname(self, opname):
        for x in self.opnames:
            if x == opname:
                self.opnames.remove(opname)
                break
