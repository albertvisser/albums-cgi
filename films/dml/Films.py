from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
from string import index
from globals import xmlpad

class FindFilm(ContentHandler):
    "Bevat de gegevens van een bepaald item"
    def __init__(self, item):
        self.search_item = item		# keywaarde
        # Initialize the flags to false
        self.founditem = 0
        self.itemfound = 0
        self.inSoortContent = 0
        self.Soort= ""
        self.inTaalContent = 0
        self.Taal= ""
        self.inGenreContent = 0
        self.Genre= ""
        self.inLocContent = 0
        self.Loc= ""
        self.inTitelContent = 0
        self.Titel= ""
        self.inVanContent = 0
        self.Van= ""
        self.inJaarContent = 0
        self.Jaar= ""
        self.inMetContent = 0
        self.Met= ""
        self.inOverContent = 0
        self.Over= ""
        self.inDuurContent = 0
        self.Duur= ""

    def startElement(self, name, attrs):
        if name == 'film':
            item = attrs.get('id', None)
            if item == self.search_item:
                self.founditem = 1
                self.Soort = attrs.get('soort',None)
                self.Taal = attrs.get('taal',None)
                self.Genre = attrs.get('genre',None)
                self.Loc = attrs.get('loc',None)
        elif name == 'titel':
            if self.founditem:
                self.inTitelContent = 1
                self.Titel = ""
        elif name == 'van':
            if self.founditem:
                self.inVanContent = 1
                self.Van = ""
        elif name == 'jaar':
            if self.founditem:
                self.inJaarContent = 1
                self.Jaar = ""
        elif name == 'met':
            if self.founditem:
                self.inMetContent = 1
                self.Met = ""
        elif name == 'over':
            if self.founditem:
                self.inOverContent = 1
                self.Over = ""
        elif name == 'duur':
            if self.founditem:
                self.inDuurContent = 1
                self.Duur = ""

    def characters(self, ch):
        if self.inTitelContent:
            self.Titel = self.Titel + ch
        elif self.inVanContent:
            self.Van = self.Van + ch
        elif self.inJaarContent:
            self.Jaar = self.Jaar + ch
        elif self.inMetContent:
            self.Met = self.Met + ch
        elif self.inOverContent:
            self.Over = self.Over + ch
        elif self.inDuurContent:
            self.Duur = self.Duur + ch

    def endElement(self, name):
        if name == 'film':
            if self.founditem:
                self.itemfound = 1
                self.founditem = 0
        elif name == 'titel':
            if self.inTitelContent:
                self.inTitelContent = 0
        elif name == 'van':
            if self.inVanContent:
                self.inVanContent = 0
        elif name == 'jaar':
            if self.inJaarContent:
                self.inJaarContent = 0
        elif name == 'met':
            if self.inMetContent:
                self.inMetContent = 0
        elif name == 'over':
            if self.inOverContent:
                self.inOverContent = 0
        elif name == 'duur':
            if self.inDuurContent:
                self.inDuurContent = 0

class UpdateFilm(XMLGenerator):
    "item updaten"
    "aan het eind zit een element genaamd laatste. Als het id van de tekst hoger is dan deze, dan laatste aanpassen."
    def __init__(self, item):
        self.dh = item
        self.search_item = self.dh.id
        self.fh = open(self.dh.fn,'w')
        self.founditem = 0
        self.itemfound = 0
        self.nowrite = 0
        XMLGenerator.__init__(self,self.fh)

    def startElement(self, name, attrs):
    #-- kijk of we met het te wijzigen item bezig zijn
        if name == 'film':
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
                if name == 'films':
                    if self.itemfound == 0:
                        self.startElement("film",{"id":self.dh.id})
                        self.endElement("film")
                        self.Laatste = self.dh.id
                        self._out.write("\n  ")
                    self._out.write('<laatste id="%s" />\n' % self.Laatste)
                    self._out.write('</films>\n')
                else:
                    XMLGenerator.endElement(self, name)
            else:
                if name == 'film':
                    self._out.write('  <film id="%s"' % self.dh.Id)
                    self._out.write(' soort="%s"' % self.dh.Soort)
                    self._out.write(' taal="%s"' % self.dh.Taal)
                    self._out.write(' genre="%s"' % self.dh.Genre)
                    self._out.write(' loc="%s"' % self.dh.Loc)
                    self._out.write(">\n")
                    self._out.write('    <titel>%s</titel>\n' % self.dh.Titel)
                    self._out.write('    <van>%s</van>\n' % self.dh.Van)
                    self._out.write('    <jaar>%s</jaar>\n' % self.dh.Jaar)
                    self._out.write('    <met>%s</met>\n' % self.dh.Met)
                    self._out.write('    <over>%s</over>\n' % self.dh.Over)
                    self._out.write('    <duur>%s</duur>\n' % self.dh.Duur)
                    self._out.write('  </film>\n')
                    self.founditem = 0

    def endDocument(self):
