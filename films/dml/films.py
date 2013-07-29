import os
import shutil
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
xmlpad = os.path.dirname(__file__)
xmlfile = os.path.join(xmlpad, "Films.xml")

class FindFilm(ContentHandler):
    "Bevat de gegevens van een bepaald item"
    def __init__(self, item):
        self.search_item = item		# keywaarde
        # Initialize the flags to false
        self.founditem = self.itemfound = False
        self.soort = self.taal = self.genre = self.loc = self.titel = ""
        self.van = self.jaar = self.met = self.over = self.duur = ""
        self.in_soort = self.in_taal = self.in_genre = self.in_loc = False
        self.in_titel = self.in_van = self.in_jaar = self.in_met = False
        self.in_over = self.in_duur = False

    def startElement(self, name, attrs):
        if name == 'film':
            item = attrs.get('id', None)
            if item == self.search_item:
                self.founditem = True
                self.soort = attrs.get('soort', '')
                self.taal = attrs.get('taal', '')
                self.genre = attrs.get('genre', '')
                self.loc = attrs.get('loc', '')
        elif name == 'titel':
            if self.founditem:
                self.in_titel = True
                self.titel = ""
        elif name == 'van':
            if self.founditem:
                self.in_van = True
                self.van = ""
        elif name == 'jaar':
            if self.founditem:
                self.in_jaar = True
                self.jaar = ""
        elif name == 'met':
            if self.founditem:
                self.in_met = True
                self.met = ""
        elif name == 'over':
            if self.founditem:
                self.in_over = True
                self.over = ""
        elif name == 'duur':
            if self.founditem:
                self.in_duur = True
                self.duur = ""

    def characters(self, ch):
        if self.in_titel:
            self.titel += ch
        elif self.in_van:
            self.van += ch
        elif self.in_jaar:
            self.jaar += ch
        elif self.in_met:
            self.met += ch
        elif self.in_over:
            self.over += ch
        elif self.in_duur:
            self.duur += ch

    def endElement(self, name):
        if name == 'film':
            if self.founditem:
                self.itemfound = True
                self.founditem = False
        elif name == 'titel':
            if self.in_titel:
                self.in_titel = False
        elif name == 'van':
            if self.in_van:
                self.in_van = False
        elif name == 'jaar':
            if self.in_jaar:
                self.in_jaar = False
        elif name == 'met':
            if self.in_met:
                self.in_met = False
        elif name == 'over':
            if self.in_over:
                self.in_over = False
        elif name == 'duur':
            if self.in_duur:
                self.in_duur = False

class UpdateFilm(XMLGenerator):
    "item updaten"
    "aan het eind zit een element genaamd laatste. Als het id van de tekst hoger is dan deze, dan laatste aanpassen."
    def __init__(self, item):
        self.dh = item
        self.search_item = self.dh.id
        self.fh = open(self.dh.fn, 'w')
        self.founditem = self.itemfound = self.nowrite = False
        XMLGenerator.__init__(self, self.fh)

    def startElement(self, name, attrs):
    #-- kijk of we met het te wijzigen item bezig zijn
        if name == 'film':
            item = attrs.get('id', None)
            if item == str(self.search_item):
                self.founditem = self.itemfound = True
        #-- xml element (door)schrijven
        if not self.founditem:
            XMLGenerator.startElement(self, name, attrs)

    def characters(self, ch):
        if not self.founditem:
            if not self.nowrite:
                XMLGenerator.characters(self, ch)

    def endElement(self, name):
        if name == 'laatste':
            nowrite = False
        else:
            if not self.founditem:
                if name == 'films':
                    if not self.itemfound:
                        self.startElement("film", {"id": self.dh.id})
                        self.endElement("film")
                        self.laatste = self.dh.id
                        self._out.write("\n  ")
                    self.startElement("laatste", {"id": self.laatste})
                    self.endElement("laatste")
                else:
                    XMLGenerator.endElement(self, name)
            else:
                if name == 'film':
                    self.startElement("film", {"id": self.dh.id,
                        'soort': self.dh.soort, 'taal': self.dh.taal,
                        'genre': self.dh.genre, 'loc': self.dh.loc})
                    self._out.write(">\n")
                    self.startElement("titel>")
                    self.characters(self.dh.titel)
                    self.endElement("titel>")
                    self._out.write("\n  ")
                    self.startElement("van>")
                    self.characters(self.dh.van)
                    self.endElement("van>")
                    self._out.write("\n  ")
                    self.startElement("jaar>")
                    self.characters(self.dh.jaar)
                    self.endElement("jaar>")
                    self._out.write("\n  ")
                    self.startElement("met>")
                    self.characters(self.dh.met)
                    self.endElement("met>")
                    self._out.write("\n  ")
                    self.startElement("over>")
                    self.characters(self.dh.over)
                    self.endElement("over>")
                    self._out.write("\n  ")
                    self.startElement("duur>")
                    self.characters(self.dh.duur)
                    self.endElement("duur>")
                    self._out.write("\n  ")
                    self.endElement("film")
                    self._out.write("\n  ")
                    self.founditem = False

    def endDocument(self):
        self.fh.close()

