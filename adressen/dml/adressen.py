from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
from xml.sax import saxutils
from xml.sax import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import escape
from string import index

class FindNaw(ContentHandler):
    "Bevat de gegevens van een bepaald item"
    def __init__(self, item):
        self.search_item = item		# keywaarde
        # Initialize the flags to false
        self.founditem = 0
        self.itemfound = 0
        self.inNaamContent = 0
        self.Naam= ""
        self.inStraatContent = 0
        self.Straat= ""
        self.inPostcodeContent = 0
        self.Postcode= ""
        self.inPlaatsContent = 0
        self.Plaats= ""
        self.inTelefoonContent = 0
        self.Telefoon= ""
        self.inGeborenContent = 0
        self.Geboren= ""
        self.inEmailContent = 0
        self.Email= ""

    def startElement(self, name, attrs):
        if name == 'naw':
            item = attrs.get('id', None)
            if item == self.search_item:
                self.founditem = 1
        elif name == 'naam':
            if self.founditem:
                self.inNaamContent = 1
                self.Naam = ""
        elif name == 'straat':
            if self.founditem:
                self.inStraatContent = 1
                self.Straat = ""
        elif name == 'postcode':
            if self.founditem:
                self.inPostcodeContent = 1
                self.Postcode = ""
        elif name == 'plaats':
            if self.founditem:
                self.inPlaatsContent = 1
                self.Plaats = ""
        elif name == 'telefoon':
            if self.founditem:
                self.inTelefoonContent = 1
                self.Telefoon = ""
        elif name == 'geboren':
            if self.founditem:
                self.inGeborenContent = 1
                self.Geboren = ""
        elif name == 'email':
            if self.founditem:
                self.inEmailContent = 1
                self.Email = ""

    def characters(self, ch):
        if self.inNaamContent:
            self.Naam = self.Naam + ch
        elif self.inStraatContent:
            self.Straat = self.Straat + ch
        elif self.inPostcodeContent:
            self.Postcode = self.Postcode + ch
        elif self.inPlaatsContent:
            self.Plaats = self.Plaats + ch
        elif self.inTelefoonContent:
            self.Telefoon = self.Telefoon + ch
        elif self.inGeborenContent:
            self.Geboren = self.Geboren + ch
        elif self.inEmailContent:
            self.Email = self.Email + ch

    def endElement(self, name):
        if name == 'naw':
            if self.founditem:
                self.itemfound = 1
                self.founditem = 0
        elif name == 'naam':
            if self.inNaamContent:
                self.inNaamContent = 0
        elif name == 'straat':
            if self.inStraatContent:
                self.inStraatContent = 0
        elif name == 'postcode':
            if self.inPostcodeContent:
                self.inPostcodeContent = 0
        elif name == 'plaats':
            if self.inPlaatsContent:
                self.inPlaatsContent = 0
        elif name == 'telefoon':
            if self.inTelefoonContent:
                self.inTelefoonContent = 0
        elif name == 'geboren':
            if self.inGeborenContent:
                self.inGeborenContent = 0
        elif name == 'email':
            if self.inEmailContent:
                self.inEmailContent = 0

class FindLaatste(ContentHandler):
    "Bevat het id van het laatst opgevoerde Naw "
    def __init__(self):
        # Initialize the flags to false
        self.founditem = 0
        self.itemfound = 0
        self.Id = 0

    def startElement(self, name, attrs):
        if name == 'laatste':
            #  self.Id = attrs.get('id', None)
            pass
        elif name == 'naw': # als er geen laatste is vergelijken we de id's
            item = attrs.get('id', None)
            if int(item) > int(self.Id):
                self.Id = item


class UpdateNaw(XMLGenerator):
    "item updaten"
    "aan het eind zit een element genaamd laatste. Als het id van de tekst hoger is dan deze, dan laatste aanpassen."
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
        if name == 'naw':
            item = attrs.get('id', None)
            if item == str(self.search_item):
                self.founditem = 1
                self.itemfound = 1
        if name == 'laatste':
            nowrite = 1
            self.Laatste = attrs.get('id',None)
        else:
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
                if name == 'adressen':
                    if self.itemfound == 0:
                        self.startElement("naw",{"id":self.dh.Id})
                        self.endElement("naw")
                        self.Laatste = self.dh.Id
                    self._out.write('<laatste id="%s" />\n' % self.Laatste)
                    self._out.write('</adressen>\n')
                else:
                    XMLGenerator.endElement(self, name)
            else:
                if name == 'naw':
                    self._out.write('  <naw id="%s"' % self.dh.Id)
                    self._out.write(">\n")
                    self._out.write('    <naam>%s</naam>\n' % self.dh.Naam)
                    self._out.write('    <straat>%s</straat>\n' % self.dh.Straat)
                    self._out.write('    <postcode>%s</postcode>\n' % self.dh.Postcode)
                    self._out.write('    <plaats>%s</plaats>\n' % self.dh.Plaats)
                    self._out.write('    <telefoon>%s</telefoon>\n' % self.dh.Telefoon)
                    self._out.write('    <email>%s</email>\n' % self.dh.Email)
                    self._out.write('    <geboren>%s</geboren>\n' % self.dh.Geboren)
                    self._out.write('  </naw>\n')
                    self.founditem = 0

    def endDocument(self):