##        XMLGenerator.endDocument(self)
        self.fh.close()

class SearchFilm(ContentHandler):
    "Bevat de gegevens van een bepaald item"
    def __init__(self, itemlist, searchlist):
        self.itemlist = itemlist		# lijst met op te nemen elementen
        self.searchlist = searchlist	# dictionary met te zoeken gegevens
        # Initialize the flags to false
        self.Items = []
        self.inTitelContent = 0
        self.Titel= ""
        self.inVanContent = 0
        self.Van= ""
        self.inJaarContent = 0
        self.Jaar= ""
        self.inMetContent = 0
        self.Met= ""
        self.inOverContent = 0
        self.Over= ""
        self.inDuurContent = 0
        self.Duur= ""

    def startElement(self, name, attrs):
        if name == 'film':
            self.SelectThis = 0
            item = attrs.get('id', None)
            self.listitem = [item]
            for z in self.itemlist:
                v = attrs.get('soort',None)
                if z == 'soort':
                    self.listitem.append(v)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('soort'):
                        h = self.searchlist['soort']
                        if v.find(h) >= 0:
                            self.SelectThis = 1
            for z in self.itemlist:
                v = attrs.get('taal',None)
                if z == 'taal':
                    self.listitem.append(v)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('taal'):
                        h = self.searchlist['taal']
                        if v.find(h) >= 0:
                            self.SelectThis = 1
            for z in self.itemlist:
                v = attrs.get('genre',None)
                if z == 'genre':
                    self.listitem.append(v)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('genre'):
                        h = self.searchlist['genre']
                        if v.find(h) >= 0:
                            self.SelectThis = 1
            for z in self.itemlist:
                v = attrs.get('loc',None)
                if z == 'loc':
                    self.listitem.append(v)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('loc'):
                        h = self.searchlist['loc']
                        if v.find(h) >= 0:
                            self.SelectThis = 1
        elif name == 'titel':
            for z in self.itemlist:
                if z == name:
                    self.inTitelContent = 1
                    self.Titel = ""
        elif name == 'van':
            for z in self.itemlist:
                if z == name:
                    self.inVanContent = 1
                    self.Van = ""
        elif name == 'jaar':
            for z in self.itemlist:
                if z == name:
                    self.inJaarContent = 1
                    self.Jaar = ""
        elif name == 'met':
            for z in self.itemlist:
                if z == name:
                    self.inMetContent = 1
                    self.Met = ""
        elif name == 'over':
            for z in self.itemlist:
                if z == name:
                    self.inOverContent = 1
                    self.Over = ""
        elif name == 'duur':
            for z in self.itemlist:
                if z == name:
                    self.inDuurContent = 1
                    self.Duur = ""

    def characters(self, ch):
        if self.inTitelContent:
            self.Titel = self.Titel + ch
        elif self.inVanContent:
            self.Van = self.Van + ch
        elif self.inJaarContent:
            self.Jaar = self.Jaar + ch
        elif self.inMetContent:
            self.Met = self.Met + ch
        elif self.inOverContent:
            self.Over = self.Over + ch
        elif self.inDuurContent:
            self.Duur = self.Duur + ch

    def endElement(self, name):
        if name == 'film':
            if self.SelectThis:
                self.Items.append(self.listitem)
        elif name == 'titel':
            if self.inTitelContent:
                self.inTitelContent = 0
                self.listitem.append(self.Titel)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('titel'):
                        h = self.searchlist['titel'].upper()
                        s = self.Titel.upper()
                        if s.find(h) >= 0:
                            self.SelectThis = 1
        elif name == 'van':
            if self.inVanContent:
                self.inVanContent = 0
                self.listitem.append(self.Van)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('van'):
                        h = self.searchlist['van'].upper()
                        s = self.Van
                        if s.find(h) >= 0:
                            self.SelectThis = 1
        elif name == 'jaar':
            if self.inJaarContent:
                self.inJaarContent = 0
                self.listitem.append(self.Jaar)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('jaar'):
                        h = self.searchlist['jaar']
                        if self.Jaar.find(h) >= 0:
                            self.SelectThis = 1
        elif name == 'met':
            if self.inMetContent:
                self.inMetContent = 0
                self.listitem.append(self.Met)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('met'):
                        h = self.searchlist['met'].upper()
                        s = self.Met
                        if s.find(h) >= 0:
                            self.SelectThis = 1
        elif name == 'over':
            if self.inOverContent:
                self.inOverContent = 0
                self.listitem.append(self.Over)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('over'):
                        h = self.searchlist['over']
                        if self.Over.find(h) >= 0:
                            self.SelectThis = 1
        elif name == 'duur':
            if self.inDuurContent:
                self.inDuurContent = 0
                self.listitem.append(self.Duur)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('duur'):
                        h = self.searchlist['duur']
                        if self.Duur.find(h) >= 0:
                            self.SelectThis = 1