class SearchFilm(ContentHandler):
    "Bevat de gegevens van een bepaald item"
    def __init__(self, itemlist=None, searchdict=None):
        self.itemlist = itemlist		# lijst met op te nemen elementen
        self.searchdict = searchdict	# dictionary met te zoeken gegevens
        # Initialize the flags to false
        self.items = []
        self.titel = self.van = self.jaar = self.met = self.over = self.duur = ""
        self.in_titel = self.in_van = self.in_jaar = False
        self.in_met = self.in_over = self.in_duur = False

    def startElement(self, name, attrs):
        if name == 'film':
            self.select_this = False
            item = attrs.get('id', None)
            self.listitem = [item]
            for zoek in ('soort', 'taal', 'genre', 'loc'):
                if not self.searchdict:
                    self.select_this = True
                else:
                    try:
                        h = self.searchdict[zoek]
                    except KeyError:
                        pass
                    else:
                        if h in v:
                            self.select_this = True
        elif name == 'titel':
            self.in_titel = True
            self.titel = ""
        elif name == 'van':
            self.in_van = True
            self.van = ""
        elif name == 'jaar':
            self.in_jaar = True
            self.jaar = ""
        elif name == 'met':
            self.in_met = True
            self.met = ""
        elif name == 'over':
            self.in_over = True
            self.over = ""
        elif name == 'duur':
            self.in_duur = True
            self.duur = ""

    def characters(self, ch):
        if self.in_titel:
            self.titel += ch
        elif self.in_van:
            self.van += ch
        elif self.in_jaar:
            self.jaar += ch
        elif self.in_met:
            self.met += ch
        elif self.in_over:
            self.over += ch
        elif self.in_duur:
            self.duur += ch

    def endElement(self, name):
        if name == 'film':
            if self.select_this:
                self.items.append(self.listitem)
        elif name == 'titel':
            if self.in_titel:
                self.in_titel = False
                if name in self.itemlist:
                    self.listitem.append(self.titel)
                if not self.searchdict:
                    self.select_this = True
                else:
                    try:
                        h = self.searchdict['titel'].upper()
                    except KeyError:
                        h = ''
                    if h and h in self.titel.upper():
                        self.select_this = True
        elif name == 'van':
            if self.in_van:
                self.in_van = False
                if name in self.itemlist:
                    self.listitem.append(self.van)
                if not self.searchdict:
                    self.select_this = True
                elif 'van' in self.searchdict:
                    if self.searchdict['van'].upper() in self.van.upper():
                        self.select_this = True
        elif name == 'jaar':
            if self.in_jaar:
                self.in_jaar = False
                if name in self.itemlist:
                    self.listitem.append(self.jaar)
                if not self.searchdict:
                    self.select_this = True
                else:
                    try:
                        h = self.searchdict['jaar']
                    except KeyError:
                        h = ''
                    if h and h in self.jaar:
                        self.select_this = True
        elif name == 'met':
            if self.in_met:
                self.in_met = False
                if name in self.itemlist:
                    self.listitem.append(self.met)
                if not self.searchdict:
                    self.select_this = True
                else:
                    try:
                        h = self.searchdict['met'].upper()
                    except KeyError:
                        h = ''
                    if h and h in self.met.upper():
                        self.select_this = True
        elif name == 'over':
            if self.in_over:
                self.in_over = False
                if name in self.itemlist:
                    self.listitem.append(self.over)
                if not self.searchdict:
                    self.select_this = True
                else:
                    try:
                        h = self.searchdict['over'].upper()
                    except KeyError:
                        h = ''
                    if h and h in self.over.upper():
                        self.select_this = True
        elif name == 'duur':
            if self.in_duur:
                self.in_duur = False
                if name in self.itemlist:
                    self.listitem.append(self.duur)
                if not self.searchdict:
                    self.select_this = True
                else:
                    try:
                        h = self.searchdict['duur']
                    except KeyError:
                        h = ''
                    if h and h in self.duur:
                        self.select_this = True

class FilmList:
    "lijst met gegevens van een selectie van items"
    def __init__(self, element_list, selection_criteria=None):
        self.fn = xmlfile # naam van het xml bestand
        self.fno = xmlfile + ".old" # naam van de backup van het xml bestand
        self.items = []
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = SearchFilm(element_list, selection_criteria)
        parser.setContentHandler(dh)
        parser.parse(self.fn)
        ## for x in dh.items:
            ## items = []
            ## for y in x:
                ## items.append(y)
            ## self.items.append(items)
        self.items = [x for x in dh.items]

class Film:
    "lijst alle gegevens van een bepaald item"
    def __init__(self, id):
        self.id = id
        self.fn = xmlfile # naam van het xml bestand
        self.fno = xmlfile + ".old" # naam van de backup van het xml bestand
        self.found = False
        self.soort = self.taal = self.genre = self.loc = self.titel = ""
        self.van = self.jaar = self.met = self.over = self.duur = ""

    def read(self):
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = FindFilm(str(self.id))
        parser.setContentHandler(dh)
        parser.parse(self.fn)
        self.found = dh.itemfound
        if self.found:
            self.soort = dh.soort
            self.taal = dh.taal
            self.genre = dh.genre
            self.loc = dh.loc
            self.titel = dh.titel
            self.van = dh.van
            self.jaar = dh.jaar
            self.met = dh.met
            self.over = dh.over
            self.duur = dh.duur

    def write(self):
        shutil.copyfile(self.fn, self.fno)
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        dh = UpdateFilm(self)
        parser.setContentHandler(dh)
        parser.parse(self.fno)