##        XMLGenerator.endDocument(self)
        self.fh.close()

class SearchNaw(ContentHandler):
    "Bevat de gegevens van een bepaald item"
    def __init__(self, itemlist, searchlist):
        self.itemlist = itemlist		# lijst met op te nemen elementen
        self.searchlist = searchlist	# dictionary met te zoeken gegevens
        # Initialize the flags to false
        self.Items = []
        self.inNaamContent = 0
        self.Naam= ""
        self.inStraatContent = 0
        self.Straat= ""
        self.inPostcodeContent = 0
        self.Postcode= ""
        self.inPlaatsContent = 0
        self.Plaats= ""
        self.inTelefoonContent = 0
        self.Telefoon= ""
        self.inGeborenContent = 0
        self.Geboren= ""
        self.inEmailContent = 0
        self.Email= ""

    def startElement(self, name, attrs):
        if name == 'naw':
            self.SelectThis = 0
            item = attrs.get('id', None)
            self.listitem = [item]
        elif name == 'naam':
            for z in self.itemlist:
                if z == name:
                    self.inNaamContent = 1
                    self.Naam = ""
        elif name == 'straat':
            for z in self.itemlist:
                if z == name:
                    self.inStraatContent = 1
                    self.Straat = ""
        elif name == 'postcode':
            for z in self.itemlist:
                if z == name:
                    self.inPostcodeContent = 1
                    self.Postcode = ""
        elif name == 'plaats':
            for z in self.itemlist:
                if z == name:
                    self.inPlaatsContent = 1
                    self.Plaats = ""
        elif name == 'telefoon':
            for z in self.itemlist:
                if z == name:
                    self.inTelefoonContent = 1
                    self.Telefoon = ""
        elif name == 'geboren':
            for z in self.itemlist:
                if z == name:
                    self.inGeborenContent = 1
                    self.Geboren = ""
        elif name == 'email':
            for z in self.itemlist:
                if z == name:
                    self.inEmailContent = 1
                    self.Email = ""

    def characters(self, ch):
        if self.inNaamContent:
            self.Naam = self.Naam + ch
        elif self.inStraatContent:
            self.Straat = self.Straat + ch
        elif self.inPostcodeContent:
            self.Postcode = self.Postcode + ch
        elif self.inPlaatsContent:
            self.Plaats = self.Plaats + ch
        elif self.inTelefoonContent:
            self.Telefoon = self.Telefoon + ch
        elif self.inGeborenContent:
            self.Geboren = self.Geboren + ch
        elif self.inEmailContent:
            self.Email = self.Email + ch

    def endElement(self, name):
        if name == 'naw':
            if self.SelectThis:
                self.Items.append(self.listitem)
        elif name == 'naam':
            if self.inNaamContent:
                self.inNaamContent = 0
                self.listitem.append(self.Naam)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('naam'):
                        h = self.searchlist['naam'].upper()
                        s = self.Naam.upper()
                        if s.find(h) >= 0:
                            self.SelectThis = 1
        elif name == 'straat':
            if self.inStraatContent:
                self.inStraatContent = 0
                self.listitem.append(self.Straat)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('straat'):
                        h = self.searchlist['straat'].upper()
                        s = self.Straat.upper()
                        if s.find(h) >= 0:
                            self.SelectThis = 1
        elif name == 'postcode':
            if self.inPostcodeContent:
                self.inPostcodeContent = 0
                self.listitem.append(self.Postcode)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('postcode'):
                        h = self.searchlist['postcode'].upper()
                        s = self.Postcode.upper()
                        if s.find(h) >= 0:
                            self.SelectThis = 1
        elif name == 'plaats':
            if self.inPlaatsContent:
                self.inPlaatsContent = 0
                self.listitem.append(self.Plaats)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('plaats'):
                        h = self.searchlist['plaats'].upper()
                        s = self.Plaats.upper()
                        if s.find(h) >= 0:
                            self.SelectThis = 1
        elif name == 'telefoon':
            if self.inTelefoonContent:
                self.inTelefoonContent = 0
                self.listitem.append(self.Telefoon)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('telefoon'):
                        h = self.searchlist['telefoon'].upper()
                        s = self.Telefoon.upper()
                        if s.find(h) >= 0:
                            self.SelectThis = 1
        elif name == 'geboren':
            if self.inGeborenContent:
                self.inGeborenContent = 0
                self.listitem.append(self.Geboren)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('geboren'):
                        h = self.searchlist['geboren'].upper()
                        s = self.Geboren.upper()
                        if s.find(h) >= 0:
                            self.SelectThis = 1
        elif name == 'email':
            if self.inEmailContent:
                self.inEmailContent = 0
                self.listitem.append(self.Email)
                if self.searchlist == None:
                    self.SelectThis = 1
                else:
                    if self.searchlist.has_key('email'):
                        h = self.searchlist['email'].upper()
                        s = self.Email.upper()
                        if s.find(h) >= 0:
                            self.SelectThis = 1