class FilmList:
    "lijst met gegevens van een selectie van items"
    def __init__(self, element_list, selection_criteria=None):
        self.fn = xmlpad + "Films.xml" # naam van het xml bestand
        self.fno = xmlpad + "Films.xml.old" # naam van de backup van het xml bestand
        self.Items = []
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = SearchFilm(element_list, selection_criteria)
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

class Film:
    "lijst alle gegevens van een bepaald item"
    def __init__(self, id):
        self.id = id
        self.fn = xmlpad + "Films.xml" # naam van het xml bestand
        self.fno = xmlpad + "Films.xml.old" # naam van de backup van het xml bestand
        self.found = 0
        self.Soort= ""
        self.Taal= ""
        self.Genre= ""
        self.Loc= ""
        self.Soort = ""
        self.Taal = ""
        self.Genre = ""
        self.Loc = ""
        self.Titel = ""
        self.Van = ""
        self.Jaar = ""
        self.Met = ""
        self.Over = ""
        self.Duur = ""

    def read(self):
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = FindFilm(str(self.id))
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fn)
        self.found = dh.itemfound
        if self.found:
            if dh.Soort != None:
                self.Soort = dh.Soort.encode('ISO-8859-1')
            if dh.Taal != None:
                self.Taal = dh.Taal.encode('ISO-8859-1')
            if dh.Genre != None:
                self.Genre = dh.Genre.encode('ISO-8859-1')
            if dh.Loc != None:
                self.Loc = dh.Loc.encode('ISO-8859-1')
            if dh.Titel != None:
                self.Titel = dh.Titel.encode('ISO-8859-1')
            if dh.Van != None:
                self.Van = dh.Van.encode('ISO-8859-1')
            if dh.Jaar != None:
                self.Jaar = dh.Jaar.encode('ISO-8859-1')
            if dh.Met != None:
                self.Met = dh.Met.encode('ISO-8859-1')
            if dh.Over != None:
                self.Over = dh.Over.encode('ISO-8859-1')
            if dh.Duur != None:
                self.Duur = dh.Duur.encode('ISO-8859-1')

    def write(self):
        from shutil import copyfile
        copyfile(self.fn,self.fno)
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = UpdateFilm(self)
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fno)

    def wijzigSoort(self,Soort):
        self.Soort = Soort

    def wijzigTaal(self,Taal):
        self.Taal = Taal

    def wijzigGenre(self,Genre):
        self.Genre = Genre

    def wijzigLoc(self,Loc):
        self.Loc = Loc

    def wijzigTitel(self,Titel):
        self.Titel = Titel

    def wijzigVan(self,Van):
        self.Van = Van

    def wijzigJaar(self,Jaar):
        self.Jaar = Jaar

    def wijzigMet(self,Met):
        self.Met = Met

    def wijzigOver(self,Over):
        self.Over = Over

    def wijzigDuur(self,Duur):
        self.Duur = Duur

if __name__ == '__main__':
##    test = 176
##    ih = Film(test)
##    ih.read()
##    if ih.found:
##        print 'Titel: ' + ih.Titel
##        print 'Van: ' + ih.Van
##        print 'Jaar: ' + ih.Jaar
##        print 'Met: ' + ih.Met
##        print 'Over: ' + ih.Over
    lh = FilmList(['titel'],{'van': 'mel'})
#    lh = FilmList(['titel','loc'])
    for x in lh.Items:
        print x