class NawList:
    "lijst met gegevens van een selectie van items"
    def __init__(self, fn, element_list, selection_criteria=None):
        # bij gebruik search als 2e arg ipv filenaam
        #~ if search == "school":
            #~ self.fn = xmlpad + "Adressen_school.xml" # naam van het xml bestand
        #~ if search == "ans":
            #~ self.fn = xmlpad + "Adressen_ans.xml" # naam van het xml bestand
        self.fn = fn
        self.fno = fn + ".old"
        self.Items = []
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = SearchNaw(element_list, selection_criteria)
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fn)
        if len(dh.Items) > 0:
            for x in dh.Items:
                items = []
                for y in x:
                    items.append(y.encode('ISO-8859-1'))
                self.Items.append(items)

class Naw:
    "lijst alle gegevens van een bepaald item"
    def __init__(self, fn, id):
        self.Id = id
        # bij gebruik search als 2e arg ipv filenaam
        #~ if search == "school":
            #~ self.fn = xmlpad + "Adressen_school.xml" # naam van het xml bestand
        #~ if search == "ans":
            #~ self.fn = xmlpad + "Adressen_ans.xml" # naam van het xml bestand
        self.fn = fn
        self.fno = fn + ".old"
        self.found = 0
        self.Naam = ""
        self.Straat = ""
        self.Postcode = ""
        self.Plaats = ""
        self.Telefoon = ""
        self.Geboren = ""
        self.Email = ""
        if self.Id == "0" or self.Id == 0:
            parser = make_parser()
            parser.setFeature(feature_namespaces, 0)
            dh = FindLaatste()
            parser.setContentHandler(dh)
            parser.parse(self.fn)
            self.Id = str(int(dh.Id) + 1)

    def read(self):
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = FindNaw(str(self.Id))
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fn)
        self.found = dh.itemfound
        if self.found:
            if self.Naam != None:
                self.Naam = dh.Naam.encode('ISO-8859-1')
            if self.Straat != None:
                self.Straat = dh.Straat.encode('ISO-8859-1')
            if self.Postcode != None:
                self.Postcode = dh.Postcode.encode('ISO-8859-1')
            if self.Plaats != None:
                self.Plaats = dh.Plaats.encode('ISO-8859-1')
            if self.Telefoon != None:
                self.Telefoon = dh.Telefoon.encode('ISO-8859-1')
            if self.Geboren != None:
                self.Geboren = dh.Geboren.encode('ISO-8859-1')
            if self.Email != None:
                self.Email = dh.Email.encode('ISO-8859-1')

    def write(self):
        from shutil import copyfile
        copyfile(self.fn,self.fno)
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = UpdateNaw(self)
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fno)

    def wijzigNaam(self,Naam):
        self.Naam = Naam

    def wijzigStraat(self,Straat):
        self.Straat = Straat

    def wijzigPostcode(self,Postcode):
        self.Postcode = Postcode

    def wijzigPlaats(self,Plaats):
        self.Plaats = Plaats

    def wijzigTelefoon(self,Telefoon):
        self.Telefoon = Telefoon

    def wijzigGeboren(self,Geboren):
        self.Geboren = Geboren

    def wijzigEmail(self,Email):
        self.Email = Email

class LaatsteNaw:
    "lijst alle gegevens van een bepaald item"
    def __init__(self,search):
        if search == "school":
            self.fn = xmlpad + "Adressen_school.xml" # naam van het xml bestand
        if search == "ans":
            self.fn = xmlpad + "Adressen_ans.xml" # naam van het xml bestand
        # Create a parser
        parser = make_parser()
        # Tell the parser we are not interested in XML namespaces
        parser.setFeature(feature_namespaces, 0)
        # Create the handler
        dh = FindLaatste()
        # Tell the parser to use our handler
        parser.setContentHandler(dh)
        # Parse the input
        parser.parse(self.fn)
        self.Id = dh.Id

if __name__ == '__main__':
    test = 1
    ih = Naw("ans", test)
    ih.read()
    if ih.found:
        print 'Naam: ' + ih.Naam
        print 'Straat: ' + ih.Straat
        print 'Postcode: ' + ih.Postcode
        print 'Plaats: ' + ih.Plaats
        print 'Telefoon: ' + ih.Telefoon
#        print 'Geboren: ' + ih.Geboren
        print 'Email: ' + ih.Email
##        ih.wijzigTelefoon("3601125")
##        ih.write()
    lh = NawList("ans",['naam','straat','postcode','plaats','telefoon','email','geboren'])
    for x in lh.Items:
        print x
##    lh = Naw("ans",0)
##    print "nieuw: " + str(lh.Id)
##    ih = Naw("ans",lh.Id)
##    ih.wijzigNaam("Naam")
##    ih.wijzigStraat("Straat")
##    ih.wijzigPostcode("9999XX")
##    ih.wijzigPlaats("Woonplaats")
##    ih.wijzigTelefoon("1234567890")
###    ih.wijzigGeboren("99999999")
##    ih.wijzigEmail("jan@ergens.com")
##    ih.write()
